# GB Noodles · Microsites · Design System — Índice, reglas y sync

> **Router** del sistema de diseño. Corto a propósito: se lee siempre y decide **qué otro
> archivo abrir**. No copies aquí el contenido de los demás.

**Fuentes de verdad en Figma:**

- **DS - Noodles** — design-system: variables, estilos y componentes de los microsites (fuente de verdad del DS) · fileKey `v4mnn154qUmiB35CCnRfgh`
- **GB Noodles · IA & page structure** — FigJam de sitemap y blueprints; no es fuente del DS · fileKey `cRgmGl36ELIUZNLUvC8KbW`
- **Wireframes | Rediseño sites** — wireframes; sus componentes locales son solo de wireframe, no del DS · fileKey `1YhsCqdqYCHlK4Y82IY5G3`
- **Noodles - sites** — pantallas (UI) de los microsites; consumen el DS, no son fuente del DS · fileKey `NfjwW15h6leh1MbJp0lYQO`

**Modo de adopción:** `new`

**Arquitectura y nomenclatura vigentes:**

DS nuevo (`new`): todavía no existe librería de variables ni de componentes en Figma. Se construirá según el estándar de la skill, sembrado con los valores probados en las landings de la Fase 1 (traspaso-microsites §9). Cada marca redefine sus colores de marca con los mismos nombres de token; los componentes no cambian.

Las fuentes pueden estar repartidas entre varios archivos. Para cada sync, identifica
qué fuente gobierna el artefacto que se va a regenerar; no asumas un fileKey único.
Modelo **B (Figma manda + artefactos generados)**: los `.md`/`.json`/`.css` de tokens y los
contratos de componentes **no se editan a mano** — se **generan** desde Figma con el sync.
Tú editas Figma; aquí solo se refleja.

---

## Enrutado — qué archivo leer según la petición

| Si la petición trata de… | Lee | No leas el resto |
|---|---|---|
| **diseñar sin Figma** (modo repo) o **sacar el DS de los prototipos de `UI/`** | `design-system/source/README.md` y `guides/sin-figma.md` | Figma, salvo para el plan de paso (`--figma-plan`) |
| color, tipografía, espaciado, radios, **valor de estilo** | `docs/tokens.md` (personas) · `tokens/tokens.json` (máquinas) · `tokens/tokens.css` (código) | components / patterns |
| un **átomo**: button, input, badge, checkbox, icon… | `docs/components.md` (solo el índice) → la ficha `docs/components/<slug>.md` (+ su realización en `css/components.css`) | patterns y el resto de fichas |
| algo **compuesto**: card, form, modal, navbar, table… | `docs/patterns.md` (índice + secciones manuales) → la ficha `docs/patterns/<slug>.md` | el resto de fichas (respeta los átomos que use: abre solo sus fichas) |
| **dirección visual**: tono, paleta o tipografía como intención, «cómo debería verse» | `../UX/direction/DESIGN.md` (se lee antes de crear tokens o proponer estilo; los valores nacen en Figma) | — |
| empezar pantalla/proyecto nuevo | `../UX/direction/DESIGN.md` + este archivo + `tokens/tokens.css` + `docs/patterns.md § Composición de pantalla` | components/patterns bajo demanda |
| **colocar componentes en una pantalla**: espaciado entre secciones, anchos, grid, breakpoints, paneles, capas | `docs/patterns.md § Composición de pantalla` | — |
| sombra, z-index, duración o easing, tamaño de icono | `docs/tokens.md` §§ Icon size · Layer · Motion · Elevation (son tokens; nunca valores sueltos) | — |
| **ver el DS entero**, componente a componente, con vista previa y estado de verificación | `../library/` (`cd library && npm start`; lo genera `scripts/ds-library.py` desde este design system) | — |
| una **imagen** en un «Ejemplo de código» | `assets/images/placeholder.svg` (las fotos reales son de las pantallas, en `UI/`; los iconos, con su ruta real `../assets/icons/<nombre>.svg`) | — |
| un **icono o fuente** del DS para una pantalla | `assets/icons/` · `assets/fonts/` (exportados de Figma) + `docs/assets.md` | — |
| **ver el DS montado** (catálogo visual, tema claro/oscuro) | `showcase/index.html` (⚙️ generado por el sync; no se edita a mano) | — |
| **añadir un archivo nuevo al DS** | sección **Estructura** abajo: solo dentro de la carpeta de su naturaleza; nunca en raíz | — |
| **comprobar que no hay valores crudos** antes de un commit | `python3 scripts/token-audit.py` (cero errores) | — |
| **vas a escribir en Figma**: crear o tocar variables, componentes o pantallas | [`figma.md`](./figma.md) — procedimiento, reglas de la API y rendimiento | el resto, hasta saber qué vas a construir |
| "el token X cambió en Figma" / sincronizar | `guides/sync-figma.md` | — |
| **eres una IA y quieres el DS como datos estructurados** | `agent-manifest.json` y solo los recursos que este enrute | no cargues todo el DS |
| **acabas de crear o modificar un componente en Figma** | paso 3 de `guides/sync-figma.md` (script de componentes) → regenera su `schemas/components/<slug>.schema.json`, `index.json` y `relationships.json` en esta misma sesión | — |
| saber si un componente **lleva icono** y cuál por defecto | `schemas/components/<slug>.schema.json` → `api.icons` y `api.props` (`type: icon`) | — |
| saber **cuándo usar** un componente, qué **no hace** o su **accesibilidad** | la ficha que indica `docs` de su schema (`docs/components/<slug>.md` o `docs/patterns/<slug>.md`, sección `<Nombre>`) | el schema no lo repite: este criterio vive solo en el `.md` |
| **vas a usar un componente en una pantalla por primera vez** | `meta.verification` de su schema; si no es `verified`, `guides/verificacion.md` antes de montar nada | — |
| validar una implementación o detectar drift | `schemas/governance/policies.json` + `schemas/governance/constraints.json` + `reports/drift-report.json` | — |
| **auditar la calidad del DS en Figma** (capas, estilos, componentes, nomenclatura) | `guides/auditoria-figma.md` · `reports/audit-report.json` | — |
| saber qué puede hacer un agente y qué requiere aprobación | `schemas/governance/capabilities.json` | — |
| **probar un cambio del DS que aún no está en Figma** en una pantalla | `../UI/overrides/<id>.css`, con `<id>` el de su propuesta en `proposals/`, enlazado solo desde las pantallas donde se prueba; `token-audit` avisa mientras la propuesta esté pendiente y da error cuando sobra (ver `guides/overrides.md`) | nunca `css/components.css` ni un `<style>` en la página |
| **redactar la accesibilidad** de componentes (rol, nombre, estados, teclado) o cambiar cualquier texto de una ficha | `guides/accesibilidad.md` · `python3 scripts/ds-text-proposal.py` (nunca se escribe el texto: se propone) | — |
| proponer un cambio al DS | `proposals/README.md` + `proposals/_proposal.schema.json`. Cada propuesta vive en la carpeta de su estado (raíz = pendiente, `aplicadas/`, `rechazadas/`); al crearla o cambiarle el estado, `python3 scripts/proposals-index.py` la coloca y regenera el índice del README | no apliques el cambio sin su aprobación requerida |
| **el usuario ha corregido lo mismo dos veces** (estilo, componente, layout) | `docs/patterns.md § Decisiones recurrentes` → añade la fila en esta sesión | — |
| saber si algo **ya se decidió** antes de proponer un cambio visual | `docs/patterns.md § Decisiones recurrentes` | — |

> Carga solo el archivo que la tarea necesita: el índice (`components.md` / `patterns.md`) y las
> fichas de los componentes que vas a usar, no la carpeta entera. Si un patrón usa un átomo, abre
> también la ficha del átomo. Para máquinas, `agent-manifest.json` es el único punto de entrada:
> resuelve rutas y devuelve solo el fragmento necesario. Los `.md` y JSON son espejos
> complementarios del mismo DS y se sincronizan juntos.

---

## Reglas duras (no negociables)

> **Alcance:** estas reglas rigen la capa **UI / DS** — `UI/*.html`, los componentes y
> `design-system/*`. Los **wireframes de UX** (`UX/wireframes/*`) están **fuera**: usan su
> propio kit de paleta `--wf-*` (documentado en `UX/wireframes/AGENTS.md`), porque en fase
> UX la fuente de verdad es el HTML y aún no se exigen los tokens del DS.

1. **Nunca valores crudos** (`#hex`, `rgb()`, `font-size` literal, `px` sueltos, duraciones,
   `z-index`, sombras) en componentes y pantallas de **UI**: siempre `var(--token)` de `tokens.css`.
   Única excepción: la capa `:root` de `tokens.css`, que es salida del sync. **Lo hace cumplir
   `scripts/token-audit.py`** (error con el token sugerido; antes de cada commit y en CI, cero
   errores). Las únicas excepciones admitidas están en su config (hairlines ≤ 2 px en bordes y
   offsets, utilidades de accesibilidad como `.visually-hidden`); cualquier otra se anota aquí con su motivo.
1b. **Cero estilos locales, ni siquiera layout.** Prohibido `<style>` de página o estilo inline en
   `UI/*.html`. Todo estilo vive en `tokens/tokens.css` y `css/components.css` y se documenta en su `.md`;
   también el layout (grids, anchos, utilidades), con medidas de la colección `Layout` (`--layout-*`).
   Las pantallas son solo markup y clases del DS. **Única excepción: el chrome del showcase**
   (`showcase/index.html`), en un bloque `<style data-showcase-chrome>` con namespace: todo selector
   lleva `.sc-*`, solo declara `--sc-*`, nunca estiliza clases del DS ni redefine tokens, y sus demos
   usan clases y tokens reales. La auditoría vigila que no salga de su namespace.
2. **Figma manda** (en modo repo, `design-system/source/`). Si un valor no existe como token, no lo inventes: se añade en la
   fuente y se corre el sync. Nunca se edita `tokens.*` a mano.
3. **Consume semánticos, no primitivos.** En componentes usa `--text-default`,
   `--surface-default`, `--action-primary-fill`… no `--neutral-900` directo. Los
   semánticos ya resuelven claro/oscuro.
4. **No inventar componentes** fuera de `components.md` / `patterns.md`: primero el contrato.
5. **Composición sobre creación.** Los patrones se construyen a partir de los átomos;
   ninguna capa redefine la de arriba.
6. **Tema oscuro gratis.** No hardcodees colores por tema: usa semánticos y el modo se
   activa con `:root[data-theme="dark"]`.
7. **Colores opacos, sin transparencias.** Todo color visible (texto, icono, borde, fondo, relleno)
   es plano y opaco y viene de un token semántico. Prohibido `rgba()`/`hsla()` con alfa menor que 1,
   hex de 8 dígitos y `opacity` sobre texto o iconos: un gris sobre negro es un token gris, no blanco
   al 60 %. Motivo: el color resultante depende de lo que haya debajo y su contraste AA no se puede
   verificar. Excepciones, translúcidas por naturaleza: sombras (`--elevation-*`) y scrims u overlays
   (`--overlay-*`, `--scrim-*`, `--backdrop-*`). **La auditoría lo comprueba** en `tokens.css`. Los
   **degradados** se permiten si la marca los exige y la dirección visual
   (`UX/direction/DESIGN.md § Paleta`) lo declara: cada parada es un token semántico opaco, documentado
   en `docs/tokens.md`; nunca un recurso decorativo improvisado en una pantalla.
8. **Accesibilidad AA obligatoria — analizar antes de definir.** Todo par texto/fondo debe
   cumplir **WCAG 2.1 AA** en Light **y** Dark antes de aprobarse: texto normal ≥ 4.5:1,
   texto grande ≥ 3:1, elementos de interfaz y foco ≥ 3:1. El análisis de contraste es
   parte del diseño del token, no un paso posterior; en el contrato de cada componente
   debe constar qué pares se han verificado.
8b. **Accesibilidad no es solo contraste.** Un lector de pantalla no navega por color. Todo
   componente declara en su contrato su rol, de dónde sale su nombre accesible, qué se anuncia al
   cambiar de estado, qué teclas lo operan, dónde entra y sale el foco y qué partes son decorativas.
   Un icono sin texto necesita nombre explícito, y un estado que solo se distingue por color no
   existe para quien no ve. Si no se puede usar sin ratón, no está terminado.

8c. **Las variantes son la lógica; los slots, el contenido.** Si el archivo soporta slots, se usan
   para el contenido variable y nunca para sustituir variantes (tamaño, jerarquía y estado). Un slot
   lleva contenido por defecto e instancias preferidas declaradas. Si no hay slots, se declara en el
   contrato y se compone con instancias anidadas.

9. **Elevación, capas, motion y tamaños de icono son tokens.** Ninguna sombra, `z-index`,
   duración, easing ni `width/height` de icono se escribe como valor: nacen en Figma
   (variables `icon/size/*`, `layer/*`, `motion/*` y effect styles de elevación), se
   sincronizan a `tokens.css` (`--icon-size-*`, `--z-*`, `--motion-*`, `--elevation-*`) y
   solo entonces se consumen. Si el DS aún no define una familia, el componente no la usa
   hasta que exista; la auditoría lo avisa.
10. **Composición documentada antes que compuesta.** Las pantallas se montan siguiendo las
   reglas de `patterns.md § Composición de pantalla` (ritmo entre secciones, anchos,
   grid y breakpoints, paneles, capas). Una regla de layout que no está escrita no se
   aplica: primero se documenta allí, con sus medidas como tokens, y luego se usa.
11. **Todo contrato lleva ejemplo de código.** Cada ficha (`docs/components/<slug>.md`,
   `docs/patterns/<slug>.md`) incluye un snippet HTML mínimo con las clases reales de
   `css/components.css`; las pantallas y el agente lo copian, no reinventan el markup, y el showcase
   lo renderiza tal cual. La raíz del ejemplo lleva `data-ds="<slug>"`, la marca que sigue el hilo
   pantalla → contrato → maestro.
12. **Estructura cerrada.** `design-system/` tiene una carpeta por naturaleza (ver
   **Estructura** más abajo) y en su raíz solo `design.md` y `agent-manifest.json`. Nada se
   crea fuera de esa lista: ni `img/`, ni `fonts/`, ni un segundo CSS, ni docs sueltos. Los
   iconos exportados viven en `assets/icons/`, las fuentes en `assets/fonts/` y se documentan
   en `docs/assets.md`. `scripts/token-audit.py` falla si aparece una entrada no prevista.
13. **Las correcciones repetidas se escriben.** Si el usuario corrige lo mismo dos veces, es una
   regla: se registra en `docs/patterns.md § Decisiones recurrentes` en esa sesión, con fecha y
   origen. Si implica una medida o un color nace como token; si afecta a un componente, se promueve
   a su contrato. Lo registrado es normativo y no se vuelve a preguntar.
14. **Ningún componente se usa en una pantalla sin verificar contra su maestro.** El sync trae la
   estructura; el CSS, el ejemplo y el criterio los escriben personas. Cada contrato declara en
   `meta.verification` si se comparó con su maestro (`verified`), nunca (`unverified`, por defecto) o
   si el maestro cambió después (`stale`). La primera vez que una pantalla usa un componente
   `unverified` o `stale` se pasa el protocolo de **Verificación contra el maestro** antes de montarla.
   `scripts/ds-fidelity.py` lo recuerda y cruza contrato, CSS y ejemplo con lo comprobable sin abrir Figma.

### Reglas duras en Figma

Solo con Figma: qué debe cumplirse al escribir variables y componentes en el canvas está en
[`guides/reglas-figma.md`](./guides/reglas-figma.md), y el cómo en [`figma.md`](./figma.md). Se leen antes de
escribir nada en Figma, no para el resto del trabajo.

## Guías (se leen solo cuando la tarea lo pide)

| Guía | Léela cuando |
|---|---|
| [`guides/sync-figma.md`](./guides/sync-figma.md) | sincronizas desde Figma, o creas o modificas un componente en Figma (protocolo de sync por MCP) |
| [`guides/reglas-figma.md`](./guides/reglas-figma.md) | vas a escribir variables o componentes en Figma |
| [`guides/auditoria-figma.md`](./guides/auditoria-figma.md) | auditas la calidad del DS en Figma |
| [`guides/verificacion.md`](./guides/verificacion.md) | vas a usar en una pantalla un componente que no está `verified` |
| [`guides/accesibilidad.md`](./guides/accesibilidad.md) | redactas accesibilidad o cambias un texto de una ficha |
| [`guides/overrides.md`](./guides/overrides.md) | pruebas en una pantalla un cambio del DS que aún no está aprobado |
| [`guides/sin-figma.md`](./guides/sin-figma.md) | el proyecto diseña sin Figma (modo repo) o saca el DS de los prototipos de `UI/` |

Con `sourceMode: repo` no se leen las guías de Figma. `python3 scripts/ds-budget.py` mide cuánto cuesta leer el proyecto.

## Estructura

```
design-system/
├── design.md            ← este archivo: router + reglas duras (se edita a mano)
├── agent-manifest.json  ← entrada única para máquinas
├── docs/                ← para personas: tokens.md · assets.md · components.md y patterns.md (índice + secciones manuales) · components/<slug>.md y patterns/<slug>.md (una ficha por contrato; _plantilla.md es la forma de una ficha nueva)
├── tokens/              ← ⚙️ GENERADO: tokens.json (máquinas) · tokens.css (código, incl. tema oscuro)
├── css/                 ← components.css — único CSS del DS (átomos + patrones + capa de pantalla)
├── assets/              ← ⚙️ exportado de Figma: icons/ · fonts/ · images/ (placeholder para las fotos de los ejemplos)
├── schemas/             ← para IA: _component.schema.json · index.json · relationships.json · governance/ · components/<slug>.schema.json
├── reports/             ← ⚙️ drift-report · audit-report · token-audit
├── proposals/           ← propuestas sujetas a revisión humana: pendientes en la raíz · aplicadas/ · rechazadas/ (las coloca scripts/proposals-index.py, que regenera el índice del README)
├── sync/                ← volcados de Figma leídos por MCP (variables.json · components.json · icons.json): entrada de ds-sync.py
├── guides/              ← guías por tema que se leen solo cuando la tarea lo pide: sync-figma · reglas-figma · auditoria-figma · verificacion · accesibilidad · overrides · sin-figma
└── showcase/index.html  ← ⚙️ catálogo visual navegable
```

**Estructura cerrada.** En la raíz de `design-system/` solo viven `design.md` y
`agent-manifest.json`; todo archivo nuevo va dentro de la carpeta de su naturaleza (un doc →
`docs/`, un svg → `assets/icons/`, un CSS → se integra en `css/components.css`, un contrato →
`schemas/components/`, un volcado de Figma → `sync/`). No se crean carpetas nuevas ni archivos sueltos: `scripts/token-audit.py`
marca como error cualquier entrada fuera de esta lista.

## Estado (2026-10-07 — proyecto recién creado)

- ⬜ Tokens: pendiente de definir en Figma y correr el primer sync.
- ⬜ Componentes: catálogo por definir según necesidades del proyecto.
- ℹ️ Madurez inicial: nivel 1; objetivo nivel 2 tras el primer sync verificado.
