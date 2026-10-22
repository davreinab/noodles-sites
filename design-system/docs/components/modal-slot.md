### Modal / Slot   ⚙️ synced: 2026-10-22T09:37:04Z

<!-- ⚙️ GENERATED:start:modal-slot -->
- **Figma:** `79:52` · página «Feedback & overlays» · COMPONENT · 1 variantes · última sync 2026-10-22T09:37:04Z
- **Descripción (Figma):** Hueco de contenido del Modal. Se sustituye con la propiedad «Content» por la instancia real (imagen de la etiqueta, texto de alérgenos, resultado de concurso, lista de resultados). No se usa fuera del Modal.
- **Anatomía:** sin instancias anidadas
- **API:** sin propiedades
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `font/family/body`, `font/line-height/desktop/caption`, `font/size/desktop/caption`, `font/style/body`, `modal/slot-bg`, `modal/text`, `radius/sm`, `space/24`
- **Text styles:** `Desktop/caption`
<!-- ⚙️ GENERATED:end:modal-slot -->

- **Propósito:** Hueco de contenido del Modal en Figma: se sustituye por la instancia real (imagen de la etiqueta, texto de alérgenos, resultado de concurso, lista de resultados).
- **Ejemplo de código:**
  ```html
  <div data-ds="modal-slot" class="modal-slot">Contenido del modal</div>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Texto de marcador en tinta sobre crema 17,2:1. En producción no aparece: el hueco lo ocupa el contenido real, que trae su propia accesibilidad.
- **Cuándo usar / qué NO hace:** Solo dentro de Modal y solo como marcador de diseño. No es un componente de contenido.
