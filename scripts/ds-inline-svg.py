#!/usr/bin/env python3
"""Incrusta en css/components.css los SVG de assets/ que se usan como máscara (iconos, fideos).

Por qué: Chrome bloquea `mask: url(archivo.svg)` cuando la página se abre como file:// (origen
opaco), y los iconos desaparecen. Un data: URI funciona igual en file://, en un servidor y en
WordPress, y ahorra una petición por icono.

La fuente sigue siendo assets/: cada máscara se escribe como
    url("data:image/svg+xml,…") /* ../assets/icons/check.svg */
y este script la regenera desde ese archivo. También acepta la forma de autor
    url("../assets/icons/check.svg")
y la convierte. Es idempotente: ejecútalo tras cambiar cualquier SVG de assets/.

Uso: python3 scripts/ds-inline-svg.py [--check]
  --check  no escribe; sale con 1 si algún data: URI no coincide con su archivo.
"""
import os
import re
import sys
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS = os.path.join(ROOT, "design-system", "css", "components.css")
CSS_DIR = os.path.dirname(CSS)

INLINED = re.compile(r'url\("data:image/svg\+xml,[^"]*"\)\s*/\* (\.\./assets/[\w/.-]+\.svg) \*/')
AUTHORED = re.compile(r'url\("(\.\./assets/[\w/.-]+\.svg)"\)')


def data_uri(rel):
    svg = open(os.path.normpath(os.path.join(CSS_DIR, rel)), encoding="utf-8").read()
    svg = re.sub(r"<\?xml[^>]*>|<!--.*?-->", "", svg, flags=re.S)
    # En una máscara solo cuenta el alfa: cualquier color opaco vale; se normaliza a black.
    svg = re.sub(r'(fill|stroke)="(#[0-9a-fA-F]{3,8}|currentColor)"', r'\1="black"', svg)
    svg = re.sub(r"\s+", " ", svg).strip().replace('"', "'")
    return 'url("data:image/svg+xml,' + quote(svg, safe=" /=:;,'()-._") + '") /* ' + rel + " */"


def main():
    check = "--check" in sys.argv
    css = open(CSS, encoding="utf-8").read()
    out = INLINED.sub(lambda m: data_uri(m.group(1)), css)
    out = AUTHORED.sub(lambda m: data_uri(m.group(1)), out)
    n = len(INLINED.findall(out))
    if check:
        if out != css:
            print(f"ds-inline-svg: hay máscaras desactualizadas respecto a assets/ ({CSS})")
            sys.exit(1)
        print(f"ds-inline-svg: {n} máscaras al día")
        return
    if out != css:
        open(CSS, "w", encoding="utf-8").write(out)
    print(f"ds-inline-svg: {n} máscaras incrustadas desde assets/")


if __name__ == "__main__":
    main()
