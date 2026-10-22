#!/usr/bin/env python3
"""ds-extract.py — saca el sistema de diseño de los prototipos de UI/ (sin Figma) y comprueba que queda completo.

Los prototipos de diseño viven SOLO en UI/ (HTML + CSS). Cuando se pide generar el design system a partir de
ellos, este script hace el inventario y deja un BORRADOR en design-system/source/_borrador/ con el mismo
formato que la fuente (ver design-system/source/README.md). Nunca escribe la fuente real: la IA revisa el
borrador, lo propone, y solo con aprobación se promueve. Después `ds-sync.py` genera todo lo demás:
tokens, contratos (schemas), fichas .md con su documentación y la library.

Uso:  python3 scripts/ds-extract.py                # inventario → _borrador/ y reports/ui-extraction.json
      python3 scripts/ds-extract.py --promote      # borrador → source/ (no pisa lo que ya existe)
      python3 scripts/ds-extract.py --verify       # cada componente de UI/ tiene contrato, ficha y library
      python3 scripts/ds-extract.py --root <dir>
Qué detecta (heurístico, siempre se revisa):
  tokens      propiedades CSS `--nombre` de UI/**/*.css y <style>; `--a-b-c` → `a/b/c`; las que apuntan a otra
              (`var(--x)`) son semánticas; los bloques `[data-theme=dark]`/`.dark` dan el modo Dark.
  componentes los elementos con `data-ds="<slug>"` de UI/**/*.html (el marcador de la skill): cada uno es una muestra; las
              clases comunes a todas son la base, las que solo salen en algunas son modificadores (los que salen
              juntos en un elemento, de ejes distintos) y las de dentro, capas. Si los prototipos no llevan ningún
              `data-ds`, se usa la convención BEM con los separadores de scripts/ds-extract.config.json (por defecto
              `__` y `--`): la skill no asume cómo se llaman las clases de un proyecto.
  valores sueltos  colores/medidas escritos a mano en el CSS que ningún token cubre (se informan, no se inventan).
Qué es un componente y qué una sección de pantalla (la propuesta la hace el script, la decisión es de una persona):
  componente  cumple al menos una: se usa en 2 o más pantallas · tiene variantes (modificadores) · tiene estados
              (:hover, :focus, :disabled, aria-…) · es interactivo (button, a, input, select, textarea, details).
  sección     ninguna de las anteriores: vive solo en su pantalla y se queda en UI/. Va a `_borrador/secciones.json`
              con el motivo, no entra en el DS. Para forzar una sección a componente, se escribe su
              `source/components/<slug>.json` a mano. Después de publicar, convertirla es un cambio con propuesta.
Sin dependencias: solo biblioteca estándar.
"""
import argparse
import glob
import json
import os
import re
import sys
from collections import OrderedDict

CLASS_RE = re.compile(r'class\s*=\s*"([^"]*)"')
TAG_CLASS_RE = re.compile(r'<([a-zA-Z][a-zA-Z0-9]*)\b[^>]*?class\s*=\s*"([^"]*)"')
STYLE_RE = re.compile(r"<style[^>]*>(.*?)</style>", re.S | re.I)
BLOCK_RE = re.compile(r"([^{}]+)\{([^{}]*)\}")
VAR_RE = re.compile(r"(--[a-zA-Z0-9_-]+)\s*:\s*([^;]+)(?:;|$)")
HEX_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")
PX_RE = re.compile(r"^-?\d+(\.\d+)?(px)?$")
NAME_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
TEXT_TAGS = {"p", "span", "h1", "h2", "h3", "h4", "h5", "h6", "label", "a", "strong", "em", "small", "li"}
INTERACTIVE = {"button", "a", "input", "select", "textarea", "details", "summary"}
STATE_RE = r":(hover|focus|focus-visible|active|disabled|checked)|\[(disabled|aria-[a-z]+|data-state)"


def jread(p, d=None):
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return d


def jwrite(p, data):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def read(p):
    try:
        with open(p, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def ui_files(root, pattern):
    return sorted(glob.glob(os.path.join(root, "UI", "**", pattern), recursive=True))


def css_sources(root):
    """Todo el CSS de los prototipos: archivos .css de UI/ y <style> de sus HTML, y css/ del proyecto."""
    out = []
    for p in ui_files(root, "*.css") + sorted(glob.glob(os.path.join(root, "design-system", "css", "*.css"))):
        out.append((os.path.relpath(p, root), read(p)))
    for p in ui_files(root, "*.html"):
        for m in STYLE_RE.finditer(read(p)):
            out.append((os.path.relpath(p, root), m.group(1)))
    return out


def token_path(var):
    return var.lstrip("-").replace("_", "-").replace("-", "/")


def scan_tokens(root):
    base, dark, order = OrderedDict(), {}, []
    for rel, css in css_sources(root):
        css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
        for sel, body in BLOCK_RE.findall(css):
            sel = sel.strip()
            is_dark = bool(re.search(r"dark", sel, re.I))
            is_root = ":root" in sel or "html" in sel or is_dark or "[data-theme" in sel
            if not is_root:
                continue
            for var, val in VAR_RE.findall(body):
                (dark if is_dark else base)[var] = (val.strip(), rel)
                if var not in order:
                    order.append(var)
    return base, dark, order


def classify(value):
    v = value.strip()
    if v.startswith("var("):
        return "alias"
    if HEX_RE.fullmatch(v):
        return "color"
    if PX_RE.match(v):
        return "number"
    return None


def build_tokens(base, dark, order):
    prim, sem, skipped = OrderedDict(), OrderedDict(), []
    for var in order:
        val, rel = base.get(var) or dark.get(var)
        kind = classify(val)
        path = token_path(var)
        if kind is None:
            skipped.append({"var": var, "value": val, "file": rel, "why": "ni color, ni medida, ni alias: se queda en el CSS"})
            continue
        if kind == "alias":
            m = re.match(r"var\(\s*(--[a-zA-Z0-9_-]+)", val)
            ref = token_path(m.group(1)) if m else None
            entry = {"type": "color", "value": "{" + ref + "}"} if ref else None
            if entry is None:
                continue
            tgt = base.get(m.group(1), (None,))[0] or ""
            entry["type"] = classify(tgt) if classify(tgt) in ("color", "number") else "color"
            if var in dark:
                dm = re.match(r"var\(\s*(--[a-zA-Z0-9_-]+)", dark[var][0])
                entry["value"] = {"Light": entry["value"], "Dark": "{" + token_path(dm.group(1)) + "}" if dm else entry["value"]}
            sem[path] = entry
        else:
            if kind == "color":
                prim[path] = {"type": "color", "value": val}
            else:
                num = float(val.replace("px", ""))
                prim[path] = {"type": "number", "value": int(num) if num == int(num) else num}
    return prim, sem, skipped


CFG = {"elementSeparator": "__", "modifierSeparator": "--"}


def _dv():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import ds_variants as dv
    return dv


def _toks(e):
    return (e["attrs"].get("class") or "").split()


def scan_components(root):
    """Componentes de UI/**/*.html. Primero por el marcador de la skill, `data-ds="<slug>"`: cada elemento que lo lleva es
    una muestra del componente; las clases comunes a todas las muestras son su base, las que solo salen en algunas son
    modificadores y las de los elementos de dentro, sus capas. Sin ningún `data-ds` en los prototipos se usa la convención
    BEM con los separadores de scripts/ds-extract.config.json (por defecto `__` y `--`); la skill no asume cómo se llaman."""
    dv = _dv()
    files = [(os.path.relpath(p, root), dv.elementos(read(p))) for p in ui_files(root, "*.html")]
    if any(e["attrs"].get("data-ds") for _, els in files for e in els):
        return _scan_data_ds(files)
    return _scan_bem(files)


def _scan_data_ds(files):
    blocks = OrderedDict()
    for rel, els in files:
        for e in els:
            slug = e["attrs"].get("data-ds")
            if not slug:
                continue
            b = blocks.setdefault(slug, {"files": set(), "occ": [], "els": OrderedDict(), "tag": e["tag"], "via": "data-ds"})
            b["files"].add(rel)
            b["occ"].append(set(_toks(e)))
            for d in els:
                if d is not e and e["start"] < d["start"] < e["end"] and not d["attrs"].get("data-ds"):
                    for c in _toks(d):
                        b["els"].setdefault(c, d["tag"])
    for b in blocks.values():
        comun = set.intersection(*b["occ"]) if b["occ"] else set()
        b["base"] = sorted(comun)
        b["mod_sets"] = [o - comun for o in b["occ"]]
        b["mods"] = OrderedDict((m, 0) for o in b["occ"] for m in sorted(o - comun))
        b["classes"] = sorted(comun | set(b["mods"]) | set(b["els"]))
    return blocks


def _scan_bem(files):
    esep, msep = CFG["elementSeparator"], CFG["modifierSeparator"]
    blocks = OrderedDict()
    for rel, els in files:
        for e in els:
            por_bloque = {}
            for c in _toks(e):
                if not NAME_RE.match(c.replace(esep, "-").replace(msep, "-")):
                    continue
                blk = re.split(re.escape(esep) + "|" + re.escape(msep), c)[0]
                b = blocks.setdefault(blk, {"files": set(), "mods": OrderedDict(), "els": OrderedDict(), "tag": None,
                                            "mod_sets": [], "via": "bem", "classes": set()})
                b["files"].add(rel)
                b["classes"].add(c)
                if esep in c:
                    b["els"].setdefault(c.split(esep, 1)[1].split(msep)[0], e["tag"])
                elif msep in c:
                    m = c.split(msep, 1)[1]
                    b["mods"].setdefault(m, 0)
                    por_bloque.setdefault(blk, set()).add(m)
                else:
                    b["tag"] = b["tag"] or e["tag"]
            for blk, ms in por_bloque.items():
                blocks[blk]["mod_sets"].append(ms)
    out = OrderedDict()
    for k, v in blocks.items():
        if v["tag"] or v["els"] or v["mods"]:
            v["base"] = [k]
            v["classes"] = sorted(v["classes"])
            out[k] = v
    return out


def motivos(name, b, css_text):
    """Por qué un bloque es componente. Lista vacía: es una sección de pantalla."""
    m = []
    if len(b["files"]) >= 2:
        m.append("se usa en %d pantallas" % len(b["files"]))
    if b["mods"]:
        m.append("tiene variantes (%s)" % ", ".join(list(b["mods"])[:4]))
    css = re.sub(r"/\*.*?\*/", "", css_text or "", flags=re.S)
    pesan = set(b.get("classes") or []) | set(b.get("base") or [])
    for sel in re.findall(r"([^{}]+)\{", css):
        if re.search(STATE_RE, sel) and pesan & set(re.findall(r"\.([\w-]+)", sel)):
            m.append("tiene estados")
            break
    if (b["tag"] or "") in INTERACTIVE or any(t in INTERACTIVE for t in b["els"].values()):
        m.append("es interactivo")
    return m


def ejes(mods, mod_sets):
    """Agrupa los modificadores en ejes: dos que salen juntos en un mismo elemento son de ejes distintos."""
    axes = []
    for m in mods:
        for ax in axes:
            if not any(m in s and any(o in s for o in ax) for s in mod_sets):
                ax.append(m)
                break
        else:
            axes.append([m])
    return axes


def draft_component(name, b):
    mods = list(b["mods"])
    props = []
    for i, ax in enumerate(ejes(mods, b.get("mod_sets") or [])):
        props.append({"name": "variant" if i == 0 else "variant-%d" % (i + 1), "type": "enum",
                      "values": ["default"] + ax, "default": "default"})
    children = []
    for el, tag in b["els"].items():
        layer = {"layer": el}
        if tag in TEXT_TAGS:
            layer["type"] = "text"
        elif tag in ("svg", "i"):
            layer["type"] = "icon"
        elif tag == "img":
            layer["type"] = "image"
        children.append(layer)
    return {
        "name": name, "kind": "component", "group": "Sin clasificar",
        "description": "Detectado en UI/ (" + ", ".join(sorted(b["files"])[:3]) + "). Por escribir: qué es y cuándo se usa.",
        "props": props,
        "anatomy": {"layer": "root", "tag": b["tag"] or "div", "children": children},
        "_extraido": {"modificadores": mods, "archivos": sorted(b["files"]), "motivo": b.get("motivos") or [],
                      "detectadoPor": b.get("via")},
    }


def loose_values(root, token_values):
    sueltos = OrderedDict()
    for rel, css in css_sources(root):
        css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
        for sel, body in BLOCK_RE.findall(css):
            if ":root" in sel or "dark" in sel.lower():
                continue
            for h in set(HEX_RE.findall(body)):
                if h.lower() not in token_values:
                    sueltos.setdefault(h.lower(), []).append(rel)
    return [{"value": k, "files": sorted(set(v))[:3]} for k, v in sueltos.items()]


def split_components(root, todos):
    """Parte los bloques de UI/ en componentes (cumplen algún criterio) y secciones de pantalla."""
    css_text = "\n".join(c for _, c in css_sources(root))
    comps, secciones = OrderedDict(), OrderedDict()
    for n, b in todos.items():
        b["motivos"] = motivos(n, b, css_text)
        (comps if b["motivos"] else secciones)[n] = b
    return comps, secciones


def extract(root):
    base, dark, order = scan_tokens(root)
    prim, sem, skipped = build_tokens(base, dark, order)
    todos = scan_components(root)
    comps, secciones = split_components(root, todos)
    bd = os.path.join(root, "design-system", "source", "_borrador")
    tokens = {"collections": [
        {"name": "Primitive", "modes": ["Default"], "tokens": prim},
        {"name": "Semantic", "modes": ["Light", "Dark"], "tokens": sem},
        {"name": "Components", "modes": ["Default"], "tokens": {}},
    ]}
    jwrite(os.path.join(bd, "tokens.json"), tokens)
    for name, b in comps.items():
        jwrite(os.path.join(bd, "components", name + ".json"), draft_component(name, b))
    jwrite(os.path.join(bd, "secciones.json"), {"nota": "Bloques de UI/ que no cumplen ningún criterio de componente: se quedan en las pantallas. Para forzar uno, escribe su source/components/<slug>.json.",
        "secciones": {n: {"archivos": sorted(b["files"]), "motivo": "una sola pantalla, sin variantes, sin estados y no interactivo"} for n, b in secciones.items()}})
    known = {v["value"].lower() for v in prim.values() if v["type"] == "color"}
    rep = {
        "tokens": {"primitive": len(prim), "semantic": len(sem), "omitidos": skipped},
        "components": {n: {"modificadores": list(b["mods"]), "elementos": list(b["els"]), "archivos": sorted(b["files"]), "motivo": b["motivos"]} for n, b in comps.items()},
        "secciones": sorted(secciones),
        "valoresSueltos": loose_values(root, known),
        "notas": ["Es un borrador heurístico: nombre, grupo, descripción, tokens de la anatomía y semántica se completan con la IA y se proponen antes de promover."],
    }
    jwrite(os.path.join(root, "design-system", "reports", "ui-extraction.json"), rep)
    vias = {b.get("via") for b in comps.values()} | {b.get("via") for b in secciones.values()}
    if vias:
        print("  componentes detectados por " + ("el marcador data-ds de los prototipos" if "data-ds" in vias else
              "la convención BEM (separadores %s y %s de scripts/ds-extract.config.json): marca los componentes con data-ds para no depender de ella" % (CFG["elementSeparator"], CFG["modifierSeparator"])))
    print(f"ds-extract · {len(prim)} tokens primitivos, {len(sem)} semánticos, {len(comps)} componentes y {len(secciones)} secciones de pantalla en UI/ → design-system/source/_borrador/")
    if skipped:
        print(f"  {len(skipped)} propiedades CSS se quedan fuera (ni color, ni medida, ni alias); ver reports/ui-extraction.json")
    if rep["valoresSueltos"]:
        print(f"  {len(rep['valoresSueltos'])} colores escritos a mano que ningún token cubre; ver reports/ui-extraction.json")
    if not comps and not prim:
        print("  [AVISO] UI/ no tiene prototipos con clases ni variables CSS: nada que extraer.")
    print("Siguiente: revisa el borrador, propónlo, y con aprobación `python3 scripts/ds-extract.py --promote`.")
    return 0


def promote(root):
    bd = os.path.join(root, "design-system", "source", "_borrador")
    sd = os.path.join(root, "design-system", "source")
    dt = jread(os.path.join(bd, "tokens.json"))
    if dt is None and not os.path.isdir(os.path.join(bd, "components")):
        print("ds-extract · no hay borrador: ejecuta antes `python3 scripts/ds-extract.py`.")
        return 1
    added = kept = 0
    st_path = os.path.join(sd, "tokens.json")
    st = jread(st_path, {"collections": []})
    cols = {c["name"]: c for c in st["collections"]}
    for c in (dt or {}).get("collections", []):
        tgt = cols.get(c["name"])
        if tgt is None:
            st["collections"].append(c)
            added += len(c["tokens"])
            continue
        for k, v in c["tokens"].items():
            if k in tgt["tokens"]:
                kept += 1
            else:
                tgt["tokens"][k] = v
                added += 1
    jwrite(st_path, st)
    comps = 0
    for p in sorted(glob.glob(os.path.join(bd, "components", "*.json"))):
        dest = os.path.join(sd, "components", os.path.basename(p))
        if os.path.exists(dest):
            kept += 1
            continue
        d = jread(p)
        d.pop("_extraido", None)
        jwrite(dest, d)
        comps += 1
    print(f"ds-extract · promovido a source/: {added} tokens, {comps} componentes; {kept} ya existían y no se tocan.")
    print("Siguiente: `python3 scripts/ds-source.py --check` y `python3 scripts/ds-sync.py`.")
    return 0


def verify(root):
    comps, _ = split_components(root, scan_components(root))
    for p in glob.glob(os.path.join(root, "design-system", "source", "components", "*.json")):
        n = os.path.basename(p)[:-5]
        comps.setdefault(n, {})
    ds = os.path.join(root, "design-system")
    miss, ok = [], 0
    lib = []
    for p in glob.glob(os.path.join(root, "library", "src", "patterns", "**", "*"), recursive=True):
        lib.append(os.path.basename(p).rsplit(".", 1)[0])
    for name in comps:
        falta = []
        if not os.path.exists(os.path.join(ds, "schemas", "components", name + ".schema.json")):
            falta.append("contrato (schemas/components/%s.schema.json)" % name)
        if not (os.path.exists(os.path.join(ds, "docs", "components", name + ".md")) or os.path.exists(os.path.join(ds, "docs", "patterns", name + ".md"))):
            falta.append("ficha .md en docs/")
        if name not in lib and not any(name in x for x in lib):
            falta.append("entrada en la library")
        if falta:
            miss.append((name, falta))
        else:
            ok += 1
    for n, f in miss:
        print(f"  [ERROR] {n}: falta " + "; ".join(f))
    print(f"ds-extract · verificación: {ok} de {len(comps)} componentes de UI/ completos (contrato + ficha + library)")
    if miss:
        print("Corrige: añádelos a design-system/source/components/ y ejecuta `python3 scripts/ds-sync.py`.")
    return 1 if miss else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    ap.add_argument("--promote", action="store_true")
    ap.add_argument("--verify", action="store_true")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    cfg = jread(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ds-extract.config.json"), {}) or {}
    for k in ("elementSeparator", "modifierSeparator"):
        if isinstance(cfg.get(k), str) and cfg[k]:
            CFG[k] = cfg[k]
    sys.exit(promote(root) if a.promote else verify(root) if a.verify else extract(root))


if __name__ == "__main__":
    main()
