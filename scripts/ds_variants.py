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


def spec_presente(spec, example):
    """¿El ejemplo muestra ese estado? Presencia: sale algún elemento que case. Atributo o clase: algún elemento que case
    (o el raíz, sin target) lo lleva con ese valor."""
    els = elementos(example)
    if not els:
        return False
    tops = {t["start"] for t in top_level(example)}
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


def analyze(sch, example, classes_in_css, fid_cfg=None):
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
    bases = _bases(slug, used)
    pattern = fid_cfg.get("modifierPattern") or ".{base}--{value}"
    mods_cfg = (fid_cfg.get("modifiers") or {}).get(slug) or {}
    ignore_values = {v.lower() for v in (cov.get("values") if cov.get("values") is not None else DEFAULT_IGNORE_VALUES)}
    comp_raw = (cov.get("components") or {}).get(slug) or []
    comp_ignore = {str(x).lower() for x in comp_raw}  # lista, o {"eje=valor": "motivo"}
    razones = {str(k).lower(): str(v) for k, v in comp_raw.items() if v} if isinstance(comp_raw, dict) else {}
    props = _props(sch, cov, fid_cfg, mods_cfg)

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
            return "class", known[:1]
        if prop["kind"] == "bool":
            for n in (prop["name"], prop["fname"]):
                tok_ = DEDUCE_BOOL.get(slug_value(n))
                if tok_:
                    ctl = [e for e in elementos(example) if e["tag"] in CONTROLES]
                    if len(ctl) == 1:  # con más de un control no se deduce
                        return "spec", {"target": ctl[0]["tag"], "add": parse_add(tok_), "presence": False}
        return "unknown", []

    # Dónde vive cada clase: en el elemento raíz del ejemplo, en un elemento interno, o no se sabe (la clase no sale en el
    # ejemplo y no sigue la convención de modificador). ds-fidelity acepta cualquier selector existente; la galería solo
    # puede aplicar a la raíz lo que es de la raíz.
    raiz = _root(slug, example, bases)
    root_tokens, child_tokens = set(), set()
    for t in top_level(example):  # los elementos de primer nivel (variantes puestas en fila) cuentan como raíz
        root_tokens |= set(_class_tokens(t["open"]))
    if raiz:
        dentro = example[raiz["start"] + len(raiz["open"]):raiz["end"]]
        for m in re.finditer(r"<([a-zA-Z][\w-]*)([^>]*)>", dentro):
            child_tokens |= set(_class_tokens(m.group(2)))

    def un_ambito(c):
        bloque = re.split(r"--|__", c)[0]
        if c in root_tokens:
            return "root"
        if "__" in c or c in child_tokens:
            return "child"  # un elemento (BEM) o una clase que solo sale dentro del raíz
        if bloque in root_tokens:
            return "root"
        if bloque in child_tokens:
            return "child"  # modificador de un elemento interno (el bloque solo sale dentro del raíz)
        if bloque in bases or c.startswith(("is-", "has-")):
            return "root"
        return "unknown"

    def ambito(cl):
        r = {un_ambito(c) for c in cl}
        return "child" if "child" in r else "unknown" if "unknown" in r else "root"

    items = []
    for p in props:
        resolved = {v: resolve(p, v) for v in p["values"]}
        mods = {c for v, (k, cl) in resolved.items() if k == "class" and str(v) != p["default"] for c in cl if c not in bases}
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
                    it["state"] = "visible" if spec_presente(cl, example) else "missing"
                items.append(it)
                continue
            cl = cl
            it = {"axis": p["name"], "kind": p["kind"], "value": v, "label": label, "classes": cl,
                  "default": (p["kind"] == "enum" and v == p["default"]), "mods": sorted(mods),
                  "scope": ambito(cl) if kind == "class" else "root"}
            if it["scope"] == "child" and p["kind"] == "enum" and cl:
                bloques = {re.split(r"--", c)[0] for c in cl}
                if len(bloques) == 1 and next(iter(bloques)) in child_tokens:
                    it["target"] = next(iter(bloques))  # el modificador es de ese elemento interno, no de la raíz
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
    for t in tops:
        if set(_class_tokens(t["open"])) & set(bases):
            return t
    return None


def _with_classes(open_tag, remove, add):
    toks = _class_tokens(open_tag)
    new = [t for t in toks if t not in remove] + [c for c in add if c not in toks]
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


def gallery(sch, example, analysis, pairs=None):
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
    for it in analysis["items"]:
        if it["state"] == "ignored":
            continue
        if it.get("spec"):
            if root is None:
                no_gen.append(it["label"])
            else:
                spec_ejes.setdefault((it["axis"], it["kind"]), []).append(it)
            continue
        if root is None or it["state"] == "unchecked" or (not it["classes"] and not it["default"]):
            no_gen.append(it["label"])
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
    if root is None:
        return None, no_gen
    text = example[root["start"]:root["end"]]
    open_tag = root["open"]
    body = text[len(open_tag):]
    k, secciones = 0, []
    for (axis, kind), its in por_eje.items():
        celdas = []
        for it in its[:MAX_CELLS_PER_AXIS]:
            opts = [(it["label"], [] if it["default"] else it["classes"])] if kind == "enum" else [
                (f"{axis}=true", it["classes"]), (f"{axis}=false", [])]
            for etiqueta, add in opts:
                if it.get("target"):
                    celdas.append((etiqueta, _unique_ids(_en_hijo(text, it["target"], set(it["mods"]), add), k)))
                else:
                    tag = _with_classes(open_tag, set(it["mods"]) | (set(it["classes"]) if kind == "bool" else set()), add)
                    celdas.append((etiqueta, _unique_ids(tag + body, k)))
                k += 1
        if len(its) > MAX_CELLS_PER_AXIS:
            no_gen.append(f"{axis}: {len(its) - MAX_CELLS_PER_AXIS} valores más")
        secciones.append((axis if kind == "enum" else f"{axis} (con y sin)", celdas))
    for it in child_bool:
        con = _unique_ids(text, k); k += 1
        sin = _unique_ids(sin_elementos_con_clase(text, set(it["classes"])), k); k += 1
        secciones.append((f"{it['axis']} (con y sin)", [(f"{it['axis']}=true", con), (f"{it['axis']}=false", sin)]))
    for (axis, kind), its in spec_ejes.items():
        todos = [i["spec"] for i in its if not i["spec"]["presence"]]
        celdas = []
        for it in its[:MAX_CELLS_PER_AXIS]:
            sp = it["spec"]
            donde = sp["target"] or "el elemento raíz"
            if kind == "enum":
                if sp["presence"]:
                    no_gen.append(f"{it['label']} (una variante de un eje no puede ser «presence»)")
                    continue
                if it["default"]:
                    h = sin_spec(text, todos)
                else:
                    h, ok = aplicar_spec(text, sp, quitar=todos)
                    if not ok:
                        no_gen.append(f"{it['label']} (el elemento «{donde}» no sale en el ejemplo)")
                        continue
                celdas.append((it["label"], _unique_ids(h, k))); k += 1
            else:
                if sp["presence"]:
                    if not spec_presente(sp, text):
                        no_gen.append(f"{it['label']} (el elemento «{donde}» no sale en el ejemplo)")
                        continue
                    con, sin = text, sin_presencia(text, sp["target"])
                else:
                    con, ok = aplicar_spec(text, sp)
                    if not ok:
                        no_gen.append(f"{it['label']} (el elemento «{donde}» no sale en el ejemplo)")
                        continue
                    sin = sin_spec(text, [sp])
                celdas.append((f"{axis}=true", _unique_ids(con, k))); k += 1
                celdas.append((f"{axis}=false", _unique_ids(sin, k))); k += 1
        if celdas:
            secciones.append((axis if kind == "enum" else f"{axis} (con y sin)", celdas))
    combos = combinaciones(analysis, pairs)
    if combos:
        todas = {c for it in analysis["items"] if it["state"] != "ignored" for c in it["classes"]} | {c for it in analysis["items"] for c in it["mods"]}
        celdas = []
        for ordenadas, etiqueta, peor in combos:
            tag = _with_classes(open_tag, todas, ordenadas)
            marca = f' <b style="color:#b00020">· {str(peor).replace(".", ",")}:1, por debajo de AA</b>' if peor is not None else ""
            celdas.append((etiqueta + marca, _unique_ids(tag + body, k)))
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
    nota = ("La galería clona el elemento raíz del ejemplo y solo cambia sus clases" + (" y atributos" if spec_ejes else "") + ": una variante que necesita otro marcado "
            "(otro contenido, otro icono) puede verse incompleta; si es el caso, añádela al ejemplo de código.")
    if analysis.get("ignored_reasons"):
        nota = ("No se pintan por su naturaleza (declarado en coverageIgnore): "
                + "; ".join(f"{l}: {r}" for l, r in analysis["ignored_reasons"]) + ". " + nota)
    if no_gen:
        nota = "No se han podido pintar (sin clase conocida en el contrato ni en el CSS): " + ", ".join(no_gen) + ". " + nota
    out.append('<p class="ds-gallery__note" style="font:13px/1.5 system-ui,sans-serif;color:#4a4a4a;max-width:75ch">' + nota + "</p>")
    out.append("</div>")
    return "\n".join(out), no_gen


def lista_faltantes(analysis):
    """Texto de la vista cuando no se puede generar ninguna celda: qué variantes de Figma no salen en el ejemplo."""
    if not analysis:
        return ""
    partes = []
    if analysis.get("ignored_reasons"):
        partes.append("No se pintan por su naturaleza: " + "; ".join(f"{l}: {r}" for l, r in analysis["ignored_reasons"]) + ".")
    if analysis["missing"]:
        partes.append("Variantes de Figma que no salen en el ejemplo: " + ", ".join(analysis["missing"]) + ".")
    if analysis["unchecked"]:
        partes.append("Sin clase conocida (no se puede comprobar): " + ", ".join(analysis["unchecked"]) + ".")
    return " ".join(partes)
