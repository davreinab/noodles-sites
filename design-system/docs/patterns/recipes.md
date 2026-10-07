### Recipes   ⚙️ synced: 2026-10-07T18:41:16Z

<!-- ⚙️ GENERATED:start:recipes -->
- **Figma:** `92:215` · página «Pattern / Recipes» · COMPONENT_SET · 2 variantes · última sync 2026-10-07T18:41:16Z
- **Descripción (Figma):** Sección de recetas (Home, página de producto con las recetas que lo usan): título (h2) + entradilla · 3 Recipe card · Link «Ver todas las recetas» a la Recipe library. Fondo color/surface/card para alternar con las secciones crema. Desktop: 3 columnas (421 px); Mobile: scroll horizontal con la siguiente card asomando y el enlace debajo. Sin buscador por ingredientes (regla de negocio). Sin variables propias.
- **Anatomía:** `link` → Type=Standalone, Surface=Light, State=Default, `icon-trailing` → Icon / arrow-right, `recipe-card` → State=Default, `icon-time` → Icon / timer, `product-chip` → Size=S, State=Default, `icon-leading` → Icon / check
- **Breakpoint:** Desktop, Mobile
- **Propiedades de componente:** `Breakpoint` (VARIANT, por defecto Desktop)
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `border/width/thin`, `chip/bg`, `chip/border`, `chip/height/s`, `chip/text`, `color/effect/shadow-ink`, `color/surface/card`, `color/text/default`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/body-s`, `font/line-height/desktop/caption`, `font/line-height/desktop/h2`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/size/desktop/body-l`, `font/size/desktop/body-s`, `font/size/desktop/caption`, `font/size/desktop/h2`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/sm`, `layout/frame`, `layout/gutter`, `layout/margin`, `layout/section-y`, `link/default`, `radius/md`, `radius/pill`, `recipe-card/bg`, `recipe-card/border`, `recipe-card/media-bg`, `recipe-card/meta`, `recipe-card/title`, `space/16`, `space/24`, `space/32`, `space/8`
- **Text styles:** `Desktop/h2`, `Desktop/body-l`, `Desktop/label`, `Desktop/caption`, `Desktop/h3`, `Desktop/body-s`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `chip/bg`, `chip/border`, `chip/text`, `color/effect/shadow-ink`, `color/surface/card`, `color/text/default`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/body-s`, `font/line-height/desktop/caption`, `font/line-height/desktop/h2`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/size/desktop/body-l`, `font/size/desktop/body-s`, `font/size/desktop/caption`, `font/size/desktop/h2`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `link/default`, `recipe-card/bg`, `recipe-card/border`, `recipe-card/media-bg`, `recipe-card/meta`, `recipe-card/title`
<!-- ⚙️ GENERATED:end:recipes -->

- **Propósito:** Sección de recetas (Home y página de producto con las recetas que lo usan): título, entradilla, tres Recipe card y enlace a la librería.
- **Ejemplo de código:**
  ```html
  <section class="section recipes" aria-labelledby="rc-title">
  <div class="section__inner">
  <div class="section__bar"><div class="section__header"><h2 class="section__title" id="rc-title">Hackea tu noodle</h2><p class="section__lead">Recetas rápidas con nuestros productos.</p></div><a class="link link--standalone" href="/recetas">Ver todas las recetas <span class="icon icon-arrow-right" aria-hidden="true"></span></a></div>
  <ul class="carousel carousel--3">
  <li><article class="recipe-card"><div class="recipe-card__body"><h3 class="recipe-card__title"><a class="recipe-card__link" href="/recetas/ramen">Ramen picante</a></h3></div></article></li>
  </ul>
  </div>
  </section>
  ```
- **Accesibilidad (pares AA verificados):** Título tinta sobre blanco 18,7:1; entradilla gris cálido sobre blanco 5,9:1. Lista de cards; en móvil se desplaza en horizontal con la siguiente asomando. Sin buscador por ingredientes (regla de negocio).
- **Cuándo usar / qué NO hace:** En la Home y en la página de producto. No es la Recipe library (que usa Library).
