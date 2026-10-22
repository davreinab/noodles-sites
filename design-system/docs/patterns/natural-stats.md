### Natural stats   ⚙️ synced: 2026-10-22T15:21:21Z

<!-- ⚙️ GENERATED:start:natural-stats -->
- **Figma:** `279:776` · página «Pattern / Detail pages» · COMPONENT_SET · 2 variantes · última sync 2026-10-22T15:21:21Z
- **Descripción (Figma):** Natural stats: bloque de cifras de la página Natural formula (wireframe UX 274:6354 desktop y 319:2744 móvil; clase CSS .natural-stats). Fondo tinta (surface/inverse) con título y subtítulo en text/on-inverse (amarillo suave, contraste alto). Cuatro Stat figure en fila en desktop y en rejilla 2×2 en móvil. Props: Title, Subtitle. Cifras, etiquetas y textos de ejemplo ⬜ TODO envase (business-rules).
- **Anatomía:** `stat-figure` → Stat figure, `stat-figure` → Stat figure, `stat-figure` → Stat figure, `stat-figure` → Stat figure
- **API:** `title` (string, por defecto Eating fast doesn't mean to eat unhealthy) · `subtitle` (string, por defecto The new formula improves the nutritional profile across the board, without adding a single minute to prep time.) · `breakpoint`: Desktop, Mobile (por defecto Desktop)
- **Nombres en Figma:** `title` ← `Title#279:18`, `subtitle` ← `Subtitle#279:21`, `breakpoint` ← `Breakpoint`
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `color/surface/brand`, `color/surface/inverse`, `color/text/default`, `color/text/on-inverse`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/body-s`, `font/line-height/desktop/h2`, `font/size/desktop/body-l`, `font/size/desktop/body-s`, `font/size/desktop/h2`, `font/style/body`, `font/style/display`, `space/16`, `space/2`, `space/32`, `space/48`, `space/64`, `space/8`, `space/96`
- **Text styles:** `Desktop/h2`, `Desktop/body-l`, `Desktop/body-s`
<!-- ⚙️ GENERATED:end:natural-stats -->

- **Propósito:** Bloque de cuatro cifras sobre fondo tinta («Eating fast doesn't mean to eat unhealthy»): título en h2, entradilla y cuatro Stat figure en fila.
- **Ejemplo de código:**
  ```html
  <section data-ds="natural-stats" class="section natural-stats" aria-labelledby="ns-title"><div class="section__inner"><div class="natural-stats__head"><h2 class="natural-stats__title" id="ns-title">Eating fast doesn't mean to eat unhealthy</h2><p class="natural-stats__subtitle">The new formula improves the nutritional profile across the board, without adding a single minute to prep time.</p></div><ul class="natural-stats__list" aria-label="Key figures"><li data-ds="stat-figure" class="stat-figure"><mark class="stat-figure__value">-45%</mark><span class="stat-figure__label">Less processed ingredients</span></li><li data-ds="stat-figure" class="stat-figure"><mark class="stat-figure__value">+5g</mark><span class="stat-figure__label">Improved protein for your muscles</span></li><li data-ds="stat-figure" class="stat-figure"><mark class="stat-figure__value">+20g</mark><span class="stat-figure__label">Natural fiber to help digestive system</span></li><li data-ds="stat-figure" class="stat-figure"><mark class="stat-figure__value">100%</mark><span class="stat-figure__label">Flavour, same as always</span></li></ul></div></section>
  ```
  Breakpoint Desktop: cuatro cifras en fila. Mobile: 2 × 2.
- **Accesibilidad (rol, nombre, estados y teclado):** `section` con nombre por el h2 y lista (`ul`) con nombre propio. Las cifras se leen con su etiqueta. Sin interacción. Contrastes: crema sobre tinta (17:1, token documentado); tinta sobre amarillo de marca en cada cifra (12,3:1).
- **Cuándo usar / qué NO hace:** En la Natural formula page, entre Natural improvement y Natural pillars. Las cuatro cifras, sus etiquetas y el título son ⬜ TODO envase: cada cifra debe salir de la tabla nutricional o de un dato verificado; no se redondea ni se compara con competidores sin estudio. Con más de cuatro cifras, no es este patrón.
