### Ingredient swap   ⚙️ synced: 2026-10-22T15:21:21Z

<!-- ⚙️ GENERATED:start:ingredient-swap -->
- **Figma:** `276:283` · página «Content» · COMPONENT · 1 variantes · última sync 2026-10-22T15:21:21Z
- **Descripción (Figma):** Ingredient swap: ingrediente retirado y su sustituto (Natural improvement → «Replaced ingredients»; wireframe UX 274:6354; clase CSS .ingredient-swap). Arriba la píldora tachada (Removed, mismo estilo que Removed tag, con «removed:» oculto), flecha chevron-down y debajo la tarjeta del sustituto: nombre en negrita en verde natural (text/natural, Archivo Bold 18/24, sin estilo de texto), motivo en Desktop/body-s y miniatura de 56 px (placeholder). Tarjeta: fondo blanco (surface/card) y borde verde natural (surface/natural); no hay variable opaca de superficie natural clara, así que no se usa verde claro. Props: Removed, Name, Reason. Ejemplos de ingredientes y motivos ⬜ TODO envase.
- **Anatomía:** `icon` → Icon / close, `arrow` → Icon / chevron-down
- **API:** `removed` (string, por defecto Palm oil) · `name` (string, por defecto Sunflower oil) · `reason` (string, por defecto Cold-pressed, no tropical deforestation footprint.)
- **Nombres en Figma:** `removed` ← `Removed#276:1`, `name` ← `Name#276:2`, `reason` ← `Reason#276:3`
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown · capas sin swap: icon, arrow
- **Tokens que consume:** `color/border/subtle`, `color/surface/card`, `color/surface/natural`, `color/surface/page`, `color/text/default`, `color/text/natural`, `color/text/secondary`, `font/family/body`, `font/line-height/desktop/body-s`, `font/size/desktop/body-s`, `font/style/body`, `icon/color/default`, `icon/size/md`, `radius/md`, `radius/pill`, `radius/sm`, `space/16`, `space/8`
- **Text styles:** `Desktop/body-s`
<!-- ⚙️ GENERATED:end:ingredient-swap -->

- **Propósito:** Muestra un cambio de ingrediente: arriba el ingrediente retirado (Removed tag), una flecha hacia abajo y debajo la tarjeta del sustituto, con su nombre en verde natural, el motivo y una miniatura. Props del maestro: Removed, Name, Reason.
- **Ejemplo de código:**
  ```html
  <li data-ds="ingredient-swap" class="ingredient-swap"><span class="removed-tag"><span class="icon icon-close" aria-hidden="true"></span><span class="visually-hidden">Removed:</span><s class="removed-tag__text">Palm oil</s></span><span class="icon icon-chevron-down ingredient-swap__arrow" aria-hidden="true"></span><div class="ingredient-swap__card"><div class="ingredient-swap__text"><p class="ingredient-swap__name">Sunflower oil</p><p class="ingredient-swap__reason">Cold-pressed, no tropical deforestation footprint.</p></div><img class="ingredient-swap__thumb" src="../assets/images/placeholder.svg" alt=""></div></li>
  ```
  Va dentro de `<ul class="natural-improvement__swaps">`. Desktop: cuatro en fila. Mobile: una columna (la rejilla de Natural improvement lo resuelve sola, sin cambiar el marcado).
- **Accesibilidad (rol, nombre, estados y teclado):** Es un `li` de la lista de reemplazos. Se lee en orden: ingrediente retirado (con «Removed:» oculto), nombre del sustituto, motivo. La flecha va con `aria-hidden`: es solo dirección. La miniatura es decorativa (`alt=""`) porque el nombre y el motivo ya dicen el cambio. No es interactivo: no hay foco ni teclado. Contrastes: nombre en verde natural sobre blanco (el token documenta 5,0:1 sobre crema y sobre blanco es algo mayor); motivo en gris cálido sobre blanco (5,4:1).
- **Cuándo usar / qué NO hace:** Solo en Natural improvement, para explicar qué sustituye a qué. No es un selector ni una comparativa de nutrientes. Los nombres, motivos e ingredientes son de ejemplo: ⬜ TODO envase (deben coincidir con la fórmula validada). La miniatura es un placeholder hasta tener foto del ingrediente.
