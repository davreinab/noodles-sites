#!/usr/bin/env python3
"""
ds-release.py — pone versión al design system y redacta el registro de cambios.

Versiona el SISTEMA, no la herramienta que lo genera. Compara el estado actual (tokens y
contratos de componente) contra la última publicación guardada en
design-system/reports/release-baseline.json y clasifica el salto:

  mayor   desaparece o se renombra algo que alguien podía estar usando
          (token, componente, variante, estado o propiedad)   → rompe a quien lo consuma
  menor   se añade algo                                        → nadie se rompe
  parche  solo cambian valores o descripciones                 → sin cambio de estructura

Por defecto solo informa. Con --apply sube la versión en agent-manifest.json, escribe la
entrada en CHANGELOG.md y guarda la nueva línea base.

Uso:  python3 scripts/ds-release.py [--root .] [--apply] [--as major|minor|patch]
      --as     fuerza el salto cuando el criterio humano manda sobre el automático.
      python3 scripts/ds-release.py --check     # estado (borrador o publicado) y propuestas que faltan

Borrador y publicado: mientras no exista una publicación (la línea base está vacía) el design system es un
BORRADOR y se edita sin propuestas. La primera `--apply` fija la línea base y lo declara publicado. Desde ahí,
cambiar o retirar algo que ya estaba publicado exige una propuesta aprobada (`proposals/`, estado approved o
applied) que lo cite en `affectedResources`. Añadir algo nuevo no la necesita. `--check` lo comprueba contra la
línea base; `proposalsEnforcement` en agent-manifest.json decide si falta una propuesta es aviso (por defecto) o error.
Sin dependencias externas: solo biblioteca estándar.
"""

import argparse
import datetime
import json
import os
import sys

ORDEN = {"none": 0, "patch": 1, "minor": 2, "major": 3}
NOMBRE = {"none": "sin cambios", "patch": "parche", "minor": "menor", "major": "mayor"}


def jload(p, default=None):
    try:
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return default


def fingerprint(ds):
    """Estado comparable del DS: estructura por un lado, valores por otro."""
    tokens, comps = {}, {}
    tj = jload(os.path.join(ds, "tokens", "tokens.json"), {}) or {}
    for cname, col in (tj.get("collections") or {}).items():
        for path, t in (col.get("tokens") or {}).items():
            modos = {m: (v or {}).get("resolvedValue") for m, v in (t.get("modes") or {}).items()}
            tokens[path] = {"collection": cname, "type": t.get("type"),
                            "values": modos or {"_": t.get("resolvedValue")},
                            "description": t.get("description")}
    cdir = os.path.join(ds, "schemas", "components")
    if os.path.isdir(cdir):
        for f in sorted(os.listdir(cdir)):
            if not f.endswith(".schema.json") or f.startswith("_"):
                continue
            sch = jload(os.path.join(cdir, f)) or {}
            api = sch.get("api") or {}
            descripcion = ((sch.get("meta") or {}).get("description") or "").strip()
            variantes = api.get("variants") or {}
            if isinstance(variantes, dict):
                variantes = {k: sorted(v or []) for k, v in variantes.items()}
            if isinstance(api.get("props"), list):
                # contrato 12.0.0: props con tipo; los enum llevan valores
                comps[f[:-len(".schema.json")]] = {
                    "props": {p["name"]: {"type": p.get("type"), "values": sorted(p.get("values") or [])} for p in api["props"] if p.get("name")},
                    "cssStates": sorted(api.get("cssStates") or []),
                    "description": descripcion,
                }
            else:
                comps[f[:-len(".schema.json")]] = {
                    "variants": variantes,
                    "states": sorted(api.get("states") or []),
                    "properties": sorted(p.get("name") for p in (api.get("properties") or []) if p.get("name")),
                }
    return {"tokens": tokens, "components": comps, "fingerprintVersion": 2}


def diff(base, now):
    quitados, anadidos, cambiados = [], [], []

    bt, nt = base.get("tokens") or {}, now.get("tokens") or {}
    for k in sorted(set(bt) - set(nt)):
        quitados.append("token `%s`" % k)
    for k in sorted(set(nt) - set(bt)):
        anadidos.append("token `%s`" % k)
    for k in sorted(set(bt) & set(nt)):
        if bt[k].get("type") != nt[k].get("type"):
            quitados.append("token `%s` cambia de tipo (%s → %s)" % (k, bt[k].get("type"), nt[k].get("type")))
        elif bt[k].get("values") != nt[k].get("values"):
            cambiados.append("token `%s`" % k)

    bc, nc = base.get("components") or {}, now.get("components") or {}
    if any("props" in v for v in nc.values()) and any("variants" in v for v in bc.values()):
        # la línea base es de un contrato anterior a la 12.0.0: sus claves no son comparables con las de ahora.
        # Se comparan solo los tokens; los componentes se dan por iguales y la próxima publicación reescribe la base.
        print("[AVISO] la línea base tiene contratos con la forma anterior a la 12.0.0: los componentes no se comparan "
              "esta vez (no es un cambio del DS, es un cambio de formato). Publica con --apply para renovar la línea base.")
        bc = {k: nc[k] for k in nc}
    for k in sorted(set(bc) - set(nc)):
        quitados.append("componente `%s`" % k)
    for k in sorted(set(nc) - set(bc)):
        anadidos.append("componente `%s`" % k)
    for k in sorted(set(bc) & set(nc)):
        if "props" in nc[k] or "props" in bc[k]:
            bp, np_ = bc[k].get("props") or {}, nc[k].get("props") or {}
            quitados += ["prop `%s` de `%s`" % (v, k) for v in sorted(set(bp) - set(np_))]
            anadidos += ["prop `%s` en `%s`" % (v, k) for v in sorted(set(np_) - set(bp))]
            for pn in sorted(set(bp) & set(np_)):
                if bp[pn].get("type") != np_[pn].get("type"):
                    quitados.append("prop `%s` de `%s` cambia de tipo (%s → %s)" % (pn, k, bp[pn].get("type"), np_[pn].get("type")))
                fuera = sorted(set(bp[pn].get("values") or []) - set(np_[pn].get("values") or []))
                dentro = sorted(set(np_[pn].get("values") or []) - set(bp[pn].get("values") or []))
                quitados += ["valor `%s` de `%s.%s`" % (v, k, pn) for v in fuera]
                anadidos += ["valor `%s` en `%s.%s`" % (v, k, pn) for v in dentro]
            fuera = sorted(set(bc[k].get("cssStates") or []) - set(nc[k].get("cssStates") or []))
            dentro = sorted(set(nc[k].get("cssStates") or []) - set(bc[k].get("cssStates") or []))
            quitados += ["estado de CSS `%s` de `%s`" % (v, k) for v in fuera]
            anadidos += ["estado de CSS `%s` en `%s`" % (v, k) for v in dentro]
            if "description" in bc[k] and bc[k].get("description") != nc[k].get("description"):
                cambiados.append("descripción de `%s`" % k)
            continue
        for campo, etiqueta in (("states", "estado"), ("properties", "propiedad")):
            fuera = sorted(set(bc[k].get(campo) or []) - set(nc[k].get(campo) or []))
            dentro = sorted(set(nc[k].get(campo) or []) - set(bc[k].get(campo) or []))
            quitados += ["%s `%s` de `%s`" % (etiqueta, v, k) for v in fuera]
            anadidos += ["%s `%s` en `%s`" % (etiqueta, v, k) for v in dentro]
        bv, nv = bc[k].get("variants") or {}, nc[k].get("variants") or {}
        for eje in sorted(set(bv) - set(nv)):
            quitados.append("eje de variante `%s` de `%s`" % (eje, k))
        for eje in sorted(set(nv) - set(bv)):
            anadidos.append("eje de variante `%s` en `%s`" % (eje, k))
        for eje in sorted(set(bv) & set(nv)):
            fuera = sorted(set(bv[eje] or []) - set(nv[eje] or []))
            dentro = sorted(set(nv[eje] or []) - set(bv[eje] or []))
            quitados += ["variante `%s/%s` de `%s`" % (eje, v, k) for v in fuera]
            anadidos += ["variante `%s/%s` en `%s`" % (eje, v, k) for v in dentro]

    nivel = "major" if quitados else "minor" if anadidos else "patch" if cambiados else "none"
    return nivel, {"quitados": quitados, "anadidos": anadidos, "cambiados": cambiados}


def recurso(item):
    """El recurso al que se refiere una línea del diff: la ruta del token, o el componente (último nombre entre
    comillas, sin el sufijo «.prop»)."""
    nombres = item.split("`")[1::2]
    if not nombres:
        return ""
    return nombres[0] if item.startswith("token") else nombres[-1].split(".")[0]


def propuestas_aprobadas(ds):
    """affectedResources de las propuestas que autorizan cambios: estado approved o applied, en la raíz o en aplicadas/."""
    out = []
    pdir = os.path.join(ds, "proposals")
    for d in (pdir, os.path.join(pdir, "aplicadas")):
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if not f.endswith(".json") or f.startswith("_"):
                continue
            pr = jload(os.path.join(d, f)) or {}
            if pr.get("status") in ("approved", "applied"):
                out.append((f, [str(r) for r in pr.get("affectedResources") or []]))
    return out


def cubierto(item, aprobadas):
    r = recurso(item)
    if not r:
        return None
    for f, recs in aprobadas:
        for x in recs:
            x = x.replace("component:", "").replace("token:", "").strip("` ")
            if x == r or x.endswith("/" + r) or x.startswith(r + "/") or x.startswith(r + "."):
                return f
    return None


def comprobar(ds, man, ahora, base):
    """Estado del ciclo de vida y propuestas que faltan. Devuelve el código de salida."""
    estado_base = (base or {}).get("state") or {}
    if base is None or not (estado_base.get("tokens") or estado_base.get("components")):
        print("Estado: BORRADOR. El design system nunca se ha publicado: se edita sin propuestas.")
        print("La primera `python3 scripts/ds-release.py --apply` fija la línea base y lo declara publicado.")
        return 0
    nivel, d = diff(estado_base, ahora)
    print("Estado: PUBLICADO (versión %s, línea base del %s)." % (base.get("version"), base.get("releasedAt")))
    pendientes = d["quitados"] + d["cambiados"]
    if not pendientes:
        print("Nada de lo ya publicado ha cambiado desde la línea base%s." % (
            "; hay %d cosas nuevas, que no necesitan propuesta" % len(d["anadidos"]) if d["anadidos"] else ""))
        return 0
    aprobadas = propuestas_aprobadas(ds)
    sin = [x for x in pendientes if not cubierto(x, aprobadas)]
    for x in pendientes:
        f = cubierto(x, aprobadas)
        print("  %s %s%s" % ("✓" if f else "✗", x, "  → " + f if f else "  → falta propuesta aprobada que lo cite en affectedResources"))
    modo = (man.get("proposalsEnforcement") or "warn").lower()
    if not sin:
        return 0
    tag = "[ERROR]" if modo == "error" else "[AVISO]"
    print("%s %d cambio(s) de lo ya publicado sin propuesta aprobada. Escribe la propuesta en design-system/proposals/ "
          "(estado approved o applied) y cita el recurso en affectedResources." % (tag, len(sin)))
    if modo != "error":
        print("(proposalsEnforcement es «warn»; ponlo en «error» en agent-manifest.json para que falle el commit)")
    return 1 if modo == "error" else 0


def bump(version, nivel):
    try:
        a, b, c = (int(x) for x in str(version).split("."))
    except Exception:
        a, b, c = 0, 0, 0
    return {"major": "%d.0.0" % (a + 1), "minor": "%d.%d.0" % (a, b + 1),
            "patch": "%d.%d.%d" % (a, b, c + 1)}.get(nivel, "%d.%d.%d" % (a, b, c))


def notes(version, fecha, nivel, d, pendientes):
    L = ["## %s · %s  _(salto %s)_" % (version, fecha, NOMBRE[nivel]), ""]
    if d["quitados"]:
        L += ["### Rompe", ""] + ["- Desaparece %s" % x for x in d["quitados"]] + [""]
        L += ["> **Ruta de actualización:** ⬜ escribe aquí qué usar en lugar de cada cosa retirada.",
              "> Sale del registro de `schemas/governance/lifecycle.json`.", ""]
    if d["anadidos"]:
        L += ["### Añade", ""] + ["- Nuevo %s" % x for x in d["anadidos"]] + [""]
    if d["cambiados"]:
        L += ["### Cambia de valor", ""] + ["- Cambia %s" % x for x in d["cambiados"]] + [""]
    if pendientes:
        L += ["### Obsoleto desde esta versión", ""] + \
             ["- `%s` → %s (desaparece en %s)" % (e["id"], e.get("replacement") or "sin sustituto", e.get("removeIn"))
              for e in pendientes] + [""]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--apply", action="store_true", help="sube la versión, escribe el CHANGELOG y guarda la línea base")
    ap.add_argument("--check", action="store_true", help="solo comprueba: borrador o publicado, y propuestas que faltan")
    ap.add_argument("--as", dest="forzado", choices=["major", "minor", "patch"], default=None)
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    ds = os.path.join(root, "design-system")
    mpath = os.path.join(ds, "agent-manifest.json")
    man = jload(mpath)
    if man is None:
        sys.exit("[ERROR] falta o no parsea design-system/agent-manifest.json")

    ahora = fingerprint(ds)
    bpath = os.path.join(ds, "reports", "release-baseline.json")
    base = jload(bpath)
    if a.check:
        return comprobar(ds, man, ahora, base)
    estado_base = (base or {}).get("state") or {}
    primera = base is None or not (estado_base.get("tokens") or estado_base.get("components"))
    if primera and base is not None:
        print("El design system nunca se ha publicado (la línea base está vacía): --apply hará la primera publicación.")

    if primera:
        nivel, d = ("minor" if (ahora["tokens"] or ahora["components"]) else "none"),\
                   {"quitados": [], "anadidos": ["primera publicación del sistema"], "cambiados": []}
    else:
        nivel, d = diff(base.get("state") or {}, ahora)

    if a.forzado:
        if ORDEN[a.forzado] < ORDEN[nivel]:
            print("[AVISO] fuerzas '%s' pero el diff exige '%s'. Se mantiene '%s': un salto menor "
                  "del debido rompe a quien consuma el sistema." % (a.forzado, NOMBRE[nivel], NOMBRE[nivel]))
        else:
            nivel = a.forzado

    actual = man.get("version") or "0.0.0"
    nueva = bump(actual, nivel)
    lc = jload(os.path.join(ds, "schemas", "governance", "lifecycle.json"), {}) or {}
    pendientes = [e for e in (lc.get("deprecations") or []) if e.get("removeIn") in (nueva, None)]

    print("Versión actual: %s" % actual)
    print("Salto detectado: %s%s" % (NOMBRE[nivel], "  (primera publicación)" if primera else ""))
    for etiqueta, clave in (("Desaparece", "quitados"), ("Se añade", "anadidos"), ("Cambia de valor", "cambiados")):
        if d[clave]:
            print("  %s (%d): %s%s" % (etiqueta, len(d[clave]), "; ".join(d[clave][:5]),
                                       " …" if len(d[clave]) > 5 else ""))
    legacy = (not primera and any("props" in v for v in (ahora.get("components") or {}).values())
              and any("variants" in v for v in ((base.get("state") or {}).get("components") or {}).values()))
    if nivel == "none":
        if legacy and a.apply:
            # misma versión: solo se renueva la línea base al formato 12.0.0 para que las próximas comparaciones sean reales
            os.makedirs(os.path.dirname(bpath), exist_ok=True)
            with open(bpath, "w", encoding="utf-8") as fh:
                fh.write(json.dumps({"version": actual, "releasedAt": base.get("releasedAt"),
                                     "note": "Línea base de la última publicación. La escribe scripts/ds-release.py --apply.",
                                     "state": ahora}, ensure_ascii=False, indent=2) + "\n")
            print("Línea base renovada al formato 12.0.0 (misma versión %s): nada que publicar." % actual)
            return 0
        print("Nada que publicar." + ("  (línea base en formato anterior: publica con --apply para renovarla)" if legacy else ""))
        return 0
    print("Versión propuesta: %s" % nueva)

    fecha = datetime.date.today().isoformat()
    entrada = notes(nueva, fecha, nivel, d, pendientes)

    if not a.apply:
        print("\n--- borrador de la entrada del CHANGELOG (no se ha escrito nada) ---\n")
        print(entrada)
        print("Para publicarla de verdad: python3 scripts/ds-release.py --apply")
        return 0

    man["version"], man["versionedAt"] = nueva, fecha
    with open(mpath, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(man, ensure_ascii=False, indent=2) + "\n")

    cpath = os.path.join(ds, "CHANGELOG.md")
    prev = open(cpath, encoding="utf-8").read() if os.path.exists(cpath) else ""
    marca = "> ⬜ Sin publicaciones todavía."
    if marca in prev:
        prev = prev[:prev.index(marca)].rstrip() + "\n"
    cab, _, cuerpo = prev.partition("\n## ")
    nuevo = cab.rstrip() + "\n\n" + entrada.rstrip() + ("\n\n## " + cuerpo if cuerpo else "\n")
    with open(cpath, "w", encoding="utf-8") as fh:
        fh.write(nuevo)

    os.makedirs(os.path.dirname(bpath), exist_ok=True)
    with open(bpath, "w", encoding="utf-8") as fh:
        fh.write(json.dumps({"version": nueva, "releasedAt": fecha,
                             "note": "Línea base de la última publicación. La escribe scripts/ds-release.py --apply.",
                             "state": ahora}, ensure_ascii=False, indent=2) + "\n")
    print("\nPublicado %s · CHANGELOG.md y línea base actualizados." % nueva)
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from activity import log
        log(root, "script", "ds-release", "publicada la versión %s del design system (salto %s)" % (nueva, NOMBRE[nivel]))
    except Exception:
        pass
    if d["quitados"]:
        print("⬜ Rellena la ruta de actualización en la entrada del CHANGELOG antes del commit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
