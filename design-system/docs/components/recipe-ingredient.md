### Recipe ingredient   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:recipe-ingredient -->
- **Figma:** `222:1906` · página «Content» · COMPONENT_SET · 2 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** Recipe ingredient: línea de ingrediente de la ficha de receta (Ingredients). Cantidad en caption («200 g») y nombre en negrita (Name); se usa con Variant=Default (tarjeta blanca con borde) o Variant=Brand (fondo tinta, texto claro y miniatura del envase a la derecha; enlaza a la ficha del producto). Uso: Recipe ingredients (wireframe 396:6398, ficha de receta 396:6292 / 396:6354). Clase CSS: .recipe-ingredient (modificador .recipe-ingredient--brand).
- **Anatomía:** sin instancias anidadas
- **API:** `quantity` (string, por defecto 200 g) · `name` (string, por defecto Cup Oriental) · `variant`: Default, Brand (por defecto Default)
- **Nombres en Figma:** `quantity` ← `Quantity#222:12`, `name` ← `Name#222:15`, `variant` ← `Variant`
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `color/border/default`, `color/surface/card`, `color/text/default`, `color/text/secondary`, `font/family/body`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/style/body`, `radius/md`, `space/16`, `space/4`
- **Text styles:** `Desktop/caption`
<!-- ⚙️ GENERATED:end:recipe-ingredient -->

- **Propósito:** Una línea de la lista de ingredientes de una receta: cantidad («200 g») en caption y nombre en negrita. Type Default: tarjeta blanca con texto. Type Brand: fondo tinta con texto claro, miniatura del envase a la derecha y enlace a la ficha del producto. La rejilla de dos columnas (escritorio) y una (móvil) la pone el patrón Recipe ingredients.
- **Ejemplo de código:**
  ```html
  <li data-ds="recipe-ingredient" class="recipe-ingredient">
  <div class="recipe-ingredient__info">
  <p class="recipe-ingredient__amount">200 g</p>
  <p class="recipe-ingredient__name">Spring onion</p>
  </div>
  </li>
  <li data-ds="recipe-ingredient" class="recipe-ingredient recipe-ingredient--brand">
  <div class="recipe-ingredient__info">
  <p class="recipe-ingredient__amount">1 unit</p>
  <p class="recipe-ingredient__name"><a class="recipe-ingredient__link" href="/productos/cup-oriental">Cup Oriental</a></p>
  </div>
  <img class="recipe-ingredient__thumb" src="../assets/images/placeholder.svg" alt="">
  </li>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Rol: `li` dentro de la lista `ul` del patrón; cantidad y nombre van en la misma fila, en ese orden. Sin enlace, el texto se lee como ingrediente. Con enlace (Brand), el enlace envuelve el nombre y su `::after` cubre toda la tarjeta: un solo destino, sin enlaces duplicados. El nombre accesible del enlace es el nombre del producto. La miniatura es decorativa (`alt=""`). Pares texto/fondo: tinta sobre blanco (Default) y crema sobre tinta (Brand); las cifras de contraste las mide ds-fidelity y no constan aquí. Teclado: Tab llega al enlace y Enter abre la ficha. Foco: en Default, contorno de 2 px en la tarjeta; en Brand, contorno en color claro sobre toda la tarjeta (`:has()`).
- **Cuándo usar / qué NO hace:** Para cada ingrediente de la lista de una receta. Brand solo cuando el ingrediente es un producto de la marca, porque enlaza a su ficha. No es un botón ni una card de receta, y no lleva pasos de preparación.
