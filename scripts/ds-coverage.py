#!/usr/bin/env python3
"""
ds-coverage.py — mide cuánto del producto usa de verdad el design system.

Pregunta que responde: de todos los elementos con clase de las pantallas, ¿cuántos usan una
clase que el DS define en css/components.css, y cuántos se la han inventado por su cuenta?

  cobertura = elementos con al menos una clase del DS ÷ elementos con alguna clase

Los elementos sin ninguna clase no cuentan en ninguno de los dos lados: un contenedor suelto
no es adopción ni es deriva. Las clases ajenas se listan una a una, que es lo accionable.

Salida: design-system/reports/coverage.json + resumen por consola.

Uso:  python3 scripts/ds-coverage.py [--root .] [--check] [--min N]
      --check  no escribe; falla si el informe en disco está desactualizado
      --min N  falla si la cobertura global baja del N por ciento
Sin dependencias externas: solo biblioteca estándar.
"""

import argparse
import json
import os
import re
import sys
from html.parser import HTMLParser


def ds_classes(css_path):
    """Clases que el DS define, leídas de los selectores de components.css."""
    if not os.path.exists(css_path):
        return set()
    css = open(css_path, encoding="utf-8", errors="ignore").read()
    css = re.sub(r"/\*.*?\*/", " ", css, flags=re.S)
    prev = None
    while prev != css:                      # deja solo selectores: vacía los bloques de dentro afuera
        prev = css
        css = re.sub(r"\{[^{}]*\}", " ", css)
    return set(re.findall(r"\.(-?[_a-zA-Z][\w-]*)", css))


class Counter(HTMLParser):
    def __init__(self, ds):
        super().__init__(convert_charrefs=True)
        self.ds, self.con_clase, self.cubiertos = ds, 0, 0
        self.ajenas = {}

    def handle_starttag(self, tag, attrs):
        clases = [c for c in (dict(attrs).get("class") or "").split() if c]
        if not clases:
            return
        self.con_clase += 1
        propias = [c for c in clases if c in self.ds]
        if propias:
            self.cubiertos += 1
        for c in clases:
            if c not in self.ds:
                self.ajenas[c] = self.ajenas.get(c, 0) + 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--min", type=float, default=None, help="cobertura global mínima, en porcentaje")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    ds = os.path.join(root, "design-system")

    clases = ds_classes(os.path.join(ds, "css", "components.css"))
    pantallas = []
    ui = os.path.join(root, "UI")
    for dirpath, _, files in os.walk(ui):
        for f in sorted(files):
            if f.endswith(".html"):
                pantallas.append(os.path.join(dirpath, f))

    por_pantalla, tot_c, tot_k, ajenas_globales = [], 0, 0, {}
    for p in pantallas:
        c = Counter(clases)
        c.feed(open(p, encoding="utf-8", errors="ignore").read())
        pct = round(100 * c.cubiertos / c.con_clase, 1) if c.con_clase else None
        por_pantalla.append({"file": os.path.relpath(p, root), "withClass": c.con_clase,
                             "covered": c.cubiertos, "coverage": pct,
                             "foreignClasses": dict(sorted(c.ajenas.items(), key=lambda x: -x[1]))})
        tot_c += c.cubiertos
        tot_k += c.con_clase
        for k, v in c.ajenas.items():
            ajenas_globales[k] = ajenas_globales.get(k, 0) + v

    global_pct = round(100 * tot_c / tot_k, 1) if tot_k else None
    rep = {"designSystem": os.path.basename(root),
           "note": "Informe de scripts/ds-coverage.py. No editar a mano.",
           "definition": "cobertura = elementos con al menos una clase de components.css ÷ elementos con alguna clase",
           "dsClasses": len(clases), "screens": len(pantallas),
           "summary": {"withClass": tot_k, "covered": tot_c, "coverage": global_pct},
           "byScreen": por_pantalla,
           "foreignClasses": dict(sorted(ajenas_globales.items(), key=lambda x: -x[1]))}

    if not pantallas:
        print("Sin pantallas en UI/ todavía: no hay nada que medir.")
    else:
        print("Clases que define el DS: %d · pantallas: %d" % (len(clases), len(pantallas)))
        for s in por_pantalla:
            print("  %-40s %5s%%  (%d de %d)" % (s["file"], s["coverage"] if s["coverage"] is not None else "—",
                                                 s["covered"], s["withClass"]))
        print("\nCobertura global: %s%%" % (global_pct if global_pct is not None else "—"))
        if ajenas_globales:
            top = list(sorted(ajenas_globales.items(), key=lambda x: -x[1]))[:8]
            print("Clases ajenas al DS (%d distintas): %s" % (len(ajenas_globales),
                                                              ", ".join("%s×%d" % t for t in top)))
            print("Cada una es o un componente que falta en el DS, o un estilo local que no debería existir.")

    text = json.dumps(rep, ensure_ascii=False, indent=2) + "\n"
    dest = os.path.join(ds, "reports", "coverage.json")
    rc = 0
    if a.check:
        if not os.path.exists(dest) or open(dest, encoding="utf-8").read() != text:
            print("DESACTUALIZADO: design-system/reports/coverage.json")
            rc = 1
    else:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(text)
    if a.min is not None and (global_pct is None or global_pct < a.min):
        print("COBERTURA INSUFICIENTE: %s%% < %s%%" % (global_pct, a.min))
        rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
