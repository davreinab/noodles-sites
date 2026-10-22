### Navbar   ⚙️ synced: 2026-10-22T09:37:04Z

<!-- ⚙️ GENERATED:start:navbar -->
- **Figma:** `55:116` · página «Pattern / Global» · COMPONENT_SET · 2 variantes · última sync 2026-10-22T09:37:04Z
- **Descripción (Figma):** Patrón de cabecera (wireframe UX). Desktop: botón menú (Icon button Secondary, abre el Menu a pantalla completa) a la izquierda · logo de marca centrado (enlace a la Home) · CTA Button Primary «New 100% Natural Formula» a la derecha (lleva a la Natural formula page) · Lang switch oculto salvo en marcas multiidioma. Mobile: botón menú · logo centrado. Sin enlaces de navegación ni buscador en la barra: la navegación vive en el Menu. Comportamiento: sticky (layer/sticky); se oculta al hacer scroll hacia abajo y reaparece al subir; respeta prefers-reduced-motion. Accesibilidad: <header> con <nav>; el botón menú lleva aria-expanded y aria-controls. Fondo color/surface/page con borde inferior color/border/default. Sin variables propias.
- **Anatomía:** `menu` → Hierarchy=Secondary, Size=M, State=Default, `icon` → Icon / menu, `logo` → Version=Positive, `lang-switch` → Selected=First, `cta` → Hierarchy=Primary, Size=M, State=Default, `icon-leading` → Icon / arrow-right, `icon-trailing` → Icon / arrow-right
- **API:** `logo` (icon, por defecto Version=Positive) · `langSwitch` (boolean, por defecto false) · `breakpoint`: Desktop, Mobile (por defecto Desktop)
- **Nombres en Figma:** `logo` ← `Logo#55:0`, `langSwitch` ← `Lang switch#55:3`, `breakpoint` ← `Breakpoint`
- **Iconos / instancias anidadas:** sí · swap: `logo` · por defecto: Version=Positive
- **Tokens que consume:** `border/width/thick`, `border/width/thin`, `button/primary/bg`, `button/primary/border`, `button/primary/text`, `button/secondary/border`, `button/secondary/text`, `color/border/default`, `color/surface/page`, `font/family/display`, `font/line-height/desktop/label`, `font/size/desktop/label`, `font/style/display`, `icon-button/size/m`, `icon/color/default`, `icon/size/md`, `icon/size/sm`, `lang-switch/bg`, `lang-switch/bg-selected`, `lang-switch/border`, `lang-switch/text`, `lang-switch/text-selected`, `layout/frame`, `layout/margin`, `radius/pill`, `space/16`, `space/24`, `space/4`, `space/8`
- **Text styles:** `Desktop/label`
<!-- ⚙️ GENERATED:end:navbar -->

- **Propósito:** Cabecera de todas las páginas (wireframe UX): botón de menú a la izquierda, logo de marca centrado y, en desktop, el CTA «New 100% Natural Formula». La navegación vive en el menú a pantalla completa.
- **Ejemplo de código:**
  ```html
  <header data-ds="navbar" class="navbar">
  <div class="navbar__inner">
  <div class="navbar__start"><button class="icon-button icon-button--secondary" type="button" aria-label="Menú" aria-expanded="false" aria-controls="menu"><span class="icon icon-menu" aria-hidden="true"></span></button></div>
  <a href="/" aria-label="Yatekomo, inicio"><img class="logo" src="../assets/logos/logo-yatekomo-positive.svg" alt="Yatekomo"></a>
  <div class="navbar__actions"><a class="button" href="/formula-natural">New 100% Natural Formula</a></div>
  </div>
  </header>
  <header data-ds="navbar" class="navbar">
  <div class="navbar__inner">
  <div class="navbar__start"><button class="icon-button icon-button--secondary" type="button" aria-label="Menú" aria-expanded="false" aria-controls="menu"><span class="icon icon-menu" aria-hidden="true"></span></button></div>
  <a href="/" aria-label="Yatekomo, inicio"><img class="logo" src="../assets/logos/logo-yatekomo-positive.svg" alt="Yatekomo"></a>
  <div class="navbar__actions"><a class="button" href="/formula-natural">New 100% Natural Formula</a><nav data-ds="lang-switch" class="lang-switch" aria-label="Idioma"><a class="lang-switch__option" href="/nl/" hreflang="nl" lang="nl" aria-current="true">NL</a><a class="lang-switch__option" href="/fr/" hreflang="fr" lang="fr">FR</a></nav></div>
  </div>
  </header>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Botón de menú con nombre accesible, `aria-expanded` y `aria-controls`; el logo es el enlace a la Home con nombre «Marca, inicio». Tinta sobre crema 17,2:1. Sticky (`--layer-sticky`); se oculta al bajar y reaparece al subir, sin animación con reduce-motion.
- **Cuándo usar / qué NO hace:** En todas las páginas. Solo marcas multiidioma muestran el Lang switch (en `.navbar__actions`). No lleva enlaces de navegación ni buscador: van en el Mobile menu.
