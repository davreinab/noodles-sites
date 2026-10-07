### Checkbox   ⚙️ synced: 2026-10-07T18:27:15Z

<!-- ⚙️ GENERATED:start:checkbox -->
- **Figma:** `47:302` · página «Checkbox» · COMPONENT_SET · 10 variantes · última sync 2026-10-07T18:27:15Z
- **Descripción (Figma):** Casilla de verificación: consentimiento GDPR y aceptación de bases legales de concursos. Toda la fila (caja + etiqueta) es clicable; área táctil mínima 44 px en código. Marcada: tinta con check crema (el estado se ve por la forma, no solo por color). Error: borde rojo; el mensaje va en el formulario con aria-describedby. Nunca premarcada en consentimientos.
- **Anatomía:** `check` → Icon / check
- **Checked:** False, True
- **State:** Default, Hover, Focus, Error, Disabled
- **Propiedades de componente:** `Label#47:42` (TEXT, por defecto Acepto las bases legales), `Check icon#50:7` (INSTANCE_SWAP, por defecto Icon / check), `Checked` (VARIANT, por defecto False), `State` (VARIANT, por defecto Default)
- **Iconos / instancias anidadas:** sí · swap: `Check icon#50:7` · por defecto: Icon / check
- **Tokens que consume:** `border/width/thin`, `checkbox/box-bg`, `checkbox/box-border`, `checkbox/check`, `checkbox/label`, `font/family/body`, `font/line-height/desktop/body-m`, `font/size/desktop/body-m`, `font/style/body`, `icon/size/md`, `icon/size/sm`, `radius/sm`, `space/16`
- **Text styles:** `Desktop/body-m`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `checkbox/box-bg`, `checkbox/box-border`, `checkbox/check`, `checkbox/label`, `font/family/body`, `font/line-height/desktop/body-m`, `font/size/desktop/body-m`, `font/style/body`
<!-- ⚙️ GENERATED:end:checkbox -->

- **Propósito:** Casilla de verificación con etiqueta: aceptar bases legales y privacidad, o elegir opciones independientes.
- **Ejemplo de código:**
  ```html
  <label class="checkbox">
  <input class="checkbox__input" type="checkbox" name="bases" required>
  <span class="checkbox__label">Acepto las <a class="link" href="/bases">bases legales</a></span>
  </label>
  ```
- **Accesibilidad (pares AA verificados):** Caja: borde de tinta sobre blanco 18,7:1 (≥ 3:1). Marcada: check crema sobre tinta 17,2:1; el estado se ve por el check, no solo por el relleno. Hover: fondo amarillo 12,3:1 con borde de tinta. Etiqueta tinta sobre crema 17,2:1. Rol: `<input type="checkbox">` nativo dentro de `<label>` (toda la etiqueta es clicable). Teclado: Espacio. Error: `aria-invalid="true"` y mensaje enlazado. Foco: contorno de 2 px pegado a la caja de 24 px; el área clicable incluye la etiqueta.
- **Cuándo usar / qué NO hace:** Para consentimientos y opciones que se pueden marcar a la vez. No es un interruptor de ajuste inmediato ni un filtro de catálogo (eso es Chip). Las casillas de consentimiento nunca van marcadas por defecto.
