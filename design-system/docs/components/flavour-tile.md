### Flavour tile   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:flavour-tile -->
- **Figma:** `209:138` · página «Cards» · COMPONENT_SET · 6 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** Flavour tile: tarjeta de sabor de la Product line (cups, bags y salsas). Size=Square: imagen 1:1 (sabores). Size=Tall: imagen 3:4 (salsas). Badge opcional arriba a la izquierda (New, Vegan o Hot!, mediante Badge type) y nombre debajo en body bold (Archivo Bold sobre Desktop/body-m). Toda la tarjeta es un enlace a la ficha del sabor. Estados: Default; Hover (elevation de Product card); Focus (anillo product-card/focus-ring). Uso: Product line del catálogo (wireframe desktop 396:5932 y móvil 396:12565). Clase CSS: .flavour-tile (variante Tall: .flavour-tile--tall). Textos de ejemplo en inglés.
- **Anatomía:** `Badge` → Type=New
- **API:** `name` (string, por defecto Chicken) · `badge` (boolean, por defecto true) · `badgeType` (icon, por defecto Type=New) · `size`: Square, Tall (por defecto Square)
- **Estados de CSS:** Hover, Focus
- **Nombres en Figma:** `name` ← `Name#209:0`, `badge` ← `Badge#209:7`, `badgeType` ← `Badge type#209:14`, `size` ← `Size`
- **Iconos / instancias anidadas:** sí · swap: `badgeType` · por defecto: Type=New
- **Tokens que consume:** `badge/new/bg`, `badge/new/text`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/mobile/label`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/mobile/label`, `font/style/body`, `font/style/display`, `product-card/media-bg`, `product-card/meta`, `product-card/title`, `radius/md`, `radius/pill`, `space/4`, `space/8`
- **Text styles:** `Desktop/caption`, `Mobile/label`
<!-- ⚙️ GENERATED:end:flavour-tile -->

- **Propósito:** Tarjeta de un sabor (Square, por defecto) o de una salsa (Tall, imagen 3:4) dentro de una línea de Product line. Lleva un badge opcional arriba a la izquierda, dentro de la imagen (New, Vegan o Hot!), y el nombre debajo en body negrita. Toda la tarjeta es el enlace a la ficha del producto. Estados como Product card: hover sube la sombra dura (elevation/2) sobre la imagen; foco, contorno fino.
- **Ejemplo de código:**
  ```html
  <a data-ds="flavour-tile" class="flavour-tile" href="/productos/chicken-yakisoba">
  <span class="flavour-tile__media"><img src="../assets/images/placeholder.svg" alt=""><span class="badge">New</span></span>
  <span class="flavour-tile__name">Chicken</span>
  </a>
  <a data-ds="flavour-tile" class="flavour-tile flavour-tile--tall" href="/productos/sesame-sauce">
  <span class="flavour-tile__media"><img src="../assets/images/placeholder.svg" alt=""><span class="badge badge--hot">Hot!</span></span>
  <span class="flavour-tile__name">Sesame sauce</span>
  </a>
  <a data-ds="flavour-tile" class="flavour-tile" href="/productos/chicken-rice-noodles">
  <span class="flavour-tile__media"><img src="../assets/images/placeholder.svg" alt=""></span>
  <span class="flavour-tile__name">Chicken rice noodles</span>
  </a>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Rol: enlace (`a`) que engloba la tarjeta. Su nombre accesible es el texto visible completo, incluido el badge si lo hay («New Chicken»), por eso el badge va antes del nombre en el DOM. La imagen lleva `alt=""` porque el nombre va escrito debajo. No tiene estado seleccionado. Hover: sombra sobre la imagen; el enlace se distingue por su nombre, no solo por el hover. Teclado: Tab alcanza el enlace y Enter abre la ficha. Foco: contorno fino sobre la imagen (trazo de foco de Product card), no sobre la tarjeta entera.
- **Cuándo usar / qué NO hace:** Para cada sabor o salsa de una rejilla dentro de Product line (Square en 5 columnas, Tall en 3). No es un botón de compra ni un filtro, y no lleva precio. El texto del badge se lee como parte del nombre; no añadir frases largas.
