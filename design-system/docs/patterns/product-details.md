### Product details   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:product-details -->
- **Figma:** `94:329` · página «Pattern / Detail pages» · COMPONENT_SET · 2 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** Sección de ingredientes y nutrición (página de producto; en la receta se usa con los valores de la receta): título (h2) · Ingredients (lista jerarquizada, alérgenos en negrita, Link «Ver etiqueta del envase» que abre Modal L con la imagen de la etiqueta) · Nutrition panel (barras proporcionales al % IR, alérgenos y nota de validación). Ancla destino de «Ver ingredientes» del Product hero. Desktop: dos columnas iguales; Mobile: ingredientes y después nutrición. Valores de ejemplo hasta tener los validados por Nutrición de GB Foods. Sin variables propias.
- **Anatomía:** `ingredients` → Ingredients, `ingredient-main` → Level=Main, `ingredient-main` → Level=Main, `ingredient-main` → Level=Main, `label-link` → Type=Standalone, Surface=Light, State=Default, `icon-trailing` → Icon / arrow-right, `nutrition-ring` → Variant=Default, Breakpoint=Desktop, `nutrition-ring` → Variant=Default, Breakpoint=Desktop, `nutrition-ring` → Variant=Default, Breakpoint=Desktop, `nutrition-ring` → Variant=Default, Breakpoint=Desktop, `nutrition-ring` → Variant=Default, Breakpoint=Desktop, `nutrition-ring` → Variant=Highlight, Breakpoint=Desktop, `allergen-card` → Allergen card, `allergen-card` → Allergen card, `allergen-card` → Allergen card, `table-link` → Type=Standalone, Surface=Light, State=Default, `icon-trailing` → Icon / arrow-right
- **API:** `breakpoint`: Desktop, Mobile (por defecto Desktop)
- **Nombres en Figma:** `breakpoint` ← `Breakpoint`
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `border/width/thin`, `color/border/subtle`, `color/surface/card`, `color/surface/page`, `color/text/default`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-m`, `font/line-height/desktop/body-s`, `font/line-height/desktop/caption`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/size/desktop/body-m`, `font/size/desktop/body-s`, `font/size/desktop/caption`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/sm`, `ingredient/meta`, `ingredient/text`, `layout/frame`, `link/default`, `nutrition/bg`, `nutrition/border`, `nutrition/fill`, `nutrition/fill-highlight`, `nutrition/label`, `nutrition/track`, `nutrition/value`, `radius/lg`, `radius/md`, `space/16`, `space/24`, `space/4`, `space/48`, `space/64`, `space/8`, `space/80`
- **Text styles:** `Desktop/h3`, `Desktop/body-s`, `Desktop/caption`, `Desktop/label`, `Desktop/body-m`
<!-- ⚙️ GENERATED:end:product-details -->

- **Propósito:** Ingredientes y nutrición de la página de producto, en dos secciones a sangre: Ingredients sobre crema (con foto a la izquierda en escritorio) y Nutritional information sobre blanco (seis anillos de ingesta, «Main allergens» con tres tarjetas y enlace a la tabla completa). Sustituye al panel de nutrición.
- **Ejemplo de código:**
  ```html
  <div data-ds="product-details" class="product-details">
  <section class="section product-details__ingredients">
  <div class="section__inner">
  <div class="product-details__grid">
  <div class="product-details__media"><img src="assets/images/placeholder.svg" alt=""></div>
  <section class="ingredients" aria-labelledby="ing-title-2">
  <h2 class="ingredients__title" id="ing-title-2">Ingredients</h2>
  <p class="ingredients__note">100% natural with nothing added. We'll give you all the details.</p>
  <ul class="ingredients__list">
  <li class="ingredient-item"><span class="ingredient-item__percent">79% of content</span><span class="ingredient-item__name">Oriental noodles</span><span class="ingredient-item__text"><strong>Wheat</strong> flour, modified starch, salt, sodium and potassium carbonate</span></li>
  <li class="ingredient-item ingredient-item--secondary">Others: salt, spices, <strong>soy</strong> sauce (<strong>soy</strong>, <strong>wheat</strong>), garlic and onion.</li>
  </ul>
  <p class="ingredients__more">Still curious? <a class="link link--standalone ingredients__link" href="#etiqueta" aria-haspopup="dialog">View pack label <span class="icon icon-arrow-right" aria-hidden="true"></span></a></p>
  </section>
  </div>
  </div>
  </section>
  <section class="section product-details__nutrition" aria-labelledby="nut-title">
  <div class="section__inner">
  <div class="product-details__allergens-head">
  <h2 class="section__title" id="nut-title">Nutritional information</h2>
  <p class="product-details__lead">Per 100 g · % of the reference intake</p>
  </div>
  <ul class="nutrition-rings" tabindex="0" aria-label="Nutrition per 100 g (scroll to see all)">
  <li class="nutrition-ring"><div class="nutrition-ring__dial"><svg class="nutrition-ring__svg" viewBox="0 0 100 100" role="img" aria-label="Energy 380 kcal, 19 % of the reference intake"><circle class="nutrition-ring__track" cx="50" cy="50" r="40" pathLength="100"/><circle class="nutrition-ring__fill" cx="50" cy="50" r="40" pathLength="100" stroke-dasharray="19 100"/></svg><span class="nutrition-ring__value" aria-hidden="true">19 %</span></div><span class="nutrition-ring__name" aria-hidden="true">Energy</span><span class="nutrition-ring__amount" aria-hidden="true">380 kcal</span></li>
  <li class="nutrition-ring"><div class="nutrition-ring__dial"><svg class="nutrition-ring__svg" viewBox="0 0 100 100" role="img" aria-label="Protein 8.3 g, 17 % of the reference intake"><circle class="nutrition-ring__track" cx="50" cy="50" r="40" pathLength="100"/><circle class="nutrition-ring__fill" cx="50" cy="50" r="40" pathLength="100" stroke-dasharray="17 100"/></svg><span class="nutrition-ring__value" aria-hidden="true">17 %</span></div><span class="nutrition-ring__name" aria-hidden="true">Protein</span><span class="nutrition-ring__amount" aria-hidden="true">8.3 g</span></li>
  <li class="nutrition-ring"><div class="nutrition-ring__dial"><svg class="nutrition-ring__svg" viewBox="0 0 100 100" role="img" aria-label="Carbohydrates 52 g, 20 % of the reference intake"><circle class="nutrition-ring__track" cx="50" cy="50" r="40" pathLength="100"/><circle class="nutrition-ring__fill" cx="50" cy="50" r="40" pathLength="100" stroke-dasharray="20 100"/></svg><span class="nutrition-ring__value" aria-hidden="true">20 %</span></div><span class="nutrition-ring__name" aria-hidden="true">Carbohydrates</span><span class="nutrition-ring__amount" aria-hidden="true">52 g</span></li>
  <li class="nutrition-ring"><div class="nutrition-ring__dial"><svg class="nutrition-ring__svg" viewBox="0 0 100 100" role="img" aria-label="Fat 15 g, 21 % of the reference intake"><circle class="nutrition-ring__track" cx="50" cy="50" r="40" pathLength="100"/><circle class="nutrition-ring__fill" cx="50" cy="50" r="40" pathLength="100" stroke-dasharray="21 100"/></svg><span class="nutrition-ring__value" aria-hidden="true">21 %</span></div><span class="nutrition-ring__name" aria-hidden="true">Fat</span><span class="nutrition-ring__amount" aria-hidden="true">15 g</span></li>
  <li class="nutrition-ring"><div class="nutrition-ring__dial"><svg class="nutrition-ring__svg" viewBox="0 0 100 100" role="img" aria-label="Fibre 1.9 g, 8 % of the reference intake"><circle class="nutrition-ring__track" cx="50" cy="50" r="40" pathLength="100"/><circle class="nutrition-ring__fill" cx="50" cy="50" r="40" pathLength="100" stroke-dasharray="8 100"/></svg><span class="nutrition-ring__value" aria-hidden="true">8 %</span></div><span class="nutrition-ring__name" aria-hidden="true">Fibre</span><span class="nutrition-ring__amount" aria-hidden="true">1.9 g</span></li>
  <li class="nutrition-ring nutrition-ring--highlight"><div class="nutrition-ring__dial"><svg class="nutrition-ring__svg" viewBox="0 0 100 100" role="img" aria-label="Salt 2.3 g, 38 % of the reference intake"><circle class="nutrition-ring__track" cx="50" cy="50" r="40" pathLength="100"/><circle class="nutrition-ring__fill" cx="50" cy="50" r="40" pathLength="100" stroke-dasharray="38 100"/></svg><span class="nutrition-ring__value" aria-hidden="true">38 %</span></div><span class="nutrition-ring__name" aria-hidden="true">Salt</span><span class="nutrition-ring__amount" aria-hidden="true">2.3 g</span></li>
  </ul>
  <div class="product-details__allergens">
  <h3 class="product-details__subtitle">Main allergens</h3>
  <ul class="allergen-cards">
  <li class="allergen-card"><p class="allergen-card__name">Gluten or derivatives</p><p class="allergen-card__note">Not suitable for coeliacs</p></li>
  <li class="allergen-card"><p class="allergen-card__name">Nuts</p><p class="allergen-card__note">May contain traces</p></li>
  <li class="allergen-card"><p class="allergen-card__name">Eggs</p><p class="allergen-card__note">Contains preparations</p></li>
  </ul>
  <a class="link link--standalone" href="#alergenos" aria-haspopup="dialog">To see all allergens · Check the detailed table <span class="icon icon-arrow-right" aria-hidden="true"></span></a>
  </div>
  </div>
  </section>
  </div>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Dos secciones con su título (`h2`); «Main allergens» es `h3` dentro de la de nutrición. El carrusel de anillos en móvil es un `ul` con `tabindex="0"` y `aria-label` para que el teclado llegue a él y se pueda desplazar; el foco tiene anillo visible. Cada anillo es un SVG `role="img"` con su nombre completo. Los enlaces a los modales llevan `aria-haspopup="dialog"`. Orden de lectura: ingredientes, nutrición, alérgenos, como en la página. Contraste: tinta sobre crema 17,2:1 y sobre blanco 18,7:1; gris cálido sobre blanco 5,9:1.
- **Cuándo usar / qué NO hace:** En las páginas de producto y receta. Los valores de ejemplo no se publican: los valida Nutrición de GB Foods. En móvil se oculta la foto de ingredientes (la del wireframe).
