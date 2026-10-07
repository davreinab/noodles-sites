### Product carousel   ⚙️ synced: 2026-10-07T18:44:44Z

<!-- ⚙️ GENERATED:start:product-carousel -->
- **Figma:** `91:837` · página «Pattern / Product carousel» · COMPONENT_SET · 2 variantes · última sync 2026-10-07T18:44:44Z
- **Descripción (Figma):** Productos de la Home: título (h2) · flechas Icon button (desktop) · Tabs de tipo (Cups / Bags / Sauces; tablist que filtra el carrusel, solo tipos con productos) · carrusel de Product card · Link «Ver todos los productos» a la Product library. Desktop: 4 cards visibles (310 px, gutter layout/gutter). Mobile: scroll horizontal con la siguiente card asomando (pista que comunica que hay más); sin flechas. Accesibilidad: el carrusel es una lista (&lt;ul&gt;) desplazable con teclado; las flechas son &lt;button&gt; con nombre y se desactivan al llegar al final. Sin variables propias.
- **Anatomía:** `prev` → Hierarchy=Secondary, Size=M, State=Default, `icon` → Icon / arrow-left, `next` → Hierarchy=Secondary, Size=M, State=Default, `icon` → Icon / arrow-right, `tab` → State=Selected, `tab` → State=Default, `product-card` → State=Default, `badge` → Type=New, `link` → Type=Standalone, Surface=Light, State=Default, `icon-trailing` → Icon / arrow-right, `badge` → Type=New
- **Breakpoint:** Desktop, Mobile
- **Propiedades de componente:** `Breakpoint` (VARIANT, por defecto Desktop)
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `badge/new/bg`, `badge/new/text`, `border/width/thick`, `border/width/thin`, `button/secondary/border`, `button/secondary/text`, `color/effect/shadow-ink`, `color/surface/page`, `color/text/default`, `font/family/body`, `font/family/display`, `font/line-height/desktop/caption`, `font/line-height/desktop/h2`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/line-height/mobile/label`, `font/size/desktop/caption`, `font/size/desktop/h2`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/size/mobile/label`, `font/style/body`, `font/style/display`, `icon/size/md`, `icon/size/sm`, `layout/frame`, `layout/gutter`, `layout/margin`, `layout/section-y`, `link/default`, `product-card/bg`, `product-card/border`, `product-card/media-bg`, `product-card/meta`, `product-card/title`, `radius/md`, `radius/pill`, `space/16`, `space/24`, `space/32`, `space/4`, `space/8`, `tab/bg`, `tab/bg-selected`, `tab/border`, `tab/text`, `tab/text-selected`
- **Text styles:** `Desktop/h2`, `Desktop/label`, `Mobile/label`, `Desktop/caption`, `Desktop/h3`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `badge/new/bg`, `badge/new/text`, `button/secondary/border`, `button/secondary/text`, `color/effect/shadow-ink`, `color/surface/page`, `color/text/default`, `font/family/body`, `font/family/display`, `font/line-height/desktop/caption`, `font/line-height/desktop/h2`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/line-height/mobile/label`, `font/size/desktop/caption`, `font/size/desktop/h2`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/size/mobile/label`, `font/style/body`, `font/style/display`, `link/default`, `product-card/bg`, `product-card/border`, `product-card/media-bg`, `product-card/meta`, `product-card/title`, `tab/bg`, `tab/bg-selected`, `tab/border`, `tab/text`, `tab/text-selected`
<!-- ⚙️ GENERATED:end:product-carousel -->

- **Propósito:** Productos de la Home: pestañas por tipo y carrusel de Product card con enlace a la librería.
- **Ejemplo de código:**
  ```html
  <section class="section product-carousel" aria-labelledby="pc-title">
  <div class="section__inner">
  <div class="section__bar"><h2 class="section__title" id="pc-title">Nuestros noodles</h2><button class="icon-button icon-button--secondary" type="button" aria-label="Anteriores"><span class="icon icon-arrow-left" aria-hidden="true"></span></button></div>
  <div class="product-carousel__tabs" role="tablist" aria-label="Tipo"><button class="tab" role="tab" aria-selected="true">Cups</button><button class="tab" role="tab" aria-selected="false" tabindex="-1">Bags</button></div>
  <ul class="carousel" role="tabpanel" aria-label="Cups">
  <li><a class="product-card" href="/productos/yatekomo-pollo"><div class="product-card__body"><h3 class="product-card__name">Yatekomo Pollo</h3></div></a></li>
  </ul>
  <a class="link link--standalone" href="/productos">Ver todos los productos <span class="icon icon-arrow-right" aria-hidden="true"></span></a>
  </div>
  </section>
  ```
- **Accesibilidad (pares AA verificados):** Título tinta sobre crema 17,2:1; el resto, los pares de Tab, Product card y Link. El carrusel es una lista desplazable con teclado (scroll-snap); las flechas son botones con nombre que se desactivan al llegar al final. Las pestañas siguen el patrón tabs.
- **Cuándo usar / qué NO hace:** En la Home. Solo se muestran tipos con productos. No sustituye a la Product library ni lleva más de doce productos.
