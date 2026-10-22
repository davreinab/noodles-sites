#!/usr/bin/env python3
"""ds-source — diseñar el design system SIN Figma: la fuente de verdad vive en el repo.

Sin dependencias (stdlib, Python 3.8+). Uso, desde la raíz del proyecto:
    python3 scripts/ds-source.py --init          # crea design-system/source/ con la estructura marcada y activa el modo repo
    python3 scripts/ds-source.py --check         # valida la fuente (alias, tipos, capas, slots) y dice qué falla
    python3 scripts/ds-source.py                 # compila la fuente al volcado que lee ds-sync (lo hace ds-sync solo)
    python3 scripts/ds-source.py --figma-plan    # plan para llevar el sistema a Figma después (reports/figma-plan.json)
    python3 scripts/ds-source.py --status        # modo actual y qué hay en la fuente

Idea: hasta ahora el sync solo entendía volcados que escribe la IA leyendo Figma. Aquí la fuente la escribe una
persona (o la IA, con propuesta) en archivos legibles; este script los compila AL MISMO formato de volcado que
produce Figma, así que contratos, fichas, library, auditorías y exportaciones funcionan igual. Cambiar a Figma
más adelante no cambia nada aguas abajo: mismos nombres, mismos slugs.

El repo es un SUPERCONJUNTO de Figma: la fuente puede expresar capas, slots, estados e interacciones que Figma no
tiene. Exportar a Figma es con pérdida declarada: --figma-plan lista, por componente, lo que no se puede trasladar
(«gaps»), para que nada se pierda en silencio. Lo que Figma sí tiene se exporta con su estructura equivalente.

Estructura de la fuente (ver design-system/source/README.md, que escribe --init):
    source/tokens.json            colecciones, modos, tokens (color, number, string, boolean), alias
    source/components/<slug>.json props, slots, eventos, estados, anatomía (árbol de capas) e interacciones
"""
import argparse
import glob
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone

REPO_KEY = "repo"
TYPES = {"color": "COLOR", "number": "FLOAT", "string": "STRING", "boolean": "BOOLEAN"}
ARCH = ["primitive", "semantic", "components"]  # la cadena de alias va Components → Semantic → Primitive
HEX_RE = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")
PATH_RE = re.compile(r"^[a-z0-9][a-z0-9-]*(?:/[a-z0-9][a-z0-9-]*)*$")
UNIT_RE = re.compile(r"^-?\d+(?:\.\d+)?(?:px|rem|em|%|ms|s)?$")
KEYWORDS = {"auto", "fill", "hug", "fixed", "center", "start", "end", "stretch", "space-between", "horizontal", "vertical",
            "grid", "wrap", "nowrap", "none", "left", "right", "top", "bottom", "inherit"}
FIGMA_INTERACTIONS = {"click", "hover", "press", "pressed", "focus", "drag", "mouse-enter", "mouse-leave", "key"}
NODE_TYPES = {"frame": "FRAME", "text": "TEXT", "image": "RECTANGLE", "icon": "INSTANCE", "instance": "INSTANCE", "vector": "VECTOR"}


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")


def kebab(name):
    """Nombre de propiedad al estilo Figma (show-cta): el motor lo vuelve a camelCase (showCta) en el contrato."""
    return re.sub(r"[^A-Za-z0-9]+", "-", re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", str(name))).strip("-").lower()


def read_json(path, default=None):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return default


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def hex_to_rgba(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    a = int(h[6:8], 16) / 255 if len(h) == 8 else 1
    return {"r": round(r, 6), "g": round(g, 6), "b": round(b, 6), "a": 1 if a == 1 else round(a, 6)}


def role_of(name):
    n = (name or "").lower()
    return "primitive" if "primitiv" in n else "semantic" if "semant" in n else "components" if "component" in n else None


# ───────────────────────────── tokens ─────────────────────────────
def compile_tokens(src, errs, warns):
    """tokens.json de la fuente → colecciones en el formato de volcado de variables. Devuelve (colecciones, índice)."""
    colls = src.get("collections") if isinstance(src, dict) else None
    if not isinstance(colls, list):
        errs.append("source/tokens.json: falta «collections» (una lista de colecciones)")
        return [], {}
    index, nombres = {}, set()
    for col in colls:
        cname = col.get("name") if isinstance(col, dict) else None
        if not cname or not isinstance(col.get("tokens", {}), dict):
            errs.append("source/tokens.json: cada colección necesita «name» y «tokens» (objeto ruta → token)")
            continue
        if cname.lower() in nombres:
            errs.append(f"colección «{cname}» repetida")
        nombres.add(cname.lower())
        for path, t in col["tokens"].items():
            index.setdefault(path, []).append((cname, t))
    cycle_graph = {}

    def resolve(ref, cname, path, mode):
        ref = ref.strip()
        want_col = None
        if ":" in ref:
            want_col, ref = ref.split(":", 1)
        cands = [(c, t) for c, t in index.get(ref, []) if not want_col or c.lower() == want_col.strip().lower()]
        if not cands:
            errs.append(f"{cname}/{path} ({mode}): el alias {{{ref}}} no existe")
            return None
        if len(cands) > 1:
            errs.append(f"{cname}/{path} ({mode}): el alias {{{ref}}} es ambiguo ({', '.join(c for c, _ in cands)}); usa {{Colección:{ref}}}")
            return None
        return cands[0][0], ref, cands[0][1]

    out = []
    for col in colls:
        cname = col.get("name") if isinstance(col, dict) else None
        if not cname:
            continue
        modes = col.get("modes") or ["Default"]
        if not isinstance(modes, list) or not modes or not all(isinstance(m, str) for m in modes):
            errs.append(f"colección «{cname}»: «modes» debe ser una lista de nombres")
            modes = ["Default"]
        cs = slug(cname)
        mode_ids = {m: f"{REPO_KEY}:{cs}:{slug(m)}" for m in modes}
        rol = role_of(cname)
        variables = []
        for path, t in col.get("tokens", {}).items():
            if not isinstance(t, dict):
                errs.append(f"{cname}/{path}: el token debe ser un objeto con «type» y «value»")
                continue
            ttype = t.get("type")
            if ttype not in TYPES:
                errs.append(f"{cname}/{path}: type «{ttype}» no válido (color, number, string o boolean)")
                continue
            if not PATH_RE.match(path):
                warns.append(f"{cname}/{path}: el nombre no sigue la convención (minúsculas, números y guiones, tramos separados por «/»)")
            val = t.get("value")
            per_mode = val if isinstance(val, dict) and (ttype != "string" or set(val) <= set(modes)) else {m: val for m in modes}
            if isinstance(val, dict):
                falta = [m for m in modes if m not in val]
                extra = [m for m in val if m not in modes]
                if falta:
                    errs.append(f"{cname}/{path}: falta el valor del modo {', '.join(falta)}")
                if extra:
                    errs.append(f"{cname}/{path}: modo(s) que la colección no tiene: {', '.join(extra)}")
            values = {}
            for m in modes:
                v = per_mode.get(m)
                if isinstance(v, str) and re.fullmatch(r"\s*\{[^{}]+\}\s*", v):
                    r = resolve(v.strip()[1:-1], cname, path, m)
                    if r is None:
                        continue
                    tc, tpath, tt = r
                    if tt.get("type") != ttype:
                        errs.append(f"{cname}/{path} ({m}): alias a {{{tpath}}} de otro tipo ({tt.get('type')} frente a {ttype})")
                    cycle_graph.setdefault((cname, path), set()).add((tc, tpath))
                    if role_of(tc) and rol and ARCH.index(role_of(tc)) > ARCH.index(rol):
                        warns.append(f"{cname}/{path}: alias hacia «{tc}», que está por encima en la cadena Components → Semantic → Primitive")
                    values[mode_ids[m]] = {"type": "alias", "id": f"VariableID:{REPO_KEY}:{slug(tc)}/{tpath}", "name": tpath}
                    continue
                try:
                    if ttype == "color":
                        if not (isinstance(v, str) and HEX_RE.match(v)):
                            raise ValueError("un color es #rgb, #rrggbb o #rrggbbaa")
                        conv = hex_to_rgba(v)
                    elif ttype == "number":
                        if isinstance(v, bool) or not isinstance(v, (int, float)):
                            raise ValueError("un number es un número")
                        conv = v
                    elif ttype == "boolean":
                        if not isinstance(v, bool):
                            raise ValueError("un boolean es true o false")
                        conv = v
                    else:
                        if not isinstance(v, str):
                            raise ValueError("un string es texto")
                        conv = v
                except ValueError as e:
                    errs.append(f"{cname}/{path} ({m}): valor «{v}» no válido, {e}")
                    continue
                if rol == "semantic" and not isinstance(v, dict):
                    warns.append(f"{cname}/{path} ({m}): un token semántico lleva un alias a un primitivo, no un valor crudo")
                values[mode_ids[m]] = {"type": "value", "value": conv}
            hidden = t.get("hidden")
            if hidden is None:
                hidden = bool(col.get("primitive")) or rol == "primitive"
            variables.append({"id": f"VariableID:{REPO_KEY}:{cs}/{path}", "name": path, "type": TYPES[ttype],
                              "description": t.get("description") or "", "scopes": t.get("scopes") or [],
                              "codeSyntax": {}, "hiddenFromPublishing": bool(hidden), "valuesByMode": values})
        out.append({"id": f"VariableCollectionId:{REPO_KEY}:{cs}", "name": cname,
                    "modes": [{"modeId": mode_ids[m], "name": m} for m in modes], "defaultModeId": mode_ids[modes[0]],
                    "variables": variables, "fileKey": REPO_KEY, "source": REPO_KEY})
    # ciclos de alias
    state = {}

    def dfs(n, trail):
        state[n] = 1
        for nxt in cycle_graph.get(n, ()):
            if state.get(nxt) == 1:
                errs.append("ciclo de alias: " + " → ".join(f"{c}/{p}" for c, p in trail + [n, nxt]))
            elif state.get(nxt) is None:
                dfs(nxt, trail + [n])
        state[n] = 2
    for n in list(cycle_graph):
        if state.get(n) is None:
            dfs(n, [])
    return out, index


# ───────────────────────────── componentes ─────────────────────────────
def _token_refs(node, index, where, errs, warns):
    """Rutas de token que usa una capa (layout, style, text.fill). Un valor crudo es un aviso, no un error."""
    refs = []

    def classify(v, campo):
        if not isinstance(v, str):
            return
        s = v.strip()
        if s.startswith("{") and s.endswith("}"):
            s = s[1:-1]
        if HEX_RE.match(s) or UNIT_RE.match(s):
            warns.append(f"{where}: {campo} usa el valor crudo «{s}»; usa un token")
        elif s in KEYWORDS:
            return
        elif s in index:
            refs.append(s)
        else:
            errs.append(f"{where}: {campo} apunta al token «{s}», que no existe en tokens.json")
    for grupo in ("layout", "style"):
        g = node.get(grupo)
        if isinstance(g, dict):
            for k, v in g.items():
                classify(v, f"{grupo}.{k}")
    tx = node.get("text")
    if isinstance(tx, dict) and "fill" in tx:
        classify(tx["fill"], "text.fill")
    return refs


def _walk(node, fn, depth=0):
    fn(node, depth)
    for ch in node.get("children") or []:
        if isinstance(ch, dict):
            _walk(ch, fn, depth + 1)


def compile_component(path, index, comp_slugs, errs, warns):
    d = read_json(path)
    fname = os.path.basename(path)
    if not isinstance(d, dict) or not d.get("name"):
        errs.append(f"{fname}: debe ser un objeto con «name»")
        return None
    name = d["name"]
    sl = slug(name)
    if slug(fname[:-5]) != sl:
        warns.append(f"{fname}: el archivo debería llamarse {sl}.json (el slug sale del nombre)")
    kind = d.get("kind") or "component"
    group = d.get("group") or ("Patterns" if kind == "pattern" else "Components")
    page = f"Patterns / {group}" if kind == "pattern" and "pattern" not in group.lower() else group
    props, axes, properties, nested, tokens = d.get("props") or [], {}, [], [], []
    for p in props:
        pn, pt = p.get("name"), p.get("type")
        if not pn or pt not in ("enum", "boolean", "string", "icon"):
            errs.append(f"{name}: la propiedad {p!r} necesita «name» y «type» (enum, boolean, string o icon)")
            continue
        if pt == "enum":
            vals = [str(v) for v in p.get("values") or []]
            if len(vals) < 2:
                errs.append(f"{name}.{pn}: un enum necesita al menos dos valores")
                continue
            axes[kebab(pn)] = vals
            properties.append({"name": kebab(pn), "kind": "VARIANT", "default": str(p.get("default", vals[0])), "values": vals})
        elif pt == "boolean":
            properties.append({"name": kebab(pn), "kind": "BOOLEAN", "default": bool(p.get("default", False))})
        elif pt == "string":
            properties.append({"name": kebab(pn), "kind": "TEXT", "default": p.get("default", "")})
        else:
            dflt = p.get("default")
            properties.append({"name": kebab(pn), "kind": "INSTANCE_SWAP", "default": None, "defaultComponent": dflt, "preferredValues": []})
            nested.append({"layer": kebab(pn), "component": dflt or "icon", "componentSet": None, "exposedAs": kebab(pn), "toggledBy": None, "visibleByDefault": True})
    states = d.get("states") or []
    if states and "state" not in axes:
        axes["state"] = [str(s) for s in states]
        properties.append({"name": "state", "kind": "VARIANT", "default": str(states[0]), "values": [str(s) for s in states]})
    slots = d.get("slots") or []
    slot_names = set()
    for s in slots:
        if not isinstance(s, dict) or not s.get("name"):
            errs.append(f"{name}: cada slot necesita «name»")
        else:
            slot_names.add(s["name"])
    prop_names = {p.get("name") for p in props}
    anatomy = d.get("anatomy")
    capas, usados = [], set()
    if anatomy is not None:
        if not isinstance(anatomy, dict):
            errs.append(f"{name}: «anatomy» debe ser una capa raíz (objeto)")
        else:
            def visit(node, depth):
                lbl = node.get("layer") or node.get("slot")
                if not lbl:
                    errs.append(f"{name}: una capa de la anatomía no tiene «layer» ni «slot»")
                    return
                capas.append(lbl)
                where = f"{name} · capa «{lbl}»"
                if node.get("type") and node["type"] not in NODE_TYPES:
                    warns.append(f"{where}: type «{node['type']}» desconocido; se trata como frame")
                if node.get("slot") and node["slot"] not in slot_names:
                    errs.append(f"{where}: usa el slot «{node['slot']}», que no está declarado en «slots»")
                vw = node.get("visibleWhen")
                if isinstance(vw, str) and re.fullmatch(r"[A-Za-z_][\w]*", vw) and vw not in prop_names:
                    errs.append(f"{where}: visibleWhen apunta a la propiedad «{vw}», que no existe")
                if node.get("instance"):
                    nested.append({"layer": lbl, "component": node["instance"], "componentSet": None, "exposedAs": None,
                                   "toggledBy": kebab(vw) if isinstance(vw, str) and vw in prop_names else None, "visibleByDefault": True})
                    if node["instance"] not in comp_slugs:
                        warns.append(f"{where}: instancia de «{node['instance']}», que no es un componente de la fuente")
                for r in _token_refs(node, index, where, errs, warns):
                    usados.add(r)
            _walk(anatomy, visit)
    for t in d.get("tokens") or []:
        if t not in index:
            errs.append(f"{name}: tokens → «{t}» no existe en tokens.json")
        else:
            usados.add(t)
    for t in sorted(usados):
        roles = {role_of(c) for c, _ in index.get(t, [])}
        if roles == {"primitive"}:
            warns.append(f"{name}: consume el primitivo «{t}»; un componente usa tokens semánticos o de componente")
        tokens.append(f"token: {t}")
    nvar = 1
    for v in axes.values():
        nvar *= len(v)
    entry = {"page": page, "name": name, "type": "COMPONENT_SET" if axes else "COMPONENT", "id": f"{REPO_KEY}:{sl}", "key": None,
             "description": d.get("description") or "", "variantAxes": axes, "variantCount": nvar if axes else 1,
             "properties": properties, "nestedInstances": nested,
             "bindings": {"variables": tokens, "textStyles": []}, "autoLayout": bool(((anatomy or {}).get("layout") or {}).get("direction"))}
    extra = {}
    if slots:
        extra["slots"] = slots
    if d.get("events"):
        extra["events"] = d["events"]
    if anatomy is not None or d.get("interactions") or states:
        extra["anatomy"] = {"layers": anatomy, "states": states, "interactions": d.get("interactions") or []}
    entry.update(extra)
    return entry


# ───────────────────────────── compilación ─────────────────────────────
def compile_source(ds, write=True):
    """Compila design-system/source/ al volcado de ds-sync. Devuelve {errors, warnings, tokens, components, written}."""
    errs, warns = [], []
    src_dir = os.path.join(ds, "source")
    tokens_src = read_json(os.path.join(src_dir, "tokens.json"))
    if tokens_src is None:
        return {"errors": ["no hay design-system/source/tokens.json (o no es JSON válido): ejecuta ds-source.py --init"],
                "warnings": [], "tokens": 0, "components": 0, "written": []}
    colecciones, index = compile_tokens(tokens_src, errs, warns)
    files = sorted(glob.glob(os.path.join(src_dir, "components", "*.json")))
    comp_slugs = {slug((read_json(f) or {}).get("name", "")) for f in files}
    entradas = []
    for f in files:
        e = compile_component(f, index, comp_slugs, errs, warns)
        if e:
            entradas.append(e)
    vistos = {}
    for e in entradas:
        s = slug(e["name"])
        if s in vistos:
            errs.append(f"componente «{e['name']}» repetido (slug {s})")
        vistos[s] = 1
    n_tok = sum(len(c["variables"]) for c in colecciones)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    via = "ds-source.py: la fuente está en el repo (design-system/source/), no en Figma"
    variables = {"fileKey": REPO_KEY, "fileName": "Repositorio · design-system/source", "version": None, "readAt": now, "readVia": via,
                 "collections": colecciones, "textStyles": [], "effectStyles": [],
                 "readProgress": {REPO_KEY: {"total": n_tok, "read": n_tok}}}
    paginas = {}
    for e in sorted(entradas, key=lambda x: (x["page"], x["name"])):
        paginas.setdefault(e["page"], []).append(e)
    pages = [{"name": p, "id": f"{REPO_KEY}:page:{slug(p)}", "fileKey": REPO_KEY, "components": cs, "total": len(cs), "read": len(cs)}
             for p, cs in sorted(paginas.items())]
    componentes = {"fileKey": REPO_KEY, "readAt": now, "readVia": via, "pages": pages}
    written = []
    if write and not errs:
        for nombre, data in (("variables.json", variables), ("components.json", componentes)):
            path = os.path.join(ds, "sync", nombre)
            old = read_json(path)
            if isinstance(old, dict):
                # no se reescribe si solo cambia la fecha de lectura: una relectura sin cambios no ensucia git
                a, b = dict(old), dict(data)
                a.pop("readAt", None), b.pop("readAt", None)
                if a == b:
                    continue
            write_json(path, data)
            written.append(nombre)
    return {"errors": errs, "warnings": warns, "tokens": n_tok, "components": len(entradas), "written": written,
            "_collections": colecciones, "_entries": entradas}


# ───────────────────────────── plan para Figma ─────────────────────────────
def _figma_layer(node, gaps, comp):
    t = NODE_TYPES.get(node.get("type") or ("frame"), "FRAME")
    if node.get("slot"):
        out = {"name": node["slot"], "figmaType": "SLOT", "fallback": "INSTANCE_SWAP con valores preferidos", "slot": node["slot"]}
    else:
        out = {"name": node.get("layer"), "figmaType": "INSTANCE" if node.get("instance") else t}
        if node.get("instance"):
            out["component"] = node["instance"]
            if node.get("props"):
                out["propertyOverrides"] = node["props"]
    lay = node.get("layout") or {}
    if lay:
        d = lay.get("direction")
        if d == "grid":
            gaps.append(f"{comp} · capa «{out['name']}»: layout en rejilla; Figma lo resuelve con auto layout y wrap, no es equivalente")
            d = "horizontal"
        out["autoLayout"] = {"layoutMode": "HORIZONTAL" if d == "horizontal" else "VERTICAL" if d == "vertical" else None,
                             "bind": {k: v for k, v in lay.items() if k not in ("direction",) and isinstance(v, str)},
                             "raw": {k: v for k, v in lay.items() if not isinstance(v, str)}}
    st = node.get("style") or {}
    if st:
        out["bindings"] = {k: v for k, v in st.items() if isinstance(v, str)}
    if node.get("text"):
        out["text"] = node["text"]
    vw = node.get("visibleWhen")
    if vw:
        if isinstance(vw, str) and re.fullmatch(r"[A-Za-z_]\w*", vw):
            out["visibleBoundTo"] = kebab(vw)
        else:
            gaps.append(f"{comp} · capa «{out['name']}»: visibleWhen «{vw}» es una expresión; Figma solo liga la visibilidad a una propiedad booleana")
    for k in node:
        if k.startswith("$") or k in ("responsive", "container", "animation", "transition"):
            gaps.append(f"{comp} · capa «{out['name']}»: «{k}» no tiene equivalente en Figma; queda en el repo y se documenta en la descripción")
    ch = [_figma_layer(c, gaps, comp) for c in node.get("children") or [] if isinstance(c, dict)]
    if ch:
        out["children"] = ch
    return out


def figma_plan(ds, res):
    """Plan estructurado para que el agente construya el sistema en Figma por el MCP. No ejecuta nada."""
    gaps_global = []
    cols = []
    for c in res["_collections"]:
        modos = {m["modeId"]: m["name"] for m in c["modes"]}
        variables = []
        for v in c["variables"]:
            valores = {}
            for mid, val in v["valuesByMode"].items():
                valores[modos[mid]] = {"alias": val["name"]} if val["type"] == "alias" else val["value"]
            variables.append({"name": v["name"], "resolvedType": v["type"], "scopes": v["scopes"], "description": v["description"],
                              "hiddenFromPublishing": v["hiddenFromPublishing"], "valuesByMode": valores})
        cols.append({"name": c["name"], "modes": list(modos.values()), "variables": variables})
    comps = []
    for e in res["_entries"]:
        gaps = []
        an = (e.get("anatomy") or {})
        capas = _figma_layer(an["layers"], gaps, e["name"]) if isinstance(an.get("layers"), dict) else None
        for it in an.get("interactions") or []:
            on = str(it.get("on", "")).lower()
            if it.get("figma"):
                continue
            if on not in FIGMA_INTERACTIONS:
                gaps.append(f"{e['name']} · interacción «{it.get('on')}»{(' sobre ' + str(it.get('target'))) if it.get('target') else ''}: "
                            f"{it.get('effect') or it.get('do') or 'sin descripción'}; no tiene equivalente en Figma, queda en el repo")
            else:
                gaps.append(f"{e['name']} · interacción «{it.get('on')}»: en Figma se representa como variante de estado o prototipo; "
                            f"decláralo en «figma» de la interacción si quieres que el plan lo incluya")
        comps.append({"name": e["name"], "slug": slug(e["name"]), "page": e["page"],
                      "figma": {"type": e["type"], "variantAxes": e["variantAxes"],
                                "properties": [{"name": p["name"], "type": p["kind"], "default": p.get("default"), "values": p.get("values")}
                                               for p in e["properties"]], "layers": capas},
                      "slots": e.get("slots") or [], "events": e.get("events") or [], "gaps": gaps})
    plan = {"generatedBy": "scripts/ds-source.py --figma-plan", "note": "Plan, no ejecución: el agente lo construye en Figma por el MCP "
            "(tokens primero, luego componentes por tramos). Los gaps son lo que Figma no puede expresar; no se pierde, sigue en el repo.",
            "variables": {"collections": cols}, "components": comps,
            "gaps": gaps_global + [g for c in comps for g in c["gaps"]]}
    write_json(os.path.join(ds, "reports", "figma-plan.json"), plan)
    return plan


# ───────────────────────────── --init ─────────────────────────────
README = """# design-system/source — la fuente de verdad, sin Figma

Esta carpeta la escriben personas (o la IA, con propuesta aprobada). Nada de aquí es generado.
`python3 scripts/ds-sync.py` la compila solo al volcado que ya entiende todo el sistema (tokens.css, tokens.json,
contratos, fichas, library, auditorías). Lo que sale de aquí no se edita a mano: se edita aquí.

El repo es un superconjunto de Figma: aquí puedes expresar capas, slots, estados e interacciones que Figma no tiene.
Pasar a Figma después es con pérdida declarada: `python3 scripts/ds-source.py --figma-plan` escribe
`design-system/reports/figma-plan.json` con la estructura equivalente y la lista de «gaps».

## tokens.json

```json
{
  "collections": [
    {"name": "Primitive", "modes": ["Default"], "tokens": {
      "color/blue/500": {"type": "color", "value": "#0055FF", "description": "azul de marca"},
      "spacing/4": {"type": "number", "value": 16}}},
    {"name": "Semantic", "modes": ["Light", "Dark"], "tokens": {
      "surface/action/primary/default": {"type": "color", "description": "fondo de la acción principal",
        "value": {"Light": "{color/blue/500}", "Dark": "{color/blue/300}"}}}},
    {"name": "Components", "modes": ["Default"], "tokens": {}}
  ]
}
```
- `type`: color (#rgb, #rrggbb, #rrggbbaa), number (px; 0 sin unidad), string, boolean.
- `value`: un valor para todos los modos, o un objeto con un valor por modo. Un alias es `{ruta}` o `{Colección:ruta}`.
- La cadena de alias va siempre Components → Semantic → Primitive. Los componentes usan tokens semánticos.
- Nombres: minúsculas, números y guiones; tramos separados por `/` (pasan a Figma tal cual y a CSS con guiones).
- Opcionales: `description`, `scopes` (los de Figma, p. ej. ALL_FILLS), `hidden`.

## components/<slug>.json

```json
{
  "name": "card-offer", "kind": "component", "group": "Cards", "description": "…",
  "props": [{"name": "size", "type": "enum", "values": ["s", "m"], "default": "m"},
            {"name": "showBadge", "type": "boolean", "default": true},
            {"name": "title", "type": "string", "default": "Título"}],
  "slots": [{"name": "content", "accepts": "texto, badge o botones"}],
  "events": [{"name": "select", "when": "la persona activa la tarjeta"}],
  "states": ["default", "hover", "focus", "disabled"],
  "anatomy": {"layer": "root", "tag": "article",
    "layout": {"direction": "vertical", "gap": "spacing/m"},
    "style": {"fill": "surface/card/default", "radius": "radius/m"},
    "children": [{"layer": "title", "type": "text", "text": {"fill": "text/default"}},
                 {"slot": "content"},
                 {"layer": "cta", "instance": "button", "props": {"type": "primary"}, "visibleWhen": "showBadge"}]},
  "interactions": [{"on": "hover", "target": "root", "effect": "eleva la sombra", "figma": "variant state=hover"},
                   {"on": "swipe", "effect": "descarta la tarjeta"}]
}
```
- `props.type`: enum, boolean, string, icon. Los enum y los estados son variantes.
- Capas: `layer` o `slot`; `type`: frame, text, image, icon, instance, vector; `layout`, `style` y `text.fill`
  llevan **rutas de token**, no valores crudos (un valor crudo da aviso).
- `interactions`: libres. Las que Figma no puede expresar (como «swipe») quedan en el repo y salen como gap al exportar.
- El ejemplo HTML, el CSS y la ficha de criterio se escriben donde siempre: la ficha `.md` y `components.css`.

Validar: `python3 scripts/ds-source.py --check`.
"""

TOKENS_INIT = {"collections": [
    {"name": "Primitive", "modes": ["Default"], "tokens": {}},
    {"name": "Semantic", "modes": ["Light", "Dark"], "tokens": {}},
    {"name": "Components", "modes": ["Default"], "tokens": {}}]}


FIG_INI, FIG_FIN = "<!-- solo-figma:inicio -->", "<!-- solo-figma:fin -->"
FIG_GUIDE = os.path.join("guides", "figma-guides.md")


def apartar_figma(ds):
    """Modo repo: las guías que solo valen con Figma (reglas duras en Figma, sync desde Figma y auditoría del DS en
    Figma, ~16 000 tokens) salen de design.md a guides/figma-guides.md para que nadie las lea sin necesitarlas.
    Devuelve cuántos bloques movió. Se deshace con --restore-figma-guides."""
    dpath = os.path.join(ds, "design.md")
    try:
        txt = open(dpath, encoding="utf-8").read()
    except OSError:
        return 0
    bloques, out, pos = [], [], 0
    while True:
        a = txt.find(FIG_INI, pos)
        if a < 0:
            break
        b = txt.find(FIG_FIN, a)
        if b < 0:
            break
        b += len(FIG_FIN)
        n = len(bloques) + 1
        bloques.append(txt[a:b])
        out.append(txt[pos:a])
        out.append("<!-- solo-figma:movido-%d -->\n> Guía solo de Figma, movida a `design-system/%s` (bloque %d): en modo repo no se lee. "
                   "Se devuelve con `python3 scripts/ds-source.py --restore-figma-guides`." % (n, FIG_GUIDE.replace(os.sep, "/"), n))
        pos = b
    if not bloques:
        return 0
    out.append(txt[pos:])
    gpath = os.path.join(ds, FIG_GUIDE)
    os.makedirs(os.path.dirname(gpath), exist_ok=True)
    with open(gpath, "w", encoding="utf-8") as fh:
        fh.write("# Guías solo de Figma\n\nMovidas de `design.md` al pasar a modo repo. Léelas solo si el proyecto vuelve a Figma "
                 "(`python3 scripts/ds-source.py --restore-figma-guides` las devuelve a `design.md`).\n\n")
        for i, bl in enumerate(bloques, 1):
            fh.write("<!-- bloque %d -->\n%s\n<!-- /bloque %d -->\n\n" % (i, bl, i))
    with open(dpath, "w", encoding="utf-8") as fh:
        fh.write("".join(out))
    return len(bloques)


def restaurar_figma(ds):
    """Devuelve a design.md los bloques de guides/figma-guides.md. Devuelve cuántos."""
    import re
    gpath, dpath = os.path.join(ds, FIG_GUIDE), os.path.join(ds, "design.md")
    try:
        guia = open(gpath, encoding="utf-8").read()
        txt = open(dpath, encoding="utf-8").read()
    except OSError:
        return 0
    n = 0
    for m in re.finditer(r"<!-- bloque (\d+) -->\n(.*?)\n<!-- /bloque \1 -->", guia, re.S):
        marca = re.search(r"<!-- solo-figma:movido-%s -->\n>[^\n]*" % m.group(1), txt)
        if marca:
            txt = txt[:marca.start()] + m.group(2) + txt[marca.end():]
            n += 1
    if n:
        with open(dpath, "w", encoding="utf-8") as fh:
            fh.write(txt)
        os.remove(gpath)
        try:
            os.rmdir(os.path.dirname(gpath))
        except OSError:
            pass
    return n


def init(ds):
    src = os.path.join(ds, "source")
    creados = []
    if not os.path.isfile(os.path.join(src, "tokens.json")):
        write_json(os.path.join(src, "tokens.json"), TOKENS_INIT)
        creados.append("source/tokens.json")
    if not os.path.isfile(os.path.join(src, "README.md")):
        with open(os.path.join(src, "README.md"), "w", encoding="utf-8") as fh:
            fh.write(README)
        creados.append("source/README.md")
    os.makedirs(os.path.join(src, "components"), exist_ok=True)
    gk = os.path.join(src, "components", ".gitkeep")
    if not os.path.exists(gk):
        open(gk, "w").close()
        creados.append("source/components/")
    mpath = os.path.join(ds, "agent-manifest.json")
    m = read_json(mpath, {}) or {}
    if m.get("sourceMode") != "repo":
        m["sourceMode"] = "repo"
        write_json(mpath, m)
        creados.append("agent-manifest.json → sourceMode: repo")
    movidos = apartar_figma(ds)
    if movidos:
        creados.append("design.md → %d guías solo de Figma movidas a guides/figma-guides.md (menos lectura por tarea)" % movidos)
    return creados


def source_mode(ds):
    return (read_json(os.path.join(ds, "agent-manifest.json"), {}) or {}).get("sourceMode") or "figma"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=None)
    ap.add_argument("--init", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--figma-plan", dest="figma_plan", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--restore-figma-guides", dest="restore_figma", action="store_true")
    a = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(a.root or os.path.dirname(here))
    ds = os.path.join(root, "design-system")
    if a.restore_figma:
        n = restaurar_figma(ds)
        print("ds-source · %d guías de Figma devueltas a design.md" % n if n else "ds-source · no hay guías de Figma que devolver")
        return 0
    if a.init:
        c = init(ds)
        print("ds-source · " + ("creado: " + ", ".join(c) if c else "ya estaba inicializado") +
              "\nSiguiente: escribe los tokens en source/tokens.json y los componentes en source/components/, "
              "y ejecuta python3 scripts/ds-source.py --check y después python3 scripts/ds-sync.py")
        return 0
    if a.status:
        r = compile_source(ds, write=False)
        print(f"modo de fuente: {source_mode(ds)} · tokens {r['tokens']} · componentes {r['components']} · "
              f"{len(r['errors'])} errores · {len(r['warnings'])} avisos")
        return 1 if r["errors"] else 0
    r = compile_source(ds, write=not a.check and not a.figma_plan)
    for w in r["warnings"]:
        print(f"  [AVISO] {w}")
    for e in r["errors"]:
        print(f"  [ERROR] {e}")
    if r["errors"]:
        print(f"ds-source · la fuente no es válida: {len(r['errors'])} errores, no se escribe nada")
        return 1
    if a.figma_plan:
        p = figma_plan(ds, r)
        print(f"ds-source · plan para Figma: {len(p['variables']['collections'])} colecciones, {r['tokens']} variables, "
              f"{r['components']} componentes, {len(p['gaps'])} gaps → design-system/reports/figma-plan.json")
        return 0
    if a.check:
        print(f"ds-source · fuente válida: {r['tokens']} tokens, {r['components']} componentes, {len(r['warnings'])} avisos")
        return 0
    print(f"ds-source · compilado: {r['tokens']} tokens y {r['components']} componentes" +
          (f" → sync/{', sync/'.join(r['written'])}" if r["written"] else " (sin cambios)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
