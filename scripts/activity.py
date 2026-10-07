#!/usr/bin/env python3
"""
activity.py — el rastro de lo que ha pasado en el proyecto.

Un archivo que solo crece, `governance/activity.jsonl`, con una línea JSON por hecho. Existe
porque la skill exige que cada requisito cite su origen y no guardaba nada de sus propias
acciones: un techo de autonomía sin registro no se puede auditar después, y explicar a un
cliente qué hizo el agente obligaba a leerle el historial de git.

**Quién escribe qué, para que no se dupliquen:**

  · Los SCRIPTS registran lo que ejecutan. Es automático y fiable: lo llaman ellos al terminar.
  · El AGENTE registra lo que decide y lo que le autorizan, que es lo único que un script no
    puede saber. **Nunca registra una ejecución**: de eso ya se encarga quien la ejecuta.

Si una acción la ejecuta un script, el agente no la anota. Si el agente anota una decisión que
después ejecuta un script, son dos líneas distintas y complementarias, no la misma dos veces.

Límite honesto: la parte del agente depende de que se acuerde de escribirla, que es justo el
tipo de control que no funciona solo. Por eso se acota a lo que git no puede saber, y la parte
que importa para auditar —qué se ejecutó y qué produjo— la escriben los scripts.

Uso como biblioteca (desde otro script):
    from activity import log
    log(root, "script", "ds-sync", "regenerados los artefactos del DS", files=[...])

Uso desde la línea de comandos (lo usa el agente):
    python3 scripts/activity.py --actor agent --action change-business-rule \
        --detail "regla de reembolso actualizada" --capability change-business-rule --approval human-review
    python3 scripts/activity.py --tail 20        # ver las últimas líneas
"""

import argparse
import datetime
import json
import os
import sys

RUTA = os.path.join("governance", "activity.jsonl")
ACTORES = ("script", "agent", "human")


def log(root, actor, action, detail, capability=None, approval=None, files=None):
    """Añade una línea. Nunca reescribe ni borra: el rastro solo crece."""
    if actor not in ACTORES:
        raise ValueError("actor debe ser uno de %s" % (ACTORES,))
    linea = {"ts": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
             "actor": actor, "action": action, "detail": detail}
    if capability:
        linea["capability"] = capability
    if approval:
        linea["approval"] = approval
    if files:
        linea["files"] = sorted(files)[:40]
    dest = os.path.join(root, RUTA)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(linea, ensure_ascii=False) + "\n")
    return linea


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--actor", choices=ACTORES, default="agent")
    ap.add_argument("--action")
    ap.add_argument("--detail", default="")
    ap.add_argument("--capability", default=None)
    ap.add_argument("--approval", default=None)
    ap.add_argument("--tail", type=int, default=None, help="muestra las últimas N líneas y sale")
    a = ap.parse_args()
    root = os.path.abspath(a.root)

    if a.tail:
        p = os.path.join(root, RUTA)
        if not os.path.exists(p):
            print("Todavía no hay rastro: %s no existe." % RUTA)
            return 0
        for l in open(p, encoding="utf-8").read().splitlines()[-a.tail:]:
            d = json.loads(l)
            print("  %s  %-6s  %-34s %s" % (d["ts"][:19], d["actor"], d["action"], d.get("detail", "")[:60]))
        return 0

    if not a.action:
        sys.exit("[ERROR] hace falta --action (o --tail para leer)")
    if a.actor == "agent" and (a.capability or "").startswith("sync-"):
        sys.exit("[ERROR] esa ejecución la registra el script que la hace. El agente registra "
                 "decisiones y autorizaciones, no ejecuciones.")
    linea = log(root, a.actor, a.action, a.detail, a.capability, a.approval)
    print("registrado: %s · %s" % (linea["actor"], linea["action"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
