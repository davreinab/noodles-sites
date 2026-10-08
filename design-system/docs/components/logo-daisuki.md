### Logo / Daisuki   ⚙️ synced: 2026-10-08T06:16:03Z

<!-- ⚙️ GENERATED:start:logo-daisuki -->
- **Figma:** `21:177` · página «Brand» · COMPONENT_SET · 2 variantes · última sync 2026-10-08T06:16:03Z
- **Descripción (Figma):** Logo Daisuki. Positivo vectorial; negativo en PNG. No se recolorea.
- **Anatomía:** sin instancias anidadas
- **Version:** Positive, Negative
- **Propiedades de componente:** `Version` (VARIANT, por defecto Positive)
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** unknown
- **Marcas:** igual en todas las marcas (no consume tokens de marca)
<!-- ⚙️ GENERATED:end:logo-daisuki -->

- **Propósito:** Logotipo de Daisuki en versión positiva (sobre fondos claros) y negativa (sobre tinta). Identifica la web de la marca en la Navbar, el Mobile menu y el Footer.
- **Ejemplo de código:**
  ```html
  <img class="logo" src="../assets/logos/logo-daisuki-positive.svg" alt="Daisuki">
  <img class="logo" src="../assets/logos/logo-daisuki-negative.svg" alt="Daisuki">
  ```
- **Accesibilidad (pares AA verificados):** Imagen con `alt` igual al nombre de la marca. Si es el enlace a la Home, el enlace se nombra con el logo («Daisuki») y no se añade «logo» ni «inicio» al alt. El logo no se evalúa como texto, pero se usa siempre sobre el fondo para el que está hecho: positivo sobre crema o blanco, negativo sobre tinta.
- **Cuándo usar / qué NO hace:** Archivo exportado tal cual del maestro (assets/logos); no se recrea, no se recolorea, no se deforma ni se genera con IA. Alto por defecto `--space-80`; se escala manteniendo la proporción.
