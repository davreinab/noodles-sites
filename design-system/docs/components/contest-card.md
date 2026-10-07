### Contest card   ⚙️ synced: 2026-10-07T18:44:44Z

<!-- ⚙️ GENERATED:start:contest-card -->
- **Figma:** `68:95` · página «Contest card» · COMPONENT_SET · 2 variantes · última sync 2026-10-07T18:44:44Z
- **Descripción (Figma):** Card de concurso (Contest library, módulo de Home). Status=Active: Badge Natural «En curso» y Button Primary «Participar» (si el concurso es externo o iframe de agencia, activar Icon trailing con external-link y abrir en pestaña nueva avisándolo). Status=Closed: Badge Neutral «Finalizado» y Link «Ver ganadores». Las bases legales (Link inline) aparecen siempre: es obligatorio publicarlas. La card no es enlace en bloque: tiene dos acciones. Desktop 448 px; en móvil FILL.
- **Anatomía:** `status` → Type=Natural, `cta` → Hierarchy=Primary, Size=M, State=Default, `icon-leading` → Icon / arrow-right, `icon-trailing` → Icon / arrow-right, `rules-link` → Type=Inline, Surface=Light, State=Default, `icon-trailing` → Icon / arrow-right
- **Status:** Active, Closed
- **Propiedades de componente:** `Title#68:0` (TEXT, por defecto Nombre del concurso), `Dates#68:3` (TEXT, por defecto Del 1 al 30 de noviembre de 2026), `Status` (VARIANT, por defecto Active)
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `badge/natural/bg`, `badge/natural/text`, `border/width/thick`, `border/width/thin`, `button/primary/bg`, `button/primary/border`, `button/primary/text`, `color/effect/shadow-ink`, `contest-card/bg`, `contest-card/border`, `contest-card/media-bg`, `contest-card/meta`, `contest-card/title`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-m`, `font/line-height/desktop/body-s`, `font/line-height/desktop/caption`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/line-height/mobile/label`, `font/size/desktop/body-m`, `font/size/desktop/body-s`, `font/size/desktop/caption`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/size/mobile/label`, `font/style/body`, `font/style/display`, `icon/size/sm`, `link/default`, `radius/md`, `radius/none`, `radius/pill`, `space/16`, `space/24`, `space/4`, `space/8`
- **Text styles:** `Mobile/label`, `Desktop/caption`, `Desktop/h3`, `Desktop/body-s`, `Desktop/label`, `Desktop/body-m`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `badge/natural/bg`, `badge/natural/text`, `button/primary/bg`, `button/primary/border`, `button/primary/text`, `color/effect/shadow-ink`, `contest-card/bg`, `contest-card/border`, `contest-card/media-bg`, `contest-card/meta`, `contest-card/title`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-m`, `font/line-height/desktop/body-s`, `font/line-height/desktop/caption`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/line-height/mobile/label`, `font/size/desktop/body-m`, `font/size/desktop/body-s`, `font/size/desktop/caption`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/size/mobile/label`, `font/style/body`, `font/style/display`, `link/default`
<!-- ⚙️ GENERATED:end:contest-card -->

- **Propósito:** Card de concurso con estado (En curso o Finalizado), fechas, acción y bases legales. No es un enlace en bloque: tiene dos acciones.
- **Ejemplo de código:**
  ```html
  <article class="contest-card">
  <div class="contest-card__media">
  <span class="badge badge--natural">En curso</span>
  <span class="contest-card__caption">Imagen de la campaña</span>
  </div>
  <div class="contest-card__body">
  <h3 class="contest-card__title">Gana un viaje a Tokio</h3>
  <p class="contest-card__dates">Del 1 al 30 de noviembre de 2026</p>
  <div class="contest-card__actions">
  <a class="button" href="https://concursos.example.org/tokio" target="_blank" rel="noopener">Participar <span class="icon icon-external-link" aria-hidden="true"></span><span class="visually-hidden"> (abre en una pestaña nueva)</span></a>
  <a class="link" href="/concursos/tokio/bases">Bases legales</a>
  </div>
  </div>
  </article>
  ```
- **Accesibilidad (pares AA verificados):** Título tinta sobre blanco 18,7:1; fechas gris cálido sobre blanco 5,9:1; estado en Badge (blanco sobre verde 5,5:1 o crema sobre tinta 17,2:1) con la palabra, no solo color. Rol: `<article>` con encabezado y dos enlaces. Si el concurso es externo o un iframe de agencia, el botón lo avisa (icono y texto oculto). Teclado: Tab por las dos acciones. Foco: el de Button y Link.
- **Cuándo usar / qué NO hace:** En la Contest library y en la Home. Closed cambia el contenido (Badge Neutral «Finalizado» y Link «Ver ganadores»), no el estilo. Las bases legales aparecen siempre (es obligatorio publicarlas).
