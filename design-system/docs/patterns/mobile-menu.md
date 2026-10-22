### Mobile menu   ⚙️ synced: 2026-10-22T09:37:04Z

<!-- ⚙️ GENERATED:start:mobile-menu -->
- **Figma:** `55:119` · página «Pattern / Global» · COMPONENT · 1 variantes · última sync 2026-10-22T09:37:04Z
- **Descripción (Figma):** Patrón: menú a pantalla completa en todos los breakpoints (wireframe UX: se abre desde el botón menú de la Navbar, también en desktop). Logo negativo · cerrar · 5 Nav item (Menu): Products, Natural formula, Recipes, Contests, FAQS · Lang switch (solo marcas multiidioma) · «Our social media:» con los iconos de redes de la marca (enlaces externos) · © GBFoods. Accesibilidad: <dialog> modal, foco atrapado dentro, Esc cierra y el foco vuelve al botón menú; layer/modal. Fondo color/surface/inverse. Sin variables propias.
- **Anatomía:** `logo` → Version=Negative, `close` → Hierarchy=Inverse, Size=M, State=Default, `icon` → Icon / close, `nav-item` → Type=Menu, State=Active, `nav-item` → Type=Menu, State=Default, `nav-item` → Type=Menu, State=Default, `nav-item` → Type=Menu, State=Default, `nav-item` → Type=Menu, State=Default, `lang-switch` → Selected=First, `social` → Icon / tiktok, `social` → Icon / instagram, `social` → Icon / x, `social` → Icon / youtube
- **API:** `logo` (icon, por defecto Version=Negative) · `langSwitch` (boolean, por defecto false)
- **Nombres en Figma:** `logo` ← `Logo#55:6`, `langSwitch` ← `Lang switch#55:7`
- **Iconos / instancias anidadas:** sí · swap: `logo` · por defecto: Version=Negative · capas sin swap: social, social, social, social
- **Tokens que consume:** `border/width/thick`, `border/width/thin`, `button/inverse/bg`, `button/inverse/border`, `button/inverse/text`, `color/surface/inverse`, `color/text/on-inverse`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-s`, `font/line-height/desktop/caption`, `font/line-height/desktop/label`, `font/line-height/mobile/h2`, `font/size/desktop/body-s`, `font/size/desktop/caption`, `font/size/desktop/label`, `font/size/mobile/h2`, `font/style/body`, `font/style/display`, `icon-button/size/m`, `icon/color/inverse`, `icon/size/md`, `lang-switch/bg`, `lang-switch/bg-selected`, `lang-switch/border`, `lang-switch/text`, `lang-switch/text-selected`, `layout/frame`, `layout/margin`, `nav-item/menu-text`, `nav-item/menu-text-active`, `radius/pill`, `radius/sm`, `space/16`, `space/4`, `space/40`, `space/48`, `space/8`
- **Text styles:** `Mobile/h2`, `Desktop/label`, `Desktop/body-s`, `Desktop/caption`
<!-- ⚙️ GENERATED:end:mobile-menu -->

- **Propósito:** Menú a pantalla completa en todos los breakpoints (wireframe UX): navegación principal, redes de la marca y ©. Se abre desde el botón de menú de la Navbar.
- **Ejemplo de código:**
  ```html
  <dialog data-ds="mobile-menu" class="mobile-menu" id="menu" aria-label="Menú" open>
  <div class="mobile-menu__inner">
  <div class="mobile-menu__top">
  <img class="logo" src="../assets/logos/logo-yatekomo-negative.svg" alt="Yatekomo">
  <button class="icon-button icon-button--inverse" type="button" aria-label="Cerrar menú"><span class="icon icon-close" aria-hidden="true"></span></button>
  </div>
  <nav class="mobile-menu__nav" aria-label="Principal">
  <a class="nav-item nav-item--menu" href="/productos" aria-current="page">Products</a>
  <a class="nav-item nav-item--menu" href="/formula-natural">Natural formula</a>
  </nav>
  <div class="mobile-menu__social">
  <p class="mobile-menu__social-label">Our social media:</p>
  <ul class="mobile-menu__social-list"><li><a class="link link--dark" href="https://www.instagram.com/" aria-label="Instagram"><span class="icon icon-instagram" aria-hidden="true"></span></a></li></ul>
  </div>
  <p class="mobile-menu__copyright">© GBFoods</p>
  </div>
  </dialog>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** `<dialog>` modal: foco atrapado, Esc cierra y el foco vuelve al botón de menú. Ítems crema sobre tinta 17:1; el activo, amarillo con indicador (forma, no solo color). Cada red es un enlace con nombre.
- **Cuándo usar / qué NO hace:** Es la navegación principal en todos los breakpoints. No lleva CTA ni buscador.
