### Community card   ⚙️ synced: 2026-10-23T09:22:57Z

<!-- ⚙️ GENERATED:start:community-card -->
- **Figma:** `308:2304` · página «Cards» · COMPONENT · 1 variantes · última sync 2026-10-23T09:22:57Z
- **Descripción (Figma):** Community card: foto de la comunidad (ganadores o participantes) con pie «@usuario · producto» en caption. Usos: Contest community (wireframe 330:6557, bloque Real moments / Shared by the community, fila desplazable). Clase CSS: .community-card. ⬜ TODO GB Foods/agencia: fotos y usuarios reales con permiso de publicación.
- **Anatomía:** sin instancias anidadas
- **API:** `caption` (string, por defecto @user · Home Ramen Kit unboxing)
- **Nombres en Figma:** `caption` ← `Caption#308:12`
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `color/border/default`, `color/surface/card`, `color/text/secondary`, `contest-card/media-bg`, `font/family/body`, `font/line-height/desktop/caption`, `font/size/desktop/caption`, `font/style/body`, `radius/md`, `space/16`, `space/8`
- **Text styles:** `Desktop/caption`
<!-- ⚙️ GENERATED:end:community-card -->

- **Propósito:** Foto de la comunidad con su pie de autoría (por ejemplo «@user2 · Home Ramen Kit unboxing»). Es una figura con pie (`figure` y `figcaption`) y no es un enlace.
- **Ejemplo de código:**
  ```html
  <figure data-ds="community-card" class="community-card">
  <div class="community-card__media"><img src="../assets/images/placeholder.svg" alt=""></div>
  <figcaption class="community-card__caption">@user2 · Home Ramen Kit unboxing</figcaption>
  </figure>
  ```
  Va dentro de `<ul class="contest-community__list">`, con una `li` por foto.
- **Accesibilidad (rol, nombre, estados y teclado):** Rol: `figure` con `figcaption`: el pie es su nombre. La imagen es decorativa (`alt` vacío) porque el pie dice quién la comparte y de qué va; si una foto necesitara descripción propia, se escribe en `alt`. No es interactivo: no tiene foco. Contraste: texto tinta sobre blanco.
- **Cuándo usar / qué NO hace:** Solo en Contest community. No es un enlace a la publicación original: si se quisiera enlazar, habría que añadirlo como un componente nuevo. Las fotos y los nombres de usuario son ⬜ TODO: hay que tener el permiso de uso de cada autor antes de publicarlas (es una condición de imagen, no de diseño).
