### Modal   ⚙️ synced: 2026-10-07T17:42:38Z

<!-- ⚙️ GENERATED:start:modal -->
- **Figma:** `79:123` · página «Modal» · COMPONENT_SET · 3 variantes · última sync 2026-10-07T17:42:38Z
- **Descripción (Figma):** Diálogo modal. Size=M (560): alérgenos, resultado de concurso. Size=L (880): etiqueta del envase (imagen ampliable), resultados de búsqueda. Size=Full (móvil, pantalla completa). Anatomía: cabecera (título h3 + Icon button cerrar) · contenido (swap «Content», por defecto Modal / Slot) · pie opcional con acción. Se muestra sobre el velo modal/overlay (layer/overlay) y el diálogo en layer/modal. Accesibilidad: &lt;dialog&gt; o role=&quot;dialog&quot; + aria-modal=&quot;true&quot; + aria-labelledby al título; el foco entra en el primer elemento (o el título), queda atrapado dentro, Esc y el botón cerrar lo cierran y el foco vuelve al disparador; el fondo queda inerte (inert) y sin scroll.
- **Anatomía:** `close` → Hierarchy=Secondary, Size=M, State=Default, `Icon / close` → Icon / close, `content` → Modal / Slot, `action` → Hierarchy=Primary, Size=M, State=Default, `icon-leading` → Icon / arrow-right, `icon-trailing` → Icon / arrow-right
- **Size:** M, L, Full
- **Propiedades de componente:** `Title#79:0` (TEXT, por defecto Título del modal), `Content#79:4` (INSTANCE_SWAP, por defecto Modal / Slot), `Footer#79:8` (BOOLEAN, por defecto True), `Size` (VARIANT, por defecto M)
- **Iconos / instancias anidadas:** sí · swap: `Content#79:4` · por defecto: Modal / Slot
- **Tokens que consume:** `border/width/thick`, `border/width/thin`, `button/primary/bg`, `button/primary/border`, `button/primary/text`, `button/secondary/border`, `font/family/body`, `font/family/display`, `font/line-height/desktop/caption`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/size/desktop/caption`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/color/default`, `icon/size/md`, `icon/size/sm`, `modal/bg`, `modal/border`, `modal/slot-bg`, `modal/text`, `modal/title`, `radius/md`, `radius/pill`, `radius/sm`, `shadow/soft`, `space/16`, `space/24`, `space/8`
- **Text styles:** `Desktop/h3`, `Desktop/caption`, `Desktop/label`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `button/primary/bg`, `button/primary/border`, `button/primary/text`, `button/secondary/border`, `font/family/body`, `font/family/display`, `font/line-height/desktop/caption`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/size/desktop/caption`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/color/default`, `modal/bg`, `modal/border`, `modal/slot-bg`, `modal/text`, `modal/title`, `shadow/soft`
<!-- ⚙️ GENERATED:end:modal -->

- **Propósito:** ⬜ TODO
- **Ejemplo de código:** ⬜ TODO _(snippet HTML mínimo con las clases reales de `components.css`; se copia a `source.code.example` del schema)_
  ```html
  <!-- ⬜ TODO -->
  ```
- **Accesibilidad (pares AA verificados):** ⬜ TODO
- **Cuándo usar / qué NO hace:** ⬜ TODO
