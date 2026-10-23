### Contest library   ⚙️ synced: 2026-10-23T09:22:57Z

<!-- ⚙️ GENERATED:start:contest-library -->
- **Figma:** `312:3141` · página «Pattern / Libraries» · COMPONENT_SET · 2 variantes · última sync 2026-10-23T09:22:57Z
- **Descripción (Figma):** Contest library: biblioteca de concursos (wireframe 190:3727 desktop, 273:7157 móvil). Library head (Search y Filters desactivados; título «Contests & promotions», subtítulo «Enter our contests and win, don't miss your chance!»). h2 «Active contests» con fila de Contest card Status=Active; h2 «Closed contests» con subtítulo y rejilla de Contest card Status=Closed (4 columnas en desktop, 1 en móvil); botón secondary «Load more». Fondo surface/page. Clase CSS: .contest-library. Desktop 1440 / Móvil 375; card 296. ⬜ TODO GB Foods/agencia: concursos reales, tamaño de tanda de «Load more» y mecánica de límite de participaciones pendiente de confirmar.
- **Anatomía:** `Library head` → State=Default, Breakpoint=Desktop, Align=Left, `Search field` → State=Default, `icon-search` → Icon / search, `icon-clear` → Icon / close, `Chip` → Size=M, State=Selected, `icon-leading` → Icon / check, `Chip` → Size=M, State=Default, `icon-leading` → Icon / check, `Chip` → Size=M, State=Default, `icon-leading` → Icon / check, `Chip` → Size=M, State=Default, `icon-leading` → Icon / check, `Chip` → Size=M, State=Default, `icon-leading` → Icon / check, `Chip` → Size=M, State=Default, `icon-leading` → Icon / check, `Chip` → Size=M, State=Default, `icon-leading` → Icon / check, `Contest card` → Status=Active, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Contest card` → Status=Closed, `Badge` → Type=Neutral, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Contest card` → Status=Closed, `Badge` → Type=Neutral, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Contest card` → Status=Closed, `Badge` → Type=Neutral, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Contest card` → Status=Closed, `Badge` → Type=Neutral, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Contest card` → Status=Closed, `Badge` → Type=Neutral, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Contest card` → Status=Closed, `Badge` → Type=Neutral, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Contest card` → Status=Closed, `Badge` → Type=Neutral, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Contest card` → Status=Closed, `Badge` → Type=Neutral, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Button` → Hierarchy=Secondary, Size=M, State=Default, `icon-leading` → Icon / arrow-right, `icon-trailing` → Icon / arrow-right
- **API:** `breakpoint`: Desktop, Mobile (por defecto Desktop)
- **Nombres en Figma:** `breakpoint` ← `Breakpoint`
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `badge/neutral/bg`, `badge/neutral/text`, `border/width/thick`, `border/width/thin`, `button/secondary/border`, `button/secondary/text`, `chip/bg`, `chip/bg-selected`, `chip/border`, `chip/height/m`, `chip/height/s`, `chip/text`, `chip/text-selected`, `color/effect/shadow-ink`, `color/surface/page`, `color/text/default`, `color/text/secondary`, `contest-card/bg`, `contest-card/border`, `contest-card/media-bg`, `contest-card/meta`, `contest-card/title`, `field/bg`, `field/border`, `field/icon`, `field/placeholder`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/body-m`, `font/line-height/desktop/body-s`, `font/line-height/desktop/caption`, `font/line-height/desktop/h1`, `font/line-height/desktop/h2`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/line-height/mobile/label`, `font/size/desktop/body-l`, `font/size/desktop/body-m`, `font/size/desktop/body-s`, `font/size/desktop/caption`, `font/size/desktop/h1`, `font/size/desktop/h2`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/size/mobile/label`, `font/style/body`, `font/style/display`, `icon/size/md`, `icon/size/sm`, `layout/margin`, `radius/md`, `radius/none`, `radius/pill`, `space/16`, `space/24`, `space/4`, `space/48`, `space/8`
- **Text styles:** `Desktop/h1`, `Desktop/body-l`, `Desktop/body-m`, `Desktop/body-s`, `Desktop/h2`, `Desktop/caption`, `Desktop/h3`, `Mobile/label`, `Desktop/label`
<!-- ⚙️ GENERATED:end:contest-library -->

- **Propósito:** Biblioteca de concursos: dos grupos, Active contests (concursos abiertos) y Closed contests (concursos terminados, con la entradilla «Take another look at everything we've given away» y «Load more»). Cada grupo es una rejilla de Contest card. Va debajo de Library head sin filtros.
- **Ejemplo de código:** Un concurso activo y un cerrado; el resto de tarjetas se repiten igual.
  ```html
  <section data-ds="contest-library" class="section contest-library" aria-label="Contests">
  <div class="section__inner contest-library__inner">
  <div class="contest-library__group" aria-labelledby="cl-active">
  <div class="section__header"><h2 class="section__title" id="cl-active">Active contests</h2></div>
  <ul class="contest-library__grid">
  <li><article class="contest-card">
  <div class="contest-card__media"><img src="../assets/images/placeholder.svg" alt=""></div>
  <div class="contest-card__body">
  <p class="contest-card__dates" id="cl-a1-dates">Available until 20/9/2026</p>
  <h3 class="contest-card__title"><a class="contest-card__link" href="/contests/slurp-and-win" aria-describedby="cl-a1-dates">Slurp &amp; Win</a></h3>
  <ul class="contest-card__prizes" aria-label="Prizes"><li><span class="chip">T-shirts</span></li><li><span class="chip">Balls</span></li><li><span class="chip">Experience</span></li></ul>
  </div>
  </article></li>
  </ul>
  </div>
  <div class="contest-library__group" aria-labelledby="cl-closed">
  <div class="section__header">
  <h2 class="section__title" id="cl-closed">Closed contests</h2>
  <p class="section__lead">Take another look at everything we've given away</p>
  </div>
  <ul class="contest-library__grid">
  <li><article class="contest-card">
  <div class="contest-card__media"><span class="badge badge--neutral">Closed</span><img src="../assets/images/placeholder.svg" alt=""></div>
  <div class="contest-card__body">
  <p class="contest-card__dates" id="cl-c1-dates">Ended on 20/9/2026</p>
  <h3 class="contest-card__title"><a class="contest-card__link" href="/contests/old-contest" aria-describedby="cl-c1-dates">Old contest</a></h3>
  <ul class="contest-card__prizes" aria-label="Prizes"><li><span class="chip">Balls</span></li></ul>
  </div>
  </article></li>
  </ul>
  <div class="contest-library__more"><button class="button button--secondary" type="button">Load more</button></div>
  </div>
  </div>
  </section>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Cada grupo es una región con nombre por su h2 (`aria-labelledby`). Las tarjetas van en `ul` y `li` y cada una es un `article` con su enlace. Teclado: Tab recorre los enlaces de los concursos en orden (Active, luego Closed) y después «Load more». Al pulsar «Load more» llegan más tarjetas: el foco se queda en el botón, que sigue disponible (⬜ decisión pendiente: si el botón desaparece al llegar al final, el foco debe pasar al primer concurso nuevo). El estado Closed se dice con el Badge y con «Ended on», no con el color. Contraste: sección blanca; la entradilla en gris cálido (5,4:1).
- **Cuándo usar / qué NO hace:** Solo en la página de concursos (Contests & promotions), con Library head sin filtros. Si no hay concursos activos, el grupo Active se oculta entero, sin mensaje (regla de composición de `patterns.md`); igual con Closed si está vacío. Fondo blanco: la cabecera va en crema y no pueden ir dos secciones crema seguidas (el maestro las dibuja juntas; ⬜ decidir con David). El tamaño de página de «Load more» y el orden de los cerrados son ⬜ TODO.
