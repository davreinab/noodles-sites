### Prize card   ⚙️ synced: 2026-10-23T09:22:57Z

<!-- ⚙️ GENERATED:start:prize-card -->
- **Figma:** `308:2303` · página «Cards» · COMPONENT_SET · 2 variantes · última sync 2026-10-23T09:22:57Z
- **Descripción (Figma):** Prize card: premio del concurso (Contest page, bloque Contest prizes). Anatomía (wireframe UX): media 4:3 · nivel en caption (Level: «Grand prize», «Featured prize», «Weekly prize · x50») · nombre h3 (Name) · descripción body-m (Description). Variant=Grand: cuerpo en surface/inverse con texto on-inverse y nivel en brand-on-inverse. Variant=Default: cuerpo en surface/card. Clase CSS: .prize-card (Grand añade .prize-card--grand). ⬜ TODO GB Foods/agencia: nombres, descripciones e imágenes reales de los premios.
- **Anatomía:** sin instancias anidadas
- **API:** `level` (string, por defecto Grand prize) · `name` (string, por defecto Prize name) · `description` (string, por defecto Prize description) · `variant`: Grand, Default (por defecto Grand)
- **Nombres en Figma:** `level` ← `Level#308:3`, `name` ← `Name#308:6`, `description` ← `Description#308:9`, `variant` ← `Variant`
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `color/border/default`, `color/surface/inverse`, `color/text/brand-on-inverse`, `color/text/on-inverse`, `contest-card/media-bg`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/desktop/h3`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/desktop/h3`, `font/style/body`, `font/style/display`, `radius/md`, `space/24`, `space/8`
- **Text styles:** `Desktop/caption`, `Desktop/h3`, `Desktop/body-m`
<!-- ⚙️ GENERATED:end:prize-card -->

- **Propósito:** Un premio del concurso: imagen 4:3, nivel del premio (caption), nombre (h3) y descripción. Dos variantes: Default (cuerpo blanco) y Grand (`.prize-card--grand`, cuerpo en tinta con textos claros y el nivel en amarillo de marca), para el gran premio.
- **Ejemplo de código:** Default y Grand en el mismo bloque. Grand cambia el cuerpo a tinta y el texto a crema (`.prize-card--grand`).
  ```html
  <article data-ds="prize-card" class="prize-card">
  <div class="prize-card__media"><img src="../assets/images/placeholder.svg" alt=""></div>
  <div class="prize-card__body">
  <p class="prize-card__level">Featured prize</p>
  <h3 class="prize-card__title">Home ramen kit</h3>
  <p class="prize-card__text">Professional-grade bowls, a chopstick set and a full year of your favourite flavours.</p>
  </div>
  </article>
  <article data-ds="prize-card" class="prize-card prize-card--grand">
  <div class="prize-card__media"><img src="../assets/images/placeholder.svg" alt=""></div>
  <div class="prize-card__body">
  <p class="prize-card__level">Grand prize</p>
  <h3 class="prize-card__title">Festival weekend for two</h3>
  <p class="prize-card__text">Two festival weekend passes, travel budget and backstage access to this year's festival partner.</p>
  </div>
  </article>
  ```
  Va dentro de `<ul class="contest-prizes__list">` (una `li` por premio).
- **Accesibilidad (rol, nombre, estados y teclado):** Rol: `article` con un `h3`. La imagen es decorativa (`alt` vacío): el nombre del premio ya está en el texto. El nivel se dice con palabras («Grand prize», «Featured prize», «Weekly prize · x50»), no con el color. Contrastes: Default, gris cálido sobre blanco (5,4:1) y tinta sobre blanco; Grand, amarillo de marca sobre tinta (12:1) y crema sobre tinta (17:1). No es interactivo: no hay foco.
- **Cuándo usar / qué NO hace:** Solo en Contest prizes. El wireframe marca el gran premio con Grand; el resto, Default. No es una tarjeta de producto ni de receta, no tiene precio ni enlace. Los nombres, niveles, descripciones y número de premios son ⬜ TODO: los confirma GB Foods con la agencia (premios y cantidades son condiciones del concurso).
