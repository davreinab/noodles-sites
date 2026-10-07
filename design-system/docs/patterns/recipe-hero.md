### Recipe hero   ⚙️ synced: 2026-10-07T18:43:11Z

<!-- ⚙️ GENERATED:start:recipe-hero -->
- **Figma:** `96:113` · página «Pattern / Recipe hero» · COMPONENT_SET · 2 variantes · última sync 2026-10-07T18:43:11Z
- **Descripción (Figma):** Cabecera de la página de receta: kicker «Receta» · título (h1) · tiempo (timer) y dificultad · descripción · productos usados como Chip M (enlazan a la ficha de producto; lista &lt;ul&gt;) · imagen principal de marca (sin vídeo al principio, regla de negocio). Fondo color/surface/brand. Después van Product details (ingredientes y nutrición de la receta) y Preparation sin Timer con Step Media=True. Desktop: texto a la izquierda; Mobile: imagen arriba. Sin variables propias.
- **Anatomía:** `icon` → Icon / timer, `icon` → Icon / circle-check, `product-chip` → Size=M, State=Default, `icon-leading` → Icon / check
- **Breakpoint:** Desktop, Mobile
- **Propiedades de componente:** `Breakpoint` (VARIANT, por defecto Desktop)
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown · capas sin swap: icon, icon
- **Tokens que consume:** `border/width/thin`, `chip/bg`, `chip/border`, `chip/height/m`, `chip/text`, `color/border/default`, `color/surface/brand`, `color/surface/page`, `color/text/default`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/body-s`, `font/line-height/desktop/caption`, `font/line-height/desktop/h1`, `font/line-height/desktop/label`, `font/size/desktop/body-l`, `font/size/desktop/body-s`, `font/size/desktop/caption`, `font/size/desktop/h1`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/md`, `icon/size/sm`, `layout/frame`, `layout/margin`, `layout/section-y`, `radius/md`, `radius/pill`, `space/16`, `space/24`, `space/64`, `space/8`
- **Text styles:** `Desktop/caption`, `Desktop/h1`, `Desktop/body-l`, `Desktop/label`, `Desktop/body-s`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `chip/bg`, `chip/border`, `chip/text`, `color/border/default`, `color/surface/brand`, `color/surface/page`, `color/text/default`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/body-s`, `font/line-height/desktop/caption`, `font/line-height/desktop/h1`, `font/line-height/desktop/label`, `font/size/desktop/body-l`, `font/size/desktop/body-s`, `font/size/desktop/caption`, `font/size/desktop/h1`, `font/size/desktop/label`, `font/style/body`, `font/style/display`
<!-- ⚙️ GENERATED:end:recipe-hero -->

- **Propósito:** Cabecera de la página de receta: kicker, título, tiempo y dificultad, descripción, productos usados e imagen principal.
- **Ejemplo de código:**
  ```html
  <section class="section recipe-hero" aria-labelledby="rh-title">
  <div class="section__inner">
  <div class="recipe-hero__grid">
  <div class="recipe-hero__info">
  <span class="recipe-hero__kicker">Receta</span>
  <h1 class="page-title" id="rh-title">Ramen picante</h1>
  <ul class="recipe-hero__meta"><li><span class="icon icon-timer" aria-hidden="true"></span>10 min</li><li><span class="icon icon-circle-check" aria-hidden="true"></span>Fácil</li></ul>
  <p class="recipe-hero__description">Para quién es y por qué apetece.</p>
  <h2 class="recipe-hero__products-label">Productos que usa</h2>
  <ul class="recipe-hero__products"><li><a class="chip chip--m" href="/productos/yatekomo-pollo">Yatekomo Pollo</a></li></ul>
  </div>
  <div class="media-frame recipe-hero__media"><img src="/media/receta-ramen.jpg" alt="Ramen picante servido en un cuenco"></div>
  </div>
  </div>
  </section>
  ```
- **Accesibilidad (pares AA verificados):** Todo el texto en tinta sobre amarillo 12,3:1; chips blancos con borde de tinta. El título es el `h1`; tiempo y dificultad van como lista con iconos decorativos; los productos son enlaces (Chip M, 40 px).
- **Cuándo usar / qué NO hace:** Solo en la página de receta. Sin vídeo al principio (regla de negocio).
