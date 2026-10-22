### Icon / chevron-down   ⚙️ synced: 2026-10-22T09:37:04Z

<!-- ⚙️ GENERATED:start:icon-chevron-down -->
- **Figma:** `21:59` · página «Iconography» · COMPONENT · 1 variantes · última sync 2026-10-22T09:37:04Z
- **Descripción (Figma):** Chevron del selector de idioma (landings), escalado a 24. Trazo 2.5 px (geometría fija del glifo). Color: icon/color/*. Tamaño: icon/size/*
- **Anatomía:** sin instancias anidadas
- **API:** sin propiedades
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `icon/color/default`, `icon/size/md`
<!-- ⚙️ GENERATED:end:icon-chevron-down -->

- **Propósito:** Glifo de interfaz: chevron del selector de idioma (landings), escalado a 24.
- **Ejemplo de código:**
  ```html
  <span data-ds="icon-chevron-down" class="icon icon-chevron-down" aria-hidden="true"></span>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Decorativo por defecto (`aria-hidden="true"`): el significado lo da el texto o el nombre accesible del control. Color `--icon-color-default` (tinta) sobre página 17,2:1 y sobre card 18,7:1; `--icon-color-inverse` (crema) sobre tinta 17,2:1; todos ≥ 3:1 de elemento gráfico. Dentro de un componente hereda su color (`currentColor`), así que el par válido es el del componente. Tamaños `--icon-size-sm/md/lg/xl` con `.icon--sm/--lg/--xl`.
- **Cuándo usar / qué NO hace:** Dentro de otro componente (Button, Icon button, Link, Chip, Alert…) o junto a un texto que dice lo mismo. Un icono solo no transmite información: si no hay texto visible, el control que lo contiene lleva `aria-label`. No se recolorea con valores sueltos ni se cambia el trazo (2,5 fijo).
