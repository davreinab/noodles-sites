### Icon button   ⚙️ synced: 2026-10-07T18:27:15Z

<!-- ⚙️ GENERATED:start:icon-button -->
- **Figma:** `33:401` · página «Icon button» · COMPONENT_SET · 24 variantes · última sync 2026-10-07T18:27:15Z
- **Descripción (Figma):** Botón solo con icono: cerrar, menú, flechas del slider, play. Mismas jerarquías y colores que Button. M 56 px (icono 24 + padding 16), L 64 px (icono 32). Accesibilidad: requiere nombre accesible (aria-label) porque no tiene texto visible.
- **Anatomía:** `icon` → Icon / close
- **Hierarchy:** Primary, Secondary, Inverse
- **Size:** M, L
- **State:** Default, Hover, Focus, Disabled
- **Propiedades de componente:** `Icon#33:125` (INSTANCE_SWAP, por defecto Icon / close), `Hierarchy` (VARIANT, por defecto Primary), `Size` (VARIANT, por defecto M), `State` (VARIANT, por defecto Default)
- **Iconos / instancias anidadas:** sí · swap: `Icon#33:125` · por defecto: Icon / close
- **Tokens que consume:** `border/width/thick`, `button/primary/bg`, `button/primary/border`, `button/primary/text`, `icon/size/md`, `radius/pill`, `space/16`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `button/primary/bg`, `button/primary/border`, `button/primary/text`
<!-- ⚙️ GENERATED:end:icon-button -->

- **Propósito:** Botón solo con icono para acciones universales: cerrar, buscar, menú, anterior y siguiente. Mismas jerarquías y colores que Button; M 56 y L 64.
- **Ejemplo de código:**
  ```html
  <button class="icon-button icon-button--secondary" type="button" aria-label="Buscar"><span class="icon icon-search" aria-hidden="true"></span></button>
  <button class="icon-button icon-button--inverse" type="button" aria-label="Cerrar menú"><span class="icon icon-close" aria-hidden="true"></span></button>
  ```
- **Accesibilidad (pares AA verificados):** Icono (elemento gráfico, mínimo 3:1): crema sobre tinta 17,2:1 en Primary, tinta sobre crema 17,2:1 en Secondary, tinta sobre crema 17,2:1 en Inverse. Rol `<button>`; el nombre sale **siempre** de `aria-label` (no hay texto visible), y si abre algo se añade `aria-expanded`/`aria-controls` (menú). Teclado: Enter y Espacio. Foco: contorno de 2 px pegado, como Button. Área táctil 56 o 64 px.
- **Cuándo usar / qué NO hace:** Solo para acciones cuyo icono se entiende sin texto (cerrar, buscar, menú, flechas de carrusel). Si la acción necesita explicación, Button con texto. No se usa como decoración ni para navegar a páginas.
