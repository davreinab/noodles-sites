"""ds_contrast — contraste WCAG 2.1 AA del texto de cada componente, calculado desde su CSS.

Módulo compartido (solo stdlib): lo usan ds-fidelity.py (comprobación `contrast-below-aa`) y ds-library.py
(tarjeta «Contraste» de la ficha). No se ejecuta solo.

Por qué desde el CSS: el volcado de Figma dice qué variables usa un componente, pero no cuál va de texto y
cuál de fondo. El CSS sí lo dice, y es lo que llega a las pantallas.

Cómo:
  1. Los estados del componente son los compuestos que su CSS escribe sobre el elemento raíz: `.badge`,
     `.button--promo`, `.button--promo.button--outline:hover`… (clases propias = el slug como
     bloque BEM: `slug`, `slug--*`, `slug__*`).
  2. Para cada estado se aplica la cascada de las reglas cuyo compuesto está contenido en él (más clases y
     pseudoclases = más específica; a igualdad, la que va después): sale su `color` y su `background`.
     Un elemento interno con `color` propio (`.badge .badge__label`) se mide sobre el fondo de su estado.
  3. Los `var(--…)` se resuelven con tokens.css: modo claro (`:root`) y, si hay, oscuro
     (`:root[data-theme="dark"]`). Texto grande (≥ 24 px, o ≥ 18,66 px y peso ≥ 700) pide 3:1; el resto 4,5:1.
  4. Exentos (WCAG 1.4.3): estados deshabilitados. No comprobables: fondo transparente o semitransparente
     (depende de dónde se ponga el componente) o color que no se puede resolver; se cuentan aparte, sin inventar.
  5. (12.27.0) Un elemento interno escrito como regla suelta (`.slug__el { color }`) se mide igual que `.slug .slug__el`. Un componente SIN fondo propio
     no falla: queda como no comprobable y trae una recomendación (`recommend`): sobre qué fondos del propio CSS del proyecto cumple AA y sobre cuáles no
     (`fondos_del_css`, ordenados por cuánto se usan). Lo mismo si el fondo del texto es ambiguo: otro elemento de la pieza tiene fondo propio, o el papel
     lo pinta un `::before`/`::after`. `sin_colores_propios` dice que la pieza solo compone otras (sus textos son los de sus piezas).
"""
import re

CONTRAST_TEXT = 4.5
CONTRAST_LARGE = 3.0


def css_rules(css):
    """[(selector, cuerpo)] de las reglas normales (no @media/@keyframes), en orden."""
    css = re.sub(r"/\*.*?\*/", "", css or "", flags=re.S)
    rules, buf, stack = [], "", []
    for ch in css:
        if ch == "{":
            stack.append(buf.strip()); buf = ""
        elif ch == "}":
            head = stack.pop() if stack else ""
            if head and not head.startswith("@") and not any(h.startswith("@") for h in stack):
                rules.append((head, buf))
            buf = ""
        else:
            buf += ch
    return rules


def declarations(body):
    out = {}
    for part in body.split(";"):
        if ":" in part:
            k, v = part.split(":", 1)
            out[k.strip().lower()] = v.strip()
    return out


def theme_vars(tokens_css):
    """{'light': {--x: valor}, 'dark': {...} o None} desde tokens.css (bloques :root y :root[data-theme=dark])."""
    light, dark = {}, {}
    for sel, body in css_rules(tokens_css):
        s = sel.replace(" ", "")
        target = light if s == ":root" else dark if s in (':root[data-theme="dark"]', ":root[data-theme='dark']", ":root[data-theme=dark]") else None
        if target is None:
            continue
        for k, v in declarations(body).items():
            if k.startswith("--"):
                target[k] = v
    return {"light": light, "dark": ({**light, **dark} if dark else None)}


VAR_RE = re.compile(r"var\(\s*(--[\w-]+)\s*(?:,\s*([^)]+))?\)")


def resolve(value, vars_, depth=0):
    if value is None or depth > 20:
        return None
    m = VAR_RE.search(value)
    while m:
        rep = vars_.get(m.group(1))
        if rep is None:
            rep = m.group(2)
        if rep is None:
            return None
        rep = resolve(rep.strip(), vars_, depth + 1)
        if rep is None:
            return None
        value = value[:m.start()] + rep + value[m.end():]
        m = VAR_RE.search(value)
    return value.strip()


def parse_color(v):
    """(r, g, b, a) o None. Admite #rgb, #rgba, #rrggbb, #rrggbbaa, rgb()/rgba(), transparent, white/black."""
    if not v:
        return None
    v = v.strip().lower().replace("!important", "").strip()
    if v == "transparent":
        return (0, 0, 0, 0.0)
    if v in ("white", "#fff"):
        return (255, 255, 255, 1.0)
    if v == "black":
        return (0, 0, 0, 1.0)
    m = re.fullmatch(r"#([0-9a-f]{3,8})", v)
    if m:
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h)
        if len(h) not in (6, 8):
            return None
        a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)
    m = re.fullmatch(r"rgba?\(\s*([\d.]+)[\s,]+([\d.]+)[\s,]+([\d.]+)(?:[\s,/]+([\d.]+%?))?\s*\)", v)
    if m:
        a = m.group(4)
        a = (float(a[:-1]) / 100 if a and a.endswith("%") else float(a)) if a else 1.0
        return (float(m.group(1)), float(m.group(2)), float(m.group(3)), a)
    return None


COLOR_IN_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)|\btransparent\b|\bwhite\b|\bblack\b")


def first_color(v):
    """El color de un valor de background, aunque sea abreviado («#fff url(…) no-repeat»)."""
    if not v:
        return None
    c = parse_color(v)
    if c is not None:
        return c
    m = COLOR_IN_RE.search(v)
    return parse_color(m.group(0)) if m else None


def decorativo(prop, value):
    """¿Este background pinta un adorno y no el fondo de la caja?

    Una línea pintada con un degradado de tamaño propio («linear-gradient(…) bottom / 100% 2px no-repeat»)
    ocupa una franja, no el fondo sobre el que va el texto. Si se tomara como fondo, saldría «texto negro
    sobre negro». Se ignora y manda el fondo que ya tenía la caja (heredado o el de otra regla)."""
    if prop != "background" or not value or "gradient(" not in value:
        return False
    fuera = re.sub(r"\([^()]*(\([^()]*\)[^()]*)*\)", "()", value)
    return "no-repeat" in fuera or "/" in fuera


def luminance(c):
    def ch(x):
        x = x / 255
        return x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(c[0]) + 0.7152 * ch(c[1]) + 0.0722 * ch(c[2])


def ratio(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def hexcol(c):
    return "#%02x%02x%02x" % tuple(int(round(x)) for x in c[:3])


NOT_RE = re.compile(r":not\(([^)]*)\)")


def compound(part):
    """'.a.b:hover:not(.c)' → (clases, pseudos, clases negadas) o None si no es un compuesto simple de clases.
    Lo que va dentro de :not(...) son clases que el elemento NO debe tener (12.8.3: antes se leían como presentes)."""
    part = part.strip()
    if not part or not re.fullmatch(r"[\w-]*(?:\.[\w-]+|:[\w-]+(?:\([^)]*\))?)+", part):
        return None
    negs = frozenset(c for inner in NOT_RE.findall(part) for c in re.findall(r"\.([\w-]+)", inner))
    rest = NOT_RE.sub("", part)
    classes = frozenset(re.findall(r"\.([\w-]+)", rest))
    pseudos = frozenset(re.findall(r":([\w-]+)", rest))
    return classes, pseudos, negs


def applies(c, state):
    """¿La regla de compuesto c aplica al estado (clases, pseudos)?"""
    return c[0] <= state[0] and c[1] <= state[1] and not (c[2] & state[0])


def spec(*cs):
    return sum(len(c[0]) + len(c[1]) + len(c[2]) for c in cs)


def own(cls, slug):
    return cls == slug or cls.startswith(slug + "--") or cls.startswith(slug + "__")


def px(value, vars_):
    v = resolve(value, vars_)
    if not v:
        return None
    m = re.fullmatch(r"([\d.]+)(px|rem)?", v.strip())
    if not m:
        return None
    n = float(m.group(1))
    return n * 16 if m.group(2) == "rem" else n


def weight(value, vars_):
    v = resolve(value, vars_)
    if not v:
        return None
    return {"normal": 400, "bold": 700}.get(v.strip().lower()) or (int(float(v)) if re.fullmatch(r"[\d.]+", v.strip()) else None)


def _opaco(raw):
    """¿Es un fondo de color sólido (no degradado ni transparente)? Sin resolver variables: basta con que no sea transparente, `none` ni un degradado."""
    return bool(raw) and "gradient(" not in raw and raw.strip().lower() not in ("transparent", "none", "inherit", "unset")


def fondos_del_css(rules, vars_, slug=None):
    """[(etiqueta, color, veces)] de los fondos opacos que el propio CSS del proyecto ya usa como superficie (reglas de una clase sin pseudoclase, sin
    degradados): son los sitios donde un componente sin fondo propio puede acabar. La etiqueta es el token (`--surface-default`) si el valor es una
    variable, y el color si no. `veces` = en cuántas reglas aparece ese color: las superficies de verdad se usan en muchos componentes y las de un
    solo componente (el fondo de un chip) casi en uno; el orden de la recomendación se apoya en eso."""
    vistos, out = {}, []
    for sel, body in rules:
        if ":" in sel and sel.replace(" ", "") not in (":root",):
            continue
        partes = [x for x in sel.split(",") if x.strip()]
        if slug and all(any(own(c, slug) for c in re.findall(r"\.([\w-]+)", x)) for x in partes):
            continue
        d = declarations(body)
        raw = d.get("background") or d.get("background-color")
        if not raw or "gradient(" in raw or decorativo("background", raw):
            continue
        col = parse_color(resolve(raw, vars_))
        if col is None or col[3] < 1:
            continue
        hexv = hexcol(col)
        m = VAR_RE.search(raw)
        etiqueta = m.group(1) if m else hexv
        if hexv not in vistos:
            vistos[hexv] = len(out)
            out.append([col, 1, {etiqueta: 1}])
        else:
            fila = out[vistos[hexv]]
            fila[1] += 1
            fila[2][etiqueta] = fila[2].get(etiqueta, 0) + 1
    # la etiqueta de un color es el token con el que más se escribe (el de superficie, no el de un chip que casualmente es del mismo color)
    return [(max(f[2].items(), key=lambda kv: kv[1])[0], f[0], f[1]) for f in out]


def recomendar(fg, superficies, tam):
    """Sobre qué fondos el color de texto `fg` cumple AA y sobre cuáles no: {need, ok: [...], fail: [...]}."""
    size, w = tam
    large = bool(size and (size >= 24 or (size >= 18.66 and (w or 400) >= 700)))
    need = CONTRAST_LARGE if large else CONTRAST_TEXT
    filas = sorted(((n, ratio(fg, col), et, hexcol(col)) for et, col, n in superficies), reverse=True)  # primero los fondos más usados
    txt = lambda n, r, et, hx: "%s %s (%s:1)" % (et, hx, ("%.2f" % r))
    return {"need": need, "ok": [txt(*x) for x in filas if x[1] >= need], "fail": [txt(*x) for x in filas if x[1] < need]}


def component_pairs(slug, rules, themes):
    """Parejas texto/fondo de un componente. Devuelve dict con pairs, untestable y exempt."""
    base_rules, elem_rules = [], []  # (compuesto, decl, orden) / (compuesto ancestro, simple elemento, decl, orden)
    raiz = (frozenset(), frozenset(), frozenset())  # sin ancestro: una regla `.slug__el` pesa una clase, no dos, y vale en todos los estados
    for order, (sel, body) in enumerate(rules):
        decl = declarations(body)
        for part in sel.split(","):
            bits = part.split()
            if len(bits) == 1:
                c = compound(bits[0])
                if c and any(x == slug or x.startswith(slug + "--") for x in c[0]):
                    base_rules.append((c, decl, order))
                elif c and any(x.startswith(slug + "__") for x in c[0]):
                    # un elemento interno escrito como regla de un solo selector BEM (`.slug__el { color }`): cuenta como `.slug .slug__el`
                    elem_rules.append((raiz, c, decl, order))
            elif len(bits) == 2:
                a, b = compound(bits[0]), compound(bits[1])
                if a and b and any(own(x, slug) for x in a[0]):
                    elem_rules.append((a, b, decl, order))
    # ¿algún elemento interno de la pieza tiene fondo propio? Entonces el fondo de un texto escrito como regla suelta `.slug__el` es ambiguo: puede ir
    # sobre la raíz o dentro de ese elemento (una tarjeta clara dentro de una banda oscura), y medirlo contra la raíz da fallos falsos.
    fondo_interno = any(("background" in d or "background-color" in d) and _opaco(d.get("background") or d.get("background-color"))
                        for _, el, d, _ in elem_rules if el[0] and any(x.startswith(slug + "__") for x in el[0]))
    # elementos cuyo papel lo pinta un pseudoelemento (`.slug__ticket::before { background }`): su fondo tampoco es el de la raíz
    fondo_pseudo = set()
    for sel, body in rules:
        d = declarations(body)
        if not _opaco(d.get("background") or d.get("background-color") or d.get("background-image")):
            continue
        for part in sel.split(","):
            m = re.fullmatch(r"\s*\.([\w-]+)[\w.:()-]*::?(?:before|after)\s*", part)
            if m and m.group(1).startswith(slug + "__"):
                fondo_pseudo.add(m.group(1))
    coloristas = [d for _, d, _ in base_rules] + [d for _, _, d, _ in elem_rules]
    sin_colores = not any(k in ("color", "background", "background-color") for d in coloristas for k in d)
    if not base_rules and not elem_rules:
        return {"pairs": [], "untestable": [], "exempt": 0, "sin_colores_propios": True}

    def cascade(state, applicable):
        """Propiedades que quedan en el estado, incluidas las personalizadas locales (--badge-bg…)."""
        props, local = {}, {}
        for c, decl, order in sorted(applicable, key=lambda r: (spec(r[0]), r[2])):
            if applies(c, state):
                for k, v in decl.items():
                    if k.startswith("--"):
                        local[k] = v
                for k in ("color", "background", "background-color", "font-size", "font-weight"):
                    if k in decl and not decorativo(k, decl[k]):
                        props["background" if k.startswith("background") else k] = decl[k]
        props["_local"] = local
        return props

    # Solo cuentan los estados cuyas reglas propias tocan el color: uno que solo cambia el tamaño
    # (--medium, --l) repite los colores de la base y no aporta otra pareja.
    COLORISH = ("color", "background", "background-color")
    states = []
    for c, decl, _ in base_rules:
        toca = any(k in COLORISH or k.startswith("--") for k in decl)
        c = (c[0] | {slug}, c[1])  # en el HTML el elemento lleva siempre su clase base (button button--primary); sin los :not
        if toca and c not in states:
            states.append(c)
    if not states and elem_rules:
        states.append((frozenset({slug}), frozenset()))  # sin reglas de color en la raíz: el estado por defecto, para medir sus elementos
    pairs, untestable, exempt = [], [], 0
    for theme, theme_vars_ in themes.items():
        if theme_vars_ is None:
            continue
        superficies = fondos_del_css(rules, theme_vars_, slug)
        for st in states:
            name = "".join("." + x for x in sorted(st[0], key=lambda x: (x != slug, x))) + "".join(":" + p for p in sorted(st[1]))
            if any("disabled" in x for x in st[0]) or "disabled" in st[1]:
                exempt += 1
                continue
            p = cascade(st, [(c, d, o) for c, d, o in base_rules])
            local = p.pop("_local")
            vars_ = {**theme_vars_, **local}

            def token_of(raw):
                """El token del DS detrás de un valor, siguiendo las variables locales (--badge-fg → --promo-text-default)."""
                seen = 0
                m = VAR_RE.search(raw or "")
                while m and m.group(1) in local and seen < 10:
                    seen += 1
                    nxt = VAR_RE.search(local[m.group(1)])
                    if not nxt:
                        break
                    m = nxt
                return m.group(1) if m else None
            targets = [(None, p)]
            # Elementos internos: por cada elemento, la cascada de TODAS sus reglas que aplican en este estado
            # (12.8.3: antes cada regla se medía suelta y una general ganaba a la específica que la pisa).
            por_elemento, sueltas = {}, set()
            for anc, el, decl, order in elem_rules:
                if applies(anc, st):
                    por_elemento.setdefault((el[0], el[1], el[2]), []).append((spec(anc, el), order, decl))
                    if anc is raiz:
                        sueltas.add((el[0], el[1], el[2]))
            for el, reglas in por_elemento.items():
                q, propio, ev = dict(p), {}, dict(vars_)
                for _, _, decl in sorted(reglas, key=lambda r: (r[0], r[1])):
                    for k in ("color", "background", "background-color", "font-size", "font-weight"):
                        if k in decl and not decorativo(k, decl[k]):
                            propio["background" if k.startswith("background") else k] = decl[k]
                    for k, v in decl.items():
                        if k.startswith("--"):
                            ev[k] = v
                if "color" not in propio:
                    continue
                q.update(propio)
                if "background" not in propio and ((el in sueltas and fondo_interno) or (set(el[0]) & fondo_pseudo)):
                    q.pop("background", None)
                    q["_ambiguo"] = True  # su fondo depende del elemento de la pieza que lo contenga
                q["_vars"] = ev
                targets.append(("".join("." + x for x in sorted(el[0])) + "".join(":" + y for y in sorted(el[1]))
                                + "".join(f":not(.{x})" for x in sorted(el[2])), q))
            for elem, q in targets:
                if "color" not in q:
                    continue
                vars_t = q.pop("_vars", vars_)
                ambiguo = q.pop("_ambiguo", False)
                where = name + (f" {elem}" if elem else "")
                fg = parse_color(resolve(q.get("color"), vars_t))
                bg_raw = q.get("background")
                bg_val = resolve(bg_raw, vars_t) if bg_raw else None
                bg = first_color(bg_val)
                if fg is None or bg is None or fg[3] < 1 or bg[3] < 1:
                    why = ("el fondo depende del elemento de la pieza que lo contenga (varios tienen fondo propio)" if ambiguo else
                           "sin fondo propio: depende de dónde se ponga" if not bg_raw else
                           "fondo transparente o semitransparente: depende de dónde se ponga" if bg is not None and bg[3] < 1 else
                           "color semitransparente" if fg is not None and fg[3] < 1 else
                           "color que no se puede resolver con tokens.css")
                    nota = {"theme": theme, "state": where, "why": why}
                    sup = fondos_del_css(rules, theme_vars_) if ambiguo else superficies
                    if not bg_raw and fg is not None and fg[3] == 1 and sup:
                        nota["recommend"] = recomendar(fg, sup, (px(q.get("font-size"), vars_t), weight(q.get("font-weight"), vars_t)))
                    untestable.append(nota)
                    continue
                size, w = px(q.get("font-size"), vars_t), weight(q.get("font-weight"), vars_t)
                large = bool(size and (size >= 24 or (size >= 18.66 and (w or 400) >= 700)))
                need = CONTRAST_LARGE if large else CONTRAST_TEXT
                r = ratio(fg, bg)
                pairs.append({"theme": theme, "state": where, "fg": hexcol(fg), "bg": hexcol(bg),
                              "fgVar": token_of(q.get("color")), "bgVar": token_of(bg_raw),
                              "ratio": round(r, 2), "need": need, "large": large, "pass": r >= need})
    # una pareja repetida (mismo estado, tema y colores) cuenta una vez
    seen, uniq = set(), []
    for x in pairs:
        k = (x["theme"], x["state"], x["fg"], x["bg"])
        if k not in seen:
            seen.add(k); uniq.append(x)
    return {"pairs": uniq, "untestable": untestable, "exempt": exempt, "sin_colores_propios": sin_colores}
