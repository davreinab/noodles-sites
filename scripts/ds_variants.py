#!/usr/bin/env python3
"""ds_variants — qué variantes del contrato salen en el «Ejemplo de código», y la galería que las muestra todas.

Módulo compartido (no se ejecuta solo): lo importan ds-fidelity.py (aviso variant-not-in-example) y
ds-library.py (nota de cobertura en la ficha y variante «Todas las variantes» de la library). Una sola lógica
para que el aviso y lo que se ve no puedan discrepar. Sin dependencias (stdlib).

Qué cuenta como variante: cada valor de cada propiedad `enum` de `api.props`, y cada propiedad `boolean`
(que no sea un estado). Qué clase la representa en el HTML, por orden:
  1. `code.classByProp[propiedad][valor]`, si el contrato ya lo trae (no hace falta escribirlo: se respeta lo
     que haya, y «(automático…)» o «:last-child» cuentan como no aplicables);
  2. `modifiers` de ds-fidelity.config.json para ese componente: ahí se declara lo que no se deduce, sin tocar
     ningún archivo generado (`{"slug": {"propiedad": {"valor": ".clase"}}}`, para las booleanas el valor es «true»);
  3. la convención `.<base>--<valor>` (modifierPattern), si esa clase existe en el CSS o en el ejemplo.
Si ninguna da una clase, la variante queda «sin comprobar»: no se sabe qué buscar, y no se inventa.
El valor por defecto no lleva modificador: cuenta como visible si el ejemplo tiene un elemento base sin
ninguno de los modificadores de ese eje.
"""
import re
from html.parser import HTMLParser

DEFAULT_IGNORE_VALUES = ["hover", "focus", "focused", "pressed", "press", "active"]
DEFAULT_EXCLUDE_AXES = ["state", "estado", "device", "divice", "viewport", "breakpoint", "platform", "responsive", "theme", "mode"]
CLASS_LIKE = re.compile(r"^[A-Za-z_][\w-]*(?:\s+[A-Za-z_][\w-]*)*$")
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
MAX_CELLS_PER_AXIS = 12
MAX_COMBOS = 24


def slug_value(v):
    s = re.sub(r"[^\w\s/-]", "", str(v), flags=re.U).strip().lower()
    s = re.sub(r"\s*/\s*", "-", s)
    s = re.sub(r"[\s_]+", "-", s)
    return re.sub(r"-{2,}", "-", s).strip("-")


def css_classes(css):
    """Todas las clases que aparecen como selector en un CSS (sin entrar en el detalle de cada regla)."""
    return set(re.findall(r"\.([A-Za-z_][\w-]*)", re.sub(r"/\*.*?\*/", "", css or "", flags=re.S)))


def _class_tokens(attrs):
    return [t for c in re.findall(r'class\s*=\s*"([^"]*)"', attrs or "") for t in c.split()]


def elements(example):
    """Cada etiqueta de apertura del ejemplo con sus clases: [(tag, [clases])]."""
    return [(m.group(1), _class_tokens(m.group(2))) for m in re.finditer(r"<([a-zA-Z][\w-]*)([^>]*)>", example or "")]


class _Top(HTMLParser):
    """Elementos de primer nivel del ejemplo, con su posición exacta en el texto."""

    def __init__(self, text):
        super().__init__(convert_charrefs=False)
        self.text = text
        self.lines = [0]
        for ln in text.split("\n")[:-1]:
            self.lines.append(self.lines[-1] + len(ln) + 1)
        self.depth, self.cur, self.tops = 0, None, []

    def _off(self):
        l, c = self.getpos()
        return self.lines[l - 1] + c

    def handle_starttag(self, tag, attrs):
        st = self.get_starttag_text() or ""
        if self.depth == 0:
            self.cur = {"tag": tag, "start": self._off(), "open": st}
            if tag in VOID:
                self.cur["end"] = self.cur["start"] + len(st)
                self.tops.append(self.cur); self.cur = None
                return
        if tag not in VOID:
            self.depth += 1

    def handle_startendtag(self, tag, attrs):
        st = self.get_starttag_text() or ""
        if self.depth == 0:
            s = self._off()
            self.tops.append({"tag": tag, "start": s, "end": s + len(st), "open": st})

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        self.depth = max(0, self.depth - 1)
        if self.depth == 0 and self.cur is not None:
            s = self._off()
            gt = self.text.find(">", s)
            self.cur["end"] = (gt + 1) if gt >= 0 else s
            self.tops.append(self.cur); self.cur = None


class _Spans(HTMLParser):
    """Posición de cada elemento (a cualquier profundidad) que lleva alguna de las clases pedidas."""

    def __init__(self, text, classes):
        super().__init__(convert_charrefs=False)
        self.text, self.classes, self.stack, self.spans = text, set(classes), [], []
        self.lines = [0]
        for ln in text.split("\n")[:-1]:
            self.lines.append(self.lines[-1] + len(ln) + 1)

    def _off(self):
        l, c = self.getpos()
        return self.lines[l - 1] + c

    def handle_starttag(self, tag, attrs):
        st = self.get_starttag_text() or ""
        hit = bool(set(_class_tokens(st)) & self.classes)
        if tag in VOID:
            if hit:
                s0 = self._off()
                self.spans.append((s0, s0 + len(st)))
            return
        self.stack.append((tag, self._off(), hit))

    def handle_startendtag(self, tag, attrs):
        st = self.get_starttag_text() or ""
        if set(_class_tokens(st)) & self.classes:
            s0 = self._off()
            self.spans.append((s0, s0 + len(st)))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                _, start, hit = self.stack.pop(i)
                if hit:
                    gt = self.text.find(">", self._off())
                    self.spans.append((start, gt + 1 if gt >= 0 else self._off()))
                break


def sin_elementos_con_clase(html_text, classes):
    """El HTML sin los elementos (con todo su contenido) que llevan alguna de esas clases."""
    p = _Spans(html_text, classes)
    try:
        p.feed(html_text); p.close()
    except Exception:
        return html_text
    out, pos = [], 0
    for a, b in sorted(p.spans):
        if a < pos:
            continue  # anidado en uno ya quitado
        out.append(html_text[pos:a])
        pos = b
    out.append(html_text[pos:])
    return "".join(out)


class _Elems(HTMLParser):
    """Todos los elementos del ejemplo (a cualquier profundidad), en orden de documento, con sus atributos y su posición."""

    def __init__(self, text):
        super().__init__(convert_charrefs=False)
        self.text, self.stack, self.els = text, [], []
        self.lines = [0]
        for ln in text.split("\n")[:-1]:
            self.lines.append(self.lines[-1] + len(ln) + 1)

    def _off(self):
        l, c = self.getpos()
        return self.lines[l - 1] + c

    def _new(self, tag, attrs):
        st = self.get_starttag_text() or ""
        el = {"tag": tag.lower(), "attrs": {k.lower(): v for k, v in attrs}, "start": self._off(), "open": st}
        el["open_end"] = el["start"] + len(st)
        self.els.append(el)
        return el

    def handle_starttag(self, tag, attrs):
        el = self._new(tag, attrs)
        if tag in VOID:
            el["end"] = el["open_end"]
        else:
            self.stack.append(el)

    def handle_startendtag(self, tag, attrs):
        el = self._new(tag, attrs)
        el["end"] = el["open_end"]

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag.lower():
                el = self.stack.pop(i)
                gt = self.text.find(">", self._off())
                el["end"] = gt + 1 if gt >= 0 else self._off()
                break


def elementos(text):
    p = _Elems(text or "")
    try:
        p.feed(text or ""); p.close()
    except Exception:
        return []
    return [e for e in p.els if "end" in e]


SELECTOR_SIMPLE = re.compile(r"[\w-]*(?:\.[\w-]+|#[\w-]+|\[[^\]]+\])*")


def coincide(el, selector):
    """¿El elemento casa con un selector CSS simple (etiqueta, .clase, #id, [atributo] o [atributo="valor"], sin combinadores)?"""
    sel = (selector or "").strip()
    if not sel or not SELECTOR_SIMPLE.fullmatch(sel):
        return False
    tag = re.match(r"[\w-]*", sel).group(0)
    if tag and tag.lower() != el["tag"]:
        return False
    for c in re.findall(r"\.([\w-]+)", re.sub(r"\[[^\]]*\]", "", sel)):
        if c not in (el["attrs"].get("class") or "").split():
            return False
    for i in re.findall(r"#([\w-]+)", re.sub(r"\[[^\]]*\]", "", sel)):
        if el["attrs"].get("id") != i:
            return False
    for a in re.findall(r"\[[^\]]+\]", sel):
        n, v = parse_attr(a)
        if n not in el["attrs"] or (v is not None and el["attrs"][n] != v):
            return False
    return True


ATTR_RE = re.compile(r"\[\s*([\w:-]+)\s*(?:=\s*(?:\"([^\"]*)\"|'([^']*)'|([^\]\s]*)))?\s*\]")


def parse_attr(token):
    """'[disabled]' → ('disabled', None); '[aria-invalid="true"]' → ('aria-invalid', 'true')."""
    m = ATTR_RE.fullmatch(token.strip())
    if not m:
        return None, None
    v = next((g for g in m.groups()[1:] if g is not None), None)
    return m.group(1).lower(), v


def parse_add(text):
    """'.a [disabled] [data-state="x"]' → {'classes': ['a'], 'attrs': [('disabled', None), ('data-state', 'x')]}"""
    out = {"classes": [], "attrs": []}
    for t in re.findall(r'\[[^\]]+\]|\.[\w-]+', str(text or "")):
        if t.startswith("."):
            out["classes"].append(t[1:])
        else:
            n, v = parse_attr(t)
            if n:
                out["attrs"].append((n, v))
    return out


def modificador_spec(raw):
    """Un valor de `modifiers.<slug>.<prop>.<valor>` que no es una clase del raíz: {'target', 'add', 'presence'} o None.
    Admite '[atributo]' / '[atributo="valor"]' (atributo en el raíz) y {'target', 'add'} o {'target', 'presence': true}."""
    if isinstance(raw, str) and raw.strip().startswith("["):
        add = parse_add(raw)
        return {"target": None, "add": add, "presence": False} if add["attrs"] else None
    if isinstance(raw, dict) and (raw.get("target") or raw.get("add")):
        return {"target": (str(raw["target"]).strip() or None) if raw.get("target") else None,
                "add": parse_add(raw.get("add") or ""), "presence": bool(raw.get("presence"))}
    return None


def _poner_attr(open_tag, nombre, valor):
    pat = re.compile(r'(\s)%s(?:\s*=\s*(?:"[^"]*"|\'[^\']*\'|[^\s>]+))?(?=[\s/>])' % re.escape(nombre), re.I)
    nuevo = (' %s="%s"' % (nombre, valor)) if valor is not None else (" " + nombre)
    if pat.search(open_tag):
        return pat.sub(lambda m: nuevo, open_tag, count=1)
    return re.sub(r"\s*/?>$", lambda m: nuevo + m.group(0).lstrip(), open_tag, count=1) if re.search(r"\s*/?>$", open_tag) else open_tag


def _quitar_attr(open_tag, nombre):
    return re.sub(r'\s%s(?:\s*=\s*(?:"[^"]*"|\'[^\']*\'|[^\s>]+))?(?=[\s/>])' % re.escape(nombre), "", open_tag, flags=re.I)


def _destino(text, target):
    """El primer elemento del texto que casa con `target` (sin target: el primero, que es el raíz)."""
    els = elementos(text)
    if not target:
        return els[0] if els else None
    return next((e for e in els if coincide(e, target)), None)


def _editar_apertura(text, target, fn):
    el = _destino(text, target)
    if not el:
        return text, False
    return text[:el["start"]] + fn(el["open"]) + text[el["open_end"]:], True


def aplicar_spec(text, spec, quitar=()):
    """El texto del raíz con el estado de `spec` aplicado al elemento que toque y sin los atributos/clases de `quitar`
    (los de los demás valores del mismo eje: no puede haber dos data-state). Devuelve (texto, aplicado)."""
    def fn(tag):
        for q in quitar:
            for n, _ in q["add"]["attrs"]:
                tag = _quitar_attr(tag, n)
        cls = spec["add"]["classes"]
        quitar_cls = {c for q in quitar for c in q["add"]["classes"]}
        if cls or quitar_cls:
            tag = _with_classes(tag, quitar_cls, cls)
        for n, v in spec["add"]["attrs"]:
            tag = _poner_attr(tag, n, v)
        return tag
    return _editar_apertura(text, spec["target"], fn)


def sin_spec(text, specs):
    """El texto del raíz sin los atributos/clases de esos estados (el valor «apagado» de un eje o de una booleana)."""
    def fn(tag):
        for q in specs:
            for n, _ in q["add"]["attrs"]:
                tag = _quitar_attr(tag, n)
        cls = {c for q in specs for c in q["add"]["classes"]}
        return _with_classes(tag, cls, []) if cls else tag
    out = text
    for t in {q["target"] for q in specs}:
        out, _ = _editar_apertura(out, t, fn)
    return out


def sin_presencia(text, target):
    """El texto sin los elementos que casan con `target` (y todo lo que llevan dentro)."""
    els = [e for e in elementos(text) if coincide(e, target) and e["start"] > 0]
    out, pos = [], 0
    for e in sorted(els, key=lambda e: e["start"]):
        if e["start"] < pos:
            continue
        out.append(text[pos:e["start"]])
        pos = e["end"]
    out.append(text[pos:])
    return "".join(out)


def spec_presente(spec, example, slug=None):
    """¿El ejemplo muestra ese estado? Presencia: sale algún elemento que case. Atributo o clase: algún elemento que case
    (o, sin target, alguna muestra: un elemento de primer nivel o uno con el data-ds del componente, aunque el ejemplo
    lo envuelva en un contenedor de maquetación) lo lleva con ese valor."""
    els = elementos(example)
    if not els:
        return False
    tops = {t["start"] for t in top_level(example)}
    tops |= {e["start"] for e in els if e["attrs"].get("data-ds") and (slug is None or e["attrs"].get("data-ds") == slug)}
    cand = [e for e in els if (coincide(e, spec["target"]) if spec["target"] else e["start"] in tops)]
    if spec["presence"]:
        return bool(cand)
    for e in cand:
        ok = all(n in e["attrs"] and (v is None or e["attrs"][n] == v) for n, v in spec["add"]["attrs"])
        ok = ok and all(c in (e["attrs"].get("class") or "").split() for c in spec["add"]["classes"])
        if ok:
            return True
    return False


# Booleanas que se deducen solas cuando el ejemplo tiene un único control de formulario.
DEDUCE_BOOL = {"disabled": '[disabled]', "error": '[aria-invalid="true"]', "invalid": '[aria-invalid="true"]', "required": "[required]"}
CONTROLES = ("input", "select", "textarea", "button")


def top_level(example):
    p = _Top(example or "")
    try:
        p.feed(example or ""); p.close()
    except Exception:
        return []
    return [t for t in p.tops if "end" in t]


def _bases(slug, tokens):
    simples = [c for c in tokens if "--" not in c]
    propias = [c for c in simples if c == slug or c.startswith(slug + "-") or slug.startswith(c)]
    out = []
    for c in (propias or simples):
        if c not in out:
            out.append(c)
    return out


def _props(sch, cov, fid_cfg, mods_cfg=None):
    api = sch.get("api") or {}
    ignore_axes = {a.lower() for a in (fid_cfg.get("excludeAxes") or DEFAULT_EXCLUDE_AXES)} | {a.lower() for a in cov.get("axes") or []}
    out = []
    for p in api.get("props") or []:
        name, figma = p.get("name"), str(p.get("figma") or "")
        fname = figma.split("#")[0]
        axis_cfg = (mods_cfg or {}).get(name) or (mods_cfg or {}).get(fname)
        # un eje excluido por defecto (p. ej. «state») entra si el proyecto lo declara con un atributo o un elemento interno
        declarado = isinstance(axis_cfg, dict) and any(modificador_spec(v) for v in axis_cfg.values())
        if not name or ((name.lower() in ignore_axes or fname.lower() in ignore_axes) and not declarado):
            continue
        if p.get("type") == "enum" and p.get("values"):
            values = [str(v) for v in p["values"]]
            default = str(p["default"]) if p.get("default") is not None else values[0]
            out.append({"name": name, "fname": fname, "kind": "enum", "values": values, "default": default})
        elif p.get("type") == "boolean" and not figma.startswith(("state=", "estado=")):
            out.append({"name": name, "fname": fname, "kind": "bool", "values": ["true"], "default": None})
    return out


def analyze(sch, example, classes_in_css, fid_cfg=None, css_rules=None):
    """Cobertura de variantes del contrato en el ejemplo.

    Devuelve {"items": [...], "visible": n, "total": n, "missing": [etiquetas], "unchecked": [etiquetas],
              "ignored": n, "prop_classes": {...}} o None si el ejemplo está vacío o no hay variantes."""
    fid_cfg = fid_cfg or {}
    cov = fid_cfg.get("coverageIgnore") or {}
    slug = (sch.get("meta") or {}).get("slug", "")
    if not (example or "").strip():
        return None
    code = sch.get("code") or {}
    cbp = code.get("classByProp") if isinstance(code.get("classByProp"), dict) else {}
    els = elements(example)
    used = []
    for _, toks in els:
        for t in toks:
            if t not in used:
                used.append(t)
    # la pieza base sale de los elementos marcados con data-ds=<slug> (las muestras), no de todas las clases del ejemplo: un contenedor de la
    # muestra con un nombre parecido al slug no es la base. Sin raíz marcada, vale lo de antes.
    raiz_toks = []
    for e in elementos(example):
        if e["attrs"].get("data-ds") == slug:
            raiz_toks += [t for t in _class_tokens(e["open"]) if t not in raiz_toks]
    bases = _bases(slug, raiz_toks if raiz_toks else used)
    pattern = fid_cfg.get("modifierPattern") or ".{base}--{value}"
    mods_cfg = (fid_cfg.get("modifiers") or {}).get(slug) or {}
    ignore_values = {v.lower() for v in (cov.get("values") if cov.get("values") is not None else DEFAULT_IGNORE_VALUES)}
    comp_raw = (cov.get("components") or {}).get(slug) or []
    comp_ignore = {str(x).lower() for x in comp_raw}  # lista, o {"eje=valor": "motivo"}
    razones = {str(k).lower(): str(v) for k, v in comp_raw.items() if v} if isinstance(comp_raw, dict) else {}
    props = _props(sch, cov, fid_cfg, mods_cfg)

    conv_classes = set()

    def resolve(prop, value):
        """('class', [clases]) | ('na', []) | ('unknown', [])."""
        m = cbp.get(prop["name"])
        if m is None:
            m = cbp.get(prop["fname"])
        keys = [str(value)] + (["yes"] if str(value) == "true" else [])
        axis_cfg0 = mods_cfg.get(prop["name"]) or mods_cfg.get(prop["fname"])
        if isinstance(axis_cfg0, dict):
            for k in keys:
                if k in axis_cfg0:
                    sp = modificador_spec(axis_cfg0[k])
                    if sp:
                        return "spec", sp
        if isinstance(m, dict):
            for k in keys:
                if k in m:
                    raw = m[k]
                    if isinstance(raw, str) and CLASS_LIKE.match(raw.strip()):
                        return "class", raw.split()
                    return "na", []
        axis_cfg = mods_cfg.get(prop["name"]) or mods_cfg.get(prop["fname"])
        if isinstance(axis_cfg, dict) and str(value) in axis_cfg:
            return "class", [t.lstrip(".") for t in str(axis_cfg[str(value)]).split()]
        if isinstance(axis_cfg, str):
            return "class", [axis_cfg.format(base=bases[0] if bases else slug, axis=slug_value(prop["name"]), value=slug_value(value)).lstrip(".")]
        cands = []
        names = [slug_value(value)] if prop["kind"] == "enum" else [slug_value(prop["name"]), slug_value(prop["fname"])]
        for b in bases or [slug]:
            for n in names:
                if n:
                    c = pattern.format(base=b, axis=slug_value(prop["name"]), value=n).lstrip(".")
                    if c not in cands:
                        cands.append(c)
        known = [c for c in cands if c in classes_in_css or c in used]
        if known:
            conv_classes.update(known[:1])
            return "class", known[:1]
        if prop["kind"] == "bool":
            deduce = {**DEDUCE_BOOL, **{str(k).lower(): v for k, v in (fid_cfg.get("deduceBooleans") or {}).items()}}
            for n in (prop["name"], prop["fname"]):
                tok_ = deduce.get(slug_value(n))
                if tok_:
                    ctl = [e for e in elementos(example) if e["tag"] in CONTROLES]
                    if len(ctl) == 1:  # con más de un control no se deduce
                        return "spec", {"target": ctl[0]["tag"], "add": parse_add(tok_), "presence": False}
        return "unknown", []

    # Dónde vive cada clase, sin mirar cómo se llama: (1) en el HTML del ejemplo (en el raíz o dentro de él), (2) por los otros
    # valores de su mismo eje, que sí salen en el ejemplo, y (3) si no sale en ningún sitio, por cómo las reglas del CSS la
    # combinan con otras clases. ds-fidelity acepta cualquier selector existente; la galería solo puede aplicar a la raíz lo
    # que es de la raíz.
    raiz = _root(slug, example, bases)
    root_tokens, child_tokens = set(), set()
    for t in top_level(example):  # los elementos de primer nivel (variantes puestas en fila) cuentan como raíz
        root_tokens |= set(_class_tokens(t["open"]))
    todos_els = elementos(example)
    muestras_ = [(t["start"], t["end"]) for t in top_level(example)]
    for e in todos_els:  # cada elemento con el data-ds del componente es una muestra más, aunque esté anidado
        if e["attrs"].get("data-ds") == slug:
            root_tokens |= set(_class_tokens(e["open"]))
            muestras_.append((e["start"], e["end"]))
    if raiz:
        muestras_.append((raiz["start"], raiz["end"]))
    for a_, b_ in set(muestras_):  # lo que hay dentro de cualquier muestra, no solo de la primera, es de un elemento interno
        for e in todos_els:
            if a_ < e["start"] < b_:
                child_tokens |= set(_class_tokens(e["open"]))
    child_tokens -= root_tokens
    directos = set()  # clases de los hijos directos del raíz
    if raiz:
        hijos = [e for e in elementos(example) if raiz["start"] < e["start"] < raiz["end"]]
        for e in hijos:
            if not any(o is not e and o["start"] > raiz["start"] and o["start"] < e["start"] and o["end"] >= e["end"] for o in hijos):
                directos |= set(_class_tokens(e["open"]))

    def por_css(c):
        """Evidencia del CSS para una clase que el ejemplo no usa: ('root', None) | ('child', clase_destino | None) | None."""
        if not css_rules:
            return None
        hijo = None
        for sel, _ in css_rules:
            for alt in sel.split(","):
                partes = [re.findall(r"\.([\w-]+)", re.sub(r":not\([^)]*\)|\[[^\]]*\]", "", x)) for x in re.split(r"\s*[>+~]\s*|\s+", alt.strip()) if x]
                for i, cl_ in enumerate(partes):
                    if c not in cl_:
                        continue
                    otras = set(cl_) - {c}
                    if otras & root_tokens:
                        return "root", None  # `.base.c`: la clase se añade a la misma pieza que la raíz
                    k = next(iter(sorted(otras & child_tokens)), None)
                    if k:
                        hijo = hijo or ("child", k)
                    elif i < len(partes) - 1 and any(set(x) & directos for x in partes[i + 1:]):
                        return "root", None  # `.c .hijo` con un hijo directo del raíz que sí sale en el ejemplo: la clase va en el raíz
                    elif i == len(partes) - 1 and any(set(x) & root_tokens for x in partes[:i]):
                        hijo = hijo or ("child", None)  # `.raiz .c`: es de algo que está dentro del raíz
        return hijo

    def clasificar(p, resolved, v, cl):
        """(ámbito, clase destino) de la variante `v` del eje `p`: 'root', 'child' o 'unknown'.
        Por cada clase manda, en este orden: dónde sale en el ejemplo; las reglas del CSS; las demás clases de su eje que sí
        salen en el ejemplo; y, si la configuración la puso con la convención `modifierPattern`, la pieza base."""
        if not cl:
            return "root", None
        vecinas = {c for w, (k_, cls_) in resolved.items() if k_ == "class" and w != v for c in cls_}
        res = []
        for c in cl:
            if c in root_tokens:
                res.append(("root", None))
            elif c in child_tokens:
                res.append(("child", c))
            elif por_css(c):
                res.append(por_css(c))
            elif vecinas & root_tokens:
                res.append(("root", None))
            elif vecinas & child_tokens:
                res.append(("child", sorted(vecinas & child_tokens)[0]))
            elif c in conv_classes:
                res.append(("root", None))
            else:
                res.append(("unknown", None))
        ambitos = {r[0] for r in res}
        if "child" in ambitos:
            return "child", next((r[1] for r in res if r[0] == "child" and r[1]), None)
        if "unknown" in ambitos:
            return "unknown", None
        return "root", None

    items = []
    for p in props:
        resolved = {v: resolve(p, v) for v in p["values"]}
        mods = {c for v, (k, cl) in resolved.items() if k == "class" and str(v) != p["default"] for c in cl if c not in bases}
        # lo que la galería quita de la raíz antes de poner el valor de la celda: las clases de TODOS los valores del eje (también las del
        # valor por defecto), salvo las de la pieza base. Así la celda sale bien sea cual sea la variante con la que está escrito el ejemplo.
        quitar = {c for v, (k, cl) in resolved.items() if k == "class" for c in cl if c not in bases}
        for v in p["values"]:
            kind, cl = resolved[v]
            label = f"{p['name']}={v}"
            if kind != "spec" and p["kind"] == "enum" and str(v) == p["default"] and any(k == "spec" for k, _ in resolved.values()):
                kind, cl = "spec", {"target": None, "add": {"classes": [], "attrs": []}, "presence": False}  # el valor por defecto de un eje con atributos: sin ellos
            if kind == "spec":
                it = {"axis": p["name"], "kind": p["kind"], "value": v, "label": label, "classes": [], "spec": cl,
                      "default": (p["kind"] == "enum" and v == p["default"]), "mods": [], "scope": "root"}
                if label.lower() in comp_ignore or v.lower() in ignore_values:
                    it["state"] = "ignored"
                elif it["default"]:
                    it["state"] = "visible"
                else:
                    it["state"] = "visible" if spec_presente(cl, example, slug) else "missing"
                items.append(it)
                continue
            cl = cl
            it = {"axis": p["name"], "kind": p["kind"], "value": v, "label": label, "classes": cl,
                  "default": (p["kind"] == "enum" and v == p["default"]), "mods": sorted(mods),
                  "quitar": sorted(quitar), "scope": "root"}
            if kind == "class":
                it["scope"], destino = clasificar(p, resolved, v, cl)
                if it["scope"] == "child" and p["kind"] == "enum" and destino:
                    it["target"] = destino  # el modificador es de ese elemento interno, no de la raíz
            if label.lower() in comp_ignore or v.lower() in ignore_values or kind == "na":
                it["state"] = "ignored"
            elif it["default"]:
                ok = any(set(toks) & set(bases) and not (set(toks) & mods) for _, toks in els)
                it["state"] = "visible" if ok else "missing"
            elif kind == "unknown":
                it["state"] = "unchecked"
            else:
                it["state"] = "visible" if any(c in used for c in cl) else "missing"
            items.append(it)
    if not items:
        return None
    vis = [i for i in items if i["state"] == "visible"]
    mis = [i for i in items if i["state"] == "missing"]
    return {"items": items, "visible": len(vis), "total": len(vis) + len(mis), "missing": [i["label"] for i in mis],
            "unchecked": [i["label"] for i in items if i["state"] == "unchecked"],
            "ignored": sum(1 for i in items if i["state"] == "ignored"), "bases": bases,
            "ignored_reasons": [(i["label"], razones[i["label"].lower()]) for i in items if i["state"] == "ignored" and i["label"].lower() in razones]}


# ───────────────────────────── galería generada ─────────────────────────────
def _root(slug, example, bases):
    """El elemento que se clona: el de primer nivel con data-ds=<slug>; si el ejemplo no lo marca, el primero que lleve una clase base."""
    tops = top_level(example)
    for t in tops:
        if re.search(r"""data-ds\s*=\s*["']%s["']""" % re.escape(slug), t["open"]):
            return t
    # el elemento que lleva data-ds=<slug> aunque esté anidado (el ejemplo lo envuelve en un contenedor de maquetación)
    for e in elementos(example):
        if e["attrs"].get("data-ds") == slug:
            return {"tag": e["tag"], "start": e["start"], "end": e["end"], "open": e["open"]}
    for t in tops:
        if set(_class_tokens(t["open"])) & set(bases):
            return t
    return None


def _with_classes(open_tag, remove, add):
    toks = _class_tokens(open_tag)
    quedan = [t for t in toks if t not in remove]
    new = quedan + [c for c in add if c not in quedan]
    cls = " ".join(new)
    if re.search(r'class\s*=\s*"[^"]*"', open_tag):
        return re.sub(r'class\s*=\s*"[^"]*"', 'class="%s"' % cls, open_tag, count=1)
    return re.sub(r"^<([a-zA-Z][\w-]*)", r'<\1 class="%s"' % cls, open_tag, count=1)


def _en_hijo(text, block, remove, add):
    """El elemento raíz con las clases cambiadas en el primer elemento interno que lleva la clase `block`."""
    primero = re.match(r"<[a-zA-Z][\w-]*[^>]*>", text)
    ini = primero.end() if primero else 0
    for m in re.finditer(r"<[a-zA-Z][\w-]*[^>]*>", text[ini:]):
        tag = m.group(0)
        if block in _class_tokens(tag):
            return text[:ini + m.start()] + _with_classes(tag, remove, add) + text[ini + m.end():]
    return text


def _fija_color(clase, css_rules):
    """¿Alguna regla del CSS con esta clase en su último compuesto pone color de texto o de fondo? Así se distingue un contenedor que
    cambia cómo se ve la variante (una superficie oscura) de uno que solo coloca (una fila, una columna)."""
    for sel, cuerpo in css_rules or []:
        for una in sel.split(","):
            ultimo = re.split(r"[\s>+~]+", una.strip())[-1]
            if ":" in ultimo or not re.search(r"\.%s(?![\w-])" % re.escape(clase), ultimo):
                continue
            if re.search(r"(^|;)\s*(background(-color)?|color)\s*:", cuerpo):
                return True
    return False


def _contexto(example, rango, css_rules=None, excluir=None):
    """(apertura, cierre) de los elementos que envuelven a la muestra `rango` = (inicio, fin) y que fijan color o fondo, de fuera adentro y
    sin sus `id`: ese contenedor (un bloque de fondo oscuro, una superficie) forma parte de cómo se ve la variante, y sin él un texto claro
    se pinta sobre el blanco de la vista previa. Cada celda lleva el de SU muestra: las variantes de un ejemplo pueden estar repartidas en
    muestras con contenedores distintos. Los que solo colocan (filas, columnas, rejillas) no se llevan. Sin reglas de CSS, no hay contexto."""
    if not rango or not css_rules:
        return "", ""
    a, b = rango
    # `excluir`: el elemento que la celda ya clona (la raíz); ni él ni lo que lleva dentro cuentan como contenedor
    anc = sorted((e for e in elementos(example) if e["start"] < a and e["end"] > b
                  and not (excluir and e["start"] >= excluir[0] and e["end"] <= excluir[1])
                  and any(_fija_color(c, css_rules) for c in _class_tokens(e["open"]))), key=lambda e: e["start"])
    pre = "".join(re.sub(r'\s+id\s*=\s*("[^"]*"|\'[^\']*\')', "", e["open"]) for e in anc)
    post = "".join("</%s>" % e["tag"] for e in reversed(anc))
    return pre, post


def _unique_ids(html_text, k):
    ids = set(re.findall(r'\bid\s*=\s*"([^"]+)"', html_text))
    if not ids or k == 0:
        return html_text
    sfx = f"-v{k}"
    out = re.sub(r'(\bid\s*=\s*")([^"]+)(")', lambda m: m.group(1) + (m.group(2) + sfx if m.group(2) in ids else m.group(2)) + m.group(3), html_text)
    for attr in ("for", "aria-controls", "aria-labelledby", "aria-describedby", "aria-owns", "aria-activedescendant", "list"):
        out = re.sub(r'(\b%s\s*=\s*")([^"]*)(")' % attr,
                     lambda m: m.group(1) + " ".join((t + sfx if t in ids else t) for t in m.group(2).split()) + m.group(3), out)
    return re.sub(r'(href\s*=\s*"#)([^"]+)(")', lambda m: m.group(1) + (m.group(2) + sfx if m.group(2) in ids else m.group(2)) + m.group(3), out)


def combinaciones(analysis, pairs):
    """Combinaciones de ejes que el CSS escribe como compuesto (`.badge--promo.badge--negative`) y que miden contraste.

    La galería por eje nunca las enseña, y son justo donde falla AA. Devuelve [(clases, etiqueta, peor_ratio | None)],
    primero las que no llegan a AA; la peor razón es la del peor par (cualquier tema) de ese compuesto."""
    if not analysis or not pairs:
        return []
    axis_of, label_of = {}, {}
    for it in analysis["items"]:
        if it["state"] == "ignored" or it["default"] or it.get("scope", "root") != "root":
            continue
        for c in it["classes"]:
            axis_of.setdefault(c, it["axis"])
            label_of.setdefault(c, it["label"])
    bases = set(analysis["bases"])
    found = {}
    for pr in pairs:
        classes = set(re.findall(r"\.([\w-]+)", str(pr.get("state") or "").split(":")[0]))
        mods = frozenset(c for c in classes if c not in bases)
        if len({axis_of.get(c) for c in mods if c in axis_of}) < 2 or not all(c in axis_of for c in mods):
            continue
        e = found.setdefault(mods, {"worst": None})
        if not pr.get("pass") and (e["worst"] is None or pr["ratio"] < e["worst"]):
            e["worst"] = pr["ratio"]
    out = []
    for mods, e in found.items():
        ordered = sorted(mods, key=lambda c: (axis_of[c], c))
        out.append((ordered, " + ".join(label_of[c] for c in ordered), e["worst"]))
    out.sort(key=lambda x: (x[2] is None, x[2] or 0, x[1]))
    return out[:MAX_COMBOS]


def agrupa_motivos(pares):
    """[(etiqueta, motivo)] → ['eje=a/b/c (motivo)', …]: las variantes de un mismo eje con el mismo motivo van en una sola entrada."""
    grupos = {}
    for et, mot in pares:
        eje, _, val = et.partition("=")
        grupos.setdefault((eje, mot), []).append(val)
    return [f"{eje}={'/'.join(v for v in vals if v)} ({mot})" if any(vals) else f"{eje} ({mot})" for (eje, mot), vals in grupos.items()]


def nota_no_pintadas(no_gen):
    """La única redacción de la lista de variantes que la galería no pudo pintar: cada una con su motivo, separadas por comas
    (los motivos no llevan comas) y terminada en punto, igual que el resto de notas de la ficha."""
    return ("No se han podido pintar: " + ", ".join(no_gen) + ".") if no_gen else ""


def gallery(sch, example, analysis, pairs=None, css_rules=None):
    """(html | None, no_generables) — la rejilla «Todas las variantes» y las variantes que no se pudieron pintar.

    Se recorre cada eje por separado (no el producto de todos) y, aparte, las combinaciones que el CSS escribe como compuesto y miden contraste (las que no llegan a AA, primero). Cada celda es el elemento raíz del ejemplo con las
    clases de ese valor y sin las de los demás valores del eje; las booleanas van «con / sin»."""
    if not analysis:
        return None, []
    slug = (sch.get("meta") or {}).get("slug", "")
    bases = analysis["bases"]
    root = _root(slug, example, bases)
    por_eje, no_gen = {}, []
    child_bool, spec_ejes = [], {}
    por_eje_n, comparten = {}, {}
    for it in analysis["items"]:
        if it["state"] != "ignored":
            por_eje_n[it["axis"]] = por_eje_n.get(it["axis"], 0) + 1
            if it["kind"] == "enum" and it["classes"] and not it.get("spec"):
                comparten.setdefault((it["axis"], tuple(it["classes"])), []).append(it["label"])
    for it in analysis["items"]:
        if it["state"] == "ignored":
            continue
        if it["kind"] == "enum" and it["default"] and por_eje_n.get(it["axis"]) == 1:
            continue  # un eje con un solo valor no tiene nada que variar: el ejemplo ya es ese valor
        grupo = comparten.get((it["axis"], tuple(it["classes"]))) or []
        if it["kind"] == "enum" and len(grupo) > 1 and not it.get("spec"):
            if grupo[0] == it["label"]:  # una sola entrada por grupo de valores que comparten clase
                vals = "/".join(x.split("=", 1)[1] for x in grupo)
                no_gen.append(f"{it['axis']}={vals} (comparten la clase .{it['classes'][0]}: por clase no se distinguen; declara un selector o un atributo para cada valor)")
            continue
        if it.get("spec"):
            spec_ejes.setdefault((it["axis"], it["kind"]), []).append(it)
            continue
        if root is None:
            no_gen.append(f"{it['label']} (el ejemplo no tiene un elemento raíz identificable: márcalo con data-ds=\"{slug}\")")
            continue
        if it["state"] == "unchecked" or (not it["classes"] and not it["default"]):
            no_gen.append(f"{it['label']} (no hay clase ni atributo declarados para ella: declara su selector en modifiers)")
            continue
        scope = it.get("scope", "root")
        if scope == "child":
            if it.get("target"):
                por_eje.setdefault((it["axis"], it["kind"]), []).append(it)  # se aplica al elemento interno
            elif it["kind"] == "bool" and it["state"] == "visible":
                child_bool.append(it)  # con = el ejemplo tal cual; sin = el ejemplo sin los elementos con esa clase
            else:
                no_gen.append(f"{it['label']} (su clase es de un elemento interno: añade ese elemento al ejemplo)")
            continue
        if scope == "unknown":
            no_gen.append(f"{it['label']} (no se sabe a qué elemento va su clase: añádela al ejemplo)")
            continue
        por_eje.setdefault((it["axis"], it["kind"]), []).append(it)
    if root is None and not spec_ejes:
        return None, no_gen
    # Sin una raíz identificable (el ejemplo va dentro de un contenedor sin data-ds ni clase base) las variantes con
    # atributo o presencia que dicen su elemento (`target`) se pintan sobre el ejemplo entero; las demás se listan.
    text = example[root["start"]:root["end"]] if root else example
    open_tag = root["open"] if root else ""
    body = text[len(open_tag):] if root else ""
    muestras = {(t["start"], t["end"]) for t in top_level(example)}
    muestras |= {(e["start"], e["end"]) for e in elementos(example) if e["attrs"].get("data-ds") == slug}
    raiz_rango = (root["start"], root["end"]) if root else (0, len(example))

    def envolver(h, rango):
        pre, post = _contexto(example, rango, css_rules, raiz_rango if root else None)
        return pre + h + post

    def rango_valor(it):
        """Dónde enseña el ejemplo esta variante: el primer elemento que lleva alguna de sus clases. De ahí sale el contenedor de la celda
        (la variante clara está en un bloque oscuro). Si no sale en ningún sitio, el de la raíz."""
        busca = set(it.get("classes") or [])
        if busca:
            for e in elementos(example):
                if busca & set(_class_tokens(e["open"])):
                    return (e["start"], e["end"])
        return raiz_rango

    def base_de(it):
        """El texto de la muestra donde sale lo que la variante cambia (una clase de un elemento interno puede estar solo en
        otra muestra que la raíz); si no sale en ninguna, la raíz."""
        busca = set(it.get("classes") or []) | ({it["target"]} if it.get("target") else set())
        if not busca:
            return text, raiz_rango
        orden = ([(root["start"], root["end"])] if root else []) + sorted(muestras)
        for a_, b_ in orden:
            for e in elementos(example[a_:b_])[1:]:
                if busca & set(_class_tokens(e["open"])):
                    return example[a_:b_], (a_, b_)
        return text, raiz_rango
    def base_spec(sp):
        """La muestra donde sale el elemento de un estado por atributo o presencia: la raíz y, si no está en ella, la primera
        otra muestra que lo tenga (un ejemplo con varias muestras puede mostrar cada estado en una distinta)."""
        if not sp["target"]:
            return text, raiz_rango
        orden = [(text, raiz_rango)] + [(example[a_:b_], (a_, b_)) for a_, b_ in sorted(muestras) if not (root and (a_, b_) == (root["start"], root["end"]))]
        return next(((t_, r_) for t_, r_ in orden if _destino(t_, sp["target"])), (text, raiz_rango))
    k, secciones = 0, []
    for (axis, kind), its in por_eje.items():
        celdas = []
        for it in its[:MAX_CELLS_PER_AXIS]:
            opts = [(it["label"], it["classes"])] if kind == "enum" else [
                (f"{axis}=true", it["classes"]), (f"{axis}=false", [])]
            for etiqueta, add in opts:
                if it.get("target"):
                    t_, r_ = base_de(it)
                    celdas.append((etiqueta, envolver(_unique_ids(_en_hijo(t_, it["target"], set(it.get("quitar") or it["mods"]), add), k), r_)))
                else:
                    tag = _with_classes(open_tag, set(it.get("quitar") or it["mods"]) | (set(it["classes"]) if kind == "bool" else set()), add)
                    celdas.append((etiqueta, envolver(_unique_ids(tag + body, k), rango_valor(it))))
                k += 1
        if len(its) > MAX_CELLS_PER_AXIS:
            no_gen.append(f"{axis} ({len(its) - MAX_CELLS_PER_AXIS} valores más: la galería pinta como mucho {MAX_CELLS_PER_AXIS} por propiedad)")
        secciones.append((axis if kind == "enum" else f"{axis} (con y sin)", celdas))
    for it in child_bool:
        t_, r_ = base_de(it)
        con = envolver(_unique_ids(t_, k), r_); k += 1
        sin = envolver(_unique_ids(sin_elementos_con_clase(t_, set(it["classes"])), k), r_); k += 1
        secciones.append((f"{it['axis']} (con y sin)", [(f"{it['axis']}=true", con), (f"{it['axis']}=false", sin)]))
    for (axis, kind), its in spec_ejes.items():
        todos = [i["spec"] for i in its if not i["spec"]["presence"]]
        celdas = []
        for it in its[:MAX_CELLS_PER_AXIS]:
            sp = it["spec"]
            donde = sp["target"] or "el elemento raíz"
            if root is None and not sp["target"]:
                no_gen.append(f"{it['label']} (el ejemplo no tiene un elemento raíz identificable: márcalo con data-ds=\"{slug}\" o declara un target)")
                continue
            if kind == "enum":
                if sp["presence"]:
                    no_gen.append(f"{it['label']} (una variante de un eje no puede ser «presence»)")
                    continue
                if it["default"]:
                    h, r_ = sin_spec(text, todos), raiz_rango
                else:
                    bt, r_ = base_spec(sp)
                    h, ok = aplicar_spec(bt, sp, quitar=todos)
                    if not ok:
                        no_gen.append(f"{it['label']} (el elemento «{donde}» no sale en el ejemplo)")
                        continue
                celdas.append((it["label"], envolver(_unique_ids(h, k), r_))); k += 1
            else:
                bs, r_ = base_spec(sp)
                if sp["presence"]:
                    if not spec_presente(sp, bs):
                        no_gen.append(f"{it['label']} (el elemento «{donde}» no sale en el ejemplo)")
                        continue
                    con, sin = bs, sin_presencia(bs, sp["target"])
                else:
                    con, ok = aplicar_spec(bs, sp)
                    if not ok:
                        no_gen.append(f"{it['label']} (el elemento «{donde}» no sale en el ejemplo)")
                        continue
                    sin = sin_spec(bs, [sp])
                celdas.append((f"{axis}=true", envolver(_unique_ids(con, k), r_))); k += 1
                celdas.append((f"{axis}=false", envolver(_unique_ids(sin, k), r_))); k += 1
        if celdas:
            secciones.append((axis if kind == "enum" else f"{axis} (con y sin)", celdas))
    combos = combinaciones(analysis, pairs) if root else []
    if combos:
        todas = {c for it in analysis["items"] if it["state"] != "ignored" for c in it["classes"]} | {c for it in analysis["items"] for c in it["mods"]}
        celdas = []
        for ordenadas, etiqueta, peor in combos:
            tag = _with_classes(open_tag, todas, ordenadas)
            marca = f' <b style="color:#b00020">· {str(peor).replace(".", ",")}:1, por debajo de AA</b>' if peor is not None else ""
            celdas.append((etiqueta + marca, envolver(_unique_ids(tag + body, k), raiz_rango)))
            k += 1
        secciones.append(("combinaciones que el CSS escribe", celdas))
    if not secciones:
        return None, no_gen
    out = ['<div class="ds-gallery">',
           "<style>.ds-gallery{font:14px/1.4 system-ui,sans-serif;color:#1f1f1f}.ds-gallery h3{font:600 12px/1.3 system-ui,sans-serif;letter-spacing:.1em;text-transform:uppercase;margin:0 0 12px;color:#4a4a4a}"
           ".ds-gallery section{margin:0 0 32px}.ds-gallery__row{display:flex;flex-wrap:wrap;align-items:center;gap:24px 32px}"
           ".ds-gallery figure{margin:0;display:flex;flex-direction:column;gap:8px;align-items:flex-start}.ds-gallery figcaption{font:12px/1.3 ui-monospace,monospace;color:#4a4a4a}"
           ".ds-gallery__stage{padding:8px;min-width:48px;min-height:32px;outline:1px dashed #bebebe;outline-offset:0}</style>"]
    for titulo, celdas in secciones:
        out.append(f"<section><h3>{titulo}</h3><div class=\"ds-gallery__row\">")
        for etiqueta, h in celdas:
            out.append(f"<figure><div class=\"ds-gallery__stage\">{h}</div><figcaption>{etiqueta}</figcaption></figure>")
        out.append("</div></section>")
    nota = ("La galería clona el elemento raíz del ejemplo, con los contenedores que le dan color o fondo, y solo cambia sus clases" + (" y atributos" if spec_ejes else "") + ": una variante que necesita otro marcado "
            "(otro contenido, otro icono) puede verse incompleta; si es el caso, añádela al ejemplo de código.")
    if analysis.get("ignored_reasons"):
        nota = ("No se pintan por su naturaleza (declarado en coverageIgnore): "
                + ", ".join(agrupa_motivos(analysis["ignored_reasons"])) + ". " + nota)
    if no_gen:
        nota = nota_no_pintadas(no_gen) + " " + nota
    out.append('<p class="ds-gallery__note" style="font:13px/1.5 system-ui,sans-serif;color:#4a4a4a;max-width:75ch">' + nota + "</p>")
    out.append("</div>")
    return "\n".join(out), no_gen


def lista_faltantes(analysis):
    """Texto de la vista cuando no se puede generar ninguna celda: qué variantes de Figma no salen en el ejemplo."""
    if not analysis:
        return ""
    partes = []
    if analysis.get("ignored_reasons"):
        partes.append("No se pintan por su naturaleza: " + ", ".join(agrupa_motivos(analysis["ignored_reasons"])) + ".")
    if analysis["missing"]:
        partes.append("Variantes de Figma que no salen en el ejemplo: " + ", ".join(analysis["missing"]) + ".")
    return " ".join(partes)
