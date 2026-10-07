### Recipe card   ⚙️ synced: 2026-10-07T18:30:51Z

<!-- ⚙️ GENERATED:start:recipe-card -->
- **Figma:** `67:133` · página «Recipe card» · COMPONENT_SET · 3 variantes · última sync 2026-10-07T18:30:51Z
- **Descripción (Figma):** Card de receta (Recipe library, Home, página de producto). Anatomía: media (imagen de marca; sin vídeo al principio) · título (h3) · tiempo (icono timer + texto, recipe-card/meta) · productos usados como Chip S (enlazan a la ficha de producto) · Link «Ver receta». La card enlaza a la receta; los Chip son enlaces propios y quedan fuera del área clicable principal. Hover: elevation/2; Focus: anillo recipe-card/focus-ring. Desktop 384 px; en móvil FILL.
- **Anatomía:** `icon-time` → Icon / timer, `product-chip` → Size=S, State=Default, `icon-leading` → Icon / check, `product-chip` → Size=S, State=Default, `icon-leading` → Icon / check, `link` → Type=Standalone, Surface=Light, State=Default, `icon-trailing` → Icon / arrow-right
- **State:** Default, Hover, Focus
- **Propiedades de componente:** `Title#67:0` (TEXT, por defecto Nombre de la receta), `Time#67:4` (TEXT, por defecto 10 min), `Time icon#67:8` (INSTANCE_SWAP, por defecto Icon / timer), `State` (VARIANT, por defecto Default)
- **Iconos / instancias anidadas:** sí · swap: `Time icon#67:8` · por defecto: Icon / timer
- **Tokens que consume:** `border/width/thin`, `chip/bg`, `chip/border`, `chip/height/s`, `chip/text`, `color/effect/shadow-ink`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-s`, `font/line-height/desktop/caption`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/size/desktop/body-s`, `font/size/desktop/caption`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/sm`, `link/default`, `radius/md`, `radius/none`, `radius/pill`, `recipe-card/bg`, `recipe-card/border`, `recipe-card/media-bg`, `recipe-card/meta`, `recipe-card/title`, `space/16`, `space/24`, `space/8`
- **Text styles:** `Desktop/caption`, `Desktop/h3`, `Desktop/body-s`, `Desktop/label`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `chip/bg`, `chip/border`, `chip/text`, `color/effect/shadow-ink`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-s`, `font/line-height/desktop/caption`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/size/desktop/body-s`, `font/size/desktop/caption`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `link/default`, `recipe-card/bg`, `recipe-card/border`, `recipe-card/media-bg`, `recipe-card/meta`, `recipe-card/title`
<!-- ⚙️ GENERATED:end:recipe-card -->

- **Propósito:** Card de receta: imagen, título, tiempo y productos usados. El título es el enlace a la receta y se estira a toda la card; los productos son enlaces propios.
- **Ejemplo de código:**
  ```html
  <article class="recipe-card">
  <div class="recipe-card__media"><img src="/media/receta-ramen.jpg" alt=""></div>
  <div class="recipe-card__body">
  <h3 class="recipe-card__title"><a class="recipe-card__link" href="/recetas/ramen-picante">Ramen picante</a></h3>
  <p class="recipe-card__meta"><span class="icon icon-timer" aria-hidden="true"></span>10 min</p>
  <ul class="recipe-card__products" aria-label="Productos de la receta">
  <li><a class="chip" href="/productos/yatekomo-pollo">Yatekomo Pollo</a></li>
  </ul>
  <span class="link link--standalone" aria-hidden="true">Ver receta <span class="icon icon-arrow-right"></span></span>
  </div>
  </article>
  ```
- **Accesibilidad (pares AA verificados):** Título tinta sobre blanco 18,7:1; tiempo gris cálido sobre blanco 5,9:1; chips con sus propios pares (ver Chip). Rol: `<article>` con un enlace principal en el título (patrón de enlace estirado: `::after` cubre la card) y los chips por encima (`z-index` raised) como enlaces independientes; «Ver receta» es visual (`aria-hidden`) porque repetiría el título. Teclado: el título y cada chip son paradas de tabulador. Foco: cuando el título tiene foco, el contorno de 2 px rodea la card entera (`:has`).
- **Cuándo usar / qué NO hace:** En la Recipe library, la Home y la página de producto. No se usa para productos (Product card) ni para concursos (Contest card). Sin vídeo en la card.
