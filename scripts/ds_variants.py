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


def _props(sch, cov, fid_cfg):
    api = sch.get("api") or {}
    ignore_axes = {a.lower() for a in (fid_cfg.get("excludeAxes") or DEFAULT_EXCLUDE_AXES)} | {a.lower() for a in cov.get("axes") or []}
    out = []
    for p in api.get("props") or []:
        name, figma = p.get("name"), str(p.get("figma") or "")
        fname = figma.split("#")[0]
        if not name or name.lower() in ignore_axes or fname.lower() in ignore_axes:
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
    comp_ignore = {str(x).lower() for x in ((cov.get("components") or {}).get(slug) or [])}  # lista, o {"eje=valor": "motivo"}
    props = _props(sch, cov, fid_cfg)

    def resolve(prop, value):
        """('class', [clases]) | ('na', []) | ('unknown', [])."""
        m = cbp.get(prop["name"])
        if m is None:
            m = cbp.get(prop["fname"])
        keys = [str(value)] + (["yes"] if str(value) == "true" else [])
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
        return ("class", known[:1]) if known else ("unknown", [])

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
            "ignored": sum(1 for i in items if i["state"] == "ignored"), "bases": bases}


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
    child_bool = []
    for it in analysis["items"]:
        if it["state"] == "ignored":
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
    nota = ("La galería clona el elemento raíz del ejemplo y solo cambia sus clases: una variante que necesita otro marcado "
            "(otro contenido, otro icono) puede verse incompleta; si es el caso, añádela al ejemplo de código.")
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
    if analysis["missing"]:
        partes.append("Variantes de Figma que no salen en el ejemplo: " + ", ".join(analysis["missing"]) + ".")
    if analysis["unchecked"]:
        partes.append("Sin clase conocida (no se puede comprobar): " + ", ".join(analysis["unchecked"]) + ".")
    return " ".join(partes)
