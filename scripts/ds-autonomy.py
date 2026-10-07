#!/usr/bin/env python3
"""
ds-autonomy.py — publica hasta dónde puede llegar el agente en este proyecto, y comprueba que
lo declarado sea coherente.

Dos dimensiones que no hay que confundir:

  · La AUTONOMÍA se declara por capacidad (governance/capabilities.json → level).
  · El TIPO DE EJECUCIÓN se declara por paso (steps: D determinista, C cognitivo, H humano).

El nivel no sale de si la capacidad escribe o no, sino de qué pasos contiene, qué decisiones
puede tomar y qué controles hay antes del efecto. Por eso regenerar tokens desde la fuente de
verdad puede ir por encima de cambiar una regla de negocio, aunque las dos escriban.

El permiso efectivo de cada capacidad es el MENOR entre su nivel natural y el techo del
proyecto. Bajar el techo aprieta todas las capacidades a la vez.

Límite honesto: esto no impide físicamente que un modelo actúe. La skill es Markdown y
scripts. El techo muerde en el gancho de pre-commit, en la integración continua y en los
scripts que se niegan a ejecutarse.

Salida: governance/reports/autonomy.json + tabla efectiva por consola.
Código de salida 1 si hay incoherencias. Con el techo sin decidir NO falla: lo dice.

Uso:  python3 scripts/ds-autonomy.py [--root .] [--check]
Sin dependencias: solo biblioteca estándar.
"""

import argparse
import json
import os
import sys

PASOS = ("D", "C", "H")


def jload(p, default=None):
    try:
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return default


class Autonomy:
    def __init__(self, root):
        self.root = root
        g = os.path.join(root, "governance")
        self.aut = jload(os.path.join(g, "autonomy.json"))
        self.cap = jload(os.path.join(g, "capabilities.json"))
        if self.aut is None or self.cap is None:
            sys.exit("[ERROR] faltan governance/autonomy.json o governance/capabilities.json")
        self.niveles = {int(x["level"]) for x in (self.aut.get("scale") or [])}
        self.techo = (self.aut.get("ceiling") or {})
        self.errores = []

    def validar(self):
        c = self.techo
        maxi = c.get("maxLevel")
        if maxi is None or int(maxi) not in self.niveles:
            self.errores.append("el techo (%s) no es un nivel de la escala %s" % (maxi, sorted(self.niveles)))
        decidido = bool(c.get("decidedBy")) and bool(c.get("decidedAt"))
        if not decidido and (c.get("decidedBy") or c.get("decidedAt")):
            self.errores.append("el techo está decidido a medias: hacen falta quién y cuándo, o ninguno de los dos")

        vistas = set()
        for x in (self.cap.get("capabilities") or []):
            a = x.get("action", "?")
            if a in vistas:
                self.errores.append("%s: capacidad duplicada" % a)
            vistas.add(a)
            if not isinstance(x.get("level"), int) or x["level"] not in self.niveles:
                self.errores.append("%s: nivel %r fuera de la escala" % (a, x.get("level")))
            pasos = x.get("steps") or []
            if not pasos or any(p not in PASOS for p in pasos):
                self.errores.append("%s: steps %r; solo valen %s" % (a, pasos, list(PASOS)))
            if not (x.get("why") or "").strip():
                self.errores.append("%s: sin 'why'; un nivel sin motivo no se puede discutir" % a)
        return decidido

    def tabla(self):
        maxi = int(self.techo.get("maxLevel") or 0)
        filas = []
        for x in sorted(self.cap.get("capabilities") or [], key=lambda y: (-int(y.get("level", 0)), y.get("action", ""))):
            nat = int(x.get("level", 0))
            filas.append({"action": x.get("action"), "domain": x.get("domain"),
                          "steps": x.get("steps"), "natural": nat,
                          "effective": min(nat, maxi), "capped": nat > maxi})
        return filas


ICONO = {True: "↓", False: " "}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--check", action="store_true", help="no escribe; falla si el informe está desactualizado")
    a = ap.parse_args()
    root = os.path.abspath(a.root)

    au = Autonomy(root)
    decidido = au.validar()
    filas = au.tabla()
    recortadas = [f for f in filas if f["capped"]]

    rep = {"project": os.path.basename(root), "generatedAt": None,
           "note": "Informe de scripts/ds-autonomy.py. No editar a mano.",
           "ceiling": au.techo,
           "summary": {"capabilities": len(filas), "aboveCeiling": len(recortadas), "errors": len(au.errores)},
           "effective": filas, "errors": au.errores}
    text = json.dumps(rep, ensure_ascii=False, indent=2) + "\n"

    techo = au.techo.get("maxLevel")
    print("Techo del proyecto: %s%s" % (techo, "" if decidido else "  ⬜ sin decidir — se aplica el valor por defecto"))
    print("%-44s %-8s %-6s %-9s %s" % ("capacidad", "dominio", "pasos", "natural", "efectivo"))
    for f in filas:
        print("  %s %-42s %-8s %-6s %-9s %s" % (ICONO[f["capped"]], f["action"], (f["domain"] or "")[:8],
                                                "".join(f["steps"] or []), f["natural"], f["effective"]))
    if recortadas:
        print("\n%d capacidades quedan por debajo de su nivel natural por el techo (marcadas ↓)." % len(recortadas))
    for e in au.errores:
        print("  ERROR  %s" % e)
    if not decidido:
        print("\nEl techo no lo ha decidido nadie todavía. Es el estado correcto al empezar: se")
        print("pregunta en el brief y se registra con quién y cuándo.")

    rc = 1 if au.errores else 0
    dest = os.path.join(root, "governance", "reports", "autonomy.json")
    if a.check:
        if not os.path.exists(dest) or open(dest, encoding="utf-8").read() != text:
            print("DESACTUALIZADO: governance/reports/autonomy.json")
            rc = 1
    else:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(text)
    return rc


if __name__ == "__main__":
    sys.exit(main())
