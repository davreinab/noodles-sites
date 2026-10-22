### Alert   ⚙️ synced: 2026-10-22T09:37:04Z

<!-- ⚙️ GENERATED:start:alert -->
- **Figma:** `80:138` · página «Feedback & overlays» · COMPONENT_SET · 8 variantes · última sync 2026-10-22T09:37:04Z
- **Descripción (Figma):** Mensaje de estado. Type=Info · Success · Alert · Error, cada uno con su icono fijo (info, circle-check, triangle-alert, circle-alert) y su título: el tipo nunca se comunica solo por color. Layout=Inline: dentro del contenido (formulario, concurso cerrado), radius/sm. Layout=Toast: flotante y temporal en layer/toast, elevation/3, abajo centrado en móvil y abajo a la derecha en desktop; se cierra solo a los 6 s salvo Error, que espera al usuario (y la pausa al pasar el ratón o con el foco). Accesibilidad: Info/Success con role="status" (aria-live polite); Alert/Error con role="alert". Cerrar es un <button aria-label="Cerrar aviso">. El título se edita en la instancia (no es propiedad para no perder el título de cada tipo).
- **Anatomía:** `icon-status` → Icon / info, `icon-close` → Icon / close
- **API:** `body` (string, por defecto Texto de ejemplo con el detalle del mensaje.) · `dismissible` (boolean, por defecto true) · `closeIcon` (icon, por defecto Icon / close) · `type`: Info, Success, Alert, Error (por defecto Info) · `layout`: Inline, Toast (por defecto Inline)
- **Nombres en Figma:** `body` ← `Body#80:9`, `dismissible` ← `Dismissible#80:18`, `closeIcon` ← `Close icon#80:36`, `type` ← `Type`, `layout` ← `Layout`
- **Iconos / instancias anidadas:** sí · swap: `closeIcon` · por defecto: Icon / close · capas sin swap: icon-status
- **Tokens que consume:** `alert/close`, `alert/info/bg`, `alert/info/border`, `alert/info/icon`, `alert/info/text`, `border/width/thin`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-s`, `font/line-height/desktop/label`, `font/size/desktop/body-s`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/md`, `icon/size/sm`, `radius/sm`, `space/16`, `space/24`, `space/4`
- **Text styles:** `Desktop/label`, `Desktop/body-s`
<!-- ⚙️ GENERATED:end:alert -->

- **Propósito:** Mensaje de estado. Inline va dentro del contenido (formularios, concurso cerrado); Toast flota y desaparece solo, salvo los errores.
- **Ejemplo de código:**
  ```html
  <div data-ds="alert" class="alert" role="status">
  <span class="icon icon-info" aria-hidden="true"></span>
  <div class="alert__content"><p class="alert__title">Información</p><p class="alert__body">El concurso abre el 1 de noviembre.</p></div>
  <button class="alert__close" type="button" aria-label="Cerrar aviso"><span class="icon icon-close" aria-hidden="true"></span></button>
  </div>
  <div data-ds="alert" class="alert alert--error alert--toast" role="alert">
  <span class="icon icon-circle-alert" aria-hidden="true"></span>
  <div class="alert__content"><p class="alert__title">Algo ha fallado</p><p class="alert__body">No hemos podido cargar el contenido.</p></div>
  </div>
  <div data-ds="alert" class="alert alert--success" role="status">
  <span class="icon icon-circle-check" aria-hidden="true"></span>
  <div class="alert__content"><p class="alert__title">Participación enviada</p><p class="alert__body">Te avisaremos por correo si ganas.</p></div>
  </div>
  <div data-ds="alert" class="alert alert--alert" role="status">
  <span class="icon icon-triangle-alert" aria-hidden="true"></span>
  <div class="alert__content"><p class="alert__title">Quedan pocas horas</p><p class="alert__body">El concurso cierra hoy a las 23:59.</p></div>
  </div>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Texto sobre fondo de estado: Info 8,3:1, Success 7,1:1, Alert 7,7:1, Error 6,7:1. Iconos y borde (≥ 3:1): Info 5,1:1, Success 4,8:1, Alert 4,7:1, Error 4,9:1. Cada tipo tiene icono y título propios: no depende del color. Rol: Info y Success con `role="status"` (educado); Alert y Error con `role="alert"`. El toast se cierra a los 6 s salvo Error, y se pausa con el ratón encima o con foco. Cerrar es un botón con nombre.
- **Cuándo usar / qué NO hace:** Para comunicar el resultado de una acción o un estado de la página. No sustituye a la validación de campo (mensaje bajo el Field) ni a un Modal. No se apilan más de tres toasts.
