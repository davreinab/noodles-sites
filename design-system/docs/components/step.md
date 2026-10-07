### Step   ⚙️ synced: 2026-10-07T18:30:51Z

<!-- ⚙️ GENERATED:start:step -->
- **Figma:** `71:164` · página «Step» · COMPONENT_SET · 2 variantes · última sync 2026-10-07T18:30:51Z
- **Descripción (Figma):** Paso numerado de preparación (página de producto, junto al temporizador de 3 minutos de la fase 5) o de receta. Anatomía: número en círculo (Anton, step/number-bg amarillo de marca, 56 px) · texto (body-l) · media opcional (Media=True: imagen o GIF 16:9; el GIF respeta prefers-reduced-motion y lleva pausa). Se usa dentro de &lt;ol&gt;: el número visual es decorativo (aria-hidden) porque la lista ya lo anuncia. Se apilan con space/32.
- **Anatomía:** sin instancias anidadas
- **Media:** False, True
- **Propiedades de componente:** `Number#71:9` (TEXT, por defecto 1), `Text#71:12` (TEXT, por defecto Abre la tapa hasta la mitad y añade agua hirviendo hasta la línea interior.), `Media` (VARIANT, por defecto False)
- **Iconos / instancias anidadas:** ninguno
- **Tokens que consume:** `border/width/thin`, `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/h3`, `font/size/desktop/body-l`, `font/size/desktop/h3`, `font/style/body`, `font/style/display`, `radius/pill`, `space/16`, `space/24`, `space/56`, `space/8`, `step/border`, `step/number-bg`, `step/number-text`, `step/text`
- **Text styles:** `Desktop/h3`, `Desktop/body-l`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `font/family/body`, `font/family/display`, `font/line-height/desktop/body-l`, `font/line-height/desktop/h3`, `font/size/desktop/body-l`, `font/size/desktop/h3`, `font/style/body`, `font/style/display`, `step/border`, `step/number-bg`, `step/number-text`, `step/text`
<!-- ⚙️ GENERATED:end:step -->

- **Propósito:** Paso numerado de la preparación de producto o de una receta, con imagen o GIF opcional.
- **Ejemplo de código:**
  ```html
  <ol class="steps">
  <li class="step">
  <span class="step__number" aria-hidden="true">1</span>
  <div class="step__content"><p class="step__text">Abre la tapa hasta la mitad.</p></div>
  </li>
  <li class="step step--media">
  <span class="step__number" aria-hidden="true">2</span>
  <div class="step__content">
  <p class="step__text">Añade agua hirviendo hasta la línea interior.</p>
  <div class="step__media"><img src="/media/paso-2.jpg" alt="Agua hasta la línea interior del vaso"></div>
  </div>
  </li>
  </ol>
  ```
- **Accesibilidad (pares AA verificados):** Número tinta sobre amarillo 12,3:1; texto tinta sobre crema 17,2:1. Rol: `<li>` dentro de `<ol>`, que ya anuncia la posición; por eso el número visual es `aria-hidden`. La imagen describe el gesto en su `alt`; un GIF va como MP4 silencioso en bucle con botón de pausa y se detiene con prefers-reduced-motion.
- **Cuándo usar / qué NO hace:** En Preparation (producto) y en la receta. El texto sale del envase o de la receta; no se mezcla con el Timer (va al lado).
