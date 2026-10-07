### Promo   ⚙️ synced: 2026-10-07T18:49:29Z

<!-- ⚙️ GENERATED:start:promo -->
- **Figma:** `91:113` · página «Pattern / Promo» · COMPONENT_SET · 2 variantes · última sync 2026-10-07T18:49:29Z
- **Descripción (Figma):** Módulo de promoción o concurso de la Home: Video player 16:9 (fachada) · Badge «Concurso» · título (h2) · texto · Button Primary «Participar» · Link de bases legales (obligatorio). Fondo color/surface/page (crema) para que el póster oscuro del vídeo se distinga; texto color/text/default. Se oculta entero si no hay promoción activa (regla de negocio); si el concurso es iframe de agencia, el CTA lleva external-link y el iframe necesita revisión de protección de datos antes de publicarse. Desktop: vídeo a la izquierda; Mobile: vídeo arriba. Sin variables propias.
- **Anatomía:** `video` → Ratio=16:9, State=Poster, `icon-play` → Icon / play, `badge` → Type=New, `cta` → Hierarchy=Primary, Size=L, State=Default, `icon-leading` → Icon / arrow-right, `icon-trailing` → Icon / arrow-right, `rules-link` → Type=Inline, Surface=Light, State=Default, `icon-trailing` → Icon / arrow-right
- **Breakpoint:** Desktop, Mobile
- **Propiedades de componente:** `Breakpoint` (VARIANT, por defecto Desktop)
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `badge/new/bg`, `badge/new/text`, `border/width/thick`, `border/width/thin`, `button/primary/bg`, `button/primary/border`, `button/primary/text`, `color/surface/page`, `color/text/default`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/desktop/h2`, `font/line-height/desktop/label`, `font/line-height/mobile/label`, `font/size/desktop/body-l`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/desktop/h2`, `font/size/desktop/label`, `font/size/mobile/label`, `font/style/body`, `font/style/display`, `icon/size/lg`, `icon/size/sm`, `layout/frame`, `layout/margin`, `layout/section-y`, `link/default`, `radius/md`, `radius/pill`, `space/16`, `space/24`, `space/32`, `space/4`, `space/64`, `space/8`, `video/border`, `video/meta-bg`, `video/meta-text`, `video/play-bg`, `video/play-icon`, `video/poster-bg`
- **Text styles:** `Desktop/caption`, `Desktop/label`, `Mobile/label`, `Desktop/h2`, `Desktop/body-l`, `Desktop/body-m`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `badge/new/bg`, `badge/new/text`, `button/primary/bg`, `button/primary/border`, `button/primary/text`, `color/surface/page`, `color/text/default`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/desktop/h2`, `font/line-height/desktop/label`, `font/line-height/mobile/label`, `font/size/desktop/body-l`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/desktop/h2`, `font/size/desktop/label`, `font/size/mobile/label`, `font/style/body`, `font/style/display`, `link/default`, `video/border`, `video/meta-bg`, `video/meta-text`, `video/play-bg`, `video/play-icon`, `video/poster-bg`
<!-- ⚙️ GENERATED:end:promo -->

- **Propósito:** Módulo de promoción o concurso de la Home con vídeo, título, texto, «Participar» y bases legales. Se oculta entero si no hay promoción activa.
- **Ejemplo de código:**
  ```html
  <section class="section promo" aria-labelledby="promo-title">
  <div class="section__inner">
  <div class="promo__grid">
  <div class="video-player"><button class="video-player__play" type="button" aria-label="Reproducir vídeo de la campaña (0:45)"><span class="icon icon-play" aria-hidden="true"></span></button></div>
  <div class="promo__content">
  <span class="badge">Concurso</span>
  <h2 class="section__title" id="promo-title">Nombre de la campaña</h2>
  <p class="promo__body">Qué se gana, hasta cuándo y cómo participar.</p>
  <div class="promo__actions"><a class="button button--l" href="/concursos/tokio">Participar</a><a class="link" href="/concursos/tokio/bases">Bases legales</a></div>
  </div>
  </div>
  </div>
  </section>
  ```
- **Accesibilidad (pares AA verificados):** Texto tinta sobre crema 17,2:1; el póster oscuro del vídeo se distingue del fondo crema. Sección con encabezado `h2`; el vídeo es la fachada del Video player. Si el CTA abre un concurso externo o un iframe, se avisa y el iframe pasa revisión de protección de datos.
- **Cuándo usar / qué NO hace:** Solo con promoción activa; sin ella, la sección no se pinta (sin hueco ni mensaje). No es el Hero ni un Banner.
