### Recipe submit   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:recipe-submit -->
- **Figma:** `219:1911` · página «Pattern / Libraries» · COMPONENT_SET · 2 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** Recipe submit: bloque de captación de recetas de usuarios (fondo surface/card, blanco). Título «Do you have your own recipes with Yatekomo?», subtítulo, y a la derecha Textarea («Tell us your recipe», ayuda «List the ingredients with their quantities and the time of each step») y Button Primary M «Send my recipe». Breakpoint Mobile: apilado. Uso: Recipe library, entre el banner y el footer (wireframe 171:3808 y móvil 486:13025). Clase CSS: .recipe-submit. Nota: el subtítulo es provisional (la SPEC no lo fija).
- **Anatomía:** `textarea` → State=Default, `icon-error` → Icon / circle-alert, `submit` → Hierarchy=Primary, Size=M, State=Default, `icon-leading` → Icon / arrow-right, `icon-trailing` → Icon / arrow-right
- **API:** `breakpoint`: Desktop, Mobile (por defecto Desktop)
- **Nombres en Figma:** `breakpoint` ← `Breakpoint`
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `border/width/thick`, `border/width/thin`, `button/primary/bg`, `button/primary/border`, `button/primary/text`, `color/surface/card`, `color/text/default`, `color/text/secondary`, `field/bg`, `field/border`, `field/error-text`, `field/helper`, `field/label`, `field/placeholder`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/desktop/h2`, `font/line-height/desktop/label`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/desktop/h2`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/sm`, `radius/pill`, `radius/sm`, `space/128`, `space/16`, `space/24`, `space/4`, `space/64`, `space/8`, `space/80`
- **Text styles:** `Desktop/h2`, `Desktop/body-m`, `Desktop/label`, `Desktop/caption`
<!-- ⚙️ GENERATED:end:recipe-submit -->

- **Propósito:** Invitación a los usuarios a enviar su propia receta y recogida de su texto en un campo libre. Va al final de la Recipe library, entre el banner y el footer. En escritorio, título y subtítulo a la izquierda y el formulario a la derecha; en móvil, todo apilado. El botón primario es `.button` sin modificador.
- **Ejemplo de código:**
  ```html
  <section data-ds="recipe-submit" class="section recipe-submit" aria-labelledby="rs-title">
  <div class="recipe-submit__inner">
  <div class="recipe-submit__intro">
  <h2 class="recipe-submit__title" id="rs-title">Do you have your own recipes with Yatekomo?</h2>
  <p class="recipe-submit__lead">Share them with us so more people can enjoy your creations.</p>
  </div>
  <form class="recipe-submit__form" action="/recipes/submit" method="post">
  <div class="field">
  <label class="field__label" for="rs-recipe">Tell us your recipe</label>
  <textarea class="field__control field__control--textarea" id="rs-recipe" name="recipe" aria-describedby="rs-help"></textarea>
  <p class="field__helper" id="rs-help">List the ingredients with their quantities and the time of each step</p>
  </div>
  <button class="button" type="submit">Send my recipe</button>
  </form>
  </div>
  </section>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Rol: sección con nombre por su h2 (`aria-labelledby`); el formulario se anuncia como formulario con su botón de envío. El Textarea tiene `label for` («Tell us your recipe») y su ayuda va en `aria-describedby`, así que el lector la anuncia junto al campo. El botón es `button type="submit"` con texto de acción («Send my recipe»). Si la validación falla, el campo lleva `aria-invalid="true"` y su mensaje de error (`field__error`) va enlazado también con `aria-describedby`; el foco pasa al primer campo con error. Teclado: Tab recorre el campo y el botón; Enter en el botón envía. El error se da con texto, no solo con el color del borde.
- **Cuándo usar / qué NO hace:** Solo al final de la Recipe library, o donde se quiera invitar a enviar recetas. Recoge el texto de la receta (un campo): no es un formulario de contacto ni de registro. Para compartir una receta ya publicada se usa Share panel.
