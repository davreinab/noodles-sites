### Product filter   ⚙️ synced: 2026-10-07T18:30:51Z

<!-- ⚙️ GENERATED:start:product-filter -->
- **Figma:** `55:253` · página «Pattern / Product filter» · COMPONENT_SET · 2 variantes · última sync 2026-10-07T18:30:51Z
- **Descripción (Figma):** Patrón: filtro de la Product library en 3 niveles. Tipo (Tab: Cups / Bags / Sauces) → línea (Chip: Original / Yakisoba / Rice) → sabor (Chip). Cada nivel depende del anterior; solo se muestran las opciones con productos (sin resultados vacíos). Mobile: cada fila se desplaza en horizontal. Los sabores son de ejemplo. Sin variables propias.
- **Anatomía:** `tab` → State=Selected, `tab` → State=Default, `tab` → State=Default, `chip` → State=Selected, `icon-leading` → Icon / check, `chip` → State=Default, `icon-leading` → Icon / check, `chip` → State=Default, `icon-leading` → Icon / check, `chip` → State=Selected, `icon-leading` → Icon / check, `chip` → State=Default, `icon-leading` → Icon / check, `chip` → State=Default, `icon-leading` → Icon / check, `chip` → State=Default, `icon-leading` → Icon / check
- **Breakpoint:** Desktop, Mobile
- **Propiedades de componente:** `Breakpoint` (VARIANT, por defecto Desktop)
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `border/width/thin`, `chip/bg`, `chip/bg-selected`, `chip/border`, `chip/text`, `chip/text-selected`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-s`, `font/line-height/desktop/caption`, `font/line-height/desktop/label`, `font/size/desktop/body-s`, `font/size/desktop/caption`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/sm`, `layout/frame`, `layout/margin`, `radius/pill`, `space/16`, `space/24`, `space/8`, `tab/bg`, `tab/bg-selected`, `tab/border`, `tab/text`, `tab/text-selected`
- **Text styles:** `Desktop/caption`, `Desktop/label`, `Desktop/body-s`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `chip/bg`, `chip/bg-selected`, `chip/border`, `chip/text`, `chip/text-selected`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-s`, `font/line-height/desktop/caption`, `font/line-height/desktop/label`, `font/size/desktop/body-s`, `font/size/desktop/caption`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `tab/bg`, `tab/bg-selected`, `tab/border`, `tab/text`, `tab/text-selected`
<!-- ⚙️ GENERATED:end:product-filter -->

- **Propósito:** Filtro de la Product library en tres niveles: tipo (Tab), línea (Chip) y sabor (Chip). Cada nivel depende del anterior y solo muestra opciones con productos.
- **Ejemplo de código:**
  ```html
  <div class="product-filter">
  <div class="product-filter__group">
  <span class="product-filter__label" id="f-tipo">Tipo</span>
  <div class="product-filter__options" role="tablist" aria-labelledby="f-tipo"><button class="tab" role="tab" aria-selected="true">Cups</button><button class="tab" role="tab" aria-selected="false" tabindex="-1">Bags</button></div>
  </div>
  <fieldset class="product-filter__group">
  <legend class="product-filter__label">Línea</legend>
  <div class="product-filter__options"><button class="chip" type="button" aria-pressed="true"><span class="icon icon-check" aria-hidden="true"></span>Original</button><button class="chip" type="button" aria-pressed="false">Yakisoba</button></div>
  </fieldset>
  </div>
  ```
- **Accesibilidad (pares AA verificados):** Etiquetas de nivel en gris cálido sobre crema 5,4:1; Tab y Chip con sus pares (seleccionado crema sobre tinta 17,2:1). Cada nivel es un grupo con nombre (`tablist` para el tipo; `fieldset`/`legend` con chips `aria-pressed` para línea y sabor). Al cambiar un nivel se anuncia el número de productos (aria-live) y el foco no se pierde. En móvil cada fila se desplaza en horizontal y sigue siendo operable con teclado.
- **Cuándo usar / qué NO hace:** Solo en la Product library (y Product carousel para el tipo). No muestra filtros que den cero resultados ni sustituye a la búsqueda.
