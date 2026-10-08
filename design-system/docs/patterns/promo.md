### Promo   ⚙️ synced: 2026-10-08T11:52:41Z

<!-- ⚙️ GENERATED:start:promo -->
- **Figma:** `91:113` · página «Pattern / Home» · COMPONENT_SET · 2 variantes · última sync 2026-10-08T11:52:41Z
- **Descripción (Figma):** Módulo de promoción o concurso de la Home (wireframe UX): arte de la campaña (PNG recortado, de marca) · título (h2) · texto con los premios · Button Primary L «I want to participate» · Link de bases legales (obligatorio por regla de negocio, aunque el wireframe no lo dibuja) · Video player 16:9 (fachada) o imagen grande de la campaña. Fondo color/surface/brand (amarillo) con la trama de fideos (Decoration / Noodle texture) a sangre por la derecha, detrás del contenido, como el módulo natural de las landings. Se oculta entero si no hay promoción activa (regla de negocio); si el concurso es iframe de agencia, el CTA lleva external-link y el iframe necesita revisión de protección de datos. Desktop: texto a la izquierda y vídeo a la derecha; Mobile: vídeo arriba. Sin variables propias.
- **Anatomía:** `noodle-texture` → Decoration / Noodle texture, `noodle` → Shape=1, Tone=Texture, `noodle` → Shape=3, Tone=Texture, `noodle` → Shape=5, Tone=Texture, `noodle` → Shape=2, Tone=Texture, `noodle` → Shape=4, Tone=Texture, `cta` → Hierarchy=Primary, Size=L, State=Default, `icon-leading` → Icon / arrow-right, `icon-trailing` → Icon / arrow-right, `rules-link` → Type=Inline, Surface=Light, State=Default, `icon-trailing` → Icon / arrow-right, `video` → Ratio=16:9, State=Poster, `icon-play` → Icon / play
- **Breakpoint:** Desktop, Mobile
- **Propiedades de componente:** `Breakpoint` (VARIANT, por defecto Desktop)
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `border/width/thick`, `border/width/thin`, `button/primary/bg`, `button/primary/border`, `button/primary/text`, `color/surface/brand`, `color/text/default`, `color/text/secondary`, `decoration/noodle/texture`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/desktop/h2`, `font/line-height/desktop/label`, `font/size/desktop/body-l`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/desktop/h2`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/lg`, `icon/size/sm`, `layout/frame`, `layout/margin`, `layout/section-y`, `link/default`, `radius/md`, `radius/pill`, `space/16`, `space/24`, `space/32`, `space/4`, `space/64`, `space/8`, `video/border`, `video/meta-bg`, `video/meta-text`, `video/play-bg`, `video/play-icon`, `video/poster-bg`
- **Text styles:** `Desktop/caption`, `Desktop/h2`, `Desktop/body-l`, `Desktop/label`, `Desktop/body-m`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `button/primary/bg`, `button/primary/border`, `button/primary/text`, `color/surface/brand`, `color/text/default`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/desktop/h2`, `font/line-height/desktop/label`, `font/size/desktop/body-l`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/desktop/h2`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `link/default`, `video/border`, `video/meta-bg`, `video/meta-text`, `video/play-bg`, `video/play-icon`, `video/poster-bg`
<!-- ⚙️ GENERATED:end:promo -->

- **Propósito:** Concurso o promoción activa en la Home (wireframe UX): arte de la campaña, título, premios, CTA de participación, bases legales y vídeo.
- **Ejemplo de código:**
  ```html
  <section class="section promo" aria-labelledby="pr-title">
  <div class="decoration-noodle-texture" aria-hidden="true"><span class="decoration-noodle decoration-noodle--texture"></span><span class="decoration-noodle decoration-noodle--3 decoration-noodle--texture"></span><span class="decoration-noodle decoration-noodle--5 decoration-noodle--texture"></span><span class="decoration-noodle decoration-noodle--2 decoration-noodle--texture"></span><span class="decoration-noodle decoration-noodle--4 decoration-noodle--texture"></span></div>
  <div class="section__inner">
  <div class="promo__grid">
  <div class="promo__content">
  <figure class="promo__art"><img src="/media/campana-arte.png" alt="Conoce a Marc Cucurella. Participa y podrás ganar más premios"></figure>
  <h2 class="section__title" id="pr-title">Enter Yatekomo’s new giveaway and win prizes</h2>
  <p class="promo__body">Official Spanish National Team jerseys and soccer balls signed by Marc Cucurella.</p>
  <div class="promo__actions"><a class="button button--l" href="/concursos/cucurella">I want to participate</a><a class="link" href="/concursos/cucurella/bases">Bases legales</a></div>
  </div>
  <div class="promo__media"><div class="video-player"><img src="/media/poster.jpg" alt=""></div></div>
  </div>
  </div>
  </section>
  ```
- **Accesibilidad (pares AA verificados):** Tinta sobre amarillo 12,3:1 y sobre el ámbar de la trama ≥ 9:1 (la trama es decorativa, `aria-hidden`). El arte de campaña lleva texto alternativo con lo que dice la pieza. Las bases legales son un enlace visible (obligatorio). El vídeo sigue el contrato de Video player.
- **Cuándo usar / qué NO hace:** Solo con una promoción activa; sin ella, la sección se oculta entera (regla de negocio). Si el concurso es iframe de agencia, el CTA lleva external-link y necesita revisión de protección de datos.
