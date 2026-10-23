### Legal table   ⬜ sin volcado de Figma

<!-- ⚙️ GENERATED:start:legal-table -->
<!-- ⚙️ GENERATED:end:legal-table -->

- **Propósito:** Tabla de dos columnas de la página legal: finalidad del tratamiento («Purpose») y plazo de conservación («Retention period»), una fila por finalidad. Cabecera en negrita con filete grueso y filas con filete fino. En escritorio es una tabla normal; en móvil cada fila se apila: la finalidad encima y el plazo debajo, cada uno con su etiqueta de columna visible.
- **Variantes:** una sola. Desktop: tabla de dos columnas. Mobile: filas apiladas (sin cambiar el marcado, solo el CSS). No hay scroll horizontal.
- **Ejemplo de código:** Tres filas (i)–(iii) de la captura, que es el texto real de Yatekomo. El caption va oculto a la vista (`visually-hidden`), porque el maestro no lo dibuja.
  ```html
  <table data-ds="legal-table" class="legal-table">
  <caption class="visually-hidden">Purposes and retention periods</caption>
  <thead>
  <tr>
  <th scope="col">Purpose</th>
  <th scope="col">Retention period</th>
  </tr>
  </thead>
  <tbody>
  <tr>
  <td data-label="Purpose">(i) To learn about your browsing preferences on our Website in order to personalise and improve our products and your experience.</td>
  <td data-label="Retention period">As indicated in our Cookie Policy, up to a maximum of 2 years.</td>
  </tr>
  <tr>
  <td data-label="Purpose">(ii) To manage and process the response to your request for information sent through our Website's contact form.</td>
  <td data-label="Retention period">Until your query has been resolved, as well as the time necessary to comply with the corresponding legal obligations.</td>
  </tr>
  <tr>
  <td data-label="Purpose">(iii) To handle emails received at our corporate email addresses for the purpose of maintaining business relationships with entities, organisations or companies and with the people who work for or collaborate with them or with their legal representatives.</td>
  <td data-label="Retention period">For a reasonable period after your last interaction with us.</td>
  </tr>
  </tbody>
  </table>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Rol: `table` con nombre por su `caption` (visualmente oculto; el nombre lo lee el lector de pantalla). Cada columna tiene `th scope="col"`. Se usa `scope="col"` y no `scope="row"` porque la finalidad es el contenido de la fila, no su rótulo: el rótulo de cada celda es el nombre de su columna. En móvil, el nombre de la columna sale visible como etiqueta encima de cada valor, sacado de `data-label` con `::before`. La cabecera no se oculta con `display: none` sino con medidas cero: así sigue en el árbol de accesibilidad y el lector puede anunciar los encabezados. ⬜ Verificación pendiente: en Safari con VoiceOver, al cambiar `display` de la tabla a bloque, algunos navegadores pierden el rol de tabla; hay que comprobarlo en iOS y macOS antes de dar el componente por verificado. Teclado: no es interactivo; no tiene foco. Contraste: texto en tinta sobre blanco; la etiqueta de columna en móvil es gris cálido sobre blanco (5,9:1). Los filetes son decorativos (la separación también la da el espacio) y no se usan para entender el contenido.
- **Cuándo usar / qué NO hace:** Solo para datos de dos columnas en la página legal: finalidades y plazos de conservación. No para tablas de datos numéricos ni comparativas de más de dos columnas (en móvil, eso exigiría scroll horizontal; no está resuelto). No es un acordeón ni una lista de definiciones: si cada entrada tiene un texto largo y varios párrafos, se usa un apartado (h2) con párrafos. Textos: las finalidades (i)–(iii) y sus plazos son los de la captura; cualquier fila nueva es ⬜ TODO, la aporta GB Foods (es texto legal).
