### Recipe ingredients   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:recipe-ingredients -->
- **Figma:** `222:2116` · página «Pattern / Detail pages» · COMPONENT_SET · 2 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** Recipe ingredients: bloque de ingredientes de la ficha de receta. Título «Ingredients» con subtítulo, lista de Recipe ingredient (2 columnas en desktop, 1 en mobile; Variant=Brand para los productos del catálogo) y Recipe macros a la derecha (desktop) o debajo (mobile). Fondo blanco (surface/card). Uso: ficha de receta (wireframe desktop 396:6398, 396:6354). Clase CSS: .recipe-ingredients.
- **Anatomía:** `Recipe ingredient` → Variant=Brand, `Recipe ingredient` → Variant=Brand, `Recipe ingredient` → Variant=Default, `Recipe ingredient` → Variant=Default, `Recipe ingredient` → Variant=Default, `Recipe ingredient` → Variant=Default, `macros` → Recipe macros, `allergen-button` → Hierarchy=Secondary, Size=M, State=Default, `icon-leading` → Icon / arrow-right, `icon-trailing` → Icon / arrow-right
- **API:** `breakpoint`: Desktop, Mobile (por defecto Desktop)
- **Nombres en Figma:** `breakpoint` ← `Breakpoint`
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `border/width/thick`, `button/secondary/border`, `button/secondary/text`, `color/border/default`, `color/surface/card`, `color/surface/inverse`, `color/text/default`, `color/text/on-inverse`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/desktop/h2`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/size/desktop/body-l`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/desktop/h2`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/sm`, `product-card/media-bg`, `radius/md`, `radius/pill`, `space/16`, `space/24`, `space/32`, `space/4`, `space/64`, `space/8`, `space/80`
- **Text styles:** `Desktop/h2`, `Desktop/body-m`, `Desktop/caption`, `Desktop/h3`, `Desktop/label`
<!-- ⚙️ GENERATED:end:recipe-ingredients -->

- **Propósito:** Sección de ingredientes de la página de receta: título «Ingredients», subtítulo («Everything you need to make this recipe for 4 people.»), la lista de ingredientes a la izquierda y Recipe macros a la derecha. Un ingrediente que es producto de la marca (Recipe ingredient, Type Brand) enlaza a su ficha dentro de la lista.
- **Ejemplo de código:**
  ```html
  <section data-ds="recipe-ingredients" class="section recipe-ingredients" aria-labelledby="ri-title">
  <div class="section__header">
  <h2 class="section__title" id="ri-title">Ingredients</h2>
  <p class="section__lead">Everything you need to make this recipe for 4 people.</p>
  </div>
  <div class="recipe-ingredients__body">
  <ul class="recipe-ingredients__list">
  <li class="recipe-ingredient"><div class="recipe-ingredient__info"><p class="recipe-ingredient__amount">150 g</p><p class="recipe-ingredient__name">Chicken breast</p></div></li>
  <li class="recipe-ingredient recipe-ingredient--brand"><div class="recipe-ingredient__info"><p class="recipe-ingredient__amount">200 g</p><p class="recipe-ingredient__name"><a class="recipe-ingredient__link" href="/productos/cup-oriental">Cup Oriental</a></p></div><img class="recipe-ingredient__thumb" src="../assets/images/placeholder.svg" alt=""></li>
  </ul>
  <section class="recipe-macros" aria-labelledby="ri-macros">
  <h3 class="recipe-macros__title" id="ri-macros">Recipe macros</h3>
  <p class="recipe-macros__head">Per serving</p>
  <ul class="recipe-macros__list">
  <li class="recipe-macros__row"><span class="recipe-macros__name">Protein</span><span class="recipe-macros__value">8.3 g</span></li>
  <li class="recipe-macros__row"><span class="recipe-macros__name">Carbohydrates</span><span class="recipe-macros__value">52 g</span></li>
  <li class="recipe-macros__row"><span class="recipe-macros__name">Fat</span><span class="recipe-macros__value">10 g</span></li>
  </ul>
  <button class="button button--secondary recipe-macros__action" type="button" aria-haspopup="dialog">See allergen table</button>
  </section>
  </div>
  </section>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Rol: sección con nombre por su h2 (`aria-labelledby`). La lista de ingredientes es un `ul` con un `li` por ingrediente; cantidad y nombre van en el mismo elemento, en ese orden. Recipe macros es un bloque con su título h3 («Recipe macros»), que sigue al h2 de la sección; el encabezado «Per serving» se lee antes de la lista de macros. Los ingredientes Brand son enlaces con el nombre del producto y la miniatura va con `alt=""`. Orden de tabulación: enlaces de la lista y después el botón «See allergen table». En móvil, las macros van debajo de la lista con el mismo orden de lectura.
- **Cuándo usar / qué NO hace:** Una vez por receta, justo después de la cabecera (Recipe hero) y antes de Recipe steps. No es la ficha de producto (Product details) ni la preparación de la receta (eso es Recipe steps).
