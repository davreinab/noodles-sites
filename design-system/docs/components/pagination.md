### Pagination   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:pagination -->
- **Figma:** `219:1662` · página «Navigation» · COMPONENT_SET · 2 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** Pagination: paginador de la Recipe library que sustituye al botón «Ver más». Previous (deshabilitado en la página 1) · 1 2 3 … 12 13 · Next; página actual en Current (aria-current=page). Breakpoint Mobile: Previous/Next como flechas y «Page 1 of 13». Uso: Library (Recipe library, wireframe 171:3808 y móvil 486:13025). Clase CSS: .pagination (ítems .pagination__item). Nota: en Mobile las flechas son texto (←/→) y no iconos; los iconos chevron/arrow existentes no se han anidado.
- **Anatomía:** `Pagination item` → State=Disabled, `icon` → Icon / arrow-left, `Pagination item` → State=Current, `icon` → Icon / arrow-left, `Pagination item` → State=Default, `icon` → Icon / arrow-left, `Pagination item` → State=Default, `icon` → Icon / arrow-left, `Pagination item` → State=Default, `icon` → Icon / arrow-left, `Pagination item` → State=Default, `icon` → Icon / arrow-left, `Pagination item` → State=Default, `icon` → Icon / arrow-left
- **API:** `breakpoint`: Desktop, Mobile (por defecto Desktop)
- **Nombres en Figma:** `breakpoint` ← `Breakpoint`
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `button/primary/bg`, `button/primary/text`, `color/border/default`, `color/border/subtle`, `color/text/default`, `color/text/disabled`, `font/family/display`, `font/line-height/desktop/label`, `font/size/desktop/label`, `font/style/display`, `icon/color/default`, `icon/size/md`, `radius/md`, `space/8`
- **Text styles:** `Desktop/label`
<!-- ⚙️ GENERATED:end:pagination -->

- **Propósito:** Navegación entre páginas de una rejilla de recetas, en lugar de «ver más». Previous · números · Next. La página actual va rellena en tinta. Botones de 40 px con borde. En móvil se ocultan los números y la elipsis, y quedan las flechas solo con icono y el texto «Page 1 of 13» (`pagination__status`, oculto en escritorio).
- **Ejemplo de código:**
  ```html
  <nav data-ds="pagination" class="pagination" aria-label="Pagination">
  <ul class="pagination__list">
  <li><button class="pagination__link" type="button" disabled aria-label="Previous page"><span class="icon icon-arrow-left" aria-hidden="true"></span><span class="pagination__text">Previous</span></button></li>
  <li><a class="pagination__link pagination__page" href="?page=1" aria-current="page">1</a></li>
  <li><a class="pagination__link pagination__page" href="?page=2">2</a></li>
  <li><a class="pagination__link pagination__page" href="?page=3">3</a></li>
  <li><span class="pagination__ellipsis" aria-hidden="true">…</span></li>
  <li><a class="pagination__link pagination__page" href="?page=12">12</a></li>
  <li><a class="pagination__link pagination__page" href="?page=13">13</a></li>
  <li><a class="pagination__link" href="?page=2" aria-label="Next page"><span class="pagination__text">Next</span><span class="icon icon-arrow-right" aria-hidden="true"></span></a></li>
  </ul>
  <p class="pagination__status">Page 1 of 13</p>
  </nav>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Rol: landmark `nav` con nombre por `aria-label` («Pagination») y lista `ul`. Página actual: `aria-current="page"` en su enlace, que se anuncia como página actual; no se distingue solo por color. Anterior en la primera página: `disabled` en el botón (no se puede enfocar ni activar); si el patrón usa enlaces, `aria-disabled="true"` y sin `href`. Anterior y siguiente llevan siempre `aria-label` («Previous page», «Next page»): en móvil su texto visible está oculto y el icono no tiene nombre. La elipsis es `aria-hidden`. En móvil los números se ocultan con display none, así que no son tabulables, y «Page 1 of 13» da la posición. Teclado: Tab recorre anterior, números visibles y siguiente; Enter o Espacio activan. Foco: contorno de 2 px.
- **Cuándo usar / qué NO hace:** Para listados paginados donde el usuario salta de página (Recipe library). No se muestra si todo cabe en una página. No es un filtro ni pestañas: cambia de página, no de criterio. Sus flechas son icono y texto del DS, no una imagen.
