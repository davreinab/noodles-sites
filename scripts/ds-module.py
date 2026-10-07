#!/usr/bin/env python3
"""
ds-module.py — de qué está hecho este proyecto, y cómo añadirle una parte más tarde.

No todos los proyectos tienen todo. Hay encargos de solo investigación y estrategia, de solo
estrategia y design system, y de los tres. Y es normal arrancar con investigación y estrategia
y montar el design system semanas después.

Lo que no está activo **no se crea, no se audita y no se exige**. Las comprobaciones consultan
este estado antes de pedir nada: sin esto, un proyecto de investigación arrastra 36 archivos de
design system que nadie va a usar y una auditoría que los reclama en cada commit.

Uso:
    python3 scripts/ds-module.py                      estado de los tres módulos
    python3 scripts/ds-module.py --activate design-system --by "Nombre"
    python3 scripts/ds-module.py --deactivate investigacion --by "Nombre"
    python3 scripts/ds-module.py --is-active design-system    sale 0 si lo está, 1 si no

`--activate` registra la decisión con fecha y persona, y lista las rutas que faltan por crear:
**no las crea él**. Copiarlas desde las plantillas de la skill es trabajo del agente, que es
quien tiene las plantillas; este script lleva la contabilidad.

Desactivar **no borra nada**: solo deja de exigirlo. Borrar es decisión de una persona.

Sin dependencias: solo biblioteca estándar.
"""

import argparse
import datetime
import json
import os
import sys

RUTA = os.path.join("governance", "modules.json")


def cargar(root):
    p = os.path.join(root, RUTA)
    if not os.path.exists(p):
        sys.exit("[ERROR] falta %s: este proyecto no declara de qué está hecho" % RUTA)
    with open(p, encoding="utf-8") as fh:
        return json.load(fh), p


def guardar(doc, p):
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(doc, ensure_ascii=False, indent=2) + "\n")


def faltan(root, mod):
    out = []
    for r in mod.get("paths") or []:
        if not os.path.exists(os.path.join(root, r.rstrip("/"))):
            out.append(r)
    return out


def estado(root, doc):
    filas = []
    for mid, m in (doc.get("modules") or {}).items():
        a = m.get("active")
        pend = faltan(root, m) if a else []
        filas.append({"id": mid, "title": m.get("title"), "active": a,
                      "decidedAt": m.get("decidedAt"), "decidedBy": m.get("decidedBy"),
                      "activatedAt": m.get("activatedAt"), "activatedBy": m.get("activatedBy"),
                      "missingPaths": pend})
    return filas


ICONO = {True: "✔", False: "–", None: "?"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--activate", metavar="ID")
    ap.add_argument("--deactivate", metavar="ID")
    ap.add_argument("--is-active", dest="is_active", metavar="ID")
    ap.add_argument("--by", default=None, help="quién lo decide; obligatorio al activar o desactivar")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    if a.is_active and not os.path.exists(os.path.join(root, RUTA)):
        # Sin declaración de módulos (proyectos anteriores a la 10.0.0) todo cuenta como activo,
        # igual que en token-audit y context-audit: así el gancho no se salta auditorías.
        return 0
    doc, p = cargar(root)
    mods = doc.get("modules") or {}

    if a.is_active:
        if a.is_active not in mods:
            sys.exit("[ERROR] no existe el módulo '%s'. Hay: %s" % (a.is_active, ", ".join(mods)))
        return 0 if mods[a.is_active].get("active") else 1

    for accion, valor in (("activate", True), ("deactivate", False)):
        mid = getattr(a, accion if accion == "activate" else "deactivate")
        if not mid:
            continue
        if mid not in mods:
            sys.exit("[ERROR] no existe el módulo '%s'. Hay: %s" % (mid, ", ".join(mods)))
        if not a.by:
            sys.exit("[ERROR] hace falta --by: una decisión sin dueño no se puede discutir después")
        m = mods[mid]
        if m.get("active") is valor:
            print("'%s' ya estaba %s. No se toca nada." % (mid, "activo" if valor else "inactivo"))
            return 0
        m["active"] = valor
        m["decidedAt"], m["decidedBy"] = datetime.date.today().isoformat(), a.by
        m["activatedAt" if valor else "deactivatedAt"] = datetime.date.today().isoformat()
        m["activatedBy" if valor else "deactivatedBy"] = a.by
        guardar(doc, p)
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from activity import log
            log(root, "script", "ds-module", "%s el módulo %s" % ("activado" if valor else "desactivado", mid))
        except Exception:
            pass
        if valor:
            pend = faltan(root, m)
            print("Módulo '%s' activado por %s." % (mid, a.by))
            if pend:
                print("\nFaltan por crear %d rutas. Cópialas desde las plantillas de la skill:" % len(pend))
                for r in pend:
                    print("  ·", r)
                print("\nY vuelve a ejecutar las comprobaciones: a partir de ahora se exigen.")
            else:
                print("Todas sus rutas ya existen.")
        else:
            print("Módulo '%s' desactivado por %s. **No se ha borrado nada**: solo deja de exigirse."
                  % (mid, a.by))
        return 0

    filas = estado(root, doc)
    if a.json:
        print(json.dumps({"modules": filas}, ensure_ascii=False, indent=2))
        return 0
    print("De qué está hecho este proyecto:\n")
    for f in filas:
        marca = ICONO[f["active"]]
        if f["active"] and f["activatedAt"]:
            cuando = " · desde %s, %s" % (f["activatedAt"], f["activatedBy"])
        elif f["active"] is False and f["decidedAt"]:
            cuando = " · apagado el %s, %s" % (f["decidedAt"], f["decidedBy"])
        else:
            cuando = ""
        print("  %s %-16s %s%s" % (marca, f["id"], f["title"], cuando))
        if f["active"] and f["missingPaths"]:
            print("      ⚠ activo pero le faltan %d rutas: %s" %
                  (len(f["missingPaths"]), ", ".join(f["missingPaths"][:3])))
    sin = [f["id"] for f in filas if f["active"] is None]
    if sin:
        print("\nSin decidir: %s. Se pregunta, no se presupone." % ", ".join(sin))
    print("\nActivar uno más tarde es normal: --activate <id> --by \"Nombre\".")
    return 0


if __name__ == "__main__":
    sys.exit(main())
