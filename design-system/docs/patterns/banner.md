### Banner   ⚙️ synced: 2026-10-07T18:43:11Z

<!-- ⚙️ GENERATED:start:banner -->
- **Figma:** `92:884` · página «Pattern / Banner» · COMPONENT_SET · 2 variantes · última sync 2026-10-07T18:43:11Z
- **Descripción (Figma):** Banner promocional de la Home (lanzamiento, sabor nuevo, mensaje de campaña): bloque color/surface/accent (naranja de marca) con borde de tinta, radius/lg y elevation/2 (sombra dura de marca) · titular (h1) · texto · Button Primary · imagen de marca. Sobre el acento solo va color/text/default (regla del token). Desktop: texto a la izquierda; Mobile: texto arriba e imagen debajo. No es un carrusel. Sin variables propias.
- **Anatomía:** `cta` → Hierarchy=Primary, Size=L, State=Default, `icon-leading` → Icon / arrow-right, `icon-trailing` → Icon / arrow-right
- **Breakpoint:** Desktop, Mobile
- **Propiedades de componente:** `Breakpoint` (VARIANT, por defecto Desktop)
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `border/width/thick`, `border/width/thin`, `button/primary/bg`, `button/primary/border`, `button/primary/text`, `color/border/default`, `color/effect/shadow-ink`, `color/surface/accent`, `color/surface/page`, `color/text/default`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/caption`, `font/line-height/desktop/h1`, `font/line-height/desktop/label`, `font/size/desktop/body-l`, `font/size/desktop/caption`, `font/size/desktop/h1`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/sm`, `layout/frame`, `layout/margin`, `layout/section-y`, `radius/lg`, `radius/md`, `radius/pill`, `space/16`, `space/24`, `space/32`, `space/48`, `space/8`
- **Text styles:** `Desktop/h1`, `Desktop/body-l`, `Desktop/label`, `Desktop/caption`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `button/primary/bg`, `button/primary/border`, `button/primary/text`, `color/border/default`, `color/effect/shadow-ink`, `color/surface/accent`, `color/surface/page`, `color/text/default`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/caption`, `font/line-height/desktop/h1`, `font/line-height/desktop/label`, `font/size/desktop/body-l`, `font/size/desktop/caption`, `font/size/desktop/h1`, `font/size/desktop/label`, `font/style/body`, `font/style/display`
<!-- ⚙️ GENERATED:end:banner -->

- **Propósito:** Banner de la Home para lanzamientos o mensajes de campaña: bloque naranja de acento con titular, texto, CTA e imagen.
- **Ejemplo de código:**
  ```html
  <section class="section banner" aria-labelledby="bn-title">
  <div class="section__inner">
  <div class="banner__box">
  <div class="banner__content"><h2 class="banner__title" id="bn-title">Nuevo sabor</h2><p class="banner__body">Texto del lanzamiento.</p><a class="button button--l" href="/productos/nuevo">Saber más</a></div>
  <div class="media-frame banner__media"><img src="/media/banner.jpg" alt=""></div>
  </div>
  </div>
  </section>
  ```
- **Accesibilidad (pares AA verificados):** Tinta sobre naranja 7,1:1 (sobre el acento solo va tinta, regla del token); botón crema sobre tinta 17,2:1. Sección con encabezado; la imagen es decorativa si el titular ya lo dice todo.
- **Cuándo usar / qué NO hace:** Uno como máximo en la Home. No es un carrusel ni sustituye al Hero o a la Promo.
