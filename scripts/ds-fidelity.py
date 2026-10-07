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
     `.<clase-base>--<eje>`.
  3. example-class-missing · Cada clase del «Ejemplo de código» (`source.code.example`) existe como
     selector en el CSS. example-external-image · El ejemplo no carga imágenes de fuera (http/https):
     lo que no sale de Figma no es del DS.
  4. screen-uses-unverified · Una pantalla de UI/ que usa clases de un contrato `unverified` o `stale`
     recibe un aviso con la lista «pantalla → componentes». El estado vive en `meta.verification` de
     cada schema (lo escribe quien verifica, siguiendo el protocolo de design.md; lo caduca ds-sync
     cuando cambia el maestro). Sin bloque, el contrato cuenta como `unverified`.

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
        "screen-uses-unverified": "warn"
    },
    "modifierPattern": ".{base}--{value}",
    "excludeAxes": ["state", "estado", "device", "divice", "viewport", "breakpoint", "platform", "responsive", "theme", "mode"],
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
        sev = "error" if sev == "error" else "warn"
        self.findings.append({"severity": sev, "code": code, "file": file, "line": line, "property": prop,
                              "value": value, "suggestion": msg})

    # ── helpers por contrato ───────────────────────────────────────────────────
    @staticmethod
    def classes_of(sch):
        return [c for c in ((sch.get("source") or {}).get("code") or {}).get("classes") or [] if c]

    def tokens_of_slug(self, slug):
        for s in self.schemas:
            if s["meta"].get("slug") == slug:
                return (s.get("api") or {}).get("tokensUsed") or []
        return []

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
        for path in (sch.get("api") or {}).get("tokensUsed") or []:
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
        api = sch.get("api") or {}
        variants = api.get("variants") or {}
        defaults = api.get("defaults") or {}
        simples = [c for c in classes if "--" not in c]
        propias = [c for c in simples if c == slug or c.startswith(slug + "-") or slug.startswith(c)]
        bases = (propias or simples or classes)[:]
        pattern = self.cfg.get("modifierPattern") or ".{base}--{value}"
        mods_cfg = (self.cfg.get("modifiers") or {}).get(slug) or {}
        excluded = {a.lower() for a in self.cfg.get("excludeAxes") or []}
        booleans = {b.lower() for b in self.cfg.get("booleanValues") or []}
        for axis, values in variants.items():
            if axis.lower() in excluded or not values:
                continue
            default = str(defaults.get(axis, values[0]))
            axis_cfg = mods_cfg.get(axis)
            for value in values:
                value = str(value)
                if value == default:
                    continue
                candidates = []
                if isinstance(axis_cfg, dict) and value in axis_cfg:
                    candidates.append(axis_cfg[value])
                elif isinstance(axis_cfg, str):
                    candidates.append(axis_cfg.format(base=bases[0], axis=slug_value(axis), value=slug_value(value)))
                else:
                    for b in bases:
                        candidates.append(pattern.format(base=b, axis=slug_value(axis), value=slug_value(value)))
                        if value.lower() in booleans:
                            candidates.append(pattern.format(base=b, axis=slug_value(axis), value=slug_value(axis)))
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

    # ── 3. ejemplo frente a CSS ────────────────────────────────────────────────
    def example(self, sch):
        slug = sch["meta"].get("slug", "")
        ex = ((sch.get("source") or {}).get("code") or {}).get("example") or ""
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
        for url in re.findall(r"""(?:src\s*=\s*["']|url\(\s*["']?)(https?://[^"')\s]+)""", ex):
            self.add("example-external-image", sch["_file"], 0, slug, url,
                     "el ejemplo carga una imagen de fuera; lo que no sale de Figma no es del DS: usa design-system/assets/ o un placeholder del propio DS")

    # ── 4. pantallas que usan contratos sin verificar ──────────────────────────
    def screens(self):
        by_class = {}
        for s in self.schemas:
            st = self.status_of(s)
            for c in self.classes_of(s):
                by_class.setdefault(c, (s["meta"].get("slug", ""), st))
        files = []
        for pat in self.cfg.get("screens") or []:
            files.extend(sorted(glob.glob(os.path.join(self.root, pat), recursive=True)))
        for f in files:
            html = read(f, "") or ""
            used = set()
            for attr in re.findall(r'class\s*=\s*"([^"]*)"', html):
                used.update(attr.split())
            pend = {}
            for c in used:
                if c in by_class and by_class[c][1] != "verified":
                    slug, st = by_class[c]
                    pend[slug] = st
            if pend:
                rel = os.path.relpath(f, self.root)
                lista = ", ".join(f"{k} ({v})" for k, v in sorted(pend.items()))
                self.add("screen-uses-unverified", rel, 0, "pantalla", f"{len(pend)} contratos sin verificar", 
                         f"usa componentes cuyo contrato no está verificado contra su maestro de Figma: {lista}. Protocolo en design.md § Verificación contra el maestro")

    def run(self):
        for s in self.schemas:
            if not self.classes_of(s):
                continue
            self.tokens(s)
            self.variants(s)
            self.example(s)
        self.screens()
        counts = {"verified": 0, "unverified": 0, "stale": 0}
        for s in self.schemas:
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
    by_code = {}
    for x in findings:
        by_code[x["code"]] = by_code.get(x["code"], 0) + 1
    con_css = sum(1 for s in audit.schemas if Audit.classes_of(s))
    report = {"root": root, "errors": len(errors), "warnings": len(warns), "byCheck": by_code,
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
        print(f"\n{len(errors)} errores · {len(warns)} avisos · {len(audit.schemas)} contratos, {con_css} con CSS")
        print(f"Verificación contra el maestro: {counts['verified']} verified · {counts['unverified']} unverified · {counts['stale']} stale")
        if by_code:
            print("Avisos por comprobación: " + ", ".join(f"{k} {v}" for k, v in sorted(by_code.items(), key=lambda kv: -kv[1])))
        if errors:
            print("Corrige el CSS o la ficha a partir del maestro de Figma (protocolo en design.md § Verificación contra el maestro); nunca el script ni su config.")
        print("Esta auditoría no abre Figma: solo contrasta los artefactos con lo que el contrato declara y con la verificación registrada.")
        if args.out:
            print(f"Informe guardado en {args.out}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
