### Suggestion bubble   ⚙️ synced: 2026-10-07T17:39:59Z

<!-- ⚙️ GENERATED:start:suggestion-bubble -->
- **Figma:** `81:87` · página «Suggestion bubble» · COMPONENT_SET · 6 variantes · última sync 2026-10-07T17:39:59Z
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

- **Propósito:** ⬜ TODO
- **Ejemplo de código:** ⬜ TODO _(snippet HTML mínimo con las clases reales de `components.css`; se copia a `source.code.example` del schema)_
  ```html
  <!-- ⬜ TODO -->
  ```
- **Accesibilidad (pares AA verificados):** ⬜ TODO
- **Cuándo usar / qué NO hace:** ⬜ TODO
