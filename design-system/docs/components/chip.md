### Chip   ⚙️ synced: 2026-10-07T18:43:11Z

<!-- ⚙️ GENERATED:start:chip -->
- **Figma:** `35:186` · página «Chip» · COMPONENT_SET · 8 variantes · última sync 2026-10-07T18:43:11Z
- **Descripción (Figma):** Píldora compacta para productos dentro de una receta (enlaza a la ficha) y para filtros. Size: S 36 px (filtros densos, productos en receta) · M 40 px (filtros principales, uso táctil preferente); altura mínima ligada a chip/height/*. Selected cuando el filtro está activo; el estado no se comunica solo por color: Selected muestra el icono check. Icon leading opcional (INSTANCE_SWAP).
- **Anatomía:** `icon-leading` → Icon / check
- **Size:** S, M
- **State:** Default, Hover, Selected, Disabled
- **Propiedades de componente:** `Label#35:17` (TEXT, por defecto Yatekomo Original), `Icon leading#35:22` (BOOLEAN, por defecto False), `Icon leading swap#35:27` (INSTANCE_SWAP, por defecto Icon / check), `Size` (VARIANT, por defecto S), `State` (VARIANT, por defecto Default)
- **Iconos / instancias anidadas:** sí · swap: `Icon leading swap#35:27` · por defecto: Icon / check
- **Tokens que consume:** `border/width/thin`, `chip/bg`, `chip/border`, `chip/height/s`, `chip/text`, `font/family/body`, `font/line-height/desktop/body-s`, `font/size/desktop/body-s`, `font/style/body`, `icon/size/sm`, `radius/pill`, `space/16`, `space/8`
- **Text styles:** `Desktop/body-s`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `chip/bg`, `chip/border`, `chip/text`, `font/family/body`, `font/line-height/desktop/body-s`, `font/size/desktop/body-s`, `font/style/body`
<!-- ⚙️ GENERATED:end:chip -->

- **Propósito:** Píldora compacta para filtrar (líneas y sabores del Product filter) y para enlazar productos dentro de una receta. Size S 36 en filtros densos; M 40 como opción táctil preferente.
- **Ejemplo de código:**
  ```html
  <button class="chip" type="button" aria-pressed="false">Yakisoba</button>
  <button class="chip" type="button" aria-pressed="true"><span class="icon icon-check" aria-hidden="true"></span>Original</button>
  <a class="chip chip--m" href="/productos/yatekomo-original">Yatekomo Original</a>
  ```
- **Accesibilidad (pares AA verificados):** Default: tinta sobre blanco 18,7:1; borde de tinta sobre crema 17,2:1 (≥ 3:1). Hover: tinta sobre amarillo 12,3:1. Selected: crema sobre tinta 17,2:1 y con icono check, así que el estado no depende solo del color. Disabled: gris cálido sobre arena 4,3:1 (exento). Rol: como filtro, `<button aria-pressed>` dentro de un grupo con nombre (`role="group" aria-label="Línea"`); como producto, `<a>`. Teclado: Tab entre chips y Enter/Espacio para alternar. Foco: contorno de 2 px pegado en tinta. Área táctil: S mide 36 px, por debajo de 44; se compensa con `--space-8` entre chips (cumple el mínimo de 24 px de WCAG 2.5.8). Para uso táctil principal, M.
- **Cuándo usar / qué NO hace:** Para filtros de selección múltiple o única y para productos citados en una receta. No es la acción principal (Button), no es una etiqueta informativa (Badge) y no navega entre pestañas de contenido (Tab).
