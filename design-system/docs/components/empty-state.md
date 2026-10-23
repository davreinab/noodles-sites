### Empty state   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:empty-state -->
- **Figma:** `219:1663` · página «Feedback & overlays» · COMPONENT · 1 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** Empty state de la Recipe library: sin resultados para la búsqueda o filtros. Título centrado (Desktop/h2) «We couldn't find any results for your search» y texto «Try with different ingredients». Debajo, en la pantalla (no dentro del componente), «Our most popular ones» con una rejilla de Recipe card. Uso: Recipe library en estado vacío (wireframe 485:6064 y móvil 486:14260). Clase CSS: .empty-state.
- **Anatomía:** sin instancias anidadas
- **API:** sin propiedades
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `color/text/default`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-m`, `font/line-height/desktop/h2`, `font/size/desktop/body-m`, `font/size/desktop/h2`, `font/style/body`, `font/style/display`, `space/48`, `space/8`
- **Text styles:** `Desktop/h2`, `Desktop/body-m`
<!-- ⚙️ GENERATED:end:empty-state -->

- **Propósito:** Mensaje de una búsqueda o un filtro que no devuelve recetas: título («We couldn't find any results for your search») y texto («Try with different ingredients»), centrados. Debajo, la página muestra el contenido alternativo, p. ej. «Our most popular ones» con una rejilla de Recipe card.
- **Ejemplo de código:**
  ```html
  <div data-ds="empty-state" class="empty-state">
  <h2 class="empty-state__title">We couldn't find any results for your search</h2>
  <p class="empty-state__text">Try with different ingredients</p>
  </div>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Rol: ninguno; es contenido de texto, sin `role`. El componente no anuncia nada: el cambio a «sin resultados» lo anuncia la página en la región de estado del patrón Library head. El título es un encabezado y su nivel lo fija la página (el ejemplo usa `h2`). No tiene elementos interactivos ni foco: el teclado pasa al contenido siguiente.
- **Móvil (fase 6):** el título pasa al tamaño móvil del h2 (`--font-size-mobile-h2` y su interlineado). El maestro de la FAQ lo dibuja con el tamaño de escritorio; en código se corrige con esta regla, no con el maestro.
- **Cuándo usar / qué NO hace:** Cuando una búsqueda o un filtro devuelve cero resultados en un listado. No lleva botones: «Clear filters» va en el patrón Library head. No es un error de página ni una alerta (eso es Alert).
