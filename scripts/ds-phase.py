#!/usr/bin/env python3
"""
ds-phase.py — responde a una sola pregunta: ¿puedo empezar esta fase?

El plugin ya es una cadena de fases con dependencias reales —la tipografía es puerta previa a
los componentes, las pantallas no se montan sin tokens ni contratos—, pero esas puertas viven
en prosa y las cumple quien se acuerda. Este script las comprueba contra los archivos.

**No es un motor.** No ejecuta nada, no guarda estado entre sesiones y no decide por ti. Mira
el proyecto, evalúa las condiciones declaradas en governance/phases.json y dice qué se puede
empezar y qué no, con el motivo. Las condiciones no son nuevas: son las que SKILL.md y
design.md ya declaran.

Uso:  python3 scripts/ds-phase.py [--root .] [--phase <id>] [--json]
      sin --phase, evalúa todas y dice por dónde se puede seguir
      --phase ui   evalúa solo esa y sale con 1 si no se puede empezar
Sin dependencias: solo biblioteca estándar.
"""

import argparse
import json
import os
import re
import sys


def jload(p, d=None):
    try:
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return d


def texto(p):
    try:
        return open(p, encoding="utf-8").read()
    except Exception:
        return ""


class Proyecto:
    """Cada condición es una pregunta sobre los archivos, no sobre lo que alguien recuerde."""

    def __init__(self, root):
        self.root = root
        self.ds = os.path.join(root, "design-system")
        self.ctx = os.path.join(root, "context")
        self.tokens = jload(os.path.join(self.ds, "tokens", "tokens.json"), {}) or {}
        self.manifest = jload(os.path.join(self.ds, "agent-manifest.json"), {}) or {}
        self.modules = jload(os.path.join(root, "governance", "modules.json"), {}) or {}

    def _todos_los_tokens(self):
        for col in (self.tokens.get("collections") or {}).values():
            for t in (col.get("tokens") or {}).values():
                yield t

    # --- condiciones ---
    def _activo(self, mid):
        m = (self.modules.get("modules") or {}).get(mid) or {}
        return m.get("active") is not False

    def scaffolding_completo(self):
        obligatorias = ["context", "scripts", "governance"]
        if self._activo("investigacion"):
            obligatorias += ["research", "analytics"]
        if self._activo("estrategia"):
            obligatorias += ["UX"]
        if self._activo("design-system"):
            obligatorias += ["design-system", "UI"]
        faltan = [r for r in obligatorias if not os.path.isdir(os.path.join(self.root, r))]
        if faltan:
            return False, "faltan carpetas del scaffolding: " + ", ".join(faltan)
        return True, "la estructura está"

    def fuentes_figma_registradas(self):
        f = self.manifest.get("figmaSources")
        return (bool(f), "fuentes registradas" if f else
                "no hay ninguna fuente de Figma en agent-manifest.json")

    def tokens_sincronizados(self):
        n = sum(1 for _ in self._todos_los_tokens())
        return (n > 0, "%d tokens sincronizados" % n if n else
                "tokens.json está vacío: falta el primer sync desde Figma")

    def tipografia_aprobada(self):
        """Vale cualquiera de las dos formas de definir la tipografía en Figma.

        Por variables: hay variables de familia y de tamaño. Por estilos de texto, que es lo más
        habitual: algún estilo con familia y al menos dos tamaños distintos (una escala)."""
        nombres = [str(t.get("path", "")).lower() for t in self._todos_los_tokens()]
        fam = any("family" in n or "font" in n for n in nombres)
        tam = any(n.startswith("size/") or "/size" in n for n in nombres)
        if fam and tam:
            return True, "hay familia y escala de tamaños en variables"
        estilos = self.tokens.get("textStyles") or []
        con_familia = [s for s in estilos if s.get("fontFamily")]
        tamanos = {s.get("fontSize") for s in estilos if isinstance(s.get("fontSize"), (int, float))}
        if con_familia and len(tamanos) >= 2:
            return True, "hay %d estilos de texto con %d tamaños distintos" % (len(estilos), len(tamanos))
        falta = [x for x, ok in (("familia tipográfica", fam or bool(con_familia)),
                                 ("escala de tamaños", tam or len(tamanos) >= 2)) if not ok]
        return False, ("falta " + " y ".join(falta) + " en variables o en estilos de texto "
                       "(design.md: la tipografía es puerta previa a los componentes)")

    def direccion_visual_escrita(self):
        t = texto(os.path.join(self.root, "UX", "direction", "DESIGN.md"))
        if not t:
            return False, "no existe UX/direction/DESIGN.md"
        pend = t.count("⬜ TODO")
        return (pend == 0, "escrita" if pend == 0 else
                "quedan %d apartados en TODO: se pide referencias antes de proponer estilo" % pend)

    def algun_contrato_de_componente(self):
        d = os.path.join(self.ds, "schemas", "components")
        n = len([f for f in os.listdir(d) if f.endswith(".schema.json")]) if os.path.isdir(d) else 0
        return (n > 0, "%d contratos" % n if n else
                "no hay ningún contrato de componente: las pantallas consumen, no definen")

    def composicion_documentada(self):
        t = texto(os.path.join(self.ds, "docs", "patterns.md"))
        if "## Composición de pantalla" not in t:
            return False, "patterns.md no tiene la sección de Composición de pantalla"
        bloque = t.split("## Composición de pantalla", 1)[1][:4000]
        pend = bloque.count("⬜ TODO")
        return (pend == 0, "reglas de composición escritas" if pend == 0 else
                "quedan %d reglas de composición en TODO" % pend)

    def flujos_definidos(self):
        t = texto(os.path.join(self.ctx, "user-flow.md"))
        if not t:
            return False, "no existe context/user-flow.md"
        pend = t.count("⬜ TODO")
        return (pend == 0, "flujos escritos" if pend == 0 else
                "user-flow.md tiene %d apartados en TODO" % pend)

    def auditorias_en_cero(self):
        malos = []
        for rel, clave in ((os.path.join(self.ds, "reports", "token-audit.json"), "errors"),
                           (os.path.join(self.ctx, "reports", "context-audit.json"), "errors")):
            d = jload(rel)
            if d is None:
                malos.append("falta " + os.path.relpath(rel, self.root))
                continue
            e = d.get(clave)
            n = len(e) if isinstance(e, list) else (e or 0)
            if n:
                malos.append("%s: %s errores" % (os.path.basename(rel), n))
        return (not malos, "las auditorías pasan" if not malos else "; ".join(malos))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--phase", default=None, help="evalúa solo esta fase y sale con 1 si no se puede empezar")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    root = os.path.abspath(a.root)

    decl = jload(os.path.join(root, "governance", "phases.json"))
    if not decl:
        sys.exit("[ERROR] falta governance/phases.json")
    pr = Proyecto(root)

    out, bloqueadas = [], 0
    for f in decl.get("phases") or []:
        mod = f.get("module")
        if mod and not pr._activo(mod):
            out.append({"id": f["id"], "title": f.get("title"), "canStart": None,
                        "blockedBy": ["el módulo '%s' no está activo en este proyecto" % mod],
                        "why": f.get("why")})
            continue
        motivos, no_aplica, puede = [], [], True
        for cond in f.get("requires") or []:
            # Una condición puede ser un id o {"id", "module"}: si su módulo está apagado, no aplica
            cmod = cond.get("module") if isinstance(cond, dict) else None
            cond = cond.get("id") if isinstance(cond, dict) else cond
            if cmod and not pr._activo(cmod):
                no_aplica.append("%s: no aplica, el módulo '%s' está apagado" % (cond, cmod))
                continue
            fn = getattr(pr, cond.replace("-", "_"), None)
            if fn is None:
                puede = False; motivos.append("condición '%s' sin comprobación implementada" % cond)
                continue
            ok, por = fn()
            if not ok:
                puede = False; motivos.append(por)
        out.append({"id": f["id"], "title": f.get("title"), "canStart": puede,
                    "blockedBy": motivos, "notApplicable": no_aplica, "why": f.get("why")})
        if not puede:
            bloqueadas += 1

    if a.json:
        print(json.dumps({"phases": out}, ensure_ascii=False, indent=2))
    elif a.phase:
        sel = [x for x in out if x["id"] == a.phase]
        if not sel:
            sys.exit("[ERROR] no existe la fase '%s'. Hay: %s" % (a.phase, ", ".join(x["id"] for x in out)))
        x = sel[0]
        if x["canStart"] is None:
            print("– «%s» no aplica: %s." % (x["title"], x["blockedBy"][0]))
            return 0
        print(("✔ Puedes empezar «%s»." % x["title"]) if x["canStart"] else
              ("✘ Todavía no puedes empezar «%s»." % x["title"]))
        for m in x["blockedBy"]:
            print("   falta: %s" % m)
        for m in x.get("notApplicable") or []:
            print("   – %s" % m)
        if not x["canStart"] and x.get("why"):
            print("   por qué existe esta puerta: %s" % x["why"])
        return 0 if x["canStart"] else 1
    else:
        for x in out:
            m = {True: "✔", False: "✘", None: "–"}[x["canStart"]]
            print("  %s %-26s %s" % (m, x["id"], "" if x["canStart"] else "← " + x["blockedBy"][0]))
        listas = [x["id"] for x in out if x["canStart"] is True]
        print("\nPuedes empezar: %s" % (", ".join(listas) if listas else "nada todavía"))
        if bloqueadas:
            print("Bloqueadas: %d. `--phase <id>` dice exactamente qué falta y por qué existe esa puerta." % bloqueadas)
    return 0


if __name__ == "__main__":
    sys.exit(main())
