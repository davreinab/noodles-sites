### Where to buy   ⚙️ synced: 2026-10-08T11:10:38Z

<!-- ⚙️ GENERATED:start:where-to-buy -->
- **Figma:** `92:990` · página «Pattern / Home» · COMPONENT_SET · 2 variantes · última sync 2026-10-08T11:10:38Z
- **Descripción (Figma):** Dónde comprar (Home, página de producto; destino del CTA de la Navbar; wireframe UX): antetítulo «Where to buy?» + título (h2, estilo h3) «You can find us at these shops» · fila de logos de distribuidores del país. Cada logo es un enlace externo (&lt;a target=&quot;_blank&quot; rel=&quot;noopener&quot;&gt;) con el logo como imagen y nombre accesible «&lt;Distribuidor&gt; (abre en una pestaña nueva)»; sin tarjeta: el logo va directo sobre color/surface/brand. Los distribuidores cambian por país y los logos los aporta GB Foods (no se recrean). Desktop: texto a la izquierda y logos a la derecha; Mobile: texto arriba y logos en fila con scroll horizontal. Sin variables propias.
- **Anatomía:** sin instancias anidadas
- **Breakpoint:** Desktop, Mobile
- **Propiedades de componente:** `Breakpoint` (VARIANT, por defecto Desktop)
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `border/width/thin`, `color/surface/brand`, `color/text/default`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/caption`, `font/line-height/desktop/h3`, `font/size/desktop/caption`, `font/size/desktop/h3`, `font/style/body`, `font/style/display`, `layout/frame`, `layout/gutter`, `layout/margin`, `layout/section-y`, `radius/md`, `space/32`, `space/4`, `space/64`
- **Text styles:** `Desktop/caption`, `Desktop/h3`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `color/surface/brand`, `color/text/default`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/caption`, `font/line-height/desktop/h3`, `font/size/desktop/caption`, `font/size/desktop/h3`, `font/style/body`, `font/style/display`
<!-- ⚙️ GENERATED:end:where-to-buy -->

- **Propósito:** Dónde comprar (wireframe UX): antetítulo, título y logos de los distribuidores del país, cada uno enlace externo.
- **Ejemplo de código:**
  ```html
  <section class="section where-to-buy" id="donde-comprar" aria-labelledby="wtb-title">
  <div class="section__inner">
  <div class="where-to-buy__grid">
  <div class="where-to-buy__text"><span class="where-to-buy__kicker">Where to buy?</span><h2 class="where-to-buy__title" id="wtb-title">You can find us at these shops</h2></div>
  <ul class="where-to-buy__list"><li><a class="where-to-buy__retailer" href="https://tienda.example.org" target="_blank" rel="noopener"><img src="/media/distribuidor.svg" alt="Distribuidor (abre en una pestaña nueva)"></a></li></ul>
  </div>
  </div>
  </section>
  ```
- **Accesibilidad (pares AA verificados):** Tinta sobre amarillo 12,3:1. Cada logo es un enlace externo con nombre «Distribuidor (abre en una pestaña nueva)» y foco visible. En móvil la fila se desplaza en horizontal con teclado.
- **Cuándo usar / qué NO hace:** En la Home y en la ficha de producto. Los distribuidores cambian por país y los logos los aporta GB Foods (no se recrean).
