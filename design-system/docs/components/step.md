### Step   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:step -->
- **Figma:** `71:164` · página «Content» · COMPONENT_SET · 2 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** Paso numerado de preparación (punto 7 de la SPEC, wireframe UX 396:6073 en el archivo 1YhsCqdqYCHlK4Y82IY5G3). Tarjeta sobre fondo color/surface/inverse: fondo color/surface/card (superficie opaca), radio md, padding 24. Número grande en display, sin círculo (step/number-text); texto en negrita (step/text). Media=True: añade la media (imagen o vídeo) bajo el texto. Anatomía: número · contenido (texto + media opcional).
- **Anatomía:** sin instancias anidadas
- **API:** `number` (string, por defecto 1) · `text` (string, por defecto Abre la tapa hasta la mitad y añade agua hirviendo hasta la línea interior.) · `title` (boolean, por defecto false) · `heading` (string, por defecto Add boiling water up to the mark) · `media` (boolean, por defecto false)
- **Nombres en Figma:** `number` ← `Number#71:9`, `text` ← `Text#71:12`, `title` ← `Title#222:6`, `heading` ← `Heading#222:9`, `media` ← `Media`
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `border/width/thin`, `color/surface/card`, `color/text/default`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/display`, `font/line-height/desktop/h3`, `font/size/desktop/body-l`, `font/size/desktop/display`, `font/size/desktop/h3`, `font/style/display`, `radius/md`, `space/16`, `space/24`, `space/8`, `step/number-text`, `step/text`
- **Text styles:** `Desktop/display`, `Desktop/h3`
<!-- ⚙️ GENERATED:end:step -->

- **Propósito:** Paso numerado de la preparación de producto o de una receta: tarjeta blanca con el número en display grande (sin círculo), título opcional (h3 display) y el texto en negrita. Imagen o GIF opcional (16:9).
- **Ejemplo de código:**
  ```html
  <ol data-ds="step" class="steps">
  <li class="step">
  <span class="step__number" aria-hidden="true">1</span>
  <div class="step__content"><h3 class="step__title">Add boiling water up to the mark</h3><p class="step__text">Open the lid halfway and pour the water in up to the inner line.</p></div>
  </li>
  <li class="step step--media">
  <span class="step__number" aria-hidden="true">2</span>
  <div class="step__content">
  <p class="step__text">Leave to stand for 3 minutes.</p>
  <div class="step__media"><img src="../assets/images/placeholder.svg" alt="Cup filled up to the inner line with boiling water"></div>
  </div>
  </li>
  </ol>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Rol: `li` dentro de `ol`, que ya anuncia la posición; por eso el número visual es `aria-hidden`. Texto tinta sobre blanco 18,7:1; el número en tinta sobre blanco. El título es un `h3` (el nivel lo fija la página; el ejemplo usa `h3`) y sin título no hay encabezado. La imagen describe el gesto en su `alt`; un GIF va como vídeo silencioso en bucle con botón de pausa y se detiene con prefers-reduced-motion.
- **Cuándo usar / qué NO hace:** En Preparation (producto) y en la receta. El texto sale del envase o de la receta; el Timer va aparte, no dentro de la tarjeta.
