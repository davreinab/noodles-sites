### Icon / external-link   ⚙️ synced: 2026-10-07T18:27:15Z

<!-- ⚙️ GENERATED:start:icon-external-link -->
- **Figma:** `30:89` · página «Icons» · COMPONENT · 1 variantes · última sync 2026-10-07T18:27:15Z
- **Descripción (Figma):** Enlace externo: contacto, concursos externos, formulario de Calidad. Fuente: Lucide (ISC). Trazo 2.5 px (geometría fija del glifo). Color: icon/color/*. Tamaño: icon/size/*
- **Anatomía:** sin instancias anidadas
- **Propiedades de componente:** ninguna
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `icon/color/default`, `icon/size/md`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `icon/color/default`
<!-- ⚙️ GENERATED:end:icon-external-link -->

- **Propósito:** Glifo de interfaz: enlace externo: contacto, concursos externos, formulario de Calidad.
- **Ejemplo de código:**
  ```html
  <span class="icon icon-external-link" aria-hidden="true"></span>
  ```
- **Accesibilidad (pares AA verificados):** Decorativo por defecto (`aria-hidden="true"`): el significado lo da el texto o el nombre accesible del control. Color `--icon-color-default` (tinta) sobre página 17,2:1 y sobre card 18,7:1; `--icon-color-inverse` (crema) sobre tinta 17,2:1; todos ≥ 3:1 de elemento gráfico. Dentro de un componente hereda su color (`currentColor`), así que el par válido es el del componente. Tamaños `--icon-size-sm/md/lg/xl` con `.icon--sm/--lg/--xl`.
- **Cuándo usar / qué NO hace:** Dentro de otro componente (Button, Icon button, Link, Chip, Alert…) o junto a un texto que dice lo mismo. Un icono solo no transmite información: si no hay texto visible, el control que lo contiene lleva `aria-label`. No se recolorea con valores sueltos ni se cambia el trazo (2,5 fijo).
