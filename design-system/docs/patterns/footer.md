### Footer   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:footer -->
- **Figma:** `56:167` · página «Pattern / Global» · COMPONENT_SET · 2 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** Patrón de pie (wireframe UX), en tinta: logo de marca (negativo) · enlaces Products, 100% Natural formula, Recipes, Contests, FAQS y hasta dos enlaces de campaña activa · caja de sugerencias («Do you have any ideas, complaints or cravings?» + texto + Button Primary «Send suggestions» con external-link: abre el formulario externo de Calidad) · franja legal por país (Legal notice, Privacy policy, Cookies policy, Legal basis, Contest rules, Contact) y © GBFoods. Sellos y certificados (EFSA, BREEAM): sin definir, falta información. Las redes van en el Menu. Desktop: logo y enlaces a la izquierda, caja de sugerencias a la derecha; Mobile: la caja arriba. Sin variables propias. Caja de sugerencias con estilo ticket (borde superior dentado, sombra elevation/3, giro -0.6°), como en la landing.
- **Anatomía:** `logo` → Version=Negative, `nav-link` → Type=Inline, Surface=Dark, State=Default, `icon-trailing` → Icon / arrow-right, `nav-link` → Type=Inline, Surface=Dark, State=Default, `icon-trailing` → Icon / arrow-right, `nav-link` → Type=Inline, Surface=Dark, State=Default, `icon-trailing` → Icon / arrow-right, `nav-link` → Type=Inline, Surface=Dark, State=Default, `icon-trailing` → Icon / arrow-right, `nav-link` → Type=Inline, Surface=Dark, State=Default, `icon-trailing` → Icon / arrow-right, `nav-link` → Type=Inline, Surface=Dark, State=Default, `icon-trailing` → Icon / arrow-right, `nav-link` → Type=Inline, Surface=Dark, State=Default, `icon-trailing` → Icon / arrow-right, `cta` → Hierarchy=Primary, Size=M, State=Default, `icon-leading` → Icon / arrow-right, `icon-trailing` → Icon / external-link, `legal-link` → Type=Inline, Surface=Dark, State=Default, `icon-trailing` → Icon / arrow-right, `legal-link` → Type=Inline, Surface=Dark, State=Default, `icon-trailing` → Icon / arrow-right, `legal-link` → Type=Inline, Surface=Dark, State=Default, `icon-trailing` → Icon / arrow-right, `legal-link` → Type=Inline, Surface=Dark, State=Default, `icon-trailing` → Icon / arrow-right, `legal-link` → Type=Inline, Surface=Dark, State=Default, `icon-trailing` → Icon / arrow-right, `legal-link` → Type=Inline, Surface=Dark, State=Default, `icon-trailing` → Icon / arrow-right
- **API:** `logo` (icon, por defecto Version=Negative) · `breakpoint`: Desktop, Mobile (por defecto Desktop)
- **Nombres en Figma:** `logo` ← `Logo#56:0`, `breakpoint` ← `Breakpoint`
- **Iconos / instancias anidadas:** sí · swap: `logo` · por defecto: Version=Negative
- **Tokens que consume:** `border/width/thick`, `border/width/thin`, `button/primary/bg`, `button/primary/border`, `button/primary/text`, `color/border/subtle`, `color/surface/inverse`, `color/surface/page`, `color/text/default`, `color/text/on-inverse`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-m`, `font/line-height/desktop/caption`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/size/desktop/body-m`, `font/size/desktop/caption`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/color/default`, `icon/size/sm`, `layout/frame`, `layout/margin`, `link/inverse`, `radius/pill`, `shadow/soft`, `space/16`, `space/24`, `space/32`, `space/48`, `space/64`, `space/8`
- **Text styles:** `Desktop/body-m`, `Desktop/h3`, `Desktop/label`, `Desktop/caption`
<!-- ⚙️ GENERATED:end:footer -->

- **Propósito:** Pie de todas las páginas (wireframe UX): logo, enlaces (con hasta dos de campaña), caja de sugerencias al formulario externo de Calidad y franja legal por país.
- **Ejemplo de código:**
  ```html
  <footer data-ds="footer" class="footer">
  <div class="footer__main">
  <div class="footer__brand"><img class="logo" src="../assets/logos/logo-yatekomo-negative.svg" alt="Yatekomo"></div>
  <nav class="footer__column" aria-label="Pie">
  <ul class="footer__links"><li><a class="link link--dark" href="/productos">Products</a></li><li><a class="link link--dark" href="/recetas">Recipes</a></li></ul>
  </nav>
  <div class="footer__ticket">
  <div class="footer__ticket-copy"><h2 class="footer__ticket-title">Do you have any ideas, complaints or cravings?</h2><p class="footer__ticket-text">Cut to the chase and tell us what you think.</p></div>
  <a class="button" href="https://calidad.example.org" target="_blank" rel="noopener">Send suggestions <span class="icon icon-external-link" aria-hidden="true"></span><span class="visually-hidden"> (abre en una pestaña nueva)</span></a>
  </div>
  </div>
  <div class="footer__legal"><a class="link link--dark" href="/aviso-legal">Legal notice</a><a class="link link--dark" href="/privacidad">Privacy policy</a><span>© GBFoods</span></div>
  </footer>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Enlaces crema sobre tinta 17:1; la caja de sugerencias, tinta sobre crema 17,2:1 con Button Primary. El botón externo avisa de que abre otra pestaña. Los enlaces legales están en el HTML de todas las páginas.
- **Cuándo usar / qué NO hace:** En todas las páginas. Los textos legales cambian por país. Sellos y certificados (EFSA, BREEAM): sin definir, falta información. Las redes van en el Mobile menu, no aquí.
