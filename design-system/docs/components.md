# GB Noodles · Microsites · Componentes (átomos)

> Catálogo de **componentes básicos / atómicos**. Cada componente tiene su **ficha** en `components/<slug>.md` (este archivo es el índice más las secciones manuales), y cada ficha es un **contrato** con dos partes:
> - **Parte viva** (anatomía, medidas, variantes, tokens que consume) → se **sincroniza
>   desde Figma** (modelo B, ver `design.md`) en el bloque `GENERATED` de la ficha. No editar a mano.
> - **Parte de criterio** (cuándo usar, qué NO hace, accesibilidad) → se escribe a mano
>   una vez debajo del bloque, porque no es expresable como variable de Figma.
>
> Reglas duras: no se inventa un componente que no esté aquí; los componentes consumen
> **tokens semánticos** de `tokens.css`, nunca primitivos ni hex.

**Estado:** 33 componentes sincronizados el 2026-10-07T13:31:29Z · una ficha por archivo en `components/<slug>.md` (este archivo solo guarda el índice y las secciones manuales).

---

## Índice

- [Icon / check](components/icon-check.md) · component · `icon-check` · ⬜ 5 pendientes
- [Icon / chevron-down](components/icon-chevron-down.md) · component · `icon-chevron-down` · ⬜ 5 pendientes
- [Icon / tiktok](components/icon-tiktok.md) · component · `icon-tiktok` · ⬜ 5 pendientes
- [Icon / instagram](components/icon-instagram.md) · component · `icon-instagram` · ⬜ 5 pendientes
- [Icon / x](components/icon-x.md) · component · `icon-x` · ⬜ 5 pendientes
- [Icon / youtube](components/icon-youtube.md) · component · `icon-youtube` · ⬜ 5 pendientes
- [Icon / arrow-right](components/icon-arrow-right.md) · component · `icon-arrow-right` · ⬜ 5 pendientes
- [Icon / arrow-left](components/icon-arrow-left.md) · component · `icon-arrow-left` · ⬜ 5 pendientes
- [Icon / close](components/icon-close.md) · component · `icon-close` · ⬜ 5 pendientes
- [Icon / menu](components/icon-menu.md) · component · `icon-menu` · ⬜ 5 pendientes
- [Icon / plus](components/icon-plus.md) · component · `icon-plus` · ⬜ 5 pendientes
- [Icon / minus](components/icon-minus.md) · component · `icon-minus` · ⬜ 5 pendientes
- [Icon / search](components/icon-search.md) · component · `icon-search` · ⬜ 5 pendientes
- [Icon / play](components/icon-play.md) · component · `icon-play` · ⬜ 5 pendientes
- [Icon / timer](components/icon-timer.md) · component · `icon-timer` · ⬜ 5 pendientes
- [Icon / external-link](components/icon-external-link.md) · component · `icon-external-link` · ⬜ 5 pendientes
- [Icon / circle-alert](components/icon-circle-alert.md) · component · `icon-circle-alert` · ⬜ 5 pendientes
- [Decoration / Noodle](components/decoration-noodle.md) · component · `decoration-noodle` · ⬜ 5 pendientes
- [Logo / GB Foods](components/logo-gb-foods.md) · component · `logo-gb-foods` · ⬜ 5 pendientes
- [Logo / Aiki](components/logo-aiki.md) · component · `logo-aiki` · ⬜ 5 pendientes
- [Logo / Yatekomo](components/logo-yatekomo.md) · component · `logo-yatekomo` · ⬜ 5 pendientes
- [Logo / Saikebon](components/logo-saikebon.md) · component · `logo-saikebon` · ⬜ 5 pendientes
- [Logo / Daisuki](components/logo-daisuki.md) · component · `logo-daisuki` · ⬜ 5 pendientes
- [Button](components/button.md) · component · `button` · ⬜ 5 pendientes
- [Icon button](components/icon-button.md) · component · `icon-button` · ⬜ 5 pendientes
- [Link](components/link.md) · component · `link` · ⬜ 5 pendientes
- [Badge](components/badge.md) · component · `badge` · ⬜ 5 pendientes
- [Chip](components/chip.md) · component · `chip` · ⬜ 5 pendientes
- [Input](components/input.md) · component · `input` · ⬜ 5 pendientes
- [Textarea](components/textarea.md) · component · `textarea` · ⬜ 5 pendientes
- [Checkbox](components/checkbox.md) · component · `checkbox` · ⬜ 5 pendientes
- [Select](components/select.md) · component · `select` · ⬜ 5 pendientes
- [Search field](components/search-field.md) · component · `search-field` · ⬜ 5 pendientes

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
