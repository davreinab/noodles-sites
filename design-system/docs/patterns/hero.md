### Hero   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:hero -->
- **Figma:** `88:132` · página «Pattern / Home» · COMPONENT_SET · 2 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** Patrón hero de la Home (wireframe UX). Claim fijo «Welcome to the new era» (h1, display) fuera del slider · slider de máximo 3 slides (regla de negocio; el wireframe dibuja 5 puntos: pendiente de confirmar): cada slide = Badge New · título (h2, estilo h3) · subtítulo · Button Primary L a la acción de la slide · controles anterior / puntos / siguiente bajo el botón. Imagen de producto o campaña de marca, sin IA, sin marco (packshot recortado sobre el fondo). Fondo color/surface/page (crema), como el hero de las landings; fideo de marca (Decoration / Noodle, Shape=1, Tone=Brand) a sangre por la izquierda (centrado en Mobile), detrás del contenido, que en código se dibuja de arriba abajo al cargar y queda quieto (sin animación con prefers-reduced-motion). Accesibilidad: carrusel con aria-roledescription=«carrusel», cada slide «1 de 3», pasa solo, con botón de pausa visible (Icon button «Pausar» / «Reanudar») y parado con prefers-reduced-motion; flechas con nombre «Slide anterior/siguiente»; el punto activo va relleno (forma, no solo color). Desktop: texto a la izquierda e imagen a la derecha; Mobile: texto arriba e imagen debajo. Sin variables propias.
- **Anatomía:** `noodle` → Shape=1, Tone=Brand, `badge` → Type=New, `cta` → Hierarchy=Primary, Size=L, State=Default, `icon-leading` → Icon / arrow-right, `icon-trailing` → Icon / arrow-right, `prev` → Hierarchy=Secondary, Size=M, State=Default, `icon` → Icon / arrow-left, `next` → Hierarchy=Secondary, Size=M, State=Default, `icon` → Icon / arrow-right, `pause` → Hierarchy=Secondary, Size=M, State=Default, `icon` → Icon / pause
- **API:** `breakpoint`: Desktop, Mobile (por defecto Desktop)
- **Nombres en Figma:** `breakpoint` ← `Breakpoint`
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `badge/new/bg`, `badge/new/text`, `border/width/thick`, `border/width/thin`, `button/primary/bg`, `button/primary/border`, `button/primary/text`, `button/secondary/border`, `button/secondary/text`, `color/border/default`, `color/surface/page`, `color/text/default`, `decoration/noodle/brand`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/display`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/line-height/mobile/label`, `font/size/desktop/body-l`, `font/size/desktop/display`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/size/mobile/label`, `font/style/body`, `font/style/display`, `icon-button/size/m`, `icon/size/md`, `icon/size/sm`, `layout/frame`, `layout/margin`, `layout/section-y`, `radius/none`, `radius/pill`, `space/16`, `space/24`, `space/32`, `space/4`, `space/48`, `space/64`, `space/8`
- **Text styles:** `Desktop/display`, `Mobile/label`, `Desktop/h3`, `Desktop/body-l`, `Desktop/label`
<!-- ⚙️ GENERATED:end:hero -->

- **Propósito:** Hero de la Home (wireframe UX): claim fijo «Welcome to the new era» y slider de máximo tres slides (NEW · título · subtítulo · CTA · controles), con el estilo de las landings (crema, fideo con draw-in, packshot sin marco).
- **Ejemplo de código:**
  ```html
  <section data-ds="hero" class="section hero" aria-roledescription="carrusel" aria-label="Destacados">
  <span class="decoration-noodle hero__noodle" aria-hidden="true"></span>
  <div class="section__inner">
  <div class="hero__slide">
  <div class="hero__content">
  <h1 class="hero__title">Welcome to the new era</h1>
  <div class="hero__slide-content" role="group" aria-roledescription="slide" aria-label="1 de 3">
  <div class="hero__slide-copy"><span class="badge">New</span><h2 class="hero__slide-title">Do you like to cook? Check out our new bags</h2><p class="hero__lead">Same amount, super convenient for your recipes</p></div>
  <a class="button button--l" href="/productos/bags">Discover flavours</a>
  <div class="hero__controls"><button class="icon-button icon-button--secondary" type="button" aria-label="Slide anterior"><span class="icon icon-arrow-left" aria-hidden="true"></span></button><div class="hero__dots"><button class="hero__dot" type="button" aria-current="true" aria-label="Slide 1"></button><button class="hero__dot" type="button" aria-label="Slide 2"></button></div><button class="icon-button icon-button--secondary" type="button" aria-label="Slide siguiente"><span class="icon icon-arrow-right" aria-hidden="true"></span></button></div>
  </div>
  </div>
  <picture class="hero__media"><source media="(max-width: 768px)" srcset="/media/hero-1-mobile.png"><img src="/media/hero-1.png" alt="Cups de Yatekomo"></picture>
  </div>
  </div>
  </section>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Claim y texto en tinta sobre crema y sobre el fideo amarillo (12,3:1), así que el fideo puede pasar por detrás del texto. El fideo es decorativo (`aria-hidden`), se dibuja una vez y no se anima con reduce-motion. Carrusel con `aria-roledescription`, slide «n de 3», sin autoplay; flechas y puntos son botones con nombre; el punto activo va relleno. El único `h1` de la Home es el claim.
- **Cuándo usar / qué NO hace:** Solo en la Home, arriba. Máximo tres slides (regla de negocio; el wireframe dibuja cinco puntos: pendiente de confirmar). La imagen es de marca, sin IA, y va sin marco. No se usa como banner intermedio (Banner).
