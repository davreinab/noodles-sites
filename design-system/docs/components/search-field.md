### Search field   ⚙️ synced: 2026-10-07T18:41:16Z

<!-- ⚙️ GENERATED:start:search-field -->
- **Figma:** `48:177` · página «Search field» · COMPONENT_SET · 4 variantes · última sync 2026-10-07T18:41:16Z
- **Descripción (Figma):** Campo de búsqueda (resultados en modal). Sin etiqueta visible: requiere aria-label («Buscar») y role=&quot;search&quot; en el formulario. Lupa delante; con texto aparece el botón borrar (aria-label «Borrar búsqueda»). Forma pill para distinguirlo de los campos de formulario. El valor se edita en la instancia.
- **Anatomía:** `icon-search` → Icon / search, `icon-clear` → Icon / close
- **State:** Default, Hover, Focus, Filled
- **Propiedades de componente:** `Icon leading#51:0` (INSTANCE_SWAP, por defecto Icon / search), `Clear icon#51:5` (INSTANCE_SWAP, por defecto Icon / close), `State` (VARIANT, por defecto Default)
- **Iconos / instancias anidadas:** sí · swap: `Icon leading#51:0`, `Clear icon#51:5` · por defecto: Icon / search, Icon / close
- **Tokens que consume:** `border/width/thin`, `field/bg`, `field/border`, `field/icon`, `field/placeholder`, `font/family/body`, `font/line-height/desktop/body-m`, `font/size/desktop/body-m`, `font/style/body`, `icon/size/md`, `radius/pill`, `space/16`, `space/8`
- **Text styles:** `Desktop/body-m`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `field/bg`, `field/border`, `field/icon`, `field/placeholder`, `font/family/body`, `font/line-height/desktop/body-m`, `font/size/desktop/body-m`, `font/style/body`
<!-- ⚙️ GENERATED:end:search-field -->

- **Propósito:** Buscador de recetas y productos en píldora: lupa, campo y botón de borrar cuando hay texto.
- **Ejemplo de código:**
  ```html
  <form class="search-field" role="search" action="/buscar">
  <span class="icon icon-search" aria-hidden="true"></span>
  <label class="visually-hidden" for="q">Buscar recetas y productos</label>
  <input class="search-field__input" id="q" name="q" type="search" placeholder="Buscar recetas y productos">
  <button class="search-field__clear" type="button" aria-label="Borrar búsqueda"><span class="icon icon-close" aria-hidden="true"></span></button>
  </form>
  ```
- **Accesibilidad (pares AA verificados):** Texto tinta sobre blanco 18,7:1; placeholder gris cálido sobre blanco 5,9:1; iconos y borde tinta (≥ 3:1). Rol: `<form role="search">` con `<input type="search">` y etiqueta (oculta visualmente porque el placeholder no cuenta como nombre). Borrar es un `<button>` con `aria-label` y devuelve el foco al campo. Los resultados se anuncian («N resultados») con aria-live. Foco: el contorno rodea la píldora entera (`:focus-within`).
- **Cuándo usar / qué NO hace:** Para buscar en la web (Navbar y página de resultados). No filtra el catálogo (eso es Product filter) y no se usa como campo de formulario genérico.
