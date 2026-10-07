### Textarea   ⚙️ synced: 2026-10-07T18:41:16Z

<!-- ⚙️ GENERATED:start:textarea -->
- **Figma:** `47:247` · página «Textarea» · COMPONENT_SET · 6 variantes · última sync 2026-10-07T18:41:16Z
- **Descripción (Figma):** Campo de texto multilínea (comentarios, respuestas de concurso). Etiqueta siempre visible (no se sustituye por el placeholder). Error: borde rojo + icono + mensaje (nunca solo color); el mensaje se asocia con aria-describedby. Required muestra asterisco y requiere aria-required. El valor y el texto de ayuda se editan en la instancia.
- **Anatomía:** `icon-error` → Icon / circle-alert
- **State:** Default, Hover, Focus, Filled, Error, Disabled
- **Propiedades de componente:** `Label#47:21` (TEXT, por defecto Mensaje), `Required#47:28` (BOOLEAN, por defecto False), `Helper#47:35` (BOOLEAN, por defecto True), `Error icon#50:0` (INSTANCE_SWAP, por defecto Icon / circle-alert), `State` (VARIANT, por defecto Default)
- **Iconos / instancias anidadas:** sí · swap: `Error icon#50:0` · por defecto: Icon / circle-alert
- **Tokens que consume:** `border/width/thin`, `field/bg`, `field/border`, `field/error-text`, `field/helper`, `field/label`, `field/placeholder`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/desktop/label`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/sm`, `radius/sm`, `space/128`, `space/16`, `space/4`, `space/8`
- **Text styles:** `Desktop/label`, `Desktop/body-m`, `Desktop/caption`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `field/bg`, `field/border`, `field/error-text`, `field/helper`, `field/label`, `field/placeholder`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/desktop/label`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/desktop/label`, `font/style/body`, `font/style/display`
<!-- ⚙️ GENERATED:end:textarea -->

- **Propósito:** Campo de texto multilínea (mensajes, respuestas de concurso). Misma anatomía que Input, alto mínimo de 128 px y redimensionable en vertical.
- **Ejemplo de código:**
  ```html
  <div class="field">
  <label class="field__label" for="mensaje">Mensaje</label>
  <textarea class="field__control field__control--textarea" id="mensaje" name="mensaje" placeholder="Escribe aquí" aria-describedby="mensaje-ayuda"></textarea>
  <p class="field__helper" id="mensaje-ayuda">Máximo 500 caracteres</p>
  </div>
  <div class="field">
  <label class="field__label" for="respuesta">Respuesta</label>
  <textarea class="field__control field__control--textarea" id="respuesta" aria-invalid="true" aria-describedby="respuesta-error"></textarea>
  <p class="field__error" id="respuesta-error"><span class="icon icon-circle-alert" aria-hidden="true"></span>Este campo es obligatorio</p>
  </div>
  ```
- **Accesibilidad (pares AA verificados):** Texto tinta sobre blanco 18,7:1; placeholder y ayuda en gris cálido sobre blanco 5,9:1; etiqueta tinta sobre crema 17,2:1; borde de tinta sobre crema 17,2:1 (≥ 3:1 de límite de control). Error: borde y mensaje en `--field-border-error`/`--field-error-text` (rojo de estado, verificado en la fase 2) con icono circle-alert y texto, nunca solo color. Desactivado: gris cálido sobre arena 4,3:1 (exento). Rol: `<textarea>` con `<label for>`; ayuda y error por `aria-describedby`. Si hay límite de caracteres, el contador se anuncia de forma educada (aria-live polite) solo al acercarse al límite. Foco igual que Input.
- **Cuándo usar / qué NO hace:** Para respuestas de más de una línea. No se usa para datos cortos (Input) ni sin etiqueta.
