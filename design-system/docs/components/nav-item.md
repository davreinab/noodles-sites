### Nav item   ⚙️ synced: 2026-10-07T18:44:44Z

<!-- ⚙️ GENERATED:start:nav-item -->
- **Figma:** `53:102` · página «Nav item» · COMPONENT_SET · 8 variantes · última sync 2026-10-07T18:44:44Z
- **Descripción (Figma):** Enlace de navegación principal. Bar: navbar de escritorio (Anton 16), fondo amarillo en hover y subrayado grueso en la sección activa. Menu: menú móvil a pantalla completa (Anton 32, crema sobre tinta; activo en amarillo con subrayado). La sección activa nunca se marca solo por color (subrayado) y lleva aria-current=&quot;page&quot;. El texto se edita en la instancia.
- **Anatomía:** sin instancias anidadas
- **Type:** Bar, Menu
- **State:** Default, Hover, Active, Focus
- **Propiedades de componente:** `Type` (VARIANT, por defecto Bar), `State` (VARIANT, por defecto Default)
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `border/width/thick`, `font/family/display`, `font/line-height/desktop/label`, `font/size/desktop/label`, `font/style/display`, `nav-item/indicator`, `nav-item/text`, `radius/sm`, `space/16`, `space/4`, `space/8`
- **Text styles:** `Desktop/label`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `font/family/display`, `font/line-height/desktop/label`, `font/size/desktop/label`, `font/style/display`, `nav-item/indicator`, `nav-item/text`
<!-- ⚙️ GENERATED:end:nav-item -->

- **Propósito:** Enlace de la navegación principal. Bar: en la Navbar de escritorio, con indicador inferior en la página activa. Menu: en el Mobile menu, en grande y en crema sobre tinta.
- **Ejemplo de código:**
  ```html
  <nav aria-label="Principal">
  <a class="nav-item" href="/productos" aria-current="page">Productos</a>
  <a class="nav-item" href="/recetas">Recetas</a>
  </nav>
  <a class="nav-item nav-item--menu" href="/recetas">Recetas</a>
  ```
- **Accesibilidad (pares AA verificados):** Bar: tinta sobre crema 17,2:1; hover tinta sobre amarillo 12,3:1; el activo se marca con `aria-current="page"` y un indicador de 4 px (no solo color). Menu: crema sobre tinta 17,2:1; activo y hover en amarillo 12,3:1, foco amarillo. Rol: enlaces `<a>` dentro de `<nav aria-label>`; Tab entre ellos. Foco: contorno de 2 px pegado, radius/sm.
- **Cuándo usar / qué NO hace:** Solo para la navegación principal de la web (cinco secciones). No se usa como pestaña de contenido (Tab) ni como enlace dentro de texto (Link).
