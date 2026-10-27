#!/usr/bin/env python3
"""ds-library — escribe el catálogo navegable del design system (library/src/patterns/) desde el repo.

El visor (library/, fork del Pattern Library de la empresa: Eleventy 3 + Nunjucks) espera un patrón por
carpeta: <nivel>/<grupo>/<slug>/<slug>.njk (plantilla), .json (título, descripción, estado, variantes)
y desde la 12.6.0 la ficha va dentro del .json («sheet»: datos del contrato, criterio manual de la ficha y
propuesta de textos pendiente), que el visor pinta como tablero. Este script los genera, siempre igual, a partir de:
    design-system/schemas/components/<slug>.schema.json   contrato 12.0.0 (api · code · figma · docs)
    design-system/docs/components|patterns/<slug>.md       la ficha (bloque generado + criterio a mano)
    design-system/agent-manifest.json                      nombre del DS
    design-system/proposals/*.proposal.json                propuestas pendientes de textos (kind component-text)
Nada se escribe a mano en library/src/patterns/: se regenera en cada sync (ds-sync.py lo llama al cerrar).
El CSS del DS no se copia: library/src/patterns/_base/base.css lo importa entero.

Mapa (decisiones del 2026-10-19): componente → atoms · patrón → organisms · página de Figma → grupo (si la
página se llama «Página / Sección», el grupo es «Página»). Dos grupos especiales (12.2.0):
    «Pendientes de construir»            los contratos sin «Ejemplo de código», por página, al final del menú
    «Internos de Figma · no se construyen»  piezas de trabajo de Figma: nombre que empieza por «.», contiene
                                         «deprecated», página «Documentation», o listadas en
                                         scripts/ds-library.config.json → internal.names · internal.namePatterns
Estado: verified → Ready · stale → In review · unverified → Draft · retirado (lifecycle) → Deprecated.

Imágenes de los ejemplos: cada src="…" se resuelve contra design-system/assets/. Un asset del DS
(../assets/…, assets/…, ../design-system/assets/…) pasa a /assets/ds/…; un icono que no existe es ERROR
(el catálogo no lo sustituye nunca); una foto que no es del DS se cambia por el placeholder
design-system/assets/images/placeholder.svg y se avisa. Con algún ERROR el script devuelve 1 (también
con --check), y el hook y la CI lo paran.

Sin dependencias (solo stdlib, Python 3.8+). Uso:
    python3 scripts/ds-library.py            # regenera library/src/patterns/ y _data/site.json
    python3 scripts/ds-library.py --check    # no escribe: exit 1 si algo está desfasado o hay un icono que no existe
    python3 scripts/ds-library.py --root .
Para ver el catálogo: cd library && npm install && npm start (Node.js solo para verlo).
"""
import argparse
import glob
import json
import os
import re
import sys

LEVEL = {"component": "atoms", "pattern": "organisms"}
SUBGRUPO_MIN = 8  # piezas de una página a partir de las cuales se reparte por sección
STATUS = {"verified": "Ready", "stale": "In review", "unverified": "Draft"}
SPECIAL = {
    "pendientes": {"slug": "pendientes", "title": "Pendientes de construir", "order": 800},
    "partes": {"slug": "partes-de-otro-componente", "title": "Partes de otro componente · las cubre el ejemplo de su padre", "order": 850},
    "internos": {"slug": "internos-de-figma", "title": "Internos de Figma · no se construyen", "order": 900},
}
PLACEHOLDER = "images/placeholder.svg"
SRC_RE = re.compile(r'(\bsrc=")([^"]+)(")')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ds_common as dcom  # una sola definición de «interno» para toda la skill

try:  # cobertura de variantes y galería (módulo compartido con ds-fidelity)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import ds_variants as dv
except ImportError:  # el proyecto no lo trae: la ficha sale sin esa parte
    dv = None
DS_ASSET_RE = re.compile(r"^(?:\./)?(?:\.\./)*(?:design-system/)?assets/(.+)$")


def slug(name):
    s = re.sub(r"[^\w\s/-]", "", name or "", flags=re.U).strip().lower()
    s = re.sub(r"\s*/\s*", "-", s)
    s = re.sub(r"[\s_]+", "-", s)
    return re.sub(r"-{2,}", "-", s).strip("-") or "sin-pagina"


def read(path, default=None):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except Exception:
        return default


def jload(path, default=None):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return default


def modulo_activo(root, mid):
    try:
        m = (jload(os.path.join(root, "governance", "modules.json"), {}).get("modules") or {}).get(mid) or {}
        return m.get("active") is not False
    except Exception:
        return True


def load_config(here):
    return dcom.load_config(here)


def pagina(meta, cfg=None):
    return dcom.pagina(meta, cfg)


def es_interno(meta, cfg):
    """Pieza de trabajo de Figma que nunca se construye: no se mezcla con los componentes utilizables.
    La definición vive en ds_common.py y es la misma para todos los scripts."""
    return dcom.es_interno(meta, cfg)


def ficha_to_md(text):
    """La ficha, sin el heading ni las marcas de bloque generado, como documentación del patrón."""
    if not text:
        return ""
    lines = [l for l in text.splitlines() if not l.startswith("### ") and "⚙️ GENERATED:" not in l]
    out = "\n".join(lines).strip("\n")
    return out + "\n" if out else ""


VERIF_LABEL = {"verified": "Verificado", "unverified": "Sin verificar", "stale": "Caducado"}
ITEM_RE = re.compile(r"^- \*\*(.+?):\*\*\s?(.*)$")
SKIP_MANUAL = {"Ejemplo de código"}  # el ejemplo ya se ve arriba, en la vista previa y en la pestaña HTML
NO_APLICA_RE = re.compile(r"^\s*no aplica\b", re.I)  # «No aplica.» / «No aplica: es decorativo» → campo resuelto


def admite_no_aplica(label):
    """Solo el campo de accesibilidad: un componente decorativo no tiene rol, nombre ni teclado. El propósito
    o cuándo usarlo siempre aplican."""
    return label.lower().startswith("accesibilidad")


def seccion_ficha(text, node_id):
    """La sección de la ficha de este componente (una ficha puede guardar varias con slug compartido)."""
    trozos = [t for t in re.split(r"(?m)^(?=### )", text or "") if t.startswith("### ")]
    for t in trozos:
        if node_id and f"`{node_id}`" in t:
            return t
    return trozos[0] if trozos else (text or "")


def campos_manuales(section):
    """Lo que el equipo escribe a mano debajo del bloque generado: [{label, md, todo}] y notas sueltas."""
    manual = section.split("⚙️ GENERATED:end:", 1)[1].split("-->", 1)[1] if "⚙️ GENERATED:end:" in section else ""
    campos, notas, actual = [], [], None
    for line in manual.splitlines():
        m = ITEM_RE.match(line)
        if m:
            actual = {"label": m.group(1).strip(), "lines": [m.group(2)]}
            campos.append(actual)
        elif actual is not None and (line.startswith("  ") or not line.strip()):
            actual["lines"].append(line[2:] if line.startswith("  ") else "")
        else:
            actual = None
            notas.append(line)
    out = []
    for c in campos:
        if c["label"] in SKIP_MANUAL:
            continue
        md = "\n".join(c["lines"]).strip()
        out.append({"label": c["label"], "md": md, "todo": (not md) or md.startswith("⬜"),
                    "na": bool(NO_APLICA_RE.match(md)), "canNA": admite_no_aplica(c["label"])})
    return out, "\n".join(notas).strip()


def fecha(ts):
    m = re.match(r"(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2})", ts or "")
    return f"{m.group(1)} · {m.group(2)} UTC" if m else (ts or "")


PROPUESTA_ESTADO = {"draft": "Pendiente de aprobación", "approved": "Aprobada, pendiente de aplicar"}


def propuestas_texto(ds):
    """Propuestas pendientes de cambio de textos (las crea el visor), por componente. Solo las sueltas en la
    raíz de proposals/: las aplicadas y rechazadas viven en subcarpetas y ya no cuentan."""
    out = {}
    for path in sorted(glob.glob(os.path.join(ds, "proposals", "*.proposal.json"))):
        p = jload(path)
        pc = (p or {}).get("proposedChange") or {}
        if not isinstance(p, dict) or pc.get("kind") != "component-text" or p.get("status") not in PROPUESTA_ESTADO:
            continue
        out[pc.get("component")] = {"file": "design-system/proposals/" + os.path.basename(path), "proposal": p}
    return out


def parrafos(texto):
    texto = (texto or "").strip()
    return [re.sub(r"\s+", " ", x).strip() for x in re.split(r"\n\s*\n", texto)] if texto and texto != "unknown" else []


def contraste(s, ctx):
    """Parejas texto/fondo medidas desde el CSS (scripts/ds_contrast.py), para la tarjeta «Contraste AA»."""
    if not ctx or not ((s.get("code") or {}).get("classes")):
        return None
    dc, rules, themes = ctx
    r = dc.component_pairs(s["meta"]["slug"], rules, themes)
    fallos = [x for x in r["pairs"] if not x["pass"]]
    usa = [u for u in ((s.get("relations") or {}).get("uses") or []) if u]
    # los fondos sobre los que cumple AA, para los textos sin fondo propio (varios estados repiten los mismos: una vez por color de texto)
    recom, vistos = [], set()
    for u in r["untestable"]:
        rc = u.get("recommend")
        if rc and (u["theme"], tuple(rc["ok"]), tuple(rc["fail"])) not in vistos:
            vistos.add((u["theme"], tuple(rc["ok"]), tuple(rc["fail"])))
            recom.append({"theme": u["theme"], "state": u["state"], "need": rc["need"], "ok": rc["ok"][:6], "fail": rc["fail"][:6]})
    sin_pares = ("Sin colores propios: sus textos son los de las piezas que usa (" + ", ".join(usa[:6]) + ")") if (r.get("sin_colores_propios") and usa and not r["untestable"]) \
        else "Sin parejas medibles"
    return {"pairs": r["pairs"], "fail": len(fallos), "untestable": r["untestable"], "exempt": r["exempt"], "recommend": recom[:6],
            "label": (sin_pares if not r["pairs"] else
                      "Cumple AA" if not fallos else f"{len(fallos)} por debajo de AA")}


def hoja(s, ficha_text, pendiente=None, ctx=None):
    """Datos de la ficha para el tablero del visor: contrato (estructurado) + criterio manual de la ficha."""
    meta, api, fg, code = s["meta"], s.get("api") or {}, s.get("figma") or {}, s.get("code") or {}
    node = fg.get("nodeId")
    url = f"https://www.figma.com/design/{fg['fileKey']}/?node-id={node.replace(':', '-')}" if fg.get("fileKey") and node else None
    ver = (meta.get("verification") or {}).get("status") or "unverified"
    desc = (meta.get("description") or "").strip()
    paras = parrafos(desc)
    props = []
    for p in api.get("props") or []:
        d = p.get("default")
        props.append({"name": p.get("name"), "type": p.get("type"), "values": p.get("values") or [],
                      "default": "" if d is None else (str(d).lower() if isinstance(d, bool) else str(d)),
                      "figma": p.get("figma") if p.get("figma") not in (None, p.get("name")) else ""})
    tokens = {}
    for t in api.get("tokens") or []:
        tokens.setdefault(t.split("/")[0], []).append(t)
    icons = api.get("icons") or {}
    nested = [{"layer": n.get("layer"), "component": n.get("componentSlug") or n.get("component"),
               "exposedAs": n.get("exposedAs") or "", "hidden": n.get("visibleByDefault") is False}
              for n in fg.get("nestedInstances") or []]
    manual, notas = campos_manuales(seccion_ficha(ficha_text, node))
    pend = None
    if pendiente:
        p = pendiente["proposal"]
        cambios = {c.get("field"): c for c in (p.get("proposedChange") or {}).get("changes") or []}
        pend = {"id": p.get("id"), "file": pendiente["file"], "status": p.get("status"),
                "statusLabel": PROPUESTA_ESTADO.get(p.get("status"), p.get("status")),
                "approver": p.get("requiredApprover") or "",
                "description": parrafos(cambios["description"]["proposed"]) if "description" in cambios else None,
                "descriptionByAI": cambios.get("description", {}).get("origin") == "ai"}
    else:
        cambios = {}
    for f in manual:
        if f["label"] in cambios:
            f["proposed"] = cambios[f["label"]].get("proposed") or ""
            f["proposedNA"] = bool(NO_APLICA_RE.match(f["proposed"]))
            f["proposedByAI"] = cambios[f["label"]].get("origin") == "ai"
    current = {"description": desc if desc != "unknown" else ""}
    current.update({f["label"]: ("" if f["todo"] else f["md"]) for f in manual})
    edit = {"slug": meta.get("slug"), "name": meta.get("name"), "fileKey": fg.get("fileKey"), "nodeId": node,
            "current": current,
            "proposed": {k: v.get("proposed") or "" for k, v in cambios.items() if k in current},
            "pending": pendiente["proposal"] if pendiente else None}
    return {
        "contrast": contraste(s, ctx),
        "pending": pend,
        "edit": edit,
        "figma": {"fromRepo": fg.get("fileKey") == "repo", "nodeId": node, "url": url, "page": meta.get("figmaPage") or "", "type": meta.get("figmaType") or "",
                  "variants": meta.get("variantCount"), "lastSync": fecha(meta.get("lastSync")),
                  "verification": ver, "verificationLabel": VERIF_LABEL.get(ver, ver)},
        "description": paras,
        "props": props,
        "cssStates": api.get("cssStates") or [], "events": api.get("events") or [], "slots": api.get("slots") or [],
        "icons": {"swap": icons.get("swapProperties") or [], "defaults": icons.get("defaultIcons") or []},
        "nested": nested,
        "tokens": [{"group": g, "items": v} for g, v in sorted(tokens.items())],
        "tokenCount": len(api.get("tokens") or []),
        "textStyles": fg.get("textStyles") or [],
        "classes": code.get("classes") or [],
        "manual": manual,
        "manualTodo": sum(1 for c in manual if c["todo"] and not c["na"] and "proposed" not in c),
        "notes": notas,
    }


def resolve_src(src, assets_dir, slug_, problemas):
    """Un src del ejemplo → ruta que el visor sirve. Iconos: existen o ERROR. Fotos: del DS o placeholder."""
    if src.startswith(("http:", "https:", "data:", "#", "/assets/ds/")) or "{{" in src:
        return src
    m = DS_ASSET_RE.match(src)
    rel = m.group(1) if m else None
    if rel and os.path.isfile(os.path.join(assets_dir, rel)):
        return "/assets/ds/" + rel
    if (rel or src).startswith("icons/") or "/icons/" in src:
        problemas.append(("ERROR", slug_, f"icono que no existe en design-system/assets/: {src}"))
        return src
    problemas.append(("AVISO", slug_, f"imagen fuera del design system ({src}): se muestra el placeholder; "
                                      f"en la ficha usa ../assets/{PLACEHOLDER}"))
    return "/assets/ds/" + PLACEHOLDER


def _prepara(html, slug_, assets_dir, problemas):
    html = html.rstrip("\n")
    if assets_dir is not None:
        html = SRC_RE.sub(lambda m: m.group(1) + resolve_src(m.group(2), assets_dir, slug_, problemas if problemas is not None else []) + m.group(3), html)
    return html.replace("../design-system/assets/", "/assets/ds/").replace("../assets/", "/assets/ds/")


def example_to_njk(example, slug_, assets_dir=None, problemas=None, galeria=None):
    """La plantilla del patrón. Con `galeria` (html, o texto plano si no se pudo pintar), la misma plantilla sirve
    la variante «Todas las variantes» cuando los datos traen view: todas; el visor usa la misma macro para todas."""
    if example and example.strip():
        body = "{% raw %}" + _prepara(example, slug_, assets_dir, problemas) + "{% endraw %}"
    else:
        body = ('<p class="ds-missing" style="font:14px/1.5 system-ui;color:#8a1f1f">Sin «Ejemplo de código» todavía: '
                'se escribe en la ficha del componente (docs § Ejemplo de código) y se regenera.</p>')
    if galeria:
        kind, contenido = galeria
        if kind == "html":
            g = "{% raw %}" + _prepara(contenido, slug_, assets_dir, problemas) + "{% endraw %}"
        else:
            esc = contenido.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            g = '<p class="ds-gallery__note" style="font:14px/1.5 system-ui;color:#1f1f1f;max-width:70ch">' + esc + "</p>"
        body = '{% if data.view == "todas" %}\n' + g + "\n{% else %}\n" + body + "\n{% endif %}"
    return "{% macro render(data) %}\n" + body + "\n{% endmacro %}\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=None)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    return generate(os.path.abspath(a.root or os.path.dirname(here)), check=a.check)


def generate(root, check=False):
    """Escribe (o comprueba) el catálogo. Lo llama main() y también ds-sync.py al cierre de cada sync."""
    here = os.path.dirname(os.path.abspath(__file__))
    cfg = load_config(here)
    ds = os.path.join(root, "design-system")
    lib = os.path.join(root, "library")
    if not modulo_activo(root, "design-system"):
        print("El módulo de design system no está activo: no hay catálogo que generar.")
        return 0
    if not os.path.isdir(lib):
        print("sin carpeta library/ (el visor no está instalado en este proyecto): nada que generar")
        return 0
    man = jload(os.path.join(ds, "agent-manifest.json"), {}) or {}
    nombre = man.get("designSystem") or os.path.basename(root)
    lc = jload(os.path.join(ds, "schemas", "governance", "lifecycle.json"), {}) or {}
    retirados = {e.get("id", "").lstrip(".") for e in (lc.get("deprecations") or []) if e.get("id")}
    assets_dir = os.path.join(ds, "assets")
    # Cobertura de variantes: el CSS del DS y la config de ds-fidelity (modificadores, estados que se ignoran).
    css_cls = dv.css_classes(read(os.path.join(ds, "css", "components.css"), "") or "") if dv else set()
    fid_cfg = jload(os.path.join(here, "ds-fidelity.config.json"), {}) or {}

    esperado = {}  # ruta relativa a library/ → contenido
    esperado["src/_data/site.json"] = json.dumps({"name": f"{nombre} · Design system"}, ensure_ascii=False, indent=2) + "\n"
    grupos = {}  # (level, group) → {"title", "order"?}
    problemas = []
    schemas = [s for s in (jload(p) for p in sorted(glob.glob(os.path.join(ds, "schemas", "components", "*.schema.json"))))
               if isinstance(s, dict) and s.get("meta")]
    pendientes, internos, partes_n = 0, 0, 0
    padres = dcom.partes_de(schemas, cfg)
    textos_pendientes = propuestas_texto(ds)
    try:
        sys.path.insert(0, here)
        import ds_contrast as dc
        ctx = (dc, dc.css_rules(read(os.path.join(ds, "css", "components.css"), "") or ""),
               dc.theme_vars(read(os.path.join(ds, "tokens", "tokens.css"), "") or ""))
    except ImportError:
        ctx = None
    # Subgrupos (12.22.3): una página de Figma con muchas piezas y varias secciones («Página / Sección») se reparte por sección.
    # Si es la única página de su nivel, las secciones suben al menú de primer nivel: no hace falta abrir la página para verlas.
    cuenta = {}
    for s in schemas:
        m = s["meta"]
        if dcom.interno_de(s, cfg) is None and ((s.get("code") or (s.get("source") or {}).get("code") or {}).get("example") or "").strip():
            k = (LEVEL.get(m.get("kind", "component"), "atoms"), pagina(m, cfg))
            cuenta.setdefault(k, []).append(dcom.seccion(m, cfg))
    paginas_nivel = {}
    for (lv, pg) in cuenta:
        paginas_nivel.setdefault(lv, set()).add(pg)
    dividir = {k for k, v in cuenta.items() if len(v) > SUBGRUPO_MIN and len({x for x in v if x}) >= 2}
    for s in schemas:
        meta = s["meta"]; sl = meta["slug"]; kind = meta.get("kind", "component")
        level = LEVEL.get(kind, "atoms")
        page = pagina(meta, cfg)
        code = s.get("code") or (s.get("source") or {}).get("code") or {}
        example = code.get("example") or ""
        interno = dcom.interno_de(s, cfg) is not None
        if interno:
            group = SPECIAL["internos"]["slug"]; grupos[(level, group)] = dict(SPECIAL["internos"]); internos += 1
        elif not example.strip() and padres.get(sl):
            group = SPECIAL["partes"]["slug"]; grupos[(level, group)] = dict(SPECIAL["partes"]); partes_n += 1
        elif not example.strip():
            group = f"{SPECIAL['pendientes']['slug']}/{slug(page)}"
            grupos[(level, SPECIAL["pendientes"]["slug"])] = dict(SPECIAL["pendientes"])
            grupos[(level, group)] = {"title": page}; pendientes += 1
        elif (level, page) in dividir and dcom.seccion(meta, cfg):
            sec = dcom.seccion(meta, cfg)
            if len(paginas_nivel[level]) == 1:
                group = slug(sec); grupos.setdefault((level, group), {"title": sec})
            else:
                group = f"{slug(page)}/{slug(sec)}"
                grupos.setdefault((level, slug(page)), {"title": page}); grupos.setdefault((level, group), {"title": sec})
        else:
            group = slug(page); grupos.setdefault((level, group), {"title": page})
        ver = (meta.get("verification") or {}).get("status") or "unverified"
        status = "Deprecated" if sl in retirados or (meta.get("lifecycle") or {}).get("status") == "deprecated" else STATUS.get(ver, "Draft")
        desc = re.sub(r"\s+", " ", (meta.get("description") or "").strip())
        desc = "" if desc == "unknown" else (desc[:179].rstrip() + "…" if len(desc) > 180 else desc)
        base = f"src/patterns/{level}/{group}/{sl}/{sl}"
        contract = os.path.relpath(os.path.join(ds, "schemas", "components", f"{sl}.schema.json"),
                                   os.path.join(lib, os.path.dirname(base))).replace(os.sep, "/")
        docs = s.get("docs") or (s.get("source") or {}).get("docs") or {}
        ficha = read(os.path.join(root, docs.get("file", "")), "") if docs.get("file") else ""
        analisis = dv.analyze(s, example, css_cls, fid_cfg, ctx[1] if ctx else None) if (dv and not interno) else None
        pares = ctx[0].component_pairs(s["meta"]["slug"], ctx[1], ctx[2])["pairs"] if (ctx and (s.get("code") or {}).get("classes")) else None
        gal_html, _no_gen = dv.gallery(s, example, analisis, pares, ctx[1] if ctx else None) if (dv and analisis) else (None, [])
        # la página existe si hay algo que pintar o algo que decir: variantes que faltan en el ejemplo, o variantes que el proyecto
        # justificó en coverageIgnore con su motivo (si no, el motivo no aparecería en ninguna parte de la library)
        galeria = ("html", gal_html) if gal_html else (("texto", dv.lista_faltantes(analisis)) if (analisis and (analisis["missing"] or analisis.get("ignored_reasons"))) else None)
        if not gal_html and _no_gen:  # nada se pudo pintar: la página existe igual y dice por qué, con el mismo formato que la nota de la galería
            galeria = ("texto", ((galeria[1] + " ") if galeria else "") + dv.nota_no_pintadas(_no_gen))
        ficha_hoja = hoja(s, ficha, textos_pendientes.get(sl), ctx)
        if analisis and analisis["total"]:
            ficha_hoja["coverage"] = {"visible": analisis["visible"], "total": analisis["total"], "missing": analisis["missing"],
                                      "unchecked": analisis["unchecked"], "complete": not analisis["missing"]}
        variantes = {"default": {"_title": "Ejemplo de código"}}
        if galeria:
            variantes["todas-las-variantes"] = {"_title": "Todas las variantes", "view": "todas"}
        esperado[base + ".json"] = json.dumps({
            "title": meta.get("name") or sl, "description": desc, "status": status,
            "sheet": ficha_hoja,
            "ds": {"slug": sl, "kind": kind, "verification": ver, "figmaNodeId": (s.get("figma") or {}).get("nodeId"), "contract": contract},
            "variants": variantes,
        }, ensure_ascii=False, indent=2) + "\n"
        esperado[base + ".njk"] = example_to_njk(example, sl, assets_dir, problemas, galeria)
        # La ficha ya no va como .md corrido: va estructurada en «sheet» y el visor la pinta como tablero.
    for (level, group), info in grupos.items():
        esperado[f"src/patterns/{level}/{group}/_group.json"] = json.dumps(
            {k: v for k, v in info.items() if k in ("title", "order")}, ensure_ascii=False, indent=2) + "\n"

    actuales = set()
    pat = os.path.join(lib, "src", "patterns")
    for dp, dn, fn in os.walk(pat):
        if os.path.basename(dp) == "_base" or "/_base" in dp:
            continue
        for f in fn:
            if not f.startswith("."):
                actuales.add(os.path.relpath(os.path.join(dp, f), lib))
    sobran = sorted(actuales - set(esperado))
    desfasados = sorted(k for k, v in esperado.items() if read(os.path.join(lib, k)) != v)
    for nivel, sl, texto in problemas:
        print(f"  [{nivel}] {sl}: {texto}")
    errores = sum(1 for n, _, _ in problemas if n == "ERROR")
    if check:
        for k in desfasados:
            print(f"  desfasado o ausente: library/{k}")
        for k in sobran:
            print(f"  sobra: library/{k}")
        ok = not desfasados and not sobran and not errores
        print("catálogo al día" if ok else "catálogo desfasado o con iconos que no existen: ejecuta scripts/ds-library.py y corrige las fichas")
        return 0 if ok else 1
    for k in desfasados:
        path = os.path.join(lib, k)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(esperado[k])
    for k in sobran:
        os.remove(os.path.join(lib, k))
    for dp, dn, fn in os.walk(pat, topdown=False):
        if dp != pat and not os.listdir(dp):
            os.rmdir(dp)
    n = len(schemas)
    print(f"catálogo: {n} patrones en {len(grupos)} grupos · {len(desfasados)} archivos escritos · {len(sobran)} retirados · "
          f"{pendientes} pendientes de construir (sin ejemplo) · {partes_n} partes de otro componente · {internos} internos de Figma"
          + (f" · {errores} iconos que no existen" if errores else ""))
    print("para verlo: cd library && npm install && npm start")
    if desfasados or sobran:
        try:
            sys.path.insert(0, here)
            from activity import log
            log(root, "script", "ds-library", f"catálogo regenerado: {n} patrones, {len(desfasados)} archivos escritos, {len(sobran)} retirados")
        except Exception:
            pass
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
