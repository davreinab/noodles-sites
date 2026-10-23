### Contest prizes   ⚙️ synced: 2026-10-23T09:22:57Z

<!-- ⚙️ GENERATED:start:contest-prizes -->
- **Figma:** `313:925` · página «Pattern / Detail pages» · COMPONENT_SET · 2 variantes · última sync 2026-10-23T09:22:57Z
- **Descripción (Figma):** Contest prizes: bloque de premios de la página de concurso (wireframe 330:6587 desktop, 361:8675 móvil). Fondo surface/page (crema). h2 «What's up for prizes», subtítulo y 4 Prize card (Variant=Grand para el gran premio, Default para el resto). Desktop: fila de 4. Móvil: carrusel horizontal con recorte (clipsContent) como los anillos de nutrición. Clase CSS: .contest-prizes. ⬜ TODO GB Foods/agencia: premios, niveles y descripciones reales; imágenes de los premios.
- **Anatomía:** `Prize card` → Variant=Grand, `Prize card` → Variant=Default, `Prize card` → Variant=Default, `Prize card` → Variant=Default
- **API:** `breakpoint`: Desktop, Mobile (por defecto Desktop)
- **Nombres en Figma:** `breakpoint` ← `Breakpoint`
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `color/border/default`, `color/surface/card`, `color/surface/inverse`, `color/surface/page`, `color/text/brand-on-inverse`, `color/text/default`, `color/text/on-inverse`, `color/text/secondary`, `contest-card/media-bg`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/desktop/h2`, `font/line-height/desktop/h3`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/desktop/h2`, `font/size/desktop/h3`, `font/style/body`, `font/style/display`, `layout/margin`, `radius/md`, `space/24`, `space/64`, `space/8`
- **Text styles:** `Desktop/h2`, `Desktop/body-m`, `Desktop/caption`, `Desktop/h3`
<!-- ⚙️ GENERATED:end:contest-prizes -->

- **Propósito:** Premios del concurso: título «What's up for prizes», entradilla y cuatro Prize card (un gran premio en Grand y tres en Default). Fondo crema.
- **Ejemplo de código:** Dos de los cuatro premios; la lista va completa con cuatro `li`.
  ```html
  <section data-ds="contest-prizes" class="section contest-prizes" aria-labelledby="cp-title">
  <div class="section__inner">
  <div class="section__header">
  <h2 class="section__title" id="cp-title">What's up for prizes</h2>
  <p class="section__lead">Four prize tiers, drawn weekly and at the grand final — every valid entry counts.</p>
  </div>
  <ul class="contest-prizes__list" tabindex="0" aria-label="Prizes">
  <li><article class="prize-card prize-card--grand">
  <div class="prize-card__media"><img src="../assets/images/placeholder.svg" alt=""></div>
  <div class="prize-card__body"><p class="prize-card__level">Grand prize</p><h3 class="prize-card__title">Festival weekend for two</h3><p class="prize-card__text">Two festival weekend passes, travel budget and backstage access to this year's festival partner.</p></div>
  </article></li>
  <li><article class="prize-card">
  <div class="prize-card__media"><img src="../assets/images/placeholder.svg" alt=""></div>
  <div class="prize-card__body"><p class="prize-card__level">Weekly prize · x50</p><h3 class="prize-card__title">Weekly runner-up boxes</h3><p class="prize-card__text">50 snack boxes given away every week for the length of the contest.</p></div>
  </article></li>
  </ul>
  </div>
  </section>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** La lista tiene nombre («Prizes») y cada premio es un `article` con su `h3`. En móvil es un carrusel horizontal: la lista es enfocable (`tabindex="0"`) y se desplaza con las flechas del teclado; el contorno de foco es el de la lista. Las tarjetas no son controles. Los niveles se dicen con texto. Contraste: como en Prize card (Grand sobre tinta; Default sobre blanco). En escritorio la lista no se desplaza, pero el `tabindex` no molesta.
- **Cuándo usar / qué NO hace:** Solo en la página de concurso, después de la cabecera. Cuatro niveles como máximo: el wireframe los dibuja así. Los premios, niveles, cantidades y descripciones son ⬜ TODO: GB Foods y la agencia los confirman (son condiciones del concurso). No muestra la mecánica del sorteo.
