#!/usr/bin/env python3
"""ds-budget.py — cuánto cuesta leer el proyecto, en tokens, y que no vuelva a engordar sin que se note.

Cada tarea de design system carga AGENTS.md y design-system/design.md (el router y las reglas duras) enteros; las
guías de design-system/guides/ se leen solo cuando la tarea lo pide. Este script mide la carga típica y cada guía, y
avisa si algo pasa del presupuesto de scripts/ds-budget.config.json.
Los tokens son una aproximación (caracteres / 3,6): sirve para comparar y para vigilar, no para facturar.

Uso:  python3 scripts/ds-budget.py              # informe: carga típica, secciones de design.md, fichas más pesadas
      python3 scripts/ds-budget.py --strict     # sale con 1 si algo pasa del presupuesto (por defecto solo avisa)
      python3 scripts/ds-budget.py --json
En un proyecto anterior a la 12.20.0 design.md trae todo dentro y pesa unas cuatro veces más: ds-sync lo reparte en
guías al actualizar. Sin dependencias: solo biblioteca estándar.
"""
import argparse
import glob
import json
import os
import re
import sys

CHARS_PER_TOKEN = 3.6


def tok(text):
    return int(round(len(text) / CHARS_PER_TOKEN))


def read(p):
    try:
        with open(p, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def jread(p, d=None):
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return d


def sections(text):
    out, titulo, buf = [], "(cabecera)", []
    for line in text.split("\n"):
        if line.startswith("## "):
            out.append((titulo, tok("\n".join(buf))))
            titulo, buf = line[3:].strip(), []
        buf.append(line)
    out.append((titulo, tok("\n".join(buf))))
    return [x for x in out if x[1] > 0]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=None)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(a.root or os.path.dirname(here))
    ds = os.path.join(root, "design-system")
    cfg = {"agentsMd": 5000, "designMd": {"figma": 8000, "repo": 8000}, "ficha": 3000, "guide": 14000}
    user = jread(os.path.join(here, "ds-budget.config.json"), {}) or {}
    for k in ("agentsMd", "ficha", "guide"):
        if isinstance(user.get(k), int):
            cfg[k] = user[k]
    if isinstance(user.get("designMd"), dict):
        cfg["designMd"].update({k: v for k, v in user["designMd"].items() if isinstance(v, int)})
    modo = (jread(os.path.join(ds, "agent-manifest.json"), {}) or {}).get("sourceMode") or "figma"
    agents = tok(read(os.path.join(root, "AGENTS.md")))
    dtext = read(os.path.join(ds, "design.md"))
    design = tok(dtext)
    secs = sorted(sections(dtext), key=lambda x: -x[1])
    fichas = []
    for p in glob.glob(os.path.join(ds, "docs", "components", "*.md")) + glob.glob(os.path.join(ds, "docs", "patterns", "*.md")):
        if not os.path.basename(p).startswith("_"):
            fichas.append((os.path.relpath(p, root), tok(read(p))))
    fichas.sort(key=lambda x: -x[1])
    guias = []
    for p in sorted(glob.glob(os.path.join(ds, "guides", "*.md"))):
        guias.append((os.path.relpath(p, root), tok(read(p))))
    avisos = []
    if agents > cfg["agentsMd"]:
        avisos.append("AGENTS.md pesa %d tokens y el presupuesto es %d" % (agents, cfg["agentsMd"]))
    limite = cfg["designMd"].get(modo, cfg["designMd"]["figma"])
    if design > limite:
        avisos.append("design.md pesa %d tokens y el presupuesto en modo %s es %d" % (design, modo, limite))
    for f, n in guias:
        if n > cfg["guide"]:
            avisos.append("la guía %s pesa %d tokens (presupuesto %d)" % (f, n, cfg["guide"]))
    for f, n in fichas:
        if n > cfg["ficha"]:
            avisos.append("la ficha %s pesa %d tokens (presupuesto %d)" % (f, n, cfg["ficha"]))
    res = {"mode": modo, "agentsMd": agents, "designMd": design, "typicalTask": agents + design,
           "guides": guias, "sections": secs, "heaviestFichas": fichas[:5], "warnings": avisos}
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print("ds-budget · modo %s" % modo)
        print("  carga típica de una tarea de DS: %d tokens (AGENTS.md %d + design.md %d)" % (agents + design, agents, design))
        print("  secciones más pesadas de design.md:")
        for t, n in secs[:5]:
            print("    %6d  %s" % (n, t[:70]))
        if guias:
            print("  guías (solo si la tarea las pide): " + ", ".join("%s %d" % (os.path.basename(f)[:-3], n) for f, n in guias))
        if fichas:
            print("  fichas más pesadas: " + ", ".join("%s %d" % (os.path.basename(f)[:-3], n) for f, n in fichas[:3]))
        for w in avisos:
            print("  [AVISO] " + w)
        if not avisos:
            print("  dentro del presupuesto")
    return 1 if (a.strict and avisos) else 0


if __name__ == "__main__":
    sys.exit(main())
