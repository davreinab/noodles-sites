### Timer   ⚙️ synced: 2026-10-07T18:17:24Z

<!-- ⚙️ GENERATED:start:timer -->
- **Figma:** `82:143` · página «Timer» · COMPONENT_SET · 4 variantes · última sync 2026-10-07T18:17:24Z
- **Descripción (Figma):** Temporizador de preparación (3 minutos) junto a los Step de la página de producto. State=Idle (3:00, «Empezar») · Running (anillo vaciándose, «Pausar» + reiniciar) · Paused («Seguir» + reiniciar) · Done (anillo verde natural, circle-check, «¡Listo!», «Otra vez»). El anillo es decorativo (aria-hidden) y no comunica nada por sí solo: el tiempo está en texto. Accesibilidad: el tiempo se expone con role=&quot;timer&quot; sin anunciar cada segundo; una región aria-live=&quot;polite&quot; anuncia solo «Quedan 1 minuto» y «¡Listo! Ya puedes comer»; el botón principal cambia su nombre (Empezar/Pausar/Seguir). Puede sonar o vibrar al terminar solo si el usuario lo activa. Respeta prefers-reduced-motion (el anillo salta en vez de animarse).
- **Anatomía:** `action` → Hierarchy=Primary, Size=M, State=Default, `icon-leading` → Icon / play, `icon-trailing` → Icon / arrow-right
- **State:** Idle, Running, Paused, Done
- **Propiedades de componente:** `State` (VARIANT, por defecto Idle)
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `border/width/thick`, `border/width/thin`, `button/primary/bg`, `button/primary/border`, `button/primary/text`, `font/family/body`, `font/family/display`, `font/line-height/desktop/caption`, `font/line-height/desktop/h2`, `font/line-height/desktop/label`, `font/size/desktop/caption`, `font/size/desktop/h2`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/sm`, `radius/md`, `radius/pill`, `space/16`, `space/24`, `space/32`, `space/4`, `space/8`, `timer/bg`, `timer/border`, `timer/label`, `timer/progress`, `timer/time`, `timer/track`
- **Text styles:** `Desktop/h2`, `Desktop/caption`, `Desktop/label`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `button/primary/bg`, `button/primary/border`, `button/primary/text`, `font/family/body`, `font/family/display`, `font/line-height/desktop/caption`, `font/line-height/desktop/h2`, `font/line-height/desktop/label`, `font/size/desktop/caption`, `font/size/desktop/h2`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `timer/bg`, `timer/border`, `timer/label`, `timer/progress`, `timer/time`, `timer/track`
<!-- ⚙️ GENERATED:end:timer -->

- **Propósito:** ⬜ TODO
- **Ejemplo de código:** ⬜ TODO _(snippet HTML mínimo con las clases reales de `components.css`; se copia a `source.code.example` del schema)_
  ```html
  <!-- ⬜ TODO -->
  ```
- **Accesibilidad (pares AA verificados):** ⬜ TODO
- **Cuándo usar / qué NO hace:** ⬜ TODO
