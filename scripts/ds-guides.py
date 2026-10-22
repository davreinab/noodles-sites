#!/usr/bin/env python3
"""ds-guides.py — reparte design-system/design.md en un router corto y guías por tema (migración de proyectos anteriores a la 12.20.0).

Hasta la 12.19.0 design.md traía dentro el protocolo de sync, la auditoría de Figma, la verificación, los overrides, los
borradores de accesibilidad y las reglas duras en Figma: unos 23 000 tokens que se cargaban en cada tarea. Ahora design.md
es solo el router y las reglas duras, y cada tema vive en design-system/guides/<tema>.md y se lee cuando la tarea lo pide.

Qué hace (idempotente; el texto de cada sección se mueve tal cual, también lo que el proyecto haya escrito dentro):
  1. si las guías solo de Figma estaban apartadas en guides/figma-guides.md (12.19.0, modo repo), las devuelve antes;
  2. mueve cada sección conocida a su guía y deja en su sitio una tabla «Guías» con cuándo leer cada una;
  3. reescribe las referencias «design.md § …» de AGENTS.md, fichas y propuestas a la guía nueva;
  4. cuenta cada sección y verifica que ninguna línea se ha perdido. Lo que no pudo enrutar lo dice.

Uso:  python3 scripts/ds-guides.py [--root .] [--check]     --check solo dice si hay algo que repartir (exit 1 si sí)
ds-sync.py lo ejecuta solo al arrancar y lo anuncia con «[MIGRACIÓN]». Sin dependencias: solo biblioteca estándar.
"""
import argparse
import importlib.util
import os
import re
import sys

NOTE = ("> Guía de `design-system/design.md`: se lee solo cuando la tarea lo pide "
        "(la tabla de «Enrutado» de `design.md` dice cuándo).\n\n")
# (título de la sección, prefijo de encabezado, archivo de la guía)
SECTIONS = [
    ("Sync desde Figma", "## ", "sync-figma.md"),
    ("Auditoría del DS en Figma", "## ", "auditoria-figma.md"),
    ("Verificación contra el maestro", "## ", "verificacion.md"),
    ("Overrides del DS", "## ", "overrides.md"),
    ("Borradores de accesibilidad", "## ", "accesibilidad.md"),
    ("Diseñar sin Figma", "## ", "sin-figma.md"),
    ("Reglas duras en Figma", "### ", "reglas-figma.md"),
]
GUIDE_FOR = {t: f for t, _, f in SECTIONS}
GUIAS = """## Guías (se leen solo cuando la tarea lo pide)

| Guía | Léela cuando |
|---|---|
| [`guides/sync-figma.md`](./guides/sync-figma.md) | sincronizas desde Figma, o creas o modificas un componente en Figma (protocolo de sync por MCP) |
| [`guides/reglas-figma.md`](./guides/reglas-figma.md) | vas a escribir variables o componentes en Figma |
| [`guides/auditoria-figma.md`](./guides/auditoria-figma.md) | auditas la calidad del DS en Figma |
| [`guides/verificacion.md`](./guides/verificacion.md) | vas a usar en una pantalla un componente que no está `verified` |
| [`guides/accesibilidad.md`](./guides/accesibilidad.md) | redactas accesibilidad o cambias un texto de una ficha |
| [`guides/overrides.md`](./guides/overrides.md) | pruebas en una pantalla un cambio del DS que aún no está aprobado |
| [`guides/sin-figma.md`](./guides/sin-figma.md) | el proyecto diseña sin Figma (modo repo) o saca el DS de los prototipos de `UI/` |

Con `sourceMode: repo` no se leen las guías de Figma. `python3 scripts/ds-budget.py` mide cuánto cuesta leer el proyecto.
"""
PTR_REGLAS = """### Reglas duras en Figma

Solo con Figma: qué debe cumplirse al escribir variables y componentes en el canvas está en
[`guides/reglas-figma.md`](./guides/reglas-figma.md), y el cómo en [`figma.md`](./figma.md). Se leen antes de
escribir nada en Figma, no para el resto del trabajo.
"""
ROUTER_FIXES = [
    ("sección **Sync desde Figma** abajo", "`guides/sync-figma.md`"),
    ("paso 3 de **Sync desde Figma**", "paso 3 de `guides/sync-figma.md`"),
    ("sección **Verificación contra el maestro** (abajo)", "`guides/verificacion.md`"),
    ("sección **Auditoría del DS en Figma** abajo", "`guides/auditoria-figma.md`"),
    ("(ver **Overrides del DS**)", "(ver `guides/overrides.md`)"),
    ("sección **Borradores de accesibilidad** abajo", "`guides/accesibilidad.md`"),
    ("la sección «Diseñar sin Figma» de este archivo", "`guides/sin-figma.md`"),
    ("router + reglas + protocolo de sync (se edita a mano)", "router + reglas duras (se edita a mano)"),
]
REF_FILES = ["AGENTS.md", "design-system/figma.md", "design-system/proposals/README.md",
             "design-system/docs/patterns.md", "design-system/docs/components.md"]


def read(p):
    try:
        with open(p, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


def write(p, t):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(t)


def find_section(text, title, prefix):
    """(inicio, fin) de la sección cuyo encabezado empieza por prefix+title; fin = siguiente encabezado igual o superior."""
    lines = text.split("\n")
    nivel = len(prefix.strip())
    for i, l in enumerate(lines):
        if l.startswith(prefix + title):
            end = len(lines)
            for j in range(i + 1, len(lines)):
                m = re.match(r"^(#{1,%d}) " % nivel, lines[j])
                if m:
                    end = j
                    break
            return i, end, lines
    return None


def remapear_allow_lines(root, orig_lines, avisos):
    """token-audit.config.json → allow.lines apunta a «archivo:línea». Al mover texto de design.md esas líneas cambian de
    sitio: se reapuntan por el contenido de la línea, sin reescribir el resto del archivo."""
    cpath = os.path.join(root, "scripts", "token-audit.config.json")
    cfg = read(cpath)
    if cfg is None:
        return
    nuevos = {}
    for m in re.finditer(r'"design-system/design\.md:(\d+)"', cfg):
        n = int(m.group(1))
        if not (1 <= n <= len(orig_lines)) or not orig_lines[n - 1].strip():
            continue
        texto = orig_lines[n - 1]
        destino = None
        for rel in ["design-system/design.md"] + ["design-system/guides/" + f for _, _, f in SECTIONS]:
            t = read(os.path.join(root, rel))
            if t is None:
                continue
            ls = t.split("\n")
            if texto in ls:
                destino = "%s:%d" % (rel, ls.index(texto) + 1)
                break
        if destino is None:
            avisos.append("la excepción de token-audit design.md:%d apunta a una línea que cambió de forma: revisa allow.lines" % n)
        elif destino != "design-system/design.md:%d" % n:
            nuevos[m.group(0)] = '"%s"' % destino
    if nuevos:
        for k, v in nuevos.items():
            cfg = cfg.replace(k, v)
        write(cpath, cfg)
        avisos.append("%d excepciones de token-audit (allow.lines) reapuntadas a su nueva ubicación" % len(nuevos))
    # si el proyecto sobrescribe la estructura permitida, la carpeta guides/ tiene que estar en ella
    try:
        import json as _json
        c = _json.loads(cfg)
        st = (c.get("structure") or {})
        if isinstance(st.get("design-system"), list) and "guides" not in st["design-system"]:
            st["design-system"].append("guides")
            st.setdefault("design-system/guides", ["*.md"])
            write(cpath, _json.dumps(c, ensure_ascii=False, indent=2) + "\n")
            avisos.append("guides/ añadida a la estructura permitida de token-audit.config.json")
    except ValueError:
        pass


def split(root, apply=True):
    ds = os.path.join(root, "design-system")
    dpath = os.path.join(ds, "design.md")
    text = read(dpath)
    if text is None:
        return {"movidas": [], "avisos": []}
    # 12.19.0: devolver las guías de Figma apartadas
    if os.path.isfile(os.path.join(ds, "guides", "figma-guides.md")) and apply:
        spec = importlib.util.spec_from_file_location("ds_source", os.path.join(os.path.dirname(os.path.abspath(__file__)), "ds-source.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.restaurar_figma(ds)
        text = read(dpath)
    orig_lines = text.split("\n")
    text = re.sub(r"<!-- solo-figma:(inicio|fin) -->\n?", "", text)
    movidas, avisos, antes = [], [], text
    guias = {}
    for title, prefix, fname in SECTIONS:
        r = find_section(text, title, prefix)
        if not r:
            continue
        i, j, lines = r
        body = lines[i:j]
        while body and not body[-1].strip():
            body.pop()
        if title == "Reglas duras en Figma" and len(body) < 12 and any("guides/reglas-figma.md" in l for l in body):
            continue  # ya es el puntero que dejó una ejecución anterior
        guias[fname] = (title, prefix, body)
        reemplazo = PTR_REGLAS.rstrip("\n").split("\n") + [""] if title == "Reglas duras en Figma" else []
        text = "\n".join(lines[:i] + reemplazo + lines[j:])
        movidas.append(title)
    if not movidas:
        return {"movidas": [], "avisos": []}
    if "## Guías (" not in text:
        k = text.find("## Estructura")
        text = (text[:k] + GUIAS + "\n" + text[k:]) if k >= 0 else text.rstrip("\n") + "\n\n" + GUIAS
    for old, new in ROUTER_FIXES:
        text = text.replace(old, new)
    text = re.sub(r"\n{3,}", "\n\n", text)
    if "├── guides/" not in text and "├── sync/" in text:
        text = re.sub(r"(├── sync/[^\n]*\n)", r"\1├── guides/              ← guías por tema que se leen solo cuando la tarea lo pide\n", text, count=1)
    for pat in ("sección **Sync desde Figma**", "sección **Verificación contra el maestro**", "sección **Auditoría del DS en Figma**",
                "sección **Overrides del DS**", "sección **Borradores de accesibilidad**"):
        if pat in text:
            avisos.append("design.md aún nombra «%s» como sección: revisa esa fila del router" % pat)
    if apply:
        for fname, (title, prefix, body) in guias.items():
            b = list(body)
            b[0] = "# " + b[0][len(prefix):]
            rest = "\n".join(b[1:]).strip("\n")
            if fname == "reglas-figma.md":
                rest = re.sub(r"^#### ", "## ", rest, flags=re.M)
            write(os.path.join(ds, "guides", fname), b[0] + "\n\n" + NOTE + rest + "\n")
        write(dpath, text.rstrip("\n") + "\n")
        mapa = {t: "guides/" + f for t, f in GUIDE_FOR.items()}
        for rel in REF_FILES:
            p = os.path.join(root, rel)
            s = read(p)
            if s is None:
                continue
            o = s
            for t, g in mapa.items():
                s = s.replace("`design-system/design.md § %s`" % t, "`design-system/%s`" % g).replace("design.md § %s" % t, g)
            if s != o:
                write(p, s)
        remapear_allow_lines(root, orig_lines, avisos)
        # verificación: ninguna línea con texto se pierde
        despues = text + "\n" + "\n".join("\n".join(b) for _, _, b in guias.values())
        perdidas = [l for l in antes.split("\n") if l.strip() and l not in despues and not l.startswith("<!-- solo-figma")]
        if perdidas:
            avisos.append("%d líneas de design.md cambiaron de forma al repartir (p. ej. filas del router reescritas): %s" % (len(perdidas), perdidas[0][:80]))
    return {"movidas": movidas, "avisos": avisos}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=None)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(a.root or os.path.dirname(here))
    r = split(root, apply=not a.check)
    if not r["movidas"]:
        print("ds-guides · design.md ya está repartido en guías: nada que hacer")
        return 0
    if a.check:
        print("ds-guides · design.md aún trae dentro %d secciones que son guías: %s" % (len(r["movidas"]), ", ".join(r["movidas"])))
        print("Repártelas con `python3 scripts/ds-guides.py` (ds-sync.py lo hace solo).")
        return 1
    print("[MIGRACIÓN] ds-guides · design.md pasa a ser un router; %d secciones se mueven tal cual a design-system/guides/: %s" % (len(r["movidas"]), ", ".join(r["movidas"])))
    for w in r["avisos"]:
        print("  [AVISO] " + w)
    return 0


if __name__ == "__main__":
    sys.exit(main())
