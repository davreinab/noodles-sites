### Ingredient item   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:ingredient-item -->
- **Figma:** `70:58` · página «Content» · COMPONENT_SET · 2 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** Tarjeta de ingrediente (punto 6 de la SPEC, wireframe UX 396:6073 en el archivo 1YhsCqdqYCHlK4Y82IY5G3). Fondo color/surface/card, borde fino color/border/subtle, radio md, padding 16/24. Level=Main: línea de porcentaje «79% of content» (caption, ingredient/meta), nombre (heading S) y composición (body S). Level=Secondary: resto de ingredientes en texto corrido (body S), sin línea de porcentaje. Los alérgenos van SIEMPRE en negrita (<strong>, Archivo Bold), también dentro de la composición. Los datos son de ejemplo; los reales se copian del envase.
- **Anatomía:** sin instancias anidadas
- **API:** `percent` (string, por defecto 79% of content) · `level`: Main, Secondary (por defecto Main)
- **Nombres en Figma:** `percent` ← `Percent#70:0`, `level` ← `Level`
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `border/width/thin`, `color/border/subtle`, `color/surface/card`, `color/text/default`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-s`, `font/line-height/desktop/caption`, `font/line-height/desktop/h3`, `font/size/desktop/body-s`, `font/size/desktop/caption`, `font/size/desktop/h3`, `font/style/body`, `font/style/display`, `ingredient/meta`, `radius/md`, `space/16`, `space/24`, `space/8`
- **Text styles:** `Desktop/caption`, `Desktop/h3`, `Desktop/body-s`
<!-- ⚙️ GENERATED:end:ingredient-item -->

- **Propósito:** Tarjeta de un ingrediente. Main: porcentaje del contenido (caption), nombre del componente (display) y composición (body S). Secondary: tarjeta solo con texto corrido, para el resto de ingredientes. Los alérgenos van en negrita dentro de la composición.
- **Ejemplo de código:**
  ```html
  <li data-ds="ingredient-item" class="ingredient-item"><span class="ingredient-item__percent">79% of content</span><span class="ingredient-item__name">Oriental noodles</span><span class="ingredient-item__text"><strong>Wheat</strong> flour, modified starch, salt, sodium and potassium carbonate</span></li>
  <li data-ds="ingredient-item" class="ingredient-item ingredient-item--secondary">Others: salt, spices, <strong>soy</strong> sauce (<strong>soy</strong>, <strong>wheat</strong>), garlic and onion.</li>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Es un `li` dentro de la lista de Ingredients. Las tres líneas son texto y se leen en orden: porcentaje, nombre, composición. Texto tinta sobre blanco 18,7:1; la línea de porcentaje y la composición en gris cálido sobre blanco 5,9:1. El alérgeno se marca con `<strong>`, que se lee como énfasis y se ve en negrita (no solo con color).
- **Cuándo usar / qué NO hace:** Solo dentro de Ingredients. Los datos se copian del envase; no se resumen ni se reordenan.
