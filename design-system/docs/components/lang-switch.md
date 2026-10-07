### Lang switch   ⚙️ synced: 2026-10-07T18:19:35Z

<!-- ⚙️ GENERATED:start:lang-switch -->
- **Figma:** `54:71` · página «Lang switch» · COMPONENT_SET · 2 variantes · última sync 2026-10-07T18:19:35Z
- **Descripción (Figma):** Selector de idioma de dos opciones (p. ej. NL | FR en Aiki). Solo en marcas multiidioma. La opción activa en tinta. En código: enlaces a la versión de idioma con hreflang y aria-current en la activa; cada opción con lang=&quot;nl&quot;/&quot;fr&quot;.
- **Anatomía:** sin instancias anidadas
- **Selected:** First, Second
- **Propiedades de componente:** `First label#54:5` (TEXT, por defecto NL), `Second label#54:8` (TEXT, por defecto FR), `Selected` (VARIANT, por defecto First)
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `border/width/thin`, `font/family/display`, `font/line-height/desktop/label`, `font/size/desktop/label`, `font/style/display`, `lang-switch/bg`, `lang-switch/bg-selected`, `lang-switch/border`, `lang-switch/text`, `lang-switch/text-selected`, `radius/pill`, `space/16`, `space/4`, `space/8`
- **Text styles:** `Desktop/label`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `font/family/display`, `font/line-height/desktop/label`, `font/size/desktop/label`, `font/style/display`, `lang-switch/bg`, `lang-switch/bg-selected`, `lang-switch/border`, `lang-switch/text`, `lang-switch/text-selected`
<!-- ⚙️ GENERATED:end:lang-switch -->

- **Propósito:** Selector de idioma de dos opciones (NL | FR) para las marcas multiidioma, como Aïki en Bélgica. Va en la Navbar y en el Mobile menu.
- **Ejemplo de código:**
  ```html
  <nav class="lang-switch" aria-label="Idioma">
  <a class="lang-switch__option" href="/nl/" hreflang="nl" lang="nl" aria-current="true">NL</a>
  <a class="lang-switch__option" href="/fr/" hreflang="fr" lang="fr">FR</a>
  </nav>
  ```
- **Accesibilidad (pares AA verificados):** Reposo: tinta sobre blanco 18,7:1; seleccionado: crema sobre tinta 17,2:1 y `aria-current`, así que no depende solo del color. Rol: dos enlaces a la versión de la página en cada idioma, con `hreflang` y `lang`; nombre accesible del grupo «Idioma». Foco: contorno de 2 px pegado. Alto de 40 px (32 de opción + 4 de marco): por debajo de 44, compensado por la separación con los vecinos (≥ 24 px).
- **Cuándo usar / qué NO hace:** Solo en marcas con dos idiomas. Cambia de idioma conservando la página; no es un desplegable de países ni se muestra en marcas monolingües.
