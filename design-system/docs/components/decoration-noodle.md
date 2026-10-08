### Decoration / Noodle   ⚙️ synced: 2026-10-08T11:52:41Z

<!-- ⚙️ GENERATED:start:decoration-noodle -->
- **Figma:** `21:165` · página «Brand assets» · COMPONENT_SET · 15 variantes · última sync 2026-10-08T11:52:41Z
- **Descripción (Figma):** Fideo decorativo de marca (5 trazos). Tone=Brand usa decoration/noodle/brand, Tone=Accent decoration/noodle/accent y Tone=Texture decoration/noodle/texture (ámbar opaco, solo dentro de Decoration / Noodle texture); cambian con el modo de marca. Escalable; solo decorativo (aria-hidden).
- **Anatomía:** sin instancias anidadas
- **Shape:** 2, 3, 4, 5, 1
- **Tone:** Brand, Accent, Texture
- **Propiedades de componente:** `Shape` (VARIANT, por defecto 1), `Tone` (VARIANT, por defecto Brand)
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `decoration/noodle/brand`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `decoration/noodle/brand`
<!-- ⚙️ GENERATED:end:decoration-noodle -->

- **Propósito:** Fideo decorativo de las landings: aporta el gesto de marca en bordes de hero y secciones. Cinco formas (Shape 1–5) y tres tonos (Brand amarillo, Accent naranja, Texture ámbar para la trama de fondo).
- **Ejemplo de código:**
  ```html
  <span class="decoration-noodle" aria-hidden="true"></span>
  <span class="decoration-noodle decoration-noodle--3 decoration-noodle--accent" aria-hidden="true"></span>
  <span class="decoration-noodle decoration-noodle--2 decoration-noodle--texture" aria-hidden="true"></span>
  ```
- **Accesibilidad (pares AA verificados):** Puramente decorativo: `aria-hidden="true"`, sin foco ni interacción (`pointer-events: none`). No necesita contraste propio, y solo pasa por detrás de un texto cuando ese texto también cumple sobre el color del fideo (tinta sobre amarillo, 12,3:1, como en el Hero); con cualquier otro texto, no.
- **Cuándo usar / qué NO hace:** Como adorno en los márgenes de Hero, Banner o secciones de marca, a sangre. No lleva información, no se anima sin respetar `prefers-reduced-motion` y no se usa como separador ni como icono. El alto lo da el contenedor; el ancho sale de la proporción de cada forma.
