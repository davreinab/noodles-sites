### Nutrition panel   ⚙️ synced: 2026-10-07T18:43:11Z

<!-- ⚙️ GENERATED:start:nutrition-panel -->
- **Figma:** `71:75` · página «Nutrition» · COMPONENT · 1 variantes · última sync 2026-10-07T18:43:11Z
- **Descripción (Figma):** Panel de nutrición de la página de producto y de receta: título (h3) · base (por 100 g, % IR) · 7 Nutrition bar (energía, grasas, saturadas, hidratos, azúcares, proteínas, sal; Highlight en los claims del pack) · alérgenos en negrita · nota de validación. Accesible como lista de pares nutriente/valor (o &lt;table&gt; con &lt;caption&gt;); las barras son aria-hidden. Valores de ejemplo hasta tener los validados por Nutrición de GB Foods.
- **Anatomía:** `nutrition-bar` → Highlight=False, `nutrition-bar` → Highlight=True, `claim` → Type=Natural
- **Propiedades de componente:** ninguna
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `badge/natural/bg`, `badge/natural/text`, `border/width/thin`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/desktop/h3`, `font/line-height/mobile/label`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/desktop/h3`, `font/size/mobile/label`, `font/style/body`, `font/style/display`, `nutrition/allergen`, `nutrition/bg`, `nutrition/border`, `nutrition/fill`, `nutrition/fill-highlight`, `nutrition/label`, `nutrition/meta`, `nutrition/track`, `nutrition/value`, `radius/md`, `radius/pill`, `space/16`, `space/24`, `space/32`, `space/4`, `space/8`
- **Text styles:** `Desktop/h3`, `Desktop/caption`, `Desktop/body-m`, `Mobile/label`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `badge/natural/bg`, `badge/natural/text`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/desktop/h3`, `font/line-height/mobile/label`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/desktop/h3`, `font/size/mobile/label`, `font/style/body`, `font/style/display`, `nutrition/allergen`, `nutrition/bg`, `nutrition/border`, `nutrition/fill`, `nutrition/fill-highlight`, `nutrition/label`, `nutrition/meta`, `nutrition/track`, `nutrition/value`
<!-- ⚙️ GENERATED:end:nutrition-panel -->

- **Propósito:** Panel de nutrición de la página de producto y de receta: base por 100 g, barras por nutriente, alérgenos en negrita y nota de validación.
- **Ejemplo de código:**
  ```html
  <section class="nutrition-panel" aria-labelledby="nut-title">
  <h3 class="nutrition-panel__title" id="nut-title">Nutrición</h3>
  <p class="nutrition-panel__base">Por 100 g · % de la ingesta de referencia de un adulto medio (8.400 kJ / 2.000 kcal).</p>
  <ul class="nutrition-panel__list">
  <li class="nutrition-bar"><div class="nutrition-bar__row"><span class="nutrition-bar__label">Grasas</span><span class="nutrition-bar__amount"><span class="nutrition-bar__value">16 g</span><span class="nutrition-bar__percent">23 % IR</span></span></div><meter class="nutrition-bar__meter" min="0" max="100" value="23" aria-hidden="true"></meter></li>
  <li class="nutrition-bar nutrition-bar--highlight"><div class="nutrition-bar__row"><span class="nutrition-bar__label">Sal</span><span class="nutrition-bar__amount"><span class="badge badge--natural">−20 %</span><span class="nutrition-bar__value">1,9 g</span><span class="nutrition-bar__percent">32 % IR</span></span></div><meter class="nutrition-bar__meter" min="0" max="100" value="32" aria-hidden="true"></meter></li>
  </ul>
  <p class="nutrition-panel__allergens"><strong>Alérgenos:</strong> contiene <strong>trigo</strong> y <strong>soja</strong>.</p>
  <p class="nutrition-panel__note">Valores validados por el equipo de Nutrición de GB Foods.</p>
  </section>
  ```
- **Accesibilidad (pares AA verificados):** Texto tinta sobre blanco 18,7:1; base y nota en gris cálido sobre blanco 5,9:1; borde de tinta. Rol: sección con encabezado; las barras son una lista de pares nutriente/valor (alternativa equivalente a una tabla con `<caption>`). Alérgenos con `<strong>`.
- **Cuándo usar / qué NO hace:** En Product details. No se publica con valores sin validar por Nutrición de GB Foods; los del maestro son de ejemplo.
