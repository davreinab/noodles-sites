### Contest hero   ⚙️ synced: 2026-10-23T09:22:57Z

<!-- ⚙️ GENERATED:start:contest-hero -->
- **Figma:** `313:866` · página «Pattern / Detail pages» · COMPONENT_SET · 2 variantes · última sync 2026-10-23T09:22:57Z
- **Descripción (Figma):** Contest hero: cabecera de la página de concurso (wireframe 330:6557 desktop y 361:8516 móvil). Fondo surface/brand (amarillo). Imagen ancha radius lg (media), Badge Natural de estado con punto («Live now · Ends 30 Sept 2026»; variante Closed pendiente: «Closed · Ended …»), h1 «Slurp & Win», texto body-l, botón Primary «Enter now» (ancla al formulario) y link «Read the rules»; a la derecha caja «How to participate» con resumen de una línea (móvil: debajo). Clase CSS: .contest-hero. Desktop 1440 / Móvil 375. ⬜ TODO GB Foods/agencia: imagen real, nombre y fechas definitivos, mecánica de resultado inmediato.
- **Anatomía:** `Badge` → Type=Natural, `Button` → Hierarchy=Primary, Size=M, State=Default, `icon-leading` → Icon / arrow-right, `icon-trailing` → Icon / arrow-right, `Link` → Type=Inline, Surface=Light, State=Default, `icon-trailing` → Icon / arrow-right
- **API:** `breakpoint`: Desktop, Mobile (por defecto Desktop)
- **Nombres en Figma:** `breakpoint` ← `Breakpoint`
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `badge/natural/bg`, `badge/natural/text`, `border/width/thick`, `button/primary/bg`, `button/primary/border`, `button/primary/text`, `color/surface/brand`, `color/surface/card`, `color/text/default`, `color/text/secondary`, `contest-card/media-bg`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/body-m`, `font/line-height/desktop/body-s`, `font/line-height/desktop/h1`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/line-height/mobile/label`, `font/size/desktop/body-l`, `font/size/desktop/body-m`, `font/size/desktop/body-s`, `font/size/desktop/h1`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/size/mobile/label`, `font/style/body`, `font/style/display`, `icon/size/sm`, `layout/margin`, `link/default`, `radius/lg`, `radius/md`, `radius/pill`, `space/16`, `space/24`, `space/4`, `space/64`, `space/8`
- **Text styles:** `Mobile/label`, `Desktop/h1`, `Desktop/body-l`, `Desktop/label`, `Desktop/body-m`, `Desktop/h3`, `Desktop/body-s`
<!-- ⚙️ GENERATED:end:contest-hero -->

- **Propósito:** Cabecera de la página de concurso sobre amarillo de marca: imagen ancha, Badge de estado («Live now · Ends 30 Sept 2026» o «Closed · Ended …»), título (h1), texto, «Enter now» (ancla al formulario, `#join`) y «Read the rules». A la derecha, la caja «How to participate» con un resumen de una línea.
- **Ejemplo de código:** Concurso en curso.
  ```html
  <section data-ds="contest-hero" class="section contest-hero" aria-labelledby="ch-title">
  <div class="section__inner">
  <figure class="contest-hero__media"><img class="contest-hero__image" src="../assets/images/placeholder.svg" alt=""></figure>
  <div class="contest-hero__grid">
  <div class="contest-hero__content">
  <span class="badge badge--natural">Live now · Ends 30 Sept 2026</span>
  <h1 class="contest-hero__title" id="ch-title">Slurp &amp; Win</h1>
  <p class="contest-hero__lead">Buy, keep your receipt, and you could take home festival trips, kitchen gear and more.</p>
  <div class="contest-hero__actions">
  <a class="button button--l" href="#join">Enter now</a>
  <a class="link" href="/contests/slurp-and-win/rules">Read the rules</a>
  </div>
  </div>
  <aside class="contest-hero__how" aria-labelledby="ch-how">
  <h2 class="contest-hero__how-title" id="ch-how">How to participate</h2>
  <p class="contest-hero__how-text">Buy a participating pack, keep your receipt, and submit it in the form below before the deadline.</p>
  </aside>
  </div>
  </div>
  </section>
  ```
  Closed: el Badge pasa a `badge badge--neutral` con «Closed · Ended 30 Sept 2026»; el botón «Enter now» se quita (no hay participación) y queda «Read the rules».
- **Accesibilidad (rol, nombre, estados y teclado):** Un solo h1 (el nombre del concurso); la caja es un `aside` con su h2. La imagen es decorativa en el ejemplo (`alt` vacío): si lleva el premio principal, su `alt` lo describe. El estado se dice con texto en el Badge, no con el color. «Enter now» es un enlace de ancla a `#join`: el destino (el formulario) debe llevar `tabindex="-1"` para que el foco pase a él y no quede en el botón. Contraste: texto tinta sobre amarillo de marca (más de 12:1). El gris secundario no se usa sobre amarillo (3,85:1, no pasa AA).
- **Cuándo usar / qué NO hace:** Solo en la cabecera de la página de un concurso. No es el hero de la Home (eso es Hero, con slider) ni de la biblioteca (Library hero). La mecánica y el límite de participaciones no se muestran aquí (⬜ TODO). El texto de estado, el resumen y las fechas son ⬜ TODO: los confirma GB Foods y la agencia.
