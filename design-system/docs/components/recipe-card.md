### Recipe card   ⚙️ synced: 2026-10-08T11:52:41Z

<!-- ⚙️ GENERATED:start:recipe-card -->
- **Figma:** `67:133` · página «Cards» · COMPONENT_SET · 3 variantes · última sync 2026-10-08T11:52:41Z
- **Descripción (Figma):** Card de receta (Recipe library, Home, página de producto). Anatomía (wireframe UX): media vertical 288:415 (imagen de marca; sin vídeo al principio) · tiempo (icono timer + texto, recipe-card/meta) · título (h3) · productos usados como Chip S (enlazan a la ficha de producto). Sin enlace «Ver receta»: el título es el enlace y su área se estira a toda la card; los Chip son enlaces propios y quedan por encima. Comensales: sin definir (falta información). Hover: elevation/2; Focus: anillo recipe-card/focus-ring. Desktop 384 px; en móvil FILL.
- **Anatomía:** `icon-time` → Icon / timer, `product-chip` → Size=S, State=Default, `icon-leading` → Icon / check, `product-chip` → Size=S, State=Default, `icon-leading` → Icon / check
- **State:** Default, Hover, Focus
- **Propiedades de componente:** `Title#67:0` (TEXT, por defecto Nombre de la receta), `Time#67:4` (TEXT, por defecto 10 min), `Time icon#67:8` (INSTANCE_SWAP, por defecto Icon / timer), `State` (VARIANT, por defecto Default)
- **Iconos / instancias anidadas:** sí · swap: `Time icon#67:8` · por defecto: Icon / timer
- **Tokens que consume:** `border/width/thin`, `chip/bg`, `chip/border`, `chip/height/s`, `chip/text`, `color/effect/shadow-ink`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-s`, `font/line-height/desktop/caption`, `font/line-height/desktop/h3`, `font/size/desktop/body-s`, `font/size/desktop/caption`, `font/size/desktop/h3`, `font/style/body`, `font/style/display`, `icon/size/sm`, `radius/md`, `radius/none`, `radius/pill`, `recipe-card/bg`, `recipe-card/border`, `recipe-card/media-bg`, `recipe-card/meta`, `recipe-card/title`, `space/16`, `space/24`, `space/8`
- **Text styles:** `Desktop/caption`, `Desktop/body-s`, `Desktop/h3`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `chip/bg`, `chip/border`, `chip/text`, `color/effect/shadow-ink`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-s`, `font/line-height/desktop/caption`, `font/line-height/desktop/h3`, `font/size/desktop/body-s`, `font/size/desktop/caption`, `font/size/desktop/h3`, `font/style/body`, `font/style/display`, `recipe-card/bg`, `recipe-card/border`, `recipe-card/media-bg`, `recipe-card/meta`, `recipe-card/title`
<!-- ⚙️ GENERATED:end:recipe-card -->

- **Propósito:** Card de receta (wireframe UX): imagen vertical, tiempo, título y productos usados. El título es el enlace a la receta y su área cubre toda la card.
- **Ejemplo de código:**
  ```html
  <article class="recipe-card">
  <div class="recipe-card__media"><img src="/media/receta.jpg" alt=""></div>
  <div class="recipe-card__body">
  <p class="recipe-card__meta"><span class="icon icon-timer" aria-hidden="true"></span>20 minutes</p>
  <h3 class="recipe-card__title"><a class="recipe-card__link" href="/recetas/spicy-noodle-salad">Spicy Noodle Salad with almond and mint</a></h3>
  <ul class="recipe-card__products" aria-label="Productos de la receta"><li><a class="chip" href="/productos/cup-oriental">Cup Oriental</a></li></ul>
  </div>
  </article>
  ```
- **Accesibilidad (pares AA verificados):** Título tinta sobre blanco 18:1; tiempo secundario 7,9:1. El enlace principal es el título (nombre accesible = nombre de la receta); los Chip son enlaces propios por encima del área estirada. Foco visible en toda la card con `:has()`.
- **Cuándo usar / qué NO hace:** En la Recipe library, la Home y la ficha de producto. Sin enlace «Ver receta». Comensales: sin definir, falta información.
