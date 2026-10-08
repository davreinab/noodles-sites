### Natural formula   ⚙️ synced: 2026-10-08T11:52:41Z

<!-- ⚙️ GENERATED:start:natural-formula -->
- **Figma:** `91:704` · página «Pattern / Home» · COMPONENT_SET · 2 variantes · última sync 2026-10-08T11:52:41Z
- **Descripción (Figma):** Sección de la fórmula natural (Home, wireframe UX): título display «100% natural noodles. Nothing else» (h2) · lista de ingredientes eliminados: cada uno con el nombre tachado (Additives, Preservatives, Palm oil, Glutamate; &lt;s&gt; o &lt;del&gt;, con texto oculto «sin») y la frase que lo explica · Button Inverse L «Learn more» a la Natural formula page (Inverse por contraste sobre el verde; el wireframe dibuja Secondary sobre blanco). Fondo color/surface/natural con texto color/text/on-natural (5,5:1). Los textos deben coincidir con el envase (restricción regulatoria). Desktop: título a la izquierda y lista a la derecha; Mobile: apilado. Sin variables propias.
- **Anatomía:** `cta` → Hierarchy=Inverse, Size=L, State=Default, `icon-leading` → Icon / arrow-right, `icon-trailing` → Icon / arrow-right
- **Breakpoint:** Desktop, Mobile
- **Propiedades de componente:** `Breakpoint` (VARIANT, por defecto Desktop)
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `border/width/thick`, `button/inverse/bg`, `button/inverse/border`, `button/inverse/text`, `color/surface/natural`, `color/text/on-natural`, `font/family/body`, `font/family/display`, `font/line-height/desktop/caption`, `font/line-height/desktop/display`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/size/desktop/caption`, `font/size/desktop/display`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/sm`, `layout/frame`, `layout/margin`, `layout/section-y`, `radius/pill`, `space/24`, `space/32`, `space/4`, `space/48`, `space/64`, `space/8`
- **Text styles:** `Desktop/display`, `Desktop/caption`, `Desktop/h3`, `Desktop/label`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `button/inverse/bg`, `button/inverse/border`, `button/inverse/text`, `color/surface/natural`, `color/text/on-natural`, `font/family/body`, `font/family/display`, `font/line-height/desktop/caption`, `font/line-height/desktop/display`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/size/desktop/caption`, `font/size/desktop/display`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/style/body`, `font/style/display`
<!-- ⚙️ GENERATED:end:natural-formula -->

- **Propósito:** Fórmula natural en la Home (wireframe UX): título display y lista de ingredientes eliminados, tachados, con la frase que explica cada uno, más «Learn more».
- **Ejemplo de código:**
  ```html
  <section class="section natural-formula" aria-labelledby="nf-title">
  <div class="section__inner">
  <div class="natural-formula__grid">
  <h2 class="natural-formula__title" id="nf-title">100% natural noodles. Nothing else</h2>
  <div class="natural-formula__list">
  <ul class="natural-formula__removed">
  <li class="natural-formula__item"><s class="natural-formula__ingredient"><span class="visually-hidden">Sin </span>Additives</s><span class="natural-formula__statement">We’re all about the natural flavour of our ingredients</span></li>
  </ul>
  <a class="button button--inverse button--l" href="/formula-natural">Learn more</a>
  </div>
  </div>
  </div>
  </section>
  ```
- **Accesibilidad (pares AA verificados):** Texto blanco sobre verde 5,5:1 (también el tachado, que es caption). El tachado no depende solo del estilo: `<s>` lleva un «Sin» oculto para lectores de pantalla. Button Inverse por contraste sobre el verde.
- **Cuándo usar / qué NO hace:** En la Home y como resumen de la Natural formula page. Los textos deben coincidir con el envase (restricción regulatoria): no se añaden ingredientes ni frases sin validación de GB Foods.
