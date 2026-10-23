### File upload   ⚙️ synced: 2026-10-23T09:22:57Z

<!-- ⚙️ GENERATED:start:file-upload -->
- **Figma:** `308:2420` · página «Forms» · COMPONENT_SET · 3 variantes · última sync 2026-10-23T09:22:57Z
- **Descripción (Figma):** File upload: campo de subida de archivo para el formulario de concurso (Proof of purchase: foto del ticket delantera y trasera). State=Empty: «No file selected — JPG, PNG or PDF, max 5MB». State=Selected: nombre del archivo y icono close (Remove). State=Error: borde y mensaje en color de error (field/border-error, field/error-text). Tokens de Input (field/*). En código: input type="file" real, visualmente oculto pero accesible, con su label; el botón «Upload file» es el visible. Clase CSS: .file-upload (estado: .file-upload--selected / --error). ⬜ TODO GB Foods: formatos y tamaño máximo definitivos (JPG, PNG, PDF, 5 MB).
- **Anatomía:** `Button` → Hierarchy=Secondary, Size=M, State=Default, `icon-leading` → Icon / arrow-right, `icon-trailing` → Icon / arrow-right
- **API:** `label` (string, por defecto Upload receipt — front) · `helper` (string, por defecto Upload a clear photo of the receipt.) · `empty` (boolean, por defecto true) · `selected` (boolean, por defecto false) · `error` (boolean, por defecto false)
- **Nombres en Figma:** `label` ← `Label#308:21`, `helper` ← `Helper#308:25`, `empty` ← `State=Empty`, `selected` ← `State=Selected`, `error` ← `State=Error`
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `border/width/thick`, `border/width/thin`, `button/secondary/border`, `button/secondary/text`, `field/bg`, `field/border`, `field/helper`, `field/label`, `field/placeholder`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-m`, `font/line-height/desktop/body-s`, `font/line-height/desktop/label`, `font/size/desktop/body-m`, `font/size/desktop/body-s`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/sm`, `radius/md`, `radius/pill`, `space/16`, `space/24`, `space/8`
- **Text styles:** `Desktop/label`, `Desktop/body-m`, `Desktop/body-s`
<!-- ⚙️ GENERATED:end:file-upload -->

- **Propósito:** Subida de un archivo (justificante de compra): etiqueta del campo, caja con el botón «Upload file» y un texto de estado («No file selected — JPG, PNG or PDF, max 5MB»), ayuda debajo y, si falla, el error. Tres estados: Empty (por defecto), Selected (nombre del archivo y botón de quitar) y Error (borde grueso en error y mensaje).
- **Ejemplo de código:** Los tres estados, cada uno como su campo: Empty (por defecto), Selected y Error.
  ```html
  <div data-ds="file-upload" class="field file-upload">
  <label class="field__label" id="fu-front-label" for="fu-front">Upload receipt – front<span class="field__required" aria-hidden="true">*</span></label>
  <div class="file-upload__control">
  <label class="button button--secondary file-upload__trigger">
  <input class="visually-hidden file-upload__input" id="fu-front" name="receipt-front" type="file" accept="image/jpeg,image/png,application/pdf" required aria-labelledby="fu-front-label" aria-describedby="fu-front-help fu-front-status">
  <span>Upload file</span>
  </label>
  <p class="file-upload__status" id="fu-front-status" aria-live="polite">No file selected — JPG, PNG or PDF, max 5MB</p>
  </div>
  <p class="field__helper" id="fu-front-help">Make sure the purchased products are clearly visible on the receipt.</p>
  </div>
  <div data-ds="file-upload" class="field file-upload">
  <label class="field__label" id="fu-back-label" for="fu-back">Upload receipt – back<span class="field__required" aria-hidden="true">*</span></label>
  <div class="file-upload__control">
  <label class="button button--secondary file-upload__trigger">
  <input class="visually-hidden file-upload__input" id="fu-back" name="receipt-back" type="file" accept="image/jpeg,image/png,application/pdf" aria-labelledby="fu-back-label" aria-describedby="fu-back-help fu-back-status">
  <span>Upload file</span>
  </label>
  <p class="file-upload__status file-upload__status--selected" id="fu-back-status" aria-live="polite">receipt-back.jpg</p>
  <button class="icon-button icon-button--secondary file-upload__remove" type="button" aria-label="Remove receipt-back.jpg"><span class="icon icon-close" aria-hidden="true"></span></button>
  </div>
  <p class="field__helper" id="fu-back-help">Optional: the back of the receipt.</p>
  </div>
  <div data-ds="file-upload" class="field file-upload">
  <label class="field__label" id="fu-err-label" for="fu-err">Upload receipt – front<span class="field__required" aria-hidden="true">*</span></label>
  <div class="file-upload__control">
  <label class="button button--secondary file-upload__trigger">
  <input class="visually-hidden file-upload__input" id="fu-err" name="receipt-err" type="file" aria-invalid="true" required aria-labelledby="fu-err-label" aria-describedby="fu-err-help fu-err-status fu-err-error">
  <span>Upload file</span>
  </label>
  <p class="file-upload__status" id="fu-err-status" aria-live="polite">No file selected — JPG, PNG or PDF, max 5MB</p>
  </div>
  <p class="field__helper" id="fu-err-help">Make sure the purchased products are clearly visible on the receipt.</p>
  <p class="field__error" id="fu-err-error">The file is bigger than 5MB. Choose another one.</p>
  </div>
  ```
  Selected: el estado pasa a `file-upload__status--selected` con el nombre del archivo y el botón de quitar va al final de `file-upload__control`. Error: el input lleva `aria-invalid="true"` y `field__error` debajo de la ayuda.
- **Accesibilidad (rol, nombre, estados y teclado):** El `input type="file"` es el control real: va visualmente oculto (`visually-hidden`) pero sigue en el orden de Tab. El foco se ve en el botón (`:has`), con contorno de 2 px. Enter o Espacio abren el selector nativo. El nombre accesible lo da `aria-labelledby` (la etiqueta del campo, «Upload receipt – front»); prevalece sobre las etiquetas, así que el texto «Upload file» no se suma al nombre. El `label for` del campo queda para la asociación visual. El estado va en `aria-live="polite"` y se anuncia al elegir o quitar un archivo. El error se dice con `aria-invalid` y con el texto del mensaje; no depende del color (el borde grueso es un refuerzo). La ayuda va en `aria-describedby`. Contraste: texto de estado gris cálido sobre blanco (5,4:1); foco en tinta sobre blanco.
- **Cuándo usar / qué NO hace:** Solo para justificantes en Contest form. Acepta un archivo por campo (sin `multiple`). Límites del wireframe: 5 MB y JPG, PNG o PDF; ⬜ TODO confirmar con GB Foods y la agencia (son condiciones de la mecánica del concurso). No hace vista previa ni sube nada por sí solo: la subida la hace el formulario al enviar. El justificante trasero es opcional y el texto de ayuda lo dice.
