### Modal   ⚙️ synced: 2026-10-07T18:49:29Z

<!-- ⚙️ GENERATED:start:modal -->
- **Figma:** `79:123` · página «Modal» · COMPONENT_SET · 3 variantes · última sync 2026-10-07T18:49:29Z
- **Descripción (Figma):** Diálogo modal. Size=M (560): alérgenos, resultado de concurso. Size=L (880): etiqueta del envase (imagen ampliable), resultados de búsqueda. Size=Full (móvil, pantalla completa). Anatomía: cabecera (título h3 + Icon button cerrar) · contenido (swap «Content», por defecto Modal / Slot) · pie opcional con acción. Se muestra sobre el velo modal/overlay (layer/overlay) y el diálogo en layer/modal. Accesibilidad: &lt;dialog&gt; o role=&quot;dialog&quot; + aria-modal=&quot;true&quot; + aria-labelledby al título; el foco entra en el primer elemento (o el título), queda atrapado dentro, Esc y el botón cerrar lo cierran y el foco vuelve al disparador; el fondo queda inerte (inert) y sin scroll.
- **Anatomía:** `close` → Hierarchy=Secondary, Size=M, State=Default, `Icon / close` → Icon / close, `content` → Modal / Slot, `action` → Hierarchy=Primary, Size=M, State=Default, `icon-leading` → Icon / arrow-right, `icon-trailing` → Icon / arrow-right
- **Size:** M, L, Full
- **Propiedades de componente:** `Title#79:0` (TEXT, por defecto Título del modal), `Content#79:4` (INSTANCE_SWAP, por defecto Modal / Slot), `Footer#79:8` (BOOLEAN, por defecto True), `Size` (VARIANT, por defecto M)
- **Iconos / instancias anidadas:** sí · swap: `Content#79:4` · por defecto: Modal / Slot
- **Tokens que consume:** `border/width/thick`, `border/width/thin`, `button/primary/bg`, `button/primary/border`, `button/primary/text`, `button/secondary/border`, `font/family/body`, `font/family/display`, `font/line-height/desktop/caption`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/size/desktop/caption`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon-button/size/m`, `icon/color/default`, `icon/size/md`, `icon/size/sm`, `modal/bg`, `modal/border`, `modal/slot-bg`, `modal/text`, `modal/title`, `modal/width/m`, `radius/md`, `radius/pill`, `radius/sm`, `shadow/soft`, `space/16`, `space/24`, `space/8`
- **Text styles:** `Desktop/h3`, `Desktop/caption`, `Desktop/label`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `button/primary/bg`, `button/primary/border`, `button/primary/text`, `button/secondary/border`, `font/family/body`, `font/family/display`, `font/line-height/desktop/caption`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/size/desktop/caption`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/color/default`, `modal/bg`, `modal/border`, `modal/slot-bg`, `modal/text`, `modal/title`, `shadow/soft`
<!-- ⚙️ GENERATED:end:modal -->

- **Propósito:** Diálogo modal para la etiqueta del envase y los resultados de búsqueda (L), alérgenos y resultado de concurso (M). En móvil ocupa la pantalla entera.
- **Ejemplo de código:**
  ```html
  <dialog class="modal modal--l" aria-labelledby="modal-title" open>
  <div class="modal__header">
  <h2 class="modal__title" id="modal-title">Etiqueta del envase</h2>
  <button class="icon-button icon-button--secondary" type="button" aria-label="Cerrar"><span class="icon icon-close" aria-hidden="true"></span></button>
  </div>
  <div class="modal__body"><div class="modal-slot">Contenido</div></div>
  <div class="modal__footer"><button class="button" type="button">Entendido</button></div>
  </dialog>
  ```
- **Accesibilidad (pares AA verificados):** Título y texto tinta sobre blanco 18,7:1; velo `--modal-overlay` (tinta al 70 %) detrás, sin texto encima. Rol: `<dialog>` abierto con `showModal()` (el ejemplo lleva `open` solo para mostrarlo en el showcase) (aporta `aria-modal`, foco atrapado y fondo inerte); nombre por `aria-labelledby` al título. El foco entra en el primer elemento (o el título), Esc y el botón cerrar lo cierran y el foco vuelve al disparador. Foco del botón cerrar: el de Icon button. Animación de entrada `--motion-duration-slow`, desactivada con reduce-motion.
- **Cuándo usar / qué NO hace:** Para contenido que exige atención o detalle sin salir de la página. No se usa para avisos breves (Alert/Toast) ni para navegar. Un solo modal a la vez.
