#!/usr/bin/env python3
"""
tokens-dtcg.py — exporta los tokens del design system al formato del Design Tokens Community
Group (borrador «Design Tokens Format Module», el que suele llamarse «el estándar W3C de tokens»).

Fuente:  design-system/tokens/tokens.json   (espejo de Figma que genera scripts/ds-sync.py)
Salida:  design-system/tokens/w3c/*.tokens.json + manifest.json

NO es fuente de verdad. Figma manda, tokens.json es su espejo y esto es un espejo de segundo
nivel para herramientas externas (Style Dictionary, Tokens Studio, importadores). El código
del proyecto sigue consumiendo `var(--token)` de tokens.css.

El formato DTCG no define modos. Se resuelve con la convención del ecosistema: cada modo es
un archivo y el consumidor combina. Cada colección de Figma con más de un modo se convierte
en un eje; `manifest.json` declara los ejes y todas las combinaciones válidas.

Esta exportación es OPCIONAL y está desactivada por defecto. Se decide al arrancar el
proyecto y queda registrada en design-system/agent-manifest.json → exports.dtcg.enabled.
Mientras esté en false, el script NO escribe nada: avisa y sale. Activarla más adelante exige
consentimiento explícito de la persona usuaria y se hace con --enable.

Uso:  python3 scripts/tokens-dtcg.py [--root .] [--check] [--enable]
      --check   no escribe; sale con código 1 si la salida en disco está desactualizada.
      --plan    NO escribe nada: imprime la lista exacta de archivos que crearía y cuántos
                tokens lleva cada uno. Es el texto que se le enseña a la persona para pedirle
                permiso. El resumen lo genera el código, no el agente: si lo redactara un
                modelo podría describir algo distinto de lo que se ejecuta.
      --enable  registra el consentimiento en agent-manifest.json y genera. Solo después de
                enseñar la salida de --plan y obtener un sí explícito contra esa lista.
Sin dependencias externas: solo biblioteca estándar.
"""

import argparse
import itertools
import json
import os
import re
import sys

VENDOR = "org.designsystem"          # clave de $extensions (namespace propio del proyecto)
UNITLESS_SEGMENTS = {"lh", "line-height", "lineheight", "opacity", "opacidad",
                     "z-index", "zindex", "ratio", "scale", "multiplier"}
DIMENSION_SCOPES = {"CORNER_RADIUS", "WIDTH_HEIGHT", "GAP", "STROKE_FLOAT", "FONT_SIZE",
                    "LETTER_SPACING", "PARAGRAPH_SPACING", "PARAGRAPH_INDENT"}
NUMBER_SCOPES = {"OPACITY", "LINE_HEIGHT"}
TIME_HINTS = ("duration", "duracion", "duración", "delay", "transition", "motion/time")
FAMILY_HINTS = ("family", "familia", "font-family", "fontfamily", "typeface")
WEIGHT_HINTS = ("weight", "peso")
NAMED_WEIGHTS = {
    "thin": 100, "extra-light": 200, "extralight": 200, "ultra-light": 200, "light": 300,
    "regular": 400, "normal": 400, "book": 400, "medium": 500, "semi-bold": 600,
    "semibold": 600, "demi-bold": 600, "bold": 700, "extra-bold": 800, "extrabold": 800,
    "ultra-bold": 800, "black": 900, "heavy": 900,
}


def slug(s):
    s = re.sub(r"[^a-z0-9]+", "-", str(s).strip().lower())
    return re.sub(r"-{2,}", "-", s).strip("-") or "default"


def dtcg_path(figma_path):
    """`action/primary/fill` → ('action', 'primary', 'fill'). Los nombres DTCG no admiten `.` ni `{}`."""
    parts = [p.strip() for p in str(figma_path).split("/") if p.strip()]
    return tuple(re.sub(r"[.${}]", "-", p) for p in parts) or ("unnamed",)


def hex_components(hx):
    hx = hx.lstrip("#")
    if len(hx) in (3, 4):
        hx = "".join(c * 2 for c in hx)
    comps = [round(int(hx[i:i + 2], 16) / 255, 6) for i in (0, 2, 4)]
    alpha = round(int(hx[6:8], 16) / 255, 6) if len(hx) == 8 else None
    return comps, alpha


def parse_color(raw):
    raw = str(raw).strip()
    m = re.fullmatch(r"#([0-9a-fA-F]{3,8})", raw)
    if m:
        comps, alpha = hex_components(raw)
        v = {"colorSpace": "srgb", "components": comps}
        if alpha is not None and alpha < 1:
            v["alpha"] = alpha
        else:
            v["hex"] = "#%02x%02x%02x" % tuple(round(c * 255) for c in comps)
        return v
    m = re.fullmatch(r"rgba?\(([^)]+)\)", raw)
    if m:
        nums = [p.strip() for p in re.split(r"[ ,/]+", m.group(1)) if p.strip()]
        comps = [round(float(n.rstrip("%")) / (100 if n.endswith("%") else 255), 6) for n in nums[:3]]
        v = {"colorSpace": "srgb", "components": comps}
        if len(nums) > 3:
            v["alpha"] = round(float(nums[3].rstrip("%")) / (100 if nums[3].endswith("%") else 1), 6)
        return v
    return None


def token_type_value(tok, raw):
    """Devuelve ($type, $value) o (None, None) si el token no tiene equivalente DTCG."""
    name = str(tok.get("path", "")).lower()
    ftype = str(tok.get("type", "")).upper()
    raw = "" if raw is None else str(raw).strip()

    if ftype == "COLOR":
        return ("color", parse_color(raw)) if parse_color(raw) else (None, None)

    if ftype == "FLOAT":
        m = re.fullmatch(r"(-?\d+(?:\.\d+)?)\s*(px|rem|ms|s)?", raw)
        if not m:
            return (None, None)
        n = float(m.group(1))
        n = int(n) if n.is_integer() else n
        unit = m.group(2)
        scopes = set(tok.get("scopes") or [])
        segments = {s.strip() for s in name.split("/")}
        if unit in ("ms", "s") or any(h in name for h in TIME_HINTS):
            return "duration", {"value": n, "unit": unit if unit in ("ms", "s") else "ms"}
        if "FONT_WEIGHT" in scopes or segments & set(WEIGHT_HINTS):
            return "fontWeight", int(n)
        if scopes & NUMBER_SCOPES or segments & UNITLESS_SEGMENTS:
            return "number", n
        if unit in ("px", "rem"):
            return "dimension", {"value": n, "unit": unit}
        if scopes & DIMENSION_SCOPES:
            return "dimension", {"value": n, "unit": "px"}
        # Sin unidad, sin scope y sin pista de nombre: un decimal es una razón, un entero una medida.
        return ("number", n) if not float(n).is_integer() else ("dimension", {"value": n, "unit": "px"})

    if ftype == "STRING":
        if any(h in name for h in FAMILY_HINTS):
            fams = [p.strip().strip('"\'') for p in raw.split(",") if p.strip()]
            return "fontFamily", (fams if len(fams) > 1 else fams[0] if fams else raw)
        if {s.strip() for s in name.split("/")} & set(WEIGHT_HINTS):
            key = slug(raw)
            return "fontWeight", NAMED_WEIGHTS.get(key, raw)
        return (None, None)

    return (None, None)


def insert(tree, path, node):
    cur = tree
    for seg in path[:-1]:
        cur = cur.setdefault(seg, {})
        if "$value" in cur:
            raise ValueError("colisión: un token es también grupo en %s" % "/".join(path))
    cur[path[-1]] = node


class Exporter:
    def __init__(self, root):
        self.root = root
        src = os.path.join(root, "design-system", "tokens", "tokens.json")
        if not os.path.exists(src):
            sys.exit("[ERROR] no existe %s — corre antes scripts/ds-sync.py" % os.path.relpath(src, root))
        with open(src, encoding="utf-8") as fh:
            self.raw = json.load(fh)
        self.out = os.path.join(root, "design-system", "tokens", "w3c")
        self.skipped, self.gaps = [], []
        self.by_cssvar = {}
        for col in (self.raw.get("collections") or {}).values():
            for t in (col.get("tokens") or {}).values():
                if t.get("cssVar"):
                    self.by_cssvar[t["cssVar"]] = ".".join(dtcg_path(t["path"]))

    def node(self, tok, mode_name):
        modes = tok.get("modes") or {}
        entry = modes.get(mode_name) or {}
        alias = entry.get("alias") or (tok.get("alias") if not modes else None)
        if alias:
            ref = self.by_cssvar.get(alias)
            if not ref:
                self.skipped.append("%s: alias a %s, que no está en tokens.json" % (tok.get("path"), alias))
                return None
            node = {"$value": "{%s}" % ref}   # $type se hereda del token referenciado
        else:
            raw = entry.get("value") if entry.get("value") is not None else entry.get("resolvedValue")
            if raw is None and not modes:
                raw = tok.get("value") if tok.get("value") is not None else tok.get("resolvedValue")
            if raw is None:
                self.gaps.append("%s: sin valor en el modo «%s»" % (tok.get("path"), mode_name))
                return None
            ttype, tvalue = token_type_value(tok, raw)
            if ttype is None:
                self.skipped.append("%s: tipo %s sin equivalente DTCG (valor %r)" % (tok.get("path"), tok.get("type"), raw))
                return None
            node = {"$value": tvalue, "$type": ttype}
        desc = tok.get("description")
        if desc and desc != "unknown":
            node["$description"] = desc
        ext = {"figmaVariable": tok.get("path"), "cssVariable": "var(%s)" % tok["cssVar"] if tok.get("cssVar") else None}
        if tok.get("scopes"):
            ext["figmaScopes"] = tok["scopes"]
        src = tok.get("source") or {}
        if src.get("variableId"):
            ext["figmaVariableId"] = src["variableId"]
        node["$extensions"] = {VENDOR: {k: v for k, v in ext.items() if v is not None}}
        return node

    def build(self):
        base, axes, files = {}, {}, {}
        for col_name, col in (self.raw.get("collections") or {}).items():
            modes = col.get("modes") or ["Default"]
            toks = list((col.get("tokens") or {}).values())
            if not toks:
                continue
            if len(modes) <= 1:
                for t in toks:
                    n = self.node(t, modes[0] if modes else "Default")
                    if n:
                        insert(base, dtcg_path(t["path"]), n)
                continue
            axis = slug(col_name)
            axes[axis] = {}
            names_by_mode = {}
            for mode in modes:
                tree = {}
                names = []
                for t in toks:
                    n = self.node(t, mode)
                    if n:
                        insert(tree, dtcg_path(t["path"]), n)
                        names.append(".".join(dtcg_path(t["path"])))
                fname = "%s.%s.tokens.json" % (axis, slug(mode))
                files[fname] = self.wrap(tree, "Colección «%s», modo «%s»." % (col_name, mode))
                axes[axis][slug(mode)] = fname
                names_by_mode[mode] = set(names)
            ref = names_by_mode[modes[0]]
            for mode in modes[1:]:
                for miss in sorted(ref - names_by_mode[mode]):
                    self.gaps.append("%s: «%s» existe en «%s» y falta en «%s»" % (col_name, miss, modes[0], mode))

        files["base.tokens.json"] = self.wrap(base, "Colecciones de un solo modo.")
        combos = {}
        keys = sorted(axes)
        for picks in itertools.product(*[sorted(axes[k]) for k in keys]) if keys else [()]:
            label = "-".join(picks) if picks else "base"
            combos[label] = ["base.tokens.json"] + [axes[keys[i]][p] for i, p in enumerate(picks)]
        files["manifest.json"] = {
            "$description": self.header(),
            "name": "%s Design Tokens" % self.raw.get("designSystem", "unknown"),
            "format": "DTCG · Design Tokens Format Module (borrador del Design Tokens Community Group)",
            "generator": "scripts/tokens-dtcg.py",
            "source": {"mirror": "design-system/tokens/tokens.json", "figmaSources": self.raw.get("figmaSources"),
                       "lastSync": self.raw.get("lastSync")},
            "note": ("El formato DTCG no define modos. Cada modo es un archivo; combina siempre "
                     "base.tokens.json más un archivo por eje antes de resolver los alias."),
            "axes": axes,
            "combinations": combos,
        }
        return files

    def header(self):
        return ("Espejo DTCG generado por scripts/tokens-dtcg.py. NO editar a mano. "
                "Fuente de verdad: Figma → design-system/tokens/tokens.json → este archivo.")

    def wrap(self, tree, note):
        return {"$description": self.header() + " " + note, **tree}

    # --- Nivel 2 de validación: ejecutabilidad ---------------------------------------------
    def resolver(self, files):
        """Que un archivo esté bien formado no significa que se pueda usar. Comprueba que en
        cada combinación declarada todo alias resuelve hasta un valor concreto, sin referencias
        colgando ni ciclos. Devuelve la lista de problemas; vacía = la exportación es usable."""
        def plano(nodo, prefijo=()):
            for k, v in nodo.items():
                if k.startswith("$"):
                    continue
                if isinstance(v, dict) and "$value" in v:
                    yield ".".join(prefijo + (k,)), v
                elif isinstance(v, dict):
                    for x in plano(v, prefijo + (k,)):
                        yield x

        problemas = []
        combos = (files.get("manifest.json") or {}).get("combinations") or {}
        for nombre, archivos in combos.items():
            tabla = {}
            for f in archivos:
                tabla.update(dict(plano(files.get(f) or {})))
            for clave, tok in tabla.items():
                visto, actual = [], tok
                while True:
                    v = actual.get("$value")
                    if not (isinstance(v, str) and v.startswith("{") and v.endswith("}")):
                        break
                    ref = v[1:-1]
                    if ref in visto:
                        problemas.append("%s · %s: ciclo de alias en %s" % (nombre, clave, ref))
                        break
                    if ref not in tabla:
                        problemas.append("%s · %s: apunta a %s, que no existe en esa combinación"
                                         % (nombre, clave, ref))
                        break
                    visto.append(ref)
                    actual = tabla[ref]
        return problemas

    def run(self, check):
        files = self.build()

        colgando = self.resolver(files)
        if colgando:
            for c in colgando[:10]:
                print("[ERROR] exportación no usable: %s" % c)
            if len(colgando) > 10:
                print("[ERROR] … y %d más" % (len(colgando) - 10))
            print("\nNo se ha escrito nada. Un alias que no resuelve describe un hueco del DS "
                  "real: se corrige en Figma y se vuelve a sincronizar.")
            return 1

        payload = {n: json.dumps(c, ensure_ascii=False, indent=2) + "\n" for n, c in files.items()}
        rel = os.path.relpath(self.out, self.root)

        if check:
            stale = [n for n, t in payload.items()
                     if not os.path.exists(os.path.join(self.out, n))
                     or open(os.path.join(self.out, n), encoding="utf-8").read() != t]
            for n in stale:
                print("DESACTUALIZADO: %s/%s" % (rel, n))
            self.report()
            return 1 if stale else 0

        os.makedirs(self.out, exist_ok=True)
        for n, t in payload.items():
            with open(os.path.join(self.out, n), "w", encoding="utf-8") as fh:
                fh.write(t)
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from activity import log
            log(self.root, "script", "tokens-dtcg", "exportación a formato de terceros regenerada",
                files=[os.path.join(rel, n) for n in payload])
        except Exception:
            pass
        for n in sorted(payload):
            if n != "manifest.json":
                print("  %-38s %3d tokens" % (n, payload[n].count('"$value"')))
        total = sum(t.count('"$value"') for n, t in payload.items() if n != "manifest.json")
        print("Total: %d tokens en %d archivos → %s/" % (total, len(payload), rel))
        self.report()
        return 0

    def report(self):
        self.gaps = list(dict.fromkeys(self.gaps))
        self.skipped = list(dict.fromkeys(self.skipped))
        if self.gaps:
            print("\nAVISO · huecos entre modos (el modo incompleto no resolverá todos los alias):")
            for g in self.gaps[:20]:
                print("  ·", g)
            if len(self.gaps) > 20:
                print("  · … y %d más" % (len(self.gaps) - 20))
            print("  Se corrigen en Figma y se vuelve a correr ds-sync.py, nunca editando la salida.")
        if self.skipped:
            print("\nAVISO · tokens no exportados (%d):" % len(self.skipped))
            for s in self.skipped[:20]:
                print("  ·", s)
            if len(self.skipped) > 20:
                print("  · … y %d más" % (len(self.skipped) - 20))


AVISO_DESACTIVADA = """La exportación a formato de terceros está DESACTIVADA en este proyecto.

No se ha escrito nada. Es una decisión registrada, no un error.

Qué crearía si se activa:
  · design-system/tokens/w3c/ con un archivo de tokens por modo y un manifest.json
  · un espejo MÁS de los tokens: la fuente de verdad sigue siendo Figma y el código sigue
    consumiendo var(--token) de tokens/tokens.css

Para activarla hay que explicárselo antes a la persona usuaria y obtener su consentimiento
explícito. Solo entonces:  python3 scripts/tokens-dtcg.py --enable
Queda registrado en design-system/agent-manifest.json → exports.dtcg."""


def enabled_state(root):
    """(activada, ruta_del_manifiesto). Una carpeta ya generada cuenta como activada:
    los proyectos creados antes de que esto fuera opcional no se rompen."""
    mpath = os.path.join(root, "design-system", "agent-manifest.json")
    flag = False
    if os.path.exists(mpath):
        try:
            with open(mpath, encoding="utf-8") as fh:
                flag = bool(((json.load(fh).get("exports") or {}).get("dtcg") or {}).get("enabled"))
        except Exception:
            flag = False
    out = os.path.join(root, "design-system", "tokens", "w3c")
    ya_existe = os.path.isdir(out) and any(f.endswith(".json") for f in os.listdir(out))
    return (flag or ya_existe), mpath


def record_consent(mpath):
    if not os.path.exists(mpath):
        print("[AVISO] no hay agent-manifest.json donde registrar el consentimiento; se genera igualmente.")
        return
    with open(mpath, encoding="utf-8") as fh:
        man = json.load(fh)
    exp = man.setdefault("exports", {}).setdefault("dtcg", {})
    exp["enabled"] = True
    exp.setdefault("path", "./tokens/w3c/")
    exp.setdefault("generator", "../scripts/tokens-dtcg.py")
    exp["decidedAt"] = __import__("datetime").date.today().isoformat()
    with open(mpath, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(man, ensure_ascii=False, indent=2) + "\n")
    print("Consentimiento registrado en design-system/agent-manifest.json → exports.dtcg.enabled = true\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="raíz del proyecto (por defecto, el directorio actual)")
    ap.add_argument("--check", action="store_true", help="no escribe; falla si la salida está desactualizada")
    ap.add_argument("--plan", action="store_true",
                    help="no escribe: imprime exactamente qué archivos crearía, para pedir permiso contra esa lista")
    ap.add_argument("--enable", action="store_true",
                    help="registra el consentimiento y genera. Solo tras explicarlo y obtener un sí explícito.")
    a = ap.parse_args()
    root = os.path.abspath(a.root)

    if a.plan:
        exp = Exporter(root)
        files = exp.build()
        print("Si autorizas la exportación, se crearán exactamente estos archivos en")
        print("design-system/tokens/w3c/ y nada más:\n")
        for n in sorted(files):
            n_tokens = json.dumps(files[n], ensure_ascii=False).count('"$value"')
            print("  %-34s %s" % (n, ("%d tokens" % n_tokens) if n != "manifest.json" else "ejes y combinaciones"))
        print("\nNo se toca ningún archivo existente. Figma sigue siendo la fuente de verdad y el")
        print("código sigue consumiendo var(--token) de tokens/tokens.css.")
        print("El formato de destino es un borrador, no un estándar cerrado.")
        print("\nSi la persona dice que sí a ESTA lista: python3 scripts/tokens-dtcg.py --enable")
        exp.report()
        return 0

    activa, mpath = enabled_state(root)
    if a.enable and not activa:
        record_consent(mpath)
        activa = True
    if not activa:
        print(AVISO_DESACTIVADA)
        return 0 if a.check else 2

    return Exporter(root).run(a.check)


if __name__ == "__main__":
    sys.exit(main())
