#!/usr/bin/env python3
"""
screen-report.py — informe de cierre de una pantalla o un flujo: qué piezas del DS usa y qué no es del DS.

Se ejecuta al terminar una pantalla, un flujo o una landing de `UI/`, y su salida es el informe que se entrega. Sale de los datos
(el HTML, los contratos, las propuestas y la auditoría), nunca de memoria: contar de memoria lo que usa una pantalla es irregular,
y lo que no es del DS es justo lo que se omite.

Por cada pantalla escribe:

  1. Componentes del DS: los que lleva con `data-ds="<slug>"` o con una clase propia del contrato (el mismo criterio que
     ds-fidelity → screen-uses-unverified), con su estado de verificación (verified, unverified o stale) y si llevan `data-ds` o
     solo se detectan por clase. La regla es que cada componente lleve su `data-ds` en el elemento raíz.
  2. Piezas internas de Figma usadas (según ds_common.interno_de): no deberían estar en una pantalla.
  3. Módulos nuevos señalizados: la marca que use el proyecto para «nuevo módulo» (scripts/screen-report.config.json →
     newModuleClasses; vacía por defecto).
  4. Overrides enlazados (UI/overrides/<id>.css|js) y el estado de su propuesta en proposals/, o «sin propuesta».
  5. Clases que no define components.css ni un override enlazado: huecos del DS o módulos sin señalizar.
  6. Errores y avisos de token-audit.py que caen en ese archivo.

Y al final, «Lo accionable»: el resumen de lo que hay que mirar (componentes sin verificar, sin data-ds, piezas internas, overrides
vivos, clases ajenas y errores de token-audit).

Uso:
    python3 scripts/screen-report.py UI/<pantalla>.html [más archivos o carpetas de UI/]
    python3 scripts/screen-report.py UI/                # todas las pantallas
    python3 scripts/screen-report.py UI/home.html --json
Sin dependencias externas: solo biblioteca estándar (Python 3.8+). Es un informe: el código de salida es 0 aunque haya cosas que
mirar; falla (2) solo si no recibe ninguna pantalla.
"""

import argparse
import glob
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ds_common as dcom  # noqa: E402

CONFIG_DEFECTO = {"newModuleClasses": []}


def read(p):
    try:
        with open(p, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def jload(p):
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def clases_definidas(css):
    css = re.sub(r"/\*.*?\*/", "", css or "", flags=re.S)
    return set(re.findall(r"\.(-?[_a-zA-Z][\w-]*)", css))


def contratos(root):
    out = []
    for p in sorted(glob.glob(os.path.join(root, "design-system", "schemas", "components", "*.schema.json"))):
        s = jload(p)
        if isinstance(s, dict) and s.get("meta"):
            out.append(s)
    return out


def estado(sch):
    v = (sch.get("meta") or {}).get("verification") or {}
    st = v.get("status") if isinstance(v, dict) else None
    return st if st in ("verified", "unverified", "stale") else "unverified"


def clases_propias(sch):
    """Las clases del propio contrato (su slug como bloque BEM), no las de los componentes que su ejemplo compone."""
    slug = sch["meta"].get("slug", "")
    code = sch.get("code") or (sch.get("source") or {}).get("code") or {}
    return [c for c in (code.get("classes") or []) if c and (c == slug or c.startswith(slug + "__") or c.startswith(slug + "--"))]


def archivos(root, args):
    out = []
    for a in args:
        p = a if os.path.isabs(a) else os.path.join(root, a)
        if os.path.isdir(p):
            out.extend(sorted(glob.glob(os.path.join(p, "**", "*.html"), recursive=True)))
        elif os.path.isfile(p):
            out.append(p)
        else:
            print("no existe: %s" % a, file=sys.stderr)
    return out


def estado_propuesta(root, ident):
    for p in glob.glob(os.path.join(root, "design-system", "proposals", "**", "%s.proposal.json" % ident), recursive=True):
        return (jload(p) or {}).get("status") or "inválida"
    return None


def overrides(root, html):
    res = []
    for ref in re.findall(r"""(?:href|src)\s*=\s*["']([^"']*overrides/[^"']+\.(?:css|js))["']""", html):
        ident = os.path.splitext(os.path.basename(ref))[0]
        res.append({"file": os.path.basename(ref), "ref": ref, "proposal": estado_propuesta(root, ident) or "sin propuesta"})
    return res


def css_enlazado(root, pagina, refs):
    css = ""
    for r in refs:
        if r.endswith(".css"):
            css += read(os.path.normpath(os.path.join(os.path.dirname(pagina), r.split("?")[0])))
    return css


def auditoria(root, rels):
    """Lo que token-audit encuentra en esos archivos. Si no se puede ejecutar, se dice: no es lo mismo que «cero errores»."""
    script = os.path.join(HERE, "token-audit.py")
    if not os.path.exists(script):
        return None
    try:
        out = subprocess.run([sys.executable, script, "--json", "--root", root], cwd=root, capture_output=True, text=True, timeout=300).stdout
        rep = json.loads(out)
    except (OSError, ValueError, subprocess.SubprocessError):
        return None
    por = {r: [] for r in rels}
    for x in rep.get("findings") or []:
        f = (x.get("file") or "").replace(os.sep, "/")
        if f in por:
            por[f].append(x)
    return por


def informe_de(root, f, rel, por_slug, por_clase, css_ds, cfg, audit, clases_slug):
    html = read(f)
    # lo que hay dentro de un <script> SÍ cuenta (12.26.0): el HTML que escribe el JavaScript es parte de la pantalla
    cuerpo = re.sub(r"<style\b.*?</style>", "", re.sub(r"<!--.*?-->", "", html, flags=re.S), flags=re.S | re.I)
    estilos = "".join(re.findall(r"<style\b[^>]*>(.*?)</style>", html, flags=re.S | re.I))
    an = dcom.analizar_pantalla(html, clases_slug)
    marcados, sin_marcar = an["marcados"], an["sin_marcar"]
    usadas = set()
    for e in dcom.elementos_de_pantalla(html):
        usadas.update(e["classes"])
    por_clases = {por_clase[c] for c in usadas if c in por_clase}
    comps = sorted(set(marcados) | por_clases | set(sin_marcar))
    detalle = []
    for s in comps:
        st, motivo = por_slug.get(s, ("no existe en el DS", None))
        detalle.append({"slug": s, "status": st, "dataDs": marcados.get(s, 0), "unmarked": sin_marcar.get(s, 0), "byClassOnly": s not in marcados})
    internos = [d["slug"] for d in detalle if d["status"] == "interno"]
    ovs = overrides(root_global[0], html)
    enlaces = [o["ref"] for o in ovs]
    definidas = css_ds | clases_definidas(css_enlazado(root_global[0], f, enlaces))
    en_pagina = clases_definidas(estilos)
    ajenas = sorted(c for c in usadas if c not in definidas)
    nuevos = {}
    for marca in cfg.get("newModuleClasses") or []:
        marca = marca.lstrip(".")
        nuevos[marca] = len(re.findall(r"""class\s*=\s*["'][^"']*(?<![\w-])%s(?![\w-])""" % re.escape(marca), cuerpo))
    hallazgos = (audit or {}).get(rel) if audit is not None else None
    return {"file": rel, "components": detalle, "mismatch": [{"dataDs": a, "tag": b, "classes": c} for a, b, c in an["no_coinciden"]], "internal": internos, "newModules": nuevos, "overrides": ovs,
            "foreignClasses": ajenas, "classesInPageStyle": sorted(c for c in ajenas if c in en_pagina),
            "tokenAudit": None if hallazgos is None else hallazgos}


root_global = [None]


def dscr(o):
    return o["file"] + (" (sin propuesta)" if o["proposal"] == "sin propuesta" else " (propuesta %s)" % o["proposal"])


def imprimir(rep, cfg):
    print("\n## %s\n" % rep["file"])
    comps = rep["components"]
    ok = [d for d in comps if d["status"] == "verified"]
    print("Componentes del DS: %d (%d verificados)" % (len(comps), len(ok)))
    for d in comps:
        if d["dataDs"]:
            marca = "data-ds ×%d" % d["dataDs"] + (" · %d elementos sin data-ds" % d["unmarked"] if d["unmarked"] else "")
        else:
            marca = "solo por clase, sin data-ds" + (" (%d elementos)" % d["unmarked"] if d["unmarked"] else "")
        print("  - %s · %s · %s" % (d["slug"], d["status"], marca))
    for m in rep.get("mismatch") or []:
        print("  ! data-ds=\"%s\" en <%s class=\"%s\">: ninguna clase del elemento es de ese contrato" % (m["dataDs"], m["tag"], m["classes"]))
    if rep["internal"]:
        print("Piezas internas de Figma (no deberían estar en una pantalla): " + ", ".join(rep["internal"]))
    marcas = cfg.get("newModuleClasses") or []
    if marcas:
        print("Módulos nuevos señalizados (%s): %s" % (", ".join("." + m.lstrip(".") for m in marcas),
                                                      ", ".join("%s ×%d" % (k, v) for k, v in rep["newModules"].items())))
    else:
        print("Módulos nuevos señalizados: marca no configurada (scripts/screen-report.config.json → newModuleClasses)")
    ovs = rep["overrides"]
    print("Overrides: " + (", ".join(dscr(o) for o in ovs) if ovs else "ninguno"))
    aj = rep["foreignClasses"]
    print("Clases que no define components.css: " + (", ".join(aj) if aj else "ninguna"))
    if rep["classesInPageStyle"]:
        print("  (definidas en un <style> de la propia página, que no debería haberlo: %s)" % ", ".join(rep["classesInPageStyle"]))
    ta = rep["tokenAudit"]
    if ta is None:
        print("token-audit en este archivo: no se ha podido ejecutar")
    else:
        err = [x for x in ta if x.get("severity") == "error"]
        print("token-audit en este archivo: %d errores, %d avisos" % (len(err), len(ta) - len(err)))
        for x in ta[:10]:
            print("  línea %s [%s] %s: %s" % (x.get("line"), (x.get("severity") or "").upper(), x.get("property"), x.get("value")))


def accionable(reps):
    print("\n## Lo accionable\n")
    sin_ver, sin_ds, internos, ovs_vivos, ajenas, errores, mal = {}, {}, {}, [], {}, 0, []
    for r in reps:
        for d in r["components"]:
            if d["status"] in ("unverified", "stale", "no existe en el DS"):
                sin_ver.setdefault(d["slug"], d["status"])
            if d.get("unmarked") and d["status"] != "interno":
                sin_ds.setdefault(r["file"], []).append((d["slug"], d["unmarked"]))
        for m in r.get("mismatch") or []:
            mal.append((r["file"], m))
        for s in r["internal"]:
            internos.setdefault(s, []).append(r["file"])
        for o in r["overrides"]:
            ovs_vivos.append((r["file"], o))
        for c in r["foreignClasses"]:
            ajenas.setdefault(c, set()).add(r["file"])
        errores += sum(1 for x in (r["tokenAudit"] or []) if x.get("severity") == "error")
    print("- Componentes sin verificar: " + (", ".join("%s (%s)" % (k, v) for k, v in sorted(sin_ver.items())) if sin_ver else "ninguno"))
    if sin_ds:
        print("- Elementos sin data-ds (añadirlo en el elemento raíz de cada componente):")
        for f, lista in sorted(sin_ds.items()):
            lista = sorted(lista, key=lambda x: (-x[1], x[0]))
            print("    %s: %d · %s" % (f, sum(n for _, n in lista), ", ".join("%s ×%d" % x for x in lista[:12]) + (" …" if len(lista) > 12 else "")))
    else:
        print("- Elementos sin data-ds: ninguno")
    if mal:
        print("- data-ds que no corresponden al elemento (cambia el slug por el del componente que es):")
        for f, m in mal[:12]:
            print("    %s: data-ds=\"%s\" en <%s class=\"%s\">" % (f, m["dataDs"], m["tag"], m["classes"]))
    else:
        print("- data-ds que no corresponden al elemento: ninguno")
    print("- Piezas internas de Figma: " + (", ".join(sorted(internos)) if internos else "ninguna"))
    print("- Overrides vivos: " + (", ".join("%s en %s" % (dscr(o), f) for f, o in ovs_vivos) if ovs_vivos else "ninguno"))
    print("- Clases ajenas al DS: " + (", ".join(sorted(ajenas)) if ajenas else "ninguna"))
    print("- Errores de token-audit en estas pantallas: %d" % errores)


def main(argv):
    ap = argparse.ArgumentParser(description="Informe de cierre de pantallas de UI/ (qué usa del DS y qué no).")
    ap.add_argument("rutas", nargs="*", help="archivos HTML o carpetas de UI/")
    ap.add_argument("--root", default=os.path.dirname(HERE), help="raíz del proyecto")
    ap.add_argument("--json", action="store_true", help="salida en JSON")
    a = ap.parse_args(argv)
    root = os.path.abspath(a.root)
    root_global[0] = root
    files = archivos(root, a.rutas)
    if not files:
        print("Uso: python3 scripts/screen-report.py UI/<pantalla>.html [más archivos o carpetas de UI/]", file=sys.stderr)
        return 2
    cfg = dict(CONFIG_DEFECTO)
    cfg.update(jload(os.path.join(HERE, "screen-report.config.json")) or {})
    cfg_ds = dcom.load_config(HERE)
    por_slug, por_clase = {}, {}
    for s in contratos(root):
        slug = s["meta"].get("slug", "")
        motivo = dcom.interno_de(s, cfg_ds)
        por_slug[slug] = ("interno", motivo) if motivo else (estado(s), None)
        for c in clases_propias(s):
            por_clase.setdefault(c, slug)
    clases_slug = {}
    for s in contratos(root):
        sl = s["meta"].get("slug", "")
        if sl and not dcom.interno_de(s, cfg_ds):
            clases_slug[sl] = set(dcom.clases_propias(s))
    css_ds = clases_definidas(read(os.path.join(root, "design-system", "css", "components.css")))
    rels = [os.path.relpath(f, root).replace(os.sep, "/") for f in files]
    audit = auditoria(root, rels)
    reps = [informe_de(root, f, rel, por_slug, por_clase, css_ds, cfg, audit, clases_slug) for f, rel in zip(files, rels)]
    if a.json:
        print(json.dumps(reps, ensure_ascii=False, indent=2))
        return 0
    for r in reps:
        imprimir(r, cfg)
    accionable(reps)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
