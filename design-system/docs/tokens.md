<!-- ⚙️ ARCHIVO GENERADO por scripts/ds-sync.py — NO EDITAR A MANO. -->

# GB Noodles · Microsites · Tokens  ·  _(espejo generado de Figma)_

> Última sync: **2026-10-07T18:19:35Z** · modo de adopción: `new` · 325 variables en 8 colecciones · 18 text styles · 4 effect styles.
> Cada token se consume en código como `var(--nombre)`. Los alias conservan su referencia y su valor resuelto.

## Índice

- [Primitive](#primitive) · 22 tokens · modos: Value
- [Semantic](#semantic) · 38 tokens · modos: Yatekomo, Saikebon, Aiki, Daisuki, DE
- [Components](#components) · 185 tokens · modos: Value
- [Layer](#layer) · 7 tokens · modos: Value
- [Spacing](#spacing) · 20 tokens · modos: Value
- [Layout](#layout) · 7 tokens · modos: Desktop, Tablet, Mobile
- [Typography](#typography) · 41 tokens · modos: Yatekomo, Saikebon, Aiki, Daisuki, DE
- [Motion](#motion) · 5 tokens · modos: Value
- [Marcas](#marcas)
- [Foundations](#foundations)
- [Text styles](#text-styles)

## Marcas

Modos de marca de las colecciones `Semantic`, `Typography`. La marca por defecto vive en `:root`; cada otra marca se activa con `[data-brand="<slug>"]` **en `<html>`** y solo redefine lo que cambia. Tiene que ir en `<html>`: las variables de componente se declaran en `:root` apuntando a las semánticas, y una variable CSS resuelve su `var()` donde se declara; en un contenedor interior los componentes no heredarían la marca.

| Marca | Slug | Selector CSS | Por defecto |
|---|---|---|---|
| Yatekomo | `yatekomo` | `[data-brand="yatekomo"]` | sí |
| Saikebon | `saikebon` | `[data-brand="saikebon"]` | — |
| Aiki | `aiki` | `[data-brand="aiki"]` | — |
| Daisuki | `daisuki` | `[data-brand="daisuki"]` | — |
| DE | `de` | `[data-brand="de"]` | — |

## Primitive

| Token | CSS | Tipo | Value | Scopes | Descripción |
|---|---|---|---|---|---|
| `color/yatekomo/yellow` | `--color-yatekomo-yellow` | COLOR | `#ffcb05` | — | Amarillo de marca Yatekomo. Primitivo: no se consume en componentes. |
| `color/yatekomo/yellow-soft` | `--color-yatekomo-yellow-soft` | COLOR | `#fff5d9` | — | Crema de fondo Yatekomo. Primitivo: no se consume en componentes. |
| `color/yatekomo/orange` | `--color-yatekomo-orange` | COLOR | `#e8890c` | — | Naranja de acento Yatekomo. Primitivo: no se consume en componentes. |
| `color/yatekomo/green` | `--color-yatekomo-green` | COLOR | `#007a33` | — | Verde Pantone 356 C del claim natural. Primitivo: no se consume en componentes. |
| `color/neutral/ink-900` | `--color-neutral-ink-900` | COLOR | `#121212` | — | Tinta: texto y fondos oscuros. Primitivo: no se consume en componentes. |
| `color/neutral/ink-600` | `--color-neutral-ink-600` | COLOR | `#6b6455` | — | Gris cálido de texto secundario. Primitivo: no se consume en componentes. |
| `color/neutral/sand-200` | `--color-neutral-sand-200` | COLOR | `#e4dcc8` | — | Filete decorativo sobre crema. Primitivo: no se consume en componentes. |
| `color/neutral/white` | `--color-neutral-white` | COLOR | `#ffffff` | — | Blanco. Primitivo: no se consume en componentes. |
| `color/red/600` | `--color-red-600` | COLOR | `#e1251b` | — | Rojo del packaging (pill NUEVO). Primitivo: no se consume en componentes. |
| `color/status/error-50` | `--color-status-error-50` | COLOR | `#fde8e7` | — | Fondo de error. Primitivo: no se consume en componentes. |
| `color/status/error-700` | `--color-status-error-700` | COLOR | `#c81e15` | — | Icono y borde de error. Primitivo: no se consume en componentes. |
| `color/status/error-900` | `--color-status-error-900` | COLOR | `#a3160e` | — | Texto de error. Primitivo: no se consume en componentes. |
| `color/status/success-50` | `--color-status-success-50` | COLOR | `#e3f3e9` | — | Fondo de éxito. Primitivo: no se consume en componentes. |
| `color/status/success-900` | `--color-status-success-900` | COLOR | `#005c26` | — | Texto de éxito. Primitivo: no se consume en componentes. |
| `color/status/alert-50` | `--color-status-alert-50` | COLOR | `#ffefc2` | — | Fondo de aviso. Primitivo: no se consume en componentes. |
| `color/status/alert-700` | `--color-status-alert-700` | COLOR | `#9a5b00` | — | Icono y borde de aviso. Primitivo: no se consume en componentes. |
| `color/status/alert-900` | `--color-status-alert-900` | COLOR | `#6b4100` | — | Texto de aviso. Primitivo: no se consume en componentes. |
| `color/status/info-50` | `--color-status-info-50` | COLOR | `#e5eef9` | — | Fondo de información. Primitivo: no se consume en componentes. |
| `color/status/info-700` | `--color-status-info-700` | COLOR | `#1f63b5` | — | Icono y borde de información. Primitivo: no se consume en componentes. |
| `color/status/info-900` | `--color-status-info-900` | COLOR | `#0b4482` | — | Texto de información. Primitivo: no se consume en componentes. |
| `shadow/ink-20` | `--shadow-ink-20` | COLOR | `rgba(18, 18, 18, 0.2)` | — | Tinta al 20%. Translúcido permitido solo en sombras de elevación |
| `overlay/ink-70` | `--overlay-ink-70` | COLOR | `rgba(18, 18, 18, 0.7)` | — | Tinta al 70 %. Translúcido permitido solo en velos (overlay) de modales y paneles. Primitivo: no se consume en componentes. |

## Semantic

| Token | CSS | Tipo | Yatekomo | Saikebon | Aiki | Daisuki | DE | Scopes | Descripción |
|---|---|---|---|---|---|---|---|---|---|
| `color/surface/page` | `--color-surface-page` | COLOR | → `--color-yatekomo-yellow-soft` | → `--color-yatekomo-yellow-soft` | → `--color-yatekomo-yellow-soft` | → `--color-yatekomo-yellow-soft` | → `--color-yatekomo-yellow-soft` | FRAME_FILL, SHAPE_FILL | Fondo base de página |
| `color/surface/brand` | `--color-surface-brand` | COLOR | → `--color-yatekomo-yellow` | → `--color-yatekomo-yellow` | → `--color-yatekomo-yellow` | → `--color-yatekomo-yellow` | → `--color-yatekomo-yellow` | FRAME_FILL, SHAPE_FILL | Fondo de marca (amarillo común a todas las marcas) |
| `color/surface/card` | `--color-surface-card` | COLOR | → `--color-neutral-white` | → `--color-neutral-white` | → `--color-neutral-white` | → `--color-neutral-white` | → `--color-neutral-white` | FRAME_FILL, SHAPE_FILL | Fondo de card clara |
| `color/surface/inverse` | `--color-surface-inverse` | COLOR | → `--color-neutral-ink-900` | → `--color-neutral-ink-900` | → `--color-neutral-ink-900` | → `--color-neutral-ink-900` | → `--color-neutral-ink-900` | FRAME_FILL, SHAPE_FILL | Secciones y fondos oscuros |
| `color/surface/natural` | `--color-surface-natural` | COLOR | → `--color-yatekomo-green` | → `--color-yatekomo-green` | → `--color-yatekomo-green` | → `--color-yatekomo-green` | → `--color-yatekomo-green` | FRAME_FILL, SHAPE_FILL | Fondo del claim natural; texto encima: color/text/on-natural |
| `color/surface/accent` | `--color-surface-accent` | COLOR | → `--color-yatekomo-orange` | → `--color-yatekomo-orange` | → `--color-yatekomo-orange` | → `--color-yatekomo-orange` | → `--color-yatekomo-orange` | FRAME_FILL, SHAPE_FILL | Acento decorativo. Texto encima solo color/text/default |
| `color/surface/badge-new` | `--color-surface-badge-new` | COLOR | → `--color-red-600` | → `--color-red-600` | → `--color-red-600` | → `--color-red-600` | → `--color-red-600` | FRAME_FILL, SHAPE_FILL | Pill NUEVO; texto encima: color/text/on-badge |
| `color/text/default` | `--color-text-default` | COLOR | → `--color-neutral-ink-900` | → `--color-neutral-ink-900` | → `--color-neutral-ink-900` | → `--color-neutral-ink-900` | → `--color-neutral-ink-900` | TEXT_FILL | Texto principal (≥12:1 sobre page, brand y card) |
| `color/text/secondary` | `--color-text-secondary` | COLOR | → `--color-neutral-ink-600` | → `--color-neutral-ink-600` | → `--color-neutral-ink-600` | → `--color-neutral-ink-600` | → `--color-neutral-ink-600` | TEXT_FILL | Texto secundario. Solo sobre page o card (5.4:1); NO sobre brand (3.85:1) |
| `color/text/on-inverse` | `--color-text-on-inverse` | COLOR | → `--color-yatekomo-yellow-soft` | → `--color-yatekomo-yellow-soft` | → `--color-yatekomo-yellow-soft` | → `--color-yatekomo-yellow-soft` | → `--color-yatekomo-yellow-soft` | TEXT_FILL | Texto sobre surface/inverse (17:1) |
| `color/text/brand-on-inverse` | `--color-text-brand-on-inverse` | COLOR | → `--color-yatekomo-yellow` | → `--color-yatekomo-yellow` | → `--color-yatekomo-yellow` | → `--color-yatekomo-yellow` | → `--color-yatekomo-yellow` | TEXT_FILL | Texto destacado amarillo sobre surface/inverse (12:1) |
| `color/text/on-natural` | `--color-text-on-natural` | COLOR | → `--color-neutral-white` | → `--color-neutral-white` | → `--color-neutral-white` | → `--color-neutral-white` | → `--color-neutral-white` | TEXT_FILL | Texto sobre surface/natural (5.5:1) |
| `color/text/natural` | `--color-text-natural` | COLOR | → `--color-yatekomo-green` | → `--color-yatekomo-green` | → `--color-yatekomo-green` | → `--color-yatekomo-green` | → `--color-yatekomo-green` | TEXT_FILL | Texto verde natural sobre page (5.0:1). Sobre brand solo texto grande (3.6:1) |
| `color/text/on-badge` | `--color-text-on-badge` | COLOR | → `--color-neutral-white` | → `--color-neutral-white` | → `--color-neutral-white` | → `--color-neutral-white` | → `--color-neutral-white` | TEXT_FILL | Texto sobre surface/badge-new (4.7:1) |
| `color/border/default` | `--color-border-default` | COLOR | → `--color-neutral-ink-900` | → `--color-neutral-ink-900` | → `--color-neutral-ink-900` | → `--color-neutral-ink-900` | → `--color-neutral-ink-900` | STROKE_COLOR | Borde de componentes (botón ghost, formularios) |
| `color/border/subtle` | `--color-border-subtle` | COLOR | → `--color-neutral-sand-200` | → `--color-neutral-sand-200` | → `--color-neutral-sand-200` | → `--color-neutral-sand-200` | → `--color-neutral-sand-200` | STROKE_COLOR | Filete decorativo de tablas. NO para límites de controles (1.3:1) |
| `color/effect/shadow-brand` | `--color-effect-shadow-brand` | COLOR | → `--color-yatekomo-yellow` | → `--color-yatekomo-yellow` | → `--color-yatekomo-yellow` | → `--color-yatekomo-yellow` | → `--color-yatekomo-yellow` | EFFECT_COLOR | Color de sombra dura de marca |
| `color/effect/shadow-ink` | `--color-effect-shadow-ink` | COLOR | → `--color-neutral-ink-900` | → `--color-neutral-ink-900` | → `--color-neutral-ink-900` | → `--color-neutral-ink-900` | → `--color-neutral-ink-900` | EFFECT_COLOR | Color de sombra dura neutra |
| `color/status/error/bg` | `--color-status-error-bg` | COLOR | → `--color-status-error-50` | → `--color-status-error-50` | → `--color-status-error-50` | → `--color-status-error-50` | → `--color-status-error-50` | FRAME_FILL, SHAPE_FILL | Fondo de mensaje de error |
| `color/status/error/text` | `--color-status-error-text` | COLOR | → `--color-status-error-900` | → `--color-status-error-900` | → `--color-status-error-900` | → `--color-status-error-900` | → `--color-status-error-900` | TEXT_FILL | Texto de error sobre su bg (≥6.6:1) |
| `color/status/error/icon` | `--color-status-error-icon` | COLOR | → `--color-status-error-700` | → `--color-status-error-700` | → `--color-status-error-700` | → `--color-status-error-700` | → `--color-status-error-700` | FRAME_FILL, SHAPE_FILL | Icono de error (≥4.7:1 sobre bg y page) |
| `color/status/error/border` | `--color-status-error-border` | COLOR | → `--color-status-error-700` | → `--color-status-error-700` | → `--color-status-error-700` | → `--color-status-error-700` | → `--color-status-error-700` | STROKE_COLOR | Borde de error (≥4.7:1) |
| `color/status/success/bg` | `--color-status-success-bg` | COLOR | → `--color-status-success-50` | → `--color-status-success-50` | → `--color-status-success-50` | → `--color-status-success-50` | → `--color-status-success-50` | FRAME_FILL, SHAPE_FILL | Fondo de mensaje de success |
| `color/status/success/text` | `--color-status-success-text` | COLOR | → `--color-status-success-900` | → `--color-status-success-900` | → `--color-status-success-900` | → `--color-status-success-900` | → `--color-status-success-900` | TEXT_FILL | Texto de success sobre su bg (≥6.6:1) |
| `color/status/success/icon` | `--color-status-success-icon` | COLOR | → `--color-yatekomo-green` | → `--color-yatekomo-green` | → `--color-yatekomo-green` | → `--color-yatekomo-green` | → `--color-yatekomo-green` | FRAME_FILL, SHAPE_FILL | Icono de success (≥4.7:1 sobre bg y page) |
| `color/status/success/border` | `--color-status-success-border` | COLOR | → `--color-yatekomo-green` | → `--color-yatekomo-green` | → `--color-yatekomo-green` | → `--color-yatekomo-green` | → `--color-yatekomo-green` | STROKE_COLOR | Borde de success (≥4.7:1) |
| `color/status/alert/bg` | `--color-status-alert-bg` | COLOR | → `--color-status-alert-50` | → `--color-status-alert-50` | → `--color-status-alert-50` | → `--color-status-alert-50` | → `--color-status-alert-50` | FRAME_FILL, SHAPE_FILL | Fondo de mensaje de alert |
| `color/status/alert/text` | `--color-status-alert-text` | COLOR | → `--color-status-alert-900` | → `--color-status-alert-900` | → `--color-status-alert-900` | → `--color-status-alert-900` | → `--color-status-alert-900` | TEXT_FILL | Texto de alert sobre su bg (≥6.6:1) |
| `color/status/alert/icon` | `--color-status-alert-icon` | COLOR | → `--color-status-alert-700` | → `--color-status-alert-700` | → `--color-status-alert-700` | → `--color-status-alert-700` | → `--color-status-alert-700` | FRAME_FILL, SHAPE_FILL | Icono de alert (≥4.7:1 sobre bg y page) |
| `color/status/alert/border` | `--color-status-alert-border` | COLOR | → `--color-status-alert-700` | → `--color-status-alert-700` | → `--color-status-alert-700` | → `--color-status-alert-700` | → `--color-status-alert-700` | STROKE_COLOR | Borde de alert (≥4.7:1) |
| `color/status/info/bg` | `--color-status-info-bg` | COLOR | → `--color-status-info-50` | → `--color-status-info-50` | → `--color-status-info-50` | → `--color-status-info-50` | → `--color-status-info-50` | FRAME_FILL, SHAPE_FILL | Fondo de mensaje de info |
| `color/status/info/text` | `--color-status-info-text` | COLOR | → `--color-status-info-900` | → `--color-status-info-900` | → `--color-status-info-900` | → `--color-status-info-900` | → `--color-status-info-900` | TEXT_FILL | Texto de info sobre su bg (≥6.6:1) |
| `color/status/info/icon` | `--color-status-info-icon` | COLOR | → `--color-status-info-700` | → `--color-status-info-700` | → `--color-status-info-700` | → `--color-status-info-700` | → `--color-status-info-700` | FRAME_FILL, SHAPE_FILL | Icono de info (≥4.7:1 sobre bg y page) |
| `color/status/info/border` | `--color-status-info-border` | COLOR | → `--color-status-info-700` | → `--color-status-info-700` | → `--color-status-info-700` | → `--color-status-info-700` | → `--color-status-info-700` | STROKE_COLOR | Borde de info (≥4.7:1) |
| `shadow/soft` | `--shadow-soft` | COLOR | → `--shadow-ink-20` | → `--shadow-ink-20` | → `--shadow-ink-20` | → `--shadow-ink-20` | → `--shadow-ink-20` | EFFECT_COLOR | Color de la sombra suave (elevation/3) |
| `color/surface/disabled` | `--color-surface-disabled` | COLOR | → `--color-neutral-sand-200` | → `--color-neutral-sand-200` | → `--color-neutral-sand-200` | → `--color-neutral-sand-200` | → `--color-neutral-sand-200` | FRAME_FILL, SHAPE_FILL, STROKE_COLOR | Fondo de control desactivado |
| `color/text/disabled` | `--color-text-disabled` | COLOR | → `--color-neutral-ink-600` | → `--color-neutral-ink-600` | → `--color-neutral-ink-600` | → `--color-neutral-ink-600` | → `--color-neutral-ink-600` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | Texto o icono de control desactivado (4.3:1 sobre surface/disabled) |
| `color/surface/overlay` | `--color-surface-overlay` | COLOR | → `--overlay-ink-70` | → `--overlay-ink-70` | → `--overlay-ink-70` | → `--overlay-ink-70` | → `--overlay-ink-70` | FRAME_FILL, SHAPE_FILL | Velo detrás de modales y del menú móvil (layer/overlay). Única superficie translúcida; nunca lleva texto encima. |

## Components

| Token | CSS | Tipo | Value | Scopes | Descripción |
|---|---|---|---|---|---|
| `icon/size/sm` | `--icon-size-sm` | FLOAT | `16px` | WIDTH_HEIGHT | 16px. Iconos inline en texto y etiquetas |
| `icon/size/md` | `--icon-size-md` | FLOAT | `24px` | WIDTH_HEIGHT | 24px. Tamaño por defecto de icono |
| `icon/size/lg` | `--icon-size-lg` | FLOAT | `32px` | WIDTH_HEIGHT | 32px. Iconos destacados (checks de producto, sociales) |
| `icon/size/xl` | `--icon-size-xl` | FLOAT | `40px` | WIDTH_HEIGHT | 40px. Iconos grandes de bloque |
| `icon/color/default` | `--icon-color-default` | COLOR | → `--color-text-default` | FRAME_FILL, SHAPE_FILL, STROKE_COLOR | Color de icono por defecto (sobre page, brand, card) |
| `icon/color/inverse` | `--icon-color-inverse` | COLOR | → `--color-text-on-inverse` | FRAME_FILL, SHAPE_FILL, STROKE_COLOR | Color de icono sobre surface/inverse |
| `decoration/noodle/brand` | `--decoration-noodle-brand` | COLOR | → `--color-surface-brand` | FRAME_FILL, SHAPE_FILL | Fideo decorativo en color de marca |
| `decoration/noodle/accent` | `--decoration-noodle-accent` | COLOR | → `--color-surface-accent` | FRAME_FILL, SHAPE_FILL | Fideo decorativo en color de acento |
| `button/primary/bg` | `--button-primary-bg` | COLOR | → `--color-surface-inverse` | FRAME_FILL, SHAPE_FILL | button primary: Fondo |
| `button/primary/text` | `--button-primary-text` | COLOR | → `--color-text-on-inverse` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | button primary: Texto e icono |
| `button/primary/border` | `--button-primary-border` | COLOR | → `--color-border-default` | STROKE_COLOR | button primary: Borde |
| `button/primary/bg-hover` | `--button-primary-bg-hover` | COLOR | → `--color-surface-accent` | FRAME_FILL, SHAPE_FILL | button primary: Fondo en hover |
| `button/primary/text-hover` | `--button-primary-text-hover` | COLOR | → `--color-text-default` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | button primary: Texto e icono en hover |
| `button/primary/border-hover` | `--button-primary-border-hover` | COLOR | → `--color-border-default` | STROKE_COLOR | button primary: Borde en hover |
| `button/primary/focus-ring` | `--button-primary-focus-ring` | COLOR | → `--color-border-default` | STROKE_COLOR | button primary: Anillo de foco |
| `button/secondary/text` | `--button-secondary-text` | COLOR | → `--color-text-default` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | button secondary: Texto e icono |
| `button/secondary/border` | `--button-secondary-border` | COLOR | → `--color-border-default` | STROKE_COLOR | button secondary: Borde |
| `button/secondary/bg-hover` | `--button-secondary-bg-hover` | COLOR | → `--color-surface-inverse` | FRAME_FILL, SHAPE_FILL | button secondary: Fondo en hover |
| `button/secondary/text-hover` | `--button-secondary-text-hover` | COLOR | → `--color-text-on-inverse` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | button secondary: Texto e icono en hover |
| `button/secondary/border-hover` | `--button-secondary-border-hover` | COLOR | → `--color-border-default` | STROKE_COLOR | button secondary: Borde en hover |
| `button/secondary/focus-ring` | `--button-secondary-focus-ring` | COLOR | → `--color-border-default` | STROKE_COLOR | button secondary: Anillo de foco |
| `button/inverse/bg` | `--button-inverse-bg` | COLOR | → `--color-text-on-inverse` | FRAME_FILL, SHAPE_FILL | button inverse: Fondo |
| `button/inverse/text` | `--button-inverse-text` | COLOR | → `--color-text-default` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | button inverse: Texto e icono |
| `button/inverse/border` | `--button-inverse-border` | COLOR | → `--color-text-on-inverse` | STROKE_COLOR | button inverse: Borde |
| `button/inverse/bg-hover` | `--button-inverse-bg-hover` | COLOR | → `--color-surface-brand` | FRAME_FILL, SHAPE_FILL | button inverse: Fondo en hover |
| `button/inverse/text-hover` | `--button-inverse-text-hover` | COLOR | → `--color-text-default` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | button inverse: Texto e icono en hover |
| `button/inverse/border-hover` | `--button-inverse-border-hover` | COLOR | → `--color-surface-brand` | STROKE_COLOR | button inverse: Borde en hover |
| `button/inverse/focus-ring` | `--button-inverse-focus-ring` | COLOR | → `--color-text-brand-on-inverse` | STROKE_COLOR | button inverse: Anillo de foco |
| `button/disabled/bg` | `--button-disabled-bg` | COLOR | → `--color-surface-disabled` | FRAME_FILL, SHAPE_FILL | button disabled: Fondo |
| `button/disabled/text` | `--button-disabled-text` | COLOR | → `--color-text-disabled` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | button disabled: Texto e icono |
| `button/disabled/border` | `--button-disabled-border` | COLOR | → `--color-surface-disabled` | STROKE_COLOR | button disabled: Borde |
| `link/default` | `--link-default` | COLOR | → `--color-text-default` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | link: Color en reposo |
| `link/hover` | `--link-hover` | COLOR | → `--color-text-natural` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | link: Color en hover |
| `link/inverse` | `--link-inverse` | COLOR | → `--color-text-on-inverse` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | link: Sobre fondo oscuro |
| `link/inverse-hover` | `--link-inverse-hover` | COLOR | → `--color-text-brand-on-inverse` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | link: Hover sobre fondo oscuro |
| `badge/new/bg` | `--badge-new-bg` | COLOR | → `--color-surface-badge-new` | FRAME_FILL, SHAPE_FILL | badge new: Fondo |
| `badge/new/text` | `--badge-new-text` | COLOR | → `--color-text-on-badge` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | badge new: Texto e icono |
| `badge/natural/bg` | `--badge-natural-bg` | COLOR | → `--color-surface-natural` | FRAME_FILL, SHAPE_FILL | badge natural: Fondo |
| `badge/natural/text` | `--badge-natural-text` | COLOR | → `--color-text-on-natural` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | badge natural: Texto e icono |
| `badge/neutral/bg` | `--badge-neutral-bg` | COLOR | → `--color-surface-inverse` | FRAME_FILL, SHAPE_FILL | badge neutral: Fondo |
| `badge/neutral/text` | `--badge-neutral-text` | COLOR | → `--color-text-on-inverse` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | badge neutral: Texto e icono |
| `chip/bg` | `--chip-bg` | COLOR | → `--color-surface-card` | FRAME_FILL, SHAPE_FILL | chip: Fondo |
| `chip/text` | `--chip-text` | COLOR | → `--color-text-default` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | chip: Texto e icono |
| `chip/border` | `--chip-border` | COLOR | → `--color-border-default` | STROKE_COLOR | chip: Borde |
| `chip/bg-hover` | `--chip-bg-hover` | COLOR | → `--color-surface-brand` | FRAME_FILL, SHAPE_FILL | chip: Fondo en hover |
| `chip/bg-selected` | `--chip-bg-selected` | COLOR | → `--color-surface-inverse` | FRAME_FILL, SHAPE_FILL | chip: Fondo seleccionado |
| `chip/text-selected` | `--chip-text-selected` | COLOR | → `--color-text-on-inverse` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | chip: Texto seleccionado |
| `chip/bg-disabled` | `--chip-bg-disabled` | COLOR | → `--color-surface-disabled` | FRAME_FILL, SHAPE_FILL | chip: Fondo desactivado |
| `chip/text-disabled` | `--chip-text-disabled` | COLOR | → `--color-text-disabled` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | chip: Texto desactivado |
| `link/focus-ring` | `--link-focus-ring` | COLOR | → `--color-border-default` | STROKE_COLOR | link: Anillo de foco |
| `link/inverse-focus-ring` | `--link-inverse-focus-ring` | COLOR | → `--color-text-brand-on-inverse` | STROKE_COLOR | link: Anillo de foco sobre fondo oscuro |
| `field/bg` | `--field-bg` | COLOR | → `--color-surface-card` | FRAME_FILL, SHAPE_FILL | field: Fondo del campo |
| `field/bg-disabled` | `--field-bg-disabled` | COLOR | → `--color-surface-disabled` | FRAME_FILL, SHAPE_FILL | field: Fondo del campo desactivado |
| `field/border` | `--field-border` | COLOR | → `--color-border-default` | STROKE_COLOR | field: Borde del campo |
| `field/border-error` | `--field-border-error` | COLOR | → `--color-status-error-border` | STROKE_COLOR | field: Borde del campo con error |
| `field/border-disabled` | `--field-border-disabled` | COLOR | → `--color-surface-disabled` | STROKE_COLOR | field: Borde del campo desactivado |
| `field/focus-ring` | `--field-focus-ring` | COLOR | → `--color-border-default` | STROKE_COLOR | field: Anillo de foco del campo |
| `field/text` | `--field-text` | COLOR | → `--color-text-default` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | field: Valor escrito |
| `field/placeholder` | `--field-placeholder` | COLOR | → `--color-text-secondary` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | field: Placeholder |
| `field/label` | `--field-label` | COLOR | → `--color-text-default` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | field: Etiqueta del campo |
| `field/helper` | `--field-helper` | COLOR | → `--color-text-secondary` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | field: Texto de ayuda |
| `field/error-text` | `--field-error-text` | COLOR | → `--color-status-error-text` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | field: Mensaje e icono de error |
| `field/text-disabled` | `--field-text-disabled` | COLOR | → `--color-text-disabled` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | field: Texto desactivado |
| `field/icon` | `--field-icon` | COLOR | → `--color-text-default` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | field: Iconos del campo (lupa, chevron, borrar) |
| `field/menu-bg` | `--field-menu-bg` | COLOR | → `--color-surface-card` | FRAME_FILL, SHAPE_FILL | field: Fondo del menú desplegable |
| `field/option-hover-bg` | `--field-option-hover-bg` | COLOR | → `--color-surface-brand` | FRAME_FILL, SHAPE_FILL | field: Fondo de la opción en hover |
| `checkbox/box-bg` | `--checkbox-box-bg` | COLOR | → `--color-surface-card` | FRAME_FILL, SHAPE_FILL | checkbox: Fondo de la caja |
| `checkbox/box-bg-hover` | `--checkbox-box-bg-hover` | COLOR | → `--color-surface-brand` | FRAME_FILL, SHAPE_FILL | checkbox: Fondo de la caja en hover |
| `checkbox/box-border` | `--checkbox-box-border` | COLOR | → `--color-border-default` | STROKE_COLOR | checkbox: Borde de la caja |
| `checkbox/box-bg-checked` | `--checkbox-box-bg-checked` | COLOR | → `--color-surface-inverse` | FRAME_FILL, SHAPE_FILL | checkbox: Fondo de la caja marcada |
| `checkbox/check` | `--checkbox-check` | COLOR | → `--color-text-on-inverse` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | checkbox: Check sobre la caja marcada |
| `checkbox/label` | `--checkbox-label` | COLOR | → `--color-text-default` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | checkbox: Etiqueta |
| `checkbox/focus-ring` | `--checkbox-focus-ring` | COLOR | → `--color-border-default` | STROKE_COLOR | checkbox: Anillo de foco |
| `checkbox/bg-disabled` | `--checkbox-bg-disabled` | COLOR | → `--color-surface-disabled` | FRAME_FILL, SHAPE_FILL | checkbox: Fondo desactivado |
| `checkbox/text-disabled` | `--checkbox-text-disabled` | COLOR | → `--color-text-disabled` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | checkbox: Etiqueta y check desactivados |
| `checkbox/border-error` | `--checkbox-border-error` | COLOR | → `--color-status-error-border` | STROKE_COLOR | checkbox: Borde con error |
| `nav-item/text` | `--nav-item-text` | COLOR | → `--color-text-default` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | nav-item: Texto del enlace de navegación |
| `nav-item/text-active` | `--nav-item-text-active` | COLOR | → `--color-text-default` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | nav-item: Texto del enlace activo |
| `nav-item/indicator` | `--nav-item-indicator` | COLOR | → `--color-border-default` | FRAME_FILL, SHAPE_FILL | nav-item: Subrayado de la sección activa |
| `nav-item/hover-bg` | `--nav-item-hover-bg` | COLOR | → `--color-surface-brand` | FRAME_FILL, SHAPE_FILL | nav-item: Fondo en hover |
| `nav-item/focus-ring` | `--nav-item-focus-ring` | COLOR | → `--color-border-default` | STROKE_COLOR | nav-item: Anillo de foco |
| `nav-item/menu-text` | `--nav-item-menu-text` | COLOR | → `--color-text-on-inverse` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | nav-item: Texto en el menú móvil |
| `nav-item/menu-text-active` | `--nav-item-menu-text-active` | COLOR | → `--color-text-brand-on-inverse` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | nav-item: Texto activo en el menú móvil |
| `nav-item/menu-focus-ring` | `--nav-item-menu-focus-ring` | COLOR | → `--color-text-brand-on-inverse` | STROKE_COLOR | nav-item: Anillo de foco en el menú móvil |
| `tab/bg` | `--tab-bg` | COLOR | → `--color-surface-card` | FRAME_FILL, SHAPE_FILL | tab: Fondo |
| `tab/bg-hover` | `--tab-bg-hover` | COLOR | → `--color-surface-brand` | FRAME_FILL, SHAPE_FILL | tab: Fondo en hover |
| `tab/bg-selected` | `--tab-bg-selected` | COLOR | → `--color-surface-inverse` | FRAME_FILL, SHAPE_FILL | tab: Fondo seleccionado |
| `tab/text` | `--tab-text` | COLOR | → `--color-text-default` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | tab: Texto |
| `tab/text-selected` | `--tab-text-selected` | COLOR | → `--color-text-on-inverse` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | tab: Texto seleccionado |
| `tab/border` | `--tab-border` | COLOR | → `--color-border-default` | STROKE_COLOR | tab: Borde |
| `tab/focus-ring` | `--tab-focus-ring` | COLOR | → `--color-border-default` | STROKE_COLOR | tab: Anillo de foco |
| `lang-switch/bg` | `--lang-switch-bg` | COLOR | → `--color-surface-card` | FRAME_FILL, SHAPE_FILL | lang-switch: Fondo |
| `lang-switch/bg-selected` | `--lang-switch-bg-selected` | COLOR | → `--color-surface-inverse` | FRAME_FILL, SHAPE_FILL | lang-switch: Fondo de la opción seleccionada |
| `lang-switch/text` | `--lang-switch-text` | COLOR | → `--color-text-default` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | lang-switch: Texto |
| `lang-switch/text-selected` | `--lang-switch-text-selected` | COLOR | → `--color-text-on-inverse` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | lang-switch: Texto de la opción seleccionada |
| `lang-switch/border` | `--lang-switch-border` | COLOR | → `--color-border-default` | STROKE_COLOR | lang-switch: Borde |
| `chip/height/s` | `--chip-height-s` | FLOAT | `36px` | WIDTH_HEIGHT | chip: Altura mínima talla S (36px). Filtros densos y productos dentro de receta |
| `chip/height/m` | `--chip-height-m` | FLOAT | `40px` | WIDTH_HEIGHT | chip: Altura mínima talla M (40px). Filtros principales y uso táctil preferente |
| `product-card/bg` | `--product-card-bg` | COLOR | → `--color-surface-card` | FRAME_FILL, SHAPE_FILL | product-card: Fondo |
| `product-card/border` | `--product-card-border` | COLOR | → `--color-border-default` | STROKE_COLOR | product-card: Borde |
| `product-card/title` | `--product-card-title` | COLOR | → `--color-text-default` | TEXT_FILL | product-card: Nombre del producto |
| `product-card/meta` | `--product-card-meta` | COLOR | → `--color-text-secondary` | TEXT_FILL | product-card: Línea y texto secundario |
| `product-card/media-bg` | `--product-card-media-bg` | COLOR | → `--color-surface-page` | FRAME_FILL, SHAPE_FILL | product-card: Fondo del hueco de imagen |
| `product-card/focus-ring` | `--product-card-focus-ring` | COLOR | → `--color-border-default` | STROKE_COLOR | product-card: Anillo de foco |
| `recipe-card/bg` | `--recipe-card-bg` | COLOR | → `--color-surface-card` | FRAME_FILL, SHAPE_FILL | recipe-card: Fondo |
| `recipe-card/border` | `--recipe-card-border` | COLOR | → `--color-border-default` | STROKE_COLOR | recipe-card: Borde |
| `recipe-card/title` | `--recipe-card-title` | COLOR | → `--color-text-default` | TEXT_FILL | recipe-card: Título de la receta |
| `recipe-card/meta` | `--recipe-card-meta` | COLOR | → `--color-text-secondary` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | recipe-card: Tiempo y metadatos (texto e icono) |
| `recipe-card/media-bg` | `--recipe-card-media-bg` | COLOR | → `--color-surface-page` | FRAME_FILL, SHAPE_FILL | recipe-card: Fondo del hueco de imagen |
| `recipe-card/focus-ring` | `--recipe-card-focus-ring` | COLOR | → `--color-border-default` | STROKE_COLOR | recipe-card: Anillo de foco |
| `contest-card/bg` | `--contest-card-bg` | COLOR | → `--color-surface-card` | FRAME_FILL, SHAPE_FILL | contest-card: Fondo |
| `contest-card/border` | `--contest-card-border` | COLOR | → `--color-border-default` | STROKE_COLOR | contest-card: Borde |
| `contest-card/title` | `--contest-card-title` | COLOR | → `--color-text-default` | TEXT_FILL | contest-card: Título del concurso |
| `contest-card/meta` | `--contest-card-meta` | COLOR | → `--color-text-secondary` | TEXT_FILL | contest-card: Fechas y bases |
| `contest-card/media-bg` | `--contest-card-media-bg` | COLOR | → `--color-surface-page` | FRAME_FILL, SHAPE_FILL | contest-card: Fondo del hueco de imagen |
| `accordion/bg` | `--accordion-bg` | COLOR | → `--color-surface-card` | FRAME_FILL, SHAPE_FILL | accordion: Fondo |
| `accordion/bg-hover` | `--accordion-bg-hover` | COLOR | → `--color-surface-brand` | FRAME_FILL, SHAPE_FILL | accordion: Fondo en hover |
| `accordion/border` | `--accordion-border` | COLOR | → `--color-border-default` | STROKE_COLOR | accordion: Borde |
| `accordion/question` | `--accordion-question` | COLOR | → `--color-text-default` | TEXT_FILL | accordion: Pregunta |
| `accordion/answer` | `--accordion-answer` | COLOR | → `--color-text-default` | TEXT_FILL | accordion: Respuesta |
| `accordion/icon` | `--accordion-icon` | COLOR | → `--color-text-default` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | accordion: Icono plus/minus |
| `accordion/focus-ring` | `--accordion-focus-ring` | COLOR | → `--color-border-default` | STROKE_COLOR | accordion: Anillo de foco |
| `ingredient/text` | `--ingredient-text` | COLOR | → `--color-text-default` | TEXT_FILL | ingredient: Nombre del ingrediente y texto corrido (alérgenos en negrita) |
| `ingredient/percent-bg` | `--ingredient-percent-bg` | COLOR | → `--color-surface-natural` | FRAME_FILL, SHAPE_FILL | ingredient: Fondo del porcentaje |
| `ingredient/percent-text` | `--ingredient-percent-text` | COLOR | → `--color-text-on-natural` | TEXT_FILL | ingredient: Texto del porcentaje |
| `ingredient/divider` | `--ingredient-divider` | COLOR | → `--color-border-subtle` | STROKE_COLOR | ingredient: Filete entre ingredientes principales (decorativo) |
| `nutrition/label` | `--nutrition-label` | COLOR | → `--color-text-default` | TEXT_FILL | nutrition: Nombre del nutriente |
| `nutrition/value` | `--nutrition-value` | COLOR | → `--color-text-default` | TEXT_FILL | nutrition: Valor por 100 g |
| `nutrition/meta` | `--nutrition-meta` | COLOR | → `--color-text-secondary` | TEXT_FILL | nutrition: % de ingesta de referencia y notas |
| `nutrition/track` | `--nutrition-track` | COLOR | → `--color-border-subtle` | FRAME_FILL, SHAPE_FILL | nutrition: Pista de la barra (decorativa) |
| `nutrition/fill` | `--nutrition-fill` | COLOR | → `--color-surface-inverse` | FRAME_FILL, SHAPE_FILL | nutrition: Relleno de la barra (≥3:1 sobre la pista) |
| `nutrition/fill-highlight` | `--nutrition-fill-highlight` | COLOR | → `--color-surface-natural` | FRAME_FILL, SHAPE_FILL | nutrition: Relleno destacado para claims (≥3:1 sobre la pista) |
| `nutrition/allergen` | `--nutrition-allergen` | COLOR | → `--color-text-default` | TEXT_FILL | nutrition: Línea de alérgenos (en negrita) |
| `step/number-bg` | `--step-number-bg` | COLOR | → `--color-surface-brand` | FRAME_FILL, SHAPE_FILL | step: Fondo del número |
| `step/number-text` | `--step-number-text` | COLOR | → `--color-text-default` | TEXT_FILL | step: Número del paso |
| `step/text` | `--step-text` | COLOR | → `--color-text-default` | TEXT_FILL | step: Texto del paso |
| `step/media-bg` | `--step-media-bg` | COLOR | → `--color-surface-page` | FRAME_FILL, SHAPE_FILL | step: Fondo del hueco de imagen o GIF |
| `step/border` | `--step-border` | COLOR | → `--color-border-default` | STROKE_COLOR | step: Borde del número y del media |
| `ingredient/meta` | `--ingredient-meta` | COLOR | → `--color-text-secondary` | TEXT_FILL | ingredient: Notas y texto secundario |
| `nutrition/bg` | `--nutrition-bg` | COLOR | → `--color-surface-card` | FRAME_FILL, SHAPE_FILL | nutrition: Fondo del panel |
| `nutrition/border` | `--nutrition-border` | COLOR | → `--color-border-default` | STROKE_COLOR | nutrition: Borde del panel |
| `modal/bg` | `--modal-bg` | COLOR | → `--color-surface-card` | FRAME_FILL, SHAPE_FILL | modal: Fondo del diálogo |
| `modal/border` | `--modal-border` | COLOR | → `--color-border-default` | STROKE_COLOR | modal: Borde del diálogo |
| `modal/title` | `--modal-title` | COLOR | → `--color-text-default` | TEXT_FILL | modal: Título |
| `modal/text` | `--modal-text` | COLOR | → `--color-text-default` | TEXT_FILL | modal: Texto del cuerpo |
| `modal/overlay` | `--modal-overlay` | COLOR | → `--color-surface-overlay` | FRAME_FILL, SHAPE_FILL | modal: Velo detrás del diálogo (translúcido) |
| `modal/slot-bg` | `--modal-slot-bg` | COLOR | → `--color-surface-page` | FRAME_FILL, SHAPE_FILL | modal: Fondo del hueco de contenido (imagen de etiqueta, resultados) |
| `suggestion/bg` | `--suggestion-bg` | COLOR | → `--color-surface-inverse` | FRAME_FILL, SHAPE_FILL | suggestion: Fondo |
| `suggestion/bg-hover` | `--suggestion-bg-hover` | COLOR | → `--color-surface-brand` | FRAME_FILL, SHAPE_FILL | suggestion: Fondo en hover |
| `suggestion/text` | `--suggestion-text` | COLOR | → `--color-text-on-inverse` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | suggestion: Texto e icono |
| `suggestion/text-hover` | `--suggestion-text-hover` | COLOR | → `--color-text-default` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | suggestion: Texto e icono en hover |
| `suggestion/border` | `--suggestion-border` | COLOR | → `--color-border-default` | STROKE_COLOR | suggestion: Borde |
| `suggestion/focus-ring` | `--suggestion-focus-ring` | COLOR | → `--color-border-default` | STROKE_COLOR | suggestion: Anillo de foco |
| `timer/bg` | `--timer-bg` | COLOR | → `--color-surface-card` | FRAME_FILL, SHAPE_FILL | timer: Fondo |
| `timer/border` | `--timer-border` | COLOR | → `--color-border-default` | STROKE_COLOR | timer: Borde |
| `timer/track` | `--timer-track` | COLOR | → `--color-border-subtle` | SHAPE_FILL, STROKE_COLOR | timer: Pista del anillo (decorativa) |
| `timer/progress` | `--timer-progress` | COLOR | → `--color-surface-inverse` | SHAPE_FILL, STROKE_COLOR | timer: Progreso del anillo (≥3:1 sobre la pista) |
| `timer/progress-done` | `--timer-progress-done` | COLOR | → `--color-surface-natural` | SHAPE_FILL, STROKE_COLOR | timer: Anillo completo al terminar |
| `timer/time` | `--timer-time` | COLOR | → `--color-text-default` | TEXT_FILL | timer: Tiempo restante |
| `timer/label` | `--timer-label` | COLOR | → `--color-text-secondary` | TEXT_FILL | timer: Etiqueta y ayuda |
| `timer/done-text` | `--timer-done-text` | COLOR | → `--color-text-natural` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | timer: Mensaje e icono de terminado |
| `video/poster-bg` | `--video-poster-bg` | COLOR | → `--color-surface-inverse` | FRAME_FILL, SHAPE_FILL | video: Fondo del póster hasta tener imagen |
| `video/border` | `--video-border` | COLOR | → `--color-border-default` | STROKE_COLOR | video: Borde |
| `video/play-bg` | `--video-play-bg` | COLOR | → `--color-surface-brand` | FRAME_FILL, SHAPE_FILL | video: Fondo del botón play |
| `video/play-icon` | `--video-play-icon` | COLOR | → `--color-text-default` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | video: Icono play |
| `video/meta-bg` | `--video-meta-bg` | COLOR | → `--color-surface-inverse` | FRAME_FILL, SHAPE_FILL | video: Fondo de la duración |
| `video/meta-text` | `--video-meta-text` | COLOR | → `--color-text-on-inverse` | TEXT_FILL | video: Texto de la duración y del póster |
| `video/focus-ring` | `--video-focus-ring` | COLOR | → `--color-text-brand-on-inverse` | STROKE_COLOR | video: Anillo de foco del play (amarillo sobre póster oscuro) |
| `alert/info/bg` | `--alert-info-bg` | COLOR | → `--color-status-info-bg` | FRAME_FILL, SHAPE_FILL | alert: Fondo (info) |
| `alert/info/text` | `--alert-info-text` | COLOR | → `--color-status-info-text` | TEXT_FILL | alert: Texto (info) |
| `alert/info/icon` | `--alert-info-icon` | COLOR | → `--color-status-info-icon` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | alert: Icono (info) |
| `alert/info/border` | `--alert-info-border` | COLOR | → `--color-status-info-border` | STROKE_COLOR | alert: Borde (info) |
| `alert/success/bg` | `--alert-success-bg` | COLOR | → `--color-status-success-bg` | FRAME_FILL, SHAPE_FILL | alert: Fondo (success) |
| `alert/success/text` | `--alert-success-text` | COLOR | → `--color-status-success-text` | TEXT_FILL | alert: Texto (success) |
| `alert/success/icon` | `--alert-success-icon` | COLOR | → `--color-status-success-icon` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | alert: Icono (success) |
| `alert/success/border` | `--alert-success-border` | COLOR | → `--color-status-success-border` | STROKE_COLOR | alert: Borde (success) |
| `alert/alert/bg` | `--alert-alert-bg` | COLOR | → `--color-status-alert-bg` | FRAME_FILL, SHAPE_FILL | alert: Fondo (alert) |
| `alert/alert/text` | `--alert-alert-text` | COLOR | → `--color-status-alert-text` | TEXT_FILL | alert: Texto (alert) |
| `alert/alert/icon` | `--alert-alert-icon` | COLOR | → `--color-status-alert-icon` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | alert: Icono (alert) |
| `alert/alert/border` | `--alert-alert-border` | COLOR | → `--color-status-alert-border` | STROKE_COLOR | alert: Borde (alert) |
| `alert/error/bg` | `--alert-error-bg` | COLOR | → `--color-status-error-bg` | FRAME_FILL, SHAPE_FILL | alert: Fondo (error) |
| `alert/error/text` | `--alert-error-text` | COLOR | → `--color-status-error-text` | TEXT_FILL | alert: Texto (error) |
| `alert/error/icon` | `--alert-error-icon` | COLOR | → `--color-status-error-icon` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | alert: Icono (error) |
| `alert/error/border` | `--alert-error-border` | COLOR | → `--color-status-error-border` | STROKE_COLOR | alert: Borde (error) |
| `alert/close` | `--alert-close` | COLOR | → `--color-text-default` | SHAPE_FILL, TEXT_FILL, STROKE_COLOR | alert: Icono cerrar |

## Layer

| Token | CSS | Tipo | Value | Scopes | Descripción |
|---|---|---|---|---|---|
| `layer/base` | `--layer-base` | FLOAT | `0` | — | z-index 0. Contenido normal de la página |
| `layer/raised` | `--layer-raised` | FLOAT | `10` | — | z-index 10. Contenido por encima de imágenes dentro de una sección (copy del hero, banderas) |
| `layer/sticky` | `--layer-sticky` | FLOAT | `100` | — | z-index 100. Navbar que se oculta al bajar y reaparece al subir |
| `layer/floating` | `--layer-floating` | FLOAT | `200` | — | z-index 200. Suggestion bubble flotante |
| `layer/overlay` | `--layer-overlay` | FLOAT | `300` | — | z-index 300. Velo (scrim) detrás de modales |
| `layer/modal` | `--layer-modal` | FLOAT | `400` | — | z-index 400. Modales: etiqueta del envase, alérgenos, resultados |
| `layer/toast` | `--layer-toast` | FLOAT | `500` | — | z-index 500. Avisos temporales por encima de todo |

## Spacing

| Token | CSS | Tipo | Value | Scopes | Descripción |
|---|---|---|---|---|---|
| `space/2` | `--space-2` | FLOAT | `2px` | GAP | 2px · excepción del grid (hairline/micro) |
| `space/4` | `--space-4` | FLOAT | `4px` | GAP | 4px · excepción del grid (hairline/micro) |
| `space/8` | `--space-8` | FLOAT | `8px` | GAP | 8px · grid de 8 |
| `space/16` | `--space-16` | FLOAT | `16px` | GAP | 16px · grid de 8 |
| `space/24` | `--space-24` | FLOAT | `24px` | GAP | 24px · grid de 8 |
| `space/32` | `--space-32` | FLOAT | `32px` | GAP | 32px · grid de 8 |
| `space/40` | `--space-40` | FLOAT | `40px` | GAP | 40px · grid de 8 |
| `space/48` | `--space-48` | FLOAT | `48px` | GAP | 48px · grid de 8 |
| `space/56` | `--space-56` | FLOAT | `56px` | GAP | 56px · grid de 8 |
| `space/64` | `--space-64` | FLOAT | `64px` | GAP | 64px · grid de 8 |
| `space/80` | `--space-80` | FLOAT | `80px` | GAP | 80px · grid de 8 |
| `space/96` | `--space-96` | FLOAT | `96px` | GAP | 96px · grid de 8 |
| `space/128` | `--space-128` | FLOAT | `128px` | GAP | 128px · grid de 8 |
| `radius/none` | `--radius-none` | FLOAT | `0` | CORNER_RADIUS | Sin radio |
| `radius/sm` | `--radius-sm` | FLOAT | `8px` | CORNER_RADIUS | Inputs, chips, etiquetas |
| `radius/md` | `--radius-md` | FLOAT | `16px` | CORNER_RADIUS | Cards y media |
| `radius/lg` | `--radius-lg` | FLOAT | `24px` | CORNER_RADIUS | Bloques y módulos grandes |
| `radius/pill` | `--radius-pill` | FLOAT | `999px` | CORNER_RADIUS | Botones y pills (totalmente redondeado) |
| `border/width/thin` | `--border-width-thin` | FLOAT | `2px` | STROKE_FLOAT | Hairline: separadores, inputs en reposo |
| `border/width/thick` | `--border-width-thick` | FLOAT | `4px` | STROKE_FLOAT | Borde de marca: botón secundario, foco, cards destacadas |

## Layout

| Token | CSS | Tipo | Desktop | Tablet | Mobile | Scopes | Descripción |
|---|---|---|---|---|---|---|---|
| `layout/columns` | `--layout-columns` | FLOAT | `12` | `8` | `4` | — | Número de columnas del grid |
| `layout/margin` | `--layout-margin` | FLOAT | `64px` | `40px` | `24px` | GAP | Margen lateral de página |
| `layout/gutter` | `--layout-gutter` | FLOAT | `24px` | `24px` | `16px` | GAP | Separación entre columnas |
| `layout/content-max` | `--layout-content-max` | FLOAT | `1280px` | `1280px` | `1280px` | WIDTH_HEIGHT | Ancho máximo del contenido |
| `layout/frame` | `--layout-frame` | FLOAT | `1440px` | `768px` | `375px` | WIDTH_HEIGHT | Ancho del frame de diseño de referencia |
| `layout/section-y` | `--layout-section-y` | FLOAT | `96px` | `80px` | `64px` | GAP | Padding vertical entre secciones |
| `layout/reading` | `--layout-reading` | FLOAT | `720px` | `720px` | `720px` | WIDTH_HEIGHT | Ancho máximo de la columna de lectura (720 px): legales, respuestas del FAQ, textos largos de Natural formula. Es un máximo: en móvil manda el ancho de la columna. |

## Typography

| Token | CSS | Tipo | Yatekomo | Saikebon | Aiki | Daisuki | DE | Scopes | Descripción |
|---|---|---|---|---|---|---|---|---|---|
| `font/family/display` | `--font-family-display` | STRING | `Anton` | `Anton` | `Anton` | `Anton` | `Anton` | FONT_FAMILY | Display: titulares, labels de botón. Siempre mayúsculas. Provisional hasta resolver licencia/fuente con acentos |
| `font/family/body` | `--font-family-body` | STRING | `Archivo` | `Archivo` | `Archivo` | `Archivo` | `Archivo` | FONT_FAMILY | Texto corrido, formularios, navegación |
| `font/style/display` | `--font-style-display` | STRING | `Regular` | `Regular` | `Regular` | `Regular` | `Regular` | FONT_STYLE | Anton solo tiene Regular |
| `font/style/body` | `--font-style-body` | STRING | `Regular` | `Regular` | `Regular` | `Regular` | `Regular` | FONT_STYLE | Cuerpo regular |
| `font/style/body-strong` | `--font-style-body-strong` | STRING | `Bold` | `Bold` | `Bold` | `Bold` | `Bold` | FONT_STYLE | Cuerpo en negrita (alérgenos, énfasis) |
| `font/size/desktop/display` | `--font-size-desktop-display` | FLOAT | `96px` | `96px` | `96px` | `96px` | `96px` | FONT_SIZE | display desktop: 96px |
| `font/line-height/desktop/display` | `--font-line-height-desktop-display` | FLOAT | `96px` | `96px` | `96px` | `96px` | `96px` | LINE_HEIGHT | display desktop: interlineado 1.0 |
| `font/size/mobile/display` | `--font-size-mobile-display` | FLOAT | `56px` | `56px` | `56px` | `56px` | `56px` | FONT_SIZE | display mobile: 56px |
| `font/line-height/mobile/display` | `--font-line-height-mobile-display` | FLOAT | `56px` | `56px` | `56px` | `56px` | `56px` | LINE_HEIGHT | display mobile: interlineado 1.0 |
| `font/size/desktop/h1` | `--font-size-desktop-h1` | FLOAT | `64px` | `64px` | `64px` | `64px` | `64px` | FONT_SIZE | h1 desktop: 64px |
| `font/line-height/desktop/h1` | `--font-line-height-desktop-h1` | FLOAT | `68px` | `68px` | `68px` | `68px` | `68px` | LINE_HEIGHT | h1 desktop: interlineado 1.05 |
| `font/size/mobile/h1` | `--font-size-mobile-h1` | FLOAT | `40px` | `40px` | `40px` | `40px` | `40px` | FONT_SIZE | h1 mobile: 40px |
| `font/line-height/mobile/h1` | `--font-line-height-mobile-h1` | FLOAT | `40px` | `40px` | `40px` | `40px` | `40px` | LINE_HEIGHT | h1 mobile: interlineado 1.05 |
| `font/size/desktop/h2` | `--font-size-desktop-h2` | FLOAT | `48px` | `48px` | `48px` | `48px` | `48px` | FONT_SIZE | h2 desktop: 48px |
| `font/line-height/desktop/h2` | `--font-line-height-desktop-h2` | FLOAT | `52px` | `52px` | `52px` | `52px` | `52px` | LINE_HEIGHT | h2 desktop: interlineado 1.1 |
| `font/size/mobile/h2` | `--font-size-mobile-h2` | FLOAT | `32px` | `32px` | `32px` | `32px` | `32px` | FONT_SIZE | h2 mobile: 32px |
| `font/line-height/mobile/h2` | `--font-line-height-mobile-h2` | FLOAT | `36px` | `36px` | `36px` | `36px` | `36px` | LINE_HEIGHT | h2 mobile: interlineado 1.1 |
| `font/size/desktop/h3` | `--font-size-desktop-h3` | FLOAT | `32px` | `32px` | `32px` | `32px` | `32px` | FONT_SIZE | h3 desktop: 32px |
| `font/line-height/desktop/h3` | `--font-line-height-desktop-h3` | FLOAT | `36px` | `36px` | `36px` | `36px` | `36px` | LINE_HEIGHT | h3 desktop: interlineado 1.15 |
| `font/size/mobile/h3` | `--font-size-mobile-h3` | FLOAT | `24px` | `24px` | `24px` | `24px` | `24px` | FONT_SIZE | h3 mobile: 24px |
| `font/line-height/mobile/h3` | `--font-line-height-mobile-h3` | FLOAT | `28px` | `28px` | `28px` | `28px` | `28px` | LINE_HEIGHT | h3 mobile: interlineado 1.15 |
| `font/size/desktop/label` | `--font-size-desktop-label` | FLOAT | `16px` | `16px` | `16px` | `16px` | `16px` | FONT_SIZE | label desktop: 16px |
| `font/line-height/desktop/label` | `--font-line-height-desktop-label` | FLOAT | `16px` | `16px` | `16px` | `16px` | `16px` | LINE_HEIGHT | label desktop: interlineado 1.0 |
| `font/size/mobile/label` | `--font-size-mobile-label` | FLOAT | `14px` | `14px` | `14px` | `14px` | `14px` | FONT_SIZE | label mobile: 14px |
| `font/line-height/mobile/label` | `--font-line-height-mobile-label` | FLOAT | `16px` | `16px` | `16px` | `16px` | `16px` | LINE_HEIGHT | label mobile: interlineado 1.0 |
| `font/size/desktop/body-l` | `--font-size-desktop-body-l` | FLOAT | `20px` | `20px` | `20px` | `20px` | `20px` | FONT_SIZE | body-l desktop: 20px |
| `font/line-height/desktop/body-l` | `--font-line-height-desktop-body-l` | FLOAT | `32px` | `32px` | `32px` | `32px` | `32px` | LINE_HEIGHT | body-l desktop: interlineado 1.5 |
| `font/size/mobile/body-l` | `--font-size-mobile-body-l` | FLOAT | `18px` | `18px` | `18px` | `18px` | `18px` | FONT_SIZE | body-l mobile: 18px |
| `font/line-height/mobile/body-l` | `--font-line-height-mobile-body-l` | FLOAT | `28px` | `28px` | `28px` | `28px` | `28px` | LINE_HEIGHT | body-l mobile: interlineado 1.5 |
| `font/size/desktop/body-m` | `--font-size-desktop-body-m` | FLOAT | `16px` | `16px` | `16px` | `16px` | `16px` | FONT_SIZE | body-m desktop: 16px |
| `font/line-height/desktop/body-m` | `--font-line-height-desktop-body-m` | FLOAT | `24px` | `24px` | `24px` | `24px` | `24px` | LINE_HEIGHT | body-m desktop: interlineado 1.5 |
| `font/size/mobile/body-m` | `--font-size-mobile-body-m` | FLOAT | `16px` | `16px` | `16px` | `16px` | `16px` | FONT_SIZE | body-m mobile: 16px |
| `font/line-height/mobile/body-m` | `--font-line-height-mobile-body-m` | FLOAT | `24px` | `24px` | `24px` | `24px` | `24px` | LINE_HEIGHT | body-m mobile: interlineado 1.5 |
| `font/size/desktop/body-s` | `--font-size-desktop-body-s` | FLOAT | `14px` | `14px` | `14px` | `14px` | `14px` | FONT_SIZE | body-s desktop: 14px |
| `font/line-height/desktop/body-s` | `--font-line-height-desktop-body-s` | FLOAT | `20px` | `20px` | `20px` | `20px` | `20px` | LINE_HEIGHT | body-s desktop: interlineado 1.5 |
| `font/size/mobile/body-s` | `--font-size-mobile-body-s` | FLOAT | `14px` | `14px` | `14px` | `14px` | `14px` | FONT_SIZE | body-s mobile: 14px |
| `font/line-height/mobile/body-s` | `--font-line-height-mobile-body-s` | FLOAT | `20px` | `20px` | `20px` | `20px` | `20px` | LINE_HEIGHT | body-s mobile: interlineado 1.5 |
| `font/size/desktop/caption` | `--font-size-desktop-caption` | FLOAT | `12px` | `12px` | `12px` | `12px` | `12px` | FONT_SIZE | caption desktop: 12px |
| `font/line-height/desktop/caption` | `--font-line-height-desktop-caption` | FLOAT | `16px` | `16px` | `16px` | `16px` | `16px` | LINE_HEIGHT | caption desktop: interlineado 1.4 |
| `font/size/mobile/caption` | `--font-size-mobile-caption` | FLOAT | `12px` | `12px` | `12px` | `12px` | `12px` | FONT_SIZE | caption mobile: 12px |
| `font/line-height/mobile/caption` | `--font-line-height-mobile-caption` | FLOAT | `16px` | `16px` | `16px` | `16px` | `16px` | LINE_HEIGHT | caption mobile: interlineado 1.4 |

## Motion

| Token | CSS | Tipo | Value | Scopes | Descripción |
|---|---|---|---|---|---|
| `motion/duration/fast` | `--motion-duration-fast` | FLOAT | `150ms` | — | Microinteracciones: hover, foco |
| `motion/duration/base` | `--motion-duration-base` | FLOAT | `250ms` | — | Transiciones por defecto |
| `motion/duration/slow` | `--motion-duration-slow` | FLOAT | `400ms` | — | Entradas de modales y paneles |
| `motion/easing/standard` | `--motion-easing-standard` | STRING | `cubic-bezier(0.2, 0, 0, 1)` | — | Easing por defecto |
| `motion/easing/emphasized` | `--motion-easing-emphasized` | STRING | `cubic-bezier(0.3, 1.3, 0.4, 1)` | — | Con rebote: momentos de marca |

## Foundations

| Familia | Estado | Tokens |
|---|---|---|
| Icon size (`--icon-size-*`) | ✅ definida | icon/size/* |
| Layer (`--z-*`) | ✅ definida | layer/* |
| Motion (`--motion-*`) | ✅ definida | motion/* |
| Elevation (`--elevation-*`) | ✅ definida | effect styles elevation/* |

## Text styles

| Estilo | CSS | Familia | Peso/estilo | Tamaño | Interlineado | Tracking |
|---|---|---|---|---|---|---|
| Desktop/display | `--font-desktop-display-*` | Anton | Regular | 96 | {"unit": "PIXELS", "value": 96} | {"unit": "PERCENT", "value": 0} |
| Desktop/h1 | `--font-desktop-h1-*` | Anton | Regular | 64 | {"unit": "PIXELS", "value": 68} | {"unit": "PERCENT", "value": 0} |
| Desktop/h2 | `--font-desktop-h2-*` | Anton | Regular | 48 | {"unit": "PIXELS", "value": 52} | {"unit": "PERCENT", "value": 0} |
| Desktop/h3 | `--font-desktop-h3-*` | Anton | Regular | 32 | {"unit": "PIXELS", "value": 36} | {"unit": "PERCENT", "value": 0} |
| Desktop/label | `--font-desktop-label-*` | Anton | Regular | 16 | {"unit": "PIXELS", "value": 16} | {"unit": "PERCENT", "value": 0} |
| Desktop/body-l | `--font-desktop-body-l-*` | Archivo | Regular | 20 | {"unit": "PIXELS", "value": 32} | {"unit": "PERCENT", "value": 0} |
| Desktop/body-m | `--font-desktop-body-m-*` | Archivo | Regular | 16 | {"unit": "PIXELS", "value": 24} | {"unit": "PERCENT", "value": 0} |
| Desktop/body-s | `--font-desktop-body-s-*` | Archivo | Regular | 14 | {"unit": "PIXELS", "value": 20} | {"unit": "PERCENT", "value": 0} |
| Desktop/caption | `--font-desktop-caption-*` | Archivo | Regular | 12 | {"unit": "PIXELS", "value": 16} | {"unit": "PERCENT", "value": 0} |
| Mobile/display | `--font-mobile-display-*` | Anton | Regular | 56 | {"unit": "PIXELS", "value": 56} | {"unit": "PERCENT", "value": 0} |
| Mobile/h1 | `--font-mobile-h1-*` | Anton | Regular | 40 | {"unit": "PIXELS", "value": 40} | {"unit": "PERCENT", "value": 0} |
| Mobile/h2 | `--font-mobile-h2-*` | Anton | Regular | 32 | {"unit": "PIXELS", "value": 36} | {"unit": "PERCENT", "value": 0} |
| Mobile/h3 | `--font-mobile-h3-*` | Anton | Regular | 24 | {"unit": "PIXELS", "value": 28} | {"unit": "PERCENT", "value": 0} |
| Mobile/label | `--font-mobile-label-*` | Anton | Regular | 14 | {"unit": "PIXELS", "value": 16} | {"unit": "PERCENT", "value": 0} |
| Mobile/body-l | `--font-mobile-body-l-*` | Archivo | Regular | 18 | {"unit": "PIXELS", "value": 28} | {"unit": "PERCENT", "value": 0} |
| Mobile/body-m | `--font-mobile-body-m-*` | Archivo | Regular | 16 | {"unit": "PIXELS", "value": 24} | {"unit": "PERCENT", "value": 0} |
| Mobile/body-s | `--font-mobile-body-s-*` | Archivo | Regular | 14 | {"unit": "PIXELS", "value": 20} | {"unit": "PERCENT", "value": 0} |
| Mobile/caption | `--font-mobile-caption-*` | Archivo | Regular | 12 | {"unit": "PIXELS", "value": 16} | {"unit": "PERCENT", "value": 0} |
