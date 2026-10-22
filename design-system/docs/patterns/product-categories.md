### Product categories   ⚙️ synced: 2026-10-22T09:37:04Z

<!-- ⚙️ GENERATED:start:product-categories -->
- **Figma:** `91:837` · página «Pattern / Home» · COMPONENT_SET · 2 variantes · última sync 2026-10-22T09:37:04Z
- **Descripción (Figma):** Productos de la Home (wireframe UX «Our products»): título (h2) + entradilla · 3 Category card, una por tipo de producto (Cups, Bags, Sauces; solo tipos con productos) que llevan a la Product library filtrada. Badge New en la categoría con novedad. Desktop: 3 columnas iguales (gutter layout/gutter); Mobile: apiladas a todo el ancho. Sustituye al antiguo Product carousel (pestañas + Product card). Sin variables propias.
- **Anatomía:** `category-card` → State=Default, `badge` → Type=New, `category-card` → State=Default, `badge` → Type=New, `category-card` → State=Default, `badge` → Type=New
- **API:** `breakpoint`: Desktop, Mobile (por defecto Desktop)
- **Nombres en Figma:** `breakpoint` ← `Breakpoint`
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `badge/new/bg`, `badge/new/text`, `border/width/thin`, `color/border/default`, `color/effect/shadow-ink`, `color/surface/card`, `color/surface/inverse`, `color/surface/page`, `color/text/default`, `color/text/on-inverse`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/h2`, `font/line-height/desktop/h3`, `font/line-height/mobile/label`, `font/size/desktop/body-l`, `font/size/desktop/h2`, `font/size/desktop/h3`, `font/size/mobile/label`, `font/style/body`, `font/style/display`, `layout/frame`, `layout/gutter`, `layout/margin`, `layout/section-y`, `radius/md`, `radius/pill`, `space/16`, `space/32`, `space/4`, `space/8`
- **Text styles:** `Desktop/h2`, `Desktop/body-l`, `Mobile/label`, `Desktop/h3`
<!-- ⚙️ GENERATED:end:product-categories -->

- **Propósito:** Productos de la Home (wireframe UX «Our products»): título, entradilla y una Category card por tipo de producto (Cups, Bags, Sauces) que lleva a la Product library filtrada.
- **Ejemplo de código:**
  ```html
  <section data-ds="product-categories" class="section product-categories" aria-labelledby="pc-title">
  <div class="section__inner">
  <div class="section__header"><h2 class="section__title" id="pc-title">Our products</h2><p class="section__lead">Products and flavors for every taste. Find your match!</p></div>
  <ul class="product-categories__grid">
  <li><a class="category-card" href="/productos?tipo=cups"><img class="category-card__media" src="/media/cups.png" alt=""><span class="category-card__name">Cups</span></a></li>
  <li><a class="category-card" href="/productos?tipo=sauces"><img class="category-card__media" src="/media/sauces.png" alt=""><span class="badge">New</span><span class="category-card__name">Sauces</span></a></li>
  </ul>
  </div>
  </section>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Título tinta sobre crema 17,2:1; el resto, los pares de Category card. La lista es un `<ul>` y cada card, un único enlace con el nombre de la categoría como texto.
- **Cuándo usar / qué NO hace:** En la Home. Solo se muestran tipos con productos (regla de negocio). Sustituye al antiguo Product carousel (pestañas + Product card): las fichas de producto viven en la Product library.
