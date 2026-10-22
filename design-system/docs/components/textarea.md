### Textarea   ⚙️ synced: 2026-10-22T09:37:04Z

<!-- ⚙️ GENERATED:start:textarea -->
- **Figma:** `47:247` · página «Forms» · COMPONENT_SET · 6 variantes · última sync 2026-10-22T09:37:04Z
- **Descripción (Figma):** Campo de texto multilínea (comentarios, respuestas de concurso). Etiqueta siempre visible (no se sustituye por el placeholder). Error: borde rojo + icono + mensaje (nunca solo color); el mensaje se asocia con aria-describedby. Required muestra asterisco y requiere aria-required. El valor y el texto de ayuda se editan en la instancia.
- **Anatomía:** `icon-error` → Icon / circle-alert
- **API:** `label` (string, por defecto Mensaje) · `required` (boolean, por defecto false) · `helper` (boolean, por defecto true) · `errorIcon` (icon, por defecto Icon / circle-alert) · `filled` (boolean, por defecto false) · `error` (boolean, por defecto false) · `disabled` (boolean, por defecto false)
- **Estados de CSS:** Hover, Focus
- **Nombres en Figma:** `label` ← `Label#47:21`, `required` ← `Required#47:28`, `helper` ← `Helper#47:35`, `errorIcon` ← `Error icon#50:0`, `filled` ← `State=Filled`, `error` ← `State=Error`, `disabled` ← `State=Disabled`
- **Iconos / instancias anidadas:** sí · swap: `errorIcon` · por defecto: Icon / circle-alert
- **Tokens que consume:** `border/width/thin`, `field/bg`, `field/border`, `field/error-text`, `field/helper`, `field/label`, `field/placeholder`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/desktop/label`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/sm`, `radius/sm`, `space/128`, `space/16`, `space/4`, `space/8`
- **Text styles:** `Desktop/label`, `Desktop/body-m`, `Desktop/caption`
<!-- ⚙️ GENERATED:end:textarea -->

- **Propósito:** Campo de texto multilínea (mensajes, respuestas de concurso). Misma anatomía que Input, alto mínimo de 128 px y redimensionable en vertical.
- **Ejemplo de código:**
  ```html
  <div data-ds="textarea" class="field">
  <label class="field__label" for="mensaje">Mensaje</label>
  <textarea class="field__control field__control--textarea" id="mensaje" name="mensaje" placeholder="Escribe aquí" aria-describedby="mensaje-ayuda"></textarea>
  <p class="field__helper" id="mensaje-ayuda">Máximo 500 caracteres</p>
  </div>
  <div data-ds="textarea" class="field">
  <label class="field__label" for="respuesta">Respuesta</label>
  <textarea class="field__control field__control--textarea" id="respuesta" aria-invalid="true" aria-describedby="respuesta-error"></textarea>
  <p class="field__error" id="respuesta-error"><span class="icon icon-circle-alert" aria-hidden="true"></span>Este campo es obligatorio</p>
  </div>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Texto tinta sobre blanco 18,7:1; placeholder y ayuda en gris cálido sobre blanco 5,9:1; etiqueta tinta sobre crema 17,2:1; borde de tinta sobre crema 17,2:1 (≥ 3:1 de límite de control). Error: borde y mensaje en `--field-border-error`/`--field-error-text` (rojo de estado, verificado en la fase 2) con icono circle-alert y texto, nunca solo color. Desactivado: gris cálido sobre arena 4,3:1 (exento). Rol: `<textarea>` con `<label for>`; ayuda y error por `aria-describedby`. Si hay límite de caracteres, el contador se anuncia de forma educada (aria-live polite) solo al acercarse al límite. Foco igual que Input.
- **Cuándo usar / qué NO hace:** Para respuestas de más de una línea. No se usa para datos cortos (Input) ni sin etiqueta.
