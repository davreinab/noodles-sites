### Pillar item   ⚙️ synced: 2026-10-22T15:21:21Z

<!-- ⚙️ GENERATED:start:pillar-item -->
- **Figma:** `277:332` · página «Content» · COMPONENT · 1 variantes · última sync 2026-10-22T15:21:21Z
- **Descripción (Figma):** Pillar item: pilar de «Taste you can trust» con número en círculo verde natural (surface/natural, número en on-natural, blanco ~5.5:1 sobre el verde) y texto a la derecha: título en negrita (Archivo Bold 18/24, sin estilo de texto) y cuerpo en Desktop/body-m. Se usa en lista ordenada de cuatro (Natural pillars; clase CSS .pillar-item; wireframe UX 274:6354). Props: Number, Title, Text. Textos de ejemplo ⬜ TODO envase.
- **Anatomía:** sin instancias anidadas
- **API:** `number` (string, por defecto 1) · `title` (string, por defecto Better noodles start with better production) · `text` (string, por defecto CO2-neutral production commitments and factory-level sourcing standards.)
- **Nombres en Figma:** `number` ← `Number#277:77`, `title` ← `Title#277:78`, `text` ← `Text#277:79`
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `color/surface/natural`, `color/text/default`, `color/text/on-natural`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-m`, `font/line-height/desktop/label`, `font/size/desktop/body-m`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `radius/pill`, `space/16`, `space/8`
- **Text styles:** `Desktop/label`, `Desktop/body-m`
<!-- ⚙️ GENERATED:end:pillar-item -->

- **Propósito:** Un pilar de «Taste you can trust»: número en círculo verde natural, título en negrita y texto explicativo.
- **Ejemplo de código:**
  ```html
  <li data-ds="pillar-item" class="pillar-item"><span class="pillar-item__number" aria-hidden="true">1</span><p class="pillar-item__title">Better noodles start with better production</p><p class="pillar-item__text">CO2-neutral production commitments and factory-level sourcing standards.</p></li>
  ```
  Va dentro de `<ol class="natural-pillars__list">`, con cuatro pilares. Desktop y Mobile: mismo marcado; en móvil cambia el tamaño de letra.
- **Accesibilidad (rol, nombre, estados y teclado):** Es un `li` de una lista ordenada: el orden de los pilares lo da el `ol`. El número visible va con `aria-hidden` para no repetir lo que la lista ya dice. El título y el texto se leen en ese orden. Contrastes: número en crema sobre verde natural (5,5:1); texto gris cálido sobre blanco (5,4:1). No es interactivo.
- **Cuándo usar / qué NO hace:** En Natural pillars, para una lista de cuatro razones numeradas. No sirve para pasos de preparación (eso es Step) ni para más de cuatro pilares sin revisar el diseño. Los textos de los pilares son ⬜ TODO envase y de ejemplo: deben validarse con el claim «Taste you can trust» antes de publicar.
