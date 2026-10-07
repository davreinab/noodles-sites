### Accordion item   ⚙️ synced: 2026-10-07T18:43:11Z

<!-- ⚙️ GENERATED:start:accordion-item -->
- **Figma:** `69:93` · página «Accordion item» · COMPONENT_SET · 6 variantes · última sync 2026-10-07T18:43:11Z
- **Descripción (Figma):** Ítem de acordeón para FAQ (página FAQS indexada, Natural formula, Home). Cabecera = &lt;button aria-expanded aria-controls&gt; dentro de un encabezado (h3); la respuesta es una región ligada a la cabecera. Enter/Espacio abren y cierran; cada ítem es independiente (varios abiertos a la vez). Icono plus (cerrado) / minus (abierto), swaps Icon collapsed / Icon expanded. Para SEO/AEO la respuesta está en el HTML aunque esté cerrada (FAQPage schema). Hover: accordion/bg-hover; Focus: anillo accordion/focus-ring. Ancho FILL de la columna de lectura.
- **Anatomía:** `icon-collapsed` → Icon / plus
- **Expanded:** False, True
- **State:** Default, Hover, Focus
- **Propiedades de componente:** `Question#69:0` (TEXT, por defecto ¿Por qué decimos que es 100 % natural?), `Answer#69:7` (TEXT, por defecto Respuesta de ejemplo: todos los ingredientes son de origen natural, sin aditivos ni conservantes. El texto definitivo lo valida GB Foods y va alineado con el envase.), `Icon collapsed#69:14` (INSTANCE_SWAP, por defecto Icon / plus), `Icon expanded#69:21` (INSTANCE_SWAP, por defecto Icon / minus), `Expanded` (VARIANT, por defecto False), `State` (VARIANT, por defecto Default)
- **Iconos / instancias anidadas:** sí · swap: `Icon collapsed#69:14`, `Icon expanded#69:21` · por defecto: Icon / plus, Icon / minus
- **Tokens que consume:** `accordion/bg`, `accordion/border`, `accordion/icon`, `accordion/question`, `border/width/thin`, `font/family/body`, `font/line-height/desktop/body-l`, `font/size/desktop/body-l`, `font/style/body`, `icon/size/md`, `radius/md`, `space/16`, `space/24`
- **Text styles:** `Desktop/body-l`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `accordion/bg`, `accordion/border`, `accordion/icon`, `accordion/question`, `font/family/body`, `font/line-height/desktop/body-l`, `font/size/desktop/body-l`, `font/style/body`
<!-- ⚙️ GENERATED:end:accordion-item -->

- **Propósito:** Pregunta y respuesta del FAQ. La pregunta es un botón que abre y cierra la respuesta; varios ítems pueden estar abiertos a la vez.
- **Ejemplo de código:**
  ```html
  <div class="accordion-item">
  <h3 class="accordion-item__heading">
  <button class="accordion-item__button" type="button" aria-expanded="true" aria-controls="faq-1">¿Por qué decimos que es 100 % natural?<span class="icon icon-plus" aria-hidden="true"></span></button>
  </h3>
  <div class="accordion-item__panel" id="faq-1" role="region" aria-labelledby="faq-1-btn">Todos los ingredientes son de origen natural, sin aditivos ni conservantes.</div>
  </div>
  ```
- **Accesibilidad (pares AA verificados):** Pregunta y respuesta en tinta sobre blanco 18,7:1; hover tinta sobre amarillo 12,3:1; icono más/menos en tinta (≥ 3:1). Rol: patrón accordion de WAI-ARIA: `<button aria-expanded aria-controls>` dentro de un encabezado y panel `role="region"`. El icono cambia de más a menos con `aria-expanded`, que es lo que se anuncia. Teclado: Tab entre preguntas, Enter o Espacio para abrir. Foco: el contorno de 2 px rodea el ítem entero. Para SEO/AEO la respuesta está en el HTML aunque esté cerrada (con `hidden` cuando se cierra) y la página lleva FAQPage.
- **Cuándo usar / qué NO hace:** Para preguntas frecuentes (FAQ de Home, Natural formula y página FAQS). No esconde contenido esencial de una página de producto ni sustituye a las pestañas.
