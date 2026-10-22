### Timer   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:timer -->
- **Figma:** `82:143` · página «Content» · COMPONENT_SET · 8 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** Temporizador de preparación de 3 minutos (punto 8 de la SPEC, wireframe UX 396:6073 en el archivo 1YhsCqdqYCHlK4Y82IY5G3). Tarjeta con fondo color/surface/card, borde fino (timer/border), radio md. Contenido: título «Not a second more!», subtítulo «Use our timer to prepare your Yatekomo», tiempo grande en display (timer/time) con etiqueta de estado, barra lineal de progreso (pista timer/track y relleno timer/progress; sustituye al anillo) y botones: Start como Button Secondary con icono play, y Reset como link (Layout=Default) o como Icon button con icono rotate-ccw (Layout=Compact). Ejes: State=Idle, Running, Paused, Done · Layout=Default (desktop, 560 px) y Compact (mobile, 327 px: fila tiempo · Start · reset).
- **Anatomía:** `action` → Hierarchy=Secondary, Size=M, State=Default, `icon-leading` → Icon / play, `icon-trailing` → Icon / arrow-right
- **API:** `running` (boolean, por defecto false) · `paused` (boolean, por defecto false) · `done` (boolean, por defecto false) · `layout`: Default, Compact (por defecto Default)
- **Nombres en Figma:** `running` ← `State=Running`, `paused` ← `State=Paused`, `done` ← `State=Done`, `layout` ← `Layout`
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `border/width/thick`, `border/width/thin`, `button/secondary/border`, `button/secondary/text`, `color/border/default`, `color/surface/card`, `color/surface/page`, `color/text/default`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-m`, `font/line-height/desktop/display`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/size/desktop/body-m`, `font/size/desktop/display`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/sm`, `radius/md`, `radius/pill`, `space/16`, `space/24`, `space/32`, `space/8`, `timer/progress`
- **Text styles:** `Desktop/h3`, `Desktop/body-m`, `Desktop/display`, `Desktop/label`
<!-- ⚙️ GENERATED:end:timer -->

- **Propósito:** Temporizador de preparación de 3 minutos: título, subtítulo, tiempo grande, etiqueta de estado (Ready · Remaining · Paused · Done!), barra de progreso lineal y controles (Start · Pause · Resume · Reset). Variante Compact para móvil: tiempo y botón en una fila, etiqueta y barra debajo.
- **Ejemplo de código:**
  ```html
  <section data-ds="timer" class="timer" data-state="running" aria-labelledby="timer-title">
  <h3 class="timer__title" id="timer-title">Not a second more!</h3>
  <p class="timer__subtitle">Use our timer to prepare your Yatekomo.</p>
  <span class="timer__time" role="timer">1:48</span>
  <p class="timer__label">Remaining</p>
  <progress class="timer__bar" max="100" value="60" aria-label="Time remaining"></progress>
  <div class="timer__controls">
  <button class="button button--secondary" type="button"><span class="icon icon-pause" aria-hidden="true"></span>Pause</button>
  <button class="timer__reset" type="button"><span>Reset</span><span class="icon icon-arrow-right" aria-hidden="true"></span></button>
  <button class="icon-button icon-button--secondary timer__reset-icon" type="button" aria-label="Reset"><span class="icon icon-rotate-ccw" aria-hidden="true"></span></button>
  </div>
  <p class="visually-hidden" aria-live="polite"></p>
  </section>
  <section data-ds="timer" class="timer" data-state="idle" aria-labelledby="timer-title-ready">
  <h3 class="timer__title" id="timer-title-ready">Not a second more!</h3>
  <p class="timer__subtitle">Use our timer to prepare your Yatekomo.</p>
  <span class="timer__time" role="timer">3:00</span>
  <p class="timer__label">Ready</p>
  <progress class="timer__bar" max="100" value="100" aria-label="Time remaining"></progress>
  <div class="timer__controls">
  <button class="button button--secondary" type="button"><span class="icon icon-play" aria-hidden="true"></span>Start</button>
  </div>
  <p class="visually-hidden" aria-live="polite"></p>
  </section>
  <section data-ds="timer" class="timer" data-state="paused" aria-labelledby="timer-title-paused">
  <h3 class="timer__title" id="timer-title-paused">Not a second more!</h3>
  <p class="timer__subtitle">Use our timer to prepare your Yatekomo.</p>
  <span class="timer__time" role="timer">1:48</span>
  <p class="timer__label">Paused</p>
  <progress class="timer__bar" max="100" value="60" aria-label="Time remaining"></progress>
  <div class="timer__controls">
  <button class="button button--secondary" type="button"><span class="icon icon-play" aria-hidden="true"></span>Resume</button>
  <button class="timer__reset" type="button"><span>Reset</span><span class="icon icon-arrow-right" aria-hidden="true"></span></button>
  <button class="icon-button icon-button--secondary timer__reset-icon" type="button" aria-label="Reset"><span class="icon icon-rotate-ccw" aria-hidden="true"></span></button>
  </div>
  <p class="visually-hidden" aria-live="polite">Paused</p>
  </section>
  <section data-ds="timer" class="timer" data-state="done" aria-labelledby="timer-title-done">
  <h3 class="timer__title" id="timer-title-done">Not a second more!</h3>
  <p class="timer__subtitle">Use our timer to prepare your Yatekomo.</p>
  <span class="timer__time" role="timer">0:00</span>
  <p class="timer__label">Done!</p>
  <progress class="timer__bar" max="100" value="100" aria-label="Time remaining"></progress>
  <div class="timer__controls">
  <button class="timer__reset" type="button"><span>Reset</span><span class="icon icon-arrow-right" aria-hidden="true"></span></button>
  <button class="icon-button icon-button--secondary timer__reset-icon" type="button" aria-label="Reset"><span class="icon icon-rotate-ccw" aria-hidden="true"></span></button>
  </div>
  <p class="visually-hidden" aria-live="polite">Done!</p>
  </section>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Título en `h3` y la sección se nombra con él. El tiempo va en `role="timer"` (no anuncia cada segundo) y la etiqueta de estado es texto. La barra es un `progress` nativo: rol progressbar con su valor (`value`, % de tiempo que queda) y nombre (`aria-label`). La región `aria-live="polite"` solo anuncia el cambio de estado, no los segundos. El botón principal cambia de nombre (Start, Pause, Resume). Reset es un botón de texto en escritorio y de icono en móvil (con `aria-label`); el otro se oculta con `display`, así que no aparece dos veces en el árbol de accesibilidad. Estado en texto además de la barra. La barra es tinta sobre la pista arena: 13,7:1 (WCAG 1.4.11, elementos gráficos, ≥ 3:1). Al terminar, verde natural (4,0:1 sobre la pista).
- **Cuándo usar / qué NO hace:** Solo en la preparación del producto (3 minutos). No es una cuenta atrás de concursos ni de promociones. Sonido o vibración al terminar solo si el usuario lo activa.
