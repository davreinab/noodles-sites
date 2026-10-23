### Newsletter   ⚙️ synced: 2026-10-23T09:22:57Z

<!-- ⚙️ GENERATED:start:newsletter -->
- **Figma:** `312:3247` · página «Pattern / Libraries» · COMPONENT_SET · 2 variantes · última sync 2026-10-23T09:22:57Z
- **Descripción (Figma):** Newsletter: captación de email con redes sociales, sobre fondo surface/inverse (wireframe 190:3727 y 330:6557, pie de bloque). Title (TEXT): «Don't miss a thing» en la biblioteca y «Never miss the next contest» en la página de concurso. Texto de suscripción, «Our social media:» con 4 icon buttons inverse (TikTok, Instagram, X, YouTube), Input de email, texto legal de consentimiento (caption) y botón Subscribe (Hierarchy=Inverse). Clase CSS: .newsletter. Desktop 1440 / Móvil 375. ⬜ TODO GB Foods/agencia: texto legal de consentimiento definitivo y destinatario del alta.
- **Anatomía:** `icon-button TikTok` → Hierarchy=Inverse, Size=M, State=Default, `icon` → Icon / tiktok, `icon-button Instagram` → Hierarchy=Inverse, Size=M, State=Default, `icon` → Icon / instagram, `icon-button X` → Hierarchy=Inverse, Size=M, State=Default, `icon` → Icon / x, `icon-button YouTube` → Hierarchy=Inverse, Size=M, State=Default, `icon` → Icon / youtube, `Input` → State=Default, `icon-error` → Icon / circle-alert, `Button` → Hierarchy=Inverse, Size=M, State=Default, `icon-leading` → Icon / arrow-right, `icon-trailing` → Icon / arrow-right
- **API:** `title` (string, por defecto Don't miss a thing) · `breakpoint`: Desktop, Mobile (por defecto Desktop)
- **Nombres en Figma:** `title` ← `Title#312:0`, `breakpoint` ← `Breakpoint`
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `border/width/thick`, `border/width/thin`, `button/inverse/bg`, `button/inverse/border`, `button/inverse/text`, `color/surface/inverse`, `color/text/on-inverse`, `field/bg`, `field/border`, `field/error-text`, `field/helper`, `field/label`, `field/placeholder`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-m`, `font/line-height/desktop/body-s`, `font/line-height/desktop/caption`, `font/line-height/desktop/h2`, `font/line-height/desktop/label`, `font/size/desktop/body-m`, `font/size/desktop/body-s`, `font/size/desktop/caption`, `font/size/desktop/h2`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon-button/size/m`, `icon/color/default`, `icon/size/md`, `icon/size/sm`, `layout/margin`, `radius/pill`, `radius/sm`, `space/16`, `space/24`, `space/4`, `space/64`, `space/8`
- **Text styles:** `Desktop/h2`, `Desktop/body-m`, `Desktop/body-s`, `Desktop/label`, `Desktop/caption`
<!-- ⚙️ GENERATED:end:newsletter -->

- **Propósito:** Captación de la newsletter sobre tinta: título, texto, «Our social media:» con los iconos de redes, y a la derecha un campo de email con el texto de consentimiento y el botón «Subscribe». Se usa al final de las páginas de concurso y de la Contest library, para no encadenar secciones crema.
- **Ejemplo de código:** Versión de la página de concurso (título «Never miss the next contest»; en la biblioteca, «Don't miss a thing»). El texto legal del ejemplo es de muestra en inglés; ⬜ TODO: el texto de consentimiento definitivo y el destinatario del alta los aporta GB Foods y el equipo de datos.
  ```html
  <section data-ds="newsletter" class="section newsletter" aria-labelledby="nl-title">
  <div class="section__inner newsletter__grid">
  <div class="newsletter__content">
  <h2 class="newsletter__title" id="nl-title">Don't miss a thing</h2>
  <p class="newsletter__text">Subscribe to our newsletter and follow us to stay up to date on all the contests from the very start.</p>
  <div class="newsletter__social">
  <p class="newsletter__social-label" id="nl-social">Our social media:</p>
  <ul class="newsletter__social-list" aria-labelledby="nl-social">
  <li><a class="icon-button icon-button--inverse" href="https://www.tiktok.com/" aria-label="TikTok"><span class="icon icon-tiktok" aria-hidden="true"></span></a></li>
  <li><a class="icon-button icon-button--inverse" href="https://www.instagram.com/" aria-label="Instagram"><span class="icon icon-instagram" aria-hidden="true"></span></a></li>
  <li><a class="icon-button icon-button--inverse" href="https://x.com/" aria-label="X"><span class="icon icon-x" aria-hidden="true"></span></a></li>
  <li><a class="icon-button icon-button--inverse" href="https://www.youtube.com/" aria-label="YouTube"><span class="icon icon-youtube" aria-hidden="true"></span></a></li>
  </ul>
  </div>
  </div>
  <form class="newsletter__form" action="/newsletter" method="post">
  <div class="field">
  <label class="visually-hidden" for="nl-email">Email address</label>
  <input class="field__control" id="nl-email" name="email" type="email" autocomplete="email" placeholder="Enter your mail" required>
  </div>
  <p class="newsletter__legal" id="nl-legal">By subscribing to the newsletter, I agree to have my email address used to send me promotions and marketing content. You can withdraw your consent at any time with the unsubscribe link in each email.</p>
  <button class="button button--inverse" type="submit" aria-describedby="nl-legal">Subscribe</button>
  </form>
  </div>
  </section>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** La sección tiene nombre por su h2. El campo tiene etiqueta oculta («Email address») y `type="email"` con `autocomplete="email"`, para que el teclado y el navegador lo traten como email; el placeholder no sustituye a la etiqueta. El texto legal se enlaza al botón con `aria-describedby`, así el consentimiento se lee al llegar a «Subscribe». Cada icono de red es un enlace con nombre propio (`aria-label`) y el icono va oculto. Teclado: Tab por el campo, el botón y los iconos en orden. Contraste: textos crema sobre tinta (17:1); el botón es crema con texto tinta. El error de email, si lo hay, lo marca el patrón de Field (⬜ TODO: pendiente de su mensaje).
- **Cuándo usar / qué NO hace:** Como captación al final de una página o biblioteca de concursos, sobre tinta. No es el formulario de participación (eso es Contest form) ni un pie de página. El texto legal de consentimiento, las redes y los enlaces son ⬜ TODO: los confirma GB Foods y el equipo de datos (RGPD).
