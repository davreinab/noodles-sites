#!/usr/bin/env python3
"""ds-text-proposal — crea o actualiza la propuesta de textos de un componente, igual que el botón «Editar» de la library.

Cambiar la descripción o el criterio de uso de un componente no es trivial (design-system/proposals/README.md):
nunca se escribe el texto, se propone. Hay UNA propuesta de textos pendiente por componente
(<fecha>-<slug>-textos.proposal.json, proposedChange.kind "component-text"); cada campo tocado es un cambio
con su texto actual y el propuesto. Este script es la versión en Python de library/src/assets/viewer/proposal.js
(misma forma de propuesta), para que la IA o una persona propongan sin Node y sin editar el JSON a mano.

Uso:
    python3 scripts/ds-text-proposal.py --missing accesibilidad [--page "Buttons"]
        lista los componentes con ese campo sin escribir y sin propuesta pendiente (para trabajar por tandas);
        en accesibilidad cuenta también el texto que solo habla de contraste (no menciona rol, nombre,
        estados, teclado ni foco): lo de antes de la 12.7.0
    python3 scripts/ds-text-proposal.py --component badge --field accesibilidad \\
        --text-file /ruta/borrador.md --reason "Borrador por tipo de componente" --approver "Nombre" --origin ai
        crea o actualiza la propuesta; --field acepta «description» o el principio de la etiqueta del campo
        («accesibilidad», «propósito», «cuándo usar»); --text en vez de --text-file para textos cortos.
Un borrador con --origin ai queda marcado «Borrador de la IA» en la library hasta que una persona lo edita.
Tras escribir, regenera el índice de propuestas y el catálogo (si hay library/).
"""
import argparse
import glob
import importlib.util
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DS = os.path.join(ROOT, "design-system")
PROPOSALS = os.path.join(DS, "proposals")


def _lib():
    spec = importlib.util.spec_from_file_location("ds_library", os.path.join(HERE, "ds-library.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def jload(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def textos_actuales(sch, lib):
    """{campo: texto vigente}: la descripción (Figma) y los campos de criterio de la ficha."""
    meta = sch.get("meta") or {}
    desc = (meta.get("description") or "").strip()
    cur = {"description": "" if desc == "unknown" else desc}
    docs = sch.get("docs") or {}
    ficha = ""
    if docs.get("file"):
        try:
            ficha = open(os.path.join(ROOT, docs["file"]), encoding="utf-8").read()
        except OSError:
            pass
    manual, _ = lib.campos_manuales(lib.seccion_ficha(ficha, (sch.get("figma") or {}).get("nodeId")))
    for f in manual:
        cur[f["label"]] = "" if f["todo"] else f["md"]
    return cur, manual


# Un texto de accesibilidad que no habla de comportamiento no está hecho, aunque no esté vacío: las fichas
# anteriores a la 12.7.0 solo apuntaban contraste, que ahora mide ds-fidelity.
# Palabras completas: «rol» no debe casar con «control», ni «tab» con «tabla».
A11Y_CLAVES_RE = __import__("re").compile(
    r"\b(rol|role|aria-[\w-]+|aria|teclado|keyboard|foco|focus|lector(es)? de pantalla|screen reader|"
    r"nombre accesible|label|anuncia\w*|tab|enter|espacio|escape|esc|flechas?|no aplica|decorativ\w*)\b", 2)


def a11y_incompleto(texto):
    t = texto or ""
    return bool(t.strip()) and not A11Y_CLAVES_RE.search(t)


def pendiente_de(slug):
    for path in sorted(glob.glob(os.path.join(PROPOSALS, "*.proposal.json"))):
        p = jload(path)
        pc = (p or {}).get("proposedChange") or {}
        if pc.get("kind") == "component-text" and pc.get("component") == slug and p.get("status") in ("draft", "approved"):
            return p, os.path.basename(path)
    return None, None


def field_info(field):
    return {"label": "descripción", "where": "figma"} if field == "description" else {"label": f"«{field}»", "where": "ficha"}


def text_proposal(existing, ds, edit, now):
    """Misma lógica que textProposal() de library/src/assets/viewer/proposal.js."""
    today = now[:10]
    field = str(edit.get("field") or "description")
    origin = "ai" if edit.get("origin") == "ai" else "person"
    if existing:
        p = json.loads(json.dumps(existing))
    else:
        p = {"id": f"{today}-{ds['slug']}-textos", "status": "draft", "summary": "", "evidence": [], "affectedResources": [],
             "proposedChange": {"kind": "component-text", "component": ds["slug"], "name": ds["name"],
                                "figma": {"fileKey": ds.get("fileKey"), "nodeId": ds.get("nodeId")}, "changes": [], "history": []},
             "impact": {}, "migration": None, "requiredApprover": "", "decision": None}
    pc = p["proposedChange"]
    pc.setdefault("changes", []); pc.setdefault("history", [])
    if p.get("status") == "approved":
        p["status"] = "draft"
        pc["history"].append({"at": now, "action": "reopened", "note": "editada después de aprobarse: vuelve a pendiente",
                              "previousDecision": p.get("decision")})
        p["decision"] = None
    text = str(edit.get("text") or "").replace("\r\n", "\n").strip()
    current = str((ds.get("current") or {}).get(field) or "").strip()
    i = next((k for k, c in enumerate(pc["changes"]) if c.get("field") == field), None)
    if text == current:
        if i is not None:
            pc["changes"].pop(i)
    elif i is not None:
        pc["changes"][i]["proposed"] = text
        pc["changes"][i]["origin"] = origin
    else:
        pc["changes"].append({"field": field, "where": field_info(field)["where"], "current": current, "proposed": text, "origin": origin})
    pc["history"].append({"at": now, "action": "drafted" if origin == "ai" else ("edited" if existing else "created"), "field": field, "origin": origin})
    reason = str(edit.get("reason") or "").strip()
    if reason:
        p["evidence"].append({"type": "ai-draft" if origin == "ai" else "library-edit", "at": now, "field": field, "note": reason})
    if str(edit.get("approver") or "").strip():
        p["requiredApprover"] = str(edit["approver"]).strip()
    nombre = ds.get("name") or ds["slug"]
    campos = [field_info(c["field"])["label"] for c in pc["changes"]]
    p["summary"] = (f"Cambiar {' y '.join(campos)} de {nombre}. Texto propuesto desde la library; pendiente de aprobación."
                    if campos else f"Sin cambios: el texto propuesto para {nombre} coincide con el actual.")
    p["affectedResources"] = ([f"Figma {ds['nodeId']} (description)"] if any(c["where"] == "figma" for c in pc["changes"]) and ds.get("nodeId") else []) + \
        [f"design-system/schemas/components/{ds['slug']}.schema.json", f"design-system/docs/components/{ds['slug']}.md"]
    p["impact"] = {"summary": f"Cambia cómo se describe {nombre} y, con ello, cuándo lo usan diseño, desarrollo y la IA. "
                              "No cambia estructura, variantes ni estilos.", "components": [ds["slug"]]}
    return p


def resolver_campo(nombre, actuales):
    n = (nombre or "description").strip().lower()
    if n in ("description", "descripción", "descripcion"):
        return "description"
    for k in actuales:
        if k != "description" and k.lower().startswith(n):
            return k
    sys.exit(f"[ERROR] campo «{nombre}» no reconocido; los de esta ficha son: {', '.join(actuales)}")


def esquemas():
    for p in sorted(glob.glob(os.path.join(DS, "schemas", "components", "*.schema.json"))):
        s = jload(p)
        if isinstance(s, dict) and s.get("meta"):
            yield s


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--missing", metavar="CAMPO")
    ap.add_argument("--page")
    ap.add_argument("--component")
    ap.add_argument("--field", default="description")
    ap.add_argument("--text")
    ap.add_argument("--text-file")
    ap.add_argument("--reason")
    ap.add_argument("--approver")
    ap.add_argument("--origin", choices=["person", "ai"], default="person")
    a = ap.parse_args()
    lib = _lib()

    if a.missing:
        filas = []
        for s in esquemas():
            meta = s["meta"]
            if a.page and (meta.get("figmaPage") or "").split("/")[0].strip().lower() != a.page.strip().lower():
                continue
            if lib.es_interno(meta, lib.load_config(HERE)):
                continue
            actuales, manual = textos_actuales(s, lib)
            campo = next((f["label"] for f in manual if f["label"].lower().startswith(a.missing.lower())), None)
            if not campo:
                continue
            texto = actuales.get(campo) or ""
            es_a11y = campo.lower().startswith("accesibilidad")
            if texto and not (es_a11y and a11y_incompleto(texto)):
                continue
            motivo = "vacío" if not texto else "solo habla de contraste"
            pend, _ = pendiente_de(meta["slug"])
            if pend and any(c.get("field") == campo for c in (pend.get("proposedChange") or {}).get("changes") or []):
                continue
            filas.append((meta.get("figmaPage") or "", meta["slug"], motivo))
        for page, slug, motivo in filas:
            print(f"{page}\t{slug}\t{motivo}")
        print(f"{len(filas)} componentes con «{a.missing}» por escribir o incompleto y sin propuesta" + (f" en la página «{a.page}»" if a.page else ""), file=sys.stderr)
        return 0

    if not a.component:
        ap.error("falta --component (o --missing para listar)")
    sch = next((s for s in esquemas() if s["meta"].get("slug") == a.component), None)
    if not sch:
        sys.exit(f"[ERROR] no hay contrato para «{a.component}»")
    actuales, _ = textos_actuales(sch, lib)
    campo = resolver_campo(a.field, actuales)
    texto = open(a.text_file, encoding="utf-8").read() if a.text_file else (a.text or "")
    if not texto.strip():
        sys.exit("[ERROR] falta el texto propuesto (--text o --text-file)")
    if not (a.reason or "").strip():
        sys.exit("[ERROR] falta --reason: la propuesta necesita evidencia de por qué cambia")
    existente, archivo = pendiente_de(a.component)
    if not (a.approver or (existente or {}).get("requiredApprover")):
        sys.exit("[ERROR] falta --approver: una persona tiene que aprobarla")
    fg = sch.get("figma") or {}
    ds = {"slug": a.component, "name": sch["meta"].get("name") or a.component, "fileKey": fg.get("fileKey"),
          "nodeId": fg.get("nodeId"), "current": actuales}
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.") + "000Z"
    p = text_proposal(existente, ds, {"field": campo, "text": texto, "reason": a.reason, "approver": a.approver, "origin": a.origin}, now)
    archivo = archivo or f"{p['id']}.proposal.json"
    with open(os.path.join(PROPOSALS, archivo), "w", encoding="utf-8") as fh:
        fh.write(json.dumps(p, ensure_ascii=False, indent=2) + "\n")
    print(f"{'actualizada' if existente else 'creada'} design-system/proposals/{archivo} · campo «{campo}» · {a.origin}")
    for script in ("proposals-index.py", "ds-library.py"):
        subprocess.run([sys.executable, os.path.join(HERE, script)], cwd=ROOT, stdout=subprocess.DEVNULL)
    return 0


if __name__ == "__main__":
    sys.exit(main())
