### Product card   ⚙️ synced: 2026-10-07T18:27:15Z

<!-- ⚙️ GENERATED:start:product-card -->
- **Figma:** `66:99` · página «Product card» · COMPONENT_SET · 3 variantes · última sync 2026-10-07T18:27:15Z
- **Descripción (Figma):** Card de producto (Product library, carruseles, productos relacionados). Anatomía: media (hueco de imagen 3D sobre product-card/media-bg; no se inventa fotografía) con Badge opcional (New/Natural) · línea (Original/Yakisoba/Rice) · nombre (h3) · Link «Ver producto». Toda la card es un único enlace al producto (el Link es la pista visual, no un segundo destino). Hover: elevation/2; Focus: anillo product-card/focus-ring. Desktop 320 px; en móvil ocupa la columna (FILL).
- **Anatomía:** `badge` → Type=New, `link` → Type=Standalone, Surface=Light, State=Default, `icon-trailing` → Icon / arrow-right
- **State:** Default, Hover, Focus
- **Propiedades de componente:** `Name#66:0` (TEXT, por defecto Nombre del producto), `Line#66:4` (TEXT, por defecto Original), `Badge#66:8` (BOOLEAN, por defecto True), `State` (VARIANT, por defecto Default)
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `badge/new/bg`, `badge/new/text`, `border/width/thin`, `color/effect/shadow-ink`, `font/family/body`, `font/family/display`, `font/line-height/desktop/caption`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/line-height/mobile/label`, `font/size/desktop/caption`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/size/mobile/label`, `font/style/body`, `font/style/display`, `icon/size/sm`, `link/default`, `product-card/bg`, `product-card/border`, `product-card/media-bg`, `product-card/meta`, `product-card/title`, `radius/md`, `radius/none`, `radius/pill`, `space/16`, `space/24`, `space/4`, `space/8`
- **Text styles:** `Mobile/label`, `Desktop/caption`, `Desktop/h3`, `Desktop/label`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `badge/new/bg`, `badge/new/text`, `color/effect/shadow-ink`, `font/family/body`, `font/family/display`, `font/line-height/desktop/caption`, `font/line-height/desktop/h3`, `font/line-height/desktop/label`, `font/line-height/mobile/label`, `font/size/desktop/caption`, `font/size/desktop/h3`, `font/size/desktop/label`, `font/size/mobile/label`, `font/style/body`, `font/style/display`, `link/default`, `product-card/bg`, `product-card/border`, `product-card/media-bg`, `product-card/meta`, `product-card/title`
<!-- ⚙️ GENERATED:end:product-card -->

- **Propósito:** Card de producto para la Product library, el Product carousel y los productos relacionados. Toda la card es un único enlace a la ficha del producto.
- **Ejemplo de código:**
  ```html
  <a class="product-card" href="/productos/yatekomo-pollo">
  <div class="product-card__media">
  <span class="badge">Nuevo</span>
  <img src="/media/yatekomo-pollo-3d.png" alt="">
  </div>
  <div class="product-card__body">
  <span class="product-card__line">Original</span>
  <h3 class="product-card__name">Yatekomo Pollo</h3>
  <span class="product-card__cta"><span class="link link--standalone">Ver producto <span class="icon icon-arrow-right" aria-hidden="true"></span></span></span>
  </div>
  </a>
  ```
- **Accesibilidad (pares AA verificados):** Nombre tinta sobre blanco 18,7:1; línea gris cálido sobre blanco 5,9:1; hueco de imagen crema; borde de tinta sobre crema 17,2:1. Rol: un solo `<a>`; su nombre es el texto de la card (Badge, línea, nombre y «Ver producto»), por eso la imagen va con `alt=""` (decorativa: el nombre ya está en texto). «Ver producto» es una pista visual dentro del enlace, no un segundo enlace. Teclado: un solo tabulador por card. Foco: contorno de 2 px pegado que sigue el radio; hover sube a `--elevation-2` y respeta reduce-motion porque solo cambia la sombra.
- **Cuándo usar / qué NO hace:** En rejillas y carruseles de producto. No lleva botones ni enlaces dentro (sería un enlace anidado); si hace falta una segunda acción, va fuera de la card. La foto es la de marca (3D o girosu), nunca generada con IA.
