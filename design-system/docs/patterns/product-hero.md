### Product hero   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:product-hero -->
- **Figma:** `93:154` · página «Pattern / Detail pages» · COMPONENT_SET · 2 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** Cabecera de la página de producto (punto 5 de la SPEC, wireframe UX 396:6073 en el archivo 1YhsCqdqYCHlK4Y82IY5G3). Fondo color/surface/inverse y textos on-inverse. Enlace de vuelta «All Cups» (Link Standalone Surface=Dark con icono arrow-left) · Badge New · nombre (display, mayúsculas) · descripción (body L) · fila de 2 Chip («100% natural ingredients», «Ready in 3'»). Media: frame «media» con rectángulo de imagen (color/surface/card) y frame «packshot» encima con el envase 3D. Breakpoint=Desktop: texto a la izquierda y media a la derecha. Breakpoint=Mobile: texto arriba y media debajo. Sin galería de miniaturas, lista de highlights ni acciones.
- **Anatomía:** `icon-leading` → Icon / arrow-left, `back-link` → Type=Standalone, Surface=Dark, State=Default, `icon-trailing` → Icon / arrow-left, `badge-new` → Type=New, `chip` → Size=M, State=Default, `icon-leading` → Icon / check, `chip` → Size=M, State=Default, `icon-leading` → Icon / check
- **API:** `breakpoint`: Desktop, Mobile (por defecto Desktop)
- **Nombres en Figma:** `breakpoint` ← `Breakpoint`
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown · capas sin swap: icon-leading
- **Tokens que consume:** `badge/new/bg`, `badge/new/text`, `border/width/thin`, `chip/bg`, `chip/border`, `chip/height/m`, `chip/text`, `color/neutral/ink-900`, `color/surface/card`, `color/surface/inverse`, `color/text/on-inverse`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/body-s`, `font/line-height/desktop/caption`, `font/line-height/desktop/h1`, `font/line-height/desktop/label`, `font/line-height/mobile/label`, `font/size/desktop/body-l`, `font/size/desktop/body-s`, `font/size/desktop/caption`, `font/size/desktop/h1`, `font/size/desktop/label`, `font/size/mobile/label`, `font/style/body`, `font/style/display`, `icon/color/inverse`, `icon/size/md`, `icon/size/sm`, `layout/frame`, `layout/margin`, `layout/section-y`, `link/inverse`, `radius/lg`, `radius/pill`, `space/16`, `space/24`, `space/4`, `space/64`, `space/8`
- **Text styles:** `Desktop/label`, `Mobile/label`, `Desktop/h1`, `Desktop/body-l`, `Desktop/body-s`, `Desktop/caption`
<!-- ⚙️ GENERATED:end:product-hero -->

- **Propósito:** Cabecera de la página de producto sobre fondo tinta: enlace de vuelta, badge NEW, nombre (display), descripción, chips de atributos («100% natural ingredients», «Ready in 3'») y packshot del envase sobre una foto a la derecha. Móvil: texto arriba y media debajo.
- **Ejemplo de código:**
  ```html
  <section data-ds="product-hero" class="section product-hero" aria-labelledby="ph-title">
  <div class="section__inner">
  <div class="product-hero__grid">
  <div class="product-hero__info">
  <a class="link link--dark link--standalone product-hero__back" href="#cups">All cups <span class="icon icon-arrow-left" aria-hidden="true"></span></a>
  <div class="product-hero__tags"><span class="badge">New</span></div>
  <h1 class="page-title product-hero__title" id="ph-title">Yakisoba chicken</h1>
  <p class="product-hero__description">Your usual chicken, with oriental yakisoba sauce.</p>
  <ul class="product-hero__chips"><li class="chip chip--m">100% natural ingredients</li><li class="chip chip--m">Ready in 3'</li></ul>
  </div>
  <div class="product-hero__media">
  <img class="product-hero__photo" src="assets/images/placeholder.svg" alt="">
  <img class="product-hero__pack" src="assets/images/placeholder.svg" alt="Yakisoba chicken cup">
  </div>
  </div>
  </div>
  </section>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** El nombre es el `h1`. El enlace de vuelta lleva texto y un icono decorativo. La foto de fondo es decorativa (`alt` vacío); el packshot lleva el `alt` del producto. Texto crema sobre tinta 17,2:1; el badge NEW es texto blanco sobre rojo 4,7:1. Los chips son texto, no botones: no reaccionan al ratón.
- **Cuándo usar / qué NO hace:** Solo en la página de producto. Imágenes de marca (3D y girosu), nunca generadas con IA.
