### Library hero   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:library-hero -->
- **Figma:** `211:327` · página «Pattern / Libraries» · COMPONENT_SET · 2 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** Library hero: cabecera a sangre de la Product library (fondo tinta). Título de página («Products»), bloque destacado con Badge New, titular («Discover the brand new Yakisoba Pollo») y entradilla («100% Natural ingredients with even more asiatic flavour»); a la derecha dos packshots 3D como placeholder (hueco product-card/media-bg, sin fotografía). Breakpoint Desktop: dos columnas; Mobile: apilado. Uso: Product library (wireframe desktop 396:5932, móvil 396:12565). Clase CSS: .library-hero.
- **Anatomía:** `Badge` → Type=New
- **API:** `breakpoint`: Desktop, Mobile (por defecto Desktop)
- **Nombres en Figma:** `breakpoint` ← `Breakpoint`
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `badge/new/bg`, `badge/new/text`, `color/surface/inverse`, `color/text/on-inverse`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/caption`, `font/line-height/desktop/h1`, `font/line-height/desktop/h3`, `font/line-height/mobile/label`, `font/size/desktop/body-l`, `font/size/desktop/caption`, `font/size/desktop/h1`, `font/size/desktop/h3`, `font/size/mobile/label`, `font/style/body`, `font/style/display`, `product-card/media-bg`, `product-card/meta`, `radius/lg`, `radius/pill`, `space/16`, `space/24`, `space/4`, `space/64`, `space/8`, `space/80`
- **Text styles:** `Desktop/h1`, `Mobile/label`, `Desktop/h3`, `Desktop/body-l`, `Desktop/caption`
<!-- ⚙️ GENERATED:end:library-hero -->

- **Propósito:** Cabecera de la página Products: título de página («Products») y un bloque destacado que presenta una novedad, con Badge New, titular (h2), texto y dos packshots a la derecha. Va sobre tinta, al inicio de la página, antes de Anchor nav y de las líneas de producto (Product line). En móvil el bloque se apila: texto primero y packshots debajo.
- **Ejemplo de código:**
  ```html
  <section data-ds="library-hero" class="section library-hero" aria-labelledby="lhero-title">
  <div class="library-hero__inner">
  <h1 class="page-title library-hero__title" id="lhero-title">Products</h1>
  <div class="library-hero__feature">
  <div class="library-hero__info">
  <span class="badge">New</span>
  <h2 class="library-hero__heading">Discover the brand new Yakisoba Pollo</h2>
  <p class="library-hero__text">100% Natural ingredients with even more asiatic flavour</p>
  </div>
  <div class="library-hero__media">
  <img class="library-hero__pack" src="../assets/images/placeholder.svg" alt="">
  <img class="library-hero__pack" src="../assets/images/placeholder.svg" alt="">
  </div>
  </div>
  </div>
  </section>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Rol: sección con nombre por su h1 (`aria-labelledby`). Hay un solo `h1` en la página (el título «Products»); el bloque destacado usa `h2`. El badge «New» se lee como texto antes del titular. Los packshots llevan `alt=""`: son decorativos porque el `h2` ya nombra el producto; si una imagen aportara un dato que no está en el texto, llevaría alt descriptivo. El patrón no tiene controles, así que no tiene foco ni teclado propio. Los textos van en crema sobre tinta (`--color-text-on-inverse`).
- **Cuándo usar / qué NO hace:** Solo en la página Products, una vez y al inicio. No es un Hero de marca ni una promoción: no lleva CTA ni fondo de marca (para eso están Hero y Promo). Para el catálogo de recetas la cabecera es Library head.
