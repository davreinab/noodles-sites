### Legal table   ⚙️ synced: 2026-10-23T09:22:57Z

<!-- ⚙️ GENERATED:start:legal-table -->
- **Figma:** `317:3484` · página «Pattern / Global» · COMPONENT_SET · 2 variantes · última sync 2026-10-23T09:22:57Z
- **Descripción (Figma):** Legal table: tabla de conservación de datos (wireframe 377:9477 desktop y 381-tabla móvil; sección 5 «How long do we keep your data?»). Dos columnas «Purpose» / «Retention period» (label en negrita con filete inferior, filas con filete fino border/subtle). Desktop: tabla de 2 columnas. Móvil: cada fila apilada (Purpose encima de Retention period, con su etiqueta en caption); la cabecera no se muestra. Clase CSS: .legal-table. ⬜ TODO GB Foods/agencia: texto definitivo de finalidades y plazos de conservación.
- **Anatomía:** sin instancias anidadas
- **API:** `breakpoint`: Desktop, Mobile (por defecto Desktop)
- **Nombres en Figma:** `breakpoint` ← `Breakpoint`
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `border/width/thin`, `color/border/default`, `color/border/subtle`, `color/text/default`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-m`, `font/line-height/desktop/label`, `font/size/desktop/body-m`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `space/16`, `space/8`
- **Text styles:** `Desktop/label`, `Desktop/body-m`
<!-- ⚙️ GENERATED:end:legal-table -->

- **Propósito:** ⬜ TODO
- **Ejemplo de código:** la tabla del maestro con sus tres filas de ejemplo (desktop: dos columnas con cabecera; móvil: la misma tabla se apila y cada celda muestra su nombre con `data-label`).
  ```html
  <table data-ds="legal-table" class="legal-table">
  <caption class="visually-hidden">How long do we keep your data?</caption>
  <thead><tr><th scope="col">Purpose</th><th scope="col">Retention period</th></tr></thead>
  <tbody>
  <tr><td data-label="Purpose">(i) To learn about your browsing preferences on our Website in order to personalise and improve our products and your experience.</td><td data-label="Retention period">As indicated in our Cookie Policy, up to a maximum of 2 years.</td></tr>
  <tr><td data-label="Purpose">(ii) To manage and process the response to your request for information sent through our Website's contact form.</td><td data-label="Retention period">Until your query has been resolved, as well as the time necessary to comply with the corresponding legal obligations.</td></tr>
  <tr><td data-label="Purpose">(iii) To handle emails received at our corporate email addresses for the purpose of maintaining business relationships with entities, organisations or companies and with the people who work for or collaborate with them or with their legal representatives.</td><td data-label="Retention period">For a reasonable period after your last interaction with us.</td></tr>
  </tbody>
  </table>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** ⬜ TODO
- **Cuándo usar / qué NO hace:** ⬜ TODO
