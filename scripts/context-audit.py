#!/usr/bin/env python3
"""context-audit — hace cumplir las reglas de `context/` que se pueden comprobar sin criterio humano.

Sin dependencias (solo stdlib, Python 3.8+). Uso:
    python3 scripts/context-audit.py                 # audita según scripts/context-audit.config.json
    python3 scripts/context-audit.py --json          # salida JSON por stdout
    python3 scripts/context-audit.py --out context/reports/context-audit.json   # guarda el JSON
    python3 scripts/context-audit.py --root .        # raíz del proyecto (por defecto: carpeta padre de scripts/)

Código de salida: 1 si hay algún ERROR; 0 si solo hay avisos o nada. Se ejecuta antes de cada
commit (ver AGENTS.md) y en CI. Si falla, se restaura la sección que falta en el documento de
`context/`; nunca el script ni su config.

Es el hermano de `token-audit.py`: aquel audita el diseño visual y el design system (valores
crudos, estructura cerrada, showcase, transparencias); este audita los documentos funcionales.
Se separaron porque compartían código de salida: un `## Estados` ausente en `user-flow.md`
bloqueaba un commit de design system que no tenía nada que ver. Cada uno falla por lo suyo.

Qué comprueba:
  1. Documentos obligatorios (config → docs): los archivos de `context/` que el scaffolding
     crea deben existir. Si falta uno, ERROR.
  2. Secciones obligatorias (config → docs): cada documento debe conservar los encabezados y
     referencias con los que nació (regla 6 de context/AGENTS.md: se puede añadir una sección,
     no quitar una). Son las que la auditoría comprueba y las que otras carpetas enlazan.
     Un encabezado se busca al principio de línea y admite cola descriptiva, pero la cola no
     puede continuar la palabra. Si falta una, ERROR.
  3. Integridad referencial de objetivos: ningún documento de `context/` cita un `OBJ-` o un
     `M-` que no esté definido en `context/objectives.md`. Si lo cita, ERROR.

Lo que no está activo no se exige: los documentos que pertenecen a un módulo apagado en
`governance/modules.json` (casi todos son de `estrategia`) no se comprueban, ni tampoco las
referencias a `objectives.md` si ese documento está apagado. Sin modules.json se exige todo.
"""
import argparse
import datetime
import glob
import json
import os
import re
import sys

# Un identificador queda DEFINIDO cuando abre una fila de tabla en objectives.md
# (`| OBJ-01 | …`). Citado, cuando aparece en cualquier documento de context/.
DEFINED_RE = re.compile(r"^\|\s*((?:OBJ|M)-\d+)\s*\|", re.M)
CITED_RE = re.compile(r"\b((?:OBJ|M)-\d+)\b")
OBJECTIVES = "context/objectives.md"

DEFAULT_DOCS = {
    "context/AGENTS.md": ["## Enrutado", "## Reglas duras", "## Distribución", "## Cambios",
                          "## Marcadores"],
    "context/project-context.md": ["## Qué es", "## Problema actual", "## Qué debe permitir",
                                   "## Usuarios", "## Alcance"],
    "context/proposal-agreements.md": ["## Fuente", "## Entregables", "## Qué entra y qué no",
                                       "## Responsabilidades y dependencias", "## Research acordado",
                                       "## Restricciones del encargo", "## Cómo se cambia lo acordado",
                                       "## Registro de cambios"],
    "context/users.md": ["## Perfiles", "## Roles y permisos"],
    "context/business-rules.md": ["## Reglas generales", "## Reglas por área", "## Condiciones y límites"],
    "context/glossary.md": ["## Términos"],
    "context/data-model.md": ["## Entidades principales"],
    "context/user-flow.md": ["## Pantallas", "## Estados"],
    "context/synthesis.md": ["## Hallazgos", "## Touchpoints", "## Features", "## User stories"],
    "context/objectives.md": ["## Objetivos", "## Métricas", "## Fuera de objetivo"],
    "context/specs.md": ["Origen"],
}


def rutas_apagadas(root):
    """Rutas de los módulos apagados (`active: false`) según governance/modules.json.

    Lo que no está activo no se exige. Mismo criterio que `modulo_activo()` de token-audit:
    solo cuenta como apagado lo que dice `false`; sin declaración de módulos (proyectos
    anteriores a la 10.0.0) o si el archivo no se puede leer, no se apaga nada y se exige todo,
    como antes. Las rutas salen del propio modules.json, no de una segunda lista escrita aquí.
    """
    try:
        with open(os.path.join(root, "governance", "modules.json"), encoding="utf-8") as fh:
            mods = json.load(fh).get("modules") or {}
    except Exception:
        return []
    return [r for m in mods.values() if m.get("active") is False for r in (m.get("paths") or [])]


def apagada(rel, rutas):
    """¿Pertenece `rel` a alguna ruta apagada? Una ruta acabada en / cubre todo lo que cuelga."""
    return any(rel == r.rstrip("/") or (r.endswith("/") and rel.startswith(r)) for r in rutas)


def load_config(cfg_path):
    cfg = {"docs": dict(DEFAULT_DOCS)}
    if cfg_path and os.path.exists(cfg_path):
        with open(cfg_path, encoding="utf-8") as fh:
            user = json.load(fh)
        for k, v in user.items():
            if k == "docs" and isinstance(v, dict):
                cfg["docs"].update(v)
            else:
                cfg[k] = v
    return cfg


def section_missing(text, needle):
    """¿Falta en `text` la sección o referencia `needle`?

    Un **encabezado** (empieza por `#`) se busca al principio de una línea y admite cola
    descriptiva, porque las plantillas la llevan a propósito: el contrato pide
    `## Enrutado` y el documento escribe `## Enrutado — qué documento abrir según la
    petición`. Lo que no vale es que la cola continúe la palabra: `## Estados` no lo
    cumple `## EstadosRenombrado` ni `## Objetivos`, que son encabezados distintos
    (regla 6 de `context/AGENTS.md`: los encabezados de plantilla no se renombran).
    Por eso tras el encabezado tiene que venir fin de línea o un carácter que no sea
    alfanumérico.

    Las **referencias que no son encabezados** (rutas del showcase, «Ejemplo de código»)
    se buscan como subcadena en todo el texto: aparecen dentro de una línea, no como línea.
    """
    if not needle.startswith("#"):
        return needle not in text
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith(needle):
            continue
        rest = line[len(needle):]
        if not rest or not rest[0].isalnum():
            return False
    return True


class Audit:
    def __init__(self, cfg, root):
        self.cfg, self.root, self.findings = cfg, root, []
        apagadas = rutas_apagadas(root)
        self.omitidos = sorted(r for r in (cfg.get("docs") or {}) if apagada(r, apagadas))
        # Los documentos que se comprueban: los del config menos los de módulos apagados
        self.docs_activos = {r: n for r, n in (cfg.get("docs") or {}).items() if r not in self.omitidos}
        self.objetivos_apagados = apagada(OBJECTIVES, apagadas)

    def add(self, severity, file, line, prop, value, suggestion):
        self.findings.append({"severity": severity, "file": file, "line": line,
                              "property": prop, "value": value, "suggestion": suggestion})

    def docs(self):
        for rel, needles in self.docs_activos.items():
            path = os.path.join(self.root, rel)
            if not os.path.exists(path):
                self.add("error", rel, 0, "estructura", "falta", "archivo obligatorio del scaffolding: no existe")
                continue
            text = open(path, encoding="utf-8").read()
            for n in needles:
                if section_missing(text, n):
                    self.add("error", rel, 0, "secciones", n,
                             "sección o referencia obligatoria ausente: restaura la plantilla de la skill (no la borres al editar)")


    def vigencia(self):
        """Avisa de los documentos cuya última confirmación ha caducado.

        No comprueba que el contenido sea correcto —eso no lo puede hacer un script—, solo que
        alguien lo haya mirado dentro del plazo. Es AVISO, nunca error: un documento sin
        reconfirmar no es un defecto de lo que se está commiteando, y bloquear por eso sería
        desproporcionado.

        Distinción que importa: las reglas de PROPIEDAD no caducan (un identificador no cambia
        de naturaleza); las de DECISIÓN sí, porque dependen de condiciones que se midieron en
        un momento dado. El plazo se aplica al documento entero como aproximación barata.
        """
        meses = int((self.cfg.get("vigencia") or {}).get("mesesPlazo", 6))
        hoy = datetime.date.today()
        exentos = set((self.cfg.get("vigencia") or {}).get("exentos") or ())
        for rel in sorted(self.docs_activos):
            if os.path.basename(rel) in exentos:
                continue  # las normas no caducan: son reglas de propiedad, no de decisión
            path = os.path.join(self.root, rel)
            if not os.path.exists(path):
                continue
            cab = open(path, encoding="utf-8").read()[:900]
            if "<!-- vigencia" not in cab:
                self.add("warn", rel, 0, "vigencia", "sin cabecera",
                         "el documento no declara autoridad ni fecha de confirmación: "
                         "restaura la cabecera de vigencia de la plantilla")
                continue
            m = re.search(r"confirmado:\s*(\d{4}-\d{2}-\d{2})", cab)
            if not m:
                # pendiente de confirmar es el estado normal de un proyecto recién creado
                continue
            try:
                fecha = datetime.date.fromisoformat(m.group(1))
            except ValueError:
                self.add("warn", rel, 0, "vigencia", m.group(1), "la fecha de confirmación no es ISO")
                continue
            dias = (hoy - fecha).days
            if dias > meses * 30:
                self.add("warn", rel, 0, "vigencia", m.group(1),
                         "confirmado hace %d días (plazo: %d meses). Que alguien con autoridad "
                         "diga si sigue siendo verdad y actualice la fecha" % (dias, meses))

    def references(self):
        """Ningún documento cita un OBJ-/M- que no exista en objectives.md.

        Es el equivalente para objetivos de lo que research-index.py hace con `R-… §O-n`:
        una referencia rota no se ve leyendo, y convierte una tabla en decoración. Sobre el
        scaffolding recién creado no hay nada definido todavía (las plantillas citan
        `OBJ-…` con puntos suspensivos, que no es un identificador) y el check no aplica.
        """
        obj_path = os.path.join(self.root, OBJECTIVES)
        if self.objetivos_apagados or not os.path.exists(obj_path):
            return
        defined = set(DEFINED_RE.findall(open(obj_path, encoding="utf-8").read()))
        if not defined:
            return
        for path in sorted(glob.glob(os.path.join(self.root, "context", "*.md"))):
            rel = os.path.relpath(path, self.root)
            for i, line in enumerate(open(path, encoding="utf-8").read().splitlines(), 1):
                for ref in CITED_RE.findall(line):
                    if ref not in defined:
                        self.add("error", rel, i, "referencias", ref,
                                 f"no existe en {OBJECTIVES}: defínelo ahí o corrige la cita "
                                 f"(los identificadores no se renumeran; lo retirado se marca, no se borra)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=None, help="raíz del proyecto")
    ap.add_argument("--config", default=None, help="ruta al config JSON")
    ap.add_argument("--json", action="store_true", help="salida JSON por stdout")
    ap.add_argument("--out", default=None, help="guardar el informe JSON en esta ruta (relativa a la raíz)")
    args = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(args.root or os.path.dirname(here))
    cfg = load_config(args.config or os.path.join(here, "context-audit.config.json"))
    audit = Audit(cfg, root)
    audit.docs()
    audit.vigencia()
    audit.references()

    findings = sorted(audit.findings, key=lambda x: (x["file"], x["line"]))
    errors = [x for x in findings if x["severity"] == "error"]
    warns = [x for x in findings if x["severity"] == "warn"]
    by_prop = {}
    for x in errors:
        by_prop[x["property"]] = by_prop.get(x["property"], 0) + 1
    report = {"root": root, "errors": len(errors), "warnings": len(warns), "errorsByProperty": by_prop,
              "docsChecked": len(audit.docs_activos), "docsSkipped": audit.omitidos, "findings": findings}
    if args.out:
        out_path = os.path.join(root, args.out)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(report, fh, ensure_ascii=False, indent=2)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for x in findings:
            print(f"{x['file']}:{x['line']}: [{x['severity'].upper()}] {x['property']}: {x['value']} → {x['suggestion']}")
        print(f"\n{len(errors)} errores · {len(warns)} avisos · documentos comprobados: {report['docsChecked']}")
        if audit.omitidos:
            print(f"No se exigen {len(audit.omitidos)} documentos de módulos apagados (governance/modules.json)")
        if by_prop:
            print("Errores por propiedad: " + ", ".join(f"{k} {v}" for k, v in sorted(by_prop.items(), key=lambda kv: -kv[1])))
        if errors:
            print("Restaura la sección que falta en su documento de context/; nunca el script ni su config.")
        print("Alcance: esta auditoría comprueba que los documentos existan y conserven sus secciones; no comprueba que su contenido sea cierto ni que el DS sea fiel a Figma (ver scripts/ds-fidelity.py).")
        if args.out:
            print(f"Informe guardado en {args.out}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
