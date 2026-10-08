### Tab   ⚙️ synced: 2026-10-08T06:16:03Z

<!-- ⚙️ GENERATED:start:tab -->
- **Figma:** `54:58` · página «Tab» · COMPONENT_SET · 4 variantes · última sync 2026-10-08T06:16:03Z
- **Descripción (Figma):** Pestaña del primer nivel del filtro de productos (Cups / Bags / Sauces). Selected en tinta con texto crema. En código: role=&quot;tablist&quot; / role=&quot;tab&quot; con aria-selected y flechas izquierda/derecha para moverse. Alto 48 (mínimo táctil).
- **Anatomía:** sin instancias anidadas
- **State:** Default, Hover, Selected, Focus
- **Propiedades de componente:** `Label#54:0` (TEXT, por defecto Cups), `State` (VARIANT, por defecto Default)
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `border/width/thin`, `font/family/display`, `font/line-height/desktop/label`, `font/size/desktop/label`, `font/style/display`, `radius/pill`, `space/16`, `space/24`, `tab/bg`, `tab/border`, `tab/text`
- **Text styles:** `Desktop/label`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `font/family/display`, `font/line-height/desktop/label`, `font/size/desktop/label`, `font/style/display`, `tab/bg`, `tab/border`, `tab/text`
<!-- ⚙️ GENERATED:end:tab -->

- **Propósito:** Pestaña de tipo de producto (Cups, Bags, Sauces): primer nivel del Product filter y del Product carousel.
- **Ejemplo de código:**
  ```html
  <div role="tablist" aria-label="Tipo de producto">
  <button class="tab" role="tab" aria-selected="true" aria-controls="panel-cups" id="tab-cups">Cups</button>
  <button class="tab" role="tab" aria-selected="false" aria-controls="panel-bags" id="tab-bags" tabindex="-1">Bags</button>
  </div>
  ```
- **Accesibilidad (pares AA verificados):** Reposo: tinta sobre blanco 18,7:1, borde de tinta sobre crema 17,2:1. Hover: tinta sobre amarillo 12,3:1. Seleccionada: crema sobre tinta 17,2:1 y `aria-selected`. Rol: patrón tabs de WAI-ARIA (`tablist`/`tab`/`tabpanel`): Tab entra en la pestaña activa y las flechas mueven entre pestañas (tabindex móvil). Foco: contorno de 2 px pegado en tinta.
- **Cuándo usar / qué NO hace:** Para cambiar el conjunto de productos mostrado en la misma página. Solo se muestran tipos con productos. No es navegación entre páginas (Nav item) ni un filtro de selección múltiple (Chip).
