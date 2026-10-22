### Suggestion bubble   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:suggestion-bubble -->
- **Figma:** `81:87` · página «Feedback & overlays» · COMPONENT_SET · 6 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** RETIRADO (2026-10-22): no se usa; la vía de sugerencias es la caja del Footer (wireframe UX). Botón flotante (suggestion box / Babelbox) hacia el formulario externo de Calidad. Fijo abajo a la derecha (layout/margin desde los bordes), layer/floating; no tapa el CTA del Mobile menu ni el Toast (que sube por encima). Expanded=True al cargar: icono + «Sugerencias» + external-link; al hacer scroll pasa a Expanded=False (solo icono, 56 px) y respeta prefers-reduced-motion. Es un <a target="_blank" rel="noopener"> con nombre accesible «Sugerencias (abre en una pestaña nueva)» también en la versión plegada. Hover: fondo amarillo de marca y elevation/2; Focus: anillo suggestion/focus-ring.
- **Anatomía:** `icon` → Icon / message-circle, `icon-external` → Icon / external-link
- **API:** `label` (string, por defecto Sugerencias) · `icon` (icon, por defecto Icon / message-circle) · `expanded` (boolean, por defecto true)
- **Estados de CSS:** Hover, Focus
- **Nombres en Figma:** `label` ← `Label#81:0`, `icon` ← `Icon#81:7`, `expanded` ← `Expanded`
- **Iconos / instancias anidadas:** sí · swap: `icon` · por defecto: Icon / message-circle · capas sin swap: icon-external
- **Tokens que consume:** `border/width/thin`, `color/effect/shadow-ink`, `font/family/display`, `font/line-height/desktop/label`, `font/size/desktop/label`, `font/style/display`, `icon/size/md`, `icon/size/sm`, `radius/pill`, `space/16`, `space/24`, `space/8`, `suggestion/bg`, `suggestion/border`, `suggestion/text`
- **Text styles:** `Desktop/label`
<!-- ⚙️ GENERATED:end:suggestion-bubble -->

- **Propósito:** Botón flotante hacia el formulario externo de Calidad (suggestion box). Abierto al cargar; se pliega a solo icono al hacer scroll.
- **Ejemplo de código:**
  ```html
  <a data-ds="suggestion-bubble" class="suggestion-bubble" href="https://calidad.example.org" target="_blank" rel="noopener" aria-label="Sugerencias (abre en una pestaña nueva)">
  <span class="icon icon-message-circle" aria-hidden="true"></span>
  <span class="suggestion-bubble__label">Sugerencias</span>
  <span class="icon icon-external-link" aria-hidden="true"></span>
  </a>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Crema sobre tinta 17,2:1; hover tinta sobre amarillo 12,3:1. Rol: `<a>` externo con nombre accesible fijo en `aria-label`, así que sigue nombrado cuando está plegado (`.suggestion-bubble--collapsed`). Foco: contorno de 2 px pegado; en tinta sobre tinta se lee como el componente 2 px más grande contra la página. No tapa contenido esencial: fijo abajo a la derecha (`--layout-margin`) en `--layer-floating`; el plegado respeta reduce-motion.
- **Cuándo usar / qué NO hace:** Una por página, siempre el mismo destino (Calidad). No es un chat ni el contacto general (formulario de GB Foods en el Footer).
