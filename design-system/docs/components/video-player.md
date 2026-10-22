### Video player   ⚙️ synced: 2026-10-22T09:37:04Z

<!-- ⚙️ GENERATED:start:video-player -->
- **Figma:** `83:70` · página «Content» · COMPONENT_SET · 4 variantes · última sync 2026-10-22T09:37:04Z
- **Descripción (Figma):** Reproductor de vídeo como fachada. State=Poster: póster de marca (sin imagen generada con IA), botón play de 80 px (video/play-bg, borde grueso) y duración. State=Playing: al pulsar se sustituye por el reproductor real (iframe de YouTube con youtube-nocookie o <video> MP4) con sus controles nativos; no se carga nada de terceros antes del clic (privacidad y rendimiento). Ratio=16:9 (preparación, promo de Home, concursos) y 9:16 (recetas en vídeo vertical). Accesibilidad: el play es un <button> con nombre «Reproducir vídeo: <título> (0:45)»; foco con anillo video/focus-ring amarillo sobre el póster oscuro; subtítulos obligatorios si el vídeo tiene voz; sin autoplay con sonido; el GIF de preparación usa este mismo componente en MP4 silencioso en bucle con botón de pausa.
- **Anatomía:** `icon-play` → Icon / play
- **API:** `duration` (string, por defecto 0:45) · `playIcon` (icon, por defecto Icon / play) · `ratio`: 16:9, 9:16 (por defecto 16:9) · `poster` (boolean, por defecto true) · `playing` (boolean, por defecto false)
- **Nombres en Figma:** `duration` ← `Duration#83:0`, `playIcon` ← `Play icon#83:5`, `ratio` ← `Ratio`, `poster` ← `State=Poster`, `playing` ← `State=Playing`
- **Iconos / instancias anidadas:** sí · swap: `playIcon` · por defecto: Icon / play
- **Tokens que consume:** `border/width/thick`, `border/width/thin`, `font/family/body`, `font/family/display`, `font/line-height/desktop/caption`, `font/line-height/desktop/label`, `font/size/desktop/caption`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/lg`, `radius/md`, `radius/pill`, `space/4`, `space/8`, `video/border`, `video/meta-bg`, `video/meta-text`, `video/play-bg`, `video/play-icon`, `video/poster-bg`
- **Text styles:** `Desktop/caption`, `Desktop/label`
<!-- ⚙️ GENERATED:end:video-player -->

- **Propósito:** Reproductor como fachada: póster de marca, botón de play y duración. Al pulsar se carga el vídeo real (YouTube sin cookies o MP4) con sus controles nativos. 16:9 por defecto; 9:16 para recetas en vertical.
- **Ejemplo de código:**
  ```html
  <div data-ds="video-player" class="video-player">
  <img class="video-player__poster" src="/media/promo-poster.jpg" alt="">
  <button class="video-player__play" type="button" aria-label="Reproducir vídeo: Gana un viaje a Tokio (0:45)"><span class="icon icon-play" aria-hidden="true"></span></button>
  <span class="video-player__duration" aria-hidden="true">0:45</span>
  </div>
  <div data-ds="video-player" class="video-player video-player--vertical"><span class="video-player__title">Receta en vídeo</span></div>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Play: tinta sobre amarillo 12,3:1 (icono, ≥ 3:1); duración crema sobre tinta 17,2:1. Rol: el play es un `<button>` con nombre que incluye el título y la duración; al activarlo se sustituye por el iframe o `<video controls>` y el foco pasa al reproductor. Foco del play: contorno de 2 px pegado en amarillo (12,3:1 sobre el póster oscuro). Subtítulos obligatorios si hay voz; sin autoplay con sonido. No se carga nada de terceros antes del clic (privacidad).
- **Cuándo usar / qué NO hace:** Para vídeo de preparación, promo de la Home y recetas en vertical. El póster es de marca, sin imágenes generadas con IA. No se usa para GIF decorativos sin control de pausa.
