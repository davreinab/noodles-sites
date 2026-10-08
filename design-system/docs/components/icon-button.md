### Icon button   ⚙️ synced: 2026-10-08T06:16:03Z

<!-- ⚙️ GENERATED:start:icon-button -->
- **Figma:** `33:401` · página «Icon button» · COMPONENT_SET · 24 variantes · última sync 2026-10-08T06:16:03Z
- **Descripción (Figma):** Botón solo con icono: cerrar, menú, flechas del slider, play. Mismas jerarquías y colores que Button. M 48 px (icono 24), L 64 px (icono 32). Accesibilidad: requiere nombre accesible (aria-label) porque no tiene texto visible. Tamaño fijo con icon-button/size/m (48) y /l (64), icono centrado. Norma de botones (2026-10-07): misma altura en la misma talla para Button e Icon button (M 48, L 64); en Button, el texto siempre en una sola línea.
- **Anatomía:** `icon` → Icon / close
- **Hierarchy:** Primary, Secondary, Inverse
- **Size:** M, L
- **State:** Default, Hover, Focus, Disabled
- **Propiedades de componente:** `Icon#33:125` (INSTANCE_SWAP, por defecto Icon / close), `Hierarchy` (VARIANT, por defecto Primary), `Size` (VARIANT, por defecto M), `State` (VARIANT, por defecto Default)
- **Iconos / instancias anidadas:** sí · swap: `Icon#33:125` · por defecto: Icon / close
- **Tokens que consume:** `border/width/thick`, `button/primary/bg`, `button/primary/border`, `button/primary/text`, `icon-button/size/m`, `icon/size/md`, `radius/pill`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `button/primary/bg`, `button/primary/border`, `button/primary/text`
<!-- ⚙️ GENERATED:end:icon-button -->

- **Propósito:** Botón solo con icono para acciones universales: cerrar, buscar, menú, anterior y siguiente. Mismas jerarquías y colores que Button; M 48 y L 64, la misma altura que Button.
- **Ejemplo de código:**
  ```html
  <button class="icon-button icon-button--secondary" type="button" aria-label="Buscar"><span class="icon icon-search" aria-hidden="true"></span></button>
  <button class="icon-button icon-button--inverse" type="button" aria-label="Cerrar menú"><span class="icon icon-close" aria-hidden="true"></span></button>
  ```
- **Accesibilidad (pares AA verificados):** Icono (elemento gráfico, mínimo 3:1): crema sobre tinta 17,2:1 en Primary, tinta sobre crema 17,2:1 en Secondary, tinta sobre crema 17,2:1 en Inverse. Rol `<button>`; el nombre sale **siempre** de `aria-label` (no hay texto visible), y si abre algo se añade `aria-expanded`/`aria-controls` (menú). Teclado: Enter y Espacio. Foco: contorno de 2 px pegado, como Button. Área táctil 48 o 64 px (≥ 44).
- **Cuándo usar / qué NO hace:** **Norma de botones:** Button e Icon button tienen la misma altura en la misma talla (M 48 px, L 64 px), así que se pueden poner juntos sin desalinearse. El texto de Button va siempre en una sola línea (`white-space: nowrap`): si no cabe, se acorta el texto; nunca se parte en dos líneas. Solo para acciones cuyo icono se entiende sin texto (cerrar, buscar, menú, flechas de carrusel). Si la acción necesita explicación, Button con texto. No se usa como decoración ni para navegar a páginas.
