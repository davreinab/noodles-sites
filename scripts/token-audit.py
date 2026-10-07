#!/usr/bin/env python3
"""token-audit — hace cumplir las reglas del DS que se pueden comprobar sin abrir Figma.

Sin dependencias (solo stdlib, Python 3.8+). Uso:
    python3 scripts/token-audit.py                 # audita según scripts/token-audit.config.json
    python3 scripts/token-audit.py --json          # salida JSON por stdout
    python3 scripts/token-audit.py --out design-system/reports/token-audit.json   # guarda el JSON
    python3 scripts/token-audit.py --root .        # raíz del proyecto (por defecto: carpeta padre de scripts/)

Código de salida: 1 si hay algún ERROR; 0 si solo hay avisos o nada. Se ejecuta antes de cada
commit (ver AGENTS.md), al cierre de cada sync y en CI. Si falla, se arregla el valor crudo
(en Figma → sync, o en la clase de components.css) o el archivo mal colocado; nunca el
script ni su config.

Qué comprueba:
  1. Valores crudos fuera de los bloques :root de tokens (css/components.css, UI/*.html, showcase):
     ERROR  color crudo (#hex, rgb(), hsl()…) · longitud cruda (px/rem/em) · tamaño de icono crudo ·
            font-weight numérico · box-shadow crudo si existen tokens de elevación · z-index /
            duración crudos si existen tokens de capa / motion · <style> o style="" en páginas
     WARN   duración / z-index / sombra crudos cuando el DS aún no define esos tokens ·
            breakpoint fuera de los documentados · filtros con valores crudos
  2. Estructura cerrada de design-system/: cualquier archivo o carpeta fuera de la lista
     permitida (config → structure) es ERROR. Evita `img/`, `fonts/`, `patterns.css` o docs
     sueltos en la raíz.
  3. Showcase (design-system/showcase/index.html): su chrome solo puede vivir en un bloque
     <style data-showcase-chrome> con selectores `.sc-*` y custom properties `--sc-*`; nunca
     estiliza clases del DS ni redefine tokens. El markup de demo se audita como una pantalla.
  4. Secciones obligatorias (config → docs): archivos del DS que deben existir y contener ciertos
     encabezados o referencias (Composición de pantalla, Decisiones recurrentes, Ejemplo de código,
     enlaces del showcase). Si faltan, ERROR. Un encabezado se comprueba como línea completa
     (renombrarlo es quitarlo); una referencia que no es encabezado, como subcadena. Los
     documentos funcionales de context/ los audita su propio script hermano,
     scripts/context-audit.py: cada uno falla por lo suyo.
  5. Transparencias (regla 7 de design.md): en tokens.css, un token de color con alfa < 1
     (rgba/hsla con alfa, `rgb(... / a)`, hex de 4 u 8 dígitos) es ERROR salvo que pertenezca a
     una familia translúcida por naturaleza (config → translucent.allowPrefixes: elevación,
     overlay, scrim, backdrop). El color resultante dependería del fondo y su contraste AA no
     se puede verificar: el tono se define opaco en Figma. En CSS y pantallas, `opacity` entre
     0 y 1 es WARN (solo para transiciones de aparición, nunca para atenuar texto o iconos).
Excepciones (config → allow): hairlines ≤ 2px en bordes/offsets, selectores utilitarios
(.visually-hidden), valores neutros (0, auto, 100%…) y líneas concretas justificadas.
"""
import argparse
import fnmatch
import glob
import json
import os
import re
import sys

HEX_RE = re.compile(r"#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b")
FUNC_COLOR_RE = re.compile(r"\b(?:rgba?|hsla?|oklch|oklab|color)\(")
LENGTH_RE = re.compile(r"(?<![\w.-])(-?\d*\.?\d+)(px|rem|em)\b")
DURATION_RE = re.compile(r"(?<![\w.-])(-?\d*\.?\d+)(ms|s)\b")
NUMBER_RE = re.compile(r"-?\d*\.?\d+")
VAR_RE = re.compile(r"var\(\s*(--[\w-]+)")
DECL_RE = re.compile(r"([a-zA-Z-]+)\s*:\s*([^;{}]+)")
TOKEN_DEF_RE = re.compile(r"(--[\w-]+)\s*:\s*([^;]+);")
STYLE_ATTR_RE = re.compile(r'style\s*=\s*"([^"]*)"', re.I)
STYLE_BLOCK_RE = re.compile(r"<style([^>]*)>(.*?)</style>", re.I | re.S)
SCRIPT_BLOCK_RE = re.compile(r"<script[^>]*>.*?</script>", re.I | re.S)

DEFAULT_FAMILIES = {
    "icon": ["--icon-size-", "--icon-"],
    "spacing": ["--spacing-", "--space-"],
    "radius": ["--radius-"],
    "layout": ["--layout-", "--container-"],
    "font-size": ["--size-", "--font-size-", "--text-", "--font-*-size"],
    "line-height": ["--lh-", "--line-height-", "--font-*-line-height"],
    "letter-spacing": ["--tracking-", "--letter-spacing-", "--font-*-letter-spacing"],
    "border-width": ["--ds-hairline", "--border-width-", "--stroke-"],
    "control": ["--ds-control-", "--control-"],
    "z-index": ["--z-", "--layer-"],
    "duration": ["--motion-", "--duration-"],
    "elevation": ["--elevation-", "--shadow-"],
    "weight": ["--weight-", "--font-weight-", "--font-*-weight"],
}
# Un patrón con * es un comodín (las variables de los estilos de texto: --font-<estilo>-size);
# sin *, es un prefijo.


def de_familia(name, p):
    return fnmatch.fnmatchcase(name, p) if "*" in p else name.startswith(p)
PROP_FAMILY = [
    (("border-radius", "border-top-left-radius", "border-top-right-radius", "border-bottom-left-radius",
      "border-bottom-right-radius"), "radius"),
    (("font-size",), "font-size"),
    (("line-height",), "line-height"),
    (("letter-spacing",), "letter-spacing"),
    (("border", "border-top", "border-right", "border-bottom", "border-left", "border-width", "outline",
      "outline-width", "outline-offset", "text-underline-offset", "stroke-width"), "border-width"),
    (("max-width", "min-width", "width", "grid-template-columns", "grid-template-rows", "flex-basis"), "layout"),
    (("padding", "margin", "gap", "row-gap", "column-gap", "inset", "top", "right", "bottom", "left",
      "height", "min-height", "max-height", "transform", "translate", "grid-auto-rows"), "spacing"),
]
IGNORED_ENTRIES = {".DS_Store", ".gitkeep", ".keep", "Thumbs.db"}



def modulo_activo(root, mid):
    """¿Está activo este módulo? Lo que no está activo no se exige.
    Sin declaración de módulos (proyectos anteriores a la 10.0.0) se asume que sí,
    para no romper nada ya creado."""
    try:
        with open(os.path.join(root, "governance", "modules.json"), encoding="utf-8") as fh:
            m = (json.load(fh).get("modules") or {}).get(mid) or {}
        return m.get("active") is not False
    except Exception:
        return True


def load_config(cfg_path):
    default = {
        "tokensFile": "design-system/tokens/tokens.css",
        "cssFiles": ["design-system/css/components.css"],
        "htmlFiles": ["UI/**/*.html", "design-system/showcase/index.html"],
        "showcase": {"file": "design-system/showcase/index.html", "prefix": "sc-"},
        "breakpoints": [],
        "families": DEFAULT_FAMILIES,
        "structure": {
            "design-system": ["design.md", "figma.md", "agent-manifest.json", "CHANGELOG.md", "docs", "tokens", "css",
                              "assets", "schemas", "reports", "proposals", "showcase", "sync"],
            "design-system/sync": ["README.md", "variables.json", "components.json", "icons.json", "parts"],
            "design-system/sync/parts": ["*.json"],
            "design-system/docs": ["tokens.md", "components.md", "patterns.md", "assets.md", "components", "patterns"],
            "design-system/docs/components": ["*.md"],
            "design-system/docs/patterns": ["*.md"],
            "design-system/tokens": ["tokens.json", "tokens.css", "w3c"],
            "design-system/tokens/w3c": ["README.md", "manifest.json", "*.tokens.json"],
            "design-system/css": ["components.css"],
            "design-system/assets": ["icons", "fonts"],
            "design-system/schemas": ["README.md", "_component.schema.json", "index.json", "relationships.json",
                                      "governance", "components"],
            "design-system/schemas/governance": ["policies.json", "constraints.json",
                                                 "maturity.json", "agent-readiness.json", "lifecycle.json"],
            "design-system/showcase": ["index.html"],
            "design-system/proposals": ["README.md", "_proposal.schema.json", "*.proposal.json"],
            "design-system/schemas/components": ["*.schema.json"],
            "design-system/reports": ["*.json", "*.md"]
        },
        "docs": {
            "design-system/docs/patterns.md": ["## Composición de pantalla", "### Ritmo vertical",
                                               "### Contenedores y anchos", "### Grid y breakpoints",
                                               "### Paneles, overlays y capas", "### Flujo de contenido",
                                               "## Decisiones recurrentes"],
            "design-system/docs/components.md": ["## Índice"],
            "design-system/docs/patterns.md": ["## Índice"],
            "design-system/docs/components/_plantilla.md": ["Ejemplo de código"],
            "design-system/showcase/index.html": ["../tokens/tokens.css", "../css/components.css",
                                                  "data-showcase-chrome"]
        },
        "allow": {
            "values": ["0", "0px", "1", "100%", "50%", "auto", "none", "inherit", "currentColor", "transparent"],
            "hairline": {"maxPx": 2, "properties": ["border", "border-top", "border-right", "border-bottom",
                                                    "border-left", "border-width", "outline", "outline-width",
                                                    "outline-offset", "text-underline-offset", "stroke-width",
                                                    "left", "top", "margin-top", "margin-bottom"]},
            "selectors": [".visually-hidden", ".sr-only"],
            "properties": ["clip", "clip-path", "aspect-ratio", "flex", "flex-grow", "flex-shrink", "order",
                           "opacity", "line-height", "grid-column", "grid-row", "scale", "font-weight-unitless"],
            "lines": []
        },
        "warnOnly": {"properties": ["transition", "animation", "transition-duration", "animation-duration",
                                    "backdrop-filter", "filter"]},
        "translucent": {"allowPrefixes": ["--elevation-", "--shadow-", "--overlay-", "--scrim-", "--backdrop-"]},
    }
    if cfg_path and os.path.exists(cfg_path):
        with open(cfg_path, encoding="utf-8") as fh:
            user = json.load(fh)
        for k, v in user.items():
            if isinstance(v, dict) and isinstance(default.get(k), dict):
                default[k].update(v)
            else:
                default[k] = v
    return default


def strip_comments(css):
    return re.sub(r"/\*.*?\*/", lambda m: " " * len(m.group(0)), css, flags=re.S)


def norm_hex(h):
    h = h.lower()
    if len(h) in (4, 5):
        h = "#" + "".join(c * 2 for c in h[1:])
    return h[:7]


class Tokens:
    def __init__(self, root, tokens_file):
        self.names, self.by_hex, self.by_len, self.by_dur = set(), {}, {}, {}
        path = os.path.join(root, tokens_file)
        if not os.path.exists(path):
            return
        css = strip_comments(open(path, encoding="utf-8").read())
        for name, value in TOKEN_DEF_RE.findall(css):
            value = value.strip()
            self.names.add(name)
            if VAR_RE.search(value):
                continue
            if HEX_RE.fullmatch(value):
                self.by_hex.setdefault(norm_hex(value), []).append(name)
                continue
            m = re.fullmatch(r"(-?\d*\.?\d+)(px|rem|em)", value)
            if m:
                self.by_len.setdefault((float(m.group(1)), m.group(2)), []).append(name)
                continue
            m = re.fullmatch(r"(-?\d*\.?\d+)(ms|s)", value)
            if m:
                self.by_dur.setdefault((float(m.group(1)), m.group(2)), []).append(name)

    def has_family(self, prefixes):
        return any(de_familia(n, p) for n in self.names for p in prefixes)

    def suggest_len(self, num, unit, prefixes, near_px=4):
        val = float(num)
        exact = self.by_len.get((val, unit), [])
        fam = [t for t in exact if any(de_familia(t, p) for p in prefixes)]
        if fam:
            return f"var({fam[0]})"
        if exact:
            return f"var({exact[0]}) (otra familia: revisa si es el token correcto)"
        if unit == "px" and prefixes:
            cands = [(abs(v - val), v, t) for (v, u), toks in self.by_len.items() if u == "px"
                     for t in toks if any(de_familia(t, p) for p in prefixes)]
            cands.sort()
            if cands and cands[0][0] <= near_px:
                return f"var({cands[0][2]}) ({cands[0][1]:g}px, el más cercano de la familia)"
        return None


ALPHA_FUNC_RE = re.compile(r"\b(?:rgba?|hsla?)\(\s*([^)]*)\)")


def alpha_below_one(value):
    """True si el valor contiene un color con canal alfa < 1 (rgba/hsla, `rgb(r g b / a)`, hex #rgba/#rrggbbaa)."""
    for m in HEX_RE.finditer(value):
        h = m.group(0)[1:]
        if len(h) == 4 and h[3].lower() != "f":
            return True
        if len(h) == 8 and h[6:8].lower() != "ff":
            return True
    for m in ALPHA_FUNC_RE.finditer(value):
        inner = m.group(1)
        a = None
        if "/" in inner:
            a = inner.split("/", 1)[1].strip()
        else:
            parts = [p.strip() for p in inner.split(",")]
            if len(parts) == 4:
                a = parts[3]
        if a is None:
            continue
        try:
            num = float(a[:-1]) / 100 if a.endswith("%") else float(a)
        except ValueError:
            continue
        if num < 1:
            return True
    return False


def family_for(prop, selector, families):
    if prop in ("width", "height") and selector and (".icon" in selector or selector.split()[-1].endswith("icon")):
        return "icon", families["icon"]
    for props, fam in PROP_FAMILY:
        if prop in props:
            return fam, families[fam]
    return None, []


def iter_rules(css_text, base_line=1):
    """Genera (line, selector, [(prop, value), ...]) por regla, marcando si está dentro de :root."""
    css = strip_comments(css_text)
    depth, root_depth, buf, sel_stack, line = 0, None, "", [], base_line
    rule_line, decls = base_line, []
    for ch in css:
        if ch == "\n":
            line += 1
        if ch == "{":
            sel = buf.strip()
            sel_stack.append(sel)
            rule_line = line
            if root_depth is None and sel.startswith(":root"):
                root_depth = depth
            depth += 1
            buf, decls = "", []
        elif ch == "}":
            tail = buf.strip()
            m = DECL_RE.match(tail) if tail else None
            if m:  # última declaración sin ';'
                decls.append((line, m.group(1).strip().lower(), m.group(2).strip()))
            if decls:
                yield rule_line, (sel_stack[-1] if sel_stack else ""), root_depth is not None, decls
            depth -= 1
            if root_depth is not None and depth == root_depth:
                root_depth = None
            if sel_stack:
                sel_stack.pop()
            buf, decls = "", []
        elif ch == ";":
            decl = buf.strip()
            buf = ""
            m = DECL_RE.match(decl) if decl else None
            if m:
                decls.append((line, m.group(1).strip().lower(), m.group(2).strip()))
        else:
            buf += ch


class Audit:
    def __init__(self, cfg, tokens, root):
        self.cfg, self.tokens, self.root, self.findings, self._seen = cfg, tokens, root, [], set()

    def add(self, sev, file, line, prop, value, msg):
        key = (file, line, prop, value)
        if key in self._seen:
            return
        self._seen.add(key)
        self.findings.append({"severity": sev, "file": file, "line": line, "property": prop,
                              "value": value, "suggestion": msg})

    # ── 1. valores crudos ─────────────────────────────────────────────────────
    def value(self, prop, value, selector, file, line, ctx="css"):
        cfg, T, allow = self.cfg, self.tokens, self.cfg["allow"]
        if any(a in selector for a in allow["selectors"]) or any(a == f"{file}:{line}" for a in allow["lines"]):
            return
        if prop.startswith("--"):
            if ctx == "inline" and not VAR_RE.search(value):
                self.add("error", file, line, prop, value, "las custom properties inline solo pueden apuntar a var(--token)")
            return
        if value.strip() in allow["values"]:
            return
        stripped = VAR_RE.sub("", value)
        severity = "warn" if prop in cfg["warnOnly"]["properties"] else "error"
        fam_name, fam_prefixes = family_for(prop, selector, cfg["families"])

        for m in HEX_RE.finditer(stripped):
            sug = T.by_hex.get(norm_hex(m.group(0)))
            self.add("error", file, line, prop, m.group(0),
                     f"usa var({sug[0]})" if sug else "no hay token con ese color: añádelo en Figma y sincroniza")
        if FUNC_COLOR_RE.search(stripped):
            self.add("error", file, line, prop, value, "color funcional crudo: usa un token semántico")
        if prop == "opacity":
            try:
                o = float(stripped.strip().rstrip("%")) / (100 if stripped.strip().endswith("%") else 1)
                if 0 < o < 1:
                    self.add("warn", file, line, prop, value,
                             "opacidad parcial: si atenúa texto, icono o fondo, usa un token de color opaco (regla 7); "
                             "solo válida para transiciones de aparición")
            except ValueError:
                pass
        if prop == "box-shadow" and stripped.strip():
            fam = T.has_family(cfg["families"]["elevation"])
            self.add("error" if fam else "warn", file, line, prop, value,
                     "usa var(--elevation-*)" if fam else "no existen tokens de elevación: créalos en Figma (effect styles) y sincroniza")
        if prop not in allow["properties"]:
            for m in LENGTH_RE.finditer(stripped):
                num, unit = m.group(1), m.group(2)
                raw = f"{num}{unit}"
                if raw in allow["values"] or float(num) == 0:
                    continue
                hl = allow["hairline"]
                if unit == "px" and abs(float(num)) <= hl["maxPx"] and prop in hl["properties"]:
                    continue
                sug = T.suggest_len(num, unit, fam_prefixes)
                if fam_name == "icon":
                    msg = (f"tamaño de icono crudo: {sug or 'usa var(--icon-size-*)'}" if T.has_family(cfg["families"]["icon"])
                           else "tamaño de icono crudo y el DS no define icon/size/*: créalos en Figma y sincroniza")
                elif sug:
                    msg = sug
                else:
                    msg = f"sin token {fam_name or ''} equivalente: añádelo en Figma y sincroniza".replace("  ", " ")
                self.add(severity, file, line, prop, raw, msg)
        for m in DURATION_RE.finditer(stripped):
            fam = T.has_family(cfg["families"]["duration"])
            sug = T.by_dur.get((float(m.group(1)), m.group(2)))
            self.add("error" if fam else "warn", file, line, prop, m.group(0),
                     f"usa var({sug[0]})" if sug else ("usa var(--motion-*)" if fam else "no existen tokens de motion: defínelos en Figma y sincroniza"))
        if prop == "z-index" and NUMBER_RE.fullmatch(stripped.strip()) and "var(" not in value:
            fam = T.has_family(cfg["families"]["z-index"])
            self.add("error" if fam else "warn", file, line, prop, value,
                     "usa var(--z-*)" if fam else "no existen tokens de capa (z-index): defínelos en Figma y sincroniza")
        if prop == "font-weight" and NUMBER_RE.fullmatch(stripped.strip()) and "var(" not in value:
            self.add("error", file, line, prop, value, "usa var(--weight-*) o la variable --font-<estilo>-weight de su estilo de texto")

    def css(self, text, file, base_line=1):
        for _, selector, in_root, decls in iter_rules(text, base_line):
            if in_root:
                continue
            for line, prop, value in decls:
                self.value(prop, value, selector, file, line)
        for m in re.finditer(r"@media[^{]*?\(\s*(?:max|min)-width\s*:\s*(\d+)px", text):
            bp = int(m.group(1))
            line = base_line + text[:m.start()].count("\n")
            if self.cfg["breakpoints"] and bp not in self.cfg["breakpoints"]:
                self.add("warn", file, line, "@media", f"{bp}px",
                         f"breakpoint fuera de los documentados {self.cfg['breakpoints']} (docs/patterns.md § Composición)")

    # ── 3. showcase: chrome aislado ───────────────────────────────────────────
    def showcase_chrome(self, css_text, file, base_line, prefix):
        """El chrome del showcase es libre en valores, pero cerrado en alcance: solo `.sc-*`/`--sc-*`.
        Un selector es válido si su SUJETO (último compuesto) lleva `.sc-*`/`[data-sc-*]`, o si es un
        elemento/universal sin clase ni id colgado de un ancestro `.sc-*` (p. ej. `.sc-nav a`).
        Puede anteponer `html[data-theme]` para reaccionar al tema, pero nunca estilizar :root/html/body."""
        cls, var = f".{prefix}", f"--{prefix}"
        for line, selector, in_root, decls in iter_rules(css_text, base_line):
            for part in selector.split(","):
                part = part.strip()
                if not part or part.startswith("@"):
                    continue
                subject = re.split(r"\s*[>+~]\s*|\s+", part)[-1]
                subject_base = re.sub(r"::?[\w-]+(\([^)]*\))?", "", subject)  # sin pseudo-clases/elementos
                if subject_base in (":root", "html", "body") or subject.startswith(":root"):
                    self.add("error", file, line, "<style data-showcase-chrome>", part,
                             f"el chrome no puede estilizar :root/html/body: usa un contenedor `{cls}root`")
                elif cls in subject or f"[data-{prefix}" in subject:
                    pass
                elif re.search(r"[.#]", subject_base):
                    self.add("error", file, line, "<style data-showcase-chrome>", part,
                             f"selector fuera del namespace del showcase: el sujeto debe ser `{cls}*` (nunca una clase del DS)")
                elif cls not in part and f"[data-{prefix}" not in part:
                    self.add("error", file, line, "<style data-showcase-chrome>", part,
                             f"selector sin ancla en el showcase: cuélgalo de un contenedor `{cls}*`")
            for dline, prop, value in decls:
                if prop.startswith("--") and not prop.startswith(var):
                    self.add("error", file, dline, prop, value,
                             f"el chrome solo declara custom properties `{var}*`; nunca redefine tokens del DS")

    def html(self, path, rel):
        html = open(path, encoding="utf-8").read()
        sc = self.cfg.get("showcase") or {}
        is_showcase = rel == sc.get("file")
        prefix = sc.get("prefix", "sc-")
        for m in STYLE_BLOCK_RE.finditer(html):
            line = html[:m.start()].count("\n") + 1
            if is_showcase and "data-showcase-chrome" in m.group(1):
                self.showcase_chrome(m.group(2), rel, line, prefix)
                continue
            self.add("error", rel, line, "<style>", "bloque de estilos en página",
                     "regla 1b: cero estilos locales — mueve las reglas a css/components.css y documenta la clase"
                     + (" (en el showcase, el chrome va en <style data-showcase-chrome>)" if is_showcase else ""))
            self.css(m.group(2), rel, base_line=line)
        markup = SCRIPT_BLOCK_RE.sub(lambda s: "\n" * s.group(0).count("\n"), html)
        for m in STYLE_ATTR_RE.finditer(markup):
            line = markup[:m.start()].count("\n") + 1
            body = m.group(1)
            decls = [d for d in body.split(";") if d.strip()]
            if decls and all(re.match(r"\s*--[\w-]+\s*:\s*var\(--[\w-]+\)\s*$", d) for d in decls):
                continue  # custom property de dato → token (swatches, demos)
            self.add("error", rel, line, "style=", body.strip()[:80], "regla 1b: sin estilos inline — usa una clase de css/components.css"
                     + (f" o una custom property `--{prefix}*`/`--sw` que apunte a var(--token)" if is_showcase else ""))
            for d in decls:
                dm = DECL_RE.match(d.strip())
                if dm:
                    self.value(dm.group(1).lower(), dm.group(2).strip(), "", rel, line, ctx="inline")

    # ── 4. secciones obligatorias ────────────────────────────────────────────
    def docs(self):
        for rel, needles in (self.cfg.get("docs") or {}).items():
            path = os.path.join(self.root, rel)
            if not os.path.exists(path):
                self.add("error", rel, 0, "estructura", "falta", "archivo obligatorio del scaffolding: no existe")
                continue
            text = open(path, encoding="utf-8").read()
            for n in needles:
                if section_missing(text, n):
                    self.add("error", rel, 0, "secciones", n,
                             "sección o referencia obligatoria ausente: restaura la plantilla de la skill (no la borres al editar)")

    # ── 5. transparencias en tokens ──────────────────────────────────────────
    def translucent(self):
        """Regla 7: los tokens de color son opacos. Alfa < 1 solo en familias translúcidas por naturaleza."""
        rel = self.cfg["tokensFile"]
        path = os.path.join(self.root, rel)
        if not os.path.exists(path):
            return
        allow = tuple((self.cfg.get("translucent") or {}).get("allowPrefixes") or [])
        raw = open(path, encoding="utf-8").read()
        css = strip_comments(raw)
        for name, value in TOKEN_DEF_RE.findall(css):
            value = value.strip()
            if VAR_RE.search(value) or name.startswith(allow):
                continue
            if alpha_below_one(value):
                line = next((i for i, l in enumerate(raw.splitlines(), 1) if name + ":" in l), 0)
                self.add("error", rel, line, name, value,
                         "token de color translúcido: define el tono opaco en Figma (el color final no puede depender del fondo; "
                         "alfa solo en " + ", ".join(p + "*" for p in allow) + ")")

    # ── 2. estructura cerrada ────────────────────────────────────────────────
    def structure(self):
        import fnmatch
        for rel_dir, allowed in (self.cfg.get("structure") or {}).items():
            d = os.path.join(self.root, rel_dir)
            if not os.path.isdir(d):
                continue
            for entry in sorted(os.listdir(d)):
                if entry in IGNORED_ENTRIES or entry.startswith("."):
                    continue
                if not any(fnmatch.fnmatch(entry, pat) for pat in allowed):
                    self.add("error", f"{rel_dir}/{entry}", 0, "estructura", entry,
                             f"no pertenece a {rel_dir}/ — permitido: {', '.join(allowed)}. Muévelo a la carpeta de su naturaleza (docs/, tokens/, css/, assets/, schemas/…)")


def section_missing(text, needle):
    """¿Falta en `text` la sección o referencia `needle`?

    Un **encabezado** (empieza por `#`) se busca al principio de una línea y admite cola
    descriptiva, porque las plantillas la llevan a propósito: el contrato pide
    `## Enrutado` y el documento escribe `## Enrutado — qué documento abrir según la
    petición`. Lo que no vale es que la cola continúe la palabra: `## Estados` no lo
    cumple `## EstadosRenombrado` ni `## Objetivos`, que son encabezados distintos
    (regla 6 de `context/AGENTS.md`: los encabezados de plantilla no se renombran).
    Por eso tras el encabezado tiene que venir fin de línea o un carácter que no sea
    alfanumérico.

    Las **referencias que no son encabezados** (rutas del showcase, «Ejemplo de código»)
    se buscan como subcadena en todo el texto: aparecen dentro de una línea, no como línea.
    """
    if not needle.startswith("#"):
        return needle not in text
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith(needle):
            continue
        rest = line[len(needle):]
        if not rest or not rest[0].isalnum():
            return False
    return True


def expand(root, patterns):
    out = []
    for p in patterns:
        out.extend(sorted(glob.glob(os.path.join(root, p), recursive=True)))
    return [f for f in out if os.path.isfile(f)]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=None, help="raíz del proyecto")
    ap.add_argument("--config", default=None, help="ruta al config JSON")
    ap.add_argument("--json", action="store_true", help="salida JSON por stdout")
    ap.add_argument("--out", default=None, help="guardar el informe JSON en esta ruta (relativa a la raíz)")
    args = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(args.root or os.path.dirname(here))
    cfg = load_config(args.config or os.path.join(here, "token-audit.config.json"))
    tokens = Tokens(root, cfg["tokensFile"])
    if not modulo_activo(root, "design-system"):
        print("El módulo de design system no está activo en este proyecto "
              "(governance/modules.json): no hay nada que auditar aquí. "
              "Si se activa, esta auditoría vuelve a aplicar.")
        return 0

    audit = Audit(cfg, tokens, root)
    if not tokens.names:
        audit.add("warn", cfg["tokensFile"], 0, "tokens", "vacío", "tokens.css sin tokens: pendiente del primer sync desde Figma")
    audit.structure()
    audit.docs()
    audit.translucent()
    for f in expand(root, cfg["cssFiles"]):
        audit.css(open(f, encoding="utf-8").read(), os.path.relpath(f, root))
    for f in expand(root, cfg["htmlFiles"]):
        audit.html(f, os.path.relpath(f, root))

    findings = sorted(audit.findings, key=lambda x: (x["file"], x["line"]))
    errors = [x for x in findings if x["severity"] == "error"]
    warns = [x for x in findings if x["severity"] == "warn"]
    by_prop = {}
    for x in errors:
        by_prop[x["property"]] = by_prop.get(x["property"], 0) + 1
    report = {"root": root, "errors": len(errors), "warnings": len(warns), "errorsByProperty": by_prop,
              "tokensKnown": len(tokens.names), "findings": findings}
    if args.out:
        out_path = os.path.join(root, args.out)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(report, fh, ensure_ascii=False, indent=2)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for x in findings:
            print(f"{x['file']}:{x['line']}: [{x['severity'].upper()}] {x['property']}: {x['value']} → {x['suggestion']}")
        print(f"\n{len(errors)} errores · {len(warns)} avisos · tokens conocidos: {len(tokens.names)}")
        if by_prop:
            print("Errores por propiedad: " + ", ".join(f"{k} {v}" for k, v in sorted(by_prop.items(), key=lambda kv: -kv[1])))
        if errors:
            print("Corrige los valores crudos (en Figma → sync, o en la clase de css/components.css) o mueve el archivo a su carpeta; nunca el script ni su config.")
        print("Alcance: esta auditoría comprueba valores, estructura y secciones; no comprueba que el CSS o las fichas sean fieles al maestro de Figma (eso lo mide scripts/ds-fidelity.py).")
        if args.out:
            print(f"Informe guardado en {args.out}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
