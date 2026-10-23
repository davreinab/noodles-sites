### Voucher   ⚙️ synced: 2026-10-23T09:22:57Z

<!-- ⚙️ GENERATED:start:voucher -->
- **Figma:** `308:2421` · página «Cards» · COMPONENT · 1 variantes · última sync 2026-10-23T09:22:57Z
- **Descripción (Figma):** Voucher: cupón de descuento que se descarga tras participar (resultado Lose y Limit del bloque Contest result, wireframe 490:13618 y 490:13867). Estilo ticket de la landing (.ideas__ticket): papel en surface/page con borde dentado (vector ticket-paper clonado del pie 184:114), sombra shadow/soft y giro -0.6°. Texto Discount (display, «15% OFF» o «25% OFF»), caption «Discount Voucher», código de barras (placeholder rectangular) y código «0876562-R» en vertical. Clase CSS: .voucher. ⬜ TODO GB Foods/agencia: código de barras real, formato del código y porcentaje de la mecánica de límite.
- **Anatomía:** sin instancias anidadas
- **API:** `discount` (string, por defecto 15% OFF)
- **Nombres en Figma:** `discount` ← `Discount#308:29`
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `color/surface/page`, `color/text/default`, `color/text/secondary`, `font/family/body`, `font/family/display`, `font/line-height/desktop/caption`, `font/line-height/desktop/display`, `font/line-height/desktop/label`, `font/size/desktop/caption`, `font/size/desktop/display`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `shadow/soft`, `space/24`
- **Text styles:** `Desktop/display`, `Desktop/label`, `Desktop/caption`
<!-- ⚙️ GENERATED:end:voucher -->

- **Propósito:** Cupón de descuento con el estilo ticket del pie de la landing: papel crema, borde superior dentado, sin radio y giro leve. Muestra el porcentaje («15% OFF» o «25% OFF»), la etiqueta «Discount voucher», un código de barras y el código de cupón en vertical.
- **Ejemplo de código:** Descuento del 15 %; para el 25 % cambia solo el texto del valor y el código.
  ```html
  <div data-ds="voucher" class="voucher">
  <div class="voucher__main">
  <p class="voucher__value">15% OFF</p>
  <p class="voucher__label">Discount voucher</p>
  </div>
  <div class="voucher__stub">
  <img class="voucher__barcode" src="../assets/images/placeholder.svg" alt="Barcode 0876562-R">
  <span class="voucher__code" aria-hidden="true">0876562-R</span>
  </div>
  </div>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Es texto: el valor («15% OFF») y la etiqueta se leen en orden. El código de barras es una imagen con `alt` que dice el código, para que quien no ve el código de barras tenga el dato. El código vertical va con `aria-hidden` para no repetirlo. No es interactivo; el botón de descarga va aparte (en Contest result). Contraste: tinta sobre crema (más de 12:1); etiqueta y código en gris cálido sobre crema (5,4:1). La sombra y el contorno son decorativos.
- **Cuándo usar / qué NO hace:** Solo en Contest result (variantes Lose y Limit). No es un cupón de producto genérico ni un código que se pueda copiar: el código real y el porcentaje son ⬜ TODO (GB Foods). Hay que confirmar la validez del cupón y el texto legal de uso antes de publicarlo. El contorno fino es una aproximación con sombra de 2 px: el clip-path no admite filete, así que el borde no es idéntico al del maestro.
