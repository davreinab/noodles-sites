### Legal page   ⚙️ synced: 2026-10-23T09:22:57Z

<!-- ⚙️ GENERATED:start:legal-page -->
- **Figma:** `317:3602` · página «Pattern / Global» · COMPONENT_SET · 2 variantes · última sync 2026-10-23T09:22:57Z
- **Descripción (Figma):** Legal page: página de texto legal (wireframe 377:8301 desktop, 381:14542 móvil). Link «Back» con icono arrow-left, h1 «Yatekomo Privacy Policy», entradilla body-l, párrafo de introducción, 12 apartados numerados (h3 de apartado) con párrafos, tabla de conservación (Legal table, apartado 5) y «Last updated: July 2026» (caption). Columna de lectura de 800 (layout/reading) centrada en desktop; fondo surface/card. Solo los apartados 1 y 2 llevan texto real de la captura; el resto ⬜ TODO (texto legal de GB Foods). Clase CSS: .legal-page (basada en la página de contenido puro de la landing). Breakpoint Desktop 1440 / Móvil 375.
- **Anatomía:** `icon-leading` → Icon / arrow-left, `Link` → Type=Inline, Surface=Light, State=Default, `icon-trailing` → Icon / arrow-left, `Legal table` → Breakpoint=Desktop
- **API:** `breakpoint`: Desktop, Mobile (por defecto Desktop)
- **Nombres en Figma:** `breakpoint` ← `Breakpoint`
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown · capas sin swap: icon-leading
- **Tokens que consume:** `border/width/thin`, `color/border/default`, `color/border/subtle`, `color/surface/card`, `color/text/default`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/desktop/h1`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/size/desktop/body-l`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/desktop/h1`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/color/default`, `icon/size/md`, `icon/size/sm`, `layout/margin`, `link/default`, `space/16`, `space/64`, `space/8`
- **Text styles:** `Desktop/body-m`, `Desktop/h1`, `Desktop/body-l`, `Desktop/h3`, `Desktop/label`, `Desktop/caption`
<!-- ⚙️ GENERATED:end:legal-page -->

- **Propósito:** Página de texto legal (política de privacidad, aviso legal) en una columna de lectura centrada (`--layout-reading`, 720 px). Orden: enlace «Back» con flecha delante, h1 con el nombre del documento, entradilla (body-l), párrafo de introducción, apartados numerados (h2 «1. …», «2. …») con sus párrafos, listas y datos de contacto, tablas de conservación con Legal table, y la fecha «Last updated». Fondo blanco (surface/card).
- **Variantes:** una. Desktop y Mobile: la misma columna; en móvil el margen lateral es 16 px y los títulos bajan a su tamaño móvil.
- **Ejemplo de código:** Apartados 1 y 2 con el texto real de la captura; el 5 con la Legal table real; el resto con la misma estructura y el texto pendiente. Los apartados 3 y 6 del ejemplo llevan texto de muestra en inglés; ⬜ TODO: el texto legal real de los apartados 3, 4 y 6–12 lo aporta GB Foods.
  ```html
  <article data-ds="legal-page" class="legal-page">
  <div class="legal-page__inner">
  <a class="link legal-page__back" href="index.html"><span class="icon icon-arrow-left" aria-hidden="true"></span>Back</a>
  <h1 class="page-title">Yatekomo Privacy Policy</h1>
  <p class="legal-page__lead">At "Yatekomo" we place great importance on current regulations regarding privacy and data protection. In this sense, protecting the security, integrity and confidentiality of all users' information is very important to us, and therefore we want to act responsibly in this area.</p>
  <p class="legal-page__intro">This Privacy Policy (hereinafter, the "Privacy Policy") describes the type of personal information we collect, how we obtain it, how we share it, and the purposes for which we process it, as well as the means available to you as a user to control such use and exercise your rights.</p>
  <section class="legal-page__section">
  <h2 class="legal-page__heading">1. Scope of the Privacy Policy</h2>
  <p class="legal-page__text">This Privacy Policy applies to the personal data obtained by Yatekomo from our customers, suppliers, information requesters, job applicants and, where applicable, users of our Website or third parties with whom we interact.</p>
  </section>
  <section class="legal-page__section">
  <h2 class="legal-page__heading">2. Who is the Data Controller?</h2>
  <p class="legal-page__text">The Data Controller for your data is GALLINA BLANCA, S.A. Below are our contact details: company name: GALLINA BLANCA, S.A.; contact email: dataprivacy@thegbfoods.com.</p>
  </section>
  <section class="legal-page__section">
  <h2 class="legal-page__heading">3. What information do we collect and how do we collect it?</h2>
  <p class="legal-page__text">We collect the information you give us directly, for example when you subscribe to our newsletter or contact us through the website, as well as basic technical data about your visit.</p>
  </section>
  <section class="legal-page__section">
  <h2 class="legal-page__heading">5. How long do we keep your data?</h2>
  <table data-ds="legal-table" class="legal-table">
  <caption class="visually-hidden">Purposes and retention periods</caption>
  <thead>
  <tr><th scope="col">Purpose</th><th scope="col">Retention period</th></tr>
  </thead>
  <tbody>
  <tr>
  <td data-label="Purpose">(i) To learn about your browsing preferences on our Website in order to personalise and improve our products and your experience.</td>
  <td data-label="Retention period">As indicated in our Cookie Policy, up to a maximum of 2 years.</td>
  </tr>
  <tr>
  <td data-label="Purpose">(ii) To manage and process the response to your request for information sent through our Website's contact form.</td>
  <td data-label="Retention period">Until your query has been resolved, as well as the time necessary to comply with the corresponding legal obligations.</td>
  </tr>
  <tr>
  <td data-label="Purpose">(iii) To handle emails received at our corporate email addresses for the purpose of maintaining business relationships with entities, organisations or companies and with the people who work for or collaborate with them or with their legal representatives.</td>
  <td data-label="Retention period">For a reasonable period after your last interaction with us.</td>
  </tr>
  </tbody>
  </table>
  </section>
  <section class="legal-page__section">
  <h2 class="legal-page__heading">6. What legitimises us to process your personal data?</h2>
  <p class="legal-page__text">We process your data on the basis of your consent, the performance of any contract with you and our legitimate interest in answering your queries.</p>
  </section>
  <p class="legal-page__updated">Last updated: <time datetime="2026-07">July 2026</time></p>
  </div>
  </article>
  ```
  Los apartados 7 a 12 repiten la misma `section` con su h2 y un `p` ⬜ TODO. Las listas de un apartado van en `ul.legal-page__list` con su `li`.
- **Accesibilidad (rol, nombre, estados y teclado):** El `article` lleva un único `h1` (`page-title`); cada apartado es una `section` con su `h2`, y el número va en el texto del h2 para que se lea («1. Scope…»). Los apartados no llevan `aria-labelledby`: no son regiones de navegación y no se quiere llenar la página de landmarks. El enlace «Back» es un `a` con su texto visible; la flecha va delante con `aria-hidden`, así que se anuncia «Back». Teclado: Tab recorre el enlace «Back» y después los enlaces que haya en el texto legal; no hay controles propios. La fecha va en `time` con `datetime="2026-07"`. Contraste: texto en tinta sobre blanco (18,7:1); la fecha, gris cálido (5,9:1). Sin color como único indicador: los apartados se distinguen por su número y su título.
- **Cuándo usar / qué NO hace:** Para cualquier texto legal de la web (privacidad, aviso legal, condiciones de un concurso que sea un documento aparte). No es una página de producto ni de receta, no tiene cabecera de librería, no lleva buscador ni acordeón (para preguntas frecuentes, FAQ list). El link «Back» vuelve a la página desde la que se llega: ⬜ TODO el destino (se decide en la implementación). El texto legal completo es ⬜ TODO: lo aporta GB Foods; ninguno de los apartados sin captura se ha redactado en el DS.
