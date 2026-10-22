### Share panel   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:share-panel -->
- **Figma:** `222:2027` · página «Feedback & overlays» · COMPONENT_SET · 2 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** Share panel: contenido del modal «Share» de la ficha de receta. «Share on your socials» con Icon button Secondary M de marca (WhatsApp, Instagram, Facebook, TikTok, X, Telegram; cada uno con aria-label «Share on …» en código); «Page link» con campo de solo lectura (Icon / link + URL) y botón Secondary «Copy link» (feedback «Link copied» en aria-live). Breakpoint Mobile: campo y botón apilados. Uso: modal Share de la ficha de receta (wireframe modal-share-desktop.png / modal-share-mobile.png; Recipe hero «Share recipe»). Clase CSS: .share-panel.
- **Anatomía:** `icon-button` → Hierarchy=Secondary, Size=M, State=Default, `icon` → Icon / whatsapp, `icon-button` → Hierarchy=Secondary, Size=M, State=Default, `icon` → Icon / instagram, `icon-button` → Hierarchy=Secondary, Size=M, State=Default, `icon` → Icon / facebook, `icon-button` → Hierarchy=Secondary, Size=M, State=Default, `icon` → Icon / tiktok, `icon-button` → Hierarchy=Secondary, Size=M, State=Default, `icon` → Icon / x, `icon-button` → Hierarchy=Secondary, Size=M, State=Default, `icon` → Icon / telegram, `icon-link` → Icon / link, `copy-link` → Hierarchy=Secondary, Size=M, State=Default, `icon-leading` → Icon / arrow-right, `icon-trailing` → Icon / arrow-right
- **API:** `breakpoint`: Desktop, Mobile (por defecto Desktop)
- **Nombres en Figma:** `breakpoint` ← `Breakpoint`
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown · capas sin swap: icon-link
- **Tokens que consume:** `border/width/thick`, `button/secondary/border`, `button/secondary/text`, `color/surface/card`, `color/text/default`, `color/text/secondary`, `field/bg`, `field/border`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/body-m`, `font/line-height/desktop/label`, `font/size/desktop/body-l`, `font/size/desktop/body-m`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon-button/size/m`, `icon/color/default`, `icon/size/md`, `icon/size/sm`, `radius/lg`, `radius/md`, `radius/pill`, `space/16`, `space/24`, `space/8`
- **Text styles:** `Desktop/body-m`, `Desktop/label`
<!-- ⚙️ GENERATED:end:share-panel -->

- **Propósito:** Contenido del modal «Share» de una receta o de un producto: título «Share on your socials», fila de icon buttons para WhatsApp, Instagram, Facebook, TikTok, X y Telegram, campo «Page link» de solo lectura con la URL y botón «Copy link». El mensaje «Link copied» aparece en `share-panel__status`. Los enlaces de redes los pone la página; el copiado lo hace la página con JavaScript, porque el componente no tiene script.
- **Ejemplo de código:**
  ```html
  <div data-ds="share-panel" class="share-panel">
  <h3 class="share-panel__title">Share on your socials</h3>
  <ul class="share-panel__socials">
  <li><a class="icon-button icon-button--secondary" href="https://wa.me/" aria-label="Share on WhatsApp"><span class="icon icon-whatsapp" aria-hidden="true"></span></a></li>
  <li><a class="icon-button icon-button--secondary" href="https://www.instagram.com/" aria-label="Share on Instagram"><span class="icon icon-instagram" aria-hidden="true"></span></a></li>
  <li><a class="icon-button icon-button--secondary" href="https://www.facebook.com/" aria-label="Share on Facebook"><span class="icon icon-facebook" aria-hidden="true"></span></a></li>
  <li><a class="icon-button icon-button--secondary" href="https://www.tiktok.com/" aria-label="Share on TikTok"><span class="icon icon-tiktok" aria-hidden="true"></span></a></li>
  <li><a class="icon-button icon-button--secondary" href="https://x.com/" aria-label="Share on X"><span class="icon icon-x" aria-hidden="true"></span></a></li>
  <li><a class="icon-button icon-button--secondary" href="https://t.me/" aria-label="Share on Telegram"><span class="icon icon-telegram" aria-hidden="true"></span></a></li>
  </ul>
  <label class="share-panel__label" for="share-link">Page link</label>
  <div class="share-panel__row">
  <div class="share-panel__field"><span class="icon icon-link" aria-hidden="true"></span><input class="share-panel__input" id="share-link" type="text" value="https://example.com/recetas/spicy-noodle-salad" readonly></div>
  <button class="button button--secondary" type="button">Copy link</button>
  </div>
  <p class="share-panel__status" aria-live="polite"></p>
  </div>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Rol: sección dentro del modal (el nombre del diálogo, «Share», lo da el modal). Cada red es un enlace con icono: el icono es decorativo (`aria-hidden`) y el nombre sale de `aria-label` («Share on …»), porque no hay texto visible. Campo: `label for` da el nombre «Page link»; `readonly` impide escribir, pero el texto se puede seleccionar y copiar. Botón «Copy link»: `button type="button"`. Al copiar, «Link copied» va en `p.share-panel__status` con `aria-live="polite"`: se anuncia sin mover el foco, que se queda en el botón. Teclado: Tab recorre redes, campo y botón; Enter activa. Foco: contorno de 2 px en botones y campo (`:focus-within`). En móvil los iconos se reparten en filas y el campo y el botón se apilan.
- **Cuándo usar / qué NO hace:** Solo dentro del modal Share de receta o producto; el botón que lo abre (p. ej. «Share recipe») va en el hero. No genera la URL ni comparte nada por sí mismo: cada red abre su destino y el copiado lo gestiona la página.
