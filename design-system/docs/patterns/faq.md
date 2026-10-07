### FAQ   ⚙️ synced: 2026-10-07T18:49:29Z

<!-- ⚙️ GENERATED:start:faq -->
- **Figma:** `92:960` · página «Pattern / FAQ» · COMPONENT_SET · 2 variantes · última sync 2026-10-07T18:49:29Z
- **Descripción (Figma):** Bloque de FAQ (Home, Natural formula con su FAQ propio, página FAQS indexada): título (h2) + entradilla + Link «Ver todas las preguntas» · lista de Accordion item (space/16 entre ítems; el primero puede ir abierto). En la página FAQS se repite por categorías sin el enlace. SEO/AEO: las respuestas están en el HTML y la página lleva datos estructurados FAQPage. Desktop: cabecera a la izquierda (400 px) y lista a la derecha; Mobile: apilado. Sin variables propias.
- **Anatomía:** `link` → Type=Standalone, Surface=Light, State=Default, `icon-trailing` → Icon / arrow-right, `accordion-item` → Expanded=True, State=Default, `icon-expanded` → Icon / minus, `accordion-item` → Expanded=False, State=Default, `icon-collapsed` → Icon / plus
- **Breakpoint:** Desktop, Mobile
- **Propiedades de componente:** `Breakpoint` (VARIANT, por defecto Desktop)
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `accordion/answer`, `accordion/bg`, `accordion/border`, `accordion/icon`, `accordion/question`, `border/width/thin`, `color/surface/page`, `color/text/default`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/body-m`, `font/line-height/desktop/h2`, `font/line-height/desktop/label`, `font/size/desktop/body-l`, `font/size/desktop/body-m`, `font/size/desktop/h2`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/md`, `icon/size/sm`, `layout/frame`, `layout/margin`, `layout/section-y`, `link/default`, `radius/md`, `space/16`, `space/24`, `space/64`, `space/8`
- **Text styles:** `Desktop/h2`, `Desktop/body-l`, `Desktop/label`, `Desktop/body-m`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `accordion/answer`, `accordion/bg`, `accordion/border`, `accordion/icon`, `accordion/question`, `color/surface/page`, `color/text/default`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/body-m`, `font/line-height/desktop/h2`, `font/line-height/desktop/label`, `font/size/desktop/body-l`, `font/size/desktop/body-m`, `font/size/desktop/h2`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `link/default`
<!-- ⚙️ GENERATED:end:faq -->

- **Propósito:** Bloque de preguntas frecuentes (Home, Natural formula, página FAQS): cabecera con enlace y lista de Accordion item.
- **Ejemplo de código:**
  ```html
  <section class="section faq" aria-labelledby="faq-title">
  <div class="section__inner">
  <div class="faq__grid">
  <div class="section__header"><h2 class="section__title" id="faq-title">Preguntas frecuentes</h2><p class="section__lead">Lo que más nos preguntáis.</p><a class="link link--standalone" href="/faqs">Ver todas las preguntas <span class="icon icon-arrow-right" aria-hidden="true"></span></a></div>
  <ul class="faq__list"><li><div class="accordion-item"><h3 class="accordion-item__heading"><button class="accordion-item__button" type="button" aria-expanded="false" aria-controls="q1">¿Cuánto tarda en estar listo?<span class="icon icon-plus" aria-hidden="true"></span></button></h3><div class="accordion-item__panel" id="q1" hidden>Tres minutos.</div></div></li></ul>
  </div>
  </div>
  </section>
  ```
- **Accesibilidad (pares AA verificados):** Título tinta sobre crema 17,2:1; entradilla gris cálido sobre crema 5,4:1; respuestas tinta sobre blanco 18,7:1. Lista de ítems del patrón accordion con un solo ítem abierto a la vez; las respuestas están en el HTML aunque estén cerradas y la página lleva datos estructurados FAQPage.
- **Cuándo usar / qué NO hace:** En la Home y la Natural formula; la página FAQS repite el bloque por categorías sin el enlace. No esconde información legal obligatoria.
