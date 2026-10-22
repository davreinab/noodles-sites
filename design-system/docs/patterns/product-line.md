### Product line   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:product-line -->
- **Figma:** `212:746` · página «Pattern / Libraries» · COMPONENT_SET · 6 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** Product line: bloque de una línea de producto de la Product library (Yatekomo, Yakisoba, Sauces): packshot grande (placeholder 3D, sin fotografía) a la izquierda en Standard y, a la derecha, nombre de línea (h3), descripción, «Find your favourite flavour» (h4) y rejilla de Flavour tile (5 columnas en desktop, 2 en mobile). Surface=Light (crema/blanco) o Dark (tinta) para alternar bandas; Header (opcional) muestra la cabecera de formato («Cups», «Sauces»). Kind=Sauces: sin packshot, rejilla de Flavour tile Tall (3 columnas en desktop; carrusel horizontal en mobile). Uso: Product library (wireframe desktop 396:5932, móvil 396:12565). Clase CSS: .product-line (modificadores .product-line--dark y .product-line--sauces).
- **Anatomía:** `Flavour tile` → Size=Square, State=Default, `Badge` → Type=New, `Flavour tile` → Size=Square, State=Default, `Badge` → Type=New, `Flavour tile` → Size=Square, State=Default, `Badge` → Type=New, `Flavour tile` → Size=Square, State=Default, `Badge` → Type=Vegan, `Flavour tile` → Size=Square, State=Default, `Badge` → Type=New, `Flavour tile` → Size=Square, State=Default, `Badge` → Type=New, `Flavour tile` → Size=Square, State=Default, `Badge` → Type=Hot, `Flavour tile` → Size=Square, State=Default, `Badge` → Type=New
- **API:** `header` (boolean, por defecto true) · `surface`: Light, Dark (por defecto Light) · `breakpoint`: Desktop, Mobile (por defecto Desktop) · `kind`: Standard, Sauces (por defecto Standard)
- **Nombres en Figma:** `header` ← `Header#212:0`, `surface` ← `Surface`, `breakpoint` ← `Breakpoint`, `kind` ← `Kind`
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `badge/natural/bg`, `badge/natural/text`, `badge/new/bg`, `badge/new/text`, `color/surface/card`, `color/surface/page`, `color/text/default`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/desktop/h2`, `font/line-height/desktop/h3`, `font/line-height/mobile/label`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/desktop/h2`, `font/size/desktop/h3`, `font/size/mobile/label`, `font/style/body`, `font/style/display`, `product-card/media-bg`, `product-card/meta`, `product-card/title`, `radius/lg`, `radius/md`, `radius/pill`, `space/16`, `space/24`, `space/32`, `space/4`, `space/48`, `space/64`, `space/8`, `space/80`
- **Text styles:** `Desktop/h2`, `Desktop/body-m`, `Desktop/caption`, `Desktop/h3`, `Mobile/label`
<!-- ⚙️ GENERATED:end:product-line -->

- **Propósito:** Bloque de una línea de producto dentro de un formato de la página Products: packshot grande a la izquierda y, a la derecha, nombre de línea (YATEKOMO, YAKISOBA), descripción, «Find your favourite flavour» y la rejilla de sabores (Flavour tile). Las líneas consecutivas alternan Surface Light (blanco) y Dark (tinta). Type Sauces no lleva packshot: muestra las salsas como Flavour tile Tall (3 columnas en escritorio; carrusel horizontal en móvil). La cabecera del formato (`product-line__head`, con «Cups» y su subtítulo) es opcional. Las secciones con ancla llevan `id` (p. ej. `id="cups"`) para Anchor nav. Las secciones con ancla tienen `scroll-margin-top` igual a la altura de la navbar, para que la barra sticky no tape el encabezado.
- **Ejemplo de código:**
  ```html
  <section data-ds="product-line" class="section product-line" id="cups" aria-labelledby="pl-yatekomo">
  <div class="product-line__head"><h2 class="section__title">Cups</h2><p class="section__lead">Ready in 3 minutes.</p></div>
  <div class="product-line__inner">
  <div class="product-line__pack"><img src="../assets/images/placeholder.svg" alt=""></div>
  <div class="product-line__info">
  <h3 class="product-line__name" id="pl-yatekomo">Yatekomo</h3>
  <p class="product-line__description">Take our word for it. Oriental-style noodles, no fuss, ready in 3 minutes.</p>
  <h4 class="product-line__subtitle">Find your favourite flavour</h4>
  <ul class="product-line__grid">
  <li><a class="flavour-tile" href="/productos/chicken-yakisoba"><span class="flavour-tile__media"><img src="../assets/images/placeholder.svg" alt=""><span class="badge">New</span></span><span class="flavour-tile__name">Chicken</span></a></li>
  <li><a class="flavour-tile" href="/productos/hot-spicy"><span class="flavour-tile__media"><img src="../assets/images/placeholder.svg" alt=""><span class="badge badge--hot">Hot!</span></span><span class="flavour-tile__name">Hot &amp; Spicy</span></a></li>
  </ul>
  </div>
  </div>
  </section>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Rol: sección (`section`) con nombre por su h3 de línea (`aria-labelledby`). Jerarquía: h2 del formato (si hay cabecera), h3 de la línea y h4 «Find your favourite flavour». El packshot lleva `alt=""` porque el nombre de la línea va escrito a su lado. Las tarjetas de sabor son enlaces (Flavour tile) cuyo nombre es el texto visible, con el badge delante si lo hay. El patrón no tiene más controles. Teclado: Tab entra en la primera tarjeta y recorre la rejilla en orden; en el carrusel móvil de Sauces, el contenedor no captura teclas y Tab sigue el orden del DOM. El foco lo pone Flavour tile.
- **Cuándo usar / qué NO hace:** Para cada línea de producto dentro de un formato (Cups, Bags, Sauces) en la página Products. No es una ficha de producto (eso son Product hero y Product details) ni un listado filtrable: no filtra y no pagina. Una línea sin sabores no se muestra.
