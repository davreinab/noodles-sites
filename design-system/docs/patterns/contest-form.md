### Contest form   ⚙️ synced: 2026-10-23T09:22:57Z

<!-- ⚙️ GENERATED:start:contest-form -->
- **Figma:** `313:3247` · página «Pattern / Detail pages» · COMPONENT_SET · 2 variantes · última sync 2026-10-23T09:22:57Z
- **Descripción (Figma):** Contest form: formulario de participación sobre fondo surface/inverse (wireframe 330:6682 desktop; 361:8561 móvil). Título «Join it now» y subtítulo; tres tarjetas blancas (Personal data, Proof of purchase, Consent) con Input (2 columnas en desktop, 1 en móvil), Select «Purchase type», 2 File upload (State=Empty: receipt front y back), 3 Checkbox, «* Required fields», Alert info «Important information» y botón Primary «Enter the contest» a todo el ancho; ayuda centrada. Clase CSS: .contest-form. ⬜ TODO GB Foods/agencia: campos y textos legales definitivos, formatos de fecha e importe, y el texto del consentimiento.
- **Anatomía:** `Input` → State=Default, `icon-error` → Icon / circle-alert, `Input` → State=Default, `icon-error` → Icon / circle-alert, `Input` → State=Default, `icon-error` → Icon / circle-alert, `Input` → State=Default, `icon-error` → Icon / circle-alert, `Select` → State=Default, `icon-chevron` → Icon / chevron-down, `icon-error` → Icon / circle-alert, `Input` → State=Default, `icon-error` → Icon / circle-alert, `Input` → State=Default, `icon-error` → Icon / circle-alert, `File upload` → State=Empty, `Button` → Hierarchy=Secondary, Size=M, State=Default, `icon-leading` → Icon / arrow-right, `icon-trailing` → Icon / arrow-right, `File upload` → State=Empty, `Button` → Hierarchy=Secondary, Size=M, State=Default, `icon-leading` → Icon / arrow-right, `icon-trailing` → Icon / arrow-right, `Checkbox` → Checked=False, State=Default, `check` → Icon / check, `Checkbox` → Checked=False, State=Default, `check` → Icon / check, `Checkbox` → Checked=False, State=Default, `check` → Icon / check, `Alert` → Type=Info, Layout=Inline, `icon-status` → Icon / info, `icon-close` → Icon / close, `Button` → Hierarchy=Primary, Size=L, State=Default, `icon-leading` → Icon / arrow-right, `icon-trailing` → Icon / arrow-right
- **API:** `breakpoint`: Desktop, Mobile (por defecto Desktop)
- **Nombres en Figma:** `breakpoint` ← `Breakpoint`
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown · capas sin swap: icon-status
- **Tokens que consume:** `alert/close`, `alert/info/bg`, `alert/info/border`, `alert/info/icon`, `alert/info/text`, `border/width/thick`, `border/width/thin`, `button/primary/bg`, `button/primary/border`, `button/primary/text`, `button/secondary/border`, `button/secondary/text`, `checkbox/box-bg`, `checkbox/box-border`, `checkbox/check`, `checkbox/label`, `color/surface/card`, `color/surface/inverse`, `color/text/default`, `color/text/on-inverse`, `color/text/secondary`, `field/bg`, `field/border`, `field/error-text`, `field/helper`, `field/icon`, `field/label`, `field/placeholder`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-m`, `font/line-height/desktop/body-s`, `font/line-height/desktop/caption`, `font/line-height/desktop/h2`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/size/desktop/body-m`, `font/size/desktop/body-s`, `font/size/desktop/caption`, `font/size/desktop/h2`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/md`, `icon/size/sm`, `layout/margin`, `radius/md`, `radius/pill`, `radius/sm`, `space/16`, `space/24`, `space/32`, `space/4`, `space/64`, `space/8`
- **Text styles:** `Desktop/h2`, `Desktop/body-m`, `Desktop/h3`, `Desktop/label`, `Desktop/caption`, `Desktop/body-s`
<!-- ⚙️ GENERATED:end:contest-form -->

- **Propósito:** Formulario de participación sobre tinta: título «Join it now» y entradilla; tres bloques en tarjetas blancas (Personal data, Proof of purchase y Consent), cada uno un fieldset con legend; y al final el botón «Enter the contest» a todo el ancho y la ayuda. Su ancla es `#join`.
- **Ejemplo de código:** Versión reducida: un bloque de cada tipo. El resto de campos sigue el mismo marcado (Input, Select y File upload).
  ```html
  <section data-ds="contest-form" class="section contest-form" aria-labelledby="cf-title">
  <div class="section__inner">
  <div class="section__header">
  <h2 class="section__title" id="cf-title">Join it now</h2>
  <p class="section__lead">Fill out the form to enter the drawing</p>
  </div>
  <form class="contest-form__form" id="join" tabindex="-1" action="/contests/slurp-and-win/enter" method="post">
  <fieldset class="contest-form__block">
  <legend class="contest-form__legend">Personal data</legend>
  <div class="contest-form__grid">
  <div class="field"><label class="field__label" for="cf-first">First name<span class="field__required" aria-hidden="true">*</span></label><input class="field__control" id="cf-first" name="first-name" type="text" autocomplete="given-name" placeholder="Enter first name" required></div>
  <div class="field"><label class="field__label" for="cf-last">Last name<span class="field__required" aria-hidden="true">*</span></label><input class="field__control" id="cf-last" name="last-name" type="text" autocomplete="family-name" placeholder="Enter last name" required></div>
  <div class="field"><label class="field__label" for="cf-email">Email address<span class="field__required" aria-hidden="true">*</span></label><input class="field__control" id="cf-email" name="email" type="email" autocomplete="email" placeholder="Enter email address" required></div>
  <div class="field"><label class="field__label" for="cf-birth">Date of birth (DD/MM/YYYY)<span class="field__required" aria-hidden="true">*</span></label><input class="field__control" id="cf-birth" name="birth-date" type="text" inputmode="numeric" autocomplete="bday" placeholder="DD/MM/YYYY" required></div>
  </div>
  </fieldset>
  <fieldset class="contest-form__block">
  <legend class="contest-form__legend">Proof of purchase</legend>
  <div class="contest-form__grid">
  <div class="field contest-form__full"><label class="field__label" for="cf-type">Purchase type<span class="field__required" aria-hidden="true">*</span></label><div class="field__select"><select class="field__control" id="cf-type" name="purchase-type" required><option value="">Select an option</option></select></div></div>
  <div class="field contest-form__full"><label class="field__label" for="cf-amount">Amount spent<span class="field__required" aria-hidden="true">*</span></label><input class="field__control" id="cf-amount" name="amount" type="text" inputmode="decimal" placeholder="0.00" required></div>
  </div>
  </fieldset>
  <fieldset class="contest-form__block">
  <legend class="contest-form__legend">Consent</legend>
  <div class="contest-form__consent">
  <label class="checkbox" data-ds="checkbox"><input class="checkbox__input" type="checkbox" name="age" required><span class="checkbox__label">I confirm I am 18 years or older and a resident of a participating country.<span class="field__required" aria-hidden="true">*</span></span></label>
  <label class="checkbox" data-ds="checkbox"><input class="checkbox__input" type="checkbox" name="rules" required><span class="checkbox__label">I have read and accept the <a class="link" href="/contests/slurp-and-win/rules">Contest Rules</a>.<span class="field__required" aria-hidden="true">*</span></span></label>
  <label class="checkbox" data-ds="checkbox"><input class="checkbox__input" type="checkbox" name="privacy" required><span class="checkbox__label">I have read the Privacy Notice on how my personal data will be processed for this contest.<span class="field__required" aria-hidden="true">*</span></span></label>
  <p class="contest-form__note">* Required fields</p>
  <div class="alert"><span class="icon icon-info" aria-hidden="true"></span><div class="alert__content"><p class="alert__title">Important information</p><p class="alert__body">Save your purchase tickets to send us if you win any of the contest prizes.</p></div></div>
  </div>
  <button class="button button--l contest-form__submit" type="submit">Enter the contest</button>
  <p class="contest-form__help">Having trouble? Check the <a class="link" href="/contests/slurp-and-win/rules">full contest rules</a> or contact <a class="link" href="/contact">customer care</a>.</p>
  </fieldset>
  </form>
  </div>
  </section>
  ```
  Los bloques de subida de justificantes (File upload, front y back) van dentro de «Proof of purchase» como `contest-form__full`.
- **Accesibilidad (rol, nombre, estados y teclado):** Cada bloque es un `fieldset` con su `legend`, así el lector anuncia el grupo al entrar en sus campos. Cada campo tiene `label for`. Los obligatorios llevan `required` (el lector lo anuncia) y un «*» con `aria-hidden` (el asterisco no se lee dos veces); la nota «* Required fields» explica la convención. Autocompletado: nombre, apellidos, email y fecha de nacimiento (`bday`). Los tres consentimientos son obligatorios, por eso también llevan «*». El formulario recibe `#join` con `tabindex="-1"`: el enlace «Enter now» o «Submit it now» lleva el foco a él. Teclado: orden de Tab por bloque y campo; Espacio marca los checkboxes; el botón envía. Contraste: campos y texto tinta sobre blanco; el texto de la ayuda final sobre tinta, crema (17:1), con los enlaces en `link--dark`. El error por campo lo marca Input o File upload con `aria-invalid` y su mensaje.
- **Cuándo usar / qué NO hace:** Solo en la página de concurso. No es el formulario de la newsletter (eso es Newsletter) ni de receta (Recipe submit). ⬜ TODO, de negocio: el límite de participaciones por persona o por compra (la pantalla «maximum participations» del wireframe depende de él), la mecánica de resultado inmediato (si el resultado se muestra al enviar o llega por correo) y el tipo de compra y la fecha válida. Los textos de consentimiento son ⬜ TODO (GB Foods, RGPD). El resumen de errores al enviar no está definido aún (⬜ TODO en el patrón de Field).
