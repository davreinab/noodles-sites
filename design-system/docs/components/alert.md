### Alert   ⚙️ synced: 2026-10-07T18:17:24Z

<!-- ⚙️ GENERATED:start:alert -->
- **Figma:** `80:138` · página «Alert» · COMPONENT_SET · 8 variantes · última sync 2026-10-07T18:17:24Z
- **Descripción (Figma):** Mensaje de estado. Type=Info · Success · Alert · Error, cada uno con su icono fijo (info, circle-check, triangle-alert, circle-alert) y su título: el tipo nunca se comunica solo por color. Layout=Inline: dentro del contenido (formulario, concurso cerrado), radius/sm. Layout=Toast: flotante y temporal en layer/toast, elevation/3, abajo centrado en móvil y abajo a la derecha en desktop; se cierra solo a los 6 s salvo Error, que espera al usuario (y la pausa al pasar el ratón o con el foco). Accesibilidad: Info/Success con role=&quot;status&quot; (aria-live polite); Alert/Error con role=&quot;alert&quot;. Cerrar es un &lt;button aria-label=&quot;Cerrar aviso&quot;&gt;. El título se edita en la instancia (no es propiedad para no perder el título de cada tipo).
- **Anatomía:** `icon-status` → Icon / info, `icon-close` → Icon / close
- **Type:** Info, Success, Alert, Error
- **Layout:** Inline, Toast
- **Propiedades de componente:** `Body#80:9` (TEXT, por defecto Texto de ejemplo con el detalle del mensaje.), `Dismissible#80:18` (BOOLEAN, por defecto True), `Close icon#80:36` (INSTANCE_SWAP, por defecto Icon / close), `Type` (VARIANT, por defecto Info), `Layout` (VARIANT, por defecto Inline)
- **Iconos / instancias anidadas:** sí · swap: `Close icon#80:36` · por defecto: Icon / close · capas sin swap: icon-status
- **Tokens que consume:** `alert/close`, `alert/info/bg`, `alert/info/border`, `alert/info/icon`, `alert/info/text`, `border/width/thin`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-s`, `font/line-height/desktop/label`, `font/size/desktop/body-s`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/md`, `icon/size/sm`, `radius/sm`, `space/16`, `space/24`, `space/4`
- **Text styles:** `Desktop/label`, `Desktop/body-s`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `alert/close`, `alert/info/bg`, `alert/info/border`, `alert/info/icon`, `alert/info/text`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-s`, `font/line-height/desktop/label`, `font/size/desktop/body-s`, `font/size/desktop/label`, `font/style/body`, `font/style/display`
<!-- ⚙️ GENERATED:end:alert -->

- **Propósito:** ⬜ TODO
- **Ejemplo de código:** ⬜ TODO _(snippet HTML mínimo con las clases reales de `components.css`; se copia a `source.code.example` del schema)_
  ```html
  <!-- ⬜ TODO -->
  ```
- **Accesibilidad (pares AA verificados):** ⬜ TODO
- **Cuándo usar / qué NO hace:** ⬜ TODO
