### Preparation   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:preparation -->
- **Figma:** `95:1158` · página «Pattern / Detail pages» · COMPONENT_SET · 2 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** Sección de preparación de la página de producto: título (h2) · Video player 16:9 (GIF o vídeo de preparación como MP4 silencioso en bucle, con pausa) · 3 Step en <ol> · Timer de 3 minutos. El texto de los pasos sale del envase. Desktop: pasos a la izquierda; vídeo y temporizador a la derecha (560 px). Mobile: vídeo arriba, pasos y temporizador al final (al alcance mientras se cocina). En la Recipe page se reutiliza sin el Timer y con Step Media=True. Sin variables propias.
- **Anatomía:** `video` → Ratio=16:9, State=Poster, `icon-play` → Icon / play, `step` → Media=False, `step` → Media=False, `step` → Media=False, `step` → Media=False, `timer` → State=Idle, Layout=Default, `action` → Hierarchy=Secondary, Size=M, State=Default, `icon-leading` → Icon / play, `icon-trailing` → Icon / arrow-right
- **API:** `breakpoint`: Desktop, Mobile (por defecto Desktop)
- **Nombres en Figma:** `breakpoint` ← `Breakpoint`
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `border/width/thick`, `border/width/thin`, `button/secondary/border`, `button/secondary/text`, `color/border/default`, `color/surface/card`, `color/surface/inverse`, `color/surface/page`, `color/text/brand-on-inverse`, `color/text/default`, `color/text/on-inverse`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/desktop/display`, `font/line-height/desktop/h2`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/size/desktop/body-l`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/desktop/display`, `font/size/desktop/h2`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/lg`, `icon/size/sm`, `layout/frame`, `layout/margin`, `layout/section-y`, `radius/md`, `radius/pill`, `space/16`, `space/24`, `space/32`, `space/4`, `space/48`, `space/8`, `step/number-text`, `step/text`, `timer/progress`, `video/border`, `video/meta-bg`, `video/meta-text`, `video/play-bg`, `video/play-icon`, `video/poster-bg`
- **Text styles:** `Desktop/h2`, `Desktop/body-m`, `Desktop/caption`, `Desktop/label`, `Desktop/display`, `Desktop/h3`
<!-- ⚙️ GENERATED:end:preparation -->

- **Propósito:** Preparación de la página de producto: título y subtítulo, vídeo de preparación, pasos numerados y temporizador de 3 minutos. Fondo tinta.
- **Ejemplo de código:**
  ```html
  <section data-ds="preparation" class="section preparation" aria-labelledby="prep-title">
  <div class="section__inner">
  <header class="section__header">
  <h2 class="section__title" id="prep-title">Preparation</h2>
  <p class="preparation__subtitle">Ready in just 4 steps</p>
  </header>
  <div class="preparation__grid">
  <div class="video-player preparation__media"><button class="video-player__play" type="button" aria-label="Watch the preparation video (0:45)"><span class="icon icon-play" aria-hidden="true"></span></button><span class="video-player__duration">0:45</span></div>
  <ol class="steps preparation__steps preparation__steps--first">
  <li class="step"><span class="step__number" aria-hidden="true">1</span><div class="step__content"><p class="step__text">Open the lid halfway and add boiling water up to the mark.</p></div></li>
  <li class="step"><span class="step__number" aria-hidden="true">2</span><div class="step__content"><p class="step__text">Leave to stand for 3 minutes.</p></div></li>
  </ol>
  <section class="timer" data-state="idle" aria-labelledby="timer-title-prep">
  <h3 class="timer__title" id="timer-title-prep">Not a second more!</h3>
  <p class="timer__subtitle">Use our timer to prepare your Yatekomo.</p>
  <span class="timer__time" role="timer">3:00</span>
  <p class="timer__label">Ready</p>
  <progress class="timer__bar" max="100" value="100" aria-label="Time remaining"></progress>
  <div class="timer__controls">
  <button class="button button--secondary" type="button"><span class="icon icon-play" aria-hidden="true"></span>Start</button>
  </div>
  <p class="visually-hidden" aria-live="polite"></p>
  </section>
  <ol class="steps preparation__steps preparation__steps--second" start="3">
  <li class="step"><span class="step__number" aria-hidden="true">3</span><div class="step__content"><p class="step__text">Drain the water (careful! contents very hot).</p></div></li>
  <li class="step"><span class="step__number" aria-hidden="true">4</span><div class="step__content"><p class="step__text">Add the sauce sachet and enjoy your Yatekomo.</p></div></li>
  </ol>
  </div>
  </div>
  </section>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Título en `h2` sobre tinta (texto crema 17,2:1; subtítulo amarillo de marca 12,3:1). Orden del DOM = orden de lectura: vídeo, pasos 1-2, temporizador, pasos 3-4. Los pasos son dos `ol`; la segunda empieza en 3 (`start="3"`) para que el lector anuncie la posición correcta. En escritorio la rejilla los coloca por filas en ese mismo orden; en móvil es una columna. El vídeo no arranca solo. El temporizador anuncia solo el cambio de estado.
- **Cuándo usar / qué NO hace:** En la página de producto. En la receta se reutiliza sin Timer y con Step con media.
