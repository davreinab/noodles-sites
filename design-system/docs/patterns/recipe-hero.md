### Recipe hero   ⚙️ synced: 2026-10-22T14:30:04Z

<!-- ⚙️ GENERATED:start:recipe-hero -->
- **Figma:** `96:113` · página «Pattern / Detail pages» · COMPONENT_SET · 2 variantes · última sync 2026-10-22T14:30:04Z
- **Descripción (Figma):** Cabecera de la página de receta: kicker «Receta» · título (h1) · tiempo (timer) y dificultad · descripción · productos usados como Chip M (enlazan a la ficha de producto; lista <ul>) · imagen principal de marca (sin vídeo al principio, regla de negocio). Fondo color/surface/brand. Después van Product details (ingredientes y nutrición de la receta) y Preparation sin Timer con Step Media=True. Desktop: texto a la izquierda; Mobile: texto arriba e imagen debajo. Sin variables propias.
- **Anatomía:** `arrow` → Icon / arrow-left, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Chip` → Size=M, State=Default, `icon-leading` → Icon / check, `Chip` → Size=M, State=Default, `icon-leading` → Icon / check, `icon-send` → Icon / send
- **API:** `breakpoint`: Desktop, Mobile (por defecto Desktop)
- **Nombres en Figma:** `breakpoint` ← `Breakpoint`
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown · capas sin swap: arrow, icon-send
- **Tokens que consume:** `border/width/thin`, `chip/bg`, `chip/border`, `chip/height/m`, `chip/height/s`, `chip/text`, `color/border/default`, `color/surface/brand`, `color/surface/page`, `color/text/default`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/body-m`, `font/line-height/desktop/body-s`, `font/line-height/desktop/caption`, `font/line-height/desktop/h1`, `font/size/desktop/body-l`, `font/size/desktop/body-m`, `font/size/desktop/body-s`, `font/size/desktop/caption`, `font/size/desktop/h1`, `font/style/body`, `font/style/display`, `icon/color/default`, `icon/size/md`, `icon/size/sm`, `layout/frame`, `layout/margin`, `layout/section-y`, `radius/md`, `radius/pill`, `space/16`, `space/24`, `space/64`, `space/8`
- **Text styles:** `Desktop/body-s`, `Desktop/h1`, `Desktop/body-l`, `Desktop/body-m`, `Desktop/caption`
<!-- ⚙️ GENERATED:end:recipe-hero -->

- **Propósito:** Cabecera de la página de receta sobre amarillo de marca: enlace «All recipes» para volver a la Recipe library, chips de los productos usados (enlazan a su ficha), título (h1), descripción, chips de tiempo y ración («15 min preparation», «4 people»), enlace «Share recipe» que abre el modal Share (Share panel) y la imagen principal de la receta.
- **Ejemplo de código:**
  ```html
  <section data-ds="recipe-hero" class="section recipe-hero" aria-labelledby="rh-title">
  <div class="section__inner">
  <div class="recipe-hero__grid">
  <div class="recipe-hero__info">
  <a class="recipe-hero__back" href="/recipes"><span class="icon icon-arrow-left" aria-hidden="true"></span>All recipes</a>
  <ul class="recipe-hero__products" aria-label="Products used in this recipe"><li><a class="chip chip--m" href="/productos/cup-oriental">Cup Oriental</a></li><li><a class="chip chip--m" href="/productos/sauce-sesame">Sauce Sesame</a></li></ul>
  <h1 class="page-title" id="rh-title">Oriental chicken noodles</h1>
  <p class="recipe-hero__description">Quick, savory noodles with a smoky soy glaze.</p>
  <ul class="recipe-hero__meta"><li><span class="chip chip--m"><span class="icon icon-timer" aria-hidden="true"></span>15 min preparation</span></li><li><span class="chip chip--m">4 people</span></li></ul>
  <button class="link" type="button" aria-haspopup="dialog"><span class="icon icon-send" aria-hidden="true"></span>Share recipe</button>
  </div>
  <div class="media-frame recipe-hero__media"><img src="../assets/images/placeholder.svg" alt="Oriental chicken noodles served in a bowl"></div>
  </div>
  </div>
  </section>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Todo el texto en tinta sobre amarillo de marca (12,3:1). El título es el `h1`. «All recipes» es un enlace con nombre visible; su flecha es decorativa. Los chips de producto son enlaces con su nombre, dentro de una `ul` con `aria-label` que dice que son productos usados. Los chips de tiempo y ración son texto (un `span` no interactivo) y su icono de timer es decorativo. «Share recipe» es un `button` con `aria-haspopup="dialog"`, no un enlace de navegación: abre el modal Share, y al cerrarlo el foco vuelve al botón. La imagen lleva alt descriptivo de la foto.
- **Cuándo usar / qué NO hace:** Solo en la página de receta. Sin vídeo al principio (regla de negocio). No muestra dificultad ni un bloque de productos aparte: los productos van como chips arriba. El modal lo gestiona Share panel; el hero solo tiene el botón que lo abre.
