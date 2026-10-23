### Pillar item   ⚙️ synced: 2026-10-23T09:22:57Z

<!-- ⚙️ GENERATED:start:pillar-item -->
- **Figma:** `308:367` · página «Content» · COMPONENT_SET · 2 variantes · última sync 2026-10-23T09:22:57Z
- **Descripción (Figma):** Pillar item: pilar de «Taste you can trust» con número en círculo (número en on-natural sobre surface/natural en Tone=Natural; número en text/on-inverse sobre surface/inverse en Tone=Ink) y texto a la derecha (title + text). Tone=Ink se usa en Contest how-to, donde el verde natural no encaja. Clase CSS: .pillar-item (Tone=Ink añade .pillar-item--ink). Usos: Natural pillars (wireframe UX) y Contest how-to (contest-howto, pasos 1–4; el paso 3 lleva link «Submit it now →» a nivel de instancia). ⬜ TODO GB Foods/agencia: confirmar si el Tone=Ink aplica también a otras páginas.
- **Anatomía:** sin instancias anidadas
- **API:** `number` (string, por defecto 1) · `title` (string, por defecto Better noodles start with better production) · `text` (string, por defecto CO2-neutral production commitments and factory-level sourcing standards.) · `tone`: Natural, Ink (por defecto Natural)
- **Nombres en Figma:** `number` ← `Number#308:0`, `title` ← `Title#308:1`, `text` ← `Text#308:2`, `tone` ← `Tone`
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `color/surface/natural`, `color/text/default`, `color/text/on-natural`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-m`, `font/line-height/desktop/label`, `font/size/desktop/body-m`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `radius/pill`, `space/16`, `space/8`
- **Text styles:** `Desktop/label`, `Desktop/body-m`
<!-- ⚙️ GENERATED:end:pillar-item -->

- **Propósito:** Un pilar o paso numerado: número en círculo, título en negrita y texto explicativo. Hay dos variantes de color del círculo: verde natural (Natural pillars, por defecto) y tinta (`.pillar-item--ink`, para los pasos de Contest how-to sobre blanco). Puede llevar una acción al final (`.pillar-item__action`, por ejemplo «Submit it now →») alineada con el círculo.
- **Ejemplo de código:** Tone=Natural (por defecto) y Tone=Ink en la misma lista: el Ink es el paso con acción (Contest how-to, paso 2).
  ```html
  <ol data-ds="pillar-item">
  <li class="pillar-item"><span class="pillar-item__number" aria-hidden="true">1</span><p class="pillar-item__title">Better noodles start with better production</p><p class="pillar-item__text">CO2-neutral production commitments and factory-level sourcing standards.</p></li>
  <li class="pillar-item pillar-item--ink"><span class="pillar-item__number" aria-hidden="true">2</span><p class="pillar-item__title">Submit your entry</p><p class="pillar-item__text">Fill in the participation form with your details and a photo of the receipt.</p><p class="pillar-item__action"><a class="link" href="#join">Submit it now →</a></p></li>
  </ol>
  ```
  Va dentro de `<ol>` (`natural-pillars__list` o `contest-howto__steps`), con sus pasos en orden. Desktop y Mobile: mismo marcado; en móvil cambia el tamaño de letra.
- **Accesibilidad (rol, nombre, estados y teclado):** Es un `li` de una lista ordenada: el orden lo da el `ol`. El número visible va con `aria-hidden` para no repetir lo que la lista ya dice. El título y el texto se leen en ese orden. Contrastes: número en crema sobre verde natural (5,5:1) o crema sobre tinta (17:1); texto tinta o gris cálido sobre blanco. La variante Ink no cambia el significado: el número sigue siendo el orden. El enlace de la acción es un `link` normal: se llega con Tab y su nombre es el texto visible («Submit it now →»; la flecha es decorativa, el texto de la acción es lo que se lee). No es interactivo salvo esa acción.
- **Cuándo usar / qué NO hace:** Para una lista de pasos o pilares numerados de hasta cuatro elementos: Natural pillars (verde) y Contest how-to (tinta). No sirve para pasos de preparación (eso es Step) ni para más de cuatro pilares sin revisar el diseño. Los textos de los pilares son ⬜ TODO envase y de ejemplo: deben validarse antes de publicar. En Contest how-to, los textos de los pasos son ⬜ TODO: los confirma GB Foods (son reglas del concurso).
