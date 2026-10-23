### Contest result   ⚙️ synced: 2026-10-23T09:22:57Z

<!-- ⚙️ GENERATED:start:contest-result -->
- **Figma:** `313:3567` · página «Pattern / Detail pages» · COMPONENT_SET · 6 variantes · última sync 2026-10-23T09:22:57Z
- **Descripción (Figma):** Contest result: pantalla tras participar (wireframe 490:13618 lose, 490:13957 win, 490:13867 limit; móviles 501:14641, 501:15446, 501:15170). Variant=Lose: «Oh crap… Your entry hasn't won a prize this time», texto de descarga con negrita, Voucher «15% OFF» y botón «Download discount voucher». Variant=Win: imagen de premios, «Oh my noodles!» y «Your entry has won the prize», texto de verificación por email (⬜ TODO) y botón secondary «Go back to the contest site». Variant=Limit: «You have surpassed the maximum participations allowed», texto de cupón con negrita, Voucher «25% OFF» y botón de descarga. Fondo surface/page. Clase CSS: .contest-result (.contest-result--win / --limit). ⬜ TODO GB Foods/agencia: mecánica de límite de participaciones y de resultado inmediato (pendiente de confirmar); código de barras real.
- **Anatomía:** `Voucher` → Voucher, `Button` → Hierarchy=Primary, Size=M, State=Default, `icon-leading` → Icon / arrow-right, `icon-trailing` → Icon / arrow-right
- **API:** `variant`: Lose, Win, Limit (por defecto Lose) · `breakpoint`: Desktop, Mobile (por defecto Desktop)
- **Nombres en Figma:** `variant` ← `Variant`, `breakpoint` ← `Breakpoint`
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `border/width/thick`, `button/primary/bg`, `button/primary/border`, `button/primary/text`, `color/surface/page`, `color/text/default`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/desktop/display`, `font/line-height/desktop/h2`, `font/line-height/desktop/label`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/desktop/display`, `font/size/desktop/h2`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/sm`, `layout/margin`, `radius/pill`, `shadow/soft`, `space/16`, `space/24`, `space/64`, `space/8`
- **Text styles:** `Desktop/h2`, `Desktop/display`, `Desktop/label`, `Desktop/caption`
<!-- ⚙️ GENERATED:end:contest-result -->

- **Propósito:** Resultado de haber participado, centrado sobre crema. Tres variantes: Lose (no ha ganado: título, texto «Don't lose your one use 15% discount voucher», Voucher 15 % y botón de descarga), Win (ha ganado: imagen del premio, «Oh my noodles! / Your entry has won the prize», texto de verificación y enlace de vuelta al concurso) y Limit (ha superado el máximo de participaciones: Voucher 25 % y botón de descarga).
- **Ejemplo de código:** las tres variantes del maestro (Lose, Win y Limit), cada una en su marcado. Win sustituye el Voucher por la imagen del premio (`.contest-result__media`); Limit es igual que Lose con otro título, otro texto y el Voucher de «25% OFF».
  ```html
  <section data-ds="contest-result" class="section contest-result" aria-labelledby="cr-title">
  <div class="contest-result__inner">
  <h1 class="contest-result__title" id="cr-title">Oh crap… Your entry hasn't won a prize this time</h1>
  <p class="contest-result__text"><strong>Don't lose your one use 15% discount voucher</strong><br>Download it and use it in your next Yatekomo noodle cup purchase:</p>
  <div data-ds="voucher" class="voucher">
  <div class="voucher__main"><p class="voucher__value">15% OFF</p><p class="voucher__label">Discount voucher</p></div>
  <div class="voucher__stub"><img class="voucher__barcode" src="../assets/images/placeholder.svg" alt="Barcode 0876562-R"><span class="voucher__code" aria-hidden="true">0876562-R</span></div>
  </div>
  <a class="button button--l" href="/contests/slurp-and-win/voucher.pdf" download>Download discount voucher</a>
  </div>
  </section>

  <section data-ds="contest-result" class="section contest-result contest-result--win" aria-labelledby="cr-title-win">
  <div class="contest-result__inner">
  <figure class="contest-result__media"><img class="contest-result__image" src="../assets/images/placeholder.svg" alt="Prize won"></figure>
  <h1 class="contest-result__title" id="cr-title-win">Oh my noodles!</h1>
  <p class="contest-result__subtitle">Your entry has won the prize</p>
  <p class="contest-result__text">We'll verify your entry and send you an email to process your prize if everything is in order.</p>
  <a class="button button--l button--secondary" href="/contests/slurp-and-win">Go back to the contest site</a>
  </div>
  </section>

  <section data-ds="contest-result" class="section contest-result contest-result--limit" aria-labelledby="cr-title-limit">
  <div class="contest-result__inner">
  <h1 class="contest-result__title" id="cr-title-limit">You have surpassed the maximum participations allowed</h1>
  <p class="contest-result__text"><strong>You can't participate in this contest anymore but we'd like to reward your loyalty with a discount voucher</strong><br>Download it and use it in your next Yatekomo noodle cup purchase:</p>
  <div data-ds="voucher" class="voucher">
  <div class="voucher__main"><p class="voucher__value">25% OFF</p><p class="voucher__label">Discount voucher</p></div>
  <div class="voucher__stub"><img class="voucher__barcode" src="../assets/images/placeholder.svg" alt="Barcode 0876562-R"><span class="voucher__code" aria-hidden="true">0876562-R</span></div>
  </div>
  <a class="button button--l" href="/contests/slurp-and-win/voucher.pdf" download>Download discount voucher</a>
  </div>
  </section>
  ```
  Win y Limit llevan su clase de variante (`.contest-result--win`, `.contest-result--limit`), que sigue la convención `.<base>--<valor>`.
- **Accesibilidad (rol, nombre, estados y teclado):** Un solo h1 por página, el título del resultado (en Win, «Oh my noodles!»). El resultado se dice en el título, no con el color ni con la imagen. El botón de descarga es un enlace con `download`: su nombre es el texto visible («Download discount voucher»); el tipo de archivo se da en el texto de la página (⬜ TODO). El Voucher se lee como texto (ver Voucher). La imagen de premio tiene `alt` con el premio (en el ejemplo, un texto de marcador: ⬜ TODO). Teclado: Tab va al botón de descarga o al enlace de vuelta. Contraste: texto tinta sobre crema (más de 12:1).
- **Cuándo usar / qué NO hace:** Como pantalla de confirmación tras enviar el formulario de Contest form. No es un mensaje de error de formulario. ⬜ TODO, de negocio: la mecánica de resultado inmediato (si Lose y Win se muestran al instante o llegan después por correo), el texto de verificación del premio, el límite de participaciones (qué cuenta como «máximo superado») y la validez del cupón (15 % y 25 %). Sin estos datos no se publica: los confirma GB Foods y la agencia.
