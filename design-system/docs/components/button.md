### Button   ⚙️ synced: 2026-10-07T18:17:24Z

<!-- ⚙️ GENERATED:start:button -->
- **Figma:** `33:295` · página «Button» · COMPONENT_SET · 24 variantes · última sync 2026-10-07T18:17:24Z
- **Descripción (Figma):** Botón de acción. Hierarchy: Primary (acción principal, 1 por vista), Secondary (alternativa), Inverse (sobre fondos oscuros). Size M (48) por defecto; L (64) para hero y CTA destacados. Label en Anton mayúsculas. Iconos opcionales delante/detrás (INSTANCE_SWAP). Focus: anillo exterior visible. Disabled sin opacidad (colores propios).
- **Anatomía:** `icon-leading` → Icon / arrow-right, `icon-trailing` → Icon / arrow-right
- **Hierarchy:** Primary, Secondary, Inverse
- **Size:** M, L
- **State:** Default, Hover, Focus, Disabled
- **Propiedades de componente:** `Label#33:0` (TEXT, por defecto Botón), `Icon leading#33:25` (BOOLEAN, por defecto False), `Icon trailing#33:50` (BOOLEAN, por defecto False), `Icon leading swap#33:75` (INSTANCE_SWAP, por defecto Icon / arrow-right), `Icon trailing swap#33:100` (INSTANCE_SWAP, por defecto Icon / arrow-right), `Hierarchy` (VARIANT, por defecto Primary), `Size` (VARIANT, por defecto M), `State` (VARIANT, por defecto Default)
- **Iconos / instancias anidadas:** sí · swap: `Icon leading swap#33:75`, `Icon trailing swap#33:100` · por defecto: Icon / arrow-right, Icon / arrow-right
- **Tokens que consume:** `border/width/thick`, `button/primary/bg`, `button/primary/border`, `button/primary/text`, `font/family/display`, `font/line-height/desktop/label`, `font/size/desktop/label`, `font/style/display`, `icon/size/sm`, `radius/pill`, `space/16`, `space/24`, `space/8`
- **Text styles:** `Desktop/label`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `button/primary/bg`, `button/primary/border`, `button/primary/text`, `font/family/display`, `font/line-height/desktop/label`, `font/size/desktop/label`, `font/style/display`
<!-- ⚙️ GENERATED:end:button -->

- **Propósito:** Botón de acción con texto. Primary es la acción principal de la vista (una por vista); Secondary, la alternativa; Inverse, la acción sobre fondos de tinta. Size L para hero y CTA destacados.
- **Ejemplo de código:**
  ```html
  <button class="button" type="button">Dónde comprar</button>
  <a class="button button--secondary" href="/recetas">Ver recetas <span class="icon icon-arrow-right" aria-hidden="true"></span></a>
  <button class="button button--inverse button--l" type="button">Participar</button>
  <button class="button" type="button" aria-disabled="true">No disponible</button>
  ```
- **Accesibilidad (pares AA verificados):** Primary: crema sobre tinta 17,2:1; hover tinta sobre naranja 7,1:1. Secondary: tinta sobre crema 17,2:1 o blanco 18,7:1; hover crema sobre tinta 17,2:1. Inverse: tinta sobre crema 17,2:1; hover tinta sobre amarillo 12,3:1. Disabled: gris cálido sobre arena 4,3:1 (exento de AA, pero legible). Rol: `<button>` para acciones y `<a>` para navegar, con la misma apariencia. Nombre: el texto visible; el icono va `aria-hidden`. Teclado: Enter y Espacio (botón) o Enter (enlace). Foco: contorno de 2 px pegado en `--button-*-focus-ring` (tinta; amarillo en Inverse, 12,3:1 sobre tinta). Desactivado: preferir `aria-disabled="true"` para que siga enfocable y se pueda explicar el motivo. Altura M 48 y L 64 (≥ 44 de área táctil).
- **Cuándo usar / qué NO hace:** Para disparar una acción o ir a un destino principal (Dónde comprar, Participar, Descubre los productos). No se usa dentro de un párrafo (eso es Link), ni solo con icono (eso es Icon button), ni como filtro (eso es Chip). No hay más de un Primary visible por vista.
