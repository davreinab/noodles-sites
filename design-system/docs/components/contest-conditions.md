### Contest conditions   ⚙️ synced: 2026-10-23T09:22:57Z

<!-- ⚙️ GENERATED:start:contest-conditions -->
- **Figma:** `308:2308` · página «Content» · COMPONENT · 1 variantes · última sync 2026-10-23T09:22:57Z
- **Descripción (Figma):** Contest conditions: caja tinta de condiciones y fechas del concurso (columna Winning conditions del bloque Contest how-to, wireframe 330:6619). Dos filas con icono (Icon calendar-clock: «Entries close» con fecha en negrita; Icon trophy: «Grand prize draw»), lista de condiciones y link «Read the full contest rules →». Clase CSS: .contest-conditions. ⬜ TODO GB Foods: la lista de condiciones, fechas reales y la mecánica del sorteo (resultado inmediato y límite de participaciones pendientes de confirmar con GB Foods y la agencia). Iconos: surface/inverse con icon/color/inverse (override en instancia).
- **Anatomía:** `Icon / calendar-clock` → Icon / calendar-clock, `Icon / trophy` → Icon / trophy
- **API:** sin propiedades
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown · capas sin swap: Icon / calendar-clock, Icon / trophy
- **Tokens que consume:** `color/surface/inverse`, `color/text/on-inverse`, `font/family/body`, `font/line-height/desktop/body-m`, `font/line-height/desktop/body-s`, `font/size/desktop/body-m`, `font/size/desktop/body-s`, `font/style/body`, `icon/color/inverse`, `icon/size/md`, `link/inverse`, `radius/md`, `space/24`, `space/32`
- **Text styles:** `Desktop/body-s`, `Desktop/body-m`
<!-- ⚙️ GENERATED:end:contest-conditions -->

- **Propósito:** Bloque de condiciones del concurso sobre tinta: dos filas con icono (cierre de participaciones y sorteo del gran premio), un texto de condiciones y el enlace a las bases completas.
- **Ejemplo de código:** Texto de muestra en inglés; ⬜ TODO: la lista de condiciones real la aporta GB Foods.
  ```html
  <div data-ds="contest-conditions" class="contest-conditions">
  <ul class="contest-conditions__list">
  <li class="contest-conditions__item"><span class="icon icon-calendar-clock icon--inverse" aria-hidden="true"></span><span>Entries close: <strong>30 September 2026 at 23:59 CET</strong></span></li>
  <li class="contest-conditions__item"><span class="icon icon-trophy icon--inverse" aria-hidden="true"></span><span>Grand prize draw: <strong>7 October 2026</strong></span></li>
  </ul>
  <p class="contest-conditions__text">Entry rules apply: one entry per purchase, and proof of purchase is required.</p>
  <a class="link link--dark" href="/contests/slurp-and-win/rules">Read the full contest rules →</a>
  </div>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Los iconos son decorativos (`aria-hidden`): las fechas van en texto y se leen en orden. Las filas son elementos de una lista sin nombre visible; la lista no necesita nombre porque sus filas se explican solas. Contrastes: crema sobre tinta (17:1); la fecha en negrita no cambia el color. El enlace es `link--dark`: crema sobre tinta con subrayado, y su foco es amarillo de marca (12:1 sobre tinta). Teclado: Tab llega al enlace de las bases. Sin controles salvo el enlace.
- **Cuándo usar / qué NO hace:** Solo en la columna «Winning conditions» de Contest how-to. No sustituye a las bases legales: el texto de condiciones es ⬜ TODO (GB Foods) y el enlace lleva a las bases completas, que son obligatorias. No sirve para otras fechas que no sean de cierre o de sorteo. Las fechas son ⬜ TODO: 30 septiembre y 7 octubre de 2026 vienen del wireframe y deben confirmarse con GB Foods y la agencia.
