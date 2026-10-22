### Nav item   ⚙️ synced: 2026-10-22T09:37:04Z

<!-- ⚙️ GENERATED:start:nav-item -->
- **Figma:** `53:102` · página «Navigation» · COMPONENT_SET · 8 variantes · última sync 2026-10-22T09:37:04Z
- **Descripción (Figma):** Enlace de navegación principal. Bar: navbar de escritorio (Anton 16), fondo amarillo en hover y subrayado grueso en la sección activa. Menu: menú móvil a pantalla completa (Anton 32, crema sobre tinta; activo en amarillo con subrayado). La sección activa nunca se marca solo por color (subrayado) y lleva aria-current="page". El texto se edita en la instancia.
- **Anatomía:** sin instancias anidadas
- **API:** `type`: Bar, Menu (por defecto Bar)
- **Estados de CSS:** Hover, Active, Focus
- **Nombres en Figma:** `type` ← `Type`
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `border/width/thick`, `font/family/display`, `font/line-height/desktop/label`, `font/size/desktop/label`, `font/style/display`, `nav-item/indicator`, `nav-item/text`, `radius/sm`, `space/16`, `space/4`, `space/8`
- **Text styles:** `Desktop/label`
<!-- ⚙️ GENERATED:end:nav-item -->

- **Propósito:** Enlace de la navegación principal. Bar: en la Navbar de escritorio, con indicador inferior en la página activa. Menu: en el Mobile menu, en grande y en crema sobre tinta.
- **Ejemplo de código:**
  ```html
  <nav data-ds="nav-item" aria-label="Principal">
  <a class="nav-item" href="/productos" aria-current="page">Productos</a>
  <a class="nav-item" href="/recetas">Recetas</a>
  </nav>
  <a data-ds="nav-item" class="nav-item nav-item--menu" href="/recetas">Recetas</a>
  ```
- **Accesibilidad (rol, nombre, estados y teclado):** Bar: tinta sobre crema 17,2:1; hover tinta sobre amarillo 12,3:1; el activo se marca con `aria-current="page"` y un indicador de 4 px (no solo color). Menu: crema sobre tinta 17,2:1; activo y hover en amarillo 12,3:1, foco amarillo. Rol: enlaces `<a>` dentro de `<nav aria-label>`; Tab entre ellos. Foco: contorno de 2 px pegado, radius/sm.
- **Cuándo usar / qué NO hace:** Solo para la navegación principal de la web (cinco secciones). No se usa como pestaña de contenido (Tab) ni como enlace dentro de texto (Link).
