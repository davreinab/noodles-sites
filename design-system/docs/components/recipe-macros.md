### Recipe macros   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:recipe-macros -->
- **Figma:** `222:1907` · página «Content» · COMPONENT · 1 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** Recipe macros: resumen nutricional por ración de la receta (Protein, Carbohydrates, Fat) con valor grande (Desktop/h3) y botón Secondary «See allergen table» que abre el modal Allergen table. Ubicado a la derecha de Recipe ingredients en desktop y debajo en mobile. Uso: Recipe ingredients (ficha de receta, wireframe 396:6398). Clase CSS: .recipe-macros.
- **Anatomía:** `allergen-button` → Hierarchy=Secondary, Size=M, State=Default, `icon-leading` → Icon / arrow-right, `icon-trailing` → Icon / arrow-right
- **API:** sin propiedades
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `border/width/thick`, `button/secondary/border`, `button/secondary/text`, `color/border/default`, `color/surface/card`, `color/text/default`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/size/desktop/body-l`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/sm`, `radius/md`, `radius/pill`, `space/16`, `space/24`, `space/8`
- **Text styles:** `Desktop/h3`, `Desktop/caption`, `Desktop/body-m`, `Desktop/label`
<!-- ⚙️ GENERATED:end:recipe-macros -->

- **Propósito:** Macronutrientes por ración de una receta: título «Recipe macros», encabezado «Per serving» y tres filas (Protein, Carbohydrates, Fat) con el valor en negrita. Debajo, el botón secondary «See allergen table» abre el modal de la tabla de alérgenos (ALLERGEN TABLE, referencia allergen-table).
- **Ejemplo de código:**
  ```html
  <section data-ds="recipe-macros" class="recipe-macros" aria-labelledby="recipe-macros-title">
  <h2 class="recipe-macros__title" id="recipe-macros-title">Recipe macros</h2>
  <p class="recipe-macros__head">Per serving</p>
  <ul class="recipe-macros__list">
  <li class="recipe-macros__row"><span class="recipe-macros__name">Protein</span><span class="recipe-macros__value">8.3 g</span></li>
  <li class="recipe-macros__row"><span class="recipe-macros__name">Carbohydrates</span><span class="recipe-macros__value">52 g</span></li>
  <li class="recipe-macros__row"><span class="recipe-macros__name">Fat</span><span class="recipe-macros__value">10 g</span></li>
  </ul>
  <button class="button button--secondary recipe-macros__action" type="button" aria-haspopup="dialog">See allergen table</button>
  </section>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Rol: sección con nombre por su título (`aria-labelledby`). Las filas son `ul`/`li`, y nombre y valor van dentro de la misma fila: un lector lee «Protein 8.3 g». «Per serving» es el encabezado de columna y se lee antes de la lista. Botón: `button` con nombre visible; `aria-haspopup="dialog"` anuncia que abre un modal. Al cerrar el modal, el foco vuelve al botón (lo gestiona el modal). Teclado: Tab llega al botón; Enter o Espacio lo abren. Pares texto/fondo: las cifras de contraste las mide ds-fidelity y no constan aquí.
- **Cuándo usar / qué NO hace:** Para los macros por ración de una receta. No calcula valores: los pone el contenido. No sustituye la tabla nutricional completa del envase (eso es Nutrition label) ni la tabla de alérgenos, que va en su modal.
