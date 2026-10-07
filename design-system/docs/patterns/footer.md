### Footer   ⚙️ synced: 2026-10-07T18:30:51Z

<!-- ⚙️ GENERATED:start:footer -->
- **Figma:** `56:167` · página «Pattern / Footer» · COMPONENT_SET · 2 variantes · última sync 2026-10-07T18:30:51Z
- **Descripción (Figma):** Patrón de pie, en tinta: logo de marca (negativo) y GB Foods · navegación · contacto (formulario externo de GB Foods, icono external-link) · redes · franja legal por país (Privacy, Legal notice, Cookies, Lawful basis, Contest rules) y ©. Los textos legales cambian por país. Sin variables propias: compone Link, Icon y Logo con semánticos.
- **Anatomía:** `logo` → Version=Negative, `logo-gb-foods` → Logo / GB Foods, `nav-link` → Type=Inline, Surface=Dark, State=Default, `icon-trailing` → Icon / arrow-right, `nav-link` → Type=Inline, Surface=Dark, State=Default, `icon-trailing` → Icon / arrow-right, `nav-link` → Type=Inline, Surface=Dark, State=Default, `icon-trailing` → Icon / arrow-right, `nav-link` → Type=Inline, Surface=Dark, State=Default, `icon-trailing` → Icon / arrow-right, `nav-link` → Type=Inline, Surface=Dark, State=Default, `icon-trailing` → Icon / arrow-right, `contact-link` → Type=Standalone, Surface=Dark, State=Default, `icon-trailing` → Icon / external-link, `social` → Icon / tiktok, `social` → Icon / instagram, `social` → Icon / x, `social` → Icon / youtube, `legal-link` → Type=Inline, Surface=Dark, State=Default, `icon-trailing` → Icon / arrow-right, `legal-link` → Type=Inline, Surface=Dark, State=Default, `icon-trailing` → Icon / arrow-right, `legal-link` → Type=Inline, Surface=Dark, State=Default, `icon-trailing` → Icon / arrow-right, `legal-link` → Type=Inline, Surface=Dark, State=Default, `icon-trailing` → Icon / arrow-right, `legal-link` → Type=Inline, Surface=Dark, State=Default, `icon-trailing` → Icon / arrow-right
- **Breakpoint:** Desktop, Mobile
- **Propiedades de componente:** `Logo#56:0` (INSTANCE_SWAP, por defecto Version=Negative), `Social 1#57:0` (INSTANCE_SWAP, por defecto Icon / tiktok), `Social 2#57:3` (INSTANCE_SWAP, por defecto Icon / instagram), `Social 3#57:6` (INSTANCE_SWAP, por defecto Icon / x), `Social 4#57:9` (INSTANCE_SWAP, por defecto Icon / youtube), `Breakpoint` (VARIANT, por defecto Desktop)
- **Iconos / instancias anidadas:** sí · swap: `Logo#56:0`, `Social 1#57:0`, `Social 2#57:3`, `Social 3#57:6`, `Social 4#57:9` · por defecto: Version=Negative, Icon / tiktok, Icon / instagram, Icon / x, Icon / youtube
- **Tokens que consume:** `border/width/thin`, `color/border/subtle`, `color/surface/inverse`, `color/text/on-inverse`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/desktop/label`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/color/default`, `icon/color/inverse`, `icon/size/md`, `icon/size/sm`, `layout/frame`, `layout/margin`, `link/inverse`, `space/16`, `space/24`, `space/32`, `space/48`, `space/64`, `space/8`
- **Text styles:** `Desktop/body-m`, `Desktop/label`, `Desktop/caption`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `color/border/subtle`, `color/surface/inverse`, `color/text/on-inverse`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/desktop/label`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/color/default`, `icon/color/inverse`, `link/inverse`
<!-- ⚙️ GENERATED:end:footer -->

- **Propósito:** Pie en tinta de todas las páginas: logo de marca y de GB Foods, navegación, contacto (formulario externo de GB Foods), redes y franja legal por país.
- **Ejemplo de código:**
  ```html
  <footer class="footer">
  <div class="footer__main">
  <div class="footer__brand"><img class="logo" src="../assets/logos/logo-yatekomo-negative.svg" alt="Yatekomo"><img class="logo logo--gb-foods" src="../assets/logos/logo-gb-foods.svg" alt="GB Foods"></div>
  <nav class="footer__column" aria-label="Pie">
  <h2 class="footer__title">Explora</h2>
  <ul class="footer__links"><li><a class="link link--dark" href="/productos">Productos</a></li><li><a class="link link--dark" href="/recetas">Recetas</a></li></ul>
  </nav>
  <div class="footer__column">
  <a class="link link--standalone link--dark" href="https://www.gbfoods.com/contacto" target="_blank" rel="noopener">Contacto <span class="icon icon-external-link" aria-hidden="true"></span><span class="visually-hidden"> (abre en una pestaña nueva)</span></a>
  <ul class="footer__social" aria-label="Redes sociales"><li><a class="link link--dark" href="https://www.instagram.com/" aria-label="Instagram"><span class="icon icon-instagram" aria-hidden="true"></span></a></li></ul>
  </div>
  </div>
  <div class="footer__legal"><a class="link link--dark" href="/privacidad">Privacy</a><a class="link link--dark" href="/cookies">Cookies</a><span>© 2026 GB Foods</span></div>
  </footer>
  ```
- **Accesibilidad (pares AA verificados):** Crema sobre tinta 17,2:1; enlaces en hover amarillo 12,3:1; iconos sociales crema (≥ 3:1). El filete de la franja legal es decorativo. Landmark `<footer>` con su `<nav>`; las redes son enlaces con nombre de la red. Los textos legales cambian por país (Privacy, Legal notice, Cookies, Lawful basis, Contest rules).
- **Cuándo usar / qué NO hace:** Uno por página. No repite la navegación completa ni lleva formularios (el contacto es externo). Los sellos de marca se añaden aquí cuando GB Foods los entregue.
