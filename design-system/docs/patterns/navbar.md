### Navbar   ⚙️ synced: 2026-10-07T18:30:51Z

<!-- ⚙️ GENERATED:start:navbar -->
- **Figma:** `55:116` · página «Pattern / Navbar» · COMPONENT_SET · 2 variantes · última sync 2026-10-07T18:30:51Z
- **Descripción (Figma):** Patrón de cabecera. Desktop: logo · 5 Nav item (Bar) · Lang switch (solo marcas multiidioma) · buscar · CTA «Dónde comprar». Mobile: logo · buscar · menú (abre Mobile menu). Comportamiento: sticky (layer/sticky); se oculta al hacer scroll hacia abajo y reaparece al subir; respeta prefers-reduced-motion. Ancho ligado a layout/frame con modo fijado por variante. Sin variables propias: compone componentes y semánticos.
- **Anatomía:** `logo` → Version=Positive, `nav-item` → Type=Bar, State=Active, `nav-item` → Type=Bar, State=Default, `nav-item` → Type=Bar, State=Default, `nav-item` → Type=Bar, State=Default, `nav-item` → Type=Bar, State=Default, `lang-switch` → Selected=First, `search` → Hierarchy=Secondary, Size=M, State=Default, `icon` → Icon / search, `cta` → Hierarchy=Primary, Size=M, State=Default, `icon-leading` → Icon / arrow-right, `icon-trailing` → Icon / arrow-right
- **Breakpoint:** Desktop, Mobile
- **Propiedades de componente:** `Logo#55:0` (INSTANCE_SWAP, por defecto Version=Positive), `Lang switch#55:3` (BOOLEAN, por defecto False), `Breakpoint` (VARIANT, por defecto Desktop)
- **Iconos / instancias anidadas:** sí · swap: `Logo#55:0` · por defecto: Version=Positive
- **Tokens que consume:** `border/width/thick`, `border/width/thin`, `button/primary/bg`, `button/primary/border`, `button/primary/text`, `button/secondary/border`, `button/secondary/text`, `color/border/default`, `color/surface/page`, `font/family/display`, `font/line-height/desktop/label`, `font/size/desktop/label`, `font/style/display`, `icon/size/md`, `icon/size/sm`, `lang-switch/bg`, `lang-switch/bg-selected`, `lang-switch/border`, `lang-switch/text`, `lang-switch/text-selected`, `layout/frame`, `layout/margin`, `nav-item/indicator`, `nav-item/text`, `nav-item/text-active`, `radius/pill`, `radius/sm`, `space/16`, `space/24`, `space/4`, `space/8`
- **Text styles:** `Desktop/label`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `button/primary/bg`, `button/primary/border`, `button/primary/text`, `button/secondary/border`, `button/secondary/text`, `color/border/default`, `color/surface/page`, `font/family/display`, `font/line-height/desktop/label`, `font/size/desktop/label`, `font/style/display`, `lang-switch/bg`, `lang-switch/bg-selected`, `lang-switch/border`, `lang-switch/text`, `lang-switch/text-selected`, `nav-item/indicator`, `nav-item/text`, `nav-item/text-active`
<!-- ⚙️ GENERATED:end:navbar -->

- **Propósito:** Cabecera de todas las páginas: logo, navegación principal, idioma (solo marcas multiidioma), buscar y «Dónde comprar». En móvil, logo, buscar y menú.
- **Ejemplo de código:**
  ```html
  <header class="navbar">
  <div class="navbar__inner">
  <a href="/" aria-label="Yatekomo, inicio"><img class="logo" src="../assets/logos/logo-yatekomo-positive.svg" alt="Yatekomo"></a>
  <nav class="navbar__nav" aria-label="Principal">
  <a class="nav-item" href="/productos" aria-current="page">Productos</a>
  <a class="nav-item" href="/recetas">Recetas</a>
  </nav>
  <div class="navbar__actions">
  <nav class="lang-switch" aria-label="Idioma"><a class="lang-switch__option" href="/nl/" aria-current="true">NL</a><a class="lang-switch__option" href="/fr/">FR</a></nav>
  <button class="icon-button icon-button--secondary" type="button" aria-label="Buscar"><span class="icon icon-search" aria-hidden="true"></span></button>
  <a class="button" href="#donde-comprar">Dónde comprar</a>
  <button class="icon-button icon-button--secondary navbar__menu-button" type="button" aria-label="Menú" aria-expanded="false" aria-controls="menu"><span class="icon icon-menu" aria-hidden="true"></span></button>
  </div>
  </div>
  </header>
  ```
- **Accesibilidad (pares AA verificados):** Fondo crema con borde inferior de tinta; los pares son los de sus componentes (Nav item 17,2:1, botones). Landmark `<header>` con `<nav aria-label="Principal">`; el logo enlaza a la Home con nombre de marca. Se oculta al bajar y reaparece al subir (`.navbar--hidden`), pero nunca mientras tenga el foco dentro; con reduce-motion no se anima. El botón de menú lleva `aria-expanded` y abre el Mobile menu. Un enlace «Saltar al contenido» la precede.
- **Cuándo usar / qué NO hace:** Una por página, siempre arriba (`--layer-sticky`). No lleva más de cinco secciones ni submenús desplegables. El Lang switch solo aparece en marcas multiidioma.
