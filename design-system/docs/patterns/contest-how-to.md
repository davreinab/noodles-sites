### Contest how-to   ⚙️ synced: 2026-10-23T09:22:57Z

<!-- ⚙️ GENERATED:start:contest-how-to -->
- **Figma:** `313:2905` · página «Pattern / Detail pages» · COMPONENT_SET · 2 variantes · última sync 2026-10-23T09:22:57Z
- **Descripción (Figma):** Contest how-to: cómo participar y condiciones de ganar (wireframe 330:6619 desktop, 361:8675 móvil; ver también 330:6619 y 361:8675). Fondo surface/card (blanco). h2 «Easy to participate, easy to win» con subtítulo; columna «Steps» con 4 Pillar item Tone=Ink (el paso 3 lleva Link «Submit it now →»); columna «Winning conditions» con Contest conditions. Móvil: columnas apiladas. Clase CSS: .contest-howto. ⬜ TODO GB Foods: texto de los pasos, fechas del sorteo y lista de condiciones reales; la mecánica de resultado inmediato sigue pendiente de confirmar con GB Foods y la agencia.
- **Anatomía:** `Pillar item` → Tone=Ink, `Pillar item` → Tone=Ink, `Pillar item` → Tone=Ink, `Link` → Type=Inline, Surface=Light, State=Default, `icon-trailing` → Icon / arrow-right, `Pillar item` → Tone=Ink, `Contest conditions` → Contest conditions, `Icon / calendar-clock` → Icon / calendar-clock, `Icon / trophy` → Icon / trophy
- **API:** `breakpoint`: Desktop, Mobile (por defecto Desktop)
- **Nombres en Figma:** `breakpoint` ← `Breakpoint`
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown · capas sin swap: Icon / calendar-clock, Icon / trophy
- **Tokens que consume:** `color/surface/card`, `color/surface/inverse`, `color/text/default`, `color/text/on-inverse`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-m`, `font/line-height/desktop/body-s`, `font/line-height/desktop/h2`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/size/desktop/body-m`, `font/size/desktop/body-s`, `font/size/desktop/h2`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/color/inverse`, `icon/size/md`, `icon/size/sm`, `layout/margin`, `link/default`, `link/inverse`, `radius/md`, `radius/pill`, `space/16`, `space/24`, `space/32`, `space/64`, `space/8`
- **Text styles:** `Desktop/h2`, `Desktop/body-m`, `Desktop/h3`, `Desktop/label`, `Desktop/body-s`
<!-- ⚙️ GENERATED:end:contest-how-to -->

- **Propósito:** Cómo participar y cómo se gana: título «Easy to participate, easy to win» y entradilla; dos columnas: los pasos (Pillar item en variante Ink, con «Submit it now →» en el paso 3) y las condiciones del concurso (Contest conditions). Fondo blanco.
- **Ejemplo de código:** Textos de muestra en inglés; ⬜ TODO: los pasos y la lista de condiciones reales los aporta GB Foods.
  ```html
  <section data-ds="contest-howto" class="section contest-howto" aria-labelledby="ch2-title">
  <div class="section__inner">
  <div class="section__header">
  <h2 class="section__title" id="ch2-title">Easy to participate, easy to win</h2>
  <p class="section__lead">No purchase-free route needed here — if you already bought the product, you're most of the way there.</p>
  </div>
  <div class="contest-howto__grid">
  <div class="contest-howto__column">
  <h3 class="contest-howto__heading" id="ch2-steps">Steps</h3>
  <ol class="contest-howto__steps" aria-labelledby="ch2-steps">
  <li data-ds="pillar-item" class="pillar-item pillar-item--ink"><span class="pillar-item__number" aria-hidden="true">1</span><p class="pillar-item__title">Buy a participating pack</p><p class="pillar-item__text">Any GB Foods Noodlebox cup or bag purchased between 1 August and 30 September 2026 qualifies.</p></li>
  <li data-ds="pillar-item" class="pillar-item pillar-item--ink"><span class="pillar-item__number" aria-hidden="true">2</span><p class="pillar-item__title">Keep your receipt</p><p class="pillar-item__text">You'll need the purchase date, time and receipt number to complete the form below.</p></li>
  <li data-ds="pillar-item" class="pillar-item pillar-item--ink"><span class="pillar-item__number" aria-hidden="true">3</span><p class="pillar-item__title">Submit your entry</p><p class="pillar-item__text">Fill in the participation form with your details and a photo of the receipt.</p><p class="pillar-item__action"><a class="link" href="#join">Submit it now →</a></p></li>
  <li data-ds="pillar-item" class="pillar-item pillar-item--ink"><span class="pillar-item__number" aria-hidden="true">4</span><p class="pillar-item__title">Wait for the draw</p><p class="pillar-item__text">Weekly winners are drawn every Monday, the grand prize is drawn after the contest closes.</p></li>
  </ol>
  </div>
  <div class="contest-howto__column contest-howto__column--conditions">
  <h3 class="contest-howto__heading" id="ch2-conditions">Winning conditions</h3>
  <div data-ds="contest-conditions" class="contest-conditions">
  <ul class="contest-conditions__list">
  <li class="contest-conditions__item"><span class="icon icon-calendar-clock icon--inverse" aria-hidden="true"></span><span>Entries close: <strong>30 September 2026 at 23:59 CET</strong></span></li>
  <li class="contest-conditions__item"><span class="icon icon-trophy icon--inverse" aria-hidden="true"></span><span>Grand prize draw: <strong>7 October 2026</strong></span></li>
  </ul>
  <p class="contest-conditions__text">One entry per purchase. Proof of purchase is required.</p>
  <a class="link link--dark" href="/contests/slurp-and-win/rules">Read the full contest rules →</a>
  </div>
  </div>
  </div>
  </div>
  </section>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Cada columna tiene su h3 y los pasos van en `ol`: el orden de los pasos lo dice la lista. Los números van con `aria-hidden`. El enlace «Submit it now →» va a `#join` (el formulario, con `tabindex="-1"`). Teclado: Tab por el enlace del paso 3 y por el de las bases. Contraste: tinta sobre blanco; los círculos tinta con número crema (17:1). El orden en móvil es el mismo: primero los pasos y después las condiciones.
- **Cuándo usar / qué NO hace:** Solo en la página de concurso, entre premios y formulario. No es una lista de preparación (eso es Preparation con Step). Los textos de los pasos son ⬜ TODO: son reglas del concurso y los confirma GB Foods; el periodo de compra (1 agosto a 30 septiembre de 2026) también.
