### Allergen table   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:allergen-table -->
- **Figma:** `193:344` · página «Content» · COMPONENT_SET · 2 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** Tabla de alérgenos UE (Reg. 1169/2011): contenido del modal «Allergy detailed table». Texto introductorio y rejilla de los 14 alérgenos (Gluten, Crustaceans, Eggs, Fish, Peanuts, Soy, Milk, Nuts, Celery, Mustard, Sesame, Sulphites, Lupin, Molluscs) con instancias de Allergen table / Cell: presente = cabecera amarilla de marca y ●; ausente = cabecera neutra y –. Breakpoint: Desktop 4 columnas, Mobile 2 columnas. Los ejemplos (Eggs, Fish, Peanuts, Soy, Milk, Celery) son provisionales hasta tener la ficha técnica validada. Se usa en el modal Allergy detailed table (wireframe UX 490:7469 y 490:11998). Clase CSS: .allergen-table.
- **Anatomía:** `Allergen table / Cell` → Present=false, `Allergen table / Cell` → Present=false, `Allergen table / Cell` → Present=true, `Allergen table / Cell` → Present=true, `Allergen table / Cell` → Present=true, `Allergen table / Cell` → Present=true, `Allergen table / Cell` → Present=true, `Allergen table / Cell` → Present=false, `Allergen table / Cell` → Present=true, `Allergen table / Cell` → Present=false, `Allergen table / Cell` → Present=false, `Allergen table / Cell` → Present=false, `Allergen table / Cell` → Present=false, `Allergen table / Cell` → Present=false
- **API:** `breakpoint`: Desktop, Mobile (por defecto Desktop)
- **Nombres en Figma:** `breakpoint` ← `Breakpoint`
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `border/width/thin`, `color/surface/brand`, `color/surface/page`, `color/text/default`, `color/text/secondary`, `font/family/body`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/style/body`, `nutrition/bg`, `nutrition/border`, `radius/md`, `radius/sm`, `space/16`, `space/24`, `space/8`
- **Text styles:** `Desktop/body-m`, `Desktop/caption`
<!-- ⚙️ GENERATED:end:allergen-table -->
- **Ejemplo de código:**
  ```html
  <section data-ds="allergen-table" class="allergen-table" aria-labelledby="allergen-table-intro">
  <p class="allergen-table__intro" id="allergen-table-intro">Allergen information (EU Reg. 1169/2011): <span aria-hidden="true">●</span> contains, <span aria-hidden="true">–</span> does not contain.</p>
  <ul class="allergen-table__list">
  <li class="allergen-table__item"><span class="allergen-table__name">Gluten</span><span class="allergen-table__mark" aria-hidden="true">–</span><span class="visually-hidden"> does not contain</span></li>
  <li class="allergen-table__item"><span class="allergen-table__name">Crustaceans</span><span class="allergen-table__mark" aria-hidden="true">–</span><span class="visually-hidden"> does not contain</span></li>
  <li class="allergen-table__item allergen-table__item--present"><span class="allergen-table__name">Eggs</span><span class="allergen-table__mark" aria-hidden="true">●</span><span class="visually-hidden"> contains</span></li>
  <li class="allergen-table__item allergen-table__item--present"><span class="allergen-table__name">Fish</span><span class="allergen-table__mark" aria-hidden="true">●</span><span class="visually-hidden"> contains</span></li>
  <li class="allergen-table__item allergen-table__item--present"><span class="allergen-table__name">Peanuts</span><span class="allergen-table__mark" aria-hidden="true">●</span><span class="visually-hidden"> contains</span></li>
  <li class="allergen-table__item allergen-table__item--present"><span class="allergen-table__name">Soy</span><span class="allergen-table__mark" aria-hidden="true">●</span><span class="visually-hidden"> contains</span></li>
  <li class="allergen-table__item allergen-table__item--present"><span class="allergen-table__name">Milk</span><span class="allergen-table__mark" aria-hidden="true">●</span><span class="visually-hidden"> contains</span></li>
  <li class="allergen-table__item"><span class="allergen-table__name">Nuts</span><span class="allergen-table__mark" aria-hidden="true">–</span><span class="visually-hidden"> does not contain</span></li>
  <li class="allergen-table__item allergen-table__item--present"><span class="allergen-table__name">Celery</span><span class="allergen-table__mark" aria-hidden="true">●</span><span class="visually-hidden"> contains</span></li>
  <li class="allergen-table__item"><span class="allergen-table__name">Mustard</span><span class="allergen-table__mark" aria-hidden="true">–</span><span class="visually-hidden"> does not contain</span></li>
  <li class="allergen-table__item"><span class="allergen-table__name">Sesame</span><span class="allergen-table__mark" aria-hidden="true">–</span><span class="visually-hidden"> does not contain</span></li>
  <li class="allergen-table__item"><span class="allergen-table__name">Sulphites</span><span class="allergen-table__mark" aria-hidden="true">–</span><span class="visually-hidden"> does not contain</span></li>
  <li class="allergen-table__item"><span class="allergen-table__name">Lupin</span><span class="allergen-table__mark" aria-hidden="true">–</span><span class="visually-hidden"> does not contain</span></li>
  <li class="allergen-table__item"><span class="allergen-table__name">Molluscs</span><span class="allergen-table__mark" aria-hidden="true">–</span><span class="visually-hidden"> does not contain</span></li>
  </ul>
  </section>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Es una lista (`ul` con `li`), no una tabla: cada celda es un dato suelto con su estado, sin cabeceras de fila ni de columna que relacionar. El estado no depende del color: el ● y el – son texto, y cada celda lleva un texto oculto (`visually-hidden`) con «contains» o «does not contain», que lee el lector de pantalla junto al nombre. Los símbolos llevan `aria-hidden`. Contrastes: tinta sobre amarillo de marca 12,3:1; tinta sobre crema 17,2:1; intro en gris cálido sobre blanco 5,9:1. El modal que lo contiene debe tener su nombre y devolver el foco al disparador.
- **Cuándo usar / qué NO hace:** Solo dentro del modal «Allergen detailed table», abierto desde el enlace de Product details. No se pone en la página: la página muestra Allergen card.
