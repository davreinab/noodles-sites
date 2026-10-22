### Nutrition ring   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:nutrition-ring -->
- **Figma:** `193:209` · página «Content» · COMPONENT_SET · 4 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** Anillo de nutriente de la ficha de producto: porcentaje de la ingesta de referencia (IR) en el centro (display), nombre del nutriente debajo (body) y valor (p. ej. 380 kcal). Pista = nutrition/track; relleno = nutrition/fill. Variant=Highlight usa nutrition/fill-highlight para un nutriente con claim (p. ej. sal reducida). Breakpoint: Desktop 148 px y Mobile 120 px (en mobile, carrusel horizontal con scroll-snap). Se usa en el módulo Nutrition de la ficha de producto (wireframe UX 396:6073). Clase CSS: .nutrition-ring. Accesible como role=img con aria-label, p. ej. «Energy 380 kcal, 19 % of the reference intake»; el anillo es decorativo y el dato accesible es el texto.
- **Anatomía:** sin instancias anidadas
- **API:** `percent` (string, por defecto 19 %) · `nutrient` (string, por defecto Energy) · `value` (string, por defecto 380 kcal) · `variant`: Default, Highlight (por defecto Default) · `breakpoint`: Desktop, Mobile (por defecto Desktop)
- **Nombres en Figma:** `percent` ← `Percent#193:3`, `nutrient` ← `Nutrient#193:8`, `value` ← `Value#193:13`, `variant` ← `Variant`, `breakpoint` ← `Breakpoint`
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `font/family/body`, `font/family/display`, `font/line-height/desktop/body-s`, `font/line-height/desktop/h3`, `font/size/desktop/body-s`, `font/size/desktop/h3`, `font/style/body`, `font/style/display`, `nutrition/fill`, `nutrition/label`, `nutrition/track`, `nutrition/value`, `space/16`, `space/4`
- **Text styles:** `Desktop/h3`, `Desktop/body-s`
<!-- ⚙️ GENERATED:end:nutrition-ring -->
- **Ejemplo de código:**
  ```html
  <li data-ds="nutrition-ring" class="nutrition-ring">
  <div class="nutrition-ring__dial">
  <svg class="nutrition-ring__svg" viewBox="0 0 100 100" role="img" aria-label="Energy 380 kcal, 19 % of the reference intake"><circle class="nutrition-ring__track" cx="50" cy="50" r="40" pathLength="100"/><circle class="nutrition-ring__fill" cx="50" cy="50" r="40" pathLength="100" stroke-dasharray="19 100"/></svg>
  <span class="nutrition-ring__value" aria-hidden="true">19 %</span>
  </div>
  <span class="nutrition-ring__name" aria-hidden="true">Energy</span>
  <span class="nutrition-ring__amount" aria-hidden="true">380 kcal</span>
  </li>
  <li data-ds="nutrition-ring" class="nutrition-ring nutrition-ring--highlight">
  <div class="nutrition-ring__dial">
  <svg class="nutrition-ring__svg" viewBox="0 0 100 100" role="img" aria-label="Salt 2.3 g, 38 % of the reference intake"><circle class="nutrition-ring__track" cx="50" cy="50" r="40" pathLength="100"/><circle class="nutrition-ring__fill" cx="50" cy="50" r="40" pathLength="100" stroke-dasharray="38 100"/></svg>
  <span class="nutrition-ring__value" aria-hidden="true">38 %</span>
  </div>
  <span class="nutrition-ring__name" aria-hidden="true">Salt</span>
  <span class="nutrition-ring__amount" aria-hidden="true">2.3 g</span>
  </li>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** El SVG es `role="img"` con `aria-label` completo («Energy 380 kcal, 19 % of the reference intake»): es el dato accesible. El %, el nombre y el valor visibles van con `aria-hidden` para no repetirlos. La pista (`--nutrition-track`) y el relleno de tinta se leen sobre blanco: el relleno de tinta da 18,7:1 sobre blanco; el relleno highlight (verde) da 4,0:1 sobre la pista arena, ≥ 3:1 para elementos gráficos. Sin color como único indicador: el % va escrito.
- **Cuándo usar / qué NO hace:** Dentro de la sección Nutritional information de Product details, en una lista (`ul`) de seis anillos. No sustituye a la tabla de la etiqueta (Nutrition label) ni al panel de barras (Nutrition bar): es la vista resumida de la ingesta de referencia.
