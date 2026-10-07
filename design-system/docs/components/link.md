### Link   ⚙️ synced: 2026-10-07T18:49:29Z

<!-- ⚙️ GENERATED:start:link -->
- **Figma:** `35:107` · página «Link» · COMPONENT_SET · 12 variantes · última sync 2026-10-07T18:49:29Z
- **Descripción (Figma):** Enlace. Inline: dentro de un párrafo, siempre subrayado (no se distingue solo por color). Standalone: enlace suelto en Anton con flecha (p. ej. «Ver todas las recetas»), subrayado en hover. Surface Dark para fondos surface/inverse. Enlaces externos: icono external-link y aviso de que abre fuera. El texto se edita directamente en la instancia (sin propiedad de texto, para conservar el formato por variante).
- **Anatomía:** `icon-trailing` → Icon / arrow-right
- **Type:** Inline, Standalone
- **Surface:** Light, Dark
- **State:** Default, Hover, Focus
- **Propiedades de componente:** `Icon#35:0` (INSTANCE_SWAP, por defecto Icon / arrow-right), `Type` (VARIANT, por defecto Inline), `Surface` (VARIANT, por defecto Light), `State` (VARIANT, por defecto Default)
- **Iconos / instancias anidadas:** sí · swap: `Icon#35:0` · por defecto: Icon / arrow-right
- **Tokens que consume:** `font/family/body`, `font/line-height/desktop/body-m`, `font/size/desktop/body-m`, `font/style/body`, `icon/size/sm`, `link/default`, `space/8`
- **Text styles:** `Desktop/body-m`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `font/family/body`, `font/line-height/desktop/body-m`, `font/size/desktop/body-m`, `font/style/body`, `link/default`
<!-- ⚙️ GENERATED:end:link -->

- **Propósito:** Enlace de navegación. Inline va dentro de un texto, subrayado; Standalone es un enlace suelto en Anton mayúsculas con flecha («Ver todas las recetas»). Surface Dark para fondos de tinta.
- **Ejemplo de código:**
  ```html
  <p>Consulta las <a class="link" href="/bases">bases legales</a> del concurso.</p>
  <a class="link link--standalone" href="/recetas">Ver todas las recetas <span class="icon icon-arrow-right" aria-hidden="true"></span></a>
  <a class="link link--dark" href="/contacto" target="_blank" rel="noopener">Contacto <span class="icon icon-external-link" aria-hidden="true"></span><span class="visually-hidden"> (abre en una pestaña nueva)</span></a>
  ```
- **Accesibilidad (pares AA verificados):** Light: tinta sobre crema 17,2:1 y sobre blanco 18,7:1; hover verde natural sobre crema 5,0:1 y sobre blanco 5,5:1. Dark: crema sobre tinta 17,2:1; hover amarillo sobre tinta 12,3:1. Inline se distingue del texto por el subrayado, no solo por el color. Rol `<a href>`; nombre: el texto visible (la flecha va `aria-hidden`). Externos: icono external-link y aviso «(abre en una pestaña nueva)» en texto oculto. Teclado: Enter. Foco: contorno de 2 px pegado con `--link-focus-ring` (amarillo `--link-inverse-focus-ring` en Dark).
- **Cuándo usar / qué NO hace:** Para ir a otra página o sección (incluidas bases legales, contacto y enlaces del footer). No dispara acciones en la página (eso es Button) y no sustituye al CTA principal. Standalone no va dentro de un párrafo; Inline no lleva flecha.
