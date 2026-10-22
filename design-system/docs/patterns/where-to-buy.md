### Where to buy   ⚙️ synced: 2026-10-22T09:37:04Z

<!-- ⚙️ GENERATED:start:where-to-buy -->
- **Figma:** `92:990` · página «Pattern / Home» · COMPONENT_SET · 2 variantes · última sync 2026-10-22T09:37:04Z
- **Descripción (Figma):** Dónde comprar (Home, página de producto; wireframe UX): antetítulo «Where to buy?» + título (h2, estilo h3) «You can find us at these shops» · fila de logos de distribuidores del país. Cada logo es un enlace externo (<a target="_blank" rel="noopener">) con el logo como imagen y nombre accesible «<Distribuidor> (abre en una pestaña nueva)»; sin tarjeta: el logo va directo sobre color/surface/brand, con la trama de fideos (Decoration / Noodle texture) a sangre por la derecha, detrás. Los distribuidores cambian por país y los logos los aporta GB Foods (no se recrean). Desktop: texto a la izquierda y logos a la derecha; Mobile: texto arriba y logos en fila con scroll horizontal. Sin variables propias.
- **Anatomía:** `noodle-texture` → Decoration / Noodle texture, `noodle` → Shape=1, Tone=Texture, `noodle` → Shape=3, Tone=Texture, `noodle` → Shape=5, Tone=Texture, `noodle` → Shape=2, Tone=Texture, `noodle` → Shape=4, Tone=Texture
- **API:** `breakpoint`: Desktop, Mobile (por defecto Desktop)
- **Nombres en Figma:** `breakpoint` ← `Breakpoint`
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `border/width/thin`, `color/surface/brand`, `color/text/default`, `color/text/secondary`, `decoration/noodle/texture`, `font/family/body`, `font/family/display`, `font/line-height/desktop/caption`, `font/line-height/desktop/h3`, `font/size/desktop/caption`, `font/size/desktop/h3`, `font/style/body`, `font/style/display`, `layout/frame`, `layout/gutter`, `layout/margin`, `layout/section-y`, `radius/md`, `space/32`, `space/4`, `space/64`
- **Text styles:** `Desktop/caption`, `Desktop/h3`
<!-- ⚙️ GENERATED:end:where-to-buy -->

- **Propósito:** Dónde comprar (wireframe UX): antetítulo, título y logos de los distribuidores del país, cada uno enlace externo.
- **Ejemplo de código:**
  ```html
  <section data-ds="where-to-buy" class="section where-to-buy" id="donde-comprar" aria-labelledby="wtb-title">
  <div class="decoration-noodle-texture" aria-hidden="true"><span class="decoration-noodle decoration-noodle--texture"></span><span class="decoration-noodle decoration-noodle--3 decoration-noodle--texture"></span><span class="decoration-noodle decoration-noodle--5 decoration-noodle--texture"></span><span class="decoration-noodle decoration-noodle--2 decoration-noodle--texture"></span><span class="decoration-noodle decoration-noodle--4 decoration-noodle--texture"></span></div>
  <div class="section__inner">
  <div class="where-to-buy__grid">
  <div class="where-to-buy__text"><span class="where-to-buy__kicker">Where to buy?</span><h2 class="where-to-buy__title" id="wtb-title">You can find us at these shops</h2></div>
  <ul class="where-to-buy__list"><li><a class="where-to-buy__retailer" href="https://tienda.example.org" target="_blank" rel="noopener"><img src="/media/distribuidor.svg" alt="Distribuidor (abre en una pestaña nueva)"></a></li></ul>
  </div>
  </div>
  </section>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Tinta sobre amarillo 12,3:1 y sobre el ámbar de la trama ≥ 9:1 (la trama es decorativa, `aria-hidden`). Cada logo es un enlace externo con nombre «Distribuidor (abre en una pestaña nueva)» y foco visible. En móvil la fila se desplaza en horizontal con teclado.
- **Cuándo usar / qué NO hace:** En la Home y en la ficha de producto. Los distribuidores cambian por país y los logos los aporta GB Foods (no se recrean).
