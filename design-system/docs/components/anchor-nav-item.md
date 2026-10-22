### Anchor nav item   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:anchor-nav-item -->
- **Figma:** `210:57` · página «Navigation» · COMPONENT_SET · 2 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** Anchor nav item: elemento de la barra de anclas del catálogo; miniatura del envase (hueco product-card/media-bg) + etiqueta en píldora Anton (Desktop/h3). State=Current marca la sección visible (aria-current en código; chip seleccionado). Propiedad Label = nombre del formato (Cups, Bags, Sauces). Uso: Anchor nav (Product library, wireframe desktop 396:5932 y móvil 396:12565). Clase CSS: .anchor-nav__item.
- **Anatomía:** sin instancias anidadas
- **API:** `label` (string, por defecto Cups) · `current` (boolean, por defecto false)
- **Nombres en Figma:** `label` ← `Label#210:0`, `current` ← `State=Current`
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `chip/bg`, `chip/text`, `font/family/display`, `font/line-height/desktop/h3`, `font/size/desktop/h3`, `font/style/display`, `product-card/media-bg`, `radius/md`, `radius/pill`, `space/24`, `space/8`
- **Text styles:** `Desktop/h3`
<!-- ⚙️ GENERATED:end:anchor-nav-item -->

- **Propósito:** Un ítem de la barra de anclas (`.anchor-nav`): miniatura del envase y etiqueta en píldora que lleva a una sección del catálogo. State=Current marca la sección visible. Lo compone `anchor-nav`; no se usa suelto.
- **Ejemplo de código:**
  ```html
  <a data-ds="anchor-nav-item" class="anchor-nav__item" href="#cups" aria-current="true"><img class="anchor-nav__thumb" src="../assets/images/placeholder.svg" alt=""><span class="anchor-nav__label">Cups</span></a>
  <a data-ds="anchor-nav-item" class="anchor-nav__item" href="#bags"><img class="anchor-nav__thumb" src="../assets/images/placeholder.svg" alt=""><span class="anchor-nav__label">Bags</span></a>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Es un enlace (`a`) a un ancla; su nombre es el texto de la etiqueta («Cups»). La miniatura es `alt=""` porque es decorativa. Current lleva `aria-current="true"` y el relleno de la píldora (chip seleccionado) solo lo refuerza. Teclado: Tab y Enter siguen el ancla. Foco: contorno de 2 px.
- **Cuándo usar / qué NO hace:** Solo dentro de `anchor-nav`. No es un botón de filtro ni una pestaña: desplaza a la sección, no cambia contenido.
