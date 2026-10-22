### Allergen card   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:allergen-card -->
- **Figma:** `193:210` · página «Content» · COMPONENT · 1 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** Tarjeta de alérgeno principal de la sección Nutrition de la ficha de producto: nombre del alérgeno en negrita (Name, p. ej. «Gluten or derivatives») y nota de uso (Note, p. ej. «Not suitable for coeliacs»). Fondo nutrition/bg, borde nutrition/border y radio md. Se muestran tres tarjetas («Main allergens») y el enlace «Check the detailed table» abre Allergen table. Wireframe UX 396:6073. Clase CSS: .allergen-card.
- **Anatomía:** sin instancias anidadas
- **API:** `name` (string, por defecto Gluten or derivatives) · `note` (string, por defecto Not suitable for coeliacs)
- **Nombres en Figma:** `name` ← `Name#193:18`, `note` ← `Note#193:19`
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `border/width/thin`, `color/text/default`, `color/text/secondary`, `font/family/body`, `font/line-height/desktop/body-m`, `font/line-height/desktop/body-s`, `font/size/desktop/body-m`, `font/size/desktop/body-s`, `font/style/body`, `nutrition/bg`, `nutrition/border`, `radius/md`, `space/16`, `space/8`
- **Text styles:** `Desktop/body-s`
<!-- ⚙️ GENERATED:end:allergen-card -->
- **Ejemplo de código:**
  ```html
  <li data-ds="allergen-card" class="allergen-card">
  <p class="allergen-card__name">Gluten or derivatives</p>
  <p class="allergen-card__note">Not suitable for coeliacs</p>
  </li>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Rol de elemento de lista (`li` dentro de `ul`). El nombre del alérgeno es el texto en negrita (`p`), no un encabezado: la sección ya tiene su `h3` «Main allergens». Texto principal tinta sobre blanco 18,7:1; la nota en gris cálido sobre blanco 5,9:1. La nota es texto, no color.
- **Cuándo usar / qué NO hace:** Dentro de Product details, bajo el encabezado «Main allergens» (tres como máximo). El listado completo va en Allergen table, en el modal.
