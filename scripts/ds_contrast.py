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


def component_pairs(slug, rules, themes):
    """Parejas texto/fondo de un componente. Devuelve dict con pairs, untestable y exempt."""
    base_rules, elem_rules = [], []  # (compuesto, decl, orden) / (compuesto ancestro, simple elemento, decl, orden)
    for order, (sel, body) in enumerate(rules):
        decl = declarations(body)
        for part in sel.split(","):
            bits = part.split()
            if len(bits) == 1:
                c = compound(bits[0])
                if c and any(x == slug or x.startswith(slug + "--") for x in c[0]):
                    base_rules.append((c, decl, order))
            elif len(bits) == 2:
                a, b = compound(bits[0]), compound(bits[1])
                if a and b and any(own(x, slug) for x in a[0]):
                    elem_rules.append((a, b, decl, order))
    if not base_rules:
        return {"pairs": [], "untestable": [], "exempt": 0}

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
    pairs, untestable, exempt = [], [], 0
    for theme, theme_vars_ in themes.items():
        if theme_vars_ is None:
            continue
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
            por_elemento = {}
            for anc, el, decl, order in elem_rules:
                if applies(anc, st):
                    por_elemento.setdefault((el[0], el[1], el[2]), []).append((spec(anc, el), order, decl))
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
                q["_vars"] = ev
                targets.append(("".join("." + x for x in sorted(el[0])) + "".join(":" + y for y in sorted(el[1]))
                                + "".join(f":not(.{x})" for x in sorted(el[2])), q))
            for elem, q in targets:
                if "color" not in q:
                    continue
                vars_t = q.pop("_vars", vars_)
                where = name + (f" {elem}" if elem else "")
                fg = parse_color(resolve(q.get("color"), vars_t))
                bg_raw = q.get("background")
                bg_val = resolve(bg_raw, vars_t) if bg_raw else None
                bg = first_color(bg_val)
                if fg is None or bg is None or fg[3] < 1 or bg[3] < 1:
                    why = ("sin fondo propio: depende de dónde se ponga" if not bg_raw else
                           "fondo transparente o semitransparente: depende de dónde se ponga" if bg is not None and bg[3] < 1 else
                           "color semitransparente" if fg is not None and fg[3] < 1 else
                           "color que no se puede resolver con tokens.css")
                    untestable.append({"theme": theme, "state": where, "why": why})
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
    return {"pairs": uniq, "untestable": untestable, "exempt": exempt}
