### Ingredient item   ⚙️ synced: 2026-10-08T06:16:03Z

<!-- ⚙️ GENERATED:start:ingredient-item -->
- **Figma:** `70:58` · página «Ingredients» · COMPONENT_SET · 2 variantes · última sync 2026-10-08T06:16:03Z
- **Descripción (Figma):** Fila de ingrediente. Level=Main: ingrediente principal con porcentaje en pill (ingredient/percent-bg, verde natural) y filete inferior decorativo. Level=Secondary: el resto de ingredientes en texto corrido. Regla de negocio: los alérgenos van SIEMPRE en negrita (&lt;strong&gt;, Archivo Bold), también dentro del nombre. El texto no es propiedad para conservar la negrita: se edita en la instancia. Los datos salen del envase; los mostrados son de ejemplo.
- **Anatomía:** sin instancias anidadas
- **Level:** Main, Secondary
- **Propiedades de componente:** `Percent#70:0` (TEXT, por defecto 52 %), `Level` (VARIANT, por defecto Main)
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `border/width/thin`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/label`, `font/size/desktop/body-l`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `ingredient/divider`, `ingredient/percent-bg`, `ingredient/percent-text`, `ingredient/text`, `radius/pill`, `space/16`, `space/4`, `space/8`
- **Text styles:** `Desktop/label`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/label`, `font/size/desktop/body-l`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `ingredient/divider`, `ingredient/percent-bg`, `ingredient/percent-text`, `ingredient/text`
<!-- ⚙️ GENERATED:end:ingredient-item -->

- **Propósito:** Fila de ingrediente. Main: ingrediente principal con su porcentaje en una píldora verde. Secondary: el resto de ingredientes en texto corrido. Los alérgenos van en negrita.
- **Ejemplo de código:**
  ```html
  <li class="ingredient-item">Fideos de <strong>trigo</strong><span class="ingredient-item__percent">52 %</span></li>
  <li class="ingredient-item ingredient-item--secondary">Otros: sal, especias, salsa de <strong>soja</strong> (<strong>soja</strong>, <strong>trigo</strong>), ajo y cebolla.</li>
  ```
- **Accesibilidad (pares AA verificados):** Texto tinta sobre crema 17,2:1 o blanco 18,7:1; porcentaje blanco sobre verde 5,5:1. Filete arena decorativo (no es límite de control). Los alérgenos se marcan con `<strong>`, que se anuncia como énfasis y se ve en negrita (regla de negocio), no solo con color. Es un `<li>` dentro de la lista de Ingredients.
- **Cuándo usar / qué NO hace:** Solo dentro de Ingredients. Los datos se copian del envase; no se resumen ni se reordenan.
