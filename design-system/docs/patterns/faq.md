### FAQ   ⚙️ synced: 2026-10-08T11:10:38Z

<!-- ⚙️ GENERATED:start:faq -->
- **Figma:** `92:960` · página «Pattern / Home» · COMPONENT_SET · 2 variantes · última sync 2026-10-08T11:10:38Z
- **Descripción (Figma):** Bloque de FAQ (Home, Natural formula y página FAQS; wireframe UX): título (h2) + entradilla · lista de Accordion item (space/16; uno abierto a la vez) · «Still curious?» + Link «See all FAQS» a la página FAQS (desktop al pie de la columna del título; mobile debajo de la lista). En la página FAQS se repite por categorías sin el enlace. SEO/AEO: las respuestas están en el HTML y la página lleva datos estructurados FAQPage; las respuestas las valida GB Foods. Desktop: cabecera a la izquierda (400 px) y lista a la derecha; Mobile: apilado. Sin variables propias.
- **Anatomía:** `link` → Type=Standalone, Surface=Light, State=Default, `icon-trailing` → Icon / arrow-right, `accordion-item` → Expanded=False, State=Default, `icon-collapsed` → Icon / plus, `accordion-item` → Expanded=True, State=Default, `icon-expanded` → Icon / minus, `accordion-item` → Expanded=False, State=Default, `icon-collapsed` → Icon / plus, `accordion-item` → Expanded=False, State=Default, `icon-collapsed` → Icon / plus
- **Breakpoint:** Desktop, Mobile
- **Propiedades de componente:** `Breakpoint` (VARIANT, por defecto Desktop)
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `accordion/answer`, `accordion/bg`, `accordion/border`, `accordion/icon`, `accordion/question`, `border/width/thin`, `color/surface/page`, `color/text/default`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/body-m`, `font/line-height/desktop/h2`, `font/line-height/desktop/label`, `font/size/desktop/body-l`, `font/size/desktop/body-m`, `font/size/desktop/h2`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/md`, `icon/size/sm`, `layout/frame`, `layout/margin`, `layout/section-y`, `link/default`, `radius/md`, `space/16`, `space/24`, `space/64`, `space/8`
- **Text styles:** `Desktop/h2`, `Desktop/body-l`, `Desktop/body-m`, `Desktop/label`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `accordion/answer`, `accordion/bg`, `accordion/border`, `accordion/icon`, `accordion/question`, `color/surface/page`, `color/text/default`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/body-m`, `font/line-height/desktop/h2`, `font/line-height/desktop/label`, `font/size/desktop/body-l`, `font/size/desktop/body-m`, `font/size/desktop/h2`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `link/default`
<!-- ⚙️ GENERATED:end:faq -->

- **Propósito:** Bloque de preguntas frecuentes (wireframe UX): título, entradilla, preguntas desplegables (una abierta a la vez) y «Still curious? See all FAQS».
- **Ejemplo de código:**
  ```html
  <section class="section faq" aria-labelledby="faq-title">
  <div class="section__inner">
  <div class="faq__grid">
  <div class="section__header"><h2 class="section__title" id="faq-title">Are you wondering how, too? We’ll tell you</h2><p class="section__lead">These are the questions we're asked most often, so you won't be left wondering</p></div>
  <ul class="faq__list"><li><div class="accordion-item"><h3 class="accordion-item__heading"><button class="accordion-item__button" type="button" aria-expanded="false" aria-controls="q1">How is it prepared?<span class="icon icon-plus" aria-hidden="true"></span></button></h3><div class="accordion-item__panel" id="q1" hidden>Respuesta.</div></div></li></ul>
  <p class="faq__more">Still curious? <a class="link link--standalone" href="/faqs">See all FAQS <span class="icon icon-arrow-right" aria-hidden="true"></span></a></p>
  </div>
  </div>
  </section>
  ```
- **Accesibilidad (pares AA verificados):** Título tinta sobre crema 17,2:1; entradilla y «Still curious?» secundarios 7,9:1. Las respuestas están en el HTML (SEO/AEO) y la página lleva datos estructurados FAQPage. Cada pregunta es un botón con `aria-expanded`.
- **Cuándo usar / qué NO hace:** En la Home, la Natural formula page y la página FAQS (por categorías, sin «See all FAQS»). Las respuestas las valida GB Foods.
