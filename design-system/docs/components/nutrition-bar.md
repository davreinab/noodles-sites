### Nutrition bar   ⚙️ synced: 2026-10-08T06:16:03Z

<!-- ⚙️ GENERATED:start:nutrition-bar -->
- **Figma:** `71:74` · página «Nutrition» · COMPONENT_SET · 2 variantes · última sync 2026-10-08T06:16:03Z
- **Descripción (Figma):** Barra de un nutriente: nombre · valor por 100 g (negrita) · % de ingesta de referencia (IR) y barra cuyo relleno mide ese % del ancho de la pista. Highlight=True: relleno verde natural y Badge Natural con el claim del envase (−20 % sal, −80 % grasas saturadas). La barra es decorativa (aria-hidden): el dato accesible es el texto, así que el valor y el % siempre se escriben. Relleno ≥3:1 sobre la pista. Los valores los valida el equipo de Nutrición de GB Foods. En Figma, el % se fija con el padding derecho de «track» (padding-right = ancho × (1 − %)); en código, width: &lt;%&gt; del relleno.
- **Anatomía:** sin instancias anidadas
- **Highlight:** False, True
- **Propiedades de componente:** `Nutrient#71:0` (TEXT, por defecto Proteínas), `Value#71:3` (TEXT, por defecto 10 g), `Percent#71:6` (TEXT, por defecto 20 % IR), `Highlight` (VARIANT, por defecto False)
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `font/family/body`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/style/body`, `nutrition/fill`, `nutrition/label`, `nutrition/meta`, `nutrition/track`, `nutrition/value`, `radius/pill`, `space/16`, `space/4`, `space/8`
- **Text styles:** `Desktop/body-m`, `Desktop/caption`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `font/family/body`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/style/body`, `nutrition/fill`, `nutrition/label`, `nutrition/meta`, `nutrition/track`, `nutrition/value`
<!-- ⚙️ GENERATED:end:nutrition-bar -->

- **Propósito:** Fila de un nutriente: nombre, valor por 100 g, porcentaje de la ingesta de referencia y una barra que lo representa. Highlight para los claims del envase, con el claim junto al valor.
- **Ejemplo de código:**
  ```html
  <li class="nutrition-bar">
  <div class="nutrition-bar__row">
  <span class="nutrition-bar__label">Proteínas</span>
  <span class="nutrition-bar__amount"><span class="nutrition-bar__value">10 g</span><span class="nutrition-bar__percent">20 % IR</span></span>
  </div>
  <meter class="nutrition-bar__meter" min="0" max="100" value="20" aria-hidden="true"></meter>
  </li>
  <li class="nutrition-bar nutrition-bar--highlight">
  <div class="nutrition-bar__row"><span class="nutrition-bar__label">Sal</span><span class="nutrition-bar__amount"><span class="badge badge--natural">−20 %</span><span class="nutrition-bar__value">1,9 g</span><span class="nutrition-bar__percent">32 % IR</span></span></div>
  <meter class="nutrition-bar__meter" min="0" max="100" value="32" aria-hidden="true"></meter>
  </li>
  ```
- **Accesibilidad (pares AA verificados):** Nombre y valor en tinta sobre blanco 18,7:1; % IR en gris cálido sobre blanco 5,9:1. Relleno de tinta sobre pista arena 13,7:1 y verde sobre arena 4,0:1 (≥ 3:1). La barra es decorativa (`aria-hidden`): el dato accesible es el texto (valor y % siempre escritos). La barra es un `<meter>` nativo (valor = % IR) oculto al lector; sin estilos inline.
- **Cuándo usar / qué NO hace:** Solo dentro de Nutrition panel. Los valores los valida el equipo de Nutrición de GB Foods; el claim de Highlight debe coincidir con el envase.
