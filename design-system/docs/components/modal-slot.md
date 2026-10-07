### Modal / Slot   ⚙️ synced: 2026-10-07T18:27:15Z

<!-- ⚙️ GENERATED:start:modal-slot -->
- **Figma:** `79:52` · página «Modal» · COMPONENT · 1 variantes · última sync 2026-10-07T18:27:15Z
- **Descripción (Figma):** Hueco de contenido del Modal. Se sustituye con la propiedad «Content» por la instancia real (imagen de la etiqueta, texto de alérgenos, resultado de concurso, lista de resultados). No se usa fuera del Modal.
- **Anatomía:** sin instancias anidadas
- **Propiedades de componente:** ninguna
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `font/family/body`, `font/line-height/desktop/caption`, `font/size/desktop/caption`, `font/style/body`, `modal/slot-bg`, `modal/text`, `radius/sm`, `space/24`
- **Text styles:** `Desktop/caption`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `font/family/body`, `font/line-height/desktop/caption`, `font/size/desktop/caption`, `font/style/body`, `modal/slot-bg`, `modal/text`
<!-- ⚙️ GENERATED:end:modal-slot -->

- **Propósito:** Hueco de contenido del Modal en Figma: se sustituye por la instancia real (imagen de la etiqueta, texto de alérgenos, resultado de concurso, lista de resultados).
- **Ejemplo de código:**
  ```html
  <div class="modal-slot">Contenido del modal</div>
  ```
- **Accesibilidad (pares AA verificados):** Texto de marcador en tinta sobre crema 17,2:1. En producción no aparece: el hueco lo ocupa el contenido real, que trae su propia accesibilidad.
- **Cuándo usar / qué NO hace:** Solo dentro de Modal y solo como marcador de diseño. No es un componente de contenido.
