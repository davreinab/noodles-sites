### Timer   ⚙️ synced: 2026-10-07T18:49:29Z

<!-- ⚙️ GENERATED:start:timer -->
- **Figma:** `82:143` · página «Timer» · COMPONENT_SET · 4 variantes · última sync 2026-10-07T18:49:29Z
- **Descripción (Figma):** Temporizador de preparación (3 minutos) junto a los Step de la página de producto. State=Idle (3:00, «Empezar») · Running (anillo vaciándose, «Pausar» + reiniciar) · Paused («Seguir» + reiniciar) · Done (anillo verde natural, circle-check, «¡Listo!», «Otra vez»). El anillo es decorativo (aria-hidden) y no comunica nada por sí solo: el tiempo está en texto. Accesibilidad: el tiempo se expone con role=&quot;timer&quot; sin anunciar cada segundo; una región aria-live=&quot;polite&quot; anuncia solo «Quedan 1 minuto» y «¡Listo! Ya puedes comer»; el botón principal cambia su nombre (Empezar/Pausar/Seguir). Puede sonar o vibrar al terminar solo si el usuario lo activa. Respeta prefers-reduced-motion (el anillo salta en vez de animarse).
- **Anatomía:** `action` → Hierarchy=Primary, Size=M, State=Default, `icon-leading` → Icon / play, `icon-trailing` → Icon / arrow-right
- **State:** Idle, Running, Paused, Done
- **Propiedades de componente:** `State` (VARIANT, por defecto Idle)
- **Iconos / instancias anidadas:** sí · swap: ninguna (⚠️ no expuesto) · por defecto: unknown
- **Tokens que consume:** `border/width/thick`, `border/width/thin`, `button/primary/bg`, `button/primary/border`, `button/primary/text`, `font/family/body`, `font/family/display`, `font/line-height/desktop/caption`, `font/line-height/desktop/h2`, `font/line-height/desktop/label`, `font/size/desktop/caption`, `font/size/desktop/h2`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `icon/size/sm`, `radius/md`, `radius/pill`, `space/16`, `space/24`, `space/32`, `space/4`, `space/8`, `timer/bg`, `timer/border`, `timer/label`, `timer/progress`, `timer/time`, `timer/track`
- **Text styles:** `Desktop/h2`, `Desktop/caption`, `Desktop/label`
- **Marcas:** cambia con la marca (yatekomo, saikebon, aiki, daisuki, de; por defecto `yatekomo`) vía `[data-brand]` · tokens de marca: `button/primary/bg`, `button/primary/border`, `button/primary/text`, `font/family/body`, `font/family/display`, `font/line-height/desktop/caption`, `font/line-height/desktop/h2`, `font/line-height/desktop/label`, `font/size/desktop/caption`, `font/size/desktop/h2`, `font/size/desktop/label`, `font/style/body`, `font/style/display`, `timer/bg`, `timer/border`, `timer/label`, `timer/progress`, `timer/time`, `timer/track`
<!-- ⚙️ GENERATED:end:timer -->

- **Propósito:** Temporizador de 3 minutos de la preparación: anillo de progreso, tiempo restante y controles Empezar, Pausar, Seguir y Reiniciar.
- **Ejemplo de código:**
  ```html
  <section class="timer" data-state="running" aria-labelledby="timer-title">
  <h3 class="visually-hidden" id="timer-title">Temporizador de preparación</h3>
  <div class="timer__dial">
  <svg class="timer__ring" viewBox="0 0 100 100" aria-hidden="true"><circle class="timer__track" cx="50" cy="50" r="46" stroke-width="8" pathLength="100"/><circle class="timer__progress" cx="50" cy="50" r="46" stroke-width="8" pathLength="100" stroke-dashoffset="40"/></svg>
  <div class="timer__readout"><span class="timer__time" role="timer">1:48</span><span class="timer__label">Quedan</span></div>
  </div>
  <p class="visually-hidden" aria-live="polite"></p>
  <div class="timer__controls">
  <button class="button button--secondary" type="button"><span class="icon icon-pause" aria-hidden="true"></span>Pausar</button>
  <button class="icon-button icon-button--secondary" type="button" aria-label="Reiniciar"><span class="icon icon-rotate-ccw" aria-hidden="true"></span></button>
  </div>
  </section>
  ```
- **Accesibilidad (pares AA verificados):** Tiempo tinta sobre blanco 18,7:1; etiqueta gris cálido sobre blanco 5,9:1; progreso de tinta sobre pista arena 13,7:1; terminado en verde sobre blanco 5,5:1. El anillo es decorativo (`aria-hidden`). El tiempo va en `role="timer"` (no anuncia cada segundo) y una región `aria-live="polite"` dice solo «Queda 1 minuto» y «¡Listo!». El botón principal cambia de nombre (Empezar/Pausar/Seguir). Sonido o vibración al terminar solo si el usuario lo activa; con reduce-motion el anillo salta sin animarse.
- **Cuándo usar / qué NO hace:** Solo en la preparación del producto (3 minutos). No es una cuenta atrás de concursos ni de promociones.
