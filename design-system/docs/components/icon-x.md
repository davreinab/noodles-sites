### Icon / x   ⚙️ synced: 2026-10-07T18:43:11Z

<!-- ⚙️ GENERATED:start:icon-x -->
- **Figma:** `21:68` · página «Icons» · COMPONENT · 1 variantes · última sync 2026-10-07T18:43:11Z
- **Descripción (Figma):** Red social: X. Color: icon/color/*. Tamaño: icon/size/*
- **Anatomía:** sin instancias anidadas
- **Propiedades de componente:** ninguna
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `icon/color/default`, `icon/size/md`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `icon/color/default`
<!-- ⚙️ GENERATED:end:icon-x -->

- **Propósito:** Glifo de la red social X para el footer (enlace a su perfil). Red social: X.
- **Ejemplo de código:**
  ```html
  <span class="icon icon-x" aria-hidden="true"></span>
  ```
- **Accesibilidad (pares AA verificados):** Decorativo por defecto (`aria-hidden="true"`): el significado lo da el texto o el nombre accesible del control. Color `--icon-color-default` (tinta) sobre página 17,2:1 y sobre card 18,7:1; `--icon-color-inverse` (crema) sobre tinta 17,2:1; todos ≥ 3:1 de elemento gráfico. Dentro de un componente hereda su color (`currentColor`), así que el par válido es el del componente. Tamaños `--icon-size-sm/md/lg/xl` con `.icon--sm/--lg/--xl`.
- **Cuándo usar / qué NO hace:** Solo como enlace a los perfiles oficiales de la marca (Footer, Social 1–4). No se usa como decoración ni para compartir contenido; el enlace lleva nombre accesible con el nombre de la red.
