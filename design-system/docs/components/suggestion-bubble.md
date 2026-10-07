### Suggestion bubble   ⚙️ synced: 2026-10-07T18:49:29Z

<!-- ⚙️ GENERATED:start:suggestion-bubble -->
- **Figma:** `81:87` · página «Suggestion bubble» · COMPONENT_SET · 6 variantes · última sync 2026-10-07T18:49:29Z
- **Descripción (Figma):** Botón flotante (suggestion box / Babelbox) hacia el formulario externo de Calidad. Fijo abajo a la derecha (layout/margin desde los bordes), layer/floating; no tapa el CTA del Mobile menu ni el Toast (que sube por encima). Expanded=True al cargar: icono + «Sugerencias» + external-link; al hacer scroll pasa a Expanded=False (solo icono, 56 px) y respeta prefers-reduced-motion. Es un &lt;a target=&quot;_blank&quot; rel=&quot;noopener&quot;&gt; con nombre accesible «Sugerencias (abre en una pestaña nueva)» también en la versión plegada. Hover: fondo amarillo de marca y elevation/2; Focus: anillo suggestion/focus-ring.
- **Anatomía:** `icon` → Icon / message-circle, `icon-external` → Icon / external-link
- **Expanded:** True, False
- **State:** Default, Hover, Focus
- **Propiedades de componente:** `Label#81:0` (TEXT, por defecto Sugerencias), `Icon#81:7` (INSTANCE_SWAP, por defecto Icon / message-circle), `Expanded` (VARIANT, por defecto True), `State` (VARIANT, por defecto Default)
- **Iconos / instancias anidadas:** sí · swap: `Icon#81:7` · por defecto: Icon / message-circle · capas sin swap: icon-external
- **Tokens que consume:** `border/width/thin`, `color/effect/shadow-ink`, `font/family/display`, `font/line-height/desktop/label`, `font/size/desktop/label`, `font/style/display`, `icon/size/md`, `icon/size/sm`, `radius/pill`, `space/16`, `space/24`, `space/8`, `suggestion/bg`, `suggestion/border`, `suggestion/text`
- **Text styles:** `Desktop/label`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `color/effect/shadow-ink`, `font/family/display`, `font/line-height/desktop/label`, `font/size/desktop/label`, `font/style/display`, `suggestion/bg`, `suggestion/border`, `suggestion/text`
<!-- ⚙️ GENERATED:end:suggestion-bubble -->

- **Propósito:** Botón flotante hacia el formulario externo de Calidad (suggestion box). Abierto al cargar; se pliega a solo icono al hacer scroll.
- **Ejemplo de código:**
  ```html
  <a class="suggestion-bubble" href="https://calidad.example.org" target="_blank" rel="noopener" aria-label="Sugerencias (abre en una pestaña nueva)">
  <span class="icon icon-message-circle" aria-hidden="true"></span>
  <span class="suggestion-bubble__label">Sugerencias</span>
  <span class="icon icon-external-link" aria-hidden="true"></span>
  </a>
  ```
- **Accesibilidad (pares AA verificados):** Crema sobre tinta 17,2:1; hover tinta sobre amarillo 12,3:1. Rol: `<a>` externo con nombre accesible fijo en `aria-label`, así que sigue nombrado cuando está plegado (`.suggestion-bubble--collapsed`). Foco: contorno de 2 px pegado; en tinta sobre tinta se lee como el componente 2 px más grande contra la página. No tapa contenido esencial: fijo abajo a la derecha (`--layout-margin`) en `--layer-floating`; el plegado respeta reduce-motion.
- **Cuándo usar / qué NO hace:** Una por página, siempre el mismo destino (Calidad). No es un chat ni el contacto general (formulario de GB Foods en el Footer).
