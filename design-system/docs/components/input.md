### Input   ⚙️ synced: 2026-10-07T18:19:35Z

<!-- ⚙️ GENERATED:start:input -->
- **Figma:** `47:122` · página «Input» · COMPONENT_SET · 6 variantes · última sync 2026-10-07T18:19:35Z
- **Descripción (Figma):** Campo de texto de una línea (formularios de concursos con estructura propia). Etiqueta siempre visible (no se sustituye por el placeholder). Error: borde rojo + icono + mensaje (nunca solo color); el mensaje se asocia al campo con aria-describedby. Required muestra asterisco y requiere aria-required. El valor y el texto de ayuda se editan en la instancia.
- **Anatomía:** `icon-error` → Icon / circle-alert
- **State:** Default, Hover, Focus, Filled, Error, Disabled
- **Propiedades de componente:** `Label#47:0` (TEXT, por defecto Nombre), `Required#47:7` (BOOLEAN, por defecto False), `Helper#47:14` (BOOLEAN, por defecto True), `Error icon#49:0` (INSTANCE_SWAP, por defecto Icon / circle-alert), `State` (VARIANT, por defecto Default)
- **Iconos / instancias anidadas:** sí · swap: `Error icon#49:0` · por defecto: Icon / circle-alert
- **Tokens que consume:** `border/width/thin`, `field/bg`, `field/border`, `field/error-text`, `field/helper`, `field/label`, `field/placeholder`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/desktop/label`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/sm`, `radius/sm`, `space/16`, `space/4`, `space/8`
- **Text styles:** `Desktop/label`, `Desktop/body-m`, `Desktop/caption`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `field/bg`, `field/border`, `field/error-text`, `field/helper`, `field/label`, `field/placeholder`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/desktop/label`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/desktop/label`, `font/style/body`, `font/style/display`
<!-- ⚙️ GENERATED:end:input -->

- **Propósito:** Campo de texto de una línea de los formularios (concursos, contacto propio si lo hubiera). Etiqueta en Anton, ayuda o error debajo.
- **Ejemplo de código:**
  ```html
  <div class="field">
  <label class="field__label" for="nombre">Nombre<span class="field__required" aria-hidden="true">*</span></label>
  <input class="field__control" id="nombre" name="nombre" type="text" placeholder="Escribe aquí" required aria-describedby="nombre-ayuda">
  <p class="field__helper" id="nombre-ayuda">Texto de ayuda</p>
  </div>
  <div class="field">
  <label class="field__label" for="email">Email</label>
  <input class="field__control" id="email" type="email" aria-invalid="true" aria-describedby="email-error">
  <p class="field__error" id="email-error"><span class="icon icon-circle-alert" aria-hidden="true"></span>Este campo es obligatorio</p>
  </div>
  ```
- **Accesibilidad (pares AA verificados):** Texto tinta sobre blanco 18,7:1; placeholder y ayuda en gris cálido sobre blanco 5,9:1; etiqueta tinta sobre crema 17,2:1; borde de tinta sobre crema 17,2:1 (≥ 3:1 de límite de control). Error: borde y mensaje en `--field-border-error`/`--field-error-text` (rojo de estado, verificado en la fase 2) con icono circle-alert y texto, nunca solo color. Desactivado: gris cálido sobre arena 4,3:1 (exento). Rol: `<input>` nativo con `<label for>` (nombre); la ayuda y el error se enlazan con `aria-describedby` y el error marca `aria-invalid="true"`. El asterisco de obligatorio es visual: el campo lleva `required`. El placeholder no sustituye a la etiqueta. Foco: contorno de 2 px pegado; el hover engorda el borde por dentro sin mover el layout.
- **Cuándo usar / qué NO hace:** Para datos de una línea (nombre, email, código). Textos largos: Textarea. Opciones cerradas: Select o Checkbox. Búsqueda: Search field. No se usa sin etiqueta visible.
