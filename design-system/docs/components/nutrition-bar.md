### Nutrition bar   ⚙️ synced: 2026-10-07T15:16:17Z

<!-- ⚙️ GENERATED:start:nutrition-bar -->
- **Figma:** `71:74` · página «Nutrition» · COMPONENT_SET · 2 variantes · última sync 2026-10-07T15:16:17Z
- **Descripción (Figma):** Barra de un nutriente: nombre · valor por 100 g (negrita) · % de ingesta de referencia (IR) y barra cuyo relleno mide ese % del ancho de la pista. Highlight=True: relleno verde natural y Badge Natural con el claim del envase (−20 % sal, −80 % grasas saturadas). La barra es decorativa (aria-hidden): el dato accesible es el texto, así que el valor y el % siempre se escriben. Relleno ≥3:1 sobre la pista. Los valores los valida el equipo de Nutrición de GB Foods. En Figma, el % se fija con el padding derecho de «track» (padding-right = ancho × (1 − %)); en código, width: &lt;%&gt; del relleno.
- **Anatomía:** sin instancias anidadas
- **Highlight:** False, True
- **Propiedades de componente:** `Nutrient#71:0` (TEXT, por defecto Proteínas), `Value#71:3` (TEXT, por defecto 10 g), `Percent#71:6` (TEXT, por defecto 20 % IR), `Highlight` (VARIANT, por defecto False)
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `font/family/body`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/style/body`, `nutrition/fill`, `nutrition/label`, `nutrition/meta`, `nutrition/track`, `nutrition/value`, `radius/pill`, `space/16`, `space/8`
- **Text styles:** `Desktop/body-m`, `Desktop/caption`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `font/family/body`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/style/body`, `nutrition/fill`, `nutrition/label`, `nutrition/meta`, `nutrition/track`, `nutrition/value`
<!-- ⚙️ GENERATED:end:nutrition-bar -->

- **Propósito:** ⬜ TODO
- **Ejemplo de código:** ⬜ TODO _(snippet HTML mínimo con las clases reales de `components.css`; se copia a `source.code.example` del schema)_
  ```html
  <!-- ⬜ TODO -->
  ```
- **Accesibilidad (pares AA verificados):** ⬜ TODO
- **Cuándo usar / qué NO hace:** ⬜ TODO
