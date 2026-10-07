### Ingredients   ⚙️ synced: 2026-10-07T18:41:16Z

<!-- ⚙️ GENERATED:start:ingredients -->
- **Figma:** `70:59` · página «Ingredients» · COMPONENT · 1 variantes · última sync 2026-10-07T18:41:16Z
- **Descripción (Figma):** Bloque de ingredientes de la página de producto y de receta: título (h3) · ingredientes principales (Ingredient item Main, con %) · resto (Ingredient item Secondary) · Link «Ver etiqueta del envase» que abre el modal con la foto de la etiqueta (fase 5). Lista semántica &lt;ul&gt;; alérgenos en &lt;strong&gt;. Sin variables propias de bloque: usa ingredient/*.
- **Anatomía:** `ingredient-main` → Level=Main, `ingredient-main` → Level=Main, `ingredient-main` → Level=Main, `ingredient-secondary` → Level=Secondary, `label-link` → Type=Standalone, Surface=Light, State=Default, `icon-trailing` → Icon / arrow-right
- **Propiedades de componente:** ninguna
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `border/width/thin`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/size/desktop/body-l`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/sm`, `ingredient/divider`, `ingredient/meta`, `ingredient/percent-bg`, `ingredient/percent-text`, `ingredient/text`, `link/default`, `radius/pill`, `space/16`, `space/4`, `space/8`
- **Text styles:** `Desktop/h3`, `Desktop/label`, `Desktop/caption`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/size/desktop/body-l`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `ingredient/divider`, `ingredient/meta`, `ingredient/percent-bg`, `ingredient/percent-text`, `ingredient/text`, `link/default`
<!-- ⚙️ GENERATED:end:ingredients -->

- **Propósito:** Bloque de ingredientes de la página de producto y de receta: título, ingredientes principales con porcentaje, el resto en texto corrido y enlace a la etiqueta del envase.
- **Ejemplo de código:**
  ```html
  <section class="ingredients" aria-labelledby="ing-title">
  <h3 class="ingredients__title" id="ing-title">Ingredientes</h3>
  <ul class="ingredients__list">
  <li class="ingredient-item">Fideos de <strong>trigo</strong><span class="ingredient-item__percent">52 %</span></li>
  <li class="ingredient-item ingredient-item--secondary">Otros: sal, especias, salsa de <strong>soja</strong>, ajo y cebolla.</li>
  </ul>
  <p class="ingredients__note">Datos del envase.</p>
  <a class="link link--standalone" href="#etiqueta" aria-haspopup="dialog">Ver etiqueta del envase <span class="icon icon-arrow-right" aria-hidden="true"></span></a>
  </section>
  ```
- **Accesibilidad (pares AA verificados):** Título y texto en tinta sobre blanco 18,7:1; nota en gris cálido sobre blanco 5,9:1. Rol: sección con encabezado y lista `<ul>`. El enlace abre el Modal L con la foto de la etiqueta (`aria-haspopup="dialog"`); la foto lleva un `alt` que remite a la lista («Etiqueta del envase; ingredientes detallados en la lista»).
- **Cuándo usar / qué NO hace:** En Product details (producto y receta). No sustituye al panel de nutrición ni muestra alérgenos sueltos: los alérgenos se marcan dentro del texto.
