#!/usr/bin/env python3
"""ds-sync — motor determinista del sync del design system: de los volcados de Figma a los artefactos.

Sin dependencias (stdlib, Python 3.8+). Uso, desde la raíz del proyecto:
    python3 scripts/ds-sync.py             # regenera todos los artefactos ⚙️ a partir de design-system/sync/
    python3 scripts/ds-sync.py --dry       # muestra qué generaría y los hallazgos, sin escribir nada
    python3 scripts/ds-sync.py --root .    # raíz del proyecto (por defecto: carpeta padre de scripts/)
    python3 scripts/ds-sync.py --merge     # solo une los trozos de sync/parts/ en los volcados y los valida
                                           # (un trozo con part.refresh, leído con NODE_IDS o con VARIABLE_IDS /
                                           # VARIABLE_NAMES, sustituye solo esos componentes o variables por id
                                           # y lo anota en partialRefresh.history)
    python3 scripts/ds-sync.py --check-dump  # solo valida los volcados: JSON, cortes, IDs repetidos, alias
    python3 scripts/ds-sync.py --allow-fewer-tokens  # permite que tokens.css pierda más del 10 % de sus tokens
                                           # (sin él, esa bajada para la generación: suele ser un volcado a medias)
    python3 scripts/ds-sync.py --variables-diff  # sync incremental: compara las huellas de sync/parts/fingerprints-*.json
                                           # (script de huellas, una llamada) con el volcado y dice qué variables
                                           # refrescar (VARIABLE_IDS), cuáles son nuevas y cuáles han desaparecido

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
                                         Si el DS está en varios archivos de Figma, cada página lleva su
                                         «fileKey» y el contrato de cada componente apunta a ese archivo.
    design-system/sync/icons.json        iconos exportados a assets/icons/ (nombre, nodo, archivo). Opcional.

Qué escribe (siempre los mismos artefactos, siempre igual para el mismo volcado; un archivo cuyo único
cambio sería la fecha del sync no se reescribe, así el diff de un sync enseña solo lo que cambió):
    tokens/tokens.json · tokens/tokens.css · docs/tokens.md
    schemas/components/<slug>.schema.json · schemas/index.json · schemas/relationships.json
        (contrato 12.0.0: api neutra de framework · code · figma · docs; un schema con la forma anterior
        se migra solo en la primera ejecución, conservando lo manual)
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
    fontFamilyMap (nombre de familia de Figma → familia CSS, y peso si el estilo no lo dice)
"""
import argparse
import glob
import hashlib
import html as htmllib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ds_common as dcom  # una sola definición de «interno» para toda la skill
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
    "cssStates": ["hover", "press", "pressed", "focus", "focused", "active"],
    "restStateValues": ["default", "enabled", "rest", "normal", "idle"],
    "fontFamilyMap": {},
    # Gravedad por comprobación del sync, para ajustarla por proyecto en ds-sync.config.json: p. ej. una librería
    # recién adoptada sin descripciones no necesita doscientos avisos de «sin descripción» antes de empezar
    # ({"missing-variable-description-or-scope": "info"}). Valores: "critical", "warning", "info", "off".
    "findingSeverity": {},
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


# Marcas de tiempo del sync (ISO 8601). Un archivo cuyo único cambio es la fecha no se reescribe: así un
# commit con sync trae solo lo que cambió de verdad. La fecha del último sync la llevan siempre
# agent-manifest.json y reports/drift-report.json, que son los que la necesitan.
TS_RE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})")
SIEMPRE_CON_FECHA = ("agent-manifest.json", "drift-report.json")


def write(path, text, dry, written):
    actual = read(path)
    if actual == text:
        return  # idéntico: no se toca ni se cuenta
    if actual is not None and os.path.basename(path) not in SIEMPRE_CON_FECHA and TS_RE.sub("<ts>", actual) == TS_RE.sub("<ts>", text):
        return  # solo cambia la fecha: no se toca ni se cuenta
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
        # Orden estable, independiente del orden de lectura (trozos, relecturas, volcados antiguos): así
        # releer lo mismo no mueve líneas en tokens.css/tokens.json/tokens.md. Estilos por nombre.
        self.text_styles = sorted(self.raw.get("textStyles", []) or [], key=lambda s: (s.get("name") or "", s.get("id") or ""))
        self.effect_styles = sorted(self.raw.get("effectStyles", []) or [], key=lambda s: (s.get("name") or "", s.get("id") or ""))
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
                    "collection": entry["name"], "description": limpiar_texto(v.get("description")),
                    "scopes": v.get("scopes") or [], "codeSyntax": v.get("codeSyntax") or {},
                    "valuesByMode": v.get("valuesByMode") or {}, "id": v.get("id"),
                    "unitless": self._unitless(v), "isTime": self._is_time(v),
                    "source": {"fileKey": col.get("fileKey") or self.file_key, "variableId": v.get("id"), "collectionId": col.get("id"),
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
            # Tokens agrupados por su ruta (todo menos el último tramo), grupos en orden alfabético y, dentro
            # de cada grupo, el orden de Figma (sort estable): xs, s, m, l no se vuelve l, m, s, xs.
            entry["tokens"].sort(key=lambda t: t["path"].rsplit("/", 1)[0] if "/" in t["path"] else "")
            self.collections.append(entry)
        self.collections.sort(key=lambda c: (c["name"], c["id"] or ""))
        self.tokens = [t for c in self.collections for t in c["tokens"]]
        self._check_scopes()
        seen = {}
        for t in self.tokens:
            if t["cssVar"] in seen:
                self.findings.append(("critical", "tokens-json-vs-css",
                                      f"colisión de nombre CSS {t['cssVar']}: {seen[t['cssVar']]} y {t['collection']}/{t['path']}"))
            seen[t["cssVar"]] = f"{t['collection']}/{t['path']}"

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
                            "cssVars": dict(rows), "description": limpiar_texto(s.get("description")) or "unknown"}
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
        # Orden de cascada, no de aparición: con max-width gana el último bloque, así que van de mayor a menor
        # (desktop → tablet → mobile → mobile-xs); con min-width, de menor a mayor. Antes seguían el orden en que
        # aparecía el primer token de cada modo, que un refresco puntual podía cambiar, y un móvil tomaba tablet.
        for (mname, query), rows in sorted(media_blocks.items(), key=lambda kv: media_sort_key(kv[0][1])):
            L += ["", f"@media {query} {{ /* modo {mname} */", "  :root {"] + rows + ["  }", "}"]
        return "\n".join(L) + "\n"

    def tokens_md(self, meta):
        L = ["<!-- ⚙️ ARCHIVO GENERADO por scripts/ds-sync.py — NO EDITAR A MANO. -->", "",
             f"# {meta['designSystem']} · Tokens  ·  _(espejo generado de la fuente)_", "",
             f"> Última sync: **{self.synced_at}** · modo de adopción: `{meta['adoptionMode']}` · "
             f"{len(self.tokens)} variables en {len(self.collections)} colecciones · {len(self.text_styles)} text styles · {len(self.effect_styles)} effect styles.",
             "> Cada token se consume en código como `var(--nombre)`. Los alias conservan su referencia y su valor resuelto.", "", "## Índice", ""]
        for col in self.collections:
            L.append(f"- [{col['name']}](#{slug(col['name'])}) · {len(col['tokens'])} tokens · modos: {', '.join(m['name'] for m in col['modes'])}")
        fs = self.foundations_status()
        L += ["- [Foundations](#foundations)", "- [Text styles](#text-styles)", ""]
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
    def __init__(self, raw, cfg, synced_at, ds_root, raw_icons=None, int_cfg=None):
        self.cfg, self.synced_at, self.ds_root = cfg, synced_at, ds_root
        self.int_cfg = int_cfg or {"internal": {"names": []}, "pagePrefixes": []}
        self.raw = raw or {}
        # La galería de iconos (sync/icons.json) también identifica iconos anidados: por su nombre completo o por su
        # último tramo («icons_line_24/search» → «search»), para proyectos cuyo DS no usa un prefijo de familia.
        self.icon_names = set()
        for ic in raw_icons or []:
            n = (ic.get("name") or "").strip()
            if n:
                self.icon_names.add(n); self.icon_names.add(n.split("/")[-1].strip())
        self.file_key = self.raw.get("fileKey")
        self.items = []
        self.findings = []
        for page in self.raw.get("pages", []) or []:
            for c in page.get("components", []) or []:
                c = dict(c)
                # Figma indenta nombres de página con espacios; se recortan siempre (figmaPage, grupo y kind dependen de él)
                c["page"] = (c.get("page") or page.get("name") or "unknown").strip()
                # cada componente apunta al archivo de Figma de SU página: un DS puede repartirse en varios archivos
                # (p. ej. Components y Patterns); el fileKey general del volcado es solo el valor por defecto
                c["fileKey"] = c.get("fileKey") or page.get("fileKey") or self.file_key
                self.items.append(c)
        self.slugs = {c["name"]: slug(c["name"]) for c in self.items}
        self.slug_set = set(self.slugs.values())
        self.slug_count = {}
        self.migrados = []
        for c in self.items:
            self.slug_count[slug(c["name"])] = self.slug_count.get(slug(c["name"]), 0) + 1
        self.md_examples = {}
        self.keep_existing = set()
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

    def interno(self, c):
        """Motivo por el que este componente del volcado es interno (ver ds_common.py), o None."""
        return dcom.interno_motivo({"name": c.get("name"), "slug": slug(c.get("name") or ""), "figmaPage": c.get("page")},
                                 self.int_cfg, c.get("published"))

    def is_icon(self, name):
        if not name:
            return False
        return any(name.startswith(p) for p in self.cfg["iconFamilyPrefix"]) or name.strip() in self.icon_names or name.split("/")[-1].strip() in self.icon_names

    def kind(self, c):
        page = (c.get("page") or "").lower()
        return "pattern" if any(k in page for k in self.cfg["patternKeywords"]) else "component"

    def resolve_slug(self, comp_name, comp_set):
        target = comp_set or comp_name
        if target in self.slugs:
            return self.slugs[target]
        if comp_set is None and comp_name:
            # icono anidado suele venir como "Icon / arrow right" (componente dentro del set Icon). Solo vale el nombre
            # de un set seguido de su separador: un prefijo suelto confundía el icono «search» con «search-bar-home».
            for n in sorted(self.slugs, key=len, reverse=True):
                if comp_name.startswith(n + "/") or comp_name.startswith(n + " /"):
                    return self.slugs[n]
        # Mismo componente escrito distinto en la instancia («Price content footer» frente a «price-content-footer»):
        # vale si su slug es el de un contrato del volcado.
        t = slug(target) if target else None
        if t and t in self.slug_set:
            return t
        # Sin contrato en el volcado (un icono, una pieza de otra librería): no se inventa un slug. La instancia queda
        # en figma.nestedInstances con su nombre; relations.uses solo lleva componentes que existen.
        return None

    def resolve_slug_legacy(self, comp_name, comp_set):
        """La resolución anterior a la 12.8.4 (aceptaba cualquier prefijo). Solo sirve para reconocer la huella con la
        que se verificaron los contratos y trasladarla a la nueva sin caducar nada: en Figma no cambió nada."""
        target = comp_set or comp_name
        if target in self.slugs:
            return self.slugs[target]
        if comp_set is None and comp_name:
            for n in self.slugs:
                if comp_name.startswith(n) or n.startswith(comp_name):
                    return self.slugs[n]
        return slug(target) if target else None

    def schema(self, c, existing):
        """Contrato 12.0.0: cuatro capas separadas.
        api    la API neutra de framework: props con tipo y defecto (sin nombres de Figma), estados de CSS aparte,
               eventos, slots y exclusiones (manuales), iconos y tokens.
        code   el enlace con HTML: ruta del CSS, clases, ejemplo, clase por valor de prop, anatomía por estado.
        figma  la trazabilidad: fileKey, nodeId, componentKey, nombre original de cada prop, ejes, instancias, bindings.
        docs   dónde vive el criterio escrito a mano.
        Lo manual (events, slots, exclusive, classByProp, stateAnatomy, example, classes, verification, related,
        accessibility) se conserva entre syncs; lo que viene de Figma se regenera. Un schema con la forma anterior
        (source/behavior/compatibility) se migra solo."""
        s = slug(c["name"])
        kind = self.kind(c)
        existing = existing or {}
        interno = self.interno(c)
        antiguo = "source" in existing and "code" not in existing
        if antiguo:
            self.migrados.append(s)
        old_code = existing.get("code") or (existing.get("source") or {}).get("code") or {}
        old_api = existing.get("api") or {}
        old_figma_key = ((existing.get("figma") or (existing.get("source") or {}).get("figma") or {})).get("componentKey")

        # ── props: de los nombres de Figma a una API neutra ──
        css_states = {x.lower() for x in self.cfg.get("cssStates") or []}
        rest_values = {x.lower() for x in self.cfg.get("restStateValues") or []}
        bool_values = {"yes", "no", "true", "false", "on", "off", "si", "sí"}
        props, names, prop_names = [], set(), {}
        def api_name(figma_name):
            base = re.sub(r"#.*$", "", figma_name or "").strip()
            parts = [w for w in re.split(r"[^0-9A-Za-zÀ-ÿ]+", base) if w]
            name = (parts[0].lower() + "".join(w[:1].upper() + w[1:] for w in parts[1:])) if parts else "prop"
            n, i = name, 2
            while n in names:
                n, i = f"{name}{i}", i + 1
            names.add(n)
            return n
        raw_props = c.get("properties", []) or []
        variants = {k: [str(x) for x in v] for k, v in (c.get("variantAxes") or {}).items()}
        variant_defaults = {p.get("name"): p.get("default") for p in raw_props if p.get("kind") == "VARIANT"}
        swap_props, default_icons = [], []
        for p in raw_props:
            kind_p, fname = p.get("kind", "unknown"), p.get("name") or ""
            if kind_p == "VARIANT":
                continue  # los ejes se tratan abajo, desde variantAxes
            n = api_name(fname); prop_names[n] = fname
            if kind_p == "BOOLEAN":
                d = p.get("default"); d = (str(d).lower() in ("true", "1", "yes")) if d is not None else None
                props.append({"name": n, "type": "boolean", "default": d, "figma": fname})
            elif kind_p == "TEXT":
                props.append({"name": n, "type": "string", "default": p.get("default"), "figma": fname})
            elif kind_p == "INSTANCE_SWAP":
                props.append({"name": n, "type": "icon", "default": p.get("defaultComponent") or None, "nullable": True,
                              "preferredValues": p.get("preferredValues") or [], "figma": fname})
                swap_props.append(n)
                if p.get("defaultComponent"):
                    default_icons.append(p["defaultComponent"])
            else:
                props.append({"name": n, "type": "unknown", "default": p.get("default"), "figma": fname})
        css_state_list = []
        for axis, vals in variants.items():
            low = [v.lower() for v in vals]
            default_v = variant_defaults.get(axis)
            if axis.lower() in ("state", "estado"):
                # estados de CSS (hover, press…) no son props; los de datos (disabled, loading…) son booleanos
                for v, vl in zip(vals, low):
                    if vl in css_states:
                        css_state_list.append(v)
                    elif vl in rest_values:
                        continue
                    else:
                        n = api_name(v); prop_names[n] = f"{axis}={v}"
                        props.append({"name": n, "type": "boolean", "default": (str(default_v) == v), "figma": f"{axis}={v}"})
                continue
            if set(low) <= bool_values:
                n = api_name(axis); prop_names[n] = axis
                props.append({"name": n, "type": "boolean", "default": (str(default_v).lower() in ("yes", "true", "on", "si", "sí")) if default_v is not None else False, "figma": axis})
                continue
            n = api_name(axis); prop_names[n] = axis
            props.append({"name": n, "type": "enum", "values": vals, "default": str(default_v) if default_v is not None else (vals[0] if vals else None), "figma": axis})

        # ── instancias anidadas, iconos, tokens (igual que antes) ──
        nested, uses, unexposed, anat_nested = [], [], [], []
        for n in c.get("nestedInstances", []) or []:
            comp = n.get("component") or "unknown"
            cs = self.resolve_slug(comp, n.get("componentSet"))
            # Para la huella de anatomía, una instancia sin contrato cuenta por el slug de su set o de su nombre: lo
            # mismo que escribía la 12.8.4, así que no caduca ninguna verificación.
            anat_nested.append(cs or slug(n.get("componentSet") or comp))
            nested.append({"layer": n.get("layer", "unknown"), "component": comp, "componentSlug": cs,
                           "exposedAs": n.get("exposedAs"), "toggledBy": n.get("toggledBy"),
                           "visibleByDefault": bool(n.get("visibleByDefault", True))})
            if cs and cs != s:
                # un componente no se usa a sí mismo: sería una relación falsa (y ds-fidelity heredaría sus propios tokens)
                uses.append(cs)
            if self.is_icon(comp) or self.is_icon(n.get("componentSet") or ""):
                if not n.get("exposedAs"):
                    unexposed.append(n.get("layer", "unknown"))
                    if not interno:  # una pieza interna no se construye: no tiene sentido pedirle un swap
                        self.findings.append(("warning", "icon-not-exposed-as-swap", f"{c['name']}: capa «{n.get('layer')}» ({comp}) sin INSTANCE_SWAP"))
        has_icon = bool(swap_props) or any(self.is_icon(n["component"]) or self.is_icon(n.get("componentSet") or "") for n in
                                           (c.get("nestedInstances") or []))
        bindings = c.get("bindings") or {}
        tokens_used = sorted({b.split(": ", 1)[-1] for b in bindings.get("variables", []) or []})

        def lista(x):
            return x if isinstance(x, list) else []
        exclusive = lista(old_api.get("exclusive")) or lista(old_api.get("invalidCombinations"))
        sch = {
            "$schema": "../_component.schema.json",
            "id": f"{kind}:{s}",
            "contractVersion": "2",
            "meta": {"name": c["name"], "slug": s, "kind": kind, "version": existing.get("meta", {}).get("version", "1.0.0"),
                     "lastSync": self.synced_at, "description": limpiar_texto(c.get("description")) or "unknown",
                     "figmaPage": c.get("page"), "figmaType": c.get("type"), "variantCount": c.get("variantCount", 1),
                     "autoLayout": c.get("autoLayout", "unknown")},
            "api": {
                "props": props,
                "cssStates": css_state_list,
                "events": lista(c["events"]) if "events" in c else lista(old_api.get("events")),
                "slots": [x for x in lista(c["slots"] if "slots" in c else old_api.get("slots")) if isinstance(x, dict)],
                "exclusive": exclusive,
                "icons": {"hasIcon": has_icon, "swapProperties": swap_props, "defaultIcons": default_icons,
                          "compatible": "any Icon / * via INSTANCE_SWAP" if swap_props else ("unknown" if has_icon else "none"),
                          "unexposedIconLayers": unexposed},
                "tokens": tokens_used,
            },
            "code": {"path": old_code.get("path", "design-system/css/components.css"),
                     "classes": (self.md_examples.get(s) or {}).get("classes", old_code.get("classes", [])),
                     "example": (self.md_examples.get(s) or {}).get("example", old_code.get("example")),
                     "classByProp": old_code.get("classByProp") if isinstance(old_code.get("classByProp"), dict) else {},
                     "stateAnatomy": lista(old_code.get("stateAnatomy")) or lista((existing.get("behavior") or {}).get("stateAnatomy")),
                     "package": old_code.get("package"), "import": old_code.get("import")},
            "figma": {"fileKey": c.get("fileKey") or self.file_key, "nodeId": c.get("id"), "componentKey": c.get("key"),
                      "propertyNames": prop_names, "variantAxes": variants, "nestedInstances": nested,
                      "variableBindings": bindings.get("variables", []) or [], "textStyles": bindings.get("textStyles", []) or []},
            "docs": {"file": f"design-system/docs/{DOCS_DIR[kind]}/{s}.md", "section": c["name"]},
            "relations": {"uses": sorted(set(uses)), "related": lista((existing.get("relations") or {}).get("related"))},
        }
        if isinstance(existing.get("accessibility"), dict) and existing["accessibility"]:
            sch["accessibility"] = existing["accessibility"]
        if c.get("anatomy"):
            # Solo con la fuente en el repo: capas, estados e interacciones tal como se diseñaron (Figma no las trae).
            sch["anatomy"] = c["anatomy"]
        if isinstance(existing.get("meta", {}).get("lifecycle"), dict):
            sch["meta"]["lifecycle"] = existing["meta"]["lifecycle"]
        # Huella de la anatomía: misma entrada que en la 11.x (key, ejes, propiedades de Figma, tokens, hijos),
        # para que migrar el contrato no caduque ninguna verificación.
        anat = {"key": c.get("key"), "variants": variants,
                "properties": sorted((p.get("name") or "", p.get("kind") or "", json.dumps([str(v) for v in (p.get("values") or [])] if p.get("kind") == "VARIANT" else None, ensure_ascii=False)) for p in raw_props),
                "tokensUsed": tokens_used, "nested": sorted(anat_nested)}
        sch["meta"]["anatomyHash"] = hashlib.sha1(json.dumps(anat, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:12]
        # Huella con la resolución de instancias anterior a la 12.8.4: si la verificación se hizo con ella, la anatomía
        # en Figma es la misma y solo cambió cómo se nombra un icono anidado; se traslada sin caducar la verificación.
        legacy = dict(anat, nested=sorted((self.resolve_slug_legacy(n.get("component") or "unknown", n.get("componentSet")) or n.get("component") or "")
                                          for n in c.get("nestedInstances", []) or []))
        legacy_hash = hashlib.sha1(json.dumps(legacy, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:12]
        old_ver = (existing.get("meta") or {}).get("verification")
        if isinstance(old_ver, dict) and old_ver:
            ver = dict(old_ver)
            if legacy_hash != sch["meta"]["anatomyHash"] and ver.get("figmaVersion") == legacy_hash:
                ver["figmaVersion"] = sch["meta"]["anatomyHash"]
                self.findings.append(("info", "verification-hash-migrated", f"{c['name']}: huella de verificación trasladada a la nueva forma de resolver iconos anidados; la anatomía en Figma no cambió"))
            colision = self.slug_count.get(s, 1) > 1
            mismo_maestro = not colision or not old_figma_key or old_figma_key == c.get("key")
            if mismo_maestro and ver.get("status") == "verified" and ver.get("figmaVersion") != sch["meta"]["anatomyHash"]:
                ver.update({"status": "stale", "staleSince": self.synced_at,
                            "reason": "la anatomía, las variantes, los tokens ligados o la key del maestro cambiaron desde la verificación"})
                self.findings.append(("warning", "verification-stale", f"{c['name']}: el maestro cambió desde que se verificó ({ver.get('date', '?')}); vuelve a pasar el protocolo de verificación"))
            elif ver.get("status") == "verified" and ver.get("figmaVersion") == sch["meta"]["anatomyHash"]:
                # re-verificado: el rastro de la caducidad anterior sobra, o parecería verificado y caducado a la vez
                ver.pop("staleSince", None); ver.pop("reason", None)
            elif mismo_maestro and ver.get("status") == "stale" and ver.get("figmaVersion") and ver.get("figmaVersion") == sch["meta"]["anatomyHash"]:
                # La huella vuelve a ser la verificada (se deshizo el cambio o se restauró el volcado): lo verificado
                # vuelve a valer tal cual, sin pasar otra vez el protocolo.
                ver["status"] = "verified"
                ver.pop("staleSince", None); ver.pop("reason", None)
                self.findings.append(("info", "verification-restored", f"{c['name']}: la anatomía vuelve a ser la verificada ({ver.get('date', '?')}); vuelve a «verified»"))
            sch["meta"]["verification"] = ver
        if (sch.get("figma") or {}).get("fileKey") == "repo":
            # Modo repo: no hay maestro de Figma con el que comparar; la fuente del repo es el maestro. El contrato consta como
            # verificado y no caduca; ds-fidelity sigue comprobando CSS, ejemplo, cobertura de variantes y contraste.
            sch["meta"]["verification"] = {"status": "verified", "date": self.synced_at[:10], "by": "fuente del repo",
                                           "figmaVersion": sch["meta"]["anatomyHash"],
                                           "note": "modo repo: la fuente (design-system/source/) es el maestro; se comprueba con ds-fidelity"}
        old_rules = existing.get("rules") or {}
        if any(old_rules.values()):
            self.keep_existing.add(s)
            self.findings.append(("critical", "criteria-only-in-schema",
                                  f"{c['name']}: el schema trae criterio en rules ({', '.join(k for k, v in old_rules.items() if v)}); "
                                  f"pásalo a {sch['docs']['file']} § {c['name']} y quita rules del schema. "
                                  f"Hasta entonces este schema no se regenera"))
        if has_icon and not nested and not swap_props:
            self.findings.append(("critical", "schema-missing-nested-instance", f"{c['name']}: tiene icono pero figma.nestedInstances está vacío"))
        if sch["code"]["example"] is None and not interno:
            self.findings.append(("warning", "code-example-missing-or-stale", f"{c['name']}: sin «Ejemplo de código» (code.example)"))
        # Marca en el contrato: cualquier herramienta lo sabe sin recalcularlo. Solo se escribe en los internos.
        if interno:
            sch["meta"]["internal"] = True
            sch["meta"]["internalReason"] = interno
        if c.get("published") is not None:
            sch["figma"]["published"] = bool(c.get("published"))
        return sch

    def live_block(self, sch):
        a, fg = sch["api"], sch["figma"]
        repo = fg.get("fileKey") == "repo"  # la fuente está en el repo (design-system/source), no en Figma
        L = [(f"- **Fuente:** `design-system/source/components/{sch['meta']['slug']}.json` · grupo «{sch['meta'].get('figmaPage')}» · "
              f"{sch['meta'].get('variantCount')} variantes · última sync {sch['meta']['lastSync']}") if repo else
             f"- **Figma:** `{fg['nodeId'] or 'unknown'}` · página «{sch['meta'].get('figmaPage')}» · {sch['meta'].get('figmaType')} · {sch['meta'].get('variantCount')} variantes · última sync {sch['meta']['lastSync']}",
             f"- **Descripción ({'fuente' if repo else 'Figma'}):** {sch['meta'].get('description') or 'unknown'}",
             "- **Anatomía:** " + (", ".join(f"`{n['layer']}` → {n['component']}" for n in fg["nestedInstances"]) or "sin instancias anidadas")]
        def pdesc(p):
            t = p["type"]
            if t == "enum":
                return f"`{p['name']}`: {', '.join(p.get('values') or [])}" + (f" (por defecto {p['default']})" if p.get("default") is not None else "")
            d = p.get("default")
            shown = str(d).lower() if t == "boolean" else str(d)
            return f"`{p['name']}` ({t}{', por defecto ' + shown if d not in (None, '') else ''})"
        L.append("- **API:** " + (" · ".join(pdesc(p) for p in a["props"]) or "sin propiedades"))
        if a["cssStates"]:
            L.append("- **Estados de CSS:** " + ", ".join(a["cssStates"]))
        if sch.get("anatomy") and sch["anatomy"].get("layers"):
            def _n(x):
                return 1 + sum(_n(c) for c in (x.get("children") or []) if isinstance(c, dict))
            L.append(f"- **Anatomía diseñada:** {_n(sch['anatomy']['layers'])} capas · {len(sch['anatomy'].get('interactions') or [])} interacciones · "
                     f"{len(a.get('slots') or [])} slots (detalle en el contrato, `anatomy`)")
        if fg["propertyNames"]:
            L.append(("- **Nombres para Figma:** " if repo else "- **Nombres en Figma:** ") + ", ".join(f"`{k}` ← `{v}`" for k, v in fg["propertyNames"].items()))
        ic = a["icons"]
        if ic["hasIcon"]:
            L.append(f"- **Iconos / instancias anidadas:** sí · swap: {', '.join(f'`{x}`' for x in ic['swapProperties']) or 'ninguna (⚠️ no expuesto)'} · por defecto: {', '.join(ic['defaultIcons']) or 'unknown'}"
                     + (f" · capas sin swap: {', '.join(ic['unexposedIconLayers'])}" if ic["unexposedIconLayers"] else ""))
        else:
            L.append("- **Iconos / instancias anidadas:** ninguno")
        L.append("- **Tokens que consume:** " + (", ".join(f"`{t}`" for t in a["tokens"]) or "unknown"))
        if fg["textStyles"]:
            L.append("- **Text styles:** " + ", ".join(f"`{t}`" for t in fg["textStyles"]))
        return "\n".join(L)


MANUAL_FIELDS = ["Propósito", "Ejemplo de código", "Accesibilidad (rol, nombre, estados y teclado)", "Cuándo usar / qué NO hace"]

# 12.7.0: el campo se llamaba «Accesibilidad (pares AA verificados)», y el nombre hacía pensar que AA era opcional
# y se apuntaba a mano. AA es obligatorio y lo mide ds-fidelity desde el CSS; el campo es para lo que el color
# no cubre. La migración cambia solo la etiqueta: lo escrito debajo se conserva tal cual.
A11Y_OLD, A11Y_NEW = "Accesibilidad (pares AA verificados)", "Accesibilidad (rol, nombre, estados y teclado)"
A11Y_OLD_EXPL = '- **Accesibilidad (pares AA verificados):** los pares texto/fondo comprobados en claro y oscuro; el\n  *rol*'
A11Y_NEW_EXPL = '- **Accesibilidad (rol, nombre, estados y teclado):** lo que el color no cubre. El contraste AA no se\n  escribe aquí: es obligatorio siempre, lo mide `ds-fidelity` desde el CSS (`contrast-below-aa`) y la\n  library lo enseña en la ficha. Aquí va el *rol*'


def migrar_a11y(texto):
    # primero la explicación entera del índice (empieza por la etiqueta vieja), después la etiqueta suelta
    nuevo = texto.replace(A11Y_OLD_EXPL, A11Y_NEW_EXPL).replace(f"- **{A11Y_OLD}:**", f"- **{A11Y_NEW}:**")
    return nuevo, nuevo != texto


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
                     "- **Ejemplo de código:** ⬜ TODO _(snippet HTML mínimo con las clases reales de `components.css`; su elemento raíz lleva data-ds=\"<slug>\"; se copia a `code.example` del schema)_\n  ```html\n  <!-- ⬜ TODO -->\n  ```"
                     for f in MANUAL_FIELDS)


def ficha_heading(name, date):
    return f"### {name}   ⚙️ synced: {date}"


def new_ficha(name, s, date, live, interno=None):
    if interno:
        # Una pieza interna se documenta solo para tener trazabilidad con Figma: sin campos de criterio pendientes.
        return (f"{ficha_heading(name, date)}\n\n{GEN_START.format(s)}\n{live}\n{GEN_END.format(s)}\n\n"
                f"> **Pieza interna de Figma** ({interno}). No forma parte del sistema compartido ni se construye: "
                f"no lleva propósito, accesibilidad ni ejemplo de código.\n")
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


OLD_EXAMPLE_HINT = "_(snippet HTML mínimo con las clases reales de `components.css`; se copia a `source.code.example` del schema)_"
NEW_EXAMPLE_HINT = "_(snippet HTML mínimo con las clases reales de `components.css`; su elemento raíz lleva data-ds=\"<slug>\"; se copia a `code.example` del schema)_"


def upsert_ficha_file(text, sch, live):
    """Ficha en docs/<carpeta>/<slug>.md: crea el archivo si no existe o sustituye solo su bloque GENERATED
    (y la fecha del heading). Todo lo manual que haya debajo se conserva tal cual. Única excepción: la
    pista de relleno del «Ejemplo de código» que escribió la propia plantilla 11.x (no es texto de una
    persona) se actualiza al contrato 12.0.0."""
    name, s, date = sch["meta"]["name"], sch["meta"]["slug"], sch["meta"]["lastSync"]
    interno = sch["meta"].get("internalReason") if sch["meta"].get("internal") else None
    if not text:
        return new_ficha(name, s, date, live, interno)
    text = text.replace(OLD_EXAMPLE_HINT, NEW_EXAMPLE_HINT)
    gs, ge = GEN_START.format(s), GEN_END.format(s)
    m = re.compile(rf"^### {re.escape(name)}(?:\s{{2,}}.*)?$", re.M).search(text)
    if m is None and gs in text:
        # mismo slug, otro nombre (renombrado en Figma): el heading que precede al bloque es el suyo
        prev = [h for h in re.finditer(r"^### .*$", text, re.M) if h.start() < text.index(gs)]
        m = prev[-1] if prev else None
    if m is None:
        return text.rstrip("\n") + "\n\n" + new_ficha(name, s, date, live, interno)
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


NODE_EN_BLOQUE_RE = re.compile(r"- \*\*Figma:\*\* `([^`]+)`")


def reasignar_secciones(files, vivos):
    """Una ficha puede guardar una sección de un componente que ya no es suyo: con un slug compartido las dos
    secciones viven en el mismo archivo y, al resolver la colisión renombrando uno en Figma, su sección se
    quedaba en la ficha antigua. Se reconoce por el nodeId del bloque GENERATED: si no es de ningún schema de
    esa ficha, se mueve a la ficha de su slug nuevo (la parte manual incluida, si la ficha nueva está en
    blanco) o, si el componente ya no existe, se avisa. `vivos` es {nodeId: slug} de TODOS los componentes
    del volcado, no solo de los schemas escritos: con un slug compartido solo se escribe el último maestro
    y el otro sigue existiendo en Figma (su sección se queda donde está). Devuelve (notas, huérfanas)."""
    por_slug = {}
    for nodo, sl in vivos.items():
        por_slug.setdefault(sl, set()).add(nodo)
    slug_de_nodo = dict(vivos)
    notas, huerfanas = [], []
    for sl in list(files):
        trozos = re.split(r"(?m)^(?=### )", files[sl])
        keep, movidas = [], []
        for t in trozos:
            if not t.startswith("### "):
                keep.append(t); continue
            m = NODE_EN_BLOQUE_RE.search(t)
            nodo = m.group(1) if m else None
            if nodo is None or nodo in por_slug.get(sl, set()):
                keep.append(t); continue
            destino = slug_de_nodo.get(nodo)
            nombre = t.splitlines()[0][4:].split("   ")[0].strip()
            if destino and destino in files and destino != sl:
                gen_end = GEN_END.format(destino)
                manual_vieja = t.split(GEN_END.format(sl), 1)[1] if GEN_END.format(sl) in t else ""
                dst = files[destino]
                if gen_end in dst:
                    cab, manual_nueva = dst.split(gen_end, 1)
                    fresca = all("⬜ TODO" in l for l in manual_nueva.splitlines() if l.startswith("- **"))
                    if fresca and manual_vieja.strip():
                        files[destino] = cab + gen_end + manual_vieja.rstrip("\n") + "\n"
                        notas.append(f"{sl}.md: la sección de «{nombre}» ({nodo}) pasa a {destino}.md con su parte manual")
                    else:
                        notas.append(f"{sl}.md: la sección de «{nombre}» ({nodo}) se retira; {destino}.md ya tenía criterio propio y no se ha pisado")
                    movidas.append(t)
                    continue
            huerfanas.append((sl, nombre, nodo))
            keep.append(t)
        if movidas:
            files[sl] = re.sub(r"\n{3,}", "\n\n", "".join(keep)).rstrip("\n") + "\n"
    return notas, huerfanas


def limpiar_texto(t):
    """Texto de Figma (descripciones) sin entidades HTML ni espacios duros: leer dos veces lo mismo da lo mismo."""
    return htmllib.unescape(t or "").replace("\xa0", " ")


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
            ex = sch["code"]["example"]
            demo = f'<div class="sc-demo">{ex}</div><pre class="sc-code">{esc(ex)}</pre>' if ex else '<div class="sc-demo"><span class="sc-tag">sin «Ejemplo de código» en el contrato</span></div>'
            tag = f"{sch['meta'].get('variantCount', 1)} variantes · {sch['figma']['nodeId'] or 'unknown'}" + (" · icono" if sch["api"]["icons"]["hasIcon"] else "")
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


def media_sort_key(query):
    """max-width: de mayor a menor (0, -ancho); min-width: de menor a mayor (1, ancho); otros, al final."""
    m = re.search(r"max-width:\s*([\d.]+)", query)
    if m:
        return (0, -float(m.group(1)))
    m = re.search(r"min-width:\s*([\d.]+)", query)
    if m:
        return (1, float(m.group(1)))
    return (2, 0)


def check_media_order(css):
    """Devuelve un mensaje si los bloques @media de tokens.css no van en orden de cascada (ver media_sort_key)."""
    queries = re.findall(r"^@media\s+(.+?)\s*\{", css or "", re.M)
    keys = [media_sort_key(q) for q in queries]
    if keys != sorted(keys):
        return "los bloques @media no van en orden de cascada (" + " → ".join(queries) + ")"
    return None


# ────────────────────────────── huellas de variables (sync incremental) ──────────────────────────────
def _canon(x):
    """Forma canónica idéntica a la del script de huellas de design.md: claves ordenadas, números a 6 decimales."""
    if x is None:
        return "null"
    if isinstance(x, bool):
        return "true" if x else "false"
    if isinstance(x, int):
        return str(x)
    if isinstance(x, float):
        return str(int(x)) if x.is_integer() else repr(round(x, 6))
    if isinstance(x, str):
        return json.dumps(x, ensure_ascii=False)
    if isinstance(x, list):
        return "[" + ",".join(_canon(v) for v in x) + "]"
    return "{" + ",".join(json.dumps(k, ensure_ascii=False) + ":" + _canon(x[k]) for k in sorted(x)) + "}"


def huella_variable(v):
    """FNV-1a (32 bits, por code point) de la forma canónica de una variable: la misma que calcula el script de
    lectura en Figma (campo `h`). Para volcados anteriores, que no la traen, se calcula aquí."""
    e = {k: v.get(k) for k in ("name", "type", "description", "scopes", "codeSyntax", "hiddenFromPublishing", "valuesByMode")}
    e["scopes"] = e.get("scopes") or []
    e["codeSyntax"] = e.get("codeSyntax") or {}
    e["description"] = e.get("description") or ""
    h = 0x811C9DC5
    for ch in _canon(e):
        h ^= ord(ch)
        h = (h * 16777619) & 0xFFFFFFFF
    return "%08x" % h


def variables_diff(ds, dry):
    """Sync incremental: compara las huellas leídas de Figma (sync/parts/fingerprints-*.json, script de huellas) con
    sync/variables.json. Imprime cambiadas, nuevas y desaparecidas, la línea VARIABLE_IDS para el refresco puntual,
    y deja un trozo refresh con part.removed para que --merge retire las desaparecidas. Devuelve el código de salida."""
    parts_dir = os.path.join(ds, "sync", "parts")
    paths = sorted(glob.glob(os.path.join(parts_dir, "fingerprints-*.json")))
    if not paths:
        print("[ERROR] no hay huellas en sync/parts/fingerprints-*.json: ejecuta el «script de huellas de variables» (design.md § Sync) y guarda la respuesta ahí")
        return 1
    partes = []
    for pth in paths:
        texto = read(pth) or ""
        if TRUNCATED_RE.search(texto):
            print(f"[ERROR] {os.path.relpath(pth)}: la respuesta llegó cortada; vuelve a pedirla"); return 1
        try:
            d = json.loads(texto)
        except json.JSONDecodeError as e:
            print(f"[ERROR] {os.path.relpath(pth)}: JSON inválido ({e})"); return 1
        if d.get("kind") != "variable-fingerprints" or not isinstance(d.get("part"), dict):
            print(f"[ERROR] {os.path.relpath(pth)}: no es la salida del script de huellas (kind variable-fingerprints)"); return 1
        partes.append(d)
    partes.sort(key=lambda d: d["part"].get("offset", 0))
    esperado, leidas = 0, {}
    for d in partes:
        if d["part"].get("offset", 0) != esperado:
            print(f"[ERROR] huellas: falta el trozo que empieza en {esperado} (llegó uno que empieza en {d['part'].get('offset')})"); return 1
        for it in d.get("items") or []:
            if isinstance(it, list) and len(it) >= 2:
                leidas[it[0]] = it[1]
        esperado += d["part"].get("count", 0)
    ultimo = partes[-1]["part"]
    if ultimo.get("nextOffset") is not None or esperado != ultimo.get("total"):
        print(f"[ERROR] huellas a medias: leídas {esperado} de {ultimo.get('total')}; repite el script con OFFSET = {ultimo.get('nextOffset')}"); return 1
    key = partes[0].get("fileKey") or partes[0].get("fileName") or "unknown"
    v_path = os.path.join(ds, "sync", "variables.json")
    var = read_json(v_path, None) or {}
    # Las huellas traen también la key de librería de cada variable y de cada colección (no cambian nunca): se
    # completan en el volcado si faltan, para poder cruzarlas con lo que ligan los componentes (library-audit).
    keys_var = {it[0]: it[2] for d in partes for it in (d.get("items") or []) if isinstance(it, list) and len(it) >= 3 and it[2]}
    keys_col = {c.get("id"): c for d in partes for c in (d.get("collections") or []) if c.get("id") and c.get("key")}
    keys_sty = {x.get("id"): x.get("key") for d in partes for x in (d.get("styles") or []) if x.get("id") and x.get("key")}
    completadas = 0
    for c in var.get("collections") or []:
        if not c.get("key") and keys_col.get(c.get("id")):
            c["key"] = keys_col[c["id"]]["key"]; completadas += 1
        for v in c.get("variables") or []:
            if not v.get("key") and keys_var.get(v.get("id")):
                v["key"] = keys_var[v["id"]]; completadas += 1
    for lista in ("textStyles", "effectStyles"):
        for x in var.get(lista) or []:
            if not x.get("key") and keys_sty.get(x.get("id")):
                x["key"] = keys_sty[x["id"]]; completadas += 1
    if completadas and not dry:
        write_json(v_path, var, False, [])
        print(f"ds-sync · {completadas} key(s) de librería completadas en sync/variables.json (variables, colecciones y estilos)")
    en_volcado = {}
    for c in var.get("collections") or []:
        if c.get("source") not in (None, "", key) and c.get("fileKey") not in (None, "", key):
            continue
        for v in c.get("variables") or []:
            en_volcado[v.get("id")] = (v.get("name"), v.get("h") or huella_variable(v))
    cambiadas = sorted(i for i, h in leidas.items() if i in en_volcado and en_volcado[i][1] != h)
    nuevas = sorted(i for i in leidas if i not in en_volcado)
    desaparecidas = sorted(i for i in en_volcado if i not in leidas)
    if not (cambiadas or nuevas or desaparecidas):
        print(f"ds-sync · huellas: {len(leidas)} variables, ninguna ha cambiado desde el volcado. Nada que releer.")
    else:
        if cambiadas:
            print(f"ds-sync · {len(cambiadas)} variable(s) cambiada(s): " + ", ".join(f"{en_volcado[i][0]} ({i})" for i in cambiadas[:40]) + (" …" if len(cambiadas) > 40 else ""))
        if nuevas:
            print(f"ds-sync · {len(nuevas)} variable(s) nueva(s) en Figma: " + ", ".join(nuevas[:40]) + (" …" if len(nuevas) > 40 else ""))
        if desaparecidas:
            print(f"ds-sync · {len(desaparecidas)} variable(s) desaparecida(s) de Figma: " + ", ".join(f"{en_volcado[i][0]} ({i})" for i in desaparecidas[:40]))
        if cambiadas or nuevas:
            print("\nRefresco puntual (script de variables, design.md § Sync), guarda la respuesta en sync/parts/ y ejecuta --merge:")
            print("const VARIABLE_IDS = " + json.dumps(cambiadas + nuevas) + ";")
        if desaparecidas:
            pth = os.path.join(parts_dir, "variables-removed.json")
            trozo = {"kind": "variables", "fileKey": partes[0].get("fileKey"), "fileName": partes[0].get("fileName"), "readAt": partes[0].get("readAt"),
                     "part": {"offset": 0, "nextOffset": None, "count": 0, "total": 0, "refresh": True, "missing": [], "removed": desaparecidas},
                     "collections": [], "textStyles": [], "effectStyles": []}
            if not dry:
                with open(pth, "w", encoding="utf-8") as fh:
                    json.dump(trozo, fh, ensure_ascii=False, indent=2)
            print(f"\nLas desaparecidas se retiran del volcado con --merge: trozo preparado en {os.path.relpath(pth)} (part.removed). "
                  f"Si alguna otra variable les hace alias, --merge lo dirá y no escribirá nada.")
    if not dry:
        for pth in paths:
            os.remove(pth)
    return 0


def library_keys(ds):
    """Imprime las constantes KNOWN_COLLECTION_KEYS y KNOWN_STYLE_KEYS para el «script de auditoría de librerías
    ligadas» (design.md § Sync), a partir de las keys del volcado de variables."""
    var = read_json(os.path.join(ds, "sync", "variables.json"), None) or {}
    vks = sorted({v.get("key") for c in var.get("collections") or [] for v in c.get("variables") or [] if v.get("key")})
    sty = sorted({x.get("key") for lista in ("textStyles", "effectStyles") for x in var.get(lista) or [] if x.get("key")})
    if not vks:
        print("[ERROR] el volcado de variables no tiene keys de librería todavía: ejecuta el script de huellas y "
              "`ds-sync.py --variables-diff` (las completa), o relee las variables con el script de la 12.12.0")
        return 1
    sin = sum(1 for c in var.get("collections") or [] for v in c.get("variables") or [] if not v.get("key"))
    print(f"// {len(vks)} variables y {len(sty)} estilos de {var.get('fileName') or var.get('fileKey')}" + (f" · {sin} variable(s) sin key" if sin else ""))
    print("const KNOWN_VARIABLE_KEYS = " + json.dumps(vks) + ";")
    print("const KNOWN_STYLE_KEYS = " + json.dumps(sty) + ";")
    return 0


def library_audit_findings(ds, raw_vars, internos=frozenset()):
    """Lee sync/library-audit/*.json (salida del script de auditoría de librerías ligadas, por archivo y trozos) y
    devuelve hallazgos: crítico por componente que liga variables de una librería que no es la declarada, aviso por
    estilos remotos que tampoco lo son. Una auditoría a medias (faltan trozos) se aparta con aviso. Un componente
    interno con variables ajenas sigue contando (arrastra el problema en Figma) pero como aviso, no como crítico."""
    out = []
    folder = os.path.join(ds, "sync", "library-audit")
    paths = sorted(glob.glob(os.path.join(folder, "*.json")))
    if not paths:
        return out, {}
    # El nombre del archivo lo da el manifiesto por su fileKey: figma.root.name devuelve «Document» en el MCP.
    manifest = read_json(os.path.join(ds, "agent-manifest.json"), {}) or {}
    nombre_por_key = {src.get("fileKey"): src.get("name") for src in manifest.get("figmaSources") or [] if src.get("fileKey")}
    def nombre_archivo(fk, dicho):
        return nombre_por_key.get(fk) or (dicho if dicho and dicho != "Document" else None) or fk
    por_archivo = {}
    for pth in paths:
        d = read_json(pth, None)
        if not isinstance(d, dict) or d.get("kind") != "library-bindings" or not isinstance(d.get("part"), dict):
            out.append(("warning", "library-audit-invalid", f"{os.path.relpath(pth)}: no es la salida del script de auditoría de librerías ligadas"))
            continue
        por_archivo.setdefault(d.get("fileKey") or d.get("fileName") or os.path.basename(pth), []).append(d)
    resumen = {}
    for fk, partes in por_archivo.items():
        partes.sort(key=lambda x: x["part"].get("offset", 0))
        esperado = 0; ok = True
        for d in partes:
            if d["part"].get("offset", 0) != esperado:
                ok = False; break
            esperado += d["part"].get("count", 0)
        ultimo = partes[-1]["part"]
        if not ok or ultimo.get("nextOffset") is not None or esperado != ultimo.get("total"):
            out.append(("warning", "library-audit-incomplete", f"auditoría de librerías de «{nombre_archivo(fk, partes[0].get('fileName'))}» a medias "
                        f"({esperado} de {ultimo.get('total')} componentes): repite el script desde OFFSET = {ultimo.get('nextOffset')}"))
            continue
        nombre = nombre_archivo(fk, partes[0].get("fileName"))
        comps = [c for d in partes for c in (d.get("components") or [])]
        n_var = n_sty = 0
        for c in comps:
            fv = c.get("foreignVariables") or []
            fs = c.get("foreignStyles") or []
            if fv:
                n_var += 1
                libs = sorted({(x.get("collectionName") or "?") + (f" [{x.get('collectionKey')}]" if x.get("collectionKey") else "") for x in fv})
                def donde(x):
                    w = x.get("where") or []
                    if not w:
                        return x.get("name") or "?"
                    sitios = ", ".join(f"{(s_.get('nodeId') or '?')} {s_.get('prop') or '?'}" + (" (en una instancia anidada)" if s_.get("viaInstance") else "") for s_ in w[:3])
                    return f"{x.get('name') or '?'} [{sitios}{' …' if len(w) > 3 else ''}]"
                todas_heredadas = all((x.get("where") or []) and all(s_.get("viaInstance") for s_ in x["where"]) for x in fv)
                out.append(("warning" if c.get("name") in internos else "critical", "variable-from-foreign-library",
                            f"{c.get('name')} (página «{(c.get('page') or '').strip()}», archivo «{nombre}»): liga {len(fv)} variable(s) de una librería que no es la "
                            f"Foundations declarada ({'; '.join(libs)}): {'; '.join(donde(x) for x in fv[:8])}{' …' if len(fv) > 8 else ''}. "
                            + ("Todas vienen de instancias anidadas: arréglalas en el componente de origen. " if todas_heredadas else "")
                            + "Arreglo en design.md § Sync (Swap library)"))
            if fs:
                n_sty += 1
                out.append(("warning", "style-from-foreign-library",
                            f"{c.get('name')} (página «{(c.get('page') or '').strip()}», archivo «{nombre}»): usa {len(fs)} estilo(s) remoto(s) que no vienen de la librería declarada: "
                            + ", ".join(f"{x.get('name')} ({x.get('type')})" for x in fs[:10])))
        resumen[fk] = {"fileName": nombre, "readAt": partes[0].get("readAt"), "components": ultimo.get("total"),
                       "withForeignVariables": n_var, "withForeignStyles": n_sty}
    return out, resumen


# ────────────────────────────── volcado: trozos y validación ──────────────────────────────
def fold_parts(ds, dry, strict=False):
    """Une los trozos de sync/parts/ en variables.json y components.json. Devuelve (unidos, errores, avisos).

    Determinista: los trozos se ordenan por archivo de tokens o página y por posición, no por el
    nombre con que se guardaron. Si falta un trozo en medio de una cadena, no se escribe nada.

    La cadena de variables de cada archivo se valida entera antes de unirla (del primer trozo hasta
    nextOffset null, sin huecos, read == total). Si está incompleta: en un `--merge` explícito con solo
    trozos de variables (la relectura en curso) es un error y no se escribe nada; en cualquier otro caso
    (el merge viene de un refresco de componentes, o es la unión previa a generar) los trozos de variables
    se dejan en sync/parts/ sin tocar, variables.json se conserva y se avisa. Así un volcado de variables a
    medias nunca llega a tokens.css, y una relectura a medias no bloquea generar con el volcado anterior."""
    parts_dir = os.path.join(ds, "sync", "parts")
    paths = sorted(p for p in glob.glob(os.path.join(parts_dir, "*.json")) if not os.path.basename(p).startswith("fingerprints-"))
    if not paths:
        return 0, [], []
    errores, avisos, partes = [], [], []
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
        if d.get("kind") == "variable-fingerprints":
            continue  # son para --variables-diff, no se unen al volcado
        if d.get("kind") not in ("variables", "components") or not isinstance(d.get("part"), dict):
            errores.append(f"{os.path.relpath(pth)}: no es un trozo de los scripts de lectura (falta kind o part)")
            continue
        d["_path"] = pth
        partes.append(d)
    if errores:
        return 0, errores, []

    v_path, c_path = os.path.join(ds, "sync", "variables.json"), os.path.join(ds, "sync", "components.json")
    var = read_json(v_path, None) or {}
    var.setdefault("collections", []); var.setdefault("textStyles", []); var.setdefault("effectStyles", [])
    var.setdefault("readProgress", {})
    com = read_json(c_path, None) or {}
    com.setdefault("pages", [])

    def clave_var(d):
        return d.get("fileKey") or d.get("fileName") or "unknown"

    cadenas = {}  # por archivo de tokens: trozos de la relectura completa, para validar la cadena entera
    for d in sorted((x for x in partes if x["kind"] == "variables"), key=lambda x: (clave_var(x), x["part"].get("offset", 0))):
        k, pt = clave_var(d), d["part"]
        if pt.get("refresh"):
            # Refresco puntual (VARIABLE_IDS / VARIABLE_NAMES en el script de lectura): cada variable se sustituye por
            # id esté en la colección que esté (pudo cambiar de colección) o se añade a la suya; los alias se resuelven
            # después contra el volcado completo (check_dump). readAt no se toca; queda en partialRefresh.history.
            faltan = [str(x) for x in (pt.get("missing") or []) if x]
            if faltan:
                avisos.append(f"variables de {k}: {len(faltan)} pedida(s) no existe(n) en Figma: {', '.join(faltan[:8])}")
            nombres, nuevas = [], 0
            retiradas = [str(x) for x in (pt.get("removed") or []) if x]
            if retiradas:
                quitadas = 0
                for c in var["collections"]:
                    antes = len(c.get("variables") or [])
                    c["variables"] = [x for x in c.get("variables") or [] if x.get("id") not in retiradas]
                    quitadas += antes - len(c["variables"])
                prog_r = var["readProgress"].get(k)
                if prog_r and quitadas:
                    prog_r["read"] = max(0, (prog_r.get("read") or 0) - quitadas)
                    prog_r["total"] = max(0, (prog_r.get("total") or 0) - quitadas)
                nombres.append(f"{quitadas} retirada(s)")
            for col in d.get("collections") or []:
                dest = next((c for c in var["collections"] if c.get("id") == col.get("id")), None)
                if dest is None:
                    dest = {**{kk: vv for kk, vv in col.items() if kk != "variables"}, "fileKey": d.get("fileKey"), "source": k, "variables": []}
                    var["collections"].append(dest)
                for v in col.get("variables") or []:
                    nombres.append(v.get("name") or v.get("id"))
                    donde = next(((c, i) for c in var["collections"] for i, x in enumerate(c.get("variables") or []) if x.get("id") == v.get("id")), None)
                    if donde is not None and donde[0] is dest:
                        dest["variables"][donde[1]] = v
                    else:
                        if donde is not None:
                            del donde[0]["variables"][donde[1]]
                        else:
                            nuevas += 1
                        dest.setdefault("variables", []).append(v)
            for lista in ("textStyles", "effectStyles"):
                for x in d.get(lista) or []:
                    x = {**x, "source": k}
                    i = next((i for i, y in enumerate(var[lista]) if y.get("id") == x.get("id")), None)
                    if i is None:
                        var[lista].append(x); nuevas += 1
                    else:
                        var[lista][i] = x
                    nombres.append(x.get("name") or x.get("id"))
            prog = var["readProgress"].get(k)
            if prog and nuevas:
                prog["read"] = (prog.get("read") or 0) + nuevas
                prog["total"] = (prog.get("total") or 0) + nuevas
            # El nombre del archivo: el que ya tiene el volcado para esa clave (un refresco desde el MCP puede devolver
            # «Document» en figma.root.name), y si no, el del trozo o la clave.
            nombre_archivo = d.get("fileName")
            if not nombre_archivo or nombre_archivo == "Document":
                nombre_archivo = (var.get("fileName") if var.get("fileKey") == k else None) or next(
                    (c.get("fileName") for c in var["collections"] if c.get("source") == k and c.get("fileName")), None) or nombre_archivo or k
            var.setdefault("partialRefresh", {"history": []}).setdefault("history", []).append(
                {"at": d.get("readAt"), "what": f"refresco puntual de {len(nombres)} variable(s)/estilo(s) de «{nombre_archivo}» con VARIABLE_IDS/VARIABLE_NAMES + --merge",
                 "scope": ", ".join(nombres), "missing": faltan})
            continue
        cadenas.setdefault(k, []).append(d)
        prog = var["readProgress"].get(k)
        if pt.get("offset", 0) == 0:
            # empieza de cero lo de este archivo de tokens. Las entradas sin «source» (volcados anteriores al
            # mecanismo de trozos o migrados) son de este archivo si no dicen otro fileKey: si se dejaran, una
            # relectura completa las duplicaría y el merge se bloquearía por IDs repetidos.
            def de_este(x):
                return x.get("source") == k or (not x.get("source") and x.get("fileKey") in (None, "", k))
            var["collections"] = [c for c in var["collections"] if not de_este(c)]
            var["textStyles"] = [x for x in var["textStyles"] if not de_este(x)]
            var["effectStyles"] = [x for x in var["effectStyles"] if not de_este(x)]
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

    # Cadena entera o nada: del primer trozo (offset 0) hasta nextOffset null, sin huecos y con read == total.
    hay_c_partes = any(x["kind"] == "components" for x in partes)
    incompletas = []
    for k, ds_ in cadenas.items():
        ultimo = max(ds_, key=lambda x: x["part"].get("offset", 0))["part"]
        prog = var["readProgress"].get(k) or {}
        if ds_[0]["part"].get("offset", 0) != 0 or ultimo.get("nextOffset") is not None or prog.get("read") != prog.get("total"):
            incompletas.append((k, prog.get("read"), prog.get("total"), len(ds_)))
    if incompletas:
        detalle = "; ".join(f"variables de {k}: {len_} trozo(s), leídas {r} de {t}" for k, r, t, len_ in incompletas)
        if strict and not hay_c_partes:
            return 0, [f"la relectura de variables está a medias ({detalle}). Sigue leyendo desde el part.nextOffset del último trozo "
                       f"y vuelve a unir cuando nextOffset sea null; los trozos se conservan y no se ha escrito nada"], []
        # Viene de un refresco de componentes: las variables a medias se apartan, variables.json queda como estaba.
        avisos.append(f"relectura de variables a medias, apartada de este merge ({detalle}): sync/variables.json se conserva y sus trozos "
                      f"siguen en sync/parts/; termina de leerla y vuelve a unir")
        apartados = {d["_path"] for k, _, _, _ in incompletas for d in cadenas[k]}
        partes = [x for x in partes if x.get("_path") not in apartados]
        paths = [p for p in paths if p not in apartados]
        var = read_json(v_path, None) or {}

    if any(x["kind"] == "variables" for x in partes):
        # Red de seguridad: si una entrada sin origen tiene el mismo id que una leída con origen, sobra la
        # antigua (la lectura nueva es la fuente).
        for lista in ("collections", "textStyles", "effectStyles"):
            con_origen = {x.get("id") for x in var[lista] if x.get("source")}
            var[lista] = [x for x in var[lista] if x.get("source") or x.get("id") not in con_origen]
        ids_var = {v.get("id") for c in var["collections"] if c.get("source") for v in c.get("variables") or []}
        for c in var["collections"]:
            if not c.get("source"):
                c["variables"] = [v for v in c.get("variables") or [] if v.get("id") not in ids_var]
        var["collections"] = [c for c in var["collections"] if c.get("source") or c.get("variables")]

    for d in sorted((x for x in partes if x["kind"] == "components"),
                    key=lambda x: ((x.get("page") or {}).get("id") or "", x["part"].get("offset", 0))):
        pg, pt = d.get("page") or {}, d["part"]
        dest = next((p for p in com["pages"] if p.get("id") == pg.get("id")), None)
        if pt.get("refresh"):
            # Refresco puntual (NODE_IDS en el script de lectura): se sustituyen esos componentes por id en su
            # página, el resto queda como estaba, y queda anotado en partialRefresh.history.
            ids, nuevos = [], []
            for c in d.get("components") or []:
                c = dict(c)
                ids.append(c.get("id"))
                # El componente se busca por su id en TODO el volcado, no por la página del trozo: la lectura completa
                # pudo guardarlo con otro nombre o id de página (p. ej. «Patterns / X», o una sección del archivo), y el
                # refresco trae la página real de Figma. De «page» salen kind (patrón o componente), figmaPage y la ruta
                # de la ficha: se conserva la que ya tenía en el volcado y se sustituye en su sitio.
                donde = next(((p, k) for p in com["pages"] for k, x in enumerate(p.get("components") or [])
                              if x.get("id") == c.get("id")), None)
                if donde is not None:
                    p_old, k = donde
                    c["page"] = (p_old["components"][k].get("page") or p_old.get("name") or c.get("page") or "").strip()
                    p_old["components"][k] = c
                elif dest is not None:
                    c["page"] = (dest.get("name") or c.get("page") or "").strip()
                    dest.setdefault("components", []).append(c)
                else:
                    nuevos.append((c.get("name") or "").strip() or c.get("id"))
            if nuevos:
                errores.append(f"página {(pg.get('name') or '').strip()}: el refresco trae componentes que no están en el volcado "
                               f"({', '.join(nuevos)}) y esa página no se ha leído entera; léela completa (sin NODE_IDS) "
                               f"o refresca solo componentes que ya estén en el volcado")
                continue
            com.setdefault("partialRefresh", {"history": []}).setdefault("history", []).append(
                {"at": d.get("readAt"), "what": f"refresco puntual de {len(ids)} componente(s) de «{(pg.get('name') or '').strip()}» con NODE_IDS + --merge",
                 "scope": ", ".join(f"{(c.get('name') or '').strip()} ({c.get('id')})" for c in d.get("components") or []), "nodeIds": ids})
            # readAt del volcado no se toca: sigue siendo la fecha de la lectura completa; el refresco queda en history.
            continue
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
        return 0, errores, []
    if not partes:
        return 0, [], avisos
    # Se valida el resultado en memoria ANTES de escribir: si no es válido, variables.json, components.json y
    # sync/parts/ quedan como estaban, para poder corregir y repetir el merge.
    hay_v = any(x["kind"] == "variables" for x in partes)
    hay_c = any(x["kind"] == "components" for x in partes)
    errores, _ = check_dump(var if hay_v else read_json(v_path, None), com if hay_c else read_json(c_path, None), {})
    if errores:
        return 0, errores + ["el resultado de unir los trozos no es válido: no se ha escrito nada y sync/parts/ se conserva"], []
    escritos = []
    if hay_v:
        write_json(v_path, var, dry, escritos)
    if hay_c:
        write_json(c_path, com, dry, escritos)
    if not dry:
        for pth in paths:
            os.remove(pth)
    return len(partes), [], avisos


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
            sin_origen = [x for x in (raw_vars.get("collections") or []) + (raw_vars.get("textStyles") or []) + (raw_vars.get("effectStyles") or [])
                          if not x.get("source")]
            motivo = ("hay entradas antiguas sin «source» en el volcado junto a la lectura nueva; vuelve a unir con --merge "
                      "(desde la 12.5.2 las retira) o quítalas del volcado" if sin_origen else "un trozo se guardó dos veces")
            errores.append(f"variables.json: {len(rep)} IDs repetidos ({', '.join(rep[:5])}): {motivo}")
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
def marcar_base_inicial(ds, dry=False):
    """Base inicial de componentes (12.22.0): solo la recibe un proyecto NUEVO que la elige al crearse, y eso lo dice
    `starterBase: "pending"` en su manifest. Un proyecto anterior (sin la marca) o que ya empezó su design system, con Figma,
    en el repo o vacío, queda marcado «not-applicable»: la base nunca se carga en él. Se marca sola, lo primero que hace el
    sync (antes de cualquier comprobación, para que también quede marcado un proyecto que aún no tiene volcados), sin
    depender de que alguien se acuerde. Devuelve True si cambió el manifest."""
    mpath = os.path.join(ds, "agent-manifest.json")
    manifest = read_json(mpath, None)
    if not isinstance(manifest, dict):
        return False

    def iniciado():
        if manifest.get("figmaSources"):
            return True
        for rel in ("sync/components.json", "sync/variables.json"):
            d = read_json(os.path.join(ds, rel), {}) or {}
            if any(d.get(k) for k in ("components", "collections", "variables")):
                return True
        sch_dir = os.path.join(ds, "schemas", "components")
        if os.path.isdir(sch_dir) and any(f.endswith(".schema.json") and not f.startswith("_") for f in os.listdir(sch_dir)):
            return True
        src = read_json(os.path.join(ds, "source", "tokens.json"), {}) or {}
        return any((c or {}).get("tokens") for c in src.get("collections") or [])

    sb = manifest.get("starterBase")
    if sb is None or (sb == "pending" and iniciado()):
        manifest["starterBase"] = "not-applicable"
        manifest["starterBaseNote"] = ("El proyecto ya usaba init-proyecto o ya había empezado su design system cuando se añadió la base "
                                       "inicial de componentes (12.22.0): no se le carga y la skill no debe aplicársela.")
        if not dry:
            with open(mpath, "w", encoding="utf-8") as fh:
                json.dump(manifest, fh, ensure_ascii=False, indent=2)
                fh.write("\n")
        print("[MIGRACIÓN] agent-manifest.json → starterBase: not-applicable (el proyecto ya tiene o ha empezado su design system; la base inicial no se carga)")
        return True
    return False


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=None)
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--merge", action="store_true", help="solo une los trozos de sync/parts/ y valida")
    ap.add_argument("--check-dump", dest="check_dump", action="store_true", help="solo valida los volcados")
    ap.add_argument("--variables-diff", dest="variables_diff", action="store_true",
                    help="sync incremental: compara las huellas de sync/parts/fingerprints-*.json con el volcado y dice qué refrescar")
    ap.add_argument("--library-keys", dest="library_keys", action="store_true",
                    help="imprime las keys de colecciones y estilos de Foundations para el script de auditoría de librerías ligadas")
    ap.add_argument("--allow-fewer-tokens", dest="allow_fewer", action="store_true",
                    help="permite escribir un tokens.css con más de un 10 %% menos de tokens que el actual")
    args = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(args.root or os.path.dirname(here))
    ds = os.path.join(root, "design-system")
    cfg = dict(DEFAULT_CFG)
    user_cfg = read_json(os.path.join(here, "ds-sync.config.json"), {})
    for k, v in (user_cfg or {}).items():
        cfg[k] = {**cfg[k], **v} if isinstance(v, dict) and isinstance(cfg.get(k), dict) else v
    os.chdir(root)
    marcar_base_inicial(ds, args.dry)

    if args.variables_diff:
        sys.exit(variables_diff(ds, args.dry))
    if args.library_keys:
        sys.exit(library_keys(ds))
    # Modo de fuente: «figma» (por defecto: los volcados los escribe la IA leyendo Figma) o «repo» (la fuente está en
    # design-system/source/ y se compila al mismo volcado, sin Figma). Todo lo demás del sync es igual.
    modo_fuente = (read_json(os.path.join(ds, "agent-manifest.json"), {}) or {}).get("sourceMode") or "figma"
    if not args.check_dump and os.path.isfile(os.path.join(ds, "design.md")):
        # 12.20.0: design.md deja de traer dentro las guías (sync, auditoría, verificación…): se reparten solas, sin perder texto
        _dm = open(os.path.join(ds, "design.md"), encoding="utf-8").read()
        if "## Sync desde Figma" in _dm or os.path.isfile(os.path.join(ds, "guides", "figma-guides.md")):
            import importlib.util as _ilu
            _sp = _ilu.spec_from_file_location("ds_guides", os.path.join(here, "ds-guides.py"))
            if os.path.isfile(os.path.join(here, "ds-guides.py")):
                _g = _ilu.module_from_spec(_sp)
                _sp.loader.exec_module(_g)
                _r = _g.split(root)
                if _r["movidas"]:
                    print("[MIGRACIÓN] design.md pasa a ser un router: %d secciones movidas tal cual a design-system/guides/ (%s)" % (len(_r["movidas"]), ", ".join(_r["movidas"])))
                    for _w in _r["avisos"]:
                        print("  [AVISO] " + _w)
    if modo_fuente == "repo" and not args.check_dump:
        import importlib.util
        spec = importlib.util.spec_from_file_location("ds_source", os.path.join(here, "ds-source.py"))
        ds_source = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ds_source)
        res_src = ds_source.compile_source(ds, write=True)
        for w in res_src["warnings"]:
            print(f"[AVISO] fuente: {w}")
        for e in res_src["errors"]:
            print(f"[ERROR] fuente: {e}")
        if res_src["errors"]:
            sys.exit("[ERROR] la fuente de design-system/source/ no es válida: no se genera nada. Corrígela (ds-source.py --check).")
        print(f"ds-sync · fuente en el repo: {res_src['tokens']} tokens y {res_src['components']} componentes compilados"
              + (f" → sync/{', sync/'.join(res_src['written'])}" if res_src["written"] else " (sin cambios)"))
    if not args.check_dump and modo_fuente != "repo":
        unidos, errs, avisos_merge = fold_parts(ds, args.dry, strict=args.merge)
        for a_ in avisos_merge:
            print(f"[AVISO] {a_}")
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
        css_generado = tokens.tokens_css(meta)
        problemas_css = check_css(css_generado)
        if problemas_css:
            for pr in problemas_css[:10]:
                print(f"[ERROR] tokens.css no es ejecutable: {pr}")
            sys.exit("[ERROR] el CSS generado no pasa la comprobación de ejecutabilidad; "
                     "no se escribe. Revisa los valores en Figma y vuelve a sincronizar.")
        orden = check_media_order(css_generado)
        if orden:
            findings.append(("critical", "tokens-media-order", orden))
        # Freno: un tokens.css con bastantes menos tokens que el actual casi siempre viene de un volcado a medias.
        # Antes de sobrescribir (y con él tokens.json, tokens.md, showcase y library) se para y se dice.
        cuenta = lambda css: len(re.findall(r"^\s*--[\w-]+\s*:", css or "", re.M))
        n_antes, n_ahora = cuenta(read(os.path.join(ds, "tokens", "tokens.css"), "")), cuenta(css_generado)
        if n_antes and n_ahora < 0.9 * n_antes and not args.allow_fewer:
            sys.exit(f"[ERROR] tokens.css pasaría de {n_antes} a {n_ahora} tokens (menos del 90 %): no se escribe nada. "
                     f"Suele ser un volcado de variables a medias (sync/variables.json: revisa readProgress y sync/parts/). "
                     f"Si la bajada es intencionada, repite con --allow-fewer-tokens.")
        write_json(os.path.join(ds, "tokens", "tokens.json"), tokens.tokens_json(meta), args.dry, written)
        write(os.path.join(ds, "tokens", "tokens.css"), css_generado, args.dry, written)
        write(os.path.join(ds, "docs", "tokens.md"), tokens.tokens_md(meta), args.dry, written)
        for fam, ok in tokens.foundations_status().items():
            if not ok:
                findings.append(("warning", "foundation-missing", f"{'La fuente' if modo_fuente == 'repo' else 'Figma'} no define la familia {fam}"))

    # ── componentes ──
    schemas = []
    comps = Components(raw_comps, cfg, synced_at, ds, raw_icons, dcom.load_config(here))
    if raw_comps is not None:
        comp_dir = os.path.join(ds, "schemas", "components")
        existing_files = {os.path.basename(p): p for p in glob.glob(os.path.join(comp_dir, "*.schema.json"))}
        # Con un slug compartido (slug-collision) hay un solo archivo y gana el último maestro del volcado:
        # se escribe una sola vez (antes cada maestro lo reescribía por turnos y el archivo cambiaba en
        # cada sync sin que nada hubiera cambiado en Figma).
        ultimo = {}
        for i, c in enumerate(comps.items):
            sl_ = slug(c["name"])
            # Con un slug compartido, el contrato es del último maestro, pero nunca el de una pieza interna si hay
            # un componente compartido con ese slug: lo interno no puede quedarse con el contrato de lo compartido.
            previo = ultimo.get(sl_)
            if previo is not None and comps.interno(c) and not comps.interno(comps.items[previo]):
                continue  # un interno no desplaza a un componente compartido que ya tiene ese slug
            ultimo[sl_] = i
        por_slug = {}
        for i, c in enumerate(comps.items):
            s = slug(c["name"])
            path = os.path.join(comp_dir, f"{s}.schema.json")
            sch = comps.schema(c, read_json(path, {}))
            if i != ultimo[s]:
                continue
            por_slug[s] = sch
            if s not in comps.keep_existing:
                write_json(path, sch, args.dry, written)
            existing_files.pop(f"{s}.schema.json", None)
        schemas.extend(por_slug.values())
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
        if comps.migrados:
            print(f"  [MIGRACIÓN] schemas: {len(set(comps.migrados))} contratos pasados a la forma 12.0.0 (API neutra: api · code · figma · docs); lo manual se conserva")
        # index + relationships
        index = read_json(os.path.join(ds, "schemas", "index.json"), {})
        index.update({"lastSync": synced_at, "components": [{
            "id": s["id"], "name": s["meta"]["name"], "slug": s["meta"]["slug"], "kind": s["meta"]["kind"],
            "contractPath": f"./components/{s['meta']['slug']}.schema.json",
            "keywords": sorted({w for w in re.split(r"[\s/_-]+", s["meta"]["name"].lower()) if w} | ({"icon"} if s["api"]["icons"]["hasIcon"] else set())),
            "dependencies": s["relations"]["uses"], "hasIcon": s["api"]["icons"]["hasIcon"],
            "figmaSource": {k: s["figma"].get(k) for k in ("fileKey", "nodeId", "componentKey")}, "codeSource": {"path": s["code"]["path"], "classes": s["code"]["classes"]}}
            for s in schemas],
            "counts": {"atoms": sum(1 for s in schemas if s["meta"]["kind"] == "component"), "patterns": sum(1 for s in schemas if s["meta"]["kind"] == "pattern")}})
        write_json(os.path.join(ds, "schemas", "index.json"), index, args.dry, written)
        rel = read_json(os.path.join(ds, "schemas", "relationships.json"), {})
        rel["relationships"] = [{"from": s["meta"]["slug"], "to": u, "type": "uses"} for s in schemas for u in s["relations"]["uses"]]
        rel["usedBy"] = {}
        for s_ in schemas:
            for u in s_["relations"]["uses"]:
                rel["usedBy"].setdefault(u, [])
                if s_["meta"]["slug"] not in rel["usedBy"][u]:
                    rel["usedBy"][u].append(s_["meta"]["slug"])
        rel["lastSync"] = synced_at
        write_json(os.path.join(ds, "schemas", "relationships.json"), rel, args.dry, written)
        # propuestas de textos pendientes (las crea la library) con el nombre viejo del campo de accesibilidad
        for pp in sorted(glob.glob(os.path.join(ds, "proposals", "*.proposal.json"))):
            prop = read_json(pp, None)
            cambios_p = ((prop or {}).get("proposedChange") or {}).get("changes") or []
            if any(c.get("field") == A11Y_OLD for c in cambios_p):
                for c in cambios_p:
                    if c.get("field") == A11Y_OLD:
                        c["field"] = A11Y_NEW
                write_json(pp, prop, args.dry, written)
                print(f"  [MIGRACIÓN] proposals/{os.path.basename(pp)}: campo «{A11Y_OLD}» → «{A11Y_NEW}»")
        # fichas (docs/<carpeta>/<slug>.md) e índices (components.md / patterns.md)
        for kind, fname in (("component", "components.md"), ("pattern", "patterns.md")):
            path, ddir = os.path.join(ds, "docs", fname), os.path.join(ds, "docs", DOCS_DIR[kind])
            md, files = read(path, ""), {}
            md, notas = migrate_fichas(md, files)
            md, cambio_idx = migrar_a11y(md)
            if cambio_idx:
                notas.append(f"campo «{A11Y_OLD}» → «{A11Y_NEW}» en la explicación del índice")
            for n in notas:
                print(f"  [MIGRACIÓN] {fname}: {n}")
            mine = [s for s in schemas if s["meta"]["kind"] == kind]
            for s in mine:
                sl = s["meta"]["slug"]
                if sl not in files:
                    files[sl] = read(os.path.join(ddir, f"{sl}.md"), "")
                files[sl] = upsert_ficha_file(files[sl], s, comps.live_block(s))
            n_a11y = 0
            for sl_ in list(files):
                files[sl_], cambio = migrar_a11y(files[sl_])
                n_a11y += cambio
            # fichas sin componente vivo y la plantilla del proyecto: también, aunque el sync no las reescriba
            for extra in sorted(glob.glob(os.path.join(ddir, "*.md"))):
                stem = os.path.splitext(os.path.basename(extra))[0]
                if stem in files or os.path.basename(extra) == PLANTILLA:
                    continue
                txt, cambio = migrar_a11y(read(extra, "") or "")
                if cambio:
                    write(extra, txt, args.dry, written)
                    n_a11y += 1
            if n_a11y:
                print(f"  [MIGRACIÓN] {fname}: {n_a11y} fichas: campo «{A11Y_OLD}» → «{A11Y_NEW}» (lo escrito se conserva)")
            notas_r, huerfanas = reasignar_secciones(files, {c.get("id"): slug(c["name"]) for c in comps.items if c.get("id")})
            for n in notas_r:
                print(f"  [MIGRACIÓN] {fname}: {n}")
            for sl, nombre, nodo in huerfanas:
                findings.append(("warning", "ficha-section-orphan", f"docs/{DOCS_DIR[kind]}/{sl}.md guarda la sección de «{nombre}» ({nodo}), que no corresponde a ningún componente del volcado: retírala o restaura el componente en Figma"))
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
            if comps.interno(c):  # un interno que comparte slug con otro no es una colisión del sistema compartido
                continue
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
        assets_md = ["<!-- ⚙️ ARCHIVO GENERADO por scripts/ds-sync.py — NO EDITAR A MANO. -->", "",
                     f"# {meta['designSystem']} · Assets  ·  _(iconos y fuentes exportados de Figma)_", "",
                     f"> Última sync: {synced_at}. Los archivos viven en `../assets/icons/` y `../assets/fonts/`; las pantallas los referencian desde ahí. No existe ningún otro `img/` ni `fonts/` en el proyecto.", "",
                     "## Iconos (`../assets/icons/`)",
                     md_table(["Archivo", "Componente Figma", "Node ID", "Tamaños (tokens `--icon-size-*`)", "Uso"],
                              [[f"`{r['file']}`", r["name"], f"`{r['nodeId']}`", ", ".join(f"`{v}`" for v in icon_sizes) or "⬜ sin tokens icon/size", r["usage"] or "—"] for r in assets_rows]) if assets_rows else "_(sin iconos exportados)_",
                     "", "## Fuentes (`../assets/fonts/`)",
                     md_table(["Archivo", "Familia · peso", "Origen (Figma / Google Fonts / licencia)", "Token `--family-*`", "Notas"],
                              [[f"`{os.path.basename(p)}`", "unknown", "unknown", "unknown", ""] for p in sorted(glob.glob(os.path.join(ds, "assets", "fonts", "*")) ) if not p.endswith(".gitkeep")]) ]
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

    # ── librerías ligadas: auditoría (script aparte) y keys de los propios volcados de componentes ──
    audit_findings, audit_resumen = library_audit_findings(ds, raw_vars, {c.get("name") for c in comps.items if comps.interno(c)})
    findings += audit_findings
    # Por la key de la variable (la de su colección puede ser la antigua en un archivo reenlazado).
    keys_foundations = {v.get("key") for c in (raw_vars or {}).get("collections") or [] for v in c.get("variables") or [] if v.get("key")}
    if keys_foundations and raw_comps:
        for page in raw_comps.get("pages") or []:
            for c in page.get("components") or []:
                vk = (c.get("bindings") or {}).get("variableKeys") or {}
                ajenas = sorted(n for n, k in vk.items() if isinstance(k, dict) and k.get("remote") and k.get("key") and k["key"] not in keys_foundations)
                if ajenas:
                    findings.append(("warning" if comps.interno(c) else "critical", "variable-from-foreign-library",
                                     f"{c.get('name')} (página «{(c.get('page') or page.get('name') or '').strip()}»): liga {len(ajenas)} variable(s) de una librería que no es la "
                                     f"Foundations declarada: {', '.join(ajenas[:12])}{' …' if len(ajenas) > 12 else ''}. Arreglo en design.md § Sync (Swap library)"))

    # ── gravedad por proyecto (ds-sync.config.json → findingSeverity) ──
    ajuste = {k: v for k, v in (cfg.get("findingSeverity") or {}).items() if v in ("critical", "warning", "info", "off")}
    if ajuste:
        findings = [(ajuste.get(c, s_), c, d) for s_, c, d in findings if ajuste.get(c, s_) != "off"]

    # ── drift + manifest ──
    drift = read_json(os.path.join(ds, "reports", "drift-report.json"), {})
    sev = {"critical": 0, "warning": 0, "info": 0}
    for s, _, _ in findings:
        sev[s] = sev.get(s, 0) + 1
    drift.update({"generatedAt": synced_at, "summary": sev,
                  "findings": [{"severity": s, "check": c, "detail": d} for s, c, d in findings],
                  "internals": [{"name": c["name"], "slug": slug(c["name"]), "page": c.get("page"), "reason": comps.interno(c)}
                                for c in comps.items if comps.interno(c)],
                  "inputs": {"variables": raw_vars is not None, "components": raw_comps is not None, "icons": bool(raw_icons),
                             "libraryAudit": audit_resumen},
                  "generatedBy": "scripts/ds-sync.py"})
    write_json(os.path.join(ds, "reports", "drift-report.json"), drift, args.dry, written)
    manifest["lastSync"] = synced_at
    write_json(os.path.join(ds, "agent-manifest.json"), manifest, args.dry, written)

    # ── resumen ──
    print(("[DRY] " if args.dry else "") + f"ds-sync · {len(tokens.tokens)} tokens en {len(tokens.collections)} colecciones · {len(schemas)} componentes/patrones · {len(assets_rows)} iconos")
    for s, c, d in findings:
        print(f"  [{s.upper()}] {c}: {d}")
    print(f"  {sev['critical']} críticos · {sev['warning']} avisos · {sev['info']} info → design-system/reports/drift-report.json")
    n_int = sum(1 for c in comps.items if comps.interno(c))
    if n_int:
        print(f"  {n_int} piezas internas de Figma (no se verifican ni se construyen): lista y motivo en drift-report.json → internals")
    print("  archivos " + ("que se escribirían" if args.dry else "escritos") + f": {len(written)}")
    if not args.dry and written:
        _rastro(root, "ds-sync", "regenerados los artefactos del DS desde los volcados de Figma", written)
    for w in written:
        print(f"    {w}")
    # ── catálogo navegable (library/) ──
    # Se regenera desde los mismos archivos que este sync acaba de escribir; si el proyecto no tiene
    # library/ (módulo sin visor) el generador no hace nada. En --dry no se toca.
    if not args.dry and os.path.isdir(os.path.join(root, "library")):
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("ds_library", os.path.join(os.path.dirname(os.path.abspath(__file__)), "ds-library.py"))
            mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
            print("  catálogo navegable (library/): ", end="")
            mod.generate(root)
        except Exception as e:
            print(f"  [WARNING] no se pudo regenerar library/: {e}; ejecuta python3 scripts/ds-library.py")
    print("Siguiente: revisa la parte de criterio (⬜ TODO) de los contratos nuevos, ejecuta python3 scripts/token-audit.py y revisa git diff.")
    sys.exit(1 if sev["critical"] else 0)


if __name__ == "__main__":
    main()
