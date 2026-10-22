### Decoration / Noodle texture   ⚙️ synced: 2026-10-22T09:37:04Z

<!-- ⚙️ GENERATED:start:decoration-noodle-texture -->
- **Figma:** `157:50` · página «Brand assets» · COMPONENT · 1 variantes · última sync 2026-10-22T09:37:04Z
- **Descripción (Figma):** Trama de fideos de fondo (como en las landings): los 5 fideos de Decoration / Noodle en tono Texture (decoration/noodle/texture: ámbar opaco, el naranja al 50 % sobre amarillo), en fila. Va a sangre por la derecha del módulo, detrás del contenido y más alta que él (se corta arriba y abajo). Solo sobre color/surface/brand; el texto encima es tinta (contraste con el ámbar ≥ 9:1). Decorativa: aria-hidden, sin interacción.
- **Anatomía:** `noodle` → Shape=1, Tone=Texture, `noodle` → Shape=3, Tone=Texture, `noodle` → Shape=5, Tone=Texture, `noodle` → Shape=2, Tone=Texture, `noodle` → Shape=4, Tone=Texture
- **API:** sin propiedades
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `decoration/noodle/texture`
<!-- ⚙️ GENERATED:end:decoration-noodle-texture -->
- **Propósito:** Trama de fideos de fondo, como en los módulos amarillos de las landings: los cinco fideos de marca en tono Texture (ámbar), en fila, a sangre por la derecha del módulo y detrás del contenido.
- **Ejemplo de código:**
  ```html
  <section data-ds="decoration-noodle-texture" class="section promo" aria-labelledby="pr-title">
  <div class="decoration-noodle-texture" aria-hidden="true"><span class="decoration-noodle decoration-noodle--texture"></span><span class="decoration-noodle decoration-noodle--3 decoration-noodle--texture"></span><span class="decoration-noodle decoration-noodle--5 decoration-noodle--texture"></span><span class="decoration-noodle decoration-noodle--2 decoration-noodle--texture"></span><span class="decoration-noodle decoration-noodle--4 decoration-noodle--texture"></span></div>
  <div class="section__inner"><h2 class="section__title" id="pr-title">Título</h2></div>
  </section>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Decorativa: `aria-hidden="true"`, sin foco ni interacción. El ámbar es opaco (`--decoration-noodle-texture`, naranja al 50 % sobre amarillo resuelto como color, regla 7): la tinta encima mantiene 9,5:1, así que el texto puede pasar por delante.
- **Cuándo usar / qué NO hace:** Solo en secciones con fondo `color/surface/brand` (amarillo): en la Home, Promo y Where to buy. La sección recorta la trama (overflow) y pone su contenido encima. No va sobre crema, blanco, verde ni tinta, ni se usa como separador.
