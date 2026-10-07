# GB Noodles · Microsites · Componentes (átomos)

> Catálogo de **componentes básicos / atómicos**. Cada componente tiene su **ficha** en `components/<slug>.md` (este archivo es el índice más las secciones manuales), y cada ficha es un **contrato** con dos partes:
> - **Parte viva** (anatomía, medidas, variantes, tokens que consume) → se **sincroniza
>   desde Figma** (modelo B, ver `design.md`) en el bloque `GENERATED` de la ficha. No editar a mano.
> - **Parte de criterio** (cuándo usar, qué NO hace, accesibilidad) → se escribe a mano
>   una vez debajo del bloque, porque no es expresable como variable de Figma.
>
> Reglas duras: no se inventa un componente que no esté aquí; los componentes consumen
> **tokens semánticos** de `tokens.css`, nunca primitivos ni hex.

**Estado:** 57 componentes sincronizados el 2026-10-07T18:17:24Z · una ficha por archivo en `components/<slug>.md` (este archivo solo guarda el índice y las secciones manuales).

---

## Índice

- [Icon / check](components/icon-check.md) · component · `icon-check` · ✅ criterio completo
- [Icon / chevron-down](components/icon-chevron-down.md) · component · `icon-chevron-down` · ✅ criterio completo
- [Icon / tiktok](components/icon-tiktok.md) · component · `icon-tiktok` · ✅ criterio completo
- [Icon / instagram](components/icon-instagram.md) · component · `icon-instagram` · ✅ criterio completo
- [Icon / x](components/icon-x.md) · component · `icon-x` · ✅ criterio completo
- [Icon / youtube](components/icon-youtube.md) · component · `icon-youtube` · ✅ criterio completo
- [Icon / arrow-right](components/icon-arrow-right.md) · component · `icon-arrow-right` · ✅ criterio completo
- [Icon / arrow-left](components/icon-arrow-left.md) · component · `icon-arrow-left` · ✅ criterio completo
- [Icon / close](components/icon-close.md) · component · `icon-close` · ✅ criterio completo
- [Icon / menu](components/icon-menu.md) · component · `icon-menu` · ✅ criterio completo
- [Icon / plus](components/icon-plus.md) · component · `icon-plus` · ✅ criterio completo
- [Icon / minus](components/icon-minus.md) · component · `icon-minus` · ✅ criterio completo
- [Icon / search](components/icon-search.md) · component · `icon-search` · ✅ criterio completo
- [Icon / play](components/icon-play.md) · component · `icon-play` · ✅ criterio completo
- [Icon / timer](components/icon-timer.md) · component · `icon-timer` · ✅ criterio completo
- [Icon / external-link](components/icon-external-link.md) · component · `icon-external-link` · ✅ criterio completo
- [Icon / circle-alert](components/icon-circle-alert.md) · component · `icon-circle-alert` · ✅ criterio completo
- [Icon / pause](components/icon-pause.md) · component · `icon-pause` · ✅ criterio completo
- [Icon / rotate-ccw](components/icon-rotate-ccw.md) · component · `icon-rotate-ccw` · ✅ criterio completo
- [Icon / info](components/icon-info.md) · component · `icon-info` · ✅ criterio completo
- [Icon / circle-check](components/icon-circle-check.md) · component · `icon-circle-check` · ✅ criterio completo
- [Icon / triangle-alert](components/icon-triangle-alert.md) · component · `icon-triangle-alert` · ✅ criterio completo
- [Icon / message-circle](components/icon-message-circle.md) · component · `icon-message-circle` · ✅ criterio completo
- [Decoration / Noodle](components/decoration-noodle.md) · component · `decoration-noodle` · ✅ criterio completo
- [Logo / GB Foods](components/logo-gb-foods.md) · component · `logo-gb-foods` · ✅ criterio completo
- [Logo / Aiki](components/logo-aiki.md) · component · `logo-aiki` · ✅ criterio completo
- [Logo / Yatekomo](components/logo-yatekomo.md) · component · `logo-yatekomo` · ✅ criterio completo
- [Logo / Saikebon](components/logo-saikebon.md) · component · `logo-saikebon` · ✅ criterio completo
- [Logo / Daisuki](components/logo-daisuki.md) · component · `logo-daisuki` · ✅ criterio completo
- [Button](components/button.md) · component · `button` · ✅ criterio completo
- [Icon button](components/icon-button.md) · component · `icon-button` · ✅ criterio completo
- [Link](components/link.md) · component · `link` · ✅ criterio completo
- [Badge](components/badge.md) · component · `badge` · ✅ criterio completo
- [Chip](components/chip.md) · component · `chip` · ✅ criterio completo
- [Input](components/input.md) · component · `input` · ⬜ 5 pendientes
- [Textarea](components/textarea.md) · component · `textarea` · ⬜ 5 pendientes
- [Checkbox](components/checkbox.md) · component · `checkbox` · ⬜ 5 pendientes
- [Select](components/select.md) · component · `select` · ⬜ 5 pendientes
- [Search field](components/search-field.md) · component · `search-field` · ⬜ 5 pendientes
- [Nav item](components/nav-item.md) · component · `nav-item` · ⬜ 5 pendientes
- [Tab](components/tab.md) · component · `tab` · ⬜ 5 pendientes
- [Lang switch](components/lang-switch.md) · component · `lang-switch` · ⬜ 5 pendientes
- [Product card](components/product-card.md) · component · `product-card` · ⬜ 5 pendientes
- [Recipe card](components/recipe-card.md) · component · `recipe-card` · ⬜ 5 pendientes
- [Contest card](components/contest-card.md) · component · `contest-card` · ⬜ 5 pendientes
- [Accordion item](components/accordion-item.md) · component · `accordion-item` · ⬜ 5 pendientes
- [Ingredient item](components/ingredient-item.md) · component · `ingredient-item` · ⬜ 5 pendientes
- [Ingredients](components/ingredients.md) · component · `ingredients` · ⬜ 5 pendientes
- [Nutrition bar](components/nutrition-bar.md) · component · `nutrition-bar` · ⬜ 5 pendientes
- [Nutrition panel](components/nutrition-panel.md) · component · `nutrition-panel` · ⬜ 5 pendientes
- [Step](components/step.md) · component · `step` · ⬜ 5 pendientes
- [Modal / Slot](components/modal-slot.md) · component · `modal-slot` · ⬜ 5 pendientes
- [Modal](components/modal.md) · component · `modal` · ⬜ 5 pendientes
- [Alert](components/alert.md) · component · `alert` · ⬜ 5 pendientes
- [Suggestion bubble](components/suggestion-bubble.md) · component · `suggestion-bubble` · ⬜ 5 pendientes
- [Timer](components/timer.md) · component · `timer` · ⬜ 5 pendientes
- [Video player](components/video-player.md) · component · `video-player` · ⬜ 5 pendientes

## Cómo rellenar una ficha

Cada ficha nace con el bloque generado y cuatro campos de criterio en `⬜ TODO` (su forma exacta:
`components/_plantilla.md`). Se escriben una vez, a mano, y el sync los conserva:

- **Propósito:** para qué sirve y qué problema resuelve.
- **Ejemplo de código:** snippet HTML mínimo con las clases reales de `components.css`, en su variante
  por defecto; una línea por variante o estado relevante si cambia el markup. Es la referencia que
  copian pantallas y agentes, y el sync lo copia al schema (`source.code.example`).
- **Accesibilidad (pares AA verificados):** los pares texto/fondo comprobados en claro y oscuro; el
  *rol* (button, textbox, checkbox, dialog… o «decorativo»); *de dónde sale su nombre* (texto visible,
  etiqueta asociada o atributo explícito: un icono sin texto siempre necesita nombre explícito); *qué se
  anuncia al cambiar de estado* (seleccionado, expandido, inválido, ocupado… un estado que solo se ve
  por color no existe para quien no ve); *teclado* (qué teclas lo operan; si no se puede usar sin
  ratón, no está terminado); *foco* (dónde entra, dónde sale, si queda atrapado a propósito) y *qué se
  oculta al lector* (partes decorativas o redundantes).
- **Cuándo usar / qué NO hace:** el límite del componente; lo que parece suyo y es de otro.

## Catálogo propuesto (⬜ por definir en Figma)
