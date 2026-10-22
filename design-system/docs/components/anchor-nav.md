### Anchor nav   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:anchor-nav -->
- **Figma:** `210:84` · página «Navigation» · COMPONENT_SET · 2 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** Anchor nav: barra de anclas sticky bajo la navbar (position sticky en código) que lleva a las secciones de formato Cups · Bags · Sauces de la única página de catálogo; sustituye al Product filter (retirado). Enlaces #cups, #bags, #sauces; el item de la sección visible va en State=Current (aria-current). Breakpoint Desktop: fila centrada sobre fondo amarillo brand; Mobile: fila desplazable en horizontal. Uso: Product library (wireframe desktop 396:5932 y móvil 396:12565). Clase CSS: .anchor-nav (items .anchor-nav__item).
- **Anatomía:** `Anchor nav item` → State=Current, `Anchor nav item` → State=Default, `Anchor nav item` → State=Default
- **API:** `breakpoint`: Desktop, Mobile (por defecto Desktop)
- **Nombres en Figma:** `breakpoint` ← `Breakpoint`
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `chip/bg`, `chip/bg-selected`, `chip/text`, `chip/text-selected`, `color/surface/brand`, `font/family/display`, `font/line-height/desktop/h3`, `font/size/desktop/h3`, `font/style/display`, `product-card/media-bg`, `radius/md`, `radius/pill`, `space/16`, `space/24`, `space/32`, `space/8`
- **Text styles:** `Desktop/h3`
<!-- ⚙️ GENERATED:end:anchor-nav -->

- **Propósito:** Barra de anclas que lleva a las secciones de formato de una página de producto (Cups · Bags · Sauces). Cada ítem muestra la miniatura del envase y su etiqueta en píldora. Es sticky bajo la navbar y su fondo es el amarillo de marca. El componente no tiene JavaScript: la página marca la sección visible con `aria-current="true"` al hacer scroll. El top del sticky es la altura de la navbar, calculada con tokens existentes (padding vertical ×2 + logo: `--space-48` en escritorio, `--space-40` en móvil).
- **Ejemplo de código:**
  ```html
  <nav data-ds="anchor-nav" class="anchor-nav" aria-label="Product formats">
  <ul class="anchor-nav__list">
  <li><a class="anchor-nav__item" href="#cups" aria-current="true"><img class="anchor-nav__thumb" src="../assets/images/placeholder.svg" alt=""><span class="anchor-nav__label">Cups</span></a></li>
  <li><a class="anchor-nav__item" href="#bags"><img class="anchor-nav__thumb" src="../assets/images/placeholder.svg" alt=""><span class="anchor-nav__label">Bags</span></a></li>
  <li><a class="anchor-nav__item" href="#sauces"><img class="anchor-nav__thumb" src="../assets/images/placeholder.svg" alt=""><span class="anchor-nav__label">Sauces</span></a></li>
  </ul>
  </nav>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Rol: landmark `nav` con nombre por `aria-label` («Product formats»), para distinguirla de la navegación principal. Cada ítem es un enlace a un ancla (`#cups`, `#bags`, `#sauces`); su nombre sale del texto visible de la etiqueta. La miniatura lleva `alt=""` porque es decorativa y repite el nombre. Estado seleccionado: la sección visible lleva `aria-current="true"` en su enlace; el relleno tinta de la etiqueta lo muestra también, pero el lector lo anuncia por el atributo. Teclado: Tab entra y recorre los enlaces en orden; Enter sigue el ancla. Foco: contorno de 2 px en el enlace. El sticky no mueve el foco, y en móvil, con la fila desplazable, los enlaces siguen siendo tabulables.
- **Cuándo usar / qué NO hace:** Para saltar entre las secciones de formato dentro de una misma página de producto. No es un filtro ni pestañas: no cambia el contenido, solo desplaza. No sustituye a la navegación principal y no se usa si la página tiene una sola sección.
