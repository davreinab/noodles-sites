#!/usr/bin/env python3
"""ds-sync — motor determinista del sync del design system: de los volcados de Figma a los artefactos.

Sin dependencias (stdlib, Python 3.8+). Uso, desde la raíz del proyecto:
    python3 scripts/ds-sync.py             # regenera todos los artefactos ⚙️ a partir de design-system/sync/
    python3 scripts/ds-sync.py --dry       # muestra qué generaría y los hallazgos, sin escribir nada
    python3 scripts/ds-sync.py --root .    # raíz del proyecto (por defecto: carpeta padre de scripts/)
    python3 scripts/ds-sync.py --merge     # solo une los trozos de sync/parts/ en los volcados y los valida
    python3 scripts/ds-sync.py --check-dump  # solo valida los volcados: JSON, cortes, IDs repetidos, alias

Trozos (sync/parts/*.json): el MCP corta cada respuesta hacia los 20 KB, así que los scripts de
lectura devuelven trozos de unos 14 KB con su posición (part.offset, part.nextOffset, part.total).
El agente guarda cada trozo tal cual; este script los une de forma determinista en variables.json
y components.json y los borra. La unión es por posición, no por orden de archivo, y se comprueba
que no falte ninguno. Un trozo con offset 0 empieza de cero ese archivo de tokens o esa página.
Cada ejecución normal une primero los trozos que haya y valida el volcado antes de generar nada.

Qué lee (lo escribe el agente tras leer Figma por el MCP oficial; ver design.md § Sync):
    design-system/sync/variables.json    colecciones, modos, variables (valor por modo, alias, scopes,
                                         descripción), text styles y effect styles
    design-system/sync/components.json   páginas y componentes (propiedades completas, ejes de variante,
                                         instancias anidadas, bindings) — salida del script de lectura
    design-system/sync/icons.json        iconos exportados a assets/icons/ (nombre, nodo, archivo). Opcional.

Qué escribe (siempre los mismos artefactos, siempre igual para el mismo volcado):
    tokens/tokens.json · tokens/tokens.css · docs/tokens.md
    schemas/components/<slug>.schema.json · schemas/index.json · schemas/relationships.json
    docs/components/<slug>.md · docs/patterns/<slug>.md — una ficha por contrato: heading, bloque GENERATED
                                            (la PARTE VIVA, que este script sustituye en cada sync) y debajo la
                                            parte de criterio escrita a mano, que se conserva y vive solo ahí:
                                            el schema no la copia, apunta a ella (source.docs). _plantilla.md es
                                            la forma de una ficha nueva y se ignora como contrato.
    docs/components.md y docs/patterns.md — cabecera, «## Índice» (una línea por ficha) y las secciones manuales
                                            (Composición de pantalla, Decisiones recurrentes…). La primera
                                            ejecución tras este cambio migra sola: saca cada sección de ficha
                                            del .md grande a su archivo y deja el índice.
    docs/assets.md · showcase/index.html (secciones GENERATED) · reports/drift-report.json
    agent-manifest.json (lastSync)

Qué NO hace: no lee Figma (eso es del MCP y lo hace el agente), no toca css/components.css,
no escribe la parte de criterio de ningún contrato, no exporta SVG. Si un dato no está en el
volcado, escribe "unknown"; nunca inventa.

Config opcional en scripts/ds-sync.config.json (todo tiene valor por defecto):
    iconFamilyPrefix, themeModes, mediaModes, patternKeywords, unitlessScopes, cssPrefixByCollection,
    primitiveCollections (colecciones de primitivos: sus variables llevan scopes vacíos a propósito),
    fontFamilyMap (nombre de familia de Figma → familia CSS, y peso si el estilo no lo dice),
    brandModes ({"collections": [...], "attribute": "data-brand"}: colecciones cuyos modos son marcas;
    cada modo que no es el por defecto sale en tokens.css como [data-brand="<slug>"] y los contratos
    declaran en api.theming si el componente cambia con la marca)
"""
import argparse
import glob
import hashlib
import html as htmllib
import json
import os
import re
import sys
from datetime import datetime, timezone

DEFAULT_CFG = {
    "iconFamilyPrefix": ["Icon /", "Icon/", "icon/"],
    "themeModes": {"dark": ["Dark", "dark", "Oscuro"]},
    "mediaModes": {"Mobile": "(max-width: 768px)", "Tablet": "(max-width: 1024px)"},
    "patternKeywords": ["pattern", "patron", "patrón", "compuesto", "molecule", "organism"],
    "unitlessScopes": ["OPACITY", "FONT_WEIGHT"],
    "unitlessNameHints": ["weight", "opacity", "z-index", "z/", "layer/"],
    "timeNameHints": ["duration", "motion/duration", "time"],
    "cssPrefixByCollection": {},
    "primitiveCollections": [],
    "fontFamilyMap": {},
    "brandModes": {"collections": [], "attribute": "data-brand"},
    "foundations": {
        "icon-size": ["icon/size", "icon-size"],
        "layer": ["layer/", "z/", "z-index"],
        "motion": ["motion/", "duration", "easing"],
    },
}
# Marca que deja el MCP cuando corta una respuesta («// truncated to 20kb»)
TRUNCATED_RE = re.compile(r"truncated to \d+\s*kb", re.I)
GEN_START, GEN_END = "<!-- ⚙️ GENERATED:start:{} -->", "<!-- ⚙️ GENERATED:end:{} -->"
# Fichas: una por archivo en docs/<carpeta>/<slug>.md. _plantilla.md es la forma de una ficha nueva, no una ficha.
DOCS_DIR = {"component": "components", "pattern": "patterns"}
PLANTILLA = "_plantilla.md"
# Heading de ficha: «### <Nombre>   ⚙️ synced: <fecha>». El heading de la plantilla antigua
# («### <Nombre>   ⚙️ <synced: fecha | manual>») no casa a propósito: no es una ficha.
FICHA_HEADING_RE = re.compile(r"^### (?P<name>.+?)\s{2,}⚙️ synced: (?P<date>\S+)[ \t]*$", re.M)
GEN_BLOCK_RE = re.compile(r"<!-- ⚙️ GENERATED:start:(?P<slug>[^ ]+) -->\n.*?<!-- ⚙️ GENERATED:end:(?P=slug) -->", re.S)


# ────────────────────────────── utilidades ──────────────────────────────
def read(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def read_json(path, default=None):
    t = read(path)
    if t is None:
        return default
    try:
        return json.loads(t)
    except json.JSONDecodeError as e:
        sys.exit(f"[ERROR] {path}: JSON inválido ({e})")


def write(path, text, dry, written):
    if read(path) == text:
        return  # idéntico: no se toca ni se cuenta
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not dry:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
    written.append(os.path.relpath(path))


def write_json(path, obj, dry, written):
    write(path, json.dumps(obj, ensure_ascii=False, indent=2) + "\n", dry, written)


def slug(name):
    s = re.sub(r"[^\w\s/-]", "", name, flags=re.U).strip().lower()
    s = re.sub(r"\s*/\s*", "-", s)
    s = re.sub(r"[\s_]+", "-", s)
    return re.sub(r"-{2,}", "-", s).strip("-")


# --- Nivel 2 de validación: ejecutabilidad ------------------------------------------------
# Que un artefacto esté bien formado no significa que funcione. Antes de escribir el CSS se
# comprueba que un intérprete lo aceptaría: llaves equilibradas, cada declaración con nombre y
# valor, y ninguna variable que apunte a otra que no existe.
# No sustituye a un navegador; corta los errores que sí se pueden ver sin uno.

def check_css(css, definidas_fuera=None):
    """Devuelve una lista de problemas. Vacía = el CSS es ejecutable.

    `definidas_fuera`: variables que el archivo puede usar aunque no las defina, porque vienen
    de otro archivo. tokens.css es autocontenido y no las necesita; components.css sí, porque
    consume las de tokens.css. Sin este parámetro, la comprobación de variables solo es válida
    en archivos autocontenidos."""
    errores = []
    limpio = re.sub(r"/\*.*?\*/", " ", css, flags=re.S)

    # 1 · llaves equilibradas
    profundidad, linea = 0, 1
    for i, ch in enumerate(limpio):
        if ch == "\n":
            linea += 1
        elif ch == "{":
            profundidad += 1
        elif ch == "}":
            profundidad -= 1
            if profundidad < 0:
                errores.append(f"línea {linea}: cierra una llave que nunca se abrió")
                profundidad = 0
    if profundidad:
        errores.append(f"quedan {profundidad} llaves sin cerrar")

    # 2 · cada declaración tiene nombre y valor
    for bloque in re.findall(r"\{([^{}]*)\}", limpio):
        for decl in bloque.split(";"):
            decl = decl.strip()
            if not decl:
                continue
            if ":" not in decl:
                errores.append(f"declaración sin valor: {decl[:60]}")
                continue
            prop, _, val = decl.partition(":")
            if not prop.strip() or not val.strip():
                errores.append(f"declaración incompleta: {decl[:60]}")

    # 3 · ninguna var() apunta a una custom property inexistente
    definidas = set(re.findall(r"(--[\w-]+)\s*:", limpio)) | set(definidas_fuera or ())
    for usada in set(re.findall(r"var\(\s*(--[\w-]+)", limpio)):
        if usada not in definidas:
            errores.append(f"var({usada}) no está definida en ninguna parte del archivo")

    return errores



# --- rastro (ver scripts/activity.py) ------------------------------------------------------
def _rastro(root, action, detail, files=None):
    """Registra lo que este script acaba de ejecutar. Si no se puede, no rompe la ejecución:
    el rastro es una ayuda, no una guarda."""
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from activity import log
        log(root, "script", action, detail, files=files)
    except Exception:
        pass


def css_var(path, prefix=""):
    p = re.sub(r"\s*/\s*", "-", path.strip().lower())
    p = re.sub(r"[\s_]+", "-", p)
    p = re.sub(r"[^a-z0-9-]", "", p)
    p = re.sub(r"-{2,}", "-", p).strip("-")
    return f"--{prefix}{p}" if prefix else f"--{p}"


def rgba_to_css(c):
    r, g, b = (round(float(c.get(k, 0)) * 255) for k in ("r", "g", "b"))
    a = float(c.get("a", 1))
    if a >= 0.999:
        return "#{:02x}{:02x}{:02x}".format(r, g, b)
    return f"rgba({r}, {g}, {b}, {round(a, 3):g})"


# Peso a partir del nombre del estilo. El orden importa: «ExtraBold» antes que «Bold».
FONT_WEIGHTS = [(r"extra\s*-?\s*light|ultra\s*-?\s*light", 200), (r"semi\s*-?\s*bold|demi\s*-?\s*bold", 600),
                (r"extra\s*-?\s*bold|ultra\s*-?\s*bold", 800), (r"thin|hairline", 100), (r"light", 300),
                (r"regular|normal|book|roman", 400), (r"medium", 500), (r"bold", 700), (r"black|heavy", 900)]


def weight_from(text):
    t = (text or "").lower()
    for pat, w in FONT_WEIGHTS:
        if re.search(pat, t):
            return w
    # «Italic» u «Oblique» a secas es la cursiva del peso normal
    return 400 if re.fullmatch(r"\s*(italic|oblique)\s*", t) else None


def fmt_num(n):
    return f"{n:g}" if isinstance(n, (int, float)) else str(n)


def replace_generated(text, section, body):
    """Sustituye lo que hay entre los marcadores GENERATED de una sección. Si no existen, añade al final."""
    s, e = GEN_START.format(section), GEN_END.format(section)
    if s in text and e in text:
        pre, rest = text.split(s, 1)
        _, post = rest.split(e, 1)
        return f"{pre}{s}\n{body.rstrip()}\n{e}{post}"
    return text.rstrip("\n") + f"\n\n{s}\n{body.rstrip()}\n{e}\n"


def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for r in rows:
        out.append("| " + " | ".join(str(c).replace("|", "\\|") for c in r) + " |")
    return "\n".join(out)


# ────────────────────────────── tokens ──────────────────────────────
class Tokens:
    def __init__(self, raw, cfg, synced_at):
        self.cfg, self.synced_at = cfg, synced_at
        self.raw = raw or {}
        self.file_key = self.raw.get("fileKey")
        self.by_id = {}           # variableId → token dict
        self.tokens = []          # lista ordenada
        self.collections = []     # [{name, id, modes:[{modeId,name}], tokens:[...]}]
        self.findings = []
        self.text_styles = self.raw.get("textStyles", []) or []
        self.effect_styles = self.raw.get("effectStyles", []) or []
        self._build()
        self._text_cache = None

    def _text_rows(self):
        """Calcula una sola vez las variables de los estilos de texto (y sus hallazgos)."""
        if self._text_cache is None:
            self._text_cache = self.text_style_css()
            usados = {t["cssVar"]: f"{t['collection']}/{t['path']}" for t in self.tokens}
            for st, rows in self._text_cache:
                for v, _ in rows:
                    if v in usados:
                        self.findings.append(("critical", "tokens-json-vs-css",
                                              f"colisión de nombre CSS {v}: {usados[v]} y el estilo de texto {st.get('name')}"))
                    usados[v] = f"estilo de texto {st.get('name')}"
        return self._text_cache

    def _unitless(self, var):
        name = var["name"].lower()
        scopes = set(var.get("scopes") or [])
        return bool(scopes & set(self.cfg["unitlessScopes"])) or any(h in name for h in self.cfg["unitlessNameHints"])

    def _is_time(self, var):
        name = var["name"].lower()
        return any(h in name for h in self.cfg["timeNameHints"])

    def _build(self):
        for col in self.raw.get("collections", []) or []:
            prefix = self.cfg["cssPrefixByCollection"].get(col.get("name", ""), "")
            entry = {"id": col.get("id"), "name": col.get("name", "unknown"),
                     "modes": col.get("modes") or [{"modeId": "default", "name": "Default"}], "tokens": []}
            for v in col.get("variables", []) or []:
                tok = {
                    "path": v["name"], "cssVar": css_var(v["name"], prefix), "type": v.get("type", "unknown"),
                    "collection": entry["name"], "description": v.get("description") or "",
                    "scopes": v.get("scopes") or [], "codeSyntax": v.get("codeSyntax") or {},
                    "valuesByMode": v.get("valuesByMode") or {}, "id": v.get("id"),
                    "unitless": self._unitless(v), "isTime": self._is_time(v),
                    "source": {"fileKey": self.file_key, "variableId": v.get("id"), "collectionId": col.get("id"),
                               "version": self.raw.get("version"), "syncedAt": self.synced_at},
                }
                if not tok["description"]:
                    self.findings.append(("warning", "missing-variable-description-or-scope",
                                          f"{entry['name']} / {v['name']}: sin descripción"))
                tok["hidden"] = bool(v.get("hiddenFromPublishing"))
                tok["primitiveCollection"] = entry["name"] in (self.cfg.get("primitiveCollections") or [])
                entry["tokens"].append(tok)
                self.tokens.append(tok)
                if v.get("id"):
                    self.by_id[v["id"]] = tok
            self.collections.append(entry)
        self._check_scopes()
        seen = {}
        for t in self.tokens:
            if t["cssVar"] in seen:
                self.findings.append(("critical", "tokens-json-vs-css",
                                      f"colisión de nombre CSS {t['cssVar']}: {seen[t['cssVar']]} y {t['collection']}/{t['path']}"))
            seen[t["cssVar"]] = f"{t['collection']}/{t['path']}"

    # ── marcas (modos de marca) ──
    def brand_collections(self):
        names = set((self.cfg.get("brandModes") or {}).get("collections") or [])
        return [c for c in self.collections if c["name"] in names]

    def brand_info(self):
        """Marcas declaradas en Figma: los modos de las colecciones de marca (el primero es el por defecto)."""
        attr = (self.cfg.get("brandModes") or {}).get("attribute") or "data-brand"
        cols = self.brand_collections()
        brands, seen = [], set()
        for col in cols:
            for i, m in enumerate(col["modes"]):
                s = slug(m["name"])
                if s not in seen:
                    seen.add(s)
                    brands.append({"name": m["name"], "slug": s, "default": i == 0})
        return {"attribute": attr, "collections": [c["name"] for c in cols], "brands": brands}

    def brand_dependent(self, path, depth=0):
        """True si el token (por path) es de una colección de marca o apunta, vía alias, a uno que lo es."""
        names = {c["name"] for c in self.brand_collections()}
        tok = next((t for t in self.tokens if t["path"] == path), None)
        if tok is None or depth > 12:
            return False
        if tok["collection"] in names:
            return True
        for val in tok["valuesByMode"].values():
            if isinstance(val, dict) and val.get("type") == "alias":
                target = self.by_id.get(val.get("id"))
                if target is not None and self.brand_dependent(target["path"], depth + 1):
                    return True
        return False

    def _es_primitivo(self, tok):
        """Un primitivo lleva `scopes: []` a propósito (design.md § Arquitectura de variables de
        color): no se usa directamente. Se reconoce por cualquiera de estas señales: está oculto
        al publicar, su colección está declarada como primitiva en la config, o es la base de
        otros (alguien le apunta) sin apuntar él a nadie."""
        if tok["hidden"] or tok["primitiveCollection"]:
            return True
        es_alias = any(isinstance(v, dict) and v.get("type") == "alias" for v in tok["valuesByMode"].values())
        return tok["id"] in self._referenciados and not es_alias

    def _check_scopes(self):
        self._referenciados = {v.get("id") for t in self.tokens for v in t["valuesByMode"].values()
                               if isinstance(v, dict) and v.get("type") == "alias"}
        for t in self.tokens:
            if t["type"] not in ("COLOR", "FLOAT"):
                continue
            if self._es_primitivo(t):
                # Lo contrario sí es un problema: un primitivo declarado que se puede elegir en un selector.
                # Solo con señal explícita (oculto o colección primitiva), para no adivinar.
                if t["scopes"] and (t["hidden"] or t["primitiveCollection"]):
                    self.findings.append(("warning", "primitive-with-scopes",
                                          f"{t['collection']} / {t['path']}: primitivo con scopes {', '.join(t['scopes'])}; "
                                          f"debería llevar scopes vacíos para que no se use directamente"))
            elif not t["scopes"]:
                self.findings.append(("info", "missing-variable-description-or-scope",
                                      f"{t['collection']} / {t['path']}: sin scopes"))

    def mode_value(self, tok, mode_id, depth=0):
        """Devuelve (css_value, alias_cssvar_or_None, resolved_raw). Sigue aliases hasta 12 niveles."""
        vm = tok["valuesByMode"]
        val = vm.get(mode_id)
        if val is None and vm:
            val = next(iter(vm.values()))
        if val is None:
            return "unknown", None, None
        if isinstance(val, dict) and val.get("type") == "alias":
            target = self.by_id.get(val.get("id"))
            if target is None or depth > 12:
                return "unknown", None, None
            resolved, _, raw = self.mode_value(target, mode_id, depth + 1)
            return f"var({target['cssVar']})", target["cssVar"], raw
        raw = val.get("value") if isinstance(val, dict) else val
        return self.to_css(tok, raw), None, raw

    def to_css(self, tok, raw):
        if raw is None:
            return "unknown"
        if tok["type"] == "COLOR" and isinstance(raw, dict):
            return rgba_to_css(raw)
        if tok["type"] == "FLOAT" and isinstance(raw, (int, float)):
            if tok["isTime"]:
                return f"{fmt_num(raw)}ms"
            return fmt_num(raw) if tok["unitless"] or raw == 0 else f"{fmt_num(raw)}px"
        if tok["type"] == "BOOLEAN":
            return "1" if raw else "0"
        if isinstance(raw, str):
            if re.fullmatch(r"[\w\s,.'\"%-]+", raw) or re.fullmatch(r"[a-z-]+\([\d\s.,%-]*\)", raw):
                return raw  # palabra suelta o función CSS (cubic-bezier, steps…): sin comillas
            return json.dumps(raw)
        return str(raw)

    def default_mode(self, col):
        return col["modes"][0]["modeId"] if col["modes"] else "default"

    def theme_mode(self, col, theme):
        names = {m.lower() for m in self.cfg["themeModes"].get(theme, [])}
        for m in col["modes"]:
            if m["name"].lower() in names:
                return m["modeId"]
        return None

    def media_modes(self, col):
        out = []
        for m in col["modes"]:
            for name, query in self.cfg["mediaModes"].items():
                if m["name"].lower() == name.lower():
                    out.append((m["modeId"], m["name"], query))
        return out

    def elevation_css(self):
        """Effect styles → --elevation-<slug>: box-shadow compuesto."""
        out = []
        for st in self.effect_styles:
            parts = []
            for ef in st.get("effects", []) or []:
                if ef.get("type") not in ("DROP_SHADOW", "INNER_SHADOW") or ef.get("visible") is False:
                    continue
                o = ef.get("offset") or {}
                color = rgba_to_css(ef.get("color") or {"r": 0, "g": 0, "b": 0, "a": 0.2})
                inset = "inset " if ef.get("type") == "INNER_SHADOW" else ""
                parts.append(f"{inset}{fmt_num(o.get('x', 0))}px {fmt_num(o.get('y', 0))}px {fmt_num(ef.get('radius', 0))}px {fmt_num(ef.get('spread', 0))}px {color}")
            name = re.sub(r"^elevation[\s/-]*", "", st.get("name", ""), flags=re.I)
            out.append((css_var("elevation/" + (name or st.get("name", "x"))), ", ".join(parts) or "none", st.get("name", "")))
        return out

    def _bound_var(self, style, prop):
        """Si el estilo liga esta propiedad a una variable que está en el volcado, su var()."""
        b = (style.get("boundVariables") or {}).get(prop)
        b = b[0] if isinstance(b, list) and b else b
        tok = self.by_id.get(b.get("id")) if isinstance(b, dict) else None
        return f"var({tok['cssVar']})" if tok else None

    def text_style_css(self):
        """Estilos de texto → variables --font-<estilo>-{family,size,weight,line-height,letter-spacing}.

        Cada estilo genera las suyas, también los que llevan el breakpoint en el nombre
        («Desktop XL / H1», «Mobile / H1»): se mantienen como estilos separados y es el CSS de
        componentes el que elige cuál usar en cada @media. Así no se adivina qué parte del nombre
        es un breakpoint. Lo que no se puede deducir no se inventa: se omite y queda un hallazgo.
        Devuelve [(estilo, [(var, valor)])] y deja los hallazgos en self.findings."""
        fmap = self.cfg.get("fontFamilyMap") or {}
        out = []
        for st in self.text_styles:
            name = st.get("name") or "x"
            base = css_var("font/" + name)
            rows = []
            fam = st.get("fontFamily")
            mapped = fmap.get(fam) if fam else None
            css_family = (mapped.get("family") if isinstance(mapped, dict) else mapped) or (json.dumps(fam) if fam else None)
            if css_family:
                rows.append((f"{base}-family", css_family))
            size = self._bound_var(st, "fontSize") or (f"{fmt_num(st['fontSize'])}px" if isinstance(st.get("fontSize"), (int, float)) else None)
            if size:
                rows.append((f"{base}-size", size))
            weight = (mapped.get("weight") if isinstance(mapped, dict) else None) or weight_from(st.get("fontStyle")) or weight_from(fam)
            if weight:
                rows.append((f"{base}-weight", str(weight)))
            else:
                self.findings.append(("warning", "text-style-weight-unknown",
                                      f"{name}: no se deduce el peso de «{fam} · {st.get('fontStyle')}»; "
                                      f"decláralo en fontFamilyMap de ds-sync.config.json"))
            if "italic" in (st.get("fontStyle") or "").lower():
                rows.append((f"{base}-style", "italic"))
            lh = st.get("lineHeight") or {}
            if isinstance(lh, dict) and lh.get("unit") == "AUTO":
                rows.append((f"{base}-line-height", "normal"))
            elif isinstance(lh, dict) and isinstance(lh.get("value"), (int, float)):
                rows.append((f"{base}-line-height", f"{fmt_num(lh['value'])}px" if lh.get("unit") == "PIXELS" else fmt_num(round(lh["value"] / 100, 4))))
            ls = st.get("letterSpacing") or {}
            if isinstance(ls, dict) and isinstance(ls.get("value"), (int, float)):
                v = ls["value"]
                rows.append((f"{base}-letter-spacing", "0" if v == 0 else
                             (f"{fmt_num(v)}px" if ls.get("unit") == "PIXELS" else f"{fmt_num(round(v / 100, 4))}em")))
            out.append((st, rows))
        return out

    def foundations_status(self):
        names = " ".join(t["path"].lower() for t in self.tokens)
        status = {}
        for fam, hints in self.cfg["foundations"].items():
            status[fam] = any(h in names for h in hints)
        status["elevation"] = bool(self.effect_styles)
        return status

    # ---- salidas ----
    def tokens_json(self, meta):
        cols = {}
        for col in self.collections:
            entry = {"id": col["id"], "modes": [m["name"] for m in col["modes"]], "tokens": {}}
            for t in col["tokens"]:
                modes = {}
                for m in col["modes"]:
                    css, alias, raw = self.mode_value(t, m["modeId"])
                    modes[m["name"]] = {"value": raw if not alias else None, "alias": alias, "resolvedValue": css}
                d_css, d_alias, d_raw = self.mode_value(t, self.default_mode(col))
                entry["tokens"][t["path"]] = {
                    "path": t["path"], "cssVar": t["cssVar"], "type": t["type"],
                    "value": (f"{{{d_alias}}}" if d_alias else d_raw), "resolvedValue": d_css, "alias": d_alias,
                    "modes": modes, "scopes": t["scopes"], "description": t["description"] or "unknown",
                    "codeSyntax": t["codeSyntax"], "source": t["source"],
                }
            cols[col["name"]] = entry
        return {
            "formatVersion": "1.0.0", "designSystem": meta["designSystem"], "figmaSources": meta["figmaSources"],
            "adoptionMode": meta["adoptionMode"], "structuralStandardsEnforced": meta["structuralStandardsEnforced"],
            "lastSync": self.synced_at, "note": "Espejo generado de Figma por scripts/ds-sync.py. No editar a mano.",
            "tokenContract": {"requiredFields": ["path", "type", "value", "resolvedValue", "alias", "modes", "scopes", "description", "source"],
                              "sourceFields": ["fileKey", "variableId", "collectionId", "version", "syncedAt"]},
            "collections": cols,
            "textStyles": [{"name": s.get("name"), "id": s.get("id"), "fontFamily": s.get("fontFamily"), "fontStyle": s.get("fontStyle"),
                            "fontSize": s.get("fontSize"), "lineHeight": s.get("lineHeight"), "letterSpacing": s.get("letterSpacing"),
                            "cssVars": dict(rows), "description": s.get("description") or "unknown"}
                           for s, rows in self._text_rows()],
            "effectStyles": [{"name": s.get("name"), "id": s.get("id"), "cssVar": v, "value": val}
                             for s, (v, val, _) in zip(self.effect_styles, self.elevation_css())],
            "foundations": self.foundations_status(),
        }

    def tokens_css(self, meta):
        srcs = ", ".join(str(s.get("fileKey") or s.get("url") or s.get("name")) for s in (meta["figmaSources"] or [])) or "unknown"
        L = [f"/* ⚙️ ARCHIVO GENERADO por scripts/ds-sync.py — NO EDITAR A MANO.",
             f"   Design system: {meta['designSystem']} · fileKey: {self.file_key or srcs}",
             f"   Última sync: {self.synced_at} · modo de adopción: {meta['adoptionMode']}",
             "   Se regenera con el protocolo de sync de design.md. */", "", ":root {"]
        dark_lines, media_blocks = [], {}
        for col in self.collections:
            if not col["tokens"]:
                continue
            L.append(f"  /* ---- {col['name']} ---- */")
            dm = self.default_mode(col)
            dark_id = self.theme_mode(col, "dark")
            medias = self.media_modes(col)
            for t in col["tokens"]:
                css, _, _ = self.mode_value(t, dm)
                desc = f" /* {t['description']} */" if t["description"] else ""
                L.append(f"  {t['cssVar']}: {css};{desc}")
                if dark_id and dark_id != dm:
                    dcss, _, _ = self.mode_value(t, dark_id)
                    if dcss != css:
                        dark_lines.append(f"  {t['cssVar']}: {dcss};")
                for mid, mname, query in medias:
                    if mid == dm:
                        continue
                    mcss, _, _ = self.mode_value(t, mid)
                    if mcss != css:
                        media_blocks.setdefault((mname, query), []).append(f"    {t['cssVar']}: {mcss};")
        elev = self.elevation_css()
        if elev:
            L.append("  /* ---- Elevation (effect styles) ---- */")
            L += [f"  {v}: {val}; /* {n} */" for v, val, n in elev]
        texto = self._text_rows()
        if texto:
            L.append("  /* ---- Tipografía (text styles) ---- */")
            for st, rows in texto:
                L.append(f"  /* {st.get('name')} */")
                L += [f"  {v}: {val};" for v, val in rows]
        L.append("}")
        L += ["", ':root[data-theme="dark"] {'] + (dark_lines or ["  /* sin modo Dark en Figma */"]) + ["}"]
        for (mname, query), rows in media_blocks.items():
            L += ["", f"@media {query} {{ /* modo {mname} */", "  :root {"] + rows + ["  }", "}"]
        info = self.brand_info()
        for b in info["brands"]:
            if b["default"]:
                continue
            rows = []
            for col in self.brand_collections():
                mode = next((m for m in col["modes"] if slug(m["name"]) == b["slug"]), None)
                if mode is None:
                    continue
                dm = self.default_mode(col)
                for tk in col["tokens"]:
                    base, _, _ = self.mode_value(tk, dm)
                    val, _, _ = self.mode_value(tk, mode["modeId"])
                    if val != base:
                        rows.append(f"  {tk['cssVar']}: {val};")
            default_name = next((x["name"] for x in info["brands"] if x["default"]), "por defecto")
            L += ["", f'[{info["attribute"]}="{b["slug"]}"] {{ /* marca {b["name"]} · solo lo que difiere de {default_name} · el atributo va en <html> */']
            L += rows or [f"  /* sin diferencias con {default_name} en Figma todavía */"]
            L += ["}"]
        return "\n".join(L) + "\n"

    def tokens_md(self, meta):
        L = ["<!-- ⚙️ ARCHIVO GENERADO por scripts/ds-sync.py — NO EDITAR A MANO. -->", "",
             f"# {meta['designSystem']} · Tokens  ·  _(espejo generado de Figma)_", "",
             f"> Última sync: **{self.synced_at}** · modo de adopción: `{meta['adoptionMode']}` · "
             f"{len(self.tokens)} variables en {len(self.collections)} colecciones · {len(self.text_styles)} text styles · {len(self.effect_styles)} effect styles.",
             "> Cada token se consume en código como `var(--nombre)`. Los alias conservan su referencia y su valor resuelto.", "", "## Índice", ""]
        for col in self.collections:
            L.append(f"- [{col['name']}](#{slug(col['name'])}) · {len(col['tokens'])} tokens · modos: {', '.join(m['name'] for m in col['modes'])}")
        fs = self.foundations_status()
        info = self.brand_info()
        L += (["- [Marcas](#marcas)"] if info["brands"] else []) + ["- [Foundations](#foundations)", "- [Text styles](#text-styles)", ""]
        if info["brands"]:
            L += ["## Marcas", "",
                  f"Modos de marca de las colecciones {', '.join(f'`{c}`' for c in info['collections'])}. La marca por defecto vive en `:root`; "
                  f"cada otra marca se activa con `[{info['attribute']}=\"<slug>\"]` **en `<html>`** y solo redefine lo que cambia. "
                  f"Tiene que ir en `<html>`: las variables de componente se declaran en `:root` apuntando a las semánticas, y una variable CSS resuelve su `var()` donde se declara; en un contenedor interior los componentes no heredarían la marca.", "",
                  md_table(["Marca", "Slug", "Selector CSS", "Por defecto"],
                           [[b["name"], f"`{b['slug']}`", f"`[{info['attribute']}=\"{b['slug']}\"]`", "sí" if b["default"] else "—"] for b in info["brands"]]), ""]
        for col in self.collections:
            L += [f"## {col['name']}", ""]
            headers = ["Token", "CSS", "Tipo"] + [m["name"] for m in col["modes"]] + ["Scopes", "Descripción"]
            rows = []
            for t in col["tokens"]:
                vals = []
                for m in col["modes"]:
                    css, alias, _ = self.mode_value(t, m["modeId"])
                    vals.append(f"`{css}`" if not alias else f"→ `{alias}`")
                rows.append([f"`{t['path']}`", f"`{t['cssVar']}`", t["type"]] + vals + [", ".join(t["scopes"]) or "—", t["description"] or "—"])
            L += [md_table(headers, rows), ""]
        L += ["## Foundations", "",
              md_table(["Familia", "Estado", "Tokens"],
                       [["Icon size (`--icon-size-*`)", "✅ definida" if fs.get("icon-size") else "⬜ pendiente en Figma", "icon/size/*"],
                        ["Layer (`--z-*`)", "✅ definida" if fs.get("layer") else "⬜ pendiente en Figma", "layer/*"],
                        ["Motion (`--motion-*`)", "✅ definida" if fs.get("motion") else "⬜ pendiente en Figma", "motion/*"],
                        ["Elevation (`--elevation-*`)", "✅ definida" if fs.get("elevation") else "⬜ pendiente en Figma (effect styles) o «sin elevación» declarado", "effect styles elevation/*"]]),
              "", "## Text styles", ""]
        if self.text_styles:
            L.append(md_table(["Estilo", "CSS", "Familia", "Peso/estilo", "Tamaño", "Interlineado", "Tracking"],
                              [[s.get("name"), f"`{css_var('font/' + (s.get('name') or 'x'))}-*`", s.get("fontFamily") or "unknown", s.get("fontStyle") or "unknown", fmt_num(s.get("fontSize")) if s.get("fontSize") is not None else "unknown",
                                json.dumps(s.get("lineHeight")) if s.get("lineHeight") else "unknown", json.dumps(s.get("letterSpacing")) if s.get("letterSpacing") else "unknown"] for s in self.text_styles]))
        else:
            L.append("_(sin text styles en el volcado)_")
        return "\n".join(L) + "\n"


# ────────────────────────────── componentes ──────────────────────────────
class Components:
    def __init__(self, raw, cfg, synced_at, ds_root):
        self.cfg, self.synced_at, self.ds_root = cfg, synced_at, ds_root
        self.raw = raw or {}
        self.file_key = self.raw.get("fileKey")
        self.items = []
        self.findings = []
        for page in self.raw.get("pages", []) or []:
            for c in page.get("components", []) or []:
                c = dict(c)
                c["page"] = c.get("page") or page.get("name") or "unknown"
                self.items.append(c)
        self.slugs = {c["name"]: slug(c["name"]) for c in self.items}
        self.slug_count = {}
        for c in self.items:
            self.slug_count[slug(c["name"])] = self.slug_count.get(slug(c["name"]), 0) + 1
        self.md_examples = {}
        self.keep_existing = set()
        self.tokens_ref = None  # Tokens, para saber qué tokens cambian con la marca
        for fname in ("components.md", "patterns.md"):
            # antes de la migración las fichas aún viven aquí; después el archivo ya no tiene secciones de ficha
            self.md_examples.update(code_examples_from_md(read(os.path.join(ds_root, "docs", fname), "")))
        for d in DOCS_DIR.values():
            for p in sorted(glob.glob(os.path.join(ds_root, "docs", d, "*.md"))):
                if os.path.basename(p) != PLANTILLA:
                    self.md_examples.update(code_examples_from_md(read(p, "")))
        self.set_of_component = {}
        for c in self.items:
            self.set_of_component[c["name"]] = c["name"]

    def is_icon(self, name):
        return any(name.startswith(p) for p in self.cfg["iconFamilyPrefix"]) if name else False

    def kind(self, c):
        page = (c.get("page") or "").lower()
        return "pattern" if any(k in page for k in self.cfg["patternKeywords"]) else "component"

    def resolve_slug(self, comp_name, comp_set):
        target = comp_set or comp_name
        if target in self.slugs:
            return self.slugs[target]
        if comp_set is None and comp_name:
            # icono anidado suele venir como "Icon / arrow right" (componente dentro del set Icon)
            for n in self.slugs:
                if comp_name.startswith(n) or n.startswith(comp_name):
                    return self.slugs[n]
        return slug(target) if target else None

    def schema(self, c, existing):
        s = slug(c["name"])
        kind = self.kind(c)
        props = []
        swap_props, default_icons = [], []
        for p in c.get("properties", []) or []:
            entry = {"name": p.get("name"), "kind": p.get("kind", "unknown"), "default": p.get("default")}
            if p.get("kind") == "VARIANT":
                entry["values"] = [str(v) for v in (p.get("values") or [])]
            if p.get("kind") == "INSTANCE_SWAP":
                entry["defaultComponent"] = p.get("defaultComponent") or "unknown"
                entry["preferredValues"] = p.get("preferredValues") or []
                swap_props.append(p.get("name"))
                if p.get("defaultComponent"):
                    default_icons.append(p["defaultComponent"])
            props.append(entry)
        nested, uses, unexposed = [], [], []
        for n in c.get("nestedInstances", []) or []:
            comp = n.get("component") or "unknown"
            cs = self.resolve_slug(comp, n.get("componentSet"))
            nested.append({"layer": n.get("layer", "unknown"), "component": comp, "componentSlug": cs,
                           "exposedAs": n.get("exposedAs"), "toggledBy": n.get("toggledBy"),
                           "visibleByDefault": bool(n.get("visibleByDefault", True))})
            if cs:
                uses.append(cs)
            if self.is_icon(comp) or self.is_icon(n.get("componentSet") or ""):
                if not n.get("exposedAs"):
                    unexposed.append(n.get("layer", "unknown"))
                    self.findings.append(("warning", "icon-not-exposed-as-swap", f"{c['name']}: capa «{n.get('layer')}» ({comp}) sin INSTANCE_SWAP"))
        has_icon = bool(swap_props) or any(self.is_icon(n["component"]) or self.is_icon(n.get("componentSet") or "") for n in
                                           (c.get("nestedInstances") or []))
        variants = c.get("variantAxes") or {}
        states = [str(v) for k, vals in variants.items() if k.lower() in ("state", "estado") for v in vals]
        defaults = {}
        for p in props:
            if p["kind"] == "VARIANT" and p.get("default") is not None:
                defaults[p["name"]] = p["default"]
        bindings = c.get("bindings") or {}
        tokens_used = sorted({b.split(": ", 1)[-1] for b in bindings.get("variables", []) or []})
        existing = existing or {}
        old_code = (existing.get("source") or {}).get("code") or {}
        sch = {
            "$schema": "../_component.schema.json",
            "id": f"{kind}:{s}",
            "meta": {"name": c["name"], "slug": s, "kind": kind, "version": existing.get("meta", {}).get("version", "1.0.0"),
                     "lastSync": self.synced_at, "description": c.get("description") or "unknown",
                     "figmaPage": c.get("page"), "figmaType": c.get("type"), "variantCount": c.get("variantCount", 1),
                     "autoLayout": c.get("autoLayout", "unknown")},
            "source": {
                "docs": {"file": f"design-system/docs/{DOCS_DIR[kind]}/{s}.md", "section": c["name"]},
                "figma": {"fileKey": self.file_key, "nodeId": c.get("id"), "componentKey": c.get("key")},
                "code": {"package": old_code.get("package"), "import": old_code.get("import"),
                         "path": old_code.get("path", "design-system/css/components.css"),
                         "classes": (self.md_examples.get(s) or {}).get("classes", old_code.get("classes", [])),
                         "example": (self.md_examples.get(s) or {}).get("example", old_code.get("example"))},
            },
            "api": {
                "properties": props, "variants": {k: [str(x) for x in v] for k, v in variants.items()},
                "states": states, "defaults": defaults, "invalidCombinations": (existing.get("api") or {}).get("invalidCombinations", []),
                "nestedInstances": nested,
                "icons": {"hasIcon": has_icon, "swapProperties": swap_props, "defaultIcons": default_icons,
                          "compatible": "any Icon / * via INSTANCE_SWAP" if swap_props else ("unknown" if has_icon else "none"),
                          "unexposedIconLayers": unexposed},
                "slots": (existing.get("api") or {}).get("slots", []),
                "tokensUsed": tokens_used, "variablesUsed": bindings.get("variables", []) or [],
                "textStyles": bindings.get("textStyles", []) or [],
                "theming": self.theming(tokens_used),
            },
            "behavior": existing.get("behavior") or {"responsive": [], "content": [], "interactions": []},
            "compatibility": existing.get("compatibility") or {},
            "relations": {"uses": sorted(set(uses)), "usedBy": [], "related": (existing.get("relations") or {}).get("related", [])},
        }
        # Huella de la anatomía: lo que, si cambia en Figma, obliga a verificar de nuevo el contrato
        # contra su maestro (key, ejes de variante, propiedades, tokens ligados, hijos). No lleva fechas:
        # dos syncs del mismo maestro dan la misma huella.
        anat = {"key": c.get("key"), "variants": sch["api"]["variants"],
                "properties": sorted((p["name"] or "", p["kind"] or "", json.dumps(p.get("values"), ensure_ascii=False)) for p in props),
                "tokensUsed": tokens_used, "nested": sorted((n["componentSlug"] or n["component"] or "") for n in nested)}
        sch["meta"]["anatomyHash"] = hashlib.sha1(json.dumps(anat, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:12]
        # Estado de verificación contra el maestro (lo escribe quien verifica; aquí solo se conserva y se
        # caduca). Sin bloque = unverified, y no se inventa uno.
        old_ver = (existing.get("meta") or {}).get("verification")
        if isinstance(old_ver, dict) and old_ver:
            ver = dict(old_ver)
            # Con un slug compartido (slug-collision) cada maestro pasa por aquí y el homónimo caducaría la
            # verificación en cada sync: en ese caso solo la caduca el maestro que el contrato registra (misma
            # componentKey). Sin colisión se compara siempre, porque un maestro republicado con otra key es
            # precisamente un cambio que hay que volver a verificar.
            old_key = ((existing.get("source") or {}).get("figma") or {}).get("componentKey")
            colision = self.slug_count.get(s, 1) > 1
            mismo_maestro = not colision or not old_key or old_key == c.get("key")
            if mismo_maestro and ver.get("status") == "verified" and ver.get("figmaVersion") != sch["meta"]["anatomyHash"]:
                ver.update({"status": "stale", "staleSince": self.synced_at,
                            "reason": "la anatomía, las variantes, los tokens ligados o la key del maestro cambiaron desde la verificación"})
                self.findings.append(("warning", "verification-stale", f"{c['name']}: el maestro cambió desde que se verificó ({ver.get('date', '?')}); vuelve a pasar el protocolo de verificación"))
            sch["meta"]["verification"] = ver
        old_rules = existing.get("rules") or {}
        if any(old_rules.values()):
            # El criterio vive solo en el .md. Un schema antiguo con contenido en «rules» no se
            # sobrescribe: se perdería ese texto. Se para hasta que alguien lo pase al .md.
            self.keep_existing.add(s)
            self.findings.append(("critical", "criteria-only-in-schema",
                                  f"{c['name']}: el schema trae criterio en rules ({', '.join(k for k, v in old_rules.items() if v)}); "
                                  f"pásalo a {sch['source']['docs']['file']} § {c['name']} y quita rules del schema. "
                                  f"Hasta entonces este schema no se regenera"))
        if has_icon and not sch["relations"]["uses"]:
            self.findings.append(("critical", "schema-missing-nested-instance", f"{c['name']}: tiene icono pero relations.uses está vacío"))
        if sch["source"]["code"]["example"] is None:
            self.findings.append(("warning", "code-example-missing-or-stale", f"{c['name']}: sin «Ejemplo de código» (source.code.example)"))
        return sch

    def theming(self, tokens_used):
        tk = self.tokens_ref
        if tk is None:
            return {"brandAware": "unknown"}
        info = tk.brand_info()
        if not info["brands"]:
            return {"brandAware": False, "brands": []}
        dep = sorted(t for t in tokens_used if tk.brand_dependent(t))
        return {"brandAware": bool(dep), "attribute": info["attribute"],
                "brands": [b["slug"] for b in info["brands"]],
                "defaultBrand": next((b["slug"] for b in info["brands"] if b["default"]), None),
                "brandTokens": dep}

    def live_block(self, sch):
        a = sch["api"]
        L = [f"- **Figma:** `{sch['source']['figma']['nodeId'] or 'unknown'}` · página «{sch['meta'].get('figmaPage')}» · {sch['meta'].get('figmaType')} · {sch['meta'].get('variantCount')} variantes · última sync {sch['meta']['lastSync']}",
             f"- **Descripción (Figma):** {sch['meta'].get('description') or 'unknown'}",
             "- **Anatomía:** " + (", ".join(f"`{n['layer']}` → {n['component']}" for n in a["nestedInstances"]) or "sin instancias anidadas")]
        for axis, vals in a["variants"].items():
            L.append(f"- **{axis}:** {', '.join(vals)}")
        def pdesc(p):
            d = p.get("defaultComponent") if p["kind"] == "INSTANCE_SWAP" else p.get("default")
            return f"`{p['name']}` ({p['kind']}{', por defecto ' + str(d) if d not in (None, '') else ''})"
        L.append("- **Propiedades de componente:** " + (", ".join(pdesc(p) for p in a["properties"]) or "ninguna"))
        ic = a["icons"]
        if ic["hasIcon"]:
            L.append(f"- **Iconos / instancias anidadas:** sí · swap: {', '.join(f'`{x}`' for x in ic['swapProperties']) or 'ninguna (⚠️ no expuesto)'} · por defecto: {', '.join(ic['defaultIcons']) or 'unknown'}"
                     + (f" · capas sin swap: {', '.join(ic['unexposedIconLayers'])}" if ic["unexposedIconLayers"] else ""))
        else:
            L.append("- **Iconos / instancias anidadas:** ninguno")
        L.append("- **Tokens que consume:** " + (", ".join(f"`{t}`" for t in a["tokensUsed"]) or "unknown"))
        if a["textStyles"]:
            L.append("- **Text styles:** " + ", ".join(f"`{t}`" for t in a["textStyles"]))
        th = a.get("theming") or {}
        if th.get("brandAware") is True:
            L.append(f"- **Marcas:** cambia con la marca ({', '.join(th['brands'])}; por defecto `{th['defaultBrand']}`) vía `[{th['attribute']}]` · tokens de marca: "
                     + ", ".join(f"`{t}`" for t in th["brandTokens"]))
        elif th.get("brandAware") is False and th.get("brands"):
            L.append("- **Marcas:** igual en todas las marcas (no consume tokens de marca)")
        return "\n".join(L)


MANUAL_FIELDS = ["Propósito", "Ejemplo de código", "Accesibilidad (pares AA verificados)", "Cuándo usar / qué NO hace"]


def code_examples_from_md(md):
    """Extrae, por contrato ('### Nombre'), el bloque ```html del «Ejemplo de código» y sus clases.
    El .md es la fuente manual del ejemplo; ds-sync lo copia a schema.source.code."""
    out = {}
    for m in re.finditer(r"^### (.+?)(?:\s{2,}.*)?$", md, re.M):
        name = m.group(1).strip()
        nxt = re.search(r"^### |^## ", md[m.end():], re.M)
        section = md[m.end(): m.end() + (nxt.start() if nxt else len(md))]
        ex = re.search(r"\*\*Ejemplo de código:\*\*.*?```html\s*\n(.*?)\n\s*```", section, re.S)
        if not ex:
            continue
        code = "\n".join(l.strip() for l in ex.group(1).splitlines()).strip()
        if not code or "⬜ TODO" in code or code.startswith("<!--"):
            continue
        classes = sorted({c for grp in re.findall(r'class="([^"]+)"', code) for c in grp.split()})
        out[slug(name)] = {"example": code, "classes": classes}
    return out


def manual_fields_block():
    """Los campos de criterio de una ficha nueva, vacíos (⬜ TODO). Se escriben una vez; el sync no los toca."""
    return "\n".join(f"- **{f}:** ⬜ TODO" if f != "Ejemplo de código" else
                     "- **Ejemplo de código:** ⬜ TODO _(snippet HTML mínimo con las clases reales de `components.css`; se copia a `source.code.example` del schema)_\n  ```html\n  <!-- ⬜ TODO -->\n  ```"
                     for f in MANUAL_FIELDS)


def ficha_heading(name, date):
    return f"### {name}   ⚙️ synced: {date}"


def new_ficha(name, s, date, live):
    return f"{ficha_heading(name, date)}\n\n{GEN_START.format(s)}\n{live}\n{GEN_END.format(s)}\n\n{manual_fields_block()}\n"


def plantilla_md(kind):
    """docs/<carpeta>/_plantilla.md: la forma exacta con la que nace una ficha. La escribe el sync para que
    nunca se desvíe del generador; no es un contrato y el sync la ignora al leer."""
    que = "componente" if kind == "component" else "patrón"
    aviso = (f"<!-- Plantilla de ficha de {que}. No es una ficha: scripts/ds-sync.py la regenera y la ignora como contrato.\n"
             f"     Cada {que} nuevo del volcado nace en docs/{DOCS_DIR[kind]}/<slug>.md con esta forma: heading, bloque\n"
             f"     GENERATED (lo escribe el sync desde Figma; no editar a mano) y, debajo, los campos de criterio que se\n"
             f"     rellenan a mano una vez y el sync conserva. -->\n\n")
    return aviso + new_ficha("<Nombre>", "<slug>", "<fecha>",
                             "(parte viva: Figma, descripción, anatomía, ejes de variante, propiedades, iconos y tokens que consume)")


def upsert_ficha_file(text, sch, live):
    """Ficha en docs/<carpeta>/<slug>.md: crea el archivo si no existe o sustituye solo su bloque GENERATED
    (y la fecha del heading). Todo lo manual que haya debajo se conserva tal cual."""
    name, s, date = sch["meta"]["name"], sch["meta"]["slug"], sch["meta"]["lastSync"]
    if not text:
        return new_ficha(name, s, date, live)
    gs, ge = GEN_START.format(s), GEN_END.format(s)
    m = re.compile(rf"^### {re.escape(name)}(?:\s{{2,}}.*)?$", re.M).search(text)
    if m is None and gs in text:
        # mismo slug, otro nombre (renombrado en Figma): el heading que precede al bloque es el suyo
        prev = [h for h in re.finditer(r"^### .*$", text, re.M) if h.start() < text.index(gs)]
        m = prev[-1] if prev else None
    if m is None:
        return text.rstrip("\n") + "\n\n" + new_ficha(name, s, date, live)
    start = m.end()
    nxt = re.search(r"^## |^### ", text[start:], re.M)
    end = start + (nxt.start() if nxt else len(text) - start)
    section = text[start:end]
    section = replace_generated(section, s, live) if gs in section else f"\n\n{gs}\n{live}\n{ge}" + section
    tail = text[end:].lstrip("\n")
    return text[:m.start()] + ficha_heading(name, date) + section.rstrip("\n") + "\n" + (f"\n{tail}" if tail.strip() else "")


def migrate_fichas(md, files):
    """Primera ejecución tras separar las fichas: saca cada sección «### <Nombre>   ⚙️ synced: …» del .md
    grande a `files[slug]` y devuelve (md sin fichas ni «Plantilla de contrato», notas). Si el .md ya no
    tiene fichas no hace nada. La parte manual se mueve literal. Dentro de una sección solo se conserva el
    bloque GENERATED de su propio slug: un bloque de otro componente es una copia obsoleta (error antiguo de
    coincidencia por prefijo al buscar el heading) y se descarta solo si ese componente tiene sección propia."""
    notas = []

    def sin_plantilla(texto):
        # La «Plantilla de contrato» se retira SIEMPRE DESPUÉS de extraer las fichas: en la plantilla anterior
        # las secciones de ficha se insertaban antes de «## Catálogo propuesto», es decir, dentro de esa misma
        # sección «##», y quitarla antes se las llevaría por delante.
        m = re.search(r"^## Plantilla de contrato.*?(?=^## |\Z)", texto, re.M | re.S)
        if not m:
            return texto
        notas.append(f"sección «Plantilla de contrato» retirada: la plantilla vive en {PLANTILLA}")
        return texto[:m.start()] + texto[m.end():]

    heads = list(FICHA_HEADING_RE.finditer(md))
    if not heads:
        # sin fichas que mover (proyecto anterior sin sync previo): solo sobra la plantilla antigua
        md2 = sin_plantilla(md)
        return (re.sub(r"\n{3,}", "\n\n", md2) if notas else md), notas
    bounds = [h.start() for h in re.finditer(r"^## |^### ", md, re.M)] + [len(md)]
    canon = {slug(h.group("name")) for h in heads}
    tramos = []
    for h in heads:
        end = next(b for b in bounds if b > h.start())
        name, date = h.group("name").strip(), h.group("date")
        s = slug(name)
        body = md[h.end():end]
        propios, ajenos = [], []
        for g in GEN_BLOCK_RE.finditer(body):
            (propios if g.group("slug") == s else ajenos).append(g.group(0))
        keep = list(propios)
        if len(propios) > 1:
            notas.append(f"{name}: {len(propios)} bloques GENERATED propios; se conservan todos (el sync solo actualiza el primero)")
        for g, gslug in ((g, re.match(r"<!-- ⚙️ GENERATED:start:([^ ]+)", g).group(1)) for g in ajenos):
            if gslug in canon:
                notas.append(f"{name}: descartada la copia obsoleta del bloque GENERATED de «{gslug}» (tiene ficha propia)")
            else:
                keep.append(g)
                notas.append(f"{name}: conservado un bloque GENERATED de «{gslug}» que no tiene ficha propia")
        manual = re.sub(r"\n{3,}", "\n\n", GEN_BLOCK_RE.sub("", body)).strip("\n")
        partes = [ficha_heading(name, date)] + keep + ([manual] if manual else [])
        texto = "\n\n".join(partes) + "\n"
        if s in files:
            files[s] = files[s].rstrip("\n") + "\n\n" + texto
            notas.append(f"{name}: comparte el slug «{s}» con otra ficha; las dos quedan en el mismo archivo")
        else:
            files[s] = texto
        tramos.append((h.start(), end))
    for a, b in reversed(tramos):
        md = md[:a] + md[b:]
    md = sin_plantilla(md)
    notas.insert(0, f"{len(heads)} fichas movidas a su archivo")
    return re.sub(r"\n{3,}", "\n\n", md), notas


def estado_ficha(text):
    n = text.count("⬜ TODO")
    return "✅ criterio completo" if n == 0 else f"⬜ {n} pendiente{'s' if n != 1 else ''}"


def update_index_section(md, entries):
    """«## Índice»: una línea por ficha (nombre enlazado a su archivo, kind, slug y estado del criterio)."""
    body = "\n".join(f"- [{n}]({d}/{s}.md) · {k} · `{s}` · {e}" for n, s, k, d, e in entries) or "_(vacío — se genera con el sync)_"
    m = re.search(r"^## Índice\s*\n(.*?)(?=^## |\Z)", md, re.M | re.S)
    if m:
        return md[:m.start(1)] + body + "\n\n" + md[m.end(1):]
    return md


# ────────────────────────────── showcase ──────────────────────────────
def showcase_sections(tokens, schemas, assets_rows, patterns_md):
    esc = htmllib.escape
    out = {}
    # tokens
    cards = []
    for col in tokens.collections:
        if not col["tokens"]:
            continue
        colors = [t for t in col["tokens"] if t["type"] == "COLOR"]
        others = [t for t in col["tokens"] if t["type"] != "COLOR"]
        inner = ""
        if colors:
            inner += '<div class="sc-demo sc-demo--block">' + "".join(
                f'<div class="sc-swatch" style="--sc-swatch: var({t["cssVar"]})"><div class="sc-swatch__chip"></div>'
                f'<div><div class="sc-swatch__name">{esc(t["cssVar"])}</div><div class="sc-swatch__value">{esc(tokens.mode_value(t, tokens.default_mode(col))[0])}</div></div></div>'
                for t in colors) + "</div>"
        if others:
            inner += '<table class="sc-table"><thead><tr><th>Token</th><th>Valor</th><th>Descripción</th></tr></thead><tbody>' + "".join(
                f"<tr><td><code>{esc(t['cssVar'])}</code></td><td>{esc(tokens.mode_value(t, tokens.default_mode(col))[0])}</td><td>{esc(t['description'] or '—')}</td></tr>"
                for t in others) + "</tbody></table>"
        cards.append(f'<div class="sc-card"><div class="sc-card__head"><h3>{esc(col["name"])}</h3><span class="sc-tag">{len(col["tokens"])} tokens · {", ".join(esc(m["name"]) for m in col["modes"])}</span></div>{inner}</div>')
    out["tokens"] = "\n".join(cards) or '<div class="sc-empty">Sin tokens todavía: pendiente del primer sync desde Figma.</div>'
    # components / patterns
    for kind, key in (("component", "components"), ("pattern", "patterns")):
        cards = []
        for sch in schemas:
            if sch["meta"]["kind"] != kind:
                continue
            ex = sch["source"]["code"]["example"]
            demo_cls = "sc-demo sc-demo--block" if kind == "pattern" else "sc-demo"  # los patrones ocupan todo el ancho
            demo = f'<div class="{demo_cls}">{ex}</div><pre class="sc-code">{esc(ex)}</pre>' if ex else '<div class="sc-demo"><span class="sc-tag">sin «Ejemplo de código» en el contrato</span></div>'
            tag = f"{sch['meta'].get('variantCount', 1)} variantes · {sch['source']['figma']['nodeId'] or 'unknown'}" + (" · icono" if sch["api"]["icons"]["hasIcon"] else "")
            cards.append(f'<div class="sc-card" id="sc-{sch["meta"]["slug"]}"><div class="sc-card__head"><h3>{esc(sch["meta"]["name"])}</h3><span class="sc-tag">{esc(tag)}</span></div>{demo}</div>')
        out[key] = ('<div class="sc-grid">' + "\n".join(cards) + "</div>") if cards else f'<div class="sc-empty">Sin {"componentes" if kind == "component" else "patrones"} todavía: se generan con el sync.</div>'
    # composition: tablas markdown de patterns.md § Composición
    comp_html = []
    m = re.search(r"^## Composición de pantalla.*?(?=^## |\Z)", patterns_md or "", re.M | re.S)
    if m:
        for sub in re.finditer(r"^### (.+?)\n(.*?)(?=^### |\Z)", m.group(0), re.M | re.S):
            rows = [l for l in sub.group(2).splitlines() if l.startswith("|")]
            if len(rows) >= 2:
                head = [c.strip() for c in rows[0].strip("|").split("|")]
                body = [[c.strip() for c in r.strip("|").split("|")] for r in rows[2:]]
                comp_html.append(f"<h3>{esc(sub.group(1))}</h3><table class=\"sc-table\"><thead><tr>" + "".join(f"<th>{esc(h)}</th>" for h in head) + "</tr></thead><tbody>"
                                 + "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in r) + "</tr>" for r in body) + "</tbody></table>")
    out["composition"] = "\n".join(comp_html) or '<div class="sc-empty">Reglas de composición pendientes.</div>'
    # assets
    if assets_rows:
        out["assets"] = '<div class="sc-grid">' + "".join(
            f'<div class="sc-card"><div class="sc-demo"><img src="../assets/icons/{esc(r["file"])}" alt="{esc(r["name"])}" width="24" height="24"></div><pre class="sc-code">{esc(r["file"])}</pre></div>'
            for r in assets_rows) + "</div>"
    else:
        out["assets"] = '<div class="sc-empty">Sin assets exportados todavía.</div>'
    return out


# ────────────────────────────── volcado: trozos y validación ──────────────────────────────
def fold_parts(ds, dry):
    """Une los trozos de sync/parts/ en variables.json y components.json. Devuelve (unidos, errores).

    Determinista: los trozos se ordenan por archivo de tokens o página y por posición, no por el
    nombre con que se guardaron. Si falta un trozo en medio de una cadena, no se escribe nada."""
    parts_dir = os.path.join(ds, "sync", "parts")
    paths = sorted(glob.glob(os.path.join(parts_dir, "*.json")))
    if not paths:
        return 0, []
    errores, partes = [], []
    for pth in paths:
        texto = read(pth) or ""
        if TRUNCATED_RE.search(texto):
            errores.append(f"{os.path.relpath(pth)}: la respuesta del MCP llegó cortada; vuelve a leer ese trozo")
            continue
        try:
            d = json.loads(texto)
        except json.JSONDecodeError as e:
            errores.append(f"{os.path.relpath(pth)}: JSON inválido ({e}); vuelve a leer ese trozo")
            continue
        if d.get("kind") not in ("variables", "components") or not isinstance(d.get("part"), dict):
            errores.append(f"{os.path.relpath(pth)}: no es un trozo de los scripts de lectura (falta kind o part)")
            continue
        partes.append(d)
    if errores:
        return 0, errores

    v_path, c_path = os.path.join(ds, "sync", "variables.json"), os.path.join(ds, "sync", "components.json")
    var = read_json(v_path, None) or {}
    var.setdefault("collections", []); var.setdefault("textStyles", []); var.setdefault("effectStyles", [])
    var.setdefault("readProgress", {})
    com = read_json(c_path, None) or {}
    com.setdefault("pages", [])

    def clave_var(d):
        return d.get("fileKey") or d.get("fileName") or "unknown"

    for d in sorted((x for x in partes if x["kind"] == "variables"), key=lambda x: (clave_var(x), x["part"].get("offset", 0))):
        k, pt = clave_var(d), d["part"]
        prog = var["readProgress"].get(k)
        if pt.get("offset", 0) == 0:
            # empieza de cero lo de este archivo de tokens
            var["collections"] = [c for c in var["collections"] if c.get("source") != k]
            var["textStyles"] = [x for x in var["textStyles"] if x.get("source") != k]
            var["effectStyles"] = [x for x in var["effectStyles"] if x.get("source") != k]
            prog = {"total": pt.get("total"), "read": 0}
        elif prog is None or prog["read"] != pt.get("offset"):
            esperado = prog["read"] if prog else 0
            errores.append(f"variables de {k}: el trozo que empieza en {pt.get('offset')} está repetido; borra la copia"
                           if pt.get("offset", 0) < esperado else
                           f"variables de {k}: falta el trozo que empieza en {esperado} (llegó uno que empieza en {pt.get('offset')})")
            continue
        for col in d.get("collections") or []:
            dest = next((c for c in var["collections"] if c.get("id") == col.get("id") and c.get("source") == k), None)
            if dest is None:
                dest = {**{kk: vv for kk, vv in col.items() if kk != "variables"}, "fileKey": d.get("fileKey"), "source": k, "variables": []}
                var["collections"].append(dest)
            dest["variables"] += col.get("variables") or []
        var["textStyles"] += [{**x, "source": k} for x in d.get("textStyles") or []]
        var["effectStyles"] += [{**x, "source": k} for x in d.get("effectStyles") or []]
        prog["read"] += pt.get("count", 0)
        prog["total"] = pt.get("total")
        var["readProgress"][k] = prog
        var["fileKey"] = var.get("fileKey") or d.get("fileKey")
        var["fileName"] = var.get("fileName") or d.get("fileName")
        var["version"] = var.get("version")
        var["readAt"] = max(filter(None, [var.get("readAt"), d.get("readAt")]), default=None)

    for d in sorted((x for x in partes if x["kind"] == "components"),
                    key=lambda x: ((x.get("page") or {}).get("id") or "", x["part"].get("offset", 0))):
        pg, pt = d.get("page") or {}, d["part"]
        dest = next((p for p in com["pages"] if p.get("id") == pg.get("id")), None)
        if pt.get("offset", 0) == 0:
            if dest is None:
                dest = {"name": pg.get("name"), "id": pg.get("id"), "fileKey": d.get("fileKey")}
                com["pages"].append(dest)
            dest.update({"components": [], "total": pt.get("total"), "read": 0})
        elif dest is None or dest.get("read") != pt.get("offset"):
            esperado = dest.get("read") if dest else 0
            errores.append(f"página {pg.get('name')}: el trozo que empieza en {pt.get('offset')} está repetido; borra la copia"
                           if pt.get("offset", 0) < esperado else
                           f"página {pg.get('name')}: falta el trozo que empieza en {esperado} (llegó uno que empieza en {pt.get('offset')})")
            continue
        dest["components"] += d.get("components") or []
        dest["read"] += pt.get("count", 0)
        dest["total"] = pt.get("total")
        com["fileKey"] = com.get("fileKey") or d.get("fileKey")
        com["readAt"] = max(filter(None, [com.get("readAt"), d.get("readAt")]), default=None)

    if errores:
        return 0, errores
    escritos = []
    if any(x["kind"] == "variables" for x in partes):
        write_json(v_path, var, dry, escritos)
    if any(x["kind"] == "components" for x in partes):
        write_json(c_path, com, dry, escritos)
    if not dry:
        for pth in paths:
            os.remove(pth)
    return len(partes), []


def check_dump(raw_vars, raw_comps, textos):
    """Valida el volcado antes de generar nada. Devuelve (errores, avisos).

    Errores: texto «truncated» (respuesta cortada), IDs repetidos y alias que no apuntan a ninguna
    variable del volcado. Avisos: volcado a medias (faltan trozos por leer). El JSON inválido ya lo
    para read_json al cargarlo."""
    errores, avisos = [], []
    for nombre, t in textos.items():
        if t and TRUNCATED_RE.search(t):
            errores.append(f"sync/{nombre}: contiene «truncated», la respuesta del MCP llegó cortada")
    if raw_vars:
        ids = [v.get("id") for c in raw_vars.get("collections") or [] for v in c.get("variables") or []]
        ids += [x.get("id") for x in (raw_vars.get("textStyles") or []) + (raw_vars.get("effectStyles") or [])]
        rep = sorted({i for i in ids if i and ids.count(i) > 1})
        if rep:
            errores.append(f"variables.json: {len(rep)} IDs repetidos ({', '.join(rep[:5])}): un trozo se guardó dos veces")
        definidos = set(ids)
        rotos = sorted({f"{v.get('name')} → {val.get('name') or val.get('id')}"
                        for c in raw_vars.get("collections") or [] for v in c.get("variables") or []
                        for val in (v.get("valuesByMode") or {}).values()
                        if isinstance(val, dict) and val.get("type") == "alias" and val.get("id") not in definidos})
        if rotos:
            errores.append(f"variables.json: {len(rotos)} alias apuntan a variables que no están en el volcado "
                           f"({'; '.join(rotos[:5])}). Si viven en otro archivo de Figma, léelo también")
        for k, pr in (raw_vars.get("readProgress") or {}).items():
            if pr.get("read") != pr.get("total"):
                avisos.append(f"variables de {k}: leídas {pr.get('read')} de {pr.get('total')}; faltan trozos")
    if raw_comps:
        ids = [c.get("id") for p in raw_comps.get("pages") or [] for c in p.get("components") or []]
        rep = sorted({i for i in ids if i and ids.count(i) > 1})
        if rep:
            errores.append(f"components.json: {len(rep)} componentes repetidos ({', '.join(rep[:5])}): un trozo se guardó dos veces")
        for p in raw_comps.get("pages") or []:
            if "total" in p and p.get("read") != p.get("total"):
                avisos.append(f"página {p.get('name')}: leídos {p.get('read')} de {p.get('total')} componentes; faltan trozos")
    return errores, avisos


# ────────────────────────────── main ──────────────────────────────
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=None)
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--merge", action="store_true", help="solo une los trozos de sync/parts/ y valida")
    ap.add_argument("--check-dump", dest="check_dump", action="store_true", help="solo valida los volcados")
    args = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(args.root or os.path.dirname(here))
    ds = os.path.join(root, "design-system")
    cfg = dict(DEFAULT_CFG)
    user_cfg = read_json(os.path.join(here, "ds-sync.config.json"), {})
    for k, v in (user_cfg or {}).items():
        cfg[k] = {**cfg[k], **v} if isinstance(v, dict) and isinstance(cfg.get(k), dict) else v
    os.chdir(root)

    if not args.check_dump:
        unidos, errs = fold_parts(ds, args.dry)
        if errs:
            for e in errs:
                print(f"[ERROR] {e}")
            sys.exit("[ERROR] no se han unido los trozos de sync/parts/: no se ha escrito nada.")
        if unidos:
            print(f"ds-sync · {unidos} trozos unidos en sync/variables.json y sync/components.json")

    textos = {n: read(os.path.join(ds, "sync", n)) for n in ("variables.json", "components.json")}
    raw_vars = read_json(os.path.join(ds, "sync", "variables.json"))
    raw_comps = read_json(os.path.join(ds, "sync", "components.json"))
    raw_icons = read_json(os.path.join(ds, "sync", "icons.json"), [])
    if raw_vars is None and raw_comps is None:
        sys.exit("[ERROR] no hay volcados en design-system/sync/ (variables.json, components.json). "
                 "Léelos de Figma con el MCP oficial (scripts en design.md § Sync) y guárdalos ahí antes de ejecutar ds-sync.")
    errs, avisos = check_dump(raw_vars, raw_comps, textos)
    for a_ in avisos:
        print(f"[AVISO] {a_}")
    for e in errs:
        print(f"[ERROR] {e}")
    if errs:
        sys.exit("[ERROR] el volcado no es válido: no se genera nada. Vuelve a leer de Figma lo que falla.")
    if args.check_dump or args.merge:
        print("ds-sync · volcado válido" + (" (a medias: ver avisos)" if avisos else ""))
        sys.exit(0)
    synced_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    manifest = read_json(os.path.join(ds, "agent-manifest.json"), {})
    meta = {"designSystem": manifest.get("designSystem", "unknown"), "figmaSources": manifest.get("figmaSources", []),
            "adoptionMode": manifest.get("adoptionMode", "unknown"), "structuralStandardsEnforced": manifest.get("structuralStandardsEnforced", False)}
    written, findings = [], []

    # ── tokens ──
    tokens = Tokens(raw_vars, cfg, synced_at)
    tokens._text_rows()  # antes de recoger los hallazgos: la tipografía también los produce
    findings += tokens.findings
    if raw_vars is not None:
        write_json(os.path.join(ds, "tokens", "tokens.json"), tokens.tokens_json(meta), args.dry, written)
        css_generado = tokens.tokens_css(meta)
        problemas_css = check_css(css_generado)
        if problemas_css:
            for pr in problemas_css[:10]:
                print(f"[ERROR] tokens.css no es ejecutable: {pr}")
            sys.exit("[ERROR] el CSS generado no pasa la comprobación de ejecutabilidad; "
                     "no se escribe. Revisa los valores en Figma y vuelve a sincronizar.")
        write(os.path.join(ds, "tokens", "tokens.css"), css_generado, args.dry, written)
        write(os.path.join(ds, "docs", "tokens.md"), tokens.tokens_md(meta), args.dry, written)
        for fam, ok in tokens.foundations_status().items():
            if not ok:
                findings.append(("warning", "foundation-missing", f"Figma no define la familia {fam}"))

    # ── componentes ──
    schemas = []
    comps = Components(raw_comps, cfg, synced_at, ds)
    comps.tokens_ref = tokens
    if raw_comps is not None:
        comp_dir = os.path.join(ds, "schemas", "components")
        existing_files = {os.path.basename(p): p for p in glob.glob(os.path.join(comp_dir, "*.schema.json"))}
        for c in comps.items:
            s = slug(c["name"])
            path = os.path.join(comp_dir, f"{s}.schema.json")
            sch = comps.schema(c, read_json(path, {}))
            schemas.append(sch)
            if s not in comps.keep_existing:
                write_json(path, sch, args.dry, written)
            existing_files.pop(f"{s}.schema.json", None)
        for orphan, opath in existing_files.items():
            findings.append(("critical", "schema-without-component", f"schemas/components/{orphan} no corresponde a ningún componente del volcado"))
            # El maestro ya no está: lo que se hubiera verificado deja de valer. Se marca stale con el motivo
            # y se conserva el archivo (su criterio lo decide una persona: reenlazar o retirar, ver figma.md).
            osch = read_json(opath, {})
            if isinstance(osch, dict) and osch.get("meta") is not None:
                ver = dict(osch["meta"].get("verification") or {})
                if ver.get("status") != "stale" or ver.get("reason") != "maestro no encontrado en el volcado":
                    ver.update({"status": "stale", "staleSince": synced_at, "reason": "maestro no encontrado en el volcado"})
                    osch["meta"]["verification"] = ver
                    write_json(opath, osch, args.dry, written)
        findings += comps.findings
        # usedBy
        by_slug = {s["meta"]["slug"]: s for s in schemas}
        for s in schemas:
            for u in s["relations"]["uses"]:
                if u in by_slug:
                    by_slug[u]["relations"]["usedBy"] = sorted(set(by_slug[u]["relations"]["usedBy"] + [s["meta"]["slug"]]))
        if not args.dry:
            for s in schemas:
                if s["meta"]["slug"] not in comps.keep_existing:
                    write_json(os.path.join(comp_dir, f"{s['meta']['slug']}.schema.json"), s, args.dry, [])
        # index + relationships
        index = read_json(os.path.join(ds, "schemas", "index.json"), {})
        index.update({"lastSync": synced_at, "components": [{
            "id": s["id"], "name": s["meta"]["name"], "slug": s["meta"]["slug"], "kind": s["meta"]["kind"],
            "contractPath": f"./components/{s['meta']['slug']}.schema.json",
            "keywords": sorted({w for w in re.split(r"[\s/_-]+", s["meta"]["name"].lower()) if w} | ({"icon"} if s["api"]["icons"]["hasIcon"] else set())),
            "dependencies": s["relations"]["uses"], "hasIcon": s["api"]["icons"]["hasIcon"],
            "figmaSource": s["source"]["figma"], "codeSource": {"path": s["source"]["code"]["path"], "classes": s["source"]["code"]["classes"]}}
            for s in schemas],
            "counts": {"atoms": sum(1 for s in schemas if s["meta"]["kind"] == "component"), "patterns": sum(1 for s in schemas if s["meta"]["kind"] == "pattern")}})
        write_json(os.path.join(ds, "schemas", "index.json"), index, args.dry, written)
        rel = read_json(os.path.join(ds, "schemas", "relationships.json"), {})
        rel["relationships"] = [{"from": s["meta"]["slug"], "to": u, "type": "uses"} for s in schemas for u in s["relations"]["uses"]]
        rel["lastSync"] = synced_at
        write_json(os.path.join(ds, "schemas", "relationships.json"), rel, args.dry, written)
        # fichas (docs/<carpeta>/<slug>.md) e índices (components.md / patterns.md)
        for kind, fname in (("component", "components.md"), ("pattern", "patterns.md")):
            path, ddir = os.path.join(ds, "docs", fname), os.path.join(ds, "docs", DOCS_DIR[kind])
            md, files = read(path, ""), {}
            md, notas = migrate_fichas(md, files)
            for n in notas:
                print(f"  [MIGRACIÓN] {fname}: {n}")
            mine = [s for s in schemas if s["meta"]["kind"] == kind]
            for s in mine:
                sl = s["meta"]["slug"]
                if sl not in files:
                    files[sl] = read(os.path.join(ddir, f"{sl}.md"), "")
                files[sl] = upsert_ficha_file(files[sl], s, comps.live_block(s))
            for sl, texto in files.items():
                write(os.path.join(ddir, f"{sl}.md"), texto, args.dry, written)
            write(os.path.join(ddir, PLANTILLA), plantilla_md(kind), args.dry, written)
            md = update_index_section(md, [(s["meta"]["name"], s["meta"]["slug"], kind, DOCS_DIR[kind], estado_ficha(files[s["meta"]["slug"]])) for s in mine])
            md = re.sub(r"^\*\*Estado:\*\* .*$",
                        f"**Estado:** {len(mine)} {'componentes' if kind == 'component' else 'patrones'} sincronizados el {synced_at} · "
                        f"una ficha por archivo en `{DOCS_DIR[kind]}/<slug>.md` (este archivo solo guarda el índice y las secciones manuales).",
                        md, count=1, flags=re.M)
            write(path, md, args.dry, written)
            en_disco = {os.path.basename(p)[:-3] for p in glob.glob(os.path.join(ddir, "*.md"))} - {PLANTILLA[:-3]}
            for huerfana in sorted((en_disco | set(files)) - {s["meta"]["slug"] for s in mine}):
                findings.append(("warning", "contract-doc-without-component",
                                 f"docs/{DOCS_DIR[kind]}/{huerfana}.md no corresponde a ningún {'componente' if kind == 'component' else 'patrón'} del volcado; su criterio se conserva hasta que alguien decida"))
        # slugs compartidos: un solo schema y una sola ficha para varios componentes
        por_slug = {}
        for c in comps.items:
            por_slug.setdefault(slug(c["name"]), []).append(f"{c['name']} ({c.get('page')})")
        for sl, nombres in sorted(por_slug.items()):
            if len(nombres) > 1:
                findings.append(("warning", "slug-collision", f"{len(nombres)} componentes comparten el slug «{sl}»: {', '.join(nombres)} → un solo schema y una sola ficha (el último gana). Lo correcto es renombrar uno de los dos en Figma; mientras tanto el contrato puede apuntar al maestro equivocado"))

    # ── assets ──
    icons_dir = os.path.join(ds, "assets", "icons")
    files_present = {os.path.basename(p) for ext in ("*.svg", "*.png") for p in glob.glob(os.path.join(icons_dir, ext))}  # también PNG: logos de marca y exportaciones @2x
    assets_rows = []
    for ic in raw_icons or []:
        icon_base = re.sub(r"^Icon\s*/\s*", "", ic.get("name", ""), flags=re.I)
        f = ic.get("file") or (slug(icon_base) + ".svg")
        if f not in files_present:
            findings.append(("warning", "figma-vs-component-contracts", f"icons.json declara {f} pero no existe en assets/icons/"))
        assets_rows.append({"name": ic.get("name", "unknown"), "nodeId": ic.get("nodeId", "unknown"), "file": f, "usage": ic.get("usage", "")})
    for f in sorted(files_present - {r["file"] for r in assets_rows}):
        assets_rows.append({"name": "unknown (no está en sync/icons.json)", "nodeId": "unknown", "file": f, "usage": ""})
        findings.append(("info", "figma-vs-component-contracts", f"assets/icons/{f} sin entrada en sync/icons.json"))
    if raw_vars is not None or raw_comps is not None:
        icon_sizes = [t["cssVar"] for t in tokens.tokens if "icon" in t["path"].lower() and "size" in t["path"].lower()]
        # sync/fonts.json (opcional): [{file, family, origin, token, notes}] — describe assets/fonts/ como icons.json describe los iconos
        fonts_meta = {f.get("file"): f for f in read_json(os.path.join(ds, "sync", "fonts.json"), []) if isinstance(f, dict)}
        assets_md = ["<!-- ⚙️ ARCHIVO GENERADO por scripts/ds-sync.py — NO EDITAR A MANO. -->", "",
                     f"# {meta['designSystem']} · Assets  ·  _(iconos y fuentes exportados de Figma)_", "",
                     f"> Última sync: {synced_at}. Los archivos viven en `../assets/icons/` y `../assets/fonts/`; las pantallas los referencian desde ahí. No existe ningún otro `img/` ni `fonts/` en el proyecto.", "",
                     "## Iconos (`../assets/icons/`)",
                     md_table(["Archivo", "Componente Figma", "Node ID", "Tamaños (tokens `--icon-size-*`)", "Uso"],
                              [[f"`{r['file']}`", r["name"], f"`{r['nodeId']}`", ", ".join(f"`{v}`" for v in icon_sizes) or "⬜ sin tokens icon/size", r["usage"] or "—"] for r in assets_rows]) if assets_rows else "_(sin iconos exportados)_",
                     "", "## Fuentes (`../assets/fonts/`)",
                     md_table(["Archivo", "Familia · peso", "Origen (Figma / Google Fonts / licencia)", "Token `--family-*`", "Notas"],
                              [[f"`{os.path.basename(p)}`"] + [fonts_meta.get(os.path.basename(p), {}).get(k, "unknown" if k != "notes" else "") for k in ("family", "origin", "token", "notes")]
                               for p in sorted(glob.glob(os.path.join(ds, "assets", "fonts", "*"))) if not p.endswith(".gitkeep")]) ]
        write(os.path.join(ds, "docs", "assets.md"), "\n".join(assets_md) + "\n", args.dry, written)

    # ── showcase ──
    sc_path = os.path.join(ds, "showcase", "index.html")
    sc = read(sc_path)
    if sc is not None:
        secs = showcase_sections(tokens, schemas, assets_rows, read(os.path.join(ds, "docs", "patterns.md"), ""))
        for k, v in secs.items():
            sc = replace_generated(sc, k, v)
        sc = re.sub(r'(<span class="sc-header__meta" data-sc-last-sync>).*?(</span>)', rf"\g<1>última sync {synced_at}\g<2>", sc)
        write(sc_path, sc, args.dry, written)

    # ── drift + manifest ──
    drift = read_json(os.path.join(ds, "reports", "drift-report.json"), {})
    sev = {"critical": 0, "warning": 0, "info": 0}
    for s, _, _ in findings:
        sev[s] = sev.get(s, 0) + 1
    drift.update({"generatedAt": synced_at, "summary": sev,
                  "findings": [{"severity": s, "check": c, "detail": d} for s, c, d in findings],
                  "inputs": {"variables": raw_vars is not None, "components": raw_comps is not None, "icons": bool(raw_icons)},
                  "generatedBy": "scripts/ds-sync.py"})
    write_json(os.path.join(ds, "reports", "drift-report.json"), drift, args.dry, written)
    manifest["lastSync"] = synced_at
    write_json(os.path.join(ds, "agent-manifest.json"), manifest, args.dry, written)

    # ── resumen ──
    print(("[DRY] " if args.dry else "") + f"ds-sync · {len(tokens.tokens)} tokens en {len(tokens.collections)} colecciones · {len(schemas)} componentes/patrones · {len(assets_rows)} iconos")
    for s, c, d in findings:
        print(f"  [{s.upper()}] {c}: {d}")
    print(f"  {sev['critical']} críticos · {sev['warning']} avisos · {sev['info']} info → design-system/reports/drift-report.json")
    print("  archivos " + ("que se escribirían" if args.dry else "escritos") + f": {len(written)}")
    if not args.dry and written:
        _rastro(root, "ds-sync", "regenerados los artefactos del DS desde los volcados de Figma", written)
    for w in written:
        print(f"    {w}")
    print("Siguiente: revisa la parte de criterio (⬜ TODO) de los contratos nuevos, ejecuta python3 scripts/token-audit.py y revisa git diff.")
    sys.exit(1 if sev["critical"] else 0)


if __name__ == "__main__":
    main()
