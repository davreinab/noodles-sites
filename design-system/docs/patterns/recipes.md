### Recipes   ⚙️ synced: 2026-10-08T11:52:41Z

<!-- ⚙️ GENERATED:start:recipes -->
- **Figma:** `92:215` · página «Pattern / Home» · COMPONENT_SET · 2 variantes · última sync 2026-10-08T11:52:41Z
- **Descripción (Figma):** Sección de recetas (Home y página de producto con las recetas que lo usan; wireframe UX): título (h2) + entradilla · Button Secondary L «See all recipes» a la Recipe library (desktop junto al título, a la derecha; mobile debajo de las cards) · Recipe card. Desktop: 4 columnas; Mobile: scroll horizontal con la siguiente card asomando. Fondo color/surface/card para alternar con las secciones crema. Sin buscador por ingredientes (regla de negocio). Comensales («2 people»): sin definir, falta información. Sin variables propias.
- **Anatomía:** `cta` → Hierarchy=Secondary, Size=L, State=Default, `icon-leading` → Icon / arrow-right, `icon-trailing` → Icon / arrow-right, `recipe-card` → State=Default, `icon-time` → Icon / timer, `product-chip` → Size=S, State=Default, `icon-leading` → Icon / check, `product-chip` → Size=S, State=Default, `icon-leading` → Icon / check, `recipe-card` → State=Default, `icon-time` → Icon / timer, `product-chip` → Size=S, State=Default, `icon-leading` → Icon / check, `product-chip` → Size=S, State=Default, `icon-leading` → Icon / check, `recipe-card` → State=Default, `icon-time` → Icon / timer, `product-chip` → Size=S, State=Default, `icon-leading` → Icon / check, `product-chip` → Size=S, State=Default, `icon-leading` → Icon / check, `recipe-card` → State=Default, `icon-time` → Icon / timer, `product-chip` → Size=S, State=Default, `icon-leading` → Icon / check, `product-chip` → Size=S, State=Default, `icon-leading` → Icon / check
- **Breakpoint:** Desktop, Mobile
- **Propiedades de componente:** `Breakpoint` (VARIANT, por defecto Desktop)
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `border/width/thick`, `border/width/thin`, `button/secondary/border`, `button/secondary/text`, `chip/bg`, `chip/border`, `chip/height/s`, `chip/text`, `color/effect/shadow-ink`, `color/surface/card`, `color/text/default`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/body-s`, `font/line-height/desktop/caption`, `font/line-height/desktop/h2`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/size/desktop/body-l`, `font/size/desktop/body-s`, `font/size/desktop/caption`, `font/size/desktop/h2`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/sm`, `layout/frame`, `layout/gutter`, `layout/margin`, `layout/section-y`, `radius/md`, `radius/none`, `radius/pill`, `recipe-card/bg`, `recipe-card/border`, `recipe-card/media-bg`, `recipe-card/meta`, `recipe-card/title`, `space/16`, `space/24`, `space/32`, `space/8`
- **Text styles:** `Desktop/h2`, `Desktop/body-l`, `Desktop/label`, `Desktop/caption`, `Desktop/body-s`, `Desktop/h3`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `button/secondary/border`, `button/secondary/text`, `chip/bg`, `chip/border`, `chip/text`, `color/effect/shadow-ink`, `color/surface/card`, `color/text/default`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/body-s`, `font/line-height/desktop/caption`, `font/line-height/desktop/h2`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/size/desktop/body-l`, `font/size/desktop/body-s`, `font/size/desktop/caption`, `font/size/desktop/h2`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `recipe-card/bg`, `recipe-card/border`, `recipe-card/media-bg`, `recipe-card/meta`, `recipe-card/title`
<!-- ⚙️ GENERATED:end:recipes -->

- **Propósito:** Recetas en la Home y en la ficha de producto (wireframe UX): título, entradilla, «See all recipes» y Recipe card en carrusel.
- **Ejemplo de código:**
  ```html
  <section class="section recipes" aria-labelledby="rc-title">
  <div class="section__inner">
  <div class="section__header"><h2 class="section__title" id="rc-title">We haven’t forgotten you, keen cook</h2><p class="section__lead">Explore and learn recipes to glow up your meals</p></div>
  <a class="button button--secondary button--l recipes__cta" href="/recetas">See all recipes</a>
  <ul class="carousel">
  <li><article class="recipe-card"><div class="recipe-card__body"><p class="recipe-card__meta"><span class="icon icon-timer" aria-hidden="true"></span>20 minutes</p><h3 class="recipe-card__title"><a class="recipe-card__link" href="/recetas/spicy-noodle-salad">Spicy Noodle Salad with almond and mint</a></h3></div></article></li>
  </ul>
  </div>
  </section>
  ```
- **Accesibilidad (pares AA verificados):** Título tinta sobre blanco 18:1; entradilla secundaria 7,9:1. El carrusel es una lista desplazable con teclado. El botón «See all recipes» va junto al título en desktop y debajo de las cards en móvil (mismo elemento, reordenado con CSS).
- **Cuándo usar / qué NO hace:** En la Home (4 cards) y en la ficha de producto (las recetas que lo usan). Sin buscador por ingredientes (regla de negocio). Comensales: sin definir, falta información.
