### Product details   ⚙️ synced: 2026-10-07T18:30:51Z

<!-- ⚙️ GENERATED:start:product-details -->
- **Figma:** `94:329` · página «Pattern / Product details» · COMPONENT_SET · 2 variantes · última sync 2026-10-07T18:30:51Z
- **Descripción (Figma):** Sección de ingredientes y nutrición (página de producto; en la receta se usa con los valores de la receta): título (h2) · Ingredients (lista jerarquizada, alérgenos en negrita, Link «Ver etiqueta del envase» que abre Modal L con la imagen de la etiqueta) · Nutrition panel (barras proporcionales al % IR, alérgenos y nota de validación). Ancla destino de «Ver ingredientes» del Product hero. Desktop: dos columnas iguales; Mobile: ingredientes y después nutrición. Valores de ejemplo hasta tener los validados por Nutrición de GB Foods. Sin variables propias.
- **Anatomía:** `ingredients` → Ingredients, `ingredient-main` → Level=Main, `ingredient-secondary` → Level=Secondary, `label-link` → Type=Standalone, Surface=Light, State=Default, `icon-trailing` → Icon / arrow-right, `nutrition-panel` → Nutrition panel, `nutrition-bar` → Highlight=False, `nutrition-bar` → Highlight=True, `claim` → Type=Natural
- **Breakpoint:** Desktop, Mobile
- **Propiedades de componente:** `Breakpoint` (VARIANT, por defecto Desktop)
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `badge/natural/bg`, `badge/natural/text`, `border/width/thin`, `color/surface/card`, `color/text/default`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/desktop/h2`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/line-height/mobile/label`, `font/size/desktop/body-l`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/desktop/h2`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/size/mobile/label`, `font/style/body`, `font/style/display`, `icon/size/sm`, `ingredient/divider`, `ingredient/meta`, `ingredient/percent-bg`, `ingredient/percent-text`, `ingredient/text`, `layout/frame`, `layout/margin`, `layout/section-y`, `link/default`, `nutrition/allergen`, `nutrition/bg`, `nutrition/border`, `nutrition/fill`, `nutrition/fill-highlight`, `nutrition/label`, `nutrition/meta`, `nutrition/track`, `nutrition/value`, `radius/md`, `radius/pill`, `space/16`, `space/24`, `space/32`, `space/4`, `space/48`, `space/64`, `space/8`
- **Text styles:** `Desktop/h2`, `Desktop/h3`, `Desktop/label`, `Desktop/caption`, `Desktop/body-m`, `Mobile/label`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `badge/natural/bg`, `badge/natural/text`, `color/surface/card`, `color/text/default`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/desktop/h2`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/line-height/mobile/label`, `font/size/desktop/body-l`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/desktop/h2`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/size/mobile/label`, `font/style/body`, `font/style/display`, `ingredient/divider`, `ingredient/meta`, `ingredient/percent-bg`, `ingredient/percent-text`, `ingredient/text`, `link/default`, `nutrition/allergen`, `nutrition/bg`, `nutrition/border`, `nutrition/fill`, `nutrition/fill-highlight`, `nutrition/label`, `nutrition/meta`, `nutrition/track`, `nutrition/value`
<!-- ⚙️ GENERATED:end:product-details -->

- **Propósito:** Sección de ingredientes y nutrición de la página de producto (y de receta).
- **Ejemplo de código:**
  ```html
  <section class="section product-details" id="ingredientes" aria-labelledby="pd-title">
  <div class="section__inner">
  <h2 class="section__title" id="pd-title">Ingredientes y nutrición</h2>
  <div class="product-details__grid">
  <section class="ingredients" aria-label="Ingredientes"><ul class="ingredients__list"><li class="ingredient-item">Fideos de <strong>trigo</strong><span class="ingredient-item__percent">52 %</span></li></ul></section>
  <section class="nutrition-panel" aria-label="Nutrición"><ul class="nutrition-panel__list"><li class="nutrition-bar nutrition-bar--highlight"><div class="nutrition-bar__row"><span class="nutrition-bar__label">Sal <span class="badge badge--natural">−20 %</span></span><span class="nutrition-bar__value">1,9 g<span class="nutrition-bar__percent">32 % IR</span></span></div><meter class="nutrition-bar__meter" min="0" max="100" value="32" aria-hidden="true"></meter></li></ul></section>
  </div>
  </div>
  </section>
  ```
- **Accesibilidad (pares AA verificados):** Título tinta sobre blanco 18,7:1; el resto, los pares de Ingredients y Nutrition panel. Es el ancla de «Ver ingredientes». En móvil, ingredientes y después nutrición, en el orden de lectura.
- **Cuándo usar / qué NO hace:** En las páginas de producto y receta. Los valores de ejemplo no se publican: los valida Nutrición de GB Foods.
