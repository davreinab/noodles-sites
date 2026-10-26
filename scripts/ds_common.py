#!/usr/bin/env python3
"""ds_common — lo que todos los scripts del design system tienen que entender igual.

Módulo compartido (no se ejecuta solo). Hoy contiene la ÚNICA definición de «componente interno»: una pieza de
trabajo de Figma que no forma parte del sistema compartido y nunca se construye. Antes la decidía solo
ds-library.py y el resto de la skill los trataba como componentes normales: ensuciaban la verificación, la
cobertura de variantes, los avisos de ejemplo y de iconos, las colisiones de slug y los borradores de textos.

Qué es un interno (en este orden, el primero que cumpla da el motivo):
  1. nombre que empieza por «.» o «_» (Figma no los publica);
  2. «deprecated» en el nombre o en la página (retirado);
  3. página «Documentation»;
  4. no publicado: `figma.published` es false en el contrato (el script de lectura lo trae si Figma lo expone);
  5. lista manual: `internal.names` de scripts/ds-library.config.json, por nombre o por slug;
  6. patrones de nombre: `internal.namePatterns` (expresiones regulares, sin distinguir mayúsculas). Vacío por defecto: cómo
     se nombran las piezas de demo o de ejemplo es una convención de cada equipo, la skill no impone ninguna.

Además, `partes_de` dice qué piezas son PARTES de otro componente (una pieza que algún componente propio instancia: un hueco
de swap, un subcomponente): no se construyen por separado, las cubre el ejemplo de su padre. Sale de `relations.uses`, no de
los nombres.
La configuración vive en scripts/ds-library.config.json y la leen todos los scripts con `load_config`.
Sin dependencias (stdlib).
"""
import json
import os
import re


def _jload(path, default=None):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return default


def load_config(here):
    """Config compartida de scripts/ds-library.config.json: internal.names y pagePrefixes."""
    cfg = {"internal": {"names": [], "namePatterns": []}, "pagePrefixes": []}
    user = _jload(os.path.join(here, "ds-library.config.json"), {}) or {}
    if isinstance(user.get("internal"), dict):
        cfg["internal"].update(user["internal"])
    if isinstance(user.get("pagePrefixes"), list):
        cfg["pagePrefixes"] = [str(x).strip() for x in user["pagePrefixes"] if str(x).strip()]
    return cfg


def pagina(meta, cfg=None):
    """Primer tramo de la página de Figma (antes de « / »), sin el prefijo que solo nombra el archivo
    (config: pagePrefixes). Es el grupo del menú de la library y la «página» a efectos de internos."""
    partes = [x.strip() for x in (meta.get("figmaPage") or "Sin página").split(" / ")]
    prefijos = {x.lower() for x in ((cfg or {}).get("pagePrefixes") or [])}
    if len(partes) > 1 and partes[0].lower() in prefijos:
        partes = partes[1:]
    return partes[0] or "Sin página"


def seccion(meta, cfg=None):
    """Segundo tramo de la página de Figma («Página / Sección»), o "" si no lo hay."""
    partes = [x.strip() for x in (meta.get("figmaPage") or "").split(" / ")]
    prefijos = {x.lower() for x in ((cfg or {}).get("pagePrefixes") or [])}
    if len(partes) > 1 and partes[0].lower() in prefijos:
        partes = partes[1:]
    return partes[1] if len(partes) > 1 else ""


def interno_motivo(meta, cfg, published=None):
    """El motivo por el que una pieza es interna, o None si es un componente normal."""
    name, sl = meta.get("name") or "", meta.get("slug") or ""
    if name.startswith("."):
        return "nombre con punto (Figma no lo publica)"
    if name.startswith("_"):
        return "nombre con guion bajo (Figma no lo publica)"
    page = meta.get("figmaPage") or ""
    if "deprecated" in name.lower() or "deprecated" in page.lower():
        return "retirado («deprecated» en el nombre o en la página)"
    if pagina(meta, cfg).lower() == "documentation":
        return "página Documentation"
    if published is False:
        return "no publicado en Figma"
    names = {str(x) for x in (cfg.get("internal") or {}).get("names") or []}
    if name in names or sl in names:
        return "lista manual: internal.names"
    for pat in (cfg.get("internal") or {}).get("namePatterns") or []:
        try:
            if re.search(str(pat), name, re.I) or re.search(str(pat), sl, re.I):
                return "coincide con internal.namePatterns: %s" % pat
        except re.error:
            continue
    return None


def interno_de(sch, cfg):
    """Motivo de interno de un contrato (schema). Respeta `meta.internal` si el sync ya lo marcó."""
    meta = sch.get("meta") or {}
    if meta.get("internal") is True:
        return meta.get("internalReason") or "marcado como interno"
    return interno_motivo(meta, cfg, (sch.get("figma") or {}).get("published"))


def es_interno(meta, cfg):
    """Versión corta para quien solo tiene la meta (la meta lleva `internal` desde que el sync lo marca)."""
    if meta.get("internal") is True:
        return True
    return interno_motivo(meta, cfg) is not None


def partes_de(schemas, cfg):
    """{slug de la pieza: [slugs de los componentes propios que la instancian]} para las piezas que son parte de otro componente.
    `schemas`: lista de contratos. Los padres internos no cuentan (una pieza interna no es el sitio donde se cubre nada)."""
    padres = {}
    for s in schemas:
        meta = s.get("meta") or {}
        if interno_de(s, cfg) is not None:
            continue
        for u in ((s.get("relations") or {}).get("uses") or []):
            if u != meta.get("slug"):
                padres.setdefault(u, []).append(meta.get("slug"))
    return {k: sorted(set(v)) for k, v in padres.items()}

