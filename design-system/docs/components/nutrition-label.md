### Nutrition label   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:nutrition-label -->
- **Figma:** `194:249` · página «Content» · COMPONENT · 1 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** Tabla nutricional de la UE (Reg. 1169/2011), no el formato de EE. UU.: contenido del modal «Pack label». Columnas: Per 100 g · Per serving (93.6 g) · %RI*. Filas: Energy (kJ / kcal), Fat, of which saturates, Carbohydrate, of which sugars, Fibre, Protein, Salt; las filas «of which» van sangradas. Filetes gruesos de tinta bajo el título y antes del pie; filetes finos entre filas. Pie: «*Reference intake of an average adult (8,400 kJ / 2,000 kcal).». Valores de ejemplo coherentes, no validados. Se abre desde el enlace «Still curious? View pack label» de Ingredients (wireframe UX 490:11998). Clase CSS: .nutrition-label. Formato UE (Reg. 1169/2011) por decisión de David Reina 2026-10-22; ⬜ TODO confirmar con GB Foods.
- **Anatomía:** sin instancias anidadas
- **API:** sin propiedades
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `border/width/thick`, `border/width/thin`, `color/border/default`, `color/text/default`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `nutrition/bg`, `nutrition/border`, `space/16`, `space/24`, `space/8`
- **Text styles:** `Desktop/h3`, `Desktop/label`, `Desktop/body-m`, `Desktop/caption`
<!-- ⚙️ GENERATED:end:nutrition-label -->
- **Ejemplo de código:**
  ```html
  <table data-ds="nutrition-label" class="nutrition-label">
  <caption class="nutrition-label__caption">Nutrition information</caption>
  <thead><tr><th scope="col"><span class="visually-hidden">Nutrient</span></th><th scope="col">Per 100 g</th><th scope="col">Per serving (93.6 g)</th><th scope="col">%RI*</th></tr></thead>
  <tbody>
  <tr><th scope="row">Energy</th><td>1,850 kJ / 442 kcal</td><td>1,732 kJ / 414 kcal</td><td>21 %</td></tr>
  <tr><th scope="row">Fat</th><td>16 g</td><td>15 g</td><td>21 %</td></tr>
  <tr><th scope="row" class="nutrition-label__sub">of which saturates</th><td>1.5 g</td><td>1.4 g</td><td>7 %</td></tr>
  <tr><th scope="row">Carbohydrate</th><td>62 g</td><td>58 g</td><td>22 %</td></tr>
  <tr><th scope="row" class="nutrition-label__sub">of which sugars</th><td>3.2 g</td><td>3.0 g</td><td>3 %</td></tr>
  <tr><th scope="row">Fibre</th><td>1.9 g</td><td>1.8 g</td><td>–</td></tr>
  <tr><th scope="row">Protein</th><td>10 g</td><td>9.4 g</td><td>19 %</td></tr>
  <tr><th scope="row">Salt</th><td>1.9 g</td><td>1.8 g</td><td>30 %</td></tr>
  </tbody>
  </table>
  <p class="nutrition-label__note">*Reference intake of an average adult (8,400 kJ / 2,000 kcal).</p>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Tabla de datos real: `caption` con el título, `th scope="col"` para las cabeceras de columna y `th scope="row"` para cada nutriente. Las filas «of which» llevan `nutrition-label__sub` (sangría visual): su relación con la fila superior va en el texto, no solo en la sangría. El valor de cada celda se lee con su cabecera. Texto tinta sobre blanco 18,7:1; filetes de tinta. El pie es un párrafo aparte, no una fila.
- **Cuándo usar / qué NO hace:** Solo dentro del modal «Pack label», abierto desde «View pack label» en Ingredients. No sustituye a Nutrition bar ni a Nutrition ring: la tabla es la cifra oficial del envase.
