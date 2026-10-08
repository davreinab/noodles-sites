### Banner   ⚙️ synced: 2026-10-08T11:52:41Z

<!-- ⚙️ GENERATED:start:banner -->
- **Figma:** `92:884` · página «Pattern / Home» · COMPONENT_SET · 2 variantes · última sync 2026-10-08T11:52:41Z
- **Descripción (Figma):** Banner de campaña de la Home (wireframe UX): una pieza gráfica de campaña a todo el ancho del contenido, dentro de un marco con borde de tinta, radius/lg y elevation/2. La imagen lleva el mensaje; el banner entero es un enlace a la campaña y su texto alternativo repite lo que dice la pieza. Se oculta si no hay campaña. No es un carrusel. Sin variables propias.
- **Anatomía:** sin instancias anidadas
- **Breakpoint:** Desktop, Mobile
- **Propiedades de componente:** `Breakpoint` (VARIANT, por defecto Desktop)
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `border/width/thin`, `color/border/default`, `color/effect/shadow-ink`, `color/surface/page`, `color/text/secondary`, `font/family/body`, `font/line-height/desktop/caption`, `font/size/desktop/caption`, `font/style/body`, `layout/frame`, `layout/margin`, `layout/section-y`, `radius/lg`, `radius/none`, `space/16`, `space/48`
- **Text styles:** `Desktop/caption`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `color/border/default`, `color/effect/shadow-ink`, `color/surface/page`, `color/text/secondary`, `font/family/body`, `font/line-height/desktop/caption`, `font/size/desktop/caption`, `font/style/body`
<!-- ⚙️ GENERATED:end:banner -->

- **Propósito:** Banner de campaña de la Home (wireframe UX): una pieza gráfica a todo el ancho del contenido; el banner entero es el enlace a la campaña.
- **Ejemplo de código:**
  ```html
  <section class="section banner" aria-label="Campaña">
  <div class="section__inner">
  <a class="banner__box" href="/concursos/cucurella"><img src="/media/banner-campana.jpg" alt="Conoce a Marc Cucurella. Participa y podrás ganar más premios"></a>
  </div>
  </section>
  ```
- **Accesibilidad (pares AA verificados):** El texto alternativo repite lo que dice la pieza (la imagen lleva el mensaje). Marco con borde de tinta y foco visible en el enlace.
- **Cuándo usar / qué NO hace:** En la Home, solo con campaña activa; sin ella se oculta. No es un carrusel ni lleva texto HTML encima de la imagen.
