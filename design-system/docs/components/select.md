### Select   ⚙️ synced: 2026-10-07T18:44:44Z

<!-- ⚙️ GENERATED:start:select -->
- **Figma:** `48:141` · página «Select» · COMPONENT_SET · 6 variantes · última sync 2026-10-07T18:44:44Z
- **Descripción (Figma):** Selector de una opción: país o idioma (Aiki NL/FR), filtros. Open muestra el menú (elevation/3) con la opción activa en amarillo de marca. En código se recomienda &lt;select&gt; nativo o un listbox accesible (teclado: flechas, Enter, Esc). Error con borde, icono y mensaje. Valor y opciones se editan en la instancia.
- **Anatomía:** `icon-chevron` → Icon / chevron-down, `icon-error` → Icon / circle-alert
- **State:** Default, Hover, Focus, Open, Error, Disabled
- **Propiedades de componente:** `Label#48:0` (TEXT, por defecto País), `Required#48:7` (BOOLEAN, por defecto False), `Icon#50:18` (INSTANCE_SWAP, por defecto Icon / chevron-down), `Error icon#50:25` (INSTANCE_SWAP, por defecto Icon / circle-alert), `State` (VARIANT, por defecto Default)
- **Iconos / instancias anidadas:** sí · swap: `Icon#50:18`, `Error icon#50:25` · por defecto: Icon / chevron-down, Icon / circle-alert
- **Tokens que consume:** `border/width/thin`, `field/bg`, `field/border`, `field/error-text`, `field/helper`, `field/icon`, `field/label`, `field/placeholder`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/desktop/label`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/md`, `icon/size/sm`, `radius/sm`, `space/16`, `space/4`, `space/8`
- **Text styles:** `Desktop/label`, `Desktop/body-m`, `Desktop/caption`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `field/bg`, `field/border`, `field/error-text`, `field/helper`, `field/icon`, `field/label`, `field/placeholder`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/desktop/label`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/desktop/label`, `font/style/body`, `font/style/display`
<!-- ⚙️ GENERATED:end:select -->

- **Propósito:** Desplegable de una opción (país, tipo de consulta). Se implementa con el `<select>` nativo y su apariencia propia; el chevron es decorativo.
- **Ejemplo de código:**
  ```html
  <div class="field">
  <label class="field__label" for="pais">País</label>
  <div class="field__select">
  <select class="field__control" id="pais" name="pais" aria-invalid="true" aria-describedby="pais-error">
  <option value="">Elige una opción</option>
  <option value="es">España</option>
  <option value="fr">Francia</option>
  </select>
  </div>
  <p class="field__error" id="pais-error"><span class="icon icon-circle-alert" aria-hidden="true"></span>Elige un país</p>
  </div>
  ```
- **Accesibilidad (pares AA verificados):** Texto tinta sobre blanco 18,7:1; placeholder y ayuda en gris cálido sobre blanco 5,9:1; etiqueta tinta sobre crema 17,2:1; borde de tinta sobre crema 17,2:1 (≥ 3:1 de límite de control). Error: borde y mensaje en `--field-border-error`/`--field-error-text` (rojo de estado, verificado en la fase 2) con icono circle-alert y texto, nunca solo color. Desactivado: gris cálido sobre arena 4,3:1 (exento). Chevron (`--field-icon`, tinta) decorativo. Rol: `<select>` nativo, que da gratis el teclado (flechas, letras, Enter, Esc) y la lista accesible en móvil; por eso el estado Open del maestro es solo referencia visual y no se reconstruye un listbox propio. Nombre por `<label for>`.
- **Cuándo usar / qué NO hace:** Para elegir una opción entre cinco o más. Con dos a cuatro opciones visibles, mejor Chip o casillas. No se usa para navegar entre páginas.
