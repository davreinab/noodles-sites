### Product hero   ⚙️ synced: 2026-10-07T18:41:16Z

<!-- ⚙️ GENERATED:start:product-hero -->
- **Figma:** `93:154` · página «Pattern / Product hero» · COMPONENT_SET · 2 variantes · última sync 2026-10-07T18:41:16Z
- **Descripción (Figma):** Cabecera de la página de producto: galería (imagen 3D principal —la «girosu» en Cups— e interior; miniaturas como botones, la seleccionada con borde grueso y aria-current) · Badge New/Natural · tipo y línea · nombre (h1) · descripción · highlights con check en color/text/natural (lista &lt;ul&gt;) · Button «Dónde comprar» (lleva a Where to buy) y Link «Ver ingredientes» (ancla a Product details). Las imágenes son las de marca, nunca generadas con IA. Desktop: galería a la izquierda; Mobile: galería arriba. Sin variables propias.
- **Anatomía:** `badge-new` → Type=New, `badge-natural` → Type=Natural, `icon-check` → Icon / check, `cta` → Hierarchy=Primary, Size=L, State=Default, `icon-leading` → Icon / arrow-right, `icon-trailing` → Icon / arrow-right, `link` → Type=Standalone, Surface=Light, State=Default, `icon-trailing` → Icon / arrow-right
- **Breakpoint:** Desktop, Mobile
- **Propiedades de componente:** `Breakpoint` (VARIANT, por defecto Desktop)
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown · capas sin swap: icon-check
- **Tokens que consume:** `badge/natural/bg`, `badge/natural/text`, `badge/new/bg`, `badge/new/text`, `border/width/thick`, `border/width/thin`, `button/primary/bg`, `button/primary/border`, `button/primary/text`, `color/border/default`, `color/surface/card`, `color/surface/page`, `color/text/default`, `color/text/natural`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/caption`, `font/line-height/desktop/h1`, `font/line-height/desktop/label`, `font/line-height/mobile/label`, `font/size/desktop/body-l`, `font/size/desktop/caption`, `font/size/desktop/h1`, `font/size/desktop/label`, `font/size/mobile/label`, `font/style/body`, `font/style/display`, `icon/size/md`, `icon/size/sm`, `layout/frame`, `layout/margin`, `layout/section-y`, `link/default`, `radius/md`, `radius/pill`, `radius/sm`, `space/16`, `space/24`, `space/32`, `space/4`, `space/64`, `space/8`
- **Text styles:** `Desktop/caption`, `Mobile/label`, `Desktop/h1`, `Desktop/body-l`, `Desktop/label`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `badge/natural/bg`, `badge/natural/text`, `badge/new/bg`, `badge/new/text`, `button/primary/bg`, `button/primary/border`, `button/primary/text`, `color/border/default`, `color/surface/card`, `color/surface/page`, `color/text/default`, `color/text/natural`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/caption`, `font/line-height/desktop/h1`, `font/line-height/desktop/label`, `font/line-height/mobile/label`, `font/size/desktop/body-l`, `font/size/desktop/caption`, `font/size/desktop/h1`, `font/size/desktop/label`, `font/size/mobile/label`, `font/style/body`, `font/style/display`, `link/default`
<!-- ⚙️ GENERATED:end:product-hero -->

- **Propósito:** Cabecera de la página de producto: galería (3D e interior), etiquetas, tipo y línea, nombre, highlights y «Dónde comprar».
- **Ejemplo de código:**
  ```html
  <section class="section product-hero" aria-labelledby="ph-title">
  <div class="section__inner">
  <div class="product-hero__grid">
  <div class="product-hero__gallery">
  <div class="media-frame product-hero__main"><img src="/media/yatekomo-pollo-3d.png" alt="Vaso de Yatekomo Pollo"></div>
  <ul class="product-hero__thumbs"><li><button class="product-hero__thumb" type="button" aria-current="true" aria-label="Imagen 3D"></button></li><li><button class="product-hero__thumb" type="button" aria-label="Interior"></button></li></ul>
  </div>
  <div class="product-hero__info">
  <div class="product-hero__tags"><span class="badge">Nuevo</span><span class="badge badge--natural">100 % natural</span></div>
  <span class="product-hero__line">Cups · Original</span>
  <h1 class="page-title" id="ph-title">Yatekomo Pollo</h1>
  <p class="product-hero__description">Descripción del sabor.</p>
  <ul class="product-hero__highlights"><li><span class="icon icon-check" aria-hidden="true"></span>Listo en 3 minutos</li></ul>
  <div class="product-hero__actions"><a class="button button--l" href="#donde-comprar">Dónde comprar</a><a class="link link--standalone" href="#ingredientes">Ver ingredientes <span class="icon icon-arrow-right" aria-hidden="true"></span></a></div>
  </div>
  </div>
  </div>
  </section>
  ```
- **Accesibilidad (pares AA verificados):** Nombre y texto tinta sobre crema 17,2:1; tipo y línea gris cálido sobre crema 5,4:1; checks verdes sobre crema 5,0:1. El nombre es el `h1`. Las miniaturas son botones con nombre y `aria-current` en la activa (borde grueso: no solo color). La imagen principal describe el producto en su `alt`.
- **Cuándo usar / qué NO hace:** Solo en la página de producto. Imágenes de marca (3D y girosu), nunca generadas con IA.
