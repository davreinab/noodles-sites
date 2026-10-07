#!/usr/bin/env python3
"""
agent-readiness.py — puntúa el design system contra la rúbrica propia de preparación para
agentes que define design-system/schemas/governance/agent-readiness.json.

Los criterios se verifican contra los artefactos que genera esta skill. La rúbrica es del
proyecto: no descarga nada, no consulta fuentes externas y no depende de convenciones ajenas.

Salida: design-system/reports/agent-readiness.json + resumen por consola.

Estados por criterio:
  cumple      la comprobación pasa
  no-cumple   la comprobación falla y explica por qué
  pendiente   aún no hay material que comprobar (p. ej. ningún componente sincronizado)
  no-aplica   el proyecto ha decidido no tener esa capacidad; sale del denominador

Uso:  python3 scripts/agent-readiness.py [--root .] [--check] [--min N]
      --check  no escribe; falla si el informe en disco está desactualizado
      --min N  además, falla si la nota es menor que N
Sin dependencias externas: solo biblioteca estándar.
"""

import argparse
import json
import os
import re
import subprocess
import sys

CUMPLE, NO_CUMPLE, PENDIENTE, NO_APLICA = "cumple", "no-cumple", "pendiente", "no-aplica"



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


def jload(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None


class Rater:
    def __init__(self, root):
        self.root = root
        self.ds = os.path.join(root, "design-system")
        self.rubric = jload(os.path.join(self.ds, "schemas", "governance", "agent-readiness.json"))
        if not self.rubric:
            sys.exit("[ERROR] falta o no parsea design-system/schemas/governance/agent-readiness.json")
        self.manifest = jload(os.path.join(self.ds, "agent-manifest.json")) or {}
        self.tokens = jload(os.path.join(self.ds, "tokens", "tokens.json")) or {}
        self.index = jload(os.path.join(self.ds, "schemas", "index.json")) or {}
        self.comp_dir = os.path.join(self.ds, "schemas", "components")
        self.schemas = {}
        if os.path.isdir(self.comp_dir):
            for f in sorted(os.listdir(self.comp_dir)):
                if f.endswith(".schema.json") and not f.startswith("_"):
                    self.schemas[f[:-len(".schema.json")]] = jload(os.path.join(self.comp_dir, f))

    # ---- utilidades ----
    def registry_slugs(self):
        out = set()
        for key in ("components", "registry"):
            for e in (self.index.get(key) or []):
                if isinstance(e, dict) and e.get("slug"):
                    out.add(e["slug"])
                elif isinstance(e, str):
                    out.add(e)
        return out

    def all_tokens(self):
        for col in (self.tokens.get("collections") or {}).values():
            for t in (col.get("tokens") or {}).values():
                yield t

    def css_text(self):
        p = os.path.join(self.ds, "css", "components.css")
        return open(p, encoding="utf-8").read() if os.path.exists(p) else ""

    # ---- criterios ----
    def c_entry_point(self):
        if not self.manifest:
            return NO_CUMPLE, "no hay agent-manifest.json legible"
        missing = [k for k, v in (self.manifest.get("resources") or {}).items()
                   if isinstance(v, str) and not os.path.exists(os.path.normpath(os.path.join(self.ds, v)))]
        if missing:
            return NO_CUMPLE, "resources apuntan a rutas inexistentes: " + ", ".join(sorted(missing))
        return CUMPLE, "manifiesto presente y todas sus rutas existen"

    def c_machine_readable_tokens(self):
        toks = list(self.all_tokens())
        if not toks:
            return PENDIENTE, "tokens.json sin tokens: falta el primer sync desde Figma"
        req = ((self.tokens.get("tokenContract") or {}).get("requiredFields")
               or ["path", "type", "value", "resolvedValue", "alias", "modes", "scopes", "description", "source"])
        bad = [t.get("path", "?") for t in toks if [f for f in req if f not in t]]
        if bad:
            return NO_CUMPLE, "%d tokens incumplen tokenContract (p. ej. %s)" % (len(bad), bad[0])
        return CUMPLE, "%d tokens con contrato completo" % len(toks)

    def c_component_registry(self):
        reg, files = self.registry_slugs(), set(self.schemas)
        if not reg and not files:
            return PENDIENTE, "sin componentes sincronizados todavía"
        if reg != files:
            only_r, only_f = sorted(reg - files), sorted(files - reg)
            det = []
            if only_r:
                det.append("en el índice sin schema: " + ", ".join(only_r))
            if only_f:
                det.append("con schema sin entrada en el índice: " + ", ".join(only_f))
            return NO_CUMPLE, "; ".join(det)
        return CUMPLE, "%d componentes con correspondencia 1:1 entre índice y contratos" % len(reg)

    def c_typed_contracts(self):
        if not self.schemas:
            return PENDIENTE, "sin contratos de componente todavía"
        base = jload(os.path.join(self.comp_dir, "..", "_component.schema.json")) or {}
        req = base.get("required") or ["id", "meta", "source", "api"]
        bad = []
        for slug, sch in self.schemas.items():
            if not isinstance(sch, dict):
                bad.append("%s: no parsea" % slug); continue
            falta = [k for k in req if k not in sch]
            if falta:
                bad.append("%s: sin %s" % (slug, ", ".join(falta))); continue
            api = sch.get("api") or {}
            if not isinstance(api.get("variants"), (dict, list)) or not isinstance(api.get("states"), list):
                bad.append("%s: variantes o estados sin lista cerrada" % slug)
        if bad:
            return NO_CUMPLE, "%d contratos incompletos (p. ej. %s)" % (len(bad), bad[0])
        return CUMPLE, "%d contratos con claves obligatorias y valores cerrados" % len(self.schemas)

    def c_runnable_patterns(self):
        if not self.schemas:
            return PENDIENTE, "sin contratos de componente todavía"
        css = self.css_text()
        if not css:
            return PENDIENTE, "css/components.css vacío o inexistente"
        bad = []
        for slug, sch in self.schemas.items():
            code = ((sch or {}).get("source") or {}).get("code") or {}
            if not code.get("example"):
                bad.append("%s: sin ejemplo de código" % slug); continue
            huerfanas = [c for c in (code.get("classes") or []) if not re.search(r"[.\s,{]" + re.escape(c) + r"\b", css)]
            if huerfanas:
                bad.append("%s: clases sin realizar en components.css (%s)" % (slug, ", ".join(huerfanas[:3])))
        if bad:
            return NO_CUMPLE, "%d contratos sin ejemplo ejecutable (p. ej. %s)" % (len(bad), bad[0])
        return CUMPLE, "%d contratos con ejemplo y clases existentes" % len(self.schemas)

    def c_scoped_retrieval(self):
        r = self.manifest.get("retrieval") or {}
        if r.get("fullSystemLoad") is not False:
            return NO_CUMPLE, "el manifiesto no declara fullSystemLoad: false"
        if not r.get("componentContract"):
            return NO_CUMPLE, "el manifiesto no declara la ruta de contrato por componente"
        return CUMPLE, "carga parcial declarada, con ruta por componente"

    def c_semantic_naming(self):
        toks = list(self.all_tokens())
        if not toks:
            return PENDIENTE, "tokens.json sin tokens todavía"
        if not any(t.get("alias") for t in toks):
            return NO_CUMPLE, "ningún token es alias de otro: no hay capa semántica"
        audit = jload(os.path.join(self.ds, "reports", "token-audit.json"))
        if audit is None:
            return PENDIENTE, "capa semántica presente; falta el informe de token-audit para confirmar el consumo"
        errores = audit.get("errors")
        n = len(errores) if isinstance(errores, list) else (errores or audit.get("errorCount") or 0)
        if n:
            return NO_CUMPLE, "token-audit reporta %s errores de consumo o valores crudos" % n
        return CUMPLE, "capa semántica presente y token-audit sin errores"

    def c_external_token_format(self):
        exp = ((self.manifest.get("exports") or {}).get("dtcg") or {})
        out = os.path.join(self.ds, "tokens", "w3c")
        existe = os.path.isdir(out) and any(f.endswith(".json") for f in os.listdir(out))
        if not exp.get("enabled") and not existe:
            return NO_APLICA, "exportación no solicitada por el proyecto"
        script = os.path.join(self.root, "scripts", "tokens-dtcg.py")
        if not os.path.exists(script):
            return NO_CUMPLE, "exportación activada pero falta scripts/tokens-dtcg.py"
        try:
            r = subprocess.run([sys.executable, script, "--root", self.root, "--check"],
                               capture_output=True, text=True, timeout=120)
        except Exception as e:
            return NO_CUMPLE, "no se pudo comprobar la exportación (%s)" % e
        if r.returncode != 0:
            return NO_CUMPLE, "la exportación está desactualizada respecto a tokens.json"
        return CUMPLE, "exportación activada y al día"

    def c_context_protocol(self):
        integ = (self.manifest.get("integrations") or {}).get("customDesignSystemMcp") or {}
        if not integ.get("required"):
            return NO_APLICA, "el proyecto no usa un servidor de contexto propio; la ruta por archivos cubre el caso"
        return (CUMPLE, "servidor propio declarado") if integ.get("configured") else \
               (NO_CUMPLE, "declarado como necesario pero no configurado")

    # ---- ejecución ----
    def run(self):
        checks = {
            "entry-point": self.c_entry_point, "machine-readable-tokens": self.c_machine_readable_tokens,
            "component-registry": self.c_component_registry, "typed-contracts": self.c_typed_contracts,
            "runnable-patterns": self.c_runnable_patterns, "scoped-retrieval": self.c_scoped_retrieval,
            "semantic-naming": self.c_semantic_naming, "external-token-format": self.c_external_token_format,
            "context-protocol": self.c_context_protocol,
        }
        results = []
        for c in self.rubric["criteria"]:
            fn = checks.get(c["id"])
            state, detail = fn() if fn else (PENDIENTE, "sin comprobación implementada")
            results.append({"id": c["id"], "title": c["title"], "status": state, "detail": detail})

        aplicables = [r for r in results if r["status"] != NO_APLICA]
        cumplidos = [r for r in aplicables if r["status"] == CUMPLE]
        score = round(5 * len(cumplidos) / len(aplicables), 1) if aplicables else 0.0
        umbral = ((self.rubric.get("scoring") or {}).get("passThreshold") or 4)
        return {
            "designSystem": self.rubric.get("designSystem"),
            "rubricVersion": self.rubric.get("rubricVersion"),
            "note": "Informe generado por scripts/agent-readiness.py. No editar a mano.",
            "score": score, "scale": "0-5", "passThreshold": umbral, "passes": score >= umbral,
            "counts": {"cumple": len(cumplidos), "aplicables": len(aplicables),
                       "noAplica": len(results) - len(aplicables)},
            "criteria": results,
        }


ICON = {CUMPLE: "✔", NO_CUMPLE: "✘", PENDIENTE: "·", NO_APLICA: "–"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--check", action="store_true", help="no escribe; falla si el informe está desactualizado")
    ap.add_argument("--min", type=float, default=None, help="falla si la nota es menor que este valor")
    a = ap.parse_args()
    root = os.path.abspath(a.root)

    if not modulo_activo(root, "design-system"):
        print("El módulo de design system no está activo: no hay artefactos que puntuar. "
              "La rúbrica vuelve a aplicar cuando se active.")
        return 0

    report = Rater(root).run()
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    dest = os.path.join(root, "design-system", "reports", "agent-readiness.json")

    for r in report["criteria"]:
        print("  %s %-26s %-10s %s" % (ICON[r["status"]], r["id"], r["status"], r["detail"]))
    print("\nNota: %s / 5 · %d de %d criterios aplicables · %d no aplican por decisión del proyecto"
          % (report["score"], report["counts"]["cumple"], report["counts"]["aplicables"], report["counts"]["noAplica"]))

    rc = 0
    if a.check:
        if not os.path.exists(dest) or open(dest, encoding="utf-8").read() != text:
            print("DESACTUALIZADO: design-system/reports/agent-readiness.json")
            rc = 1
    else:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(text)
    if a.min is not None and report["score"] < a.min:
        print("NOTA INSUFICIENTE: %s < %s" % (report["score"], a.min))
        rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
