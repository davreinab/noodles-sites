#!/usr/bin/env python3
"""
ds-lifecycle.py — gobierna las retiradas del design system.

Lee el registro design-system/schemas/governance/lifecycle.json (se mantiene a mano, o desde
una propuesta aprobada) y hace tres cosas:

  1. Valida cada entrada contra su propio contrato y contra el plazo de aviso de la política.
  2. Busca en el código quién sigue usando lo que está marcado obsoleto.
  3. Sella `meta.lifecycle` en los contratos de componente, para que quien lea un contrato vea
     su estado sin abrir el registro.

Regla de plazos, configurable en el propio registro:
  · desde el día 0        el uso existente AVISA
  · desde blockNewUsage   un uso nuevo es ERROR
  · antes de minNoticeDays no se puede retirar nada

Salida: design-system/reports/lifecycle.json + resumen por consola.
Código de salida 1 si hay errores.

Uso:  python3 scripts/ds-lifecycle.py [--root .] [--check]
Sin dependencias externas: solo biblioteca estándar.
"""

import argparse
import datetime
import json
import os
import re
import sys

REQ = ["id", "kind", "since", "removeIn", "reason", "replacement"]
KINDS = ("component", "pattern", "token", "class")


def jload(p, default=None):
    try:
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return default


def days_since(iso, today):
    try:
        return (today - datetime.date.fromisoformat(iso)).days
    except Exception:
        return None


class Lifecycle:
    def __init__(self, root, today):
        self.root, self.today = root, today
        self.ds = os.path.join(root, "design-system")
        self.reg = jload(os.path.join(self.ds, "schemas", "governance", "lifecycle.json"))
        if self.reg is None:
            sys.exit("[ERROR] falta o no parsea design-system/schemas/governance/lifecycle.json")
        self.pol = self.reg.get("policy") or {}
        self.comp_dir = os.path.join(self.ds, "schemas", "components")
        self.schemas = {}
        if os.path.isdir(self.comp_dir):
            for f in sorted(os.listdir(self.comp_dir)):
                if f.endswith(".schema.json") and not f.startswith("_"):
                    self.schemas[f[:-len(".schema.json")]] = (os.path.join(self.comp_dir, f),
                                                              jload(os.path.join(self.comp_dir, f)))
        self.errors, self.warnings = [], []

    # ---- 1 · validación ----
    def validate(self):
        seen = set()
        for i, e in enumerate(self.reg.get("deprecations") or []):
            tag = e.get("id") or "entrada %d" % i
            falta = [k for k in REQ if k not in e]
            if falta:
                self.errors.append("%s: faltan campos %s" % (tag, ", ".join(falta))); continue
            if e["kind"] not in KINDS:
                self.errors.append("%s: kind '%s' no válido" % (tag, e["kind"]))
            if days_since(e["since"], self.today) is None:
                self.errors.append("%s: 'since' no es una fecha ISO" % tag)
            if e["id"] in seen:
                self.errors.append("%s: duplicado en el registro" % tag)
            seen.add(e["id"])
            if not e.get("replacement") and not (e.get("reason") or "").strip():
                self.errors.append("%s: sin sustituto hay que explicar el porqué en 'reason'" % tag)
            if e["kind"] in ("component", "pattern") and e["id"] not in self.schemas:
                self.warnings.append("%s: no hay contrato con ese slug; ¿ya se retiró?" % tag)
            d = days_since(e["since"], self.today)
            minimo = self.pol.get("minNoticeDays", 180)
            if d is not None and e.get("removed") and d < minimo:
                self.errors.append("%s: retirado a los %d días, antes del plazo mínimo de %d" % (tag, d, minimo))

    # ---- 2 · uso en el código ----
    def code_files(self, kind=None):
        """Para componentes, patrones y clases se excluye components.css: ahí está su DEFINICIÓN,
        no su uso. Para tokens sí cuenta, porque consumirlo desde el CSS del DS es uso real."""
        definicion = os.path.join(self.root, "design-system", "css", "components.css")
        out = []
        for rel in ("UI", os.path.join("design-system", "css"), os.path.join("design-system", "showcase")):
            base = os.path.join(self.root, rel)
            for dirpath, _, files in os.walk(base):
                for f in files:
                    if not f.endswith((".html", ".css")):
                        continue
                    full = os.path.join(dirpath, f)
                    if kind in ("component", "pattern", "class") and os.path.abspath(full) == os.path.abspath(definicion):
                        continue
                    out.append(full)
        return out

    def needles(self, e):
        if e["kind"] == "token":
            v = e["id"] if e["id"].startswith("--") else "--" + e["id"].replace("/", "-")
            return [v]
        if e["kind"] == "class":
            return [e["id"].lstrip(".")]
        _, sch = self.schemas.get(e["id"], (None, None))
        code = ((sch or {}).get("source") or {}).get("code") or {}
        return list(code.get("classes") or []) or [e["id"]]

    def scan(self):
        cache = {}
        usos = {}
        for e in self.reg.get("deprecations") or []:
            if not all(k in e for k in REQ):
                continue
            files = self.code_files(e["kind"])
            for f in files:
                if f not in cache:
                    cache[f] = open(f, encoding="utf-8", errors="ignore").read()
            hits = []
            for n in self.needles(e):
                pat = re.compile(r"(?<![\w-])" + re.escape(n) + r"(?![\w-])")
                for f in files:
                    c = len(pat.findall(cache[f]))
                    if c:
                        hits.append((os.path.relpath(f, self.root), c))
            if not hits:
                continue
            usos[e["id"]] = hits
            d = days_since(e["since"], self.today)
            bloqueo = self.pol.get("blockNewUsageFromDay", 120)
            total = sum(c for _, c in hits)
            donde = ", ".join("%s (%d)" % h for h in sorted(hits)[:4])
            if d is not None and d >= bloqueo:
                self.errors.append("%s: %d usos %d días después de marcarlo obsoleto, pasado el corte de %d → %s"
                                   % (e["id"], total, d, bloqueo, donde))
            else:
                self.warnings.append("%s: %d usos todavía en el código (sustituto: %s) → %s"
                                     % (e["id"], total, e.get("replacement") or "ninguno", donde))
        return usos

    # ---- 3 · sellado en los contratos ----
    def stamp(self, write):
        by_id = {e["id"]: e for e in (self.reg.get("deprecations") or []) if e.get("id")}
        cambiados = []
        for slug, (path, sch) in self.schemas.items():
            if not isinstance(sch, dict):
                continue
            e = by_id.get(slug)
            life = ({"status": "deprecated", "since": e["since"], "removeIn": e["removeIn"],
                     "replacement": e.get("replacement"), "reason": e.get("reason")}
                    if e else {"status": "active", "since": None, "removeIn": None,
                               "replacement": None, "reason": None})
            if (sch.get("meta") or {}).get("lifecycle") == life:
                continue
            sch.setdefault("meta", {})["lifecycle"] = life
            cambiados.append(slug)
            if write:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(json.dumps(sch, ensure_ascii=False, indent=2) + "\n")
        return cambiados

    def report(self, usos, sellados):
        return {
            "designSystem": self.reg.get("designSystem"),
            "generatedAt": self.today.isoformat(),
            "note": "Informe de scripts/ds-lifecycle.py. No editar a mano.",
            "policy": self.pol,
            "summary": {"deprecations": len(self.reg.get("deprecations") or []),
                        "errors": len(self.errors), "warnings": len(self.warnings),
                        "stillUsed": len(usos)},
            "errors": self.errors, "warnings": self.warnings,
            "usage": {k: [{"file": f, "hits": c} for f, c in v] for k, v in usos.items()},
            "contractsStamped": sellados,
        }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--check", action="store_true", help="no escribe nada; solo valida e informa")
    ap.add_argument("--today", default=None, help="fecha ISO de referencia (para pruebas)")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    today = datetime.date.fromisoformat(a.today) if a.today else datetime.date.today()

    lc = Lifecycle(root, today)
    lc.validate()
    usos = lc.scan()
    sellados = lc.stamp(write=not a.check)
    rep = lc.report(usos, sellados)

    n = rep["summary"]["deprecations"]
    print("Retiradas registradas: %d · en uso todavía: %d" % (n, rep["summary"]["stillUsed"]))
    for w in lc.warnings:
        print("  AVISO  ", w)
    for e in lc.errors:
        print("  ERROR  ", e)
    if sellados:
        print("  %s meta.lifecycle en: %s" % ("Sellaría" if a.check else "Sellado", ", ".join(sellados[:8])
                                              + (" …" if len(sellados) > 8 else "")))
    if not n:
        print("  Nada marcado como obsoleto. El registro está vacío, que es lo normal al principio.")

    if not a.check and sellados:
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from activity import log
            log(root, "script", "ds-lifecycle", "sellado meta.lifecycle en %d contratos" % len(sellados))
        except Exception:
            pass
    if not a.check:
        dest = os.path.join(root, "design-system", "reports", "lifecycle.json")
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(json.dumps(rep, ensure_ascii=False, indent=2) + "\n")
    return 1 if lc.errors else 0


if __name__ == "__main__":
    sys.exit(main())
