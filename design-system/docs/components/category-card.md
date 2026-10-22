### Category card   ⚙️ synced: 2026-10-22T09:37:04Z

<!-- ⚙️ GENERATED:start:category-card -->
- **Figma:** `147:1353` · página «Cards» · COMPONENT_SET · 3 variantes · última sync 2026-10-22T09:37:04Z
- **Descripción (Figma):** Card de categoría de producto (Home · «Our products»: Cups, Bags, Sauces). Anatomía (wireframe UX): imagen de la categoría a sangre (fondo) · Badge New opcional arriba a la izquierda · nombre de la categoría en display h3 sobre placa color/surface/inverse abajo a la izquierda (texto color/text/on-inverse, 17:1). Toda la card es un enlace a la Product library filtrada por ese tipo. Hover: elevation/2; Focus: borde grueso. Desktop 392 px cuadrada; en móvil FILL (343). Sin variables propias.
- **Anatomía:** `badge` → Type=New
- **API:** `name` (string, por defecto Cups) · `badge` (boolean, por defecto false)
- **Estados de CSS:** Hover, Focus
- **Nombres en Figma:** `name` ← `Name#147:0`, `badge` ← `Badge#147:4`
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `badge/new/bg`, `badge/new/text`, `border/width/thin`, `color/border/default`, `color/effect/shadow-ink`, `color/surface/card`, `color/surface/inverse`, `color/text/on-inverse`, `font/family/display`, `font/line-height/desktop/h3`, `font/line-height/mobile/label`, `font/size/desktop/h3`, `font/size/mobile/label`, `font/style/display`, `radius/md`, `radius/pill`, `space/16`, `space/4`, `space/8`
- **Text styles:** `Mobile/label`, `Desktop/h3`
<!-- ⚙️ GENERATED:end:category-card -->

- **Propósito:** Card de categoría de producto (wireframe UX): imagen de la categoría a sangre, Badge New opcional y el nombre sobre una placa de tinta. Lleva a la Product library filtrada por ese tipo.
- **Ejemplo de código:**
  ```html
  <a data-ds="category-card" class="category-card" href="/productos?tipo=cups">
  <img class="category-card__media" src="/media/cups.png" alt="">
  <span class="badge">New</span>
  <span class="category-card__name">Cups</span>
  </a>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Nombre crema sobre tinta 17:1, legible sobre cualquier foto porque va en su placa. La imagen es decorativa (`alt=""`): el nombre da el destino. Toda la card es un único enlace con foco visible; hover y foco no dependen solo del color (sombra y contorno).
- **Cuándo usar / qué NO hace:** En «Our products» de la Home, una por tipo con productos. No muestra productos sueltos (eso es Product card) ni lleva más texto que el nombre.
