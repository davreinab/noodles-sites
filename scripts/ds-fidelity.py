#!/usr/bin/env python3
"""ds-fidelity — ¿se parece lo que hay en código a lo que hay en Figma? Lo que se puede comprobar sin abrir Figma.

Sin dependencias (solo stdlib, Python 3.8+). Uso:
    python3 scripts/ds-fidelity.py                 # audita según scripts/ds-fidelity.config.json
    python3 scripts/ds-fidelity.py --json          # salida JSON por stdout
    python3 scripts/ds-fidelity.py --out design-system/reports/fidelity.json   # guarda el JSON
    python3 scripts/ds-fidelity.py --root .        # raíz del proyecto (por defecto: carpeta padre de scripts/)

Código de salida: 1 si hay algún ERROR; 0 si solo hay avisos o nada. Mismo formato y mismos códigos
que token-audit.py. Por defecto TODO es aviso: un proyecto que ya existe no se rompe al recibir este
script. Cada comprobación se puede subir a error en la config (severity).

Por qué existe: token-audit comprueba que el código use variables y que la estructura sea la
prevista; context-audit, que los documentos tengan sus secciones. Un design system puede pasar las dos
con cero errores y aun así describir en el CSS y en las fichas un componente distinto del maestro de
Figma (otro token, una variante que no existe en código, un ejemplo de una maqueta antigua). Este
script cruza lo que el sync trajo de Figma (el contrato) con lo que las personas escribieron a mano
(CSS, ejemplo) y con el estado de verificación que cada contrato declara.

Qué comprueba (solo sobre contratos que ya tienen realización en CSS, es decir, `source.code.classes`
no vacío; los que no la tienen ya los señala agent-readiness con `runnable-patterns`):
  1. token-not-used · Cada token de `api.tokensUsed` (lo que el maestro tiene ligado en Figma) debe
     aparecer como `var(--…)` en alguna regla CSS de las clases del componente. La variable CSS de cada
     token sale de tokens/tokens.json (`cssVar`), la misma que generó ds-sync. Un token que el maestro
     consume y el CSS no es la señal más directa de «CSS escrito sin abrir el maestro».
     Excepciones por componente en config → ignoreTokens (p. ej. tokens que llegan por un hijo).
  2. variant-without-css · Cada valor de cada eje de `api.variants`, salvo el valor por defecto, debe
     tener un modificador reconocible en el CSS: `.<clase-base>--<valor>` (patrón configurable) o un
     mapa explícito por componente (config → modifiers). El eje de estado (`state`) se excluye por
     defecto: hover y press son pseudoclases, no modificadores. Un eje booleano (`no`/`yes`) acepta
     `.<clase-base>--<eje>`. Lo declarado con su motivo en `coverageIgnore.components.<slug>` («eje=valor»:
     un placeholder de slot, una barra nativa, una cantidad) no se pide: la misma justificación cierra este
     aviso y variant-not-in-example.
  3. example-class-missing · Cada clase del «Ejemplo de código» (`source.code.example`) existe como
     selector en el CSS. example-external-image · El ejemplo no carga imágenes de fuera (http/https):
     lo que no sale de Figma no es del DS. example-placeholder-ellipsis · El ejemplo no usa «…» o «...»
     como contenido de un elemento (es un marcador y la vista previa queda vacía), salvo en un elemento
     marcado como elipsis real: clase que contenga «ellipsis», «dots» o «more», o una de las que el
     proyecto declare en `ellipsisClasses` de la config.
  3b. variant-not-in-example · Cada valor de cada eje de variante y cada propiedad booleana del contrato
     sale en el «Ejemplo de código» (resumen «N de M»). La clase de cada valor sale de code.classByProp,
     de `modifiers` o de la convención `.<base>--<valor>`; si ninguna existe, variant-coverage-unchecked
     (info). No cuentan los estados de pseudoclase (`coverageIgnore.values`), los ejes de `excludeAxes`
     ni lo declarado en `coverageIgnore.components.<slug>` con su justificación.
  4. screen-uses-unverified · Una pantalla de UI/ que usa un contrato `unverified` o `stale` recibe un
     aviso con la lista «pantalla → componentes». Usa = lleva data-ds="<slug>" o alguna clase propia del
     contrato (su slug como bloque BEM); no cuentan las clases de los componentes que su ejemplo compone. El estado vive en `meta.verification` de
     cada schema (lo escribe quien verifica, siguiendo el protocolo de design.md; lo caduca ds-sync
     cuando cambia el maestro). Sin bloque, el contrato cuenta como `unverified`.
  6. example-without-data-ds (nota, no aviso) · El elemento raíz del «Ejemplo de código» lleva
     data-ds="<slug>": es la marca que permite seguir el hilo pantalla → contrato → maestro de Figma, y la
     que un futuro validador de desarrollo necesitará. Severidad `info` por defecto.
  6b. screen-without-data-ds · Cuenta por ELEMENTO (12.26.0): cada elemento cuya clase es la de un contrato y que no
     lleva data-ds. Con diez botones y uno marcado, avisa de nueve. Lee también el HTML que escribe un script
     (una cadena con `<span class="icon …">` es parte de la pantalla). Una línea por pantalla con la lista; aviso por
     defecto. screen-data-ds-mismatch · un data-ds de un contrato conocido en un elemento que no lleva ninguna clase
     de ese contrato (`<section class="faq" data-ds="faq-list">`). Informe por pantalla: scripts/screen-report.py.
  7. contrast-below-aa · El texto de cada componente cumple WCAG 2.1 AA (4,5:1; 3:1 si es grande) en
     cada estado que su CSS escribe, en claro y, si existe, en oscuro. Se calcula desde el CSS y tokens.css
     (scripts/ds_contrast.py: cascada de modificadores y pseudoclases, variables locales incluidas). Exentos:
     estados deshabilitados. No comprobables (se cuentan, no se inventan): fondo propio ausente,
     transparente o semitransparente. AVISO por defecto (12.8.1): mide y avisa en cada commit sin parar a
     nadie, porque el arreglo suele ser un color de marca que se decide en Figma. Un proyecto que quiera
     bloquear lo sube a error en la config (severity). Entonces, mientras se arregla un color, una pareja
     puede declararse en contrastExceptions [{component, state, proposal}] atada a una propuesta: con la
     propuesta pendiente baja a aviso; aplicada, rechazada o inexistente, vuelve a error.
  5. screen-state-anatomy · Un componente puede tener clases válidas en una pantalla y aun así estar
     incompleto para su estado: un campo de búsqueda «relleno» que debe llevar un badge con el código
     además del nombre, montado copiando otro campo del mismo buscador que es solo texto, pasa todas
     las demás comprobaciones.
     Quien verifica un contrato declara en `behavior.stateAnatomy` del schema (bloque manual que ds-sync
     conserva) los casos en que un estado cambia la ESTRUCTURA y no solo el estilo:
         { "id": "location-filled-with-code",
           "when": ".search-form__field--location .search-field .search-field__value",
           "require": [".code-badge.code-badge--large .code-badge__code"],
           "why": "El campo de ubicación relleno muestra el código como badge además del nombre (Figma show-code)." }
     `when` localiza el caso en la pantalla; cada `require` debe existir DENTRO del elemento que casa;
     `why` es la frase del aviso. Selectores mínimos: clases compuestas (`.a.b`), etiqueta opcional
     (`span.a`) y descendiente con espacio; nada más, y sin dependencias (html.parser). Cada fallo da
     pantalla, línea aproximada, componente, id de la regla y su `why`. Sin contratos con
     `stateAnatomy` no hay nada que comprobar y no falla.

Al final resume cuántos contratos están verified / unverified / stale. Esta auditoría no abre Figma: la
verificación contra el maestro, variante a variante, la hace una persona o un agente por MCP y queda
registrada en el contrato; aquí solo se comprueba lo que de esa verificación se puede contrastar en
los artefactos.
"""
import argparse
import glob
import hashlib
import json
import os
import re
import sys

import ds_common as dcom  # una sola definición de «interno» para toda la skill

try:  # cobertura de variantes (módulo compartido con ds-library)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import ds_variants as dv
except ImportError:
    dv = None

DEFAULT_CONFIG = {
    "cssFile": "design-system/css/components.css",
    "tokensJson": "design-system/tokens/tokens.json",
    "schemasDir": "design-system/schemas/components",
    "screens": ["UI/**/*.html"],
    "severity": {
        "token-not-used": "warn",
        "variant-without-css": "warn",
        "example-class-missing": "warn",
        "example-external-image": "warn",
        "example-placeholder-ellipsis": "warn",
        "variant-not-in-example": "warn",
        "variant-coverage-unchecked": "info",
        "screen-uses-unverified": "warn",
        "screen-uses-internal": "warn",
        "screen-state-anatomy": "warn",
        "example-without-data-ds": "info",
        "screen-without-data-ds": "warn",
        "screen-data-ds-mismatch": "warn",
        "contrast-below-aa": "warn"
    },
    "contrastExceptions": [],
    "modifierPattern": ".{base}--{value}",
    "excludeAxes": ["state", "estado", "device", "divice", "viewport", "breakpoint", "platform", "responsive", "theme", "mode"],
    "coverageIgnore": {"values": ["hover", "focus", "focused", "pressed", "press", "active"], "axes": [], "components": {}},
    "ignoreTokenFamilies": ["paragraph-spacing"],
    "skipTokensInheritedFromChildren": True,
    "booleanValues": ["yes", "true", "on", "si", "sí"],
    "modifiers": {},
    "ignoreTokens": {"_all": []},
    "ignoreExampleClasses": ["sc-*"]
}


def load_config(path):
    cfg = json.loads(json.dumps(DEFAULT_CONFIG))
    if path and os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            user = json.load(fh)
        for k, v in user.items():
            if isinstance(v, dict) and isinstance(cfg.get(k), dict):
                cfg[k].update(v)
            else:
                cfg[k] = v
    return cfg


def modulo_activo(root, mid):
    """Sin declaración de módulos (proyectos anteriores a la 10.0.0) se asume activo."""
    try:
        with open(os.path.join(root, "governance", "modules.json"), encoding="utf-8") as fh:
            m = (json.load(fh).get("modules") or {}).get(mid) or {}
        return m.get("active") is not False
    except Exception:
        return True


def read(path, default=None):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except Exception:
        return default


def jload(path, default=None):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return default


def slug_value(v):
    s = re.sub(r"[^\w\s/-]", "", str(v), flags=re.U).strip().lower()
    s = re.sub(r"\s*/\s*", "-", s)
    s = re.sub(r"[\s_]+", "-", s)
    return re.sub(r"-{2,}", "-", s).strip("-")


def css_var_fallback(path):
    p = re.sub(r"\s*/\s*", "-", path.strip().lower())
    p = re.sub(r"[\s_]+", "-", p)
    p = re.sub(r"[^a-z0-9-]", "", p)
    return "--" + re.sub(r"-{2,}", "-", p).strip("-")


# ── HTML: árbol mínimo con html.parser y emparejador de selectores (.a.b, tag.a, descendiente) ──
from html.parser import HTMLParser

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class Node:
    __slots__ = ("tag", "classes", "parent", "children", "line")

    def __init__(self, tag, classes, parent, line):
        self.tag, self.classes, self.parent, self.children, self.line = tag, classes, parent, [], line


class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", set(), None, 0)
        self.cur = self.root
        self.all = []

    def handle_starttag(self, tag, attrs):
        classes = set((dict(attrs).get("class") or "").split())
        n = Node(tag, classes, self.cur, self.getpos()[0])
        self.cur.children.append(n)
        self.all.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.cur = self.cur.parent

    def handle_endtag(self, tag):
        n = self.cur
        while n is not None and n.tag != tag:
            n = n.parent
        if n is not None and n.parent is not None:
            self.cur = n.parent


def parse_simple(compound):
    """'span.a.b' → ('span', {'a','b'}); '.a' → (None, {'a'})."""
    parts = compound.split(".")
    tag = parts[0] or None
    return tag, {c for c in parts[1:] if c}


def matches_simple(node, simple):
    tag, classes = simple
    return (tag is None or node.tag == tag) and classes <= node.classes


def matches_selector(node, selector):
    """Descendiente con espacio: el último simple casa con node y los anteriores con algún ancestro, en orden."""
    simples = [parse_simple(p) for p in selector.split() if p]
    if not simples or not matches_simple(node, simples[-1]):
        return False
    anc, i = node.parent, len(simples) - 2
    while i >= 0 and anc is not None and anc.tag != "#root":
        if matches_simple(anc, simples[i]):
            i -= 1
        anc = anc.parent
    return i < 0


def descendants(node):
    for ch in node.children:
        yield ch
        yield from descendants(ch)


def select(root_nodes, selector):
    return [n for n in root_nodes if matches_selector(n, selector)]


# ── CSS: reglas planas (selector, declaraciones), atravesando @media y similares ─────────────
def css_rules(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    rules, buf, depth, stack = [], "", 0, []
    i = 0
    while i < len(css):
        ch = css[i]
        if ch == "{":
            head = buf.strip()
            buf = ""
            stack.append(head)
            depth += 1
        elif ch == "}":
            head = stack.pop() if stack else ""
            if head and not head.startswith("@"):
                rules.append((head, buf))
            buf = ""
            depth -= 1
        else:
            buf += ch
        i += 1
    return rules


def class_in_selector(selector, cls):
    return re.search(r"\." + re.escape(cls) + r"(?![\w-])", selector) is not None


class Audit:
    def __init__(self, cfg, root):
        self.cfg, self.root = cfg, root
        self.findings, self._seen = [], set()
        self.int_cfg = dcom.load_config(os.path.dirname(os.path.abspath(__file__)))
        css_path = os.path.join(root, cfg["cssFile"])
        self.css_rel = cfg["cssFile"]
        self.css = read(css_path, "") or ""
        self.rules = css_rules(self.css)
        self.selectors = " ".join(sel for sel, _ in self.rules)
        self.css_classes = set(re.findall(r"\.([A-Za-z_][\w-]*)", self.selectors))
        # alias: una variable definida como var(--otra) consume esa otra. Lo normal con la tipografía:
        # el CSS usa --font-primary (estilo de texto) y ese alias apunta al token --family-primary.
        self.alias = {}
        for texto in (read(os.path.join(root, cfg["tokensJson"]).replace(".json", ".css"), "") or "", self.css):
            for a, b in re.findall(r"(--[\w-]+)\s*:\s*var\(\s*(--[\w-]+)", texto):
                self.alias.setdefault(a, set()).add(b)
        self.var_by_path = {}
        tj = jload(os.path.join(root, cfg["tokensJson"]), {}) or {}
        for col in (tj.get("collections") or {}).values():
            for path, t in (col.get("tokens") or {}).items():
                self.var_by_path.setdefault(path, t.get("cssVar") or css_var_fallback(path))
        self.schemas = []
        for p in sorted(glob.glob(os.path.join(root, cfg["schemasDir"], "*.schema.json"))):
            if os.path.basename(p).startswith("_"):
                continue
            s = jload(p)
            if s and isinstance(s, dict) and s.get("meta"):
                s["_file"] = os.path.relpath(p, root)
                self.schemas.append(s)

    def add(self, code, file, line, prop, value, msg):
        key = (code, file, line, prop, value)
        if key in self._seen:
            return
        self._seen.add(key)
        sev = (self.cfg.get("severity") or {}).get(code, "warn")
        sev = sev if sev in ("error", "warn", "info") else "warn"
        self.findings.append({"severity": sev, "code": code, "file": file, "line": line, "property": prop,
                              "value": value, "suggestion": msg})

    # ── helpers por contrato ───────────────────────────────────────────────────
    @staticmethod
    def code_of(sch):
        return sch.get("code") or (sch.get("source") or {}).get("code") or {}

    @staticmethod
    def classes_of(sch):
        return [c for c in Audit.code_of(sch).get("classes") or [] if c]

    @staticmethod
    def enum_props(sch):
        """Ejes de variante como props enum (12.0.0) o, en un schema anterior, api.variants + api.defaults."""
        api = sch.get("api") or {}
        if isinstance(api.get("props"), list):
            return [(p["name"], p.get("values") or [], p.get("default"), p.get("figma") or "") for p in api["props"]
                    if p.get("type") == "enum" and p.get("name")] + \
                   [(p["name"], ["yes"], None, p.get("figma") or "") for p in api["props"]
                    if p.get("type") == "boolean" and p.get("name") and not str(p.get("figma") or "").startswith(("state=", "estado="))]
        out = []
        for axis, values in (api.get("variants") or {}).items():
            out.append((axis, values, (api.get("defaults") or {}).get(axis, values[0] if values else None), axis))
        return out

    def tokens_of_slug(self, slug):
        for s in self.schemas:
            if s["meta"].get("slug") == slug:
                api_ = s.get("api") or {}
                return (api_.get("tokens") if isinstance(api_.get("tokens"), list) else api_.get("tokensUsed")) or []
        return []

    def interno(self, sch):
        """Motivo de interno del contrato (ds_common.py) o None: una pieza de trabajo de Figma no se verifica."""
        return dcom.interno_de(sch, self.int_cfg)

    @staticmethod
    def status_of(sch):
        v = (sch.get("meta") or {}).get("verification") or {}
        st = v.get("status") if isinstance(v, dict) else None
        return st if st in ("verified", "unverified", "stale") else "unverified"

    def resolve(self, var, seen=None):
        """La variable y todo lo que alcanza por alias (--font-primary → --family-primary → …)."""
        seen = seen or set()
        if var in seen:
            return seen
        seen.add(var)
        for b in self.alias.get(var, ()):
            self.resolve(b, seen)
        return seen

    def rules_of(self, classes):
        return [(sel, body) for sel, body in self.rules if any(class_in_selector(sel, c) for c in classes)]

    def line_of_class(self, cls):
        m = re.search(r"^.*\." + re.escape(cls) + r"(?![\w-]).*$", self.css, re.M)
        return self.css[:m.start()].count("\n") + 1 if m else 0

    # ── 1. tokens declarados frente a tokens usados ────────────────────────────
    def tokens(self, sch):
        classes = self.classes_of(sch)
        slug = sch["meta"].get("slug", "")
        used_vars = set()
        for _, body in self.rules_of(classes):
            for v in re.findall(r"var\(\s*(--[\w-]+)", body):
                used_vars |= self.resolve(v)
        ignore = set((self.cfg.get("ignoreTokens") or {}).get("_all") or []) | set((self.cfg.get("ignoreTokens") or {}).get(slug) or [])
        families = {f.lower() for f in self.cfg.get("ignoreTokenFamilies") or []}
        inherited = set()
        if self.cfg.get("skipTokensInheritedFromChildren", True):
            # lo que liga un hijo (icono, badge…) lo realiza el CSS del hijo, no el del padre
            for child in (sch.get("relations") or {}).get("uses") or []:
                inherited |= set(self.tokens_of_slug(child))
        api_ = sch.get("api") or {}
        for path in (api_.get("tokens") if isinstance(api_.get("tokens"), list) else api_.get("tokensUsed")) or []:
            if path in ignore or path.split("/")[0].lower() in families or path in inherited:
                continue
            var = self.var_by_path.get(path) or css_var_fallback(path)
            if var in ignore or var in used_vars:
                continue
            self.add("token-not-used", sch["_file"], 0, slug, path,
                     f"el maestro de Figma liga {path} ({var}) y ninguna regla de {', '.join('.' + c for c in classes[:3])} lo usa en {self.css_rel}: "
                     f"compara con el maestro por MCP y corrige el CSS (o declara la excepción en ds-fidelity.config.json → ignoreTokens)")

    # ── 2. variantes sin CSS ───────────────────────────────────────────────────
    def variants(self, sch):
        classes = self.classes_of(sch)
        slug = sch["meta"].get("slug", "")
        simples = [c for c in classes if "--" not in c]
        propias = [c for c in simples if c == slug or c.startswith(slug + "-") or slug.startswith(c)]
        bases = (propias or simples or classes)[:]
        pattern = self.cfg.get("modifierPattern") or ".{base}--{value}"
        mods_cfg = (self.cfg.get("modifiers") or {}).get(slug) or {}
        excluded = {a.lower() for a in self.cfg.get("excludeAxes") or []}
        booleans = {b.lower() for b in self.cfg.get("booleanValues") or []}
        # lo declarado en coverageIgnore.components.<slug> con su motivo («eje=valor», lista o {"eje=valor": "motivo"}) cierra este aviso igual
        # que cierra variant-not-in-example: la misma justificación vale para los dos
        sin_css = {str(x).lower() for x in ((self.cfg.get("coverageIgnore") or {}).get("components") or {}).get(slug) or []}
        for axis, values, default_v, figma_axis in self.enum_props(sch):
            if axis.lower() in excluded or figma_axis.lower() in excluded or not values:
                continue
            default = str(default_v if default_v is not None else values[0])
            axis_cfg = mods_cfg.get(axis) or mods_cfg.get(figma_axis)
            for value in values:
                value = str(value)
                if value == default:
                    continue
                if f"{axis}={value}".lower() in sin_css or (figma_axis and f"{figma_axis}={value}".lower() in sin_css):
                    continue
                candidates = []
                if isinstance(axis_cfg, dict) and value in axis_cfg and dv is not None and dv.modificador_spec(axis_cfg[value]):
                    continue  # se declara con un atributo o un elemento interno: no necesita una clase en el CSS
                if isinstance(axis_cfg, dict) and value in axis_cfg:
                    candidates.append(axis_cfg[value])
                elif isinstance(axis_cfg, str):
                    candidates.append(axis_cfg.format(base=bases[0], axis=slug_value(axis), value=slug_value(value)))
                else:
                    for b in bases:
                        candidates.append(pattern.format(base=b, axis=slug_value(axis), value=slug_value(value)))
                        if value.lower() in booleans:
                            candidates.append(pattern.format(base=b, axis=slug_value(axis), value=slug_value(axis)))
                            if figma_axis and figma_axis != axis:
                                candidates.append(pattern.format(base=b, axis=slug_value(figma_axis), value=slug_value(figma_axis)))
                if any(self._selector_exists(c) for c in candidates):
                    continue
                self.add("variant-without-css", sch["_file"], 0, slug, f"{axis}={value}",
                         f"el contrato declara la variante {axis}={value} y {self.css_rel} no tiene {candidates[0]} ni equivalente: "
                         f"impleméntala a partir del maestro (variante {axis}={value} por MCP) o declara su selector en ds-fidelity.config.json → modifiers")

    def _selector_exists(self, candidate):
        cls = candidate.lstrip(".").strip()
        if not cls:
            return False
        if candidate.strip().startswith("."):
            return cls in self.css_classes
        return candidate in self.selectors

    # ── 2b. variantes del contrato que el ejemplo no muestra ───────────────────
    def coverage(self, sch):
        """Cada valor de cada eje de variante y cada propiedad booleana del contrato debería salir en el «Ejemplo de
        código»: es lo que la library enseña, y una muestra parcial es una muestra sesgada. La lógica vive en
        ds_variants.py (la misma que pinta la nota y la galería de la ficha)."""
        if dv is None:
            return
        slug = sch["meta"].get("slug", "")
        ex = self.code_of(sch).get("example") or ""
        a = dv.analyze(sch, ex, self.css_classes, self.cfg, self.rules)
        if not a:
            return
        if a["missing"]:
            ver = " El contrato figura como verificado: la verificación no está completa hasta cubrirlo o justificarlo." if self.status_of(sch) == "verified" else ""
            self.add("variant-not-in-example", sch["_file"], 0, slug, f"{a['visible']} de {a['total']}",
                     f"el «Ejemplo de código» muestra {a['visible']} de {a['total']} variantes de Figma; faltan: {', '.join(a['missing'])}. "
                     f"Añádelas al ejemplo (o, si no deben mostrarse, decláralas con su motivo en ds-fidelity.config.json → coverageIgnore.components.{slug}).{ver}")
        if a["unchecked"]:
            self.add("variant-coverage-unchecked", sch["_file"], 0, slug, str(len(a["unchecked"])),
                     f"no se puede comprobar la cobertura de {len(a['unchecked'])} variante(s) ({', '.join(a['unchecked'][:8])}{' …' if len(a['unchecked']) > 8 else ''}): "
                     f"ni el contrato ni el CSS dicen cómo se representan: decláralo en ds-fidelity.config.json → modifiers.{slug} ({{\"propiedad\": {{\"valor\": \".clase\"}}}}; un atributo: \"[aria-invalid=\\\"true\\\"]\"; un elemento interno: {{\"target\": \".x\", \"add\": \"[disabled]\"}} o {{\"target\": \".x\", \"presence\": true}}; sin un elemento: {{\"target\": \".x\", \"presence\": false}}; un trozo de texto: {{\"target\": \".x\", \"text\": \"€\"}}; "
                     f"un estado que solo define el CSS (un pseudoelemento, una barra nativa): {{\"css\": \".x::after\"}}); no hace falta tocar el schema")

    # ── 3. ejemplo frente a CSS ────────────────────────────────────────────────
    def example(self, sch):
        slug = sch["meta"].get("slug", "")
        ex = self.code_of(sch).get("example") or ""
        if not ex.strip():
            return
        import fnmatch
        ignore_pats = self.cfg.get("ignoreExampleClasses") or []
        used = set()
        for attr in re.findall(r'class\s*=\s*"([^"]*)"', ex):
            used.update(attr.split())
        for cls in sorted(used):
            if any(fnmatch.fnmatch(cls, p) for p in ignore_pats):
                continue
            if cls not in self.css_classes:
                self.add("example-class-missing", sch["_file"], 0, slug, cls,
                         f"el «Ejemplo de código» usa .{cls} y no existe en {self.css_rel}: el ejemplo describe otra cosa que el CSS; actualiza uno de los dos tras verificar el maestro")
        if f'data-ds="{slug}"' not in ex and "data-ds='" + slug + "'" not in ex:
            self.add("example-without-data-ds", sch["_file"], 0, slug, "data-ds",
                     f"el elemento raíz del «Ejemplo de código» no lleva data-ds=\"{slug}\": sin esa marca una pantalla no dice qué contrato (y qué maestro de Figma) es cada bloque")
        # «…» o «...» como contenido de un elemento es un marcador de «aquí va algo», no contenido: la vista previa lo
        # pinta como un punto vacío. Vale si el elemento es una elipsis real (clase o atributo «ellipsis»).
        # Elipsis real: clase o atributo que lo diga («ellipsis», «dots», «more», o lo que el proyecto declare en
        # ellipsisClasses, p. ej. «pagination-item--more»).
        elip_pats = ["*ellipsis*", "*dots*", "*more*"] + list(self.cfg.get("ellipsisClasses") or [])
        for m in re.finditer(r"<([a-zA-Z][\w-]*)([^>]*)>\s*(…|\.\.\.)\s*</\1>", ex):
            clases = re.findall(r'class\s*=\s*"([^"]*)"', m.group(2))
            toks = [t for c in clases for t in c.split()]
            if any(fnmatch.fnmatch(t, p) for t in toks for p in elip_pats) or "ellipsis" in m.group(2).lower():
                continue
            self.add("example-placeholder-ellipsis", sch["_file"], 0, slug, m.group(0)[:60],
                     "el «Ejemplo de código» usa «…» como contenido de un elemento: parece un marcador y la vista previa queda vacía; escribe un contenido de ejemplo real, o marca el elemento con la clase o el atributo «ellipsis» si es una elipsis de verdad (p. ej. la de una paginación)")
        for url in re.findall(r"""(?:src\s*=\s*["']|url\(\s*["']?)(https?://[^"')\s]+)""", ex):
            self.add("example-external-image", sch["_file"], 0, slug, url,
                     "el ejemplo carga una imagen de fuera; lo que no sale de Figma no es del DS: usa design-system/assets/ o un placeholder del propio DS")

    # ── 4. pantallas que usan contratos sin verificar ──────────────────────────
    @staticmethod
    def own_classes(sch):
        """Las clases que son del propio contrato (su slug como bloque BEM), no las de los componentes que su
        ejemplo compone: un ejemplo de tarjeta con un botón no convierte al botón en uso de la tarjeta."""
        slug = sch["meta"].get("slug", "")
        return [c for c in Audit.classes_of(sch) if c == slug or c.startswith(slug + "__") or c.startswith(slug + "--")]

    def screens(self):
        """Una pantalla usa un contrato si lleva data-ds="<slug>" o alguna clase propia del contrato."""
        by_class, by_slug, internos = {}, {}, {}
        for s in self.schemas:
            st = self.status_of(s); slug = s["meta"].get("slug", "")
            if self.interno(s):
                internos[slug] = self.interno(s)
                st = "interno"
            by_slug[slug] = st
            for c in self.own_classes(s):
                by_class.setdefault(c, (slug, st))
        clases_construibles = {sl: set(dcom.clases_propias(sch)) for sch in self.schemas
                               for sl in [sch["meta"].get("slug", "")] if sl and not self.interno(sch)}
        files = []
        for pat in self.cfg.get("screens") or []:
            files.extend(sorted(glob.glob(os.path.join(self.root, pat), recursive=True)))
        for f in files:
            html = read(f, "") or ""
            used = set()
            for attr in re.findall(r'class\s*=\s*"([^"]*)"', html):
                used.update(attr.split())
            pend, usa_internos = {}, {}
            for slug in re.findall(r'data-ds\s*=\s*["\']([^"\']+)["\']', html):
                if slug in internos:
                    usa_internos[slug] = internos[slug]
                elif slug in by_slug and by_slug[slug] != "verified":
                    pend[slug] = by_slug[slug]
            for c in used:
                if c in by_class:
                    slug, st = by_class[c]
                    if st == "interno":
                        usa_internos[slug] = internos.get(slug, "")
                    elif st != "verified":
                        pend[slug] = st
            an = dcom.analizar_pantalla(html, clases_construibles)
            rel = os.path.relpath(f, self.root)
            if an["sin_marcar"]:
                n = sum(an["sin_marcar"].values())
                lista = ", ".join("%s ×%d" % (k, v) for k, v in sorted(an["sin_marcar"].items(), key=lambda kv: (-kv[1], kv[0])))
                self.add("screen-without-data-ds", rel, 0, "pantalla", f"{n} elementos sin data-ds",
                         f"{n} elementos son un componente (llevan la clase de su contrato) y no llevan data-ds en su elemento raíz: {lista}. "
                         f"Añade data-ds=\"<slug>\" a cada uno; el informe por pantalla es scripts/screen-report.py")
            if an["no_coinciden"]:
                lista = "; ".join("data-ds=\"%s\" en <%s class=\"%s\">" % x for x in an["no_coinciden"][:6]) + (" …" if len(an["no_coinciden"]) > 6 else "")
                self.add("screen-data-ds-mismatch", rel, 0, "pantalla", f"{len(an['no_coinciden'])} data-ds que no corresponden",
                         f"un data-ds nombra un contrato que ninguna clase del elemento es: {lista}. Cambia el data-ds por el slug del componente que ese elemento es de verdad")
            if usa_internos:
                rel = os.path.relpath(f, self.root)
                lista = ", ".join(f"{k} ({v})" for k, v in sorted(usa_internos.items()))
                self.add("screen-uses-internal", rel, 0, "pantalla", f"{len(usa_internos)} piezas internas",
                         f"usa una pieza interna de Figma, que no forma parte del sistema compartido y no debería estar en una pantalla: {lista}. Sustitúyela por el componente compartido que corresponda")
            if pend:
                rel = os.path.relpath(f, self.root)
                lista = ", ".join(f"{k} ({v})" for k, v in sorted(pend.items()))
                self.add("screen-uses-unverified", rel, 0, "pantalla", f"{len(pend)} contratos sin verificar", 
                         f"usa componentes cuyo contrato no está verificado contra su maestro de Figma: {lista}. Protocolo en guides/verificacion.md")

    # ── 5. anatomía obligatoria por estado dentro de las pantallas ─────────────
    def state_anatomy(self):
        rules = []
        for s in self.schemas:
            for r in (self.code_of(s).get("stateAnatomy") or (s.get("behavior") or {}).get("stateAnatomy") or []):
                if isinstance(r, dict) and r.get("when") and r.get("require"):
                    rules.append((s["meta"].get("slug", ""), r))
        self.state_rules = len(rules)
        if not rules:
            return
        files = []
        for pat in self.cfg.get("screens") or []:
            files.extend(sorted(glob.glob(os.path.join(self.root, pat), recursive=True)))
        for f in files:
            tree = Tree()
            try:
                tree.feed(read(f, "") or "")
            except Exception:
                continue
            rel = os.path.relpath(f, self.root)
            for slug, r in rules:
                reqs = r["require"] if isinstance(r["require"], list) else [r["require"]]
                for hit in select(tree.all, r["when"]):
                    inside = list(descendants(hit))
                    falta = [q for q in reqs if not select(inside, q)]
                    if falta:
                        self.add("screen-state-anatomy", rel, hit.line, slug, r.get("id") or r["when"],
                                 f"{r.get('why') or 'anatomía incompleta para este estado'} Falta dentro de «{r['when']}»: {', '.join(falta)}. "
                                 f"Abre la ficha del componente y aplica el ejemplo completo de ese estado; no copies el marcado de otra instancia")

    # ── 7. contraste AA del texto, desde el CSS ────────────────────────────────
    def proposal_status(self, pid):
        for p in glob.glob(os.path.join(self.root, "design-system", "proposals", "**", f"{pid}.proposal.json"), recursive=True):
            d = jload(p)
            return (d or {}).get("status") or "invalid"
        return None

    def contrast(self, sch):
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import ds_contrast as dc
        except ImportError:
            return
        if not hasattr(self, "_themes"):
            tokens_css = read(os.path.join(self.root, self.cfg["tokensJson"]).replace(".json", ".css"), "") or ""
            self._themes = dc.theme_vars(tokens_css)
            self._crules = dc.css_rules(self.css)
            self.contrast_counts = {"pairs": 0, "fail": 0, "untestable": 0, "excepted": 0}
        slug = sch["meta"].get("slug", "")
        res = dc.component_pairs(slug, self._crules, self._themes)
        m = re.search(r"^\s*\." + re.escape(slug) + r"(?![\w-])[^{]*\{", self.css, re.M)
        linea = self.css.count("\n", 0, m.start()) + 1 if m else self.line_of_class(slug)
        self.contrast_counts["pairs"] += len(res["pairs"])
        self.contrast_counts["untestable"] += len(res["untestable"])
        excepciones = {(e.get("component"), e.get("state")): e.get("proposal") for e in self.cfg.get("contrastExceptions") or []}
        for x in res["pairs"]:
            if x["pass"]:
                continue
            self.contrast_counts["fail"] += 1
            tema = "" if x["theme"] == "light" else " (modo oscuro)"
            msg = (f"texto {x['fg']} ({x['fgVar'] or 'color'}) sobre {x['bg']} ({x['bgVar'] or 'fondo'}): {x['ratio']}:1, "
                   f"AA pide {x['need']}:1{tema}. Cambia la pareja de tokens en Figma (con propuesta) y sincroniza")
            pid = excepciones.get((slug, x["state"]))
            st = self.proposal_status(pid) if pid else None
            if pid and st in ("draft", "approved"):
                self.contrast_counts["excepted"] += 1
                self.add("contrast-below-aa", self.css_rel, linea, slug, x["state"],
                         msg + f" · excepción temporal mientras la propuesta {pid} esté pendiente")
                self.findings[-1]["severity"] = "warn"
            else:
                extra = (f" · la excepción apunta a la propuesta {pid}, que está {st or 'sin crear'}: ya no cubre" if pid else "")
                self.add("contrast-below-aa", self.css_rel, linea, slug, x["state"], msg + extra)

    def run(self):
        for s in self.schemas:
            if self.interno(s) or not self.classes_of(s):
                continue
            self.tokens(s)
            self.variants(s)
            self.coverage(s)
            self.example(s)
            self.contrast(s)
        self.screens()
        self.state_anatomy()
        counts = {"verified": 0, "unverified": 0, "stale": 0, "internal": 0}
        for s in self.schemas:
            if self.interno(s):
                counts["internal"] += 1  # no se verifican: no tienen CSS ni se construyen
                continue
            counts[self.status_of(s)] += 1
        return counts


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=None, help="raíz del proyecto")
    ap.add_argument("--config", default=None, help="ruta al config JSON")
    ap.add_argument("--json", action="store_true", help="salida JSON por stdout")
    ap.add_argument("--out", default=None, help="guardar el informe JSON en esta ruta (relativa a la raíz)")
    args = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(args.root or os.path.dirname(here))
    cfg = load_config(args.config or os.path.join(here, "ds-fidelity.config.json"))
    if not modulo_activo(root, "design-system"):
        print("El módulo de design system no está activo en este proyecto (governance/modules.json): "
              "no hay nada que comprobar aquí. Si se activa, esta auditoría vuelve a aplicar.")
        return 0
    audit = Audit(cfg, root)
    counts = audit.run()
    findings = sorted(audit.findings, key=lambda x: (x["file"], x["code"], x["property"], x["value"]))
    errors = [x for x in findings if x["severity"] == "error"]
    warns = [x for x in findings if x["severity"] == "warn"]
    infos = [x for x in findings if x["severity"] == "info"]
    by_code = {}
    for x in findings:
        by_code[x["code"]] = by_code.get(x["code"], 0) + 1
    con_css = sum(1 for s in audit.schemas if Audit.classes_of(s) and not audit.interno(s))
    report = {"root": ".", "errors": len(errors), "warnings": len(warns), "infos": len(infos), "byCheck": by_code,
              "contracts": len(audit.schemas), "contractsWithCss": con_css, "verification": counts, "findings": findings}
    if args.out:
        out_path = os.path.join(root, args.out)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(report, fh, ensure_ascii=False, indent=2)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        if not audit.schemas:
            print("Sin contratos en schemas/components/: nada que medir todavía (pendiente del primer sync desde Figma).")
        for x in findings:
            print(f"{x['file']}:{x['line']}: [{x['severity'].upper()}] {x['code']} · {x['property']}: {x['value']} → {x['suggestion']}")
        print(f"\n{len(errors)} errores · {len(warns)} avisos · {len(infos)} notas · {len(audit.schemas)} contratos "
              f"({counts['internal']} internos, no se verifican), {con_css} con CSS")
        print(f"Verificación contra el maestro: {counts['verified']} verified · {counts['unverified']} unverified · {counts['stale']} stale")
        if getattr(audit, "state_rules", 0):
            print(f"Anatomía por estado: {audit.state_rules} reglas declaradas en behavior.stateAnatomy, comprobadas en las pantallas de UI/")
        elif audit.schemas:
            print("Anatomía por estado: ningún contrato declara behavior.stateAnatomy; nada que comprobar en las pantallas")
        cc = getattr(audit, "contrast_counts", None)
        if cc:
            print(f"Contraste AA: {cc['pairs']} parejas texto/fondo medidas · {cc['fail']} por debajo"
                  + (f" ({cc['excepted']} con excepción temporal atada a propuesta)" if cc["excepted"] else "")
                  + f" · {cc['untestable']} no comprobables (sin fondo propio o transparente: la ficha recomienda sobre qué fondos cumplen)")
        if by_code:
            print("Avisos por comprobación: " + ", ".join(f"{k} {v}" for k, v in sorted(by_code.items(), key=lambda kv: -kv[1])))
        if errors:
            print("Corrige el CSS o la ficha a partir del maestro de Figma (protocolo en guides/verificacion.md); nunca el script ni su config.")
        print("Esta auditoría no abre Figma: solo contrasta los artefactos con lo que el contrato declara y con la verificación registrada.")
        if args.out:
            print(f"Informe guardado en {args.out}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
