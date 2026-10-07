### Mobile menu   ⚙️ synced: 2026-10-07T18:43:11Z

<!-- ⚙️ GENERATED:start:mobile-menu -->
- **Figma:** `55:119` · página «Pattern / Mobile menu» · COMPONENT · 1 variantes · última sync 2026-10-07T18:43:11Z
- **Descripción (Figma):** Patrón: menú móvil a pantalla completa (se abre desde el botón menú de la Navbar). Logo negativo · cerrar · 5 Nav item (Menu) · Lang switch (solo marcas multiidioma) · CTA. Accesibilidad: role=&quot;dialog&quot; con aria-modal, foco atrapado dentro, Esc cierra y el foco vuelve al botón menú; layer/modal. Sin variables propias.
- **Anatomía:** `logo` → Version=Negative, `close` → Hierarchy=Inverse, Size=M, State=Default, `icon` → Icon / close, `nav-item` → Type=Menu, State=Active, `nav-item` → Type=Menu, State=Default, `nav-item` → Type=Menu, State=Default, `nav-item` → Type=Menu, State=Default, `nav-item` → Type=Menu, State=Default, `lang-switch` → Selected=First, `cta` → Hierarchy=Inverse, Size=L, State=Default, `icon-leading` → Icon / arrow-right, `icon-trailing` → Icon / arrow-right
- **Propiedades de componente:** `Logo#55:6` (INSTANCE_SWAP, por defecto Version=Negative), `Lang switch#55:7` (BOOLEAN, por defecto False)
- **Iconos / instancias anidadas:** sí · swap: `Logo#55:6` · por defecto: Version=Negative
- **Tokens que consume:** `border/width/thick`, `border/width/thin`, `button/inverse/bg`, `button/inverse/border`, `button/inverse/text`, `color/surface/inverse`, `font/family/display`, `font/line-height/desktop/label`, `font/line-height/mobile/h2`, `font/size/desktop/label`, `font/size/mobile/h2`, `font/style/display`, `icon/size/md`, `icon/size/sm`, `lang-switch/bg`, `lang-switch/bg-selected`, `lang-switch/border`, `lang-switch/text`, `lang-switch/text-selected`, `layout/frame`, `layout/margin`, `nav-item/menu-text`, `nav-item/menu-text-active`, `radius/pill`, `radius/sm`, `space/16`, `space/24`, `space/32`, `space/4`, `space/40`, `space/48`, `space/8`
- **Text styles:** `Mobile/h2`, `Desktop/label`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `button/inverse/bg`, `button/inverse/border`, `button/inverse/text`, `color/surface/inverse`, `font/family/display`, `font/line-height/desktop/label`, `font/line-height/mobile/h2`, `font/size/desktop/label`, `font/size/mobile/h2`, `font/style/display`, `lang-switch/bg`, `lang-switch/bg-selected`, `lang-switch/border`, `lang-switch/text`, `lang-switch/text-selected`, `nav-item/menu-text`, `nav-item/menu-text-active`
<!-- ⚙️ GENERATED:end:mobile-menu -->

- **Propósito:** Menú móvil a pantalla completa sobre tinta: logo negativo, cerrar, las cinco secciones, idioma y «Dónde comprar».
- **Ejemplo de código:**
  ```html
  <dialog class="mobile-menu" id="menu" aria-label="Menú" open>
  <div class="mobile-menu__inner">
  <div class="mobile-menu__top">
  <img class="logo" src="../assets/logos/logo-yatekomo-negative.svg" alt="Yatekomo">
  <button class="icon-button icon-button--inverse" type="button" aria-label="Cerrar menú"><span class="icon icon-close" aria-hidden="true"></span></button>
  </div>
  <nav class="mobile-menu__nav" aria-label="Principal">
  <a class="nav-item nav-item--menu" href="/productos" aria-current="page">Productos</a>
  <a class="nav-item nav-item--menu" href="/recetas">Recetas</a>
  </nav>
  <a class="button button--inverse button--l" href="#donde-comprar">Dónde comprar</a>
  </div>
  </dialog>
  ```
- **Accesibilidad (pares AA verificados):** Crema sobre tinta 17,2:1; activo y foco en amarillo 12,3:1. Rol: `<dialog>` modal abierto con `showModal()` (foco atrapado, fondo inerte; el ejemplo lleva `open` solo para mostrarlo), abierto desde el botón de menú de la Navbar; Esc y «Cerrar menú» lo cierran y el foco vuelve al botón de menú. Enlaces grandes (Mobile/h2), muy por encima de 44 px de área táctil.
- **Cuándo usar / qué NO hace:** Solo en móvil y tablet. No es un menú lateral parcial ni contiene búsqueda (la búsqueda sigue en la Navbar).
