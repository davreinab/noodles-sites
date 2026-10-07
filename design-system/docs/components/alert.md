### Alert   ⚙️ synced: 2026-10-07T18:43:11Z

<!-- ⚙️ GENERATED:start:alert -->
- **Figma:** `80:138` · página «Alert» · COMPONENT_SET · 8 variantes · última sync 2026-10-07T18:43:11Z
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

- **Propósito:** Mensaje de estado. Inline va dentro del contenido (formularios, concurso cerrado); Toast flota y desaparece solo, salvo los errores.
- **Ejemplo de código:**
  ```html
  <div class="alert" role="status">
  <span class="icon icon-info" aria-hidden="true"></span>
  <div class="alert__content"><p class="alert__title">Información</p><p class="alert__body">El concurso abre el 1 de noviembre.</p></div>
  <button class="alert__close" type="button" aria-label="Cerrar aviso"><span class="icon icon-close" aria-hidden="true"></span></button>
  </div>
  <div class="alert alert--error alert--toast" role="alert">
  <span class="icon icon-circle-alert" aria-hidden="true"></span>
  <div class="alert__content"><p class="alert__title">Algo ha fallado</p><p class="alert__body">No hemos podido cargar el contenido.</p></div>
  </div>
  ```
- **Accesibilidad (pares AA verificados):** Texto sobre fondo de estado: Info 8,3:1, Success 7,1:1, Alert 7,7:1, Error 6,7:1. Iconos y borde (≥ 3:1): Info 5,1:1, Success 4,8:1, Alert 4,7:1, Error 4,9:1. Cada tipo tiene icono y título propios: no depende del color. Rol: Info y Success con `role="status"` (educado); Alert y Error con `role="alert"`. El toast se cierra a los 6 s salvo Error, y se pausa con el ratón encima o con foco. Cerrar es un botón con nombre.
- **Cuándo usar / qué NO hace:** Para comunicar el resultado de una acción o un estado de la página. No sustituye a la validación de campo (mensaje bajo el Field) ni a un Modal. No se apilan más de tres toasts.
