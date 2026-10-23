### FAQ list   ⚙️ synced: 2026-10-23T09:22:57Z

<!-- ⚙️ GENERATED:start:faq-list -->
- **Figma:** `317:3438` · página «Pattern / Global» · COMPONENT_SET · 6 variantes · última sync 2026-10-23T09:22:57Z
- **Descripción (Figma):** FAQ list: lista de preguntas frecuentes con Accordion item (wireframe 428:10606 desktop, 428:12306 móvil; resultados 428:10962 / 501:14324; sin resultados 495:14043 / 428:12490). Columna de lectura de 808 centrada en desktop (1 columna en móvil). State=Default: 13 preguntas, solo una abierta a la vez (Accordion Expanded=True en la segunda). State=Results: caption «3 results for "Yatekomo"» y 3 preguntas. State=Empty: Empty state (219:1663) con «We couldn't find any results for your search» y «Try with a different word or topic», después «Or maybe you're interested in these other questions:» y 3 preguntas sugeridas. Clase CSS: .faq-list. Breakpoint Desktop 1440 / Móvil 375. ⬜ TODO GB Foods: respuestas definitivas (solo hay una respuesta en el wireframe) y preguntas definitivas.
- **Anatomía:** `Accordion item` → Expanded=False, State=Default, `icon-collapsed` → Icon / plus, `Accordion item` → Expanded=True, State=Default, `icon-expanded` → Icon / minus, `Accordion item` → Expanded=False, State=Default, `icon-collapsed` → Icon / plus, `Accordion item` → Expanded=False, State=Default, `icon-collapsed` → Icon / plus, `Accordion item` → Expanded=False, State=Default, `icon-collapsed` → Icon / plus, `Accordion item` → Expanded=False, State=Default, `icon-collapsed` → Icon / plus, `Accordion item` → Expanded=False, State=Default, `icon-collapsed` → Icon / plus, `Accordion item` → Expanded=False, State=Default, `icon-collapsed` → Icon / plus, `Accordion item` → Expanded=False, State=Default, `icon-collapsed` → Icon / plus, `Accordion item` → Expanded=False, State=Default, `icon-collapsed` → Icon / plus, `Accordion item` → Expanded=False, State=Default, `icon-collapsed` → Icon / plus, `Accordion item` → Expanded=False, State=Default, `icon-collapsed` → Icon / plus, `Accordion item` → Expanded=False, State=Default, `icon-collapsed` → Icon / plus
- **API:** `results` (boolean, por defecto false) · `empty` (boolean, por defecto false) · `breakpoint`: Desktop, Mobile (por defecto Desktop)
- **Nombres en Figma:** `results` ← `State=Results`, `empty` ← `State=Empty`, `breakpoint` ← `Breakpoint`
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `accordion/answer`, `accordion/bg`, `accordion/border`, `accordion/icon`, `accordion/question`, `border/width/thin`, `font/family/body`, `font/line-height/desktop/body-l`, `font/line-height/desktop/body-m`, `font/size/desktop/body-l`, `font/size/desktop/body-m`, `font/style/body`, `icon/size/md`, `layout/margin`, `radius/md`, `space/16`, `space/24`, `space/32`, `space/64`
- **Text styles:** `Desktop/body-l`, `Desktop/body-m`
<!-- ⚙️ GENERATED:end:faq-list -->

- **Propósito:** Lista de preguntas frecuentes de la página FAQ, en una columna de lectura centrada (`--layout-reading`, 720 px) con Accordion item. Tres estados: Default (la lista completa, de 6 a 11 preguntas), Results (la lista filtrada por la búsqueda, con el recuento «3 results for "Yatekomo"») y Empty (sin resultados: Empty state, la frase «Or maybe you're interested in these other questions:» y tres preguntas sugeridas). Va debajo de Library head con `library-head--center` y `library-head--no-filters`.
- **Variantes:** Default · Results · Empty. Breakpoint Desktop y Mobile: en móvil la misma columna ocupa todo el ancho del margen (16 px); no cambia la estructura.
- **Ejemplo de código:** Página de preguntas frecuentes completa (cabecera y lista). El contenedor `section` lleva `.faq` porque es el fondo blanco ya existente del patrón FAQ (la cabecera va en crema y no pueden ir dos secciones crema seguidas). Las respuestas del ejemplo son de muestra en inglés; ⬜ TODO: las respuestas reales las aporta GB Foods.
  ```html
  <section data-ds="library-head" class="section library-head library-head--center library-head--no-filters" aria-labelledby="faq-title">
  <div class="library-head__inner">
  <div class="library-head__intro">
  <h1 class="page-title" id="faq-title">Frequently Asked Questions</h1>
  <p class="library-head__lead">These are the questions we're asked most often, so you won't be left wondering</p>
  </div>
  <form class="search-field library-head__search" role="search" action="/faq">
  <span class="icon icon-search" aria-hidden="true"></span>
  <label class="visually-hidden" for="faq-q">Search for questions about our products</label>
  <input class="search-field__input" id="faq-q" name="q" type="search" placeholder="Search for questions about our products">
  </form>
  </div>
  </section>
  <section class="section faq">
  <div data-ds="faq-list" class="faq-list">
  <p class="faq-list__status visually-hidden" role="status"></p>
  <ul class="faq-list__items">
  <li><div class="accordion-item">
  <h3 class="accordion-item__heading"><button class="accordion-item__button" type="button" id="faq-q1-btn" aria-expanded="true" aria-controls="faq-q1">How is it prepared?<span class="icon icon-plus" aria-hidden="true"></span></button></h3>
  <div class="accordion-item__panel" id="faq-q1" role="region" aria-labelledby="faq-q1-btn">Full preparation instructions are printed on the pack. In general, the noodles only need a few minutes in hot water.</div>
  </div></li>
  <li><div class="accordion-item">
  <h3 class="accordion-item__heading"><button class="accordion-item__button" type="button" id="faq-q2-btn" aria-expanded="false" aria-controls="faq-q2">Has the taste of the product changed?<span class="icon icon-plus" aria-hidden="true"></span></button></h3>
  <div class="accordion-item__panel" id="faq-q2" role="region" aria-labelledby="faq-q2-btn" hidden>We review our recipes from time to time. If a change affects the taste, we will say so on the pack.</div>
  </div></li>
  <li><div class="accordion-item">
  <h3 class="accordion-item__heading"><button class="accordion-item__button" type="button" id="faq-q3-btn" aria-expanded="false" aria-controls="faq-q3">Where can I find the noodles?<span class="icon icon-plus" aria-hidden="true"></span></button></h3>
  <div class="accordion-item__panel" id="faq-q3" role="region" aria-labelledby="faq-q3-btn" hidden>Our products are sold in supermarkets and selected stores. Use the Where to buy section to find a shop near you.</div>
  </div></li>
  </ul>
  </div>
  </section>
  ```
  Results: la misma lista con el recuento visible. Se quita `visually-hidden` del `p` de estado y se escribe el texto; el resto no cambia.
  ```html
  <div data-ds="faq-list" class="faq-list">
  <p class="faq-list__status" role="status">3 results for "Yatekomo"</p>
  <ul class="faq-list__items">
  <li><div class="accordion-item">
  <h3 class="accordion-item__heading"><button class="accordion-item__button" type="button" id="faq-r1-btn" aria-expanded="false" aria-controls="faq-r1">Has the taste of the product changed?<span class="icon icon-plus" aria-hidden="true"></span></button></h3>
  <div class="accordion-item__panel" id="faq-r1" role="region" aria-labelledby="faq-r1-btn" hidden>We review our recipes from time to time. If a change affects the taste, we will say so on the pack.</div>
  </div></li>
  <li><div class="accordion-item">
  <h3 class="accordion-item__heading"><button class="accordion-item__button" type="button" id="faq-r2-btn" aria-expanded="false" aria-controls="faq-r2">Does Yatekomo contain MSG (glutamate) or flavor enhancers?<span class="icon icon-plus" aria-hidden="true"></span></button></h3>
  <div class="accordion-item__panel" id="faq-r2" role="region" aria-labelledby="faq-r2-btn" hidden>The full ingredient list is printed on each pack. Check it for the most accurate information about additives.</div>
  </div></li>
  <li><div class="accordion-item">
  <h3 class="accordion-item__heading"><button class="accordion-item__button" type="button" id="faq-r3-btn" aria-expanded="false" aria-controls="faq-r3">Is Yatekomo suitable for people with celiac disease or gluten intolerance?<span class="icon icon-plus" aria-hidden="true"></span></button></h3>
  <div class="accordion-item__panel" id="faq-r3" role="region" aria-labelledby="faq-r3-btn" hidden>Not all of our products are gluten-free. Check the allergen information on the pack before you buy.</div>
  </div></li>
  </ul>
  </div>
  ```
  Empty: el Empty state encima; la región de estado lleva el resultado (oculta a la vista, porque el título ya lo dice) y debajo, las sugerencias con su rótulo. Las sugerencias son preguntas de la lista completa.
  ```html
  <div data-ds="faq-list" class="faq-list faq-list--empty">
  <p class="faq-list__status visually-hidden" role="status">0 results for "pizza"</p>
  <div data-ds="empty-state" class="empty-state">
  <h2 class="empty-state__title">We couldn't find any results for your search</h2>
  <p class="empty-state__text">Try with a different word or topic</p>
  </div>
  <p class="faq-list__suggest" id="faq-sug">Or maybe you're interested in these other questions:</p>
  <ul class="faq-list__items" aria-labelledby="faq-sug">
  <li><div class="accordion-item">
  <h3 class="accordion-item__heading"><button class="accordion-item__button" type="button" id="faq-s1-btn" aria-expanded="false" aria-controls="faq-s1">Has the taste of the product changed?<span class="icon icon-plus" aria-hidden="true"></span></button></h3>
  <div class="accordion-item__panel" id="faq-s1" role="region" aria-labelledby="faq-s1-btn" hidden>We review our recipes from time to time. If a change affects the taste, we will say so on the pack.</div>
  </div></li>
  <li><div class="accordion-item">
  <h3 class="accordion-item__heading"><button class="accordion-item__button" type="button" id="faq-s2-btn" aria-expanded="false" aria-controls="faq-s2">Does Yatekomo contain MSG (glutamate) or flavor enhancers?<span class="icon icon-plus" aria-hidden="true"></span></button></h3>
  <div class="accordion-item__panel" id="faq-s2" role="region" aria-labelledby="faq-s2-btn" hidden>The full ingredient list is printed on each pack. Check it for the most accurate information about additives.</div>
  </div></li>
  <li><div class="accordion-item">
  <h3 class="accordion-item__heading"><button class="accordion-item__button" type="button" id="faq-s3-btn" aria-expanded="false" aria-controls="faq-s3">Is Yatekomo suitable for people with celiac disease or gluten intolerance?<span class="icon icon-plus" aria-hidden="true"></span></button></h3>
  <div class="accordion-item__panel" id="faq-s3" role="region" aria-labelledby="faq-s3-btn" hidden>Not all of our products are gluten-free. Check the allergen information on the pack before you buy.</div>
  </div></li>
  </ul>
  </div>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** La lista es un `ul` con un `li` por pregunta, y cada pregunta es un Accordion item (encabezado `h3` con `button` y `aria-expanded`; respuesta en región). Una sola respuesta abierta a la vez: al abrir una, el script de la página cierra la anterior y actualiza su `aria-expanded` y su `hidden`. El script de la maqueta (`UI/home.html`) lo hace para todos los `.accordion-item__button` de la página; en producción, la lista debe llevar el mismo comportamiento. El recuento y el estado vacío van en `p role="status"` (región viva, «polite»): cuando cambia el filtro, el lector anuncia «3 results for "Yatekomo"» o «0 results…» sin mover el foco. En Default la región existe y va oculta con `visually-hidden`, no con `display: none`, para que siga viva. El título del Empty state es un `h2` y las sugerencias se nombran con `aria-labelledby` en su `ul`. Teclado: Tab recorre la búsqueda y después las preguntas en orden; Enter o Espacio abren y cierran; no hay foco en la región de estado. Contraste: el recuento y el rótulo, gris cálido (`text-secondary`) sobre blanco 5,9:1 y sobre crema 5,4:1; las preguntas y respuestas, en tinta (18,7:1 sobre blanco).
- **Cuándo usar / qué NO hace:** Solo en la página de preguntas frecuentes. No es un buscador (la búsqueda es Library head) ni el FAQ de la Home (ese es el patrón `faq`, con su propio título y «Still curious?»). No filtra por sí mismo: el script de la página recibe el texto y decide la lista. El ancho es `--layout-reading` (720 px) y no los 808 px del wireframe: no existe token de 808 y la columna de lectura del DS es 720 (`patterns.md § Contenedores y anchos`). Textos: las preguntas son las del wireframe; **todas las respuestas son ⬜ TODO** (las confirma GB Foods). El número de preguntas por defecto (6–11) y la lista de sugerencias del Empty state (tres preguntas) son ⬜ TODO: la regla de negocio es que las sugerencias sean preguntas reales de la lista, no inventadas.
