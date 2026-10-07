<!-- ⚙️ ARCHIVO GENERADO por scripts/ds-sync.py — NO EDITAR A MANO. -->

# GB Noodles · Microsites · Tokens  ·  _(espejo generado de Figma)_

> Última sync: **2026-10-07T08:51:38Z** · modo de adopción: `new` · 94 variables en 6 colecciones · 6 text styles · 0 effect styles.
> Cada token se consume en código como `var(--nombre)`. Los alias conservan su referencia y su valor resuelto.

## Índice

- [Primitive](#primitive) · 20 tokens · modos: Value
- [Semantic](#semantic) · 34 tokens · modos: Yatekomo
- [Spacing](#spacing) · 17 tokens · modos: Value
- [Layout](#layout) · 5 tokens · modos: Desktop, Mobile
- [Typography](#typography) · 16 tokens · modos: Desktop, Mobile
- [Motion](#motion) · 2 tokens · modos: Value
- [Foundations](#foundations)
- [Text styles](#text-styles)

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

## Semantic

| Token | CSS | Tipo | Yatekomo | Scopes | Descripción |
|---|---|---|---|---|---|
| `color/surface/page` | `--color-surface-page` | COLOR | → `--color-yatekomo-yellow-soft` | FRAME_FILL, SHAPE_FILL | Fondo base de página |
| `color/surface/brand` | `--color-surface-brand` | COLOR | → `--color-yatekomo-yellow` | FRAME_FILL, SHAPE_FILL | Fondo de marca (amarillo común a todas las marcas) |
| `color/surface/card` | `--color-surface-card` | COLOR | → `--color-neutral-white` | FRAME_FILL, SHAPE_FILL | Fondo de card clara |
| `color/surface/inverse` | `--color-surface-inverse` | COLOR | → `--color-neutral-ink-900` | FRAME_FILL, SHAPE_FILL | Secciones y fondos oscuros |
| `color/surface/natural` | `--color-surface-natural` | COLOR | → `--color-yatekomo-green` | FRAME_FILL, SHAPE_FILL | Fondo del claim natural; texto encima: color/text/on-natural |
| `color/surface/accent` | `--color-surface-accent` | COLOR | → `--color-yatekomo-orange` | FRAME_FILL, SHAPE_FILL | Acento decorativo. Texto encima solo color/text/default |
| `color/surface/badge-new` | `--color-surface-badge-new` | COLOR | → `--color-red-600` | FRAME_FILL, SHAPE_FILL | Pill NUEVO; texto encima: color/text/on-badge |
| `color/text/default` | `--color-text-default` | COLOR | → `--color-neutral-ink-900` | TEXT_FILL | Texto principal (≥12:1 sobre page, brand y card) |
| `color/text/secondary` | `--color-text-secondary` | COLOR | → `--color-neutral-ink-600` | TEXT_FILL | Texto secundario. Solo sobre page o card (5.4:1); NO sobre brand (3.85:1) |
| `color/text/on-inverse` | `--color-text-on-inverse` | COLOR | → `--color-yatekomo-yellow-soft` | TEXT_FILL | Texto sobre surface/inverse (17:1) |
| `color/text/brand-on-inverse` | `--color-text-brand-on-inverse` | COLOR | → `--color-yatekomo-yellow` | TEXT_FILL | Texto destacado amarillo sobre surface/inverse (12:1) |
| `color/text/on-natural` | `--color-text-on-natural` | COLOR | → `--color-neutral-white` | TEXT_FILL | Texto sobre surface/natural (5.5:1) |
| `color/text/natural` | `--color-text-natural` | COLOR | → `--color-yatekomo-green` | TEXT_FILL | Texto verde natural sobre page (5.0:1). Sobre brand solo texto grande (3.6:1) |
| `color/text/on-badge` | `--color-text-on-badge` | COLOR | → `--color-neutral-white` | TEXT_FILL | Texto sobre surface/badge-new (4.7:1) |
| `color/border/default` | `--color-border-default` | COLOR | → `--color-neutral-ink-900` | STROKE_COLOR | Borde de componentes (botón ghost, formularios) |
| `color/border/subtle` | `--color-border-subtle` | COLOR | → `--color-neutral-sand-200` | STROKE_COLOR | Filete decorativo de tablas. NO para límites de controles (1.3:1) |
| `color/effect/shadow-brand` | `--color-effect-shadow-brand` | COLOR | → `--color-yatekomo-yellow` | EFFECT_COLOR | Color de sombra dura de marca |
| `color/effect/shadow-ink` | `--color-effect-shadow-ink` | COLOR | → `--color-neutral-ink-900` | EFFECT_COLOR | Color de sombra dura neutra |
| `color/status/error/bg` | `--color-status-error-bg` | COLOR | → `--color-status-error-50` | FRAME_FILL, SHAPE_FILL | Fondo de mensaje de error |
| `color/status/error/text` | `--color-status-error-text` | COLOR | → `--color-status-error-900` | TEXT_FILL | Texto de error sobre su bg (≥6.6:1) |
| `color/status/error/icon` | `--color-status-error-icon` | COLOR | → `--color-status-error-700` | FRAME_FILL, SHAPE_FILL | Icono de error (≥4.7:1 sobre bg y page) |
| `color/status/error/border` | `--color-status-error-border` | COLOR | → `--color-status-error-700` | STROKE_COLOR | Borde de error (≥4.7:1) |
| `color/status/success/bg` | `--color-status-success-bg` | COLOR | → `--color-status-success-50` | FRAME_FILL, SHAPE_FILL | Fondo de mensaje de success |
| `color/status/success/text` | `--color-status-success-text` | COLOR | → `--color-status-success-900` | TEXT_FILL | Texto de success sobre su bg (≥6.6:1) |
| `color/status/success/icon` | `--color-status-success-icon` | COLOR | → `--color-yatekomo-green` | FRAME_FILL, SHAPE_FILL | Icono de success (≥4.7:1 sobre bg y page) |
| `color/status/success/border` | `--color-status-success-border` | COLOR | → `--color-yatekomo-green` | STROKE_COLOR | Borde de success (≥4.7:1) |
| `color/status/alert/bg` | `--color-status-alert-bg` | COLOR | → `--color-status-alert-50` | FRAME_FILL, SHAPE_FILL | Fondo de mensaje de alert |
| `color/status/alert/text` | `--color-status-alert-text` | COLOR | → `--color-status-alert-900` | TEXT_FILL | Texto de alert sobre su bg (≥6.6:1) |
| `color/status/alert/icon` | `--color-status-alert-icon` | COLOR | → `--color-status-alert-700` | FRAME_FILL, SHAPE_FILL | Icono de alert (≥4.7:1 sobre bg y page) |
| `color/status/alert/border` | `--color-status-alert-border` | COLOR | → `--color-status-alert-700` | STROKE_COLOR | Borde de alert (≥4.7:1) |
| `color/status/info/bg` | `--color-status-info-bg` | COLOR | → `--color-status-info-50` | FRAME_FILL, SHAPE_FILL | Fondo de mensaje de info |
| `color/status/info/text` | `--color-status-info-text` | COLOR | → `--color-status-info-900` | TEXT_FILL | Texto de info sobre su bg (≥6.6:1) |
| `color/status/info/icon` | `--color-status-info-icon` | COLOR | → `--color-status-info-700` | FRAME_FILL, SHAPE_FILL | Icono de info (≥4.7:1 sobre bg y page) |
| `color/status/info/border` | `--color-status-info-border` | COLOR | → `--color-status-info-700` | STROKE_COLOR | Borde de info (≥4.7:1) |

## Spacing

| Token | CSS | Tipo | Value | Scopes | Descripción |
|---|---|---|---|---|---|
| `space/quarter` | `--space-quarter` | FLOAT | `2px` | GAP | 2px. Sistema de 8 puntos (excepción hairline/micro) |
| `space/half` | `--space-half` | FLOAT | `4px` | GAP | 4px. Sistema de 8 puntos (excepción hairline/micro) |
| `space/1` | `--space-1` | FLOAT | `8px` | GAP | 8px. Sistema de 8 puntos |
| `space/2` | `--space-2` | FLOAT | `16px` | GAP | 16px. Sistema de 8 puntos |
| `space/3` | `--space-3` | FLOAT | `24px` | GAP | 24px. Sistema de 8 puntos |
| `space/4` | `--space-4` | FLOAT | `32px` | GAP | 32px. Sistema de 8 puntos |
| `space/5` | `--space-5` | FLOAT | `40px` | GAP | 40px. Sistema de 8 puntos |
| `space/6` | `--space-6` | FLOAT | `48px` | GAP | 48px. Sistema de 8 puntos |
| `space/7` | `--space-7` | FLOAT | `56px` | GAP | 56px. Sistema de 8 puntos |
| `space/8` | `--space-8` | FLOAT | `64px` | GAP | 64px. Sistema de 8 puntos |
| `space/9` | `--space-9` | FLOAT | `72px` | GAP | 72px. Sistema de 8 puntos |
| `space/10` | `--space-10` | FLOAT | `80px` | GAP | 80px. Sistema de 8 puntos |
| `space/12` | `--space-12` | FLOAT | `96px` | GAP | 96px. Sistema de 8 puntos |
| `space/14` | `--space-14` | FLOAT | `112px` | GAP | 112px. Sistema de 8 puntos |
| `radius/md` | `--radius-md` | FLOAT | `24px` | CORNER_RADIUS | Radio de cards, formularios y media |
| `radius/pill` | `--radius-pill` | FLOAT | `80px` | CORNER_RADIUS | Radio de botones y pills |
| `border/width/default` | `--border-width-default` | FLOAT | `4px` | STROKE_FLOAT | Grosor de borde (botón ghost, formularios) |

## Layout

| Token | CSS | Tipo | Desktop | Mobile | Scopes | Descripción |
|---|---|---|---|---|---|---|
| `layout/max-width` | `--layout-max-width` | FLOAT | `1400px` | `1400px` | WIDTH_HEIGHT | Ancho máximo de contenido |
| `layout/max-width-narrow` | `--layout-max-width-narrow` | FLOAT | `1200px` | `1200px` | WIDTH_HEIGHT | Ancho máximo estrecho |
| `layout/section-padding-y` | `--layout-section-padding-y` | FLOAT | `112px` | `40px` | GAP | Padding vertical de sección |
| `layout/section-padding-x` | `--layout-section-padding-x` | FLOAT | `64px` | `24px` | GAP | Padding horizontal de sección |
| `layout/gap` | `--layout-gap` | FLOAT | `24px` | `24px` | GAP | Gap por defecto entre cards |

## Typography

| Token | CSS | Tipo | Desktop | Mobile | Scopes | Descripción |
|---|---|---|---|---|---|---|
| `font/family/display` | `--font-family-display` | STRING | `Anton` | `Anton` | FONT_FAMILY | Display: titulares, kickers, botones, badges. Siempre mayúsculas |
| `font/family/body` | `--font-family-body` | STRING | `Archivo` | `Archivo` | FONT_FAMILY | Cuerpo, formularios, nav |
| `font/style/display` | `--font-style-display` | STRING | `Regular` | `Regular` | FONT_STYLE | Anton solo tiene Regular |
| `font/style/body` | `--font-style-body` | STRING | `Regular` | `Regular` | FONT_STYLE | Peso de cuerpo |
| `font/size/hero` | `--font-size-hero` | FLOAT | `128px` | `64px` | FONT_SIZE | Tamaño hero |
| `font/line-height/hero` | `--font-line-height-hero` | FLOAT | `120px` | `60px` | LINE_HEIGHT | Interlineado hero (0.94) |
| `font/size/h2` | `--font-size-h2` | FLOAT | `72px` | `44px` | FONT_SIZE | Tamaño h2 |
| `font/line-height/h2` | `--font-line-height-h2` | FLOAT | `68px` | `41px` | LINE_HEIGHT | Interlineado h2 (0.94) |
| `font/size/h3` | `--font-size-h3` | FLOAT | `44px` | `30px` | FONT_SIZE | Tamaño h3 |
| `font/line-height/h3` | `--font-line-height-h3` | FLOAT | `41px` | `28px` | LINE_HEIGHT | Interlineado h3 (0.94) |
| `font/size/lead` | `--font-size-lead` | FLOAT | `27px` | `20px` | FONT_SIZE | Tamaño lead |
| `font/line-height/lead` | `--font-line-height-lead` | FLOAT | `38px` | `28px` | LINE_HEIGHT | Interlineado lead (1.4) |
| `font/size/body` | `--font-size-body` | FLOAT | `24px` | `18px` | FONT_SIZE | Tamaño body |
| `font/line-height/body` | `--font-line-height-body` | FLOAT | `36px` | `27px` | LINE_HEIGHT | Interlineado body (1.5) |
| `font/size/kicker` | `--font-size-kicker` | FLOAT | `22px` | `22px` | FONT_SIZE | Tamaño kicker |
| `font/line-height/kicker` | `--font-line-height-kicker` | FLOAT | `22px` | `22px` | LINE_HEIGHT | Interlineado kicker (1.0) |

## Motion

| Token | CSS | Tipo | Value | Scopes | Descripción |
|---|---|---|---|---|---|
| `motion/duration/base` | `--motion-duration-base` | FLOAT | `500ms` | — | Duración base de transiciones (ms) |
| `motion/easing/punch` | `--motion-easing-punch` | STRING | `"cubic-bezier(.22,1.2,.36,1)"` | — | Easing con rebote para hovers y reveal |

## Foundations

| Familia | Estado | Tokens |
|---|---|---|
| Icon size (`--icon-size-*`) | ⬜ pendiente en Figma | icon/size/* |
| Layer (`--z-*`) | ⬜ pendiente en Figma | layer/* |
| Motion (`--motion-*`) | ✅ definida | motion/* |
| Elevation (`--elevation-*`) | ⬜ pendiente en Figma (effect styles) o «sin elevación» declarado | effect styles elevation/* |

## Text styles

| Estilo | CSS | Familia | Peso/estilo | Tamaño | Interlineado | Tracking |
|---|---|---|---|---|---|---|
| Hero | `--font-hero-*` | Anton | Regular | 128 | {"unit": "PIXELS", "value": 120} | {"unit": "PERCENT", "value": 0} |
| H2 | `--font-h2-*` | Anton | Regular | 72 | {"unit": "PIXELS", "value": 68} | {"unit": "PERCENT", "value": 0} |
| H3 | `--font-h3-*` | Anton | Regular | 44 | {"unit": "PIXELS", "value": 41} | {"unit": "PERCENT", "value": 0} |
| Lead | `--font-lead-*` | Archivo | Regular | 27 | {"unit": "PIXELS", "value": 38} | {"unit": "PERCENT", "value": 0} |
| Body | `--font-body-*` | Archivo | Regular | 24 | {"unit": "PIXELS", "value": 36} | {"unit": "PERCENT", "value": 0} |
| Kicker | `--font-kicker-*` | Anton | Regular | 22 | {"unit": "PIXELS", "value": 22} | {"unit": "PERCENT", "value": 0} |
