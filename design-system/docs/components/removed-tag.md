### Removed tag   ⚙️ synced: 2026-10-22T15:21:21Z

<!-- ⚙️ GENERATED:start:removed-tag -->
- **Figma:** `276:51` · página «Tags & chips» · COMPONENT · 1 variantes · última sync 2026-10-22T15:21:21Z
- **Descripción (Figma):** Removed tag: píldora de ingrediente retirado de la fórmula natural (Natural formula, wireframe UX 274:6354; clase CSS .removed-tag). Icono x (close) a la izquierda y texto tachado en color/text/secondary; el texto oculto «removed:» va delante para lectores de pantalla, porque el tachado por sí solo no comunica el estado. Se usa en «We also removed» (Natural improvement) y dentro de Ingredient swap. Label: nombre del ingrediente retirado, p. ej. «Preservatives» (ejemplo ⬜ TODO envase).
- **Anatomía:** `icon` → Icon / close
- **API:** `label` (string, por defecto Preservatives)
- **Nombres en Figma:** `label` ← `Label#276:0`
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown · capas sin swap: icon
- **Tokens que consume:** `color/border/subtle`, `color/surface/card`, `color/text/secondary`, `font/family/body`, `font/line-height/desktop/body-s`, `font/size/desktop/body-s`, `font/style/body`, `icon/color/default`, `radius/pill`, `space/16`, `space/8`
- **Text styles:** `Desktop/body-s`
<!-- ⚙️ GENERATED:end:removed-tag -->

- **Propósito:** Píldora que marca un ingrediente retirado de la fórmula: icono x y el nombre tachado. Se usa sola en «We also removed» y dentro de Ingredient swap, donde el ingrediente retirado va arriba del sustituto.
- **Ejemplo de código:**
  ```html
  <span data-ds="removed-tag" class="removed-tag"><span class="icon icon-close" aria-hidden="true"></span><span class="visually-hidden">Removed:</span><s class="removed-tag__text">Preservatives</s></span>
  ```
  Variante Desktop y Mobile: mismo marcado; en móvil cambia solo el tamaño de letra (media query de `components.css`).
- **Accesibilidad (rol, nombre, estados y teclado):** Sin rol propio: es texto en línea. El nombre sale del texto visible, precedido por el texto oculto «Removed:» (`visually-hidden`), porque el tachado solo se ve y no lo anuncia ningún lector. El icono x va con `aria-hidden`. No es interactivo: no recibe foco ni tiene teclado. Contraste: texto tinta sobre tarjeta blanca (más de 12:1); el borde beige es decorativo y el dato no depende de él.
- **Cuándo usar / qué NO hace:** Solo para ingredientes retirados de la fórmula natural, con el texto exacto del envase (⬜ TODO envase: los nombres de ejemplo «Preservatives», «Refined sugar», «Hydrogenated fats» y «GMO ingredients» deben validarse con GB Foods). No es un filtro ni un botón, no se pulsa. No sirve para alérgenos: esos van en Allergen table.
