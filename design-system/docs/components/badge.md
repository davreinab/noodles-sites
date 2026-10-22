### Badge   ⚙️ synced: 2026-10-22T09:37:04Z

<!-- ⚙️ GENERATED:start:badge -->
- **Figma:** `35:167` · página «Tags & chips» · COMPONENT_SET · 3 variantes · última sync 2026-10-22T09:37:04Z
- **Descripción (Figma):** Etiqueta corta en Anton mayúsculas. New: «Nuevo» (rojo pack). Natural: claims de naturalidad (verde 356). Neutral: formato o línea (Cup, Bag, Sauce). No es interactivo; no usar como botón.
- **Anatomía:** sin instancias anidadas
- **API:** `label` (string, por defecto Nuevo) · `type`: New, Natural, Neutral (por defecto New)
- **Nombres en Figma:** `label` ← `Label#35:13`, `type` ← `Type`
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `badge/new/bg`, `badge/new/text`, `font/family/display`, `font/line-height/mobile/label`, `font/size/mobile/label`, `font/style/display`, `radius/pill`, `space/4`, `space/8`
- **Text styles:** `Mobile/label`
<!-- ⚙️ GENERATED:end:badge -->

- **Propósito:** Etiqueta corta de estado o atributo: «Nuevo», «100 % natural», «En curso», «Finalizado», claims como «−20 %». New en rojo de packaging, Natural en verde y Neutral en tinta.
- **Ejemplo de código:**
  ```html
  <span data-ds="badge" class="badge">Nuevo</span>
  <span data-ds="badge" class="badge badge--natural">100 % natural</span>
  <span data-ds="badge" class="badge badge--neutral">Finalizado</span>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** New: blanco sobre rojo 4,7:1. Natural: blanco sobre verde 5,5:1. Neutral: crema sobre tinta 17,2:1. Texto en mayúsculas de Anton a 14 px: los tres pares superan 4,5:1. No es interactivo (sin foco ni rol); su texto se lee en el orden del contenido. El estado lo dice la palabra, nunca solo el color.
- **Cuándo usar / qué NO hace:** Para marcar un estado o un atributo de un producto, concurso o claim. Máximo dos por card. No es un botón ni un filtro (eso es Chip) y no lleva frases: una o dos palabras.
