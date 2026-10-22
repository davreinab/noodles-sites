### Recipe card   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:recipe-card -->
- **Figma:** `67:133` · página «Cards» · COMPONENT_SET · 3 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** Card de receta (Recipe library, Home, página de producto). Anatomía (wireframe UX): media vertical 4:5 (380×475, imagen de marca; sin vídeo al principio) · meta encima del nombre: People («2 people») · icono timer + Time («20 minutes») · nombre de la receta (h3, Title) · chips de producto Chip S (enlazan a la ficha; ejemplo «Cup Oriental», «Sauce Sesame»). Hover: elevation; Focus: anillo. Clase CSS: .recipe-card. Uso: Recipe library (wireframe 171:3808 y estados 483:5711 / 485:6064).
- **Anatomía:** `icon-time` → Icon / timer, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check
- **API:** `title` (string, por defecto Recipe name) · `time` (string, por defecto 20 minutes) · `timeIcon` (icon, por defecto Icon / timer) · `people` (string, por defecto 2 people)
- **Estados de CSS:** Hover, Focus
- **Nombres en Figma:** `title` ← `Title#67:0`, `time` ← `Time#67:4`, `timeIcon` ← `Time icon#67:8`, `people` ← `People#219:0`
- **Iconos / instancias anidadas:** sí · swap: `timeIcon` · por defecto: Icon / timer
- **Tokens que consume:** `border/width/thin`, `chip/bg`, `chip/border`, `chip/height/s`, `chip/text`, `color/effect/shadow-ink`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-s`, `font/line-height/desktop/caption`, `font/line-height/desktop/h3`, `font/size/desktop/body-s`, `font/size/desktop/caption`, `font/size/desktop/h3`, `font/style/body`, `font/style/display`, `icon/size/sm`, `radius/md`, `radius/none`, `radius/pill`, `recipe-card/bg`, `recipe-card/border`, `recipe-card/media-bg`, `recipe-card/meta`, `recipe-card/title`, `space/16`, `space/24`, `space/8`
- **Text styles:** `Desktop/caption`, `Desktop/body-s`, `Desktop/h3`
<!-- ⚙️ GENERATED:end:recipe-card -->

- **Propósito:** Card de receta (Recipe library, Home y ficha de producto): imagen vertical 4:5; encima del nombre, la meta «2 people · 20 minutes» con icono timer; el nombre de la receta es el enlace y su área cubre toda la card; los productos usados van como chips pequeños con enlace propio por encima.
- **Ejemplo de código:**
  ```html
  <article data-ds="recipe-card" class="recipe-card">
  <div class="recipe-card__media"><img src="../assets/images/placeholder.svg" alt=""></div>
  <div class="recipe-card__body">
  <p class="recipe-card__meta">2 people · <span class="icon icon-timer" aria-hidden="true"></span>20 minutes</p>
  <h3 class="recipe-card__title"><a class="recipe-card__link" href="/recetas/spicy-noodle-salad">Spicy Noodle Salad with almond and mint</a></h3>
  <ul class="recipe-card__products" aria-label="Products used in this recipe"><li><a class="chip" href="/productos/cup-oriental">Cup Oriental</a></li></ul>
  </div>
  </article>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Título tinta sobre blanco 18:1; tiempo secundario 7,9:1. El enlace principal es el título (nombre accesible = nombre de la receta); los Chip son enlaces propios por encima del área estirada. Foco visible en toda la card con `:has()`.
- **Cuándo usar / qué NO hace:** En la Recipe library, la Home y la ficha de producto. Sin enlace «Ver receta». Comensales: sin definir, falta información.
