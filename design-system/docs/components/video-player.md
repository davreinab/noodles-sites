### Video player   ⚙️ synced: 2026-10-07T18:41:16Z

<!-- ⚙️ GENERATED:start:video-player -->
- **Figma:** `83:70` · página «Video player» · COMPONENT_SET · 4 variantes · última sync 2026-10-07T18:41:16Z
- **Descripción (Figma):** Reproductor de vídeo como fachada. State=Poster: póster de marca (sin imagen generada con IA), botón play de 80 px (video/play-bg, borde grueso) y duración. State=Playing: al pulsar se sustituye por el reproductor real (iframe de YouTube con youtube-nocookie o &lt;video&gt; MP4) con sus controles nativos; no se carga nada de terceros antes del clic (privacidad y rendimiento). Ratio=16:9 (preparación, promo de Home, concursos) y 9:16 (recetas en vídeo vertical). Accesibilidad: el play es un &lt;button&gt; con nombre «Reproducir vídeo: &lt;título&gt; (0:45)»; foco con anillo video/focus-ring amarillo sobre el póster oscuro; subtítulos obligatorios si el vídeo tiene voz; sin autoplay con sonido; el GIF de preparación usa este mismo componente en MP4 silencioso en bucle con botón de pausa.
- **Anatomía:** `icon-play` → Icon / play
- **Ratio:** 16:9, 9:16
- **State:** Poster, Playing
- **Propiedades de componente:** `Duration#83:0` (TEXT, por defecto 0:45), `Play icon#83:5` (INSTANCE_SWAP, por defecto Icon / play), `Ratio` (VARIANT, por defecto 16:9), `State` (VARIANT, por defecto Poster)
- **Iconos / instancias anidadas:** sí · swap: `Play icon#83:5` · por defecto: Icon / play
- **Tokens que consume:** `border/width/thick`, `border/width/thin`, `font/family/body`, `font/family/display`, `font/line-height/desktop/caption`, `font/line-height/desktop/label`, `font/size/desktop/caption`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/lg`, `radius/md`, `radius/pill`, `space/4`, `space/8`, `video/border`, `video/meta-bg`, `video/meta-text`, `video/play-bg`, `video/play-icon`, `video/poster-bg`
- **Text styles:** `Desktop/caption`, `Desktop/label`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `font/family/body`, `font/family/display`, `font/line-height/desktop/caption`, `font/line-height/desktop/label`, `font/size/desktop/caption`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `video/border`, `video/meta-bg`, `video/meta-text`, `video/play-bg`, `video/play-icon`, `video/poster-bg`
<!-- ⚙️ GENERATED:end:video-player -->

- **Propósito:** Reproductor como fachada: póster de marca, botón de play y duración. Al pulsar se carga el vídeo real (YouTube sin cookies o MP4) con sus controles nativos. 16:9 por defecto; 9:16 para recetas en vertical.
- **Ejemplo de código:**
  ```html
  <div class="video-player">
  <img class="video-player__poster" src="/media/promo-poster.jpg" alt="">
  <button class="video-player__play" type="button" aria-label="Reproducir vídeo: Gana un viaje a Tokio (0:45)"><span class="icon icon-play" aria-hidden="true"></span></button>
  <span class="video-player__duration" aria-hidden="true">0:45</span>
  </div>
  <div class="video-player video-player--vertical"><span class="video-player__title">Receta en vídeo</span></div>
  ```
- **Accesibilidad (pares AA verificados):** Play: tinta sobre amarillo 12,3:1 (icono, ≥ 3:1); duración crema sobre tinta 17,2:1. Rol: el play es un `<button>` con nombre que incluye el título y la duración; al activarlo se sustituye por el iframe o `<video controls>` y el foco pasa al reproductor. Foco del play: contorno de 2 px pegado en amarillo (12,3:1 sobre el póster oscuro). Subtítulos obligatorios si hay voz; sin autoplay con sonido. No se carga nada de terceros antes del clic (privacidad).
- **Cuándo usar / qué NO hace:** Para vídeo de preparación, promo de la Home y recetas en vertical. El póster es de marca, sin imágenes generadas con IA. No se usa para GIF decorativos sin control de pausa.
