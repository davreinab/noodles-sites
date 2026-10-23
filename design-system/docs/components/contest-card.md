### Contest card   ⚙️ synced: 2026-10-23T09:22:57Z

<!-- ⚙️ GENERATED:start:contest-card -->
- **Figma:** `68:95` · página «Cards» · COMPONENT_SET · 2 variantes · última sync 2026-10-23T09:22:57Z
- **Descripción (Figma):** Card de concurso (Contest library y Home). Anatomía (wireframe UX): imagen cuadrada 384 (radius md) · en Status=Closed, Badge Neutral «Closed» sobre la imagen · caption «Available until» (Status=Active) o «Ended on» (Status=Closed) con la propiedad Dates · nombre del concurso h3 de 2 líneas con la propiedad Title · chips S de premios (T-shirts, Balls, Experience). Toda la tarjeta es un enlace: sin botones «Participar» ni «Bases legales». Clase CSS: .contest-card. ⬜ TODO GB Foods/agencia: texto de los premios y fecha de cierre reales; mecánica de límite de participaciones pendiente de confirmar.
- **Anatomía:** `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check, `Chip` → Size=S, State=Default, `icon-leading` → Icon / check
- **API:** `title` (string, por defecto Contest name) · `dates` (string, por defecto Available until 20/9/2026) · `status`: Active, Closed (por defecto Active)
- **Nombres en Figma:** `title` ← `Title#68:0`, `dates` ← `Dates#68:3`, `status` ← `Status`
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `border/width/thin`, `chip/bg`, `chip/border`, `chip/height/s`, `chip/text`, `color/effect/shadow-ink`, `contest-card/bg`, `contest-card/border`, `contest-card/media-bg`, `contest-card/meta`, `contest-card/title`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-s`, `font/line-height/desktop/caption`, `font/line-height/desktop/h3`, `font/size/desktop/body-s`, `font/size/desktop/caption`, `font/size/desktop/h3`, `font/style/body`, `font/style/display`, `icon/size/sm`, `radius/md`, `radius/none`, `radius/pill`, `space/16`, `space/24`, `space/8`
- **Text styles:** `Desktop/caption`, `Desktop/h3`, `Desktop/body-s`
<!-- ⚙️ GENERATED:end:contest-card -->

> ⚠️ El bloque GENERATED de arriba es del volcado anterior (tarjeta con botón «Participar» y «Bases legales»). El maestro aprobado de la fase 5 (Active y Closed, sin botones) aún no está en Figma: el próximo sync lo sustituye. Hasta entonces, el criterio y el ejemplo de abajo son los que manda.

- **Propósito:** Tarjeta de un concurso en la Contest library. Imagen cuadrada, fechas (activos: «Available until …»; cerrados: «Ended on …»), nombre del concurso (h3) y premios en chips. Toda la tarjeta es un enlace a la página del concurso: el título lleva el enlace y este se estira a toda la tarjeta, igual que Recipe card. No lleva botones ni bases legales: las bases están en la página del concurso.
- **Ejemplo de código:** Active y Closed en el mismo bloque: es el mismo componente. Closed añade el Badge «Closed» dentro de la imagen y cambia la fecha a «Ended on …»; no cambia el estilo.
  ```html
  <article data-ds="contest-card" class="contest-card">
  <div class="contest-card__media"><img src="../assets/images/placeholder.svg" alt=""></div>
  <div class="contest-card__body">
  <p class="contest-card__dates" id="cc-slurp-dates">Available until 20/9/2026</p>
  <h3 class="contest-card__title"><a class="contest-card__link" href="/contests/slurp-and-win" aria-describedby="cc-slurp-dates">Slurp &amp; Win</a></h3>
  <ul class="contest-card__prizes" aria-label="Prizes">
  <li><span class="chip">T-shirts</span></li>
  <li><span class="chip">Balls</span></li>
  <li><span class="chip">Experience</span></li>
  </ul>
  </div>
  </article>
  <article data-ds="contest-card" class="contest-card">
  <div class="contest-card__media"><span class="badge badge--neutral">Closed</span><img src="../assets/images/placeholder.svg" alt=""></div>
  <div class="contest-card__body">
  <p class="contest-card__dates" id="cc-old-dates">Ended on 20/9/2026</p>
  <h3 class="contest-card__title"><a class="contest-card__link" href="/contests/old-contest" aria-describedby="cc-old-dates">Old contest</a></h3>
  <ul class="contest-card__prizes" aria-label="Prizes">
  <li><span class="chip">Balls</span></li>
  </ul>
  </div>
  </article>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Rol: `article` con un `h3`. El nombre del enlace es el título; `aria-describedby` añade la fecha, así que el lector anuncia «Slurp & Win, Available until 20/9/2026». El estado Closed se dice con texto (el Badge «Closed» y «Ended on»), no con el color. La imagen es decorativa (`alt` vacío) porque el nombre ya va en el texto. Los premios son texto dentro de una lista con nombre («Prizes»); los chips no son controles, así que el cursor no cambia. Contrastes: título tinta sobre blanco (más de 12:1); fechas en gris cálido sobre blanco (5,4:1); Badge neutral crema sobre tinta (17:1). Teclado: Tab llega al enlace del título (un solo punto de parada por tarjeta) y Enter abre el concurso. Foco: el trazo de la tarjeta pasa a grueso y al color de foco (`:has`), además del contorno del enlace si lo hubiera.
- **Cuándo usar / qué NO hace:** Solo en la Contest library (concursos activos y cerrados). No tiene botones de participar ni de bases: si un concurso necesita acciones propias, eso va en su página, no en la tarjeta. En móvil ocupa todo el ancho; en rejilla, su columna. Los nombres, fechas y premios de ejemplo son ⬜ TODO: los confirma GB Foods con la agencia. La mecánica de resultado inmediato y el límite de participaciones no se muestran en la tarjeta (⬜ TODO, ver la ficha de Contest result).
