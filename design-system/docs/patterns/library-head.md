### Library head   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:library-head -->
- **Figma:** `219:1839` · página «Pattern / Libraries» · COMPONENT_SET · 4 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** Library head: cabecera de la Recipe library: título de página («Recipes»), subtítulo («Explore and learn recipes to level up your dishes.»), Search field («Search a recipe or ingredient», sin etiqueta visible: aria-label «Buscar» y role=search) y fila de chips de filtro (All, Less ingredients, Quick recipes, High protein, Single, +2 people, Spicy) con aria-pressed. State=Default: All seleccionado. State=Filtered: un chip seleccionado (Less ingredients), fila «48 results for your search» (48 en negrita) y «Clear filters» con Icon / trash a la derecha. Mobile: chips en fila desplazable. Fondo crema (surface/page). Uso: Recipe library (wireframe desktop 171:3808, estados 483:5711 y 485:6064; móvil 486:13025 y 265:3948). Clase CSS: .library-head (.library-head--filtered).
- **Anatomía:** `Search field` → State=Default, `icon-search` → Icon / search, `icon-clear` → Icon / close, `Chip` → Size=M, State=Selected, `icon-leading` → Icon / check, `Chip` → Size=M, State=Default, `icon-leading` → Icon / check, `Chip` → Size=M, State=Default, `icon-leading` → Icon / check, `Chip` → Size=M, State=Default, `icon-leading` → Icon / check, `Chip` → Size=M, State=Default, `icon-leading` → Icon / check, `Chip` → Size=M, State=Default, `icon-leading` → Icon / check, `Chip` → Size=M, State=Default, `icon-leading` → Icon / check
- **API:** `filtered` (boolean, por defecto false) · `breakpoint`: Desktop, Mobile (por defecto Desktop)
- **Nombres en Figma:** `filtered` ← `State=Filtered`, `breakpoint` ← `Breakpoint`
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `border/width/thin`, `chip/bg`, `chip/bg-selected`, `chip/border`, `chip/height/m`, `chip/text`, `chip/text-selected`, `color/surface/page`, `color/text/default`, `color/text/secondary`, `field/bg`, `field/border`, `field/icon`, `field/placeholder`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/body-m`, `font/line-height/desktop/body-s`, `font/line-height/desktop/h1`, `font/size/desktop/body-l`, `font/size/desktop/body-m`, `font/size/desktop/body-s`, `font/size/desktop/h1`, `font/style/body`, `font/style/display`, `icon/size/md`, `icon/size/sm`, `radius/pill`, `space/16`, `space/24`, `space/48`, `space/64`, `space/8`
- **Text styles:** `Desktop/h1`, `Desktop/body-l`, `Desktop/body-m`, `Desktop/body-s`
<!-- ⚙️ GENERATED:end:library-head -->

- **Propósito:** Cabecera de la Recipe library: título «Recipes», subtítulo, buscador y fila de chips de filtro (All, Less ingredients, Quick recipes, High protein…). Tiene dos estados. Default, sin filtro: solo título, buscador y chips. Filtered, con filtros activos: la fila de resultados («48 results for your search») a la izquierda y «Clear filters» con icono de papelera a la derecha. Si la búsqueda o los filtros no devuelven recetas, la rejilla se sustituye por Empty state; la cabecera se queda.
- **Ejemplo de código:**
  ```html
  <section data-ds="library-head" class="section library-head" aria-labelledby="lhead-title">
  <div class="library-head__inner">
  <div class="library-head__intro">
  <h1 class="page-title" id="lhead-title">Recipes</h1>
  <p class="library-head__lead">Explore and learn recipes to level up your dishes.</p>
  </div>
  <form class="search-field library-head__search" role="search" action="/recipes">
  <span class="icon icon-search" aria-hidden="true"></span>
  <label class="visually-hidden" for="lhead-q">Search a recipe or ingredient</label>
  <input class="search-field__input" id="lhead-q" name="q" type="search" placeholder="Search a recipe or ingredient">
  </form>
  <ul class="library-head__filters" aria-label="Filter recipes">
  <li><button class="chip" type="button" aria-pressed="true"><span class="icon icon-check" aria-hidden="true"></span>All</button></li>
  <li><button class="chip" type="button" aria-pressed="false">Less ingredients</button></li>
  <li><button class="chip" type="button" aria-pressed="false">Quick recipes</button></li>
  <li><button class="chip" type="button" aria-pressed="false">High protein</button></li>
  </ul>
  <div class="library-head__results">
  <p aria-live="polite"><strong>48</strong> results for your search</p>
  <button class="link" type="button"><span class="icon icon-trash" aria-hidden="true"></span>Clear filters</button>
  </div>
  </div>
  </section>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Rol: sección con nombre por su h1 (`aria-labelledby`). El buscador es un `form role="search"` con etiqueta oculta («Search a recipe or ingredient») y `input type="search"`. Cada chip es un `button` con `aria-pressed`: «true» cuando el filtro está activo y «false» cuando no; el lector anuncia ese estado y el relleno tinta solo lo refuerza. El icono de check es decorativo. El recuento va en un `p` con `aria-live="polite"`, así que «48 results for your search» se anuncia al cambiar los filtros; «Clear filters» queda fuera de esa región para que no se lea junto al recuento. Teclado: Tab recorre el buscador, los chips en orden y «Clear filters»; Enter o Espacio conmutan un chip y el foco se queda en él. Al pulsar «Clear filters» la fila de resultados desaparece, así que el foco va al chip «All», que vuelve a quedar activo. Móvil: la fila de chips es desplazable y el chip enfocado se mantiene a la vista.
- **Cuándo usar / qué NO hace:** Solo en la Recipe library (catálogo de recetas). Los chips filtran la rejilla: no son pestañas, no cambian de vista ni de sección. No es un buscador global del sitio y no sirve para productos: el catálogo de productos usa Library hero, Anchor nav y Product line.
