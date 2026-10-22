### Ingredients   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:ingredients -->
- **Figma:** `70:59` · página «Content» · COMPONENT · 1 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** Bloque de ingredientes de la ficha de producto (punto 6 de la SPEC, wireframe UX 396:6073 en el archivo 1YhsCqdqYCHlK4Y82IY5G3): fondo color/surface/page. Imagen de placeholder a la izquierda (desktop) y a la derecha el título «Ingredients», subtítulo «100% natural with nothing added. We'll give you all the details», lista de tarjetas Ingredient item Level=Main («79% of content» · «Oriental noodles» · composición; «16.6% of content» · «Liquid sauce»; «4.4% of content» · «Vegetables and dehydrated chicken») y pie «Still curious?» con el link «View pack label» (abre el modal Nutrition label). Sin variante Secondary en este bloque (sí en Ingredient item).
- **Anatomía:** `ingredient-main` → Level=Main, `ingredient-main` → Level=Main, `ingredient-main` → Level=Main, `label-link` → Type=Standalone, Surface=Light, State=Default, `icon-trailing` → Icon / arrow-right
- **API:** sin propiedades
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `border/width/thin`, `color/border/subtle`, `color/surface/card`, `color/surface/page`, `color/text/default`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-s`, `font/line-height/desktop/caption`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/size/desktop/body-s`, `font/size/desktop/caption`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/sm`, `ingredient/meta`, `ingredient/text`, `link/default`, `radius/lg`, `radius/md`, `space/16`, `space/24`, `space/64`, `space/8`
- **Text styles:** `Desktop/h3`, `Desktop/body-s`, `Desktop/caption`, `Desktop/label`
<!-- ⚙️ GENERATED:end:ingredients -->

- **Propósito:** Bloque de ingredientes de la página de producto y de receta: título, subtítulo, tarjetas de ingrediente y enlace a la etiqueta del envase («Still curious? View pack label»).
- **Ejemplo de código:**
  ```html
  <section data-ds="ingredients" class="ingredients" aria-labelledby="ing-title">
  <h2 class="ingredients__title" id="ing-title">Ingredients</h2>
  <p class="ingredients__note">100% natural with nothing added. We'll give you all the details.</p>
  <ul class="ingredients__list">
  <li class="ingredient-item"><span class="ingredient-item__percent">79% of content</span><span class="ingredient-item__name">Oriental noodles</span><span class="ingredient-item__text"><strong>Wheat</strong> flour, modified starch, salt, sodium and potassium carbonate</span></li>
  <li class="ingredient-item ingredient-item--secondary">Others: salt, spices, <strong>soy</strong> sauce (<strong>soy</strong>, <strong>wheat</strong>), garlic and onion.</li>
  </ul>
  <p class="ingredients__more">Still curious? <a class="link link--standalone ingredients__link" href="#etiqueta" aria-haspopup="dialog">View pack label <span class="icon icon-arrow-right" aria-hidden="true"></span></a></p>
  </section>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Título en `h2` (en Product details) con texto tinta sobre crema 17,2:1 y sobre blanco 18,7:1; subtítulo y composición en gris cálido 5,4:1 sobre crema. Rol: sección con encabezado y lista `ul`. El enlace abre el modal Nutrition label (`aria-haspopup="dialog"`); la foto del envase lleva su `alt` en el modal.
- **Cuándo usar / qué NO hace:** En Product details (producto y receta). No sustituye al panel de nutrición ni muestra alérgenos sueltos: los alérgenos se marcan dentro del texto.
