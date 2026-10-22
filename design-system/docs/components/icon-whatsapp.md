### Icon / whatsapp   ⚙️ synced: 2026-10-22T14:07:02Z

<!-- ⚙️ GENERATED:start:icon-whatsapp -->
- **Figma:** `208:66` · página «Iconography» · COMPONENT · 1 variantes · última sync 2026-10-22T14:07:02Z
- **Descripción (Figma):** Logo de WhatsApp (Simple Icons, CC0), relleno, 24×24. Uso: botón «Share on WhatsApp» del Share panel (wireframe 396:6290).
- **Anatomía:** sin instancias anidadas
- **API:** sin propiedades
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `icon/color/default`
<!-- ⚙️ GENERATED:end:icon-whatsapp -->

- **Propósito:** Logo de WhatsApp del botón «Share on WhatsApp» del Share panel.
- **Ejemplo de código:** Glifo sobre la máscara `.icon`; el color lo toma de `color` (currentColor).
  ```html
  <span data-ds="icon-whatsapp" class="icon icon-whatsapp" aria-hidden="true"></span>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Icono decorativo: `aria-hidden="true"`. El nombre accesible lo da el enlace con `aria-label` («Share on WhatsApp»).
- **Cuándo usar / qué NO hace:** Icono de marca. Lo usa `share-panel` dentro de un `icon-button` con `aria-label` («Share on WhatsApp»). Solo como glifo dentro de un botón con nombre accesible. No es un botón ni un enlace: el contenedor pone la interacción.
