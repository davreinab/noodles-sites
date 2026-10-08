### Hero   ⚙️ synced: 2026-10-08T10:21:35Z

<!-- ⚙️ GENERATED:start:hero -->
- **Figma:** `88:132` · página «Pattern / Home» · COMPONENT_SET · 2 variantes · última sync 2026-10-08T10:21:35Z
- **Descripción (Figma):** Patrón hero de la Home. Slider de máximo 3 slides (regla de negocio): cada slide = imagen de producto o campaña (de marca, sin IA) · sello Badge Natural «The only 100% natural» · claim «Welcome to the new noodles era» (display) · texto · CTA a la acción principal (campaña activa o, sin campaña, producto). Controles: puntos (el activo relleno; el estado no depende solo del color: forma rellena vs contorno) y flechas Icon button. Accesibilidad: carrusel con aria-roledescription=&amp;quot;carrusel&amp;quot;, cada slide «1 de 3», sin autoplay (o con pausa visible y parado con prefers-reduced-motion); flechas con nombre «Slide anterior/siguiente». Fondo color/surface/page (crema), como el hero de las landings. Fideo de marca (Decoration / Noodle, Shape=1, Tone=Brand) a sangre por el lateral izquierdo (centrado en Mobile), detrás del contenido; en código se dibuja de arriba abajo al cargar (draw-in) y queda quieto, sin animación con prefers-reduced-motion. Imagen de producto sin marco (sin fondo, borde ni radio), packshot recortado sobre el fondo. Desktop: texto a la izquierda e imagen a la derecha; Mobile: imagen arriba. Sin variables propias.
- **Anatomía:** `noodle` → Shape=1, Tone=Brand, `seal` → Type=Natural, `cta` → Hierarchy=Primary, Size=L, State=Default, `icon-leading` → Icon / arrow-right, `icon-trailing` → Icon / arrow-right, `prev` → Hierarchy=Secondary, Size=M, State=Default, `icon` → Icon / arrow-left, `next` → Hierarchy=Secondary, Size=M, State=Default, `icon` → Icon / arrow-right
- **Breakpoint:** Desktop, Mobile
- **Propiedades de componente:** `Breakpoint` (VARIANT, por defecto Desktop)
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `badge/natural/bg`, `badge/natural/text`, `border/width/thick`, `border/width/thin`, `button/primary/bg`, `button/primary/border`, `button/primary/text`, `button/secondary/border`, `button/secondary/text`, `color/border/default`, `color/surface/page`, `color/text/default`, `decoration/noodle/brand`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/display`, `font/line-height/desktop/label`, `font/line-height/mobile/label`, `font/size/desktop/body-l`, `font/size/desktop/display`, `font/size/desktop/label`, `font/size/mobile/label`, `font/style/body`, `font/style/display`, `icon-button/size/m`, `icon/size/md`, `icon/size/sm`, `layout/frame`, `layout/margin`, `layout/section-y`, `radius/none`, `radius/pill`, `space/16`, `space/24`, `space/32`, `space/4`, `space/48`, `space/64`, `space/8`
- **Text styles:** `Mobile/label`, `Desktop/display`, `Desktop/body-l`, `Desktop/label`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `badge/natural/bg`, `badge/natural/text`, `button/primary/bg`, `button/primary/border`, `button/primary/text`, `button/secondary/border`, `button/secondary/text`, `color/border/default`, `color/surface/page`, `color/text/default`, `decoration/noodle/brand`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/display`, `font/line-height/desktop/label`, `font/line-height/mobile/label`, `font/size/desktop/body-l`, `font/size/desktop/display`, `font/size/desktop/label`, `font/size/mobile/label`, `font/style/body`, `font/style/display`
<!-- ⚙️ GENERATED:end:hero -->

- **Propósito:** Hero de la Home: slider de máximo tres slides con el claim, el sello natural y la acción principal (la campaña activa o, sin campaña, el producto).
- **Ejemplo de código:**
  ```html
  <section class="section hero" aria-roledescription="carrusel" aria-label="Destacados">
  <span class="decoration-noodle hero__noodle" aria-hidden="true"></span>
  <div class="section__inner">
  <div class="hero__slide" role="group" aria-roledescription="slide" aria-label="1 de 3">
  <div class="hero__content">
  <span class="badge badge--natural">The only 100% natural</span>
  <h1 class="hero__title">Welcome to the new noodles era</h1>
  <p class="hero__lead">Texto de apoyo.</p>
  <a class="button button--l" href="/productos">Descubre los productos</a>
  </div>
  <picture class="hero__media"><source media="(max-width: 768px)" srcset="/media/hero-1-mobile.png"><img src="/media/hero-1.png" alt="Cups de Yatekomo"></picture>
  </div>
  <div class="hero__controls">
  <div class="hero__dots"><button class="hero__dot" type="button" aria-current="true" aria-label="Slide 1"></button><button class="hero__dot" type="button" aria-label="Slide 2"></button></div>
  <div class="hero__arrows"><button class="icon-button icon-button--secondary" type="button" aria-label="Slide anterior"><span class="icon icon-arrow-left" aria-hidden="true"></span></button><button class="icon-button icon-button--secondary" type="button" aria-label="Slide siguiente"><span class="icon icon-arrow-right" aria-hidden="true"></span></button></div>
  </div>
  </div>
  </section>
  ```
- **Accesibilidad (pares AA verificados):** Claim y texto en tinta sobre crema y sobre el fideo amarillo (12,3:1), así que el fideo puede pasar por detrás del texto; sello blanco sobre verde 5,5:1; puntos con borde de tinta (el activo relleno: forma, no solo color). Carrusel con `aria-roledescription`, cada slide «n de 3», sin autoplay (o con pausa visible, y parado con reduce-motion). Flechas y puntos son botones con nombre. El único `h1` de la Home es el claim. El fideo es decorativo (`aria-hidden`), se dibuja una sola vez al cargar y no se anima con `prefers-reduced-motion`.
- **Cuándo usar / qué NO hace:** Solo en la Home, arriba. Máximo tres slides (regla de negocio); la imagen es de marca, sin IA, y va sin marco: packshot recortado (PNG transparente) sobre el crema. No se usa como banner intermedio (Banner).
