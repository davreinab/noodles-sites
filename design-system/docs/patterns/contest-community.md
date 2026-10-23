### Contest community   ⚙️ synced: 2026-10-23T09:22:57Z

<!-- ⚙️ GENERATED:start:contest-community -->
- **Figma:** `313:3452` · página «Pattern / Detail pages» · COMPONENT_SET · 2 variantes · última sync 2026-10-23T09:22:57Z
- **Descripción (Figma):** Contest community: comunidad y ganadores (wireframe 330:6742 desktop, 361:8675 móvil). Fondo surface/card. h2 «Real moments from past winners» con subtítulo, Video player 16:9 (poster), h3 «Shared by the community» y fila desplazable (recorte) de Community card con pie «@user · producto». Clase CSS: .contest-community. ⬜ TODO GB Foods/agencia: vídeo y fotos reales con permiso de publicación; usuarios de la comunidad.
- **Anatomía:** `Video player` → Ratio=16:9, State=Poster, `icon-play` → Icon / play, `Community card` → Community card, `Community card` → Community card, `Community card` → Community card, `Community card` → Community card, `Community card` → Community card
- **API:** `breakpoint`: Desktop, Mobile (por defecto Desktop)
- **Nombres en Figma:** `breakpoint` ← `Breakpoint`
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `border/width/thick`, `border/width/thin`, `color/border/default`, `color/surface/card`, `color/text/default`, `color/text/secondary`, `contest-card/media-bg`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/desktop/h2`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/desktop/h2`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/lg`, `layout/margin`, `radius/md`, `radius/pill`, `space/16`, `space/4`, `space/64`, `space/8`, `video/border`, `video/meta-bg`, `video/meta-text`, `video/play-bg`, `video/play-icon`, `video/poster-bg`
- **Text styles:** `Desktop/h2`, `Desktop/body-m`, `Desktop/caption`, `Desktop/label`, `Desktop/h3`
<!-- ⚙️ GENERATED:end:contest-community -->

- **Propósito:** Vídeo de los ganadores y fila de fotos de la comunidad: título «Real moments from past winners» y entradilla, el Video player ancho, y debajo el h3 «Shared by the community» con las Community card. Fondo blanco.
- **Ejemplo de código:** Vídeo y tres fotos; la lista lleva el resto de Community card.
  ```html
  <section data-ds="contest-community" class="section contest-community" aria-labelledby="cc2-title">
  <div class="section__inner">
  <div class="section__header">
  <h2 class="section__title" id="cc2-title">Real moments from past winners</h2>
  <p class="section__lead">Past festival-weekend winners share what they walked away with.</p>
  </div>
  <div data-ds="video-player" class="video-player">
  <img class="video-player__poster" src="../assets/images/placeholder.svg" alt="">
  <button class="video-player__play" type="button" aria-label="Play video: Real moments from past winners (0:45)"><span class="icon icon-play" aria-hidden="true"></span></button>
  <span class="video-player__duration" aria-hidden="true">0:45</span>
  </div>
  <h3 class="contest-community__heading" id="cc2-shared">Shared by the community</h3>
  <ul class="contest-community__list" tabindex="0" aria-label="Shared by the community">
  <li><figure data-ds="community-card" class="community-card"><div class="community-card__media"><img src="../assets/images/placeholder.svg" alt=""></div><figcaption class="community-card__caption">@user2 · Home Ramen Kit unboxing</figcaption></figure></li>
  <li><figure data-ds="community-card" class="community-card"><div class="community-card__media"><img src="../assets/images/placeholder.svg" alt=""></div><figcaption class="community-card__caption">@user3 · Merch pack haul</figcaption></figure></li>
  <li><figure data-ds="community-card" class="community-card"><div class="community-card__media"><img src="../assets/images/placeholder.svg" alt=""></div><figcaption class="community-card__caption">@user4 · Weekend winner tour</figcaption></figure></li>
  </ul>
  </div>
  </section>
  ```
  El vídeo sigue el marcado y la accesibilidad de Video player; el texto del botón de reproducir lo da su `aria-label`.
- **Accesibilidad (rol, nombre, estados y teclado):** La sección tiene nombre por su h2. La lista de fotos es enfocable (`tabindex="0"`) y se desplaza con el teclado en móvil, con nombre («Shared by the community»); su contorno de foco es el de Contest prizes. Cada foto es una `figure` con pie (el pie dice quién la comparte). El vídeo: su poster es decorativo y el botón de reproducir lleva el nombre del vídeo. Contraste: texto tinta sobre blanco. Duración visible con `aria-hidden` (el botón ya dice el tiempo en su nombre).
- **Cuándo usar / qué NO hace:** Solo en la página de concurso, después del formulario de FAQ. Cuidado de contenido: los vídeos y las fotos de ganadores tienen condiciones de imagen (permiso de cada persona), y los nombres de usuario y el vídeo son ⬜ TODO. No es un muro de redes sociales ni se carga desde una API: el contenido se pone a mano.
