### Stat figure   ⚙️ synced: 2026-10-22T15:21:21Z

<!-- ⚙️ GENERATED:start:stat-figure -->
- **Figma:** `277:325` · página «Content» · COMPONENT · 1 variantes · última sync 2026-10-22T15:21:21Z
- **Descripción (Figma):** Stat figure: cifra destacada con marcador tipo <mark> (clase CSS .stat-figure; wireframe UX 274:6354, módulo Natural stats). Cifra en Desktop/h2 (Anton) sobre bloque amarillo de marca (surface/brand) con texto en tinta (text/default, contraste ~12:1); el marcador lleva relleno de space/2 vertical y space/8 horizontal (la landing usa 2px 10px; 10 px no existe como variable, se usa space/8). Etiqueta en Desktop/body-s en text/on-inverse sobre el fondo tinta del patrón. Cifras de ejemplo ⬜ TODO envase (-45%, +5g, +20g, 100%). Props: Figure, Label.
- **Anatomía:** sin instancias anidadas
- **API:** `figure` (string, por defecto -45%) · `label` (string, por defecto Less processed ingredients)
- **Nombres en Figma:** `figure` ← `Figure#277:75`, `label` ← `Label#277:76`
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `color/surface/brand`, `color/text/default`, `color/text/on-inverse`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-s`, `font/line-height/desktop/h2`, `font/size/desktop/body-s`, `font/size/desktop/h2`, `font/style/body`, `font/style/display`, `space/2`, `space/8`
- **Text styles:** `Desktop/body-s`
<!-- ⚙️ GENERATED:end:stat-figure -->

- **Propósito:** Una cifra destacada (−45 %, +5 g, +20 g, 100 %) con marcador amarillo de marca detrás y su etiqueta debajo, sobre fondo tinta. Es la pieza de Natural stats.
- **Ejemplo de código:**
  ```html
  <li data-ds="stat-figure" class="stat-figure"><mark class="stat-figure__value">-45%</mark><span class="stat-figure__label">Less processed ingredients</span></li>
  ```
  Va dentro de `<ul class="natural-stats__list">`. Desktop: cuatro en fila. Mobile: dos columnas (2 × 2), por la misma rejilla del patrón.
- **Accesibilidad (rol, nombre, estados y teclado):** Es un `li`. La cifra y la etiqueta son texto y se leen en ese orden («-45% Less processed ingredients»). El `mark` es solo el marcador visual de la landing; el significado está en el texto, no en el color ni en el resaltado. El texto no se transforma: `text-transform: none` evita que «+5g» se lea distinto. Contrastes: tinta sobre amarillo de marca (12,3:1, token documentado); etiqueta en crema sobre tinta (17:1). No es interactivo.
- **Cuándo usar / qué NO hace:** Solo en Natural stats, con cifras de la fórmula. Las cifras (−45 %, +5 g, +20 g, 100 %) y sus etiquetas son ⬜ TODO envase: deben coincidir con la tabla nutricional y con la norma de claims; no se redondean ni se inventan. No sustituye a Nutrition label ni a Nutrition ring.
