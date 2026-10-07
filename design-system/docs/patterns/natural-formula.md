### Natural formula   ⚙️ synced: 2026-10-07T18:43:11Z

<!-- ⚙️ GENERATED:start:natural-formula -->
- **Figma:** `91:704` · página «Pattern / Natural formula» · COMPONENT_SET · 2 variantes · última sync 2026-10-07T18:43:11Z
- **Descripción (Figma):** Sección de la fórmula natural (Home): título (h2) · texto · 4 claims del pack en display (100 % natural · −20 % sal · −80 % grasas saturadas · 0 aditivos ni conservantes) · Link Standalone Dark a la Natural formula page. Fondo color/surface/natural con texto color/text/on-natural (5,5:1, también en display). Los claims deben coincidir con el envase (restricción regulatoria): no se añaden claims nuevos sin validación de GB Foods. Los claims son una lista (&lt;ul&gt;), no encabezados. Desktop: 4 columnas; Mobile: 2×2. Sin variables propias.
- **Anatomía:** `link` → Type=Standalone, Surface=Dark, State=Default, `icon-trailing` → Icon / arrow-right
- **Breakpoint:** Desktop, Mobile
- **Propiedades de componente:** `Breakpoint` (VARIANT, por defecto Desktop)
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `color/surface/natural`, `color/text/on-natural`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/display`, `font/line-height/desktop/h2`, `font/line-height/desktop/label`, `font/size/desktop/body-l`, `font/size/desktop/display`, `font/size/desktop/h2`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/sm`, `layout/frame`, `layout/gutter`, `layout/margin`, `layout/section-y`, `link/inverse`, `space/16`, `space/32`, `space/48`, `space/8`
- **Text styles:** `Desktop/h2`, `Desktop/body-l`, `Desktop/display`, `Desktop/label`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `color/surface/natural`, `color/text/on-natural`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/display`, `font/line-height/desktop/h2`, `font/line-height/desktop/label`, `font/size/desktop/body-l`, `font/size/desktop/display`, `font/size/desktop/h2`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `link/inverse`
<!-- ⚙️ GENERATED:end:natural-formula -->

- **Propósito:** Sección de la fórmula natural de la Home: los claims del envase en grande sobre verde y enlace a la página de naturalidad.
- **Ejemplo de código:**
  ```html
  <section class="section natural-formula" aria-labelledby="nf-title">
  <div class="section__inner">
  <div class="section__header"><h2 class="section__title" id="nf-title">La fórmula natural</h2><p class="section__lead">Texto alineado con el envase.</p></div>
  <ul class="natural-formula__claims">
  <li class="natural-formula__claim"><span class="natural-formula__value">100 %</span><span class="natural-formula__label">natural</span></li>
  <li class="natural-formula__claim"><span class="natural-formula__value">−20 %</span><span class="natural-formula__label">de sal</span></li>
  </ul>
  <a class="link link--standalone link--dark" href="/formula-natural">Conoce la fórmula natural <span class="icon icon-arrow-right" aria-hidden="true"></span></a>
  </div>
  </section>
  ```
- **Accesibilidad (pares AA verificados):** Blanco sobre verde natural 5,5:1 en todos los tamaños; enlace crema sobre verde 5,0:1. Los claims son una lista (`<ul>`), no encabezados; cada uno se lee como «100 % natural».
- **Cuándo usar / qué NO hace:** En la Home. Los claims deben coincidir con el envase (restricción regulatoria): no se añaden sin validación de GB Foods.
