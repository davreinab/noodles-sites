### Allergen table / Cell   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:allergen-table-cell -->
- **Figma:** `193:176` · página «Content» · COMPONENT_SET · 2 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** Celda de la tabla de alérgenos (subcomponente de Allergen table). Present=true: el producto contiene el alérgeno; cabecera en amarillo de marca (color/surface/brand) y marca ●. Present=false: no lo contiene; cabecera en superficie neutra (color/surface/page) y marca –. La presencia no depende solo del color: la marca ● o – y el texto oculto contains / does not contain lo indican. Propiedad de texto Name: nombre del alérgeno (en inglés). Se usa solo dentro de Allergen table (modal Allergy detailed table, wireframe UX 490:7469 y 490:11998). Clase CSS: .allergen-table (celda).
- **Anatomía:** sin instancias anidadas
- **API:** `name` (string, por defecto Gluten) · `present` (boolean, por defecto true)
- **Nombres en Figma:** `name` ← `Name#193:0`, `present` ← `Present`
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `color/surface/brand`, `color/text/default`, `color/text/secondary`, `font/family/body`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/style/body`, `radius/sm`, `space/16`, `space/8`
- **Text styles:** `Desktop/body-m`, `Desktop/caption`
<!-- ⚙️ GENERATED:end:allergen-table-cell -->

- **Propósito:** Celda de un alérgeno dentro de la tabla de alérgenos: nombre del alérgeno y estado (contiene o no contiene), con la marca ● o – y el color de marca solo en «contiene». Es el hijo de `.allergen-table__item`; la tabla la compone.
- **Ejemplo de código:**
  ```html
  <li data-ds="allergen-table-cell" class="allergen-table__item allergen-table__item--present"><span class="allergen-table__name">Gluten</span><span class="allergen-table__mark" aria-hidden="true">●</span><span class="visually-hidden">contains</span></li>
  <li data-ds="allergen-table-cell" class="allergen-table__item"><span class="allergen-table__name">Eggs</span><span class="allergen-table__mark" aria-hidden="true">–</span><span class="visually-hidden">does not contain</span></li>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Cada celda es un `li` dentro de la lista de la tabla. El estado no depende solo del color: la marca ● / – va oculta a lectores y el texto oculto dice «contains» o «does not contain». Texto tinta sobre brand y sobre page, según el maestro.
- **Cuándo usar / qué NO hace:** Solo dentro de Allergen table (14 alérgenos UE). No es un control: no tiene interacción.
