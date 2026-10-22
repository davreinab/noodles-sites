### Recipe steps   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:recipe-steps -->
- **Figma:** `224:487` · página «Pattern / Detail pages» · COMPONENT_SET · 2 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** Recipe steps: módulo de pasos de preparación de la ficha de receta, con fondo crema (surface/page). Breakpoint=Desktop: título «Step-by-step preparation» y subtítulo; lista de 6 Step (640 de ancho) con Title=true y Heading; el paso 2 con Media=True. Breakpoint=Mobile (375): padding space/48 vertical y space/16 lateral, pasos a ancho completo (343). Uso: ficha de receta (wireframe desktop 396:6398 y 396:6354). Clase CSS: .recipe-steps.
- **Anatomía:** `Step 1` → Media=False, `Step 2` → Media=True, `Step 3` → Media=False, `Step 4` → Media=False, `Step 5` → Media=False, `Step 6` → Media=False
- **API:** `breakpoint`: Desktop, Mobile (por defecto Desktop)
- **Nombres en Figma:** `breakpoint` ← `Breakpoint`
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `border/width/thin`, `color/surface/card`, `color/surface/page`, `color/text/default`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/desktop/display`, `font/line-height/desktop/h2`, `font/line-height/desktop/h3`, `font/size/desktop/body-l`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/desktop/display`, `font/size/desktop/h2`, `font/size/desktop/h3`, `font/style/body`, `font/style/display`, `radius/md`, `space/16`, `space/24`, `space/48`, `space/64`, `space/8`, `space/80`, `step/border`, `step/media-bg`, `step/number-text`, `step/text`
- **Text styles:** `Desktop/h2`, `Desktop/body-m`, `Desktop/display`, `Desktop/h3`, `Desktop/caption`
<!-- ⚙️ GENERATED:end:recipe-steps -->

- **Propósito:** Sección de pasos de una receta: título «Step-by-step preparation», subtítulo («Follow the steps below for a perfect result.») y la lista numerada de Step. Cada paso puede llevar título (h3) y texto, y una imagen cuando el paso la necesita (Step Media=True). Es el módulo de pasos de la página de receta.
- **Ejemplo de código:**
  ```html
  <section data-ds="recipe-steps" class="section recipe-steps" aria-labelledby="rsteps-title">
  <div class="section__header">
  <h2 class="section__title" id="rsteps-title">Step-by-step preparation</h2>
  <p class="section__lead">Follow the steps below for a perfect result.</p>
  </div>
  <ol class="steps">
  <li class="step">
  <span class="step__number" aria-hidden="true">1</span>
  <div class="step__content"><h3 class="step__title">Add boiling water up to the mark</h3><p class="step__text">Open the lid halfway and add boiling water up to the inner line.</p></div>
  </li>
  <li class="step">
  <span class="step__number" aria-hidden="true">2</span>
  <div class="step__content"><h3 class="step__title">Wait 3 minutes</h3><p class="step__text">Let the noodles rest while the sauce warms up.</p></div>
  </li>
  <li class="step">
  <span class="step__number" aria-hidden="true">3</span>
  <div class="step__content"><p class="step__text">Drain the water carefully and set the noodles aside.</p></div>
  </li>
  </ol>
  </section>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Rol: sección con nombre por su h2 (`aria-labelledby`). La lista es un `ol`, así que el lector anuncia cuántos pasos hay y los lee en orden; por eso el número de cada paso va con `aria-hidden`. Un paso con título lo lleva como h3; un paso sin título se lee solo con su texto. Las imágenes de paso llevan alt que describe la acción (ver Step). El patrón no tiene controles ni foco propio.
- **Cuándo usar / qué NO hace:** Pasos de preparación de una receta. No es Preparation (la preparación de la ficha de producto, con vídeo y temporizador de 3 minutos) ni Recipe ingredients (la lista de ingredientes va antes, en su propio módulo).
