### Pagination item   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:pagination-item -->
- **Figma:** `219:1639` · página «Navigation» · COMPONENT_SET · 3 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** Pagination item: botón cuadrado 40×40 con borde (radius/md) para el paginador de la Recipe library. State=Default (número o Previous/Next activos), Current (página actual, relleno tinta con aria-current=page), Disabled (Previous en la primera página). Propiedad Label (número o texto). Uso: Pagination (Recipe library, wireframe 171:3808 y móviles 486:13025 / 265:3948). Clase CSS: .pagination__item (.pagination__item--current, .pagination__item--disabled).
- **Anatomía:** `icon` → Icon / arrow-left
- **API:** `label` (string, por defecto 1) · `icon` (boolean, por defecto false) · `arrow` (icon, por defecto Icon / arrow-left) · `current` (boolean, por defecto false) · `disabled` (boolean, por defecto false)
- **Nombres en Figma:** `label` ← `Label#219:4`, `icon` ← `Icon#221:0`, `arrow` ← `Arrow#221:4`, `current` ← `State=Current`, `disabled` ← `State=Disabled`
- **Iconos / instancias anidadas:** sí · swap: `arrow` · por defecto: Icon / arrow-left
- **Tokens que consume:** `color/border/default`, `color/text/default`, `font/family/display`, `font/line-height/desktop/label`, `font/size/desktop/label`, `font/style/display`, `icon/color/default`, `icon/size/md`, `radius/md`, `space/8`
- **Text styles:** `Desktop/label`
<!-- ⚙️ GENERATED:end:pagination-item -->

- **Propósito:** Un número, o Previous/Next, dentro del paginador (`.pagination`). Es el enlace o botón de una página: la página actual (`aria-current="page"`), Previous deshabilitado en la primera página (`disabled`), y en móvil solo flecha (`icon`). Lo compone `pagination`; no se usa suelto.
- **Ejemplo de código:**
  ```html
  <ul data-ds="pagination-item" class="pagination__list">
  <li><a class="pagination__link pagination__page" href="?page=2">2</a></li>
  <li><a class="pagination__link pagination__page" href="?page=1" aria-current="page">1</a></li>
  <li><button class="pagination__link" type="button" disabled aria-label="Previous page"><span class="pagination__text">Previous</span></button></li>
  <li><a class="pagination__link" href="?page=2" aria-label="Next page"><span class="icon icon-arrow-right" aria-hidden="true"></span></a></li>
  </ul>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Página actual: `aria-current="page"` (se anuncia como página actual; no se distingue solo por color). Previous en la primera página: `disabled` en el botón, o `aria-disabled="true"` sin `href` si es enlace. Los botones solo con icono llevan `aria-label`. Teclado: Tab y Enter o Espacio.
- **Cuándo usar / qué NO hace:** Para cada página o flecha de un `pagination`. No gestiona la paginación por sí solo: el enlace apunta a la página que corresponda.
