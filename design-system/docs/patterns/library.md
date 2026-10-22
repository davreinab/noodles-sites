### Library   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:library -->
- **Figma:** `96:1453` · página «Pattern / Libraries» · COMPONENT_SET · 2 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** Library (Recipe library): cabecera Library head (título «Recipes», subtítulo, Search field, chips de filtro y estado Filtered con «48 results for your search» y «Clear filters»), rejilla de Recipe card (Desktop 4 columnas de 310 px con gutter 24 y space/48 entre filas; Mobile 1 columna) y Pagination (Previous · 1 2 3 … 12 13 · Next) en lugar del botón «Ver más». Solo recetas: la Product library usa Library hero y Product line (Pattern / Libraries). Sin variables propias.
- **Anatomía:** `Library head` → State=Default, Breakpoint=Desktop, `Search field` → State=Default, `icon-search` → Icon / search, `icon-clear` → Icon / close, `Chip` → Size=M, State=Selected, `icon-leading` → Icon / check, `Chip` → Size=M, State=Default, `icon-leading` → Icon / check, `Chip` → Size=M, State=Default, `icon-leading` → Icon / check, `Chip` → Size=M, State=Default, `icon-leading` → Icon / check, `Chip` → Size=M, State=Default, `icon-leading` → Icon / check, `Chip` → Size=M, State=Default, `icon-leading` → Icon / check, `Chip` → Size=M, State=Default, `icon-leading` → Icon / check, `product-card` → State=Default, `icon-time` → Icon / timer, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `product-card` → State=Default, `icon-time` → Icon / timer, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `product-card` → State=Default, `icon-time` → Icon / timer, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `product-card` → State=Default, `icon-time` → Icon / timer, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `product-card` → State=Default, `icon-time` → Icon / timer, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `product-card` → State=Default, `icon-time` → Icon / timer, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `product-card` → State=Default, `icon-time` → Icon / timer, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `product-card` → State=Default, `icon-time` → Icon / timer, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Pagination` → Breakpoint=Desktop, `Pagination item` → State=Disabled, `icon` → Icon / arrow-left, `Pagination item` → State=Current, `icon` → Icon / arrow-left, `Pagination item` → State=Default, `icon` → Icon / arrow-left, `Pagination item` → State=Default, `icon` → Icon / arrow-left, `Pagination item` → State=Default, `icon` → Icon / arrow-left, `Pagination item` → State=Default, `icon` → Icon / arrow-left, `Pagination item` → State=Default, `icon` → Icon / arrow-left
- **API:** `breakpoint`: Desktop, Mobile (por defecto Desktop)
- **Nombres en Figma:** `breakpoint` ← `Breakpoint`
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `border/width/thin`, `button/primary/bg`, `button/primary/text`, `chip/bg`, `chip/bg-selected`, `chip/border`, `chip/height/m`, `chip/height/s`, `chip/text`, `chip/text-selected`, `color/border/default`, `color/border/subtle`, `color/effect/shadow-ink`, `color/surface/page`, `color/text/default`, `color/text/disabled`, `color/text/secondary`, `field/bg`, `field/border`, `field/icon`, `field/placeholder`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/body-m`, `font/line-height/desktop/body-s`, `font/line-height/desktop/caption`, `font/line-height/desktop/h1`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/size/desktop/body-l`, `font/size/desktop/body-m`, `font/size/desktop/body-s`, `font/size/desktop/caption`, `font/size/desktop/h1`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/color/default`, `icon/size/md`, `icon/size/sm`, `layout/frame`, `layout/gutter`, `layout/margin`, `layout/section-y`, `radius/md`, `radius/none`, `radius/pill`, `recipe-card/bg`, `recipe-card/border`, `recipe-card/media-bg`, `recipe-card/meta`, `recipe-card/title`, `space/16`, `space/24`, `space/32`, `space/48`, `space/64`, `space/8`
- **Text styles:** `Desktop/h1`, `Desktop/body-l`, `Desktop/body-m`, `Desktop/body-s`, `Desktop/caption`, `Desktop/h3`, `Desktop/label`
<!-- ⚙️ GENERATED:end:library -->

- **Propósito:** Rejilla del catálogo de recetas: cards de Recipe card en 4 columnas en escritorio, 2 en tablet y 1 en móvil, y debajo Pagination en lugar de «ver más». La cabecera (Library head) va encima, fuera de este patrón. Solo recetas: los productos ya no van en Library (son Product line con anclas).
- **Ejemplo de código:**
  ```html
  <section data-ds="library" class="library" aria-label="Recipes">
  <ul class="library__grid">
  <li><article class="recipe-card">
  <div class="recipe-card__media"><img src="../assets/images/placeholder.svg" alt=""></div>
  <div class="recipe-card__body">
  <p class="recipe-card__meta">2 people · <span class="icon icon-timer" aria-hidden="true"></span>20 minutes</p>
  <h3 class="recipe-card__title"><a class="recipe-card__link" href="/recetas/spicy-noodle-salad">Spicy Noodle Salad with almond and mint</a></h3>
  <ul class="recipe-card__products" aria-label="Products used in this recipe"><li><a class="chip" href="/productos/cup-oriental">Cup Oriental</a></li></ul>
  </div>
  </article></li>
  </ul>
  <div class="library__more"><nav class="pagination" aria-label="Pagination">
  <ul class="pagination__list">
  <li><button class="pagination__link" type="button" disabled aria-label="Previous page"><span class="icon icon-arrow-left" aria-hidden="true"></span><span class="pagination__text">Previous</span></button></li>
  <li><a class="pagination__link pagination__page" href="?page=1" aria-current="page">1</a></li>
  <li><a class="pagination__link pagination__page" href="?page=2">2</a></li>
  <li><a class="pagination__link pagination__page" href="?page=3">3</a></li>
  <li><span class="pagination__ellipsis" aria-hidden="true">…</span></li>
  <li><a class="pagination__link pagination__page" href="?page=13">13</a></li>
  <li><a class="pagination__link" href="?page=2" aria-label="Next page"><span class="pagination__text">Next</span><span class="icon icon-arrow-right" aria-hidden="true"></span></a></li>
  </ul>
  <p class="pagination__status">Page 1 of 13</p>
  </nav></div>
  </section>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** La rejilla es un `ul` con un `li` por receta; cada card es un `article` con su título en `h3`, y el enlace del título es su nombre accesible. La sección lleva nombre («Recipes»). La paginación es un `nav` propio con nombre «Pagination»; la página actual va con `aria-current="page"` (ver Pagination). El patrón no tiene JavaScript: al cambiar de página, la página debe mover el foco al inicio de la rejilla y anunciar la página nueva («Page 2 of 13»). Teclado: Tab recorre los enlaces de las cards y después la paginación.
- **Cuándo usar / qué NO hace:** Para el catálogo de recetas (Recipe library), debajo de Library head. Solo recetas: el filtro de producto (Product filter) está retirado y los productos se muestran con Product line y anclas. No es el módulo de productos ni un listado de concursos.
