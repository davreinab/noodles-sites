### Decoration / Noodle   ⚙️ synced: 2026-10-07T18:43:11Z

<!-- ⚙️ GENERATED:start:decoration-noodle -->
- **Figma:** `21:165` · página «Decoration» · COMPONENT_SET · 10 variantes · última sync 2026-10-07T18:43:11Z
- **Descripción (Figma):** Fideo decorativo de marca (5 trazos). Tone=Brand usa decoration/noodle/brand y Tone=Accent decoration/noodle/accent; ambos cambian con el modo de marca. Escalable; solo decorativo (aria-hidden).
- **Anatomía:** sin instancias anidadas
- **Shape:** 2, 3, 4, 5, 1
- **Tone:** Brand, Accent
- **Propiedades de componente:** `Shape` (VARIANT, por defecto 1), `Tone` (VARIANT, por defecto Brand)
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `decoration/noodle/brand`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `decoration/noodle/brand`
<!-- ⚙️ GENERATED:end:decoration-noodle -->

- **Propósito:** Fideo decorativo de las landings: aporta el gesto de marca en bordes de hero y secciones. Cinco formas (Shape 1–5) y dos tonos (Brand amarillo, Accent naranja).
- **Ejemplo de código:**
  ```html
  <span class="decoration-noodle" aria-hidden="true"></span>
  <span class="decoration-noodle decoration-noodle--3 decoration-noodle--accent" aria-hidden="true"></span>
  ```
- **Accesibilidad (pares AA verificados):** Puramente decorativo: `aria-hidden="true"`, sin foco ni interacción (`pointer-events: none`). No necesita contraste propio, pero nunca pasa por detrás de un texto: si lo tocara, el par texto/fondo dejaría de ser verificable.
- **Cuándo usar / qué NO hace:** Como adorno en los márgenes de Hero, Banner o secciones de marca, a sangre. No lleva información, no se anima sin respetar `prefers-reduced-motion` y no se usa como separador ni como icono. El alto lo da el contenedor; el ancho sale de la proporción de cada forma.
