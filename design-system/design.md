# GB Noodles · Microsites · Design System — Índice, reglas y sync

> **Router** del sistema de diseño. Corto a propósito: se lee siempre y decide **qué otro
> archivo abrir**. No copies aquí el contenido de los demás.

**Fuentes de verdad en Figma:**

- **GB Noodles · IA & page structure** — ia-sitemap (FigJam: sitemap y blueprints por página) · fileKey `cRgmGl36ELIUZNLUvC8KbW`
- **Wireframes | Rediseño sites** — wireframes (home mobile alta fidelidad + blueprints desktop; home desktop en 87:642) · fileKey `1YhsCqdqYCHlK4Y82IY5G3`
- ⬜ TODO — librería del DS (variables y componentes): aún no existe.

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
| color, tipografía, espaciado, radios, **valor de estilo** | `docs/tokens.md` (personas) · `tokens/tokens.json` (máquinas) · `tokens/tokens.css` (código) | components / patterns |
| un **átomo**: button, input, badge, checkbox, icon… | `docs/components.md` (solo el índice) → la ficha `docs/components/<slug>.md` (+ su realización en `css/components.css`) | patterns y el resto de fichas |
| algo **compuesto**: card, form, modal, navbar, table… | `docs/patterns.md` (índice + secciones manuales) → la ficha `docs/patterns/<slug>.md` | el resto de fichas (respeta los átomos que use: abre solo sus fichas) |
| **dirección visual**: tono, paleta o tipografía como intención, «cómo debería verse» | `../UX/direction/DESIGN.md` (se lee antes de crear tokens o proponer estilo; los valores nacen en Figma) | — |
| empezar pantalla/proyecto nuevo | `../UX/direction/DESIGN.md` + este archivo + `tokens/tokens.css` + `docs/patterns.md § Composición de pantalla` | components/patterns bajo demanda |
| **colocar componentes en una pantalla**: espaciado entre secciones, anchos, grid, breakpoints, paneles, capas | `docs/patterns.md § Composición de pantalla` | — |
| sombra, z-index, duración o easing, tamaño de icono | `docs/tokens.md` §§ Icon size · Layer · Motion · Elevation (son tokens; nunca valores sueltos) | — |
| un **icono o fuente** del DS para una pantalla | `assets/icons/` · `assets/fonts/` (exportados de Figma) + `docs/assets.md` | — |
| **ver el DS montado** (catálogo visual, tema claro/oscuro) | `showcase/index.html` (⚙️ generado por el sync; no se edita a mano) | — |
| **añadir un archivo nuevo al DS** | sección **Estructura** abajo: solo dentro de la carpeta de su naturaleza; nunca en raíz | — |
| **comprobar que no hay valores crudos** antes de un commit | `python3 scripts/token-audit.py` (cero errores) | — |
| **vas a escribir en Figma**: crear o tocar variables, componentes o pantallas | [`figma.md`](./figma.md) — procedimiento, reglas de la API y rendimiento | el resto, hasta saber qué vas a construir |
| "el token X cambió en Figma" / sincronizar | sección **Sync desde Figma** abajo | — |
| **eres una IA y quieres el DS como datos estructurados** | `agent-manifest.json` y solo los recursos que este enrute | no cargues todo el DS |
| **acabas de crear o modificar un componente en Figma** | paso 3 de **Sync desde Figma** (script de componentes) → regenera su `schemas/components/<slug>.schema.json`, `index.json` y `relationships.json` en esta misma sesión | — |
| saber si un componente **lleva icono** y cuál por defecto | `schemas/components/<slug>.schema.json` → `api.icons` y `api.properties` (`kind: INSTANCE_SWAP`) | — |
| saber **cuándo usar** un componente, qué **no hace** o su **accesibilidad** | la ficha que indica `source.docs` de su schema (`docs/components/<slug>.md` o `docs/patterns/<slug>.md`, sección `<Nombre>`) | el schema no lo repite: este criterio vive solo en el `.md` |
| **vas a usar un componente en una pantalla por primera vez** | `meta.verification` de su schema; si no es `verified`, sección **Verificación contra el maestro** (abajo) antes de montar nada | — |
| validar una implementación o detectar drift | `schemas/governance/policies.json` + `schemas/governance/constraints.json` + `reports/drift-report.json` | — |
| **auditar la calidad del DS en Figma** (capas, estilos, componentes, nomenclatura) | sección **Auditoría del DS en Figma** abajo · `reports/audit-report.json` | — |
| saber qué puede hacer un agente y qué requiere aprobación | `schemas/governance/capabilities.json` | — |
| proponer un cambio al DS | `proposals/_proposal.schema.json` | no apliques el cambio sin su aprobación requerida |
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
   `z-index` numéricos, sombras) en componentes y pantallas de **UI**. Siempre `var(--token)`
   de `tokens.css`. Única excepción: la capa `:root` de `tokens.css` (que es output del
   sync). **La regla se hace cumplir con `scripts/token-audit.py`**, que devuelve error si
   encuentra un valor crudo y sugiere el token: se ejecuta antes de cada commit y en CI, y
   exige cero errores. Las únicas excepciones admitidas están en su config (hairlines
   ≤ 2 px en bordes y offsets, utilidades de accesibilidad como `.visually-hidden`) y
   cualquier otra debe anotarse aquí con su motivo.
1b. **Cero estilos locales — ni siquiera layout.** Prohibido cualquier `<style>` de página
   o estilo inline en `UI/*.html`. Todo estilo vive en `tokens/tokens.css` /
   `css/components.css` y se documenta en su `.md`. Incluye el layout de pantalla: grids,
   anchos y utilidades se definen como clases documentadas en `css/components.css`; las
   dimensiones estructurales salen de la colección `Layout` de Figma (→ `--layout-*`). Las
   pantallas son solo markup + clases del DS. **Única excepción: el chrome del showcase**
   (`showcase/index.html`), que es agnóstico del cliente y vive en un bloque
   `<style data-showcase-chrome>` cerrado por namespace: todo selector incluye `.sc-*`, solo
   declara custom properties `--sc-*`, nunca estiliza clases del DS ni redefine tokens, y las
   demos que contiene usan exclusivamente clases y tokens reales. Los valores crudos del
   chrome están permitidos porque no forman parte del DS; la auditoría vigila que no salga
   de su namespace.
2. **Figma manda.** Si un valor no existe como token, no lo inventes: se añade en
   **Figma** y se corre el sync. Nunca se edita `tokens.*` a mano.
3. **Consume semánticos, no primitivos.** En componentes usa `--text-default`,
   `--surface-default`, `--action-primary-fill`… no `--neutral-900` directo. Los
   semánticos ya resuelven claro/oscuro.
4. **No inventar componentes** fuera de `components.md` / `patterns.md`: primero el contrato.
5. **Composición sobre creación.** Los patrones se construyen a partir de los átomos;
   ninguna capa redefine la de arriba.
6. **Tema oscuro gratis.** No hardcodees colores por tema: usa semánticos y el modo se
   activa con `:root[data-theme="dark"]`.
7. **Colores opacos, sin transparencias.** Todo color que se ve (texto, icono, borde, fondo,
   relleno) es un color **plano y opaco** que viene de un token semántico. Prohibido resolver
   un tono con transparencia sobre otro fondo: nada de `rgba()`/`hsla()` con alfa menor que 1,
   hex de 8 dígitos ni `opacity` sobre texto o iconos. Un gris sobre negro es un token gris
   definido en Figma, no blanco al 60 %. Motivo: el color resultante depende de lo que haya
   debajo, cambia al mover el elemento y su contraste AA no se puede verificar. Únicas
   excepciones, por naturaleza translúcidas: sombras (`--elevation-*`) y scrims u overlays de
   modales y paneles (`--overlay-*`, `--scrim-*`, `--backdrop-*`). **La auditoría lo
   comprueba** en `tokens.css`: un token de color con alfa fuera de esas familias es error.
   Los **degradados** no están prohibidos: se permiten cuando la marca los exige y la
   dirección visual (`UX/direction/DESIGN.md § Paleta`) lo declara. En ese caso nacen en Figma
   como estilo o variable, cada parada es un token semántico opaco y se documentan en
   `docs/tokens.md`. Nunca como recurso decorativo improvisado en una pantalla.
8. **Accesibilidad AA obligatoria — analizar antes de definir.** Todo par texto/fondo debe
   cumplir **WCAG 2.1 AA** en Light **y** Dark antes de aprobarse: texto normal ≥ 4.5:1,
   texto grande ≥ 3:1, elementos de interfaz y foco ≥ 3:1. El análisis de contraste es
   parte del diseño del token, no un paso posterior; en el contrato de cada componente
   debe constar qué pares se han verificado.
8b. **Accesibilidad no es solo contraste.** El contraste AA es condición necesaria y no
   suficiente: **un lector de pantalla no navega por color**. Todo componente declara en su
   contrato su rol, de dónde sale su nombre accesible, qué se anuncia al cambiar de estado, qué
   teclas lo operan, dónde entra y sale el foco y qué partes se ocultan por decorativas. Dos
   consecuencias que se incumplen siempre: **un icono sin texto necesita nombre explícito**, y
   **un estado que solo se distingue por color no existe** para quien no ve. Si el componente no
   se puede usar sin ratón, no está terminado.

8c. **Las variantes son la lógica; los slots, el contenido.** Cuando el archivo de Figma
   soporte slots nativos, se usan para el contenido variable y **nunca para sustituir variantes**.
   Las variantes siguen expresando tamaño, jerarquía y estado; el slot evita la explosión
   combinatoria de crear una variante por cada tipo de contenido. Un slot lleva contenido por
   defecto, para que el componente no se vea vacío, e instancias preferidas declaradas. Si el
   archivo no soporta slots, se declara así en el contrato y se compone con instancias anidadas.

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
11. **Todo contrato lleva ejemplo de código.** Cada ficha de
   `docs/components/<slug>.md` / `docs/patterns/<slug>.md` incluye un snippet HTML mínimo con las clases
   reales de `css/components.css`. Las pantallas y el agente copian ese ejemplo; no
   reinventan el markup. El showcase lo renderiza tal cual.
12. **Estructura cerrada.** `design-system/` tiene una carpeta por naturaleza (ver
   **Estructura** abajo) y en su raíz solo `design.md` y `agent-manifest.json`. Nada se
   crea fuera de esa lista: ni `img/`, ni `fonts/`, ni un segundo CSS, ni docs sueltos. Los
   iconos exportados viven en `assets/icons/`, las fuentes en `assets/fonts/` y se documentan
   en `docs/assets.md`. `scripts/token-audit.py` falla si aparece una entrada no prevista.
13. **Las correcciones repetidas se escriben.** Si el usuario corrige lo mismo dos veces
   (espaciado, color, variante, colocación…), es una regla: se registra en
   `docs/patterns.md § Decisiones recurrentes` en esa misma sesión, con fecha y origen. Si
   implica una medida o un color, nace como token en Figma y se sincroniza; si afecta a un
   componente, se promueve a su contrato. Lo registrado es normativo y no se vuelve a preguntar.
14. **Ningún componente se usa en una pantalla sin verificar contra su maestro.** El sync trae de
   Figma la estructura (variantes, propiedades, tokens ligados); el CSS, el ejemplo y el criterio los
   escriben personas, y nada garantiza que se escribieran con el maestro delante. Cada contrato
   declara en `meta.verification` si se ha comparado con su maestro (`verified`), nunca
   (`unverified`, el valor por defecto) o si el maestro cambió después (`stale`). La primera vez que
   una pantalla usa un componente `unverified` o `stale` se pasa el protocolo de **Verificación
   contra el maestro** (abajo) antes de montarla. `scripts/ds-fidelity.py` lo recuerda y además cruza
   contrato, CSS y ejemplo con lo que se puede comprobar sin abrir Figma.

### Reglas duras en Figma

> Estas reglas dicen **qué** debe cumplirse. El **cómo** —orden de trabajo, llamadas,
> errores de la API que fallan en silencio y troceado por rendimiento— está en
> [`figma.md`](./figma.md), y se lee antes de escribir nada en el canvas.


#### Protección de sistemas existentes

- Antes de escribir, determina el modo de adopción registrado arriba. Si es
  `preserve-existing` o `pending-inspection`, las reglas estructurales de esta sección
  son referencia para el análisis, no instrucciones de migración.
- En un DS existente y operativo no cambies colecciones, modos, jerarquías, aliases,
  nombres, estilos, keys ni estructura de componentes sin una decisión explícita de
  reestructuración y un plan de migración aprobado.
- En modo `preserve-existing`, todos los documentos y artefactos generados reflejan la
  metodología y nomenclatura reales del DS. Las nuevas variables y componentes siguen
  esas convenciones para no crear dos arquitecturas dentro de la misma librería.
- Presenta las diferencias con este estándar como hallazgos, no como errores que deban
  corregirse automáticamente.
- Completar scopes y descripciones de variables sigue siendo obligatorio en cualquier
  modo, siempre que no cambie identidad, valor, alias, colección, modo ni key.

#### Arquitectura de variables de color

- Para un DS nuevo o una reestructuración aprobada usa tres niveles:
  **`Primitive` → `Semantic` → `Components`**. No impongas esta arquitectura sobre un
  DS existente que el usuario haya decidido conservar.
- `Primitive` contiene valores base y nunca se consume directamente en componentes,
  patterns ni pantallas. Sus variables de color llevan `scopes: []` y se ocultan para
  publicación cuando la API lo permita. Solo `Semantic` puede referenciarlas.
- `Semantic` expresa intención y debe incluir como mínimo familias para `alert`,
  `success`, `error` e `info`, con los roles de fondo, texto, icono y borde que requiera
  cada estado. Todos los pares deben cumplir WCAG AA en cada modo.
- El diseñador decide cuántas familias de marca necesita: puede definir `primary`,
  `secondary` u otras. No fuerces un número cerrado.
- Las variables de `Components` solo se crean al construir componentes estructurales
  del catálogo del DS. **Nunca se crean variables específicas para patterns**: estos
  componen componentes y consumen semánticos o variables de los componentes existentes.
- Los aliases siguen siempre la cadena Components → Semantic → Primitive; no dupliques
  valores crudos entre niveles.

#### Scopes y descripciones

- Define en cada variable el scope compatible más estrecho con su uso real. Nunca dejes
  `ALL_SCOPES`. Usa, según corresponda, fill de frame/shape, text fill, stroke, gap,
  radius, width/height o los scopes tipográficos admitidos por Figma.
- Cada variable debe tener una descripción breve de su propósito, dónde se usa y, si
  resulta útil, dónde no debe usarse.
- En un DS existente, scope y descripción son mejoras de metadatos permitidas, pero se
  aplican por lotes revisables y sin alterar ninguna propiedad estructural.

#### Medidas y grids

- El sistema se basa en un **grid de 8 puntos**. Crea además los tamaños `2` y `4` para
  hairlines, microespaciado y ajustes que no puedan resolverse con 8. El resto de
  spacing, padding, gap y medidas discretas usa múltiplos de 8.
- El diseñador elige para cada breakpoint o pantalla el número de columnas, márgenes,
  gutter y ancho. Documenta la decisión y expresa esas medidas con el sistema de 8
  puntos; reserva 2 y 4 para las excepciones anteriores.

#### Nomenclatura

- Ninguna página, frame, grupo, capa, componente, variante, propiedad o variable puede
  quedar sin nombre ni conservar nombres genéricos como "Frame", "Group" o "Rectangle".
- En proyectos nuevos usa una convención común: variables jerárquicas separadas por `/`,
  frames y capas en kebab-case o BEM, componentes con el nombre del catálogo y variantes
  `Propiedad=Valor`. Mantén exactamente el mismo vocabulario, idioma y casing en todas
  las páginas.
- En archivos existentes, inspecciona primero sus convenciones. Si chocan con el estándar
  del equipo, audita y acuerda la migración antes de renombrar; no impongas cambios de
  nomenclatura silenciosamente.

#### Auto Layout y bindings

- Construye con Auto Layout todos los componentes, módulos, patterns, secciones y frames
  que representen páginas o pantallas. La obligación no aplica al nodo `PAGE` ni a
  primitivas gráficas sin estructura interna.
- Toda propiedad visual o estructural que Figma permita vincular debe tener una variable
  o estilo asociado: color, tipografía, spacing, gap, padding, radio, border/stroke,
  opacidad, ancho y altura.
- Solo una dimensión realmente líquida puede quedar sin variable de ancho o altura,
  según corresponda. Las propiedades que Figma no permita vincular y la geometría fija
  imprescindible deben quedar documentadas como excepciones técnicas.
- No uses valores locales como sustituto provisional. Si falta una variable o estilo,
  créalo, limita su scope y descríbelo antes de continuar.
- Los separadores se realizan como border del contenedor, no como líneas sueltas.
- Todo componente con icono lo expone como `INSTANCE_SWAP`, con un icono real de la
  galería como valor inicial; nunca uses un frame de color como sustituto.

#### Iconos, capas, motion y elevación

- **Tamaños de icono:** variables `FLOAT` `icon/size/<nombre>` en la colección
  `Components` (p. ej. `icon/size/sm`, `md`, `lg`, `xl`), en múltiplos de 4, scope
  `WIDTH_HEIGHT`, code syntax `var(--icon-size-<nombre>)`. Toda instancia de icono dentro
  de un componente liga su ancho y alto a una de ellas; en CSS los `.icon` solo usan
  `--icon-size-*`. Los iconos siguen exponiéndose como `INSTANCE_SWAP`.
- **Capas (z-index):** colección `Layer` con variables `FLOAT` `layer/<nombre>` (p. ej.
  `base`, `sticky`, `overlay`, `drawer`, `modal`, `toast`), valores enteros crecientes con
  hueco entre niveles, descripción de qué elemento vive en cada capa, code syntax
  `var(--z-<nombre>)`. Figma no aplica z-index, pero la escalera se define aquí para que
  el código la consuma y la documentación la muestre.
- **Motion:** colección `Motion` con duraciones `FLOAT` en ms (`motion/duration/<nombre>`,
  p. ej. `fast`, `base`, `slow`) y easings `STRING` (`motion/easing/<nombre>`, con la
  curva `cubic-bezier(...)` como valor). Code syntax `var(--motion-duration-<nombre>)` y
  `var(--motion-easing-<nombre>)`. Se aplican en prototipos de Figma cuando el editor lo
  permita y siempre en CSS.
- **Elevación:** Figma no admite variables de sombra, así que se define como **effect
  styles** `elevation/<nivel>` (p. ej. `0`, `1`, `2`, `3`) cuyos colores de sombra
  referencian variables semánticas. El sync los serializa a `--elevation-<nivel>` en
  `tokens.css`. Si el DS decide no usar sombras, se documenta explícitamente en
  `tokens.md` § Elevation («sin elevación: separación por borde + superficie») y la
  auditoría marcará como error cualquier `box-shadow`.
- Estas cuatro familias forman parte del **primer sync**: si faltan en Figma, el informe
  de drift las lista como `foundation-missing` y el catálogo de componentes no se da por
  completo hasta que existan o se declaren no aplicables.

#### Tipografía: puerta previa a componentes

- Antes de crear componentes o elementos visuales, comprueba que el diseñador ha definido
  familia, pesos, escala, line-height y comportamiento responsive.
- Si aún no existen estilos tipográficos, detén la creación visual y pide su definición.
  No inventes familias, estilos, escalas ni transformaciones responsive.
- El diseñador debe proporcionar las escalas Desktop y Mobile o una regla explícita para
  derivar una de otra. Cuando exista esa definición, crea automáticamente ambos grupos
  de estilos.
- Vincula a variables todas las propiedades tipográficas que Figma permita asociar y
  verifica los nombres reales de familia y estilo antes de crearlos.

#### Documentación de tokens

- Al generar o sincronizar la documentación Markdown, regenera en la misma operación
  `tokens.md`, `tokens.json` y `tokens.css`. Son tres espejos del mismo estado de Figma,
  comparten fuentes y fecha de sync y no se editan a mano.
- `tokens.json` conserva colecciones, modos, aliases, scopes y descripciones, incluida la
  jerarquía Primitive → Semantic → Components. `tokens.css` es la salida consumible por
  código; componentes y pantallas solo consumen tokens semánticos o de componente.
- Revisa conjuntamente el diff de los tres artefactos en cada sincronización.

#### Gobierno agentic y confianza gradual

- Los agentes pueden **leer**, recuperar contexto acotado, generar propuestas y ejecutar
  auditorías sin aprobación. Pueden aplicar cambios mecánicos solo cuando la fuente de
  verdad y el resultado sean deterministas y la política los marque como automáticos.
- Crear o cambiar tokens, componentes, contratos o primitivas requiere revisión humana.
  Publicar una librería de Figma requiere siempre aprobación explícita.
- Un agente nunca convierte una propuesta en cambio aprobado por sí mismo. Cada propuesta
  registra evidencia, impacto, aprobador requerido y estado.
- El scaffolding nace en **nivel 1** y tiene como objetivo alcanzar **nivel 2
  machine-readable** tras el primer sync verificado. Los archivos locales permiten
  recuperar contexto acotado sin exigir un servidor MCP personalizado del DS.

#### Integración con Figma y portabilidad

- El **MCP oficial (nativo) de Figma es la única vía tanto de extracción como de
  escritura** en Figma; está contemplado desde el inicio. Úsalo para inspeccionar
  fuentes, crear o actualizar variables y componentes, validar bindings y ejecutar la
  sincronización. Antes de cualquier operación contra Figma, comprueba que el MCP está
  conectado y configurado y que tiene acceso a las fuentes registradas arriba.
- El MCP no se usa solo en el primer sync: **mientras se trabaje sobre el DS**, es la vía
  para extraer de Figma la información que la tarea necesite y para **mantener
  actualizados los archivos del DS del proyecto** (`tokens.*`, contratos, `schemas/`,
  informes). Toda sesión de trabajo que cambie Figma termina ejecutando el protocolo de
  sync para que los artefactos locales reflejen el estado real.
- **La extracción es incremental por norma.** No se ofrece ni se ejecuta un volcado completo
  del DS en una sola tanda: se trocea por archivo y, cuando el archivo es grande, por página,
  empezando siempre por el que contiene variables y estilos. El coste en tokens de una lectura
  masiva es lo que impide terminar el sync, así que el troceado no es una preferencia del
  usuario sino parte del protocolo.
- El usuario puede pedir a la IA **crear componentes en Figma desde fuera de Figma**
  (desde la conversación o el código), usando el DS existente: sus tokens, estilos,
  convenciones y nomenclatura. Estas escrituras se ejecutan únicamente mediante el MCP
  oficial y conservan las aprobaciones de «Gobierno agentic y confianza gradual»; nunca
  se materializan por otra vía.
- Antes de escribir en Figma, carga y respeta las instrucciones oficiales de la
  integración Figma disponible en el entorno. Las operaciones que cambien tokens,
  componentes, contratos o la publicación de una librería conservan las aprobaciones
  definidas en este documento.
- `agent-manifest.json`, `tokens.json`, los contratos de `schemas/` y los informes son el
  **espejo local estructurado** del DS y el contexto portable para cualquier LLM. No
  reemplazan a Figma ni al MCP de Figma; permiten consultar el DS sin cargar toda la
  documentación y trabajar con sus artefactos locales.
- Un **MCP personalizado del DS no es necesario** para este flujo y esta skill no lo
  crea, configura ni exige. En el futuro podría añadirse como capa opcional para servir
  los mismos archivos locales a múltiples herramientas, pero no forma parte del
  scaffolding, del sync ni de los criterios de madurez.
- Si el LLM o herramienta actual no dispone del MCP oficial de Figma, no simules la
  conexión ni generes contenido supuestamente leído de Figma. Deja el primer sync
  pendiente e indica que debe ejecutarse desde un entorno que sí tenga esa integración.
- No conectes ni propongas servicios externos que el usuario no haya solicitado
  explícitamente. La arquitectura debe funcionar con Figma y los archivos locales.

---

## Verificación contra el maestro  ✅  (antes de usar un componente en una pantalla)

Lo que el sync trae de Figma es la estructura del componente. El CSS de sus clases, el «Ejemplo de
código» y el criterio de la ficha los escribe una persona o un agente, a menudo en bloque y sin abrir
el maestro, y las auditorías de forma no lo detectan: `token-audit` con cero errores solo dice que el
CSS usa variables, no que use *las* variables del maestro. Por eso cada contrato lleva un estado:

| `meta.verification.status` | Qué significa | Quién lo pone |
|---|---|---|
| ausente o `unverified` | Nadie ha comparado CSS, ejemplo y ficha con el maestro de Figma | valor por defecto |
| `verified` | Se comparó, variante a variante, y se corrigió lo que no cuadraba | quien verifica, al cerrar el protocolo |
| `stale` | Se verificó, pero el maestro cambió después (anatomía, variantes, tokens, key) o ya no existe | `ds-sync.py`, al detectar el cambio |

**Protocolo** (la primera vez que una pantalla usa un componente que no está `verified`):

1. **Leer el maestro por MCP**, variante a variante de las que la pantalla va a usar: layout y
   dirección, paddings y gaps, variables ligadas a cada propiedad, `textCase`, capas ocultas y
   propiedades de componente. Solo lectura. Lo que se lee se compara, no se transcribe de memoria.
2. **Comparar con el CSS** de las clases del contrato (`source.code.classes` en
   `css/components.css`): mismos tokens, mismos modificadores por variante, mismas medidas.
3. **Corregir el CSS** donde no cuadre. Un token distinto del que liga el maestro es un error, no
   una interpretación.
4. **Actualizar la ficha** (`docs/components/<slug>.md` o `docs/patterns/<slug>.md`): ejemplo con las
   clases reales y una muestra por variante comprobada; propósito y accesibilidad si faltan.
5. **Marcar `verified`** en el schema: `meta.verification = { "status": "verified", "date": "YYYY-MM-DD",
   "figmaVersion": <el meta.anatomyHash actual>, "variantsChecked": ["type=negative, state=default", …],
   "by": "<persona o agente>" }`. Relanzar `ds-sync.py` para que el ejemplo pase al schema.

`scripts/ds-fidelity.py` comprueba después lo que de esto se puede contrastar sin abrir Figma: tokens
que el maestro liga y el CSS no usa, variantes declaradas sin modificador CSS, clases del ejemplo que no
existen, imágenes externas en los ejemplos y pantallas que usan contratos sin verificar. Resume
cuántos contratos están en cada estado. Todo nace como aviso; el proyecto decide qué sube a error en
`scripts/ds-fidelity.config.json`.

Si un maestro desaparece de la librería (se borró o se republicó con otra key), el sync lo marca
`stale` con motivo «maestro no encontrado». Cómo reenlazar las instancias huérfanas en Figma está en
`figma.md § 6`.

## Sync desde Figma  ⚙️  (cómo se regeneran los artefactos)

**Cuándo:** cuando algo cambie en Figma (color, token nuevo, modo, componente) y, de
forma continua, **al cierre de cualquier sesión de trabajo sobre el DS** que haya tocado
Figma — la extracción vía MCP mantiene los archivos del DS del proyecto al día.
**No edites los archivos generados** — vuelve a generarlos y revisa el diff de git.

**Artefactos generados (no editar a mano):** `docs/tokens.md`, `tokens/tokens.json`,
`tokens/tokens.css`, la parte viva de cada ficha `docs/components/<slug>.md`/`docs/patterns/<slug>.md` y el
`## Índice` de `docs/components.md`/`docs/patterns.md`, los contratos
de `schemas/components/`, `assets/icons/` y `assets/fonts/`, `showcase/index.html` (secciones
`GENERATED`) y todo `reports/`. Llevan procedencia, versión y fecha del último sync. Los genera
`scripts/ds-sync.py` a partir de los volcados de `sync/` (ver `sync/README.md`); la única
escritura del agente es el volcado.

**Procedimiento (lo ejecuta cualquier LLM/agente con acceso al MCP oficial de Figma).**
Tiene dos mitades: **leer Figma** (solo el agente, por MCP, sin transformar nada) y **generar
los artefactos** (solo el script, determinista, sin leer Figma). La frontera es la carpeta
`sync/`: el agente vuelca ahí lo leído, el script parte de ahí. Mismo volcado → mismos
artefactos, con cualquier modelo.

1. **Comprobar el MCP.** Conectado, configurado y con acceso a las fuentes registradas; si no,
   detener el sync, informar y dejarlo pendiente. Consultar qué archivo gobierna tokens,
   componentes y patrones y leer solo los necesarios. Confirmar el modo de adopción: en
   `preserve-existing` no se transforma nada estructural.
1b. **Planificar la extracción por pasos.** Nunca se vuelca todo de una vez: se trocea para
   no agotar la sesión en tokens. El primer tramo es siempre **variables y estilos** y, si hay
   varias fuentes, se pregunta cuál las contiene y se empieza por ella. Después, **un archivo
   por tanda** en el orden variables y estilos → componentes → patrones → iconos; y si un
   archivo es grande, **una página por tanda**, listando antes las páginas y acordando cuáles
   quedan fuera. Entre tramo y tramo, un resumen de tres líneas y confirmación para seguir.
   **Cada lectura, además, va por trozos**: `use_figma` corta cada respuesta hacia los
   **20 KB** (`// truncated to 20kb`) y un DS mediano ya lo supera. Los dos scripts de lectura
   devuelven trozos de unos 14 KB y dicen dónde empieza el siguiente (`part.nextOffset`); se
   llaman en bucle hasta que sea `null`. **No pegues el JSON en el texto de la conversación ni
   lo resumas campo a campo: guárdalo en `sync/parts/` en la misma vuelta en que lo recibes,
   sin modificarlo.** La unión la hace el script, nunca el agente.
2. **Volcar variables y estilos → `sync/parts/variables-<NNN>.json`.** Ejecutar el script
   «lectura de variables y estilos» (abajo) sobre el archivo de tokens con `OFFSET = 0` y
   después con cada `part.nextOffset`, guardando cada respuesta tal cual. Si los tokens están
   repartidos en varios archivos, el mismo bucle en cada uno: cada trozo lleva su `fileKey`.
3. **Volcar componentes → `sync/parts/components-<NNN>.json`.** Ejecutar el script «lectura
   de componentes» (abajo) **una página por llamada** y, dentro de la página, por trozos igual
   que las variables, con `skipInvisibleInstanceChildren = false` (los iconos suelen estar
   ocultos por defecto). Todo `COMPONENT_SET` y todo `COMPONENT` suelto de las páginas leídas
   acaba en el volcado; ninguno se filtra a mano.
3b. **Unir y validar: `python3 scripts/ds-sync.py --merge`.** Une los trozos en
   `sync/variables.json` y `sync/components.json` por su posición (no por el nombre del
   archivo), los borra y valida el volcado: que ningún trozo llegó cortado, que no falta ni
   sobra ninguno, que no hay IDs repetidos y que todos los alias apuntan a una variable del
   volcado. Si algo falla no escribe nada y dice qué trozo volver a leer. `--check-dump` hace
   solo la validación. Un trozo con `OFFSET = 0` empieza de cero ese archivo o esa página, así
   que releer algo es volver a pedirlo desde 0. El resultado es idéntico al de una lectura
   de una sola pasada.
4. **Exportar iconos → `assets/icons/` + `sync/icons.json`.** Exportar como SVG, mediante el MCP,
   cada icono de la galería (`Icon / <nombre>` → `<nombre-kebab>.svg`) y registrar
   `{ "name", "nodeId", "file", "usage" }` en `sync/icons.json`. Fuentes necesarias →
   `assets/fonts/`. No existe ningún otro `img/` ni `fonts/` en el proyecto.
5. **Generar: `python3 scripts/ds-sync.py`.** A partir de `sync/` regenera, siempre igual:
   `docs/tokens.md`, `tokens/tokens.json`, `tokens/tokens.css` (primitivos, alias resueltos,
   modo Dark bajo `[data-theme="dark"]`, modos de dispositivo bajo `@media`, elevación desde
   effect styles y **tipografía desde text styles**: por estilo,
   `--font-<estilo>-{family,size,weight,line-height,letter-spacing}`, con `AUTO` → `normal` y
   el tracking en porcentaje → `em`. Un estilo con el breakpoint en el nombre («Desktop XL /
   H1», «Mobile / H1») sigue siendo un estilo aparte con sus variables: el CSS de componentes
   elige cuál usar en cada `@media`. Si Figma no da un nombre de familia válido para la web o
   no se deduce el peso, se declara en `fontFamilyMap` de `ds-sync.config.json`; no se adivina); un `schemas/components/<slug>.schema.json` por componente con propiedades
   completas, ejes de variante, instancias anidadas incluidas las invisibles, `api.icons`,
   tokens usados y `relations.uses`/`usedBy`; `schemas/index.json` y `relationships.json`; la
   **parte viva** de cada ficha `docs/components/<slug>.md`/`docs/patterns/<slug>.md` (bloque
   `GENERATED:<slug>`) y el `## Índice` de `docs/components.md`/`docs/patterns.md`, conservando la
   parte de criterio escrita a mano (que vive solo en la ficha; el schema la señala con `source.docs`)
   y creando la ficha con `⬜ TODO` si el componente es nuevo (su forma: `docs/<carpeta>/_plantilla.md`); `docs/assets.md`; las secciones `GENERATED` del
   `showcase/index.html`; `reports/drift-report.json` con los hallazgos
   (`icon-not-exposed-as-swap`, `foundation-missing`, `schema-without-component`,
   `missing-variable-description-or-scope`, `primitive-with-scopes`, `text-style-weight-unknown`,
   `code-example-missing-or-stale`, `verification-stale`…). Un primitivo con `scopes: []` **no** es un hallazgo:
   es lo que pide «Arquitectura de variables de color». Se reconoce por estar oculto al
   publicar, por su colección (`primitiveCollections` en la config) o por ser base de otros
   sin apuntar a nadie; lo que sí se marca es un primitivo con scopes y `lastSync` en
   `agent-manifest.json`. Con `--dry` muestra qué haría sin escribir. Devuelve error si hay
   hallazgos críticos. **Ningún componente sin schema; ningún schema sin componente.**
6. **Completar el criterio.** Para cada contrato nuevo, rellenar a mano en el `.md` lo que
   Figma no puede decir: Propósito, **Ejemplo de código** (snippet HTML con las clases reales
   de `css/components.css`; `ds-sync` lo copia al schema como `source.code.example` y
   `classes` en la siguiente ejecución), Accesibilidad y Cuándo usar. Propósito, Accesibilidad y
   Cuándo usar se escriben **solo** en el `.md`, nunca en el schema. Comprobar que todas las
   clases del ejemplo existen en `components.css` y viceversa, y que
   `patterns.md § Composición de pantalla` tiene sus tablas rellenas o marcadas `⬜ TODO` con
   fecha. Volver a ejecutar `ds-sync.py` para propagar los ejemplos al schema y al showcase.
7. **Verificar.** `python3 scripts/token-audit.py --out design-system/reports/token-audit.json`
   con **cero errores** y `python3 scripts/ds-fidelity.py --out design-system/reports/fidelity.json`
   (avisos: lo que el CSS y los ejemplos no cuadran con el contrato, y cuántos contratos siguen sin verificar); abrir el showcase en el navegador como prueba visual de que tokens,
   componentes y ejemplos cuadran. Revisar la tabla componente → iconos detectados con el
   usuario. Después, `git diff` (incluye `sync/`, que muestra qué cambió en Figma) y commit.

En modo `preserve-existing`, la regeneración describe la arquitectura y nomenclatura
real de Figma. Las diferencias frente al estándar quedan en el informe de drift como
hallazgos informativos o decisiones aceptadas, no como órdenes de reestructuración. La
única escritura de mejora prevista sobre variables existentes es completar scopes y
descripciones mediante un lote previamente informado.

<details><summary>Script de lectura de variables y estilos (solo lectura; por trozos)</summary>

```js
// Se ejecuta con la herramienta de scripts del MCP oficial de Figma (`use_figma`), Plugin API.
// POR TROZOS: el MCP corta cada respuesta hacia los 20 KB, y un DS mediano ya lo supera. Cada
// llamada devuelve un trozo de unos 14 KB y dice dónde empieza el siguiente (part.nextOffset).
// Se llama con OFFSET = 0 y después con cada nextOffset, hasta que nextOffset sea null.
// Cada respuesta se guarda TAL CUAL en design-system/sync/parts/variables-<NNN>.json, en la misma
// vuelta en que llega. La unión la hace `python3 scripts/ds-sync.py --merge`, no el agente.
const OFFSET = 0;          // 0 en la primera llamada; después, el part.nextOffset de la anterior
const MAX_CHARS = 14000;   // tamaño máximo del trozo. No lo subas: por encima de ~20 KB el MCP corta

const collections = await figma.variables.getLocalVariableCollectionsAsync();
const textStyles = await figma.getLocalTextStylesAsync();
const effectStyles = await figma.getLocalEffectStylesAsync();
// Todo lo que hay que leer, en una lista plana y en orden fijo: un número basta para retomar.
const items = [];
for (const col of collections) for (const id of col.variableIds) items.push({ kind: 'variable', col, id });
for (const s of textStyles) items.push({ kind: 'text', s });
for (const s of effectStyles) items.push({ kind: 'effect', s });

const out = { kind: 'variables', fileKey: figma.fileKey || null, fileName: figma.root.name, version: null,
  readAt: new Date().toISOString(), part: { offset: OFFSET, nextOffset: null, count: 0, total: items.length },
  collections: [], textStyles: [], effectStyles: [] };
let size = JSON.stringify(out).length;
const colOut = new Map();

async function variable(id) {
  const v = await figma.variables.getVariableByIdAsync(id);
  if (!v) return null;
  const valuesByMode = {};
  for (const [modeId, val] of Object.entries(v.valuesByMode)) {
    if (val && typeof val === 'object' && val.type === 'VARIABLE_ALIAS') {
      const target = await figma.variables.getVariableByIdAsync(val.id);
      valuesByMode[modeId] = { type: 'alias', id: val.id, name: target ? target.name : null };
    } else {
      valuesByMode[modeId] = { type: 'value', value: val };
    }
  }
  return { id: v.id, name: v.name, type: v.resolvedType, description: v.description || '', scopes: v.scopes || [],
    codeSyntax: v.codeSyntax || {}, hiddenFromPublishing: v.hiddenFromPublishing, valuesByMode };
}

for (let i = OFFSET; i < items.length; i++) {
  const it = items[i];
  let entry, newCol = null;
  if (it.kind === 'variable') {
    entry = await variable(it.id);
    if (entry && !colOut.has(it.col.id)) {
      newCol = { id: it.col.id, name: it.col.name, modes: it.col.modes.map(m => ({ modeId: m.modeId, name: m.name })),
        defaultModeId: it.col.defaultModeId, variables: [] };
    }
  } else if (it.kind === 'text') {
    const s = it.s;
    entry = { id: s.id, name: s.name, description: s.description || '', fontFamily: s.fontName?.family || null,
      fontStyle: s.fontName?.style || null, fontSize: s.fontSize, lineHeight: s.lineHeight,
      letterSpacing: s.letterSpacing, boundVariables: s.boundVariables || {} };
  } else {
    const s = it.s;
    entry = { id: s.id, name: s.name, description: s.description || '', effects: s.effects.map(e => ({ type: e.type,
      visible: e.visible, radius: e.radius, spread: e.spread || 0, offset: e.offset || null, color: e.color || null })) };
  }
  const add = (entry ? JSON.stringify(entry).length + 1 : 0) + (newCol ? JSON.stringify(newCol).length + 1 : 0);
  if (out.part.count > 0 && size + add > MAX_CHARS) { out.part.nextOffset = i; break; }
  if (entry && it.kind === 'variable') {
    if (newCol) { colOut.set(it.col.id, newCol); out.collections.push(newCol); }
    colOut.get(it.col.id).variables.push(entry);
  } else if (entry) {
    (it.kind === 'text' ? out.textStyles : out.effectStyles).push(entry);
  }
  size += add;
  out.part.count++;
}
return out;
```
</details>

<details><summary>Script de lectura de componentes (solo lectura; una página por llamada, por trozos)</summary>

```js
// Se ejecuta con la herramienta de scripts del MCP oficial de Figma (`use_figma`), que expone la
// Plugin API de Figma. Es independiente del LLM: cualquier agente conectado al MCP la tiene.
// Antes de ejecutarlo, leer la guía `figma-use` que sirve el propio MCP (recurso skill://figma/figma-use).
// UNA PÁGINA POR LLAMADA y, dentro de la página, POR TROZOS: el MCP corta cada respuesta hacia
// los 20 KB y una página con muchas variantes lo supera. Se llama con OFFSET = 0 y después con cada
// part.nextOffset, hasta que sea null; luego, la página siguiente.
// Cada respuesta se guarda TAL CUAL en design-system/sync/parts/components-<NNN>.json, en la misma
// vuelta en que llega. La unión la hace `python3 scripts/ds-sync.py --merge`, no el agente.
const PAGE_ID = '0:1';     // id de la página (listar antes con figma.root.children: solo nombre e id)
const OFFSET = 0;          // 0 en la primera llamada de cada página; después, el part.nextOffset
const MAX_CHARS = 14000;   // tamaño máximo del trozo. No lo subas: por encima de ~20 KB el MCP corta
figma.skipInvisibleInstanceChildren = false; // imprescindible: los iconos suelen estar ocultos por defecto
const page = await figma.getNodeByIdAsync(PAGE_ID);
await figma.setCurrentPageAsync(page);

const nameOf = async (id) => { try { const n = await figma.getNodeByIdAsync(id); return n ? n.name : null; } catch { return null; } };
const varName = async (id) => { try { const v = await figma.variables.getVariableByIdAsync(id); return v ? v.name : id; } catch { return id; } };

async function bindings(root) {
  const vars = new Set(), styles = new Set();
  const nodes = [root, ...('findAll' in root ? root.findAll(() => true) : [])];
  for (const n of nodes) {
    const bv = n.boundVariables || {};
    for (const [prop, val] of Object.entries(bv)) {
      const list = Array.isArray(val) ? val : [val];
      for (const b of list) if (b && b.id) vars.add(`${prop}: ${await varName(b.id)}`);
    }
    for (const paint of [...(Array.isArray(n.fills) ? n.fills : []), ...(Array.isArray(n.strokes) ? n.strokes : [])])
      if (paint.boundVariables?.color?.id) vars.add(`color: ${await varName(paint.boundVariables.color.id)}`);
    if (n.type === 'TEXT' && typeof n.textStyleId === 'string' && n.textStyleId) {
      const s = await figma.getStyleByIdAsync(n.textStyleId); if (s) styles.add(s.name);
    }
  }
  return { variables: [...vars], textStyles: [...styles] };
}

async function nestedInstances(root) {
  const out = [];
  for (const inst of root.findAll(n => n.type === 'INSTANCE')) {
    const main = await inst.getMainComponentAsync();
    const refs = inst.componentPropertyReferences || {};
    out.push({
      layer: inst.name,
      component: main ? main.name : 'unknown',
      componentSet: main && main.parent && main.parent.type === 'COMPONENT_SET' ? main.parent.name : null,
      exposedAs: refs.mainComponent || null,   // nombre de la prop INSTANCE_SWAP que lo controla, o null
      toggledBy: refs.visible || null,          // nombre de la prop BOOLEAN que lo muestra/oculta, o null
      visibleByDefault: inst.visible
    });
  }
  return out;
}

const roots = page.findAllWithCriteria({ types: ['COMPONENT', 'COMPONENT_SET'] })
  .filter(n => !(n.type === 'COMPONENT' && n.parent && n.parent.type === 'COMPONENT_SET'));

const out = { kind: 'components', fileKey: figma.fileKey || null, readAt: new Date().toISOString(),
  page: { id: page.id, name: page.name }, part: { offset: OFFSET, nextOffset: null, count: 0, total: roots.length },
  components: [] };
let size = JSON.stringify(out).length;
for (let i = OFFSET; i < roots.length; i++) {
  const n = roots[i];
  const defs = n.componentPropertyDefinitions || {};
  const properties = [];
  for (const [name, d] of Object.entries(defs)) {
    const p = { name, kind: d.type, default: d.defaultValue ?? null };
    if (d.type === 'VARIANT') p.values = d.variantOptions || [];
    if (d.type === 'INSTANCE_SWAP') {
      p.defaultComponent = typeof d.defaultValue === 'string' ? await nameOf(d.defaultValue) : null;
      p.preferredValues = (d.preferredValues || []).map(v => ({ type: v.type, key: v.key }));
    }
    properties.push(p);
  }
  const sample = n.type === 'COMPONENT_SET' ? (n.defaultVariant || n.children[0]) : n;
  const entry = ({
    page: page.name, name: n.name, type: n.type, id: n.id, key: n.key || null,
    description: n.description || '',
    variantAxes: n.type === 'COMPONENT_SET' ? Object.fromEntries(Object.entries(n.variantGroupProperties || {}).map(([k, v]) => [k, v.values])) : {},
    variantCount: n.type === 'COMPONENT_SET' ? n.children.length : 1,
    properties,
    nestedInstances: await nestedInstances(sample),
    bindings: await bindings(sample),
    autoLayout: sample.layoutMode && sample.layoutMode !== 'NONE'
  });
  const add = JSON.stringify(entry).length + 1;
  if (out.part.count > 0 && size + add > MAX_CHARS) { out.part.nextOffset = i; break; }
  out.components.push(entry);
  size += add;
  out.part.count++;
}
return out;
```

Con esta salida, un componente **tiene icono** si alguna `properties[].kind === 'INSTANCE_SWAP'`
o alguna `nestedInstances[].component` pertenece a la familia de iconos del DS. Ambas cosas
se vuelcan al schema (`api.properties`, `api.nestedInstances`, `api.icons`, `relations.uses`).
Si un icono anidado no tiene `exposedAs`, el componente incumple la regla «icono =
`INSTANCE_SWAP`»: se registra igualmente en el schema y se abre hallazgo de auditoría.
</details>

---

## Auditoría del DS en Figma  🔍  (informe + remediación asistida)

**Cuándo:** al registrar por primera vez las fuentes de Figma, tras cambios grandes en
el DS, o cuando el usuario pida "auditar el design system". La auditoría es de **solo
lectura** y no requiere aprobación; cualquier corrección posterior sí. No confundir con
el informe de drift: el drift compara Figma con los artefactos generados; la auditoría
evalúa la calidad del **propio Figma**.

### Alcance multi-archivo

El DS puede repartirse entre varios archivos. Antes de evaluar nada:

1. Enumera todas las fuentes registradas arriba y determina el **rol real** de cada una
   (tokens, estilos, componentes, patrones, iconos, documentación) leyendo su contenido;
   el rol declarado por el usuario tiene prioridad y las discrepancias se reportan.
2. Evalúa cada archivo **solo contra las reglas propias de su rol**. Que un archivo
   contenga únicamente variables y ningún componente **no es un hallazgo**: la cobertura
   se evalúa sobre el conjunto.
3. El informe final consolida el conjunto: cobertura global (tokens, tipografía,
   componentes, patrones, iconos), dependencias entre archivos (qué librerías se
   publican y quién las consume), duplicidades y contradicciones entre archivos. Solo es
   hallazgo de cobertura lo que falte en **todo** el conjunto, no en un archivo suelto.

### Qué se comprueba

**A. Estándares propios del equipo** — las "Reglas duras" y "Reglas duras en Figma" de
este documento, aplicadas según el modo de adopción registrado arriba: con
`preserve-existing` o `pending-inspection`, las desviaciones estructurales se reportan
como hallazgos informativos, nunca como órdenes de corrección.

**B. Buenas prácticas generales de DS en Figma**, como mínimo:

- **Nomenclatura**: ninguna página, frame, grupo, capa, componente, variante o variable
  sin nombre o con nombre genérico ("Frame 123", "Group 7", "Rectangle 40"); una sola
  convención coherente (idioma, casing, separadores, jerarquía `/`, variantes
  `Propiedad=Valor`) en todo el conjunto de archivos, no solo dentro de cada uno.
- **Vinculación a estilos/variables**: todo color, texto, efecto, radio, spacing y
  tipografía ligado a una variable o estilo; se reporta cualquier valor local,
  hardcodeado o estilo desanexado, con la variable/estilo candidato cuando exista.
- **Componentización**: variantes agrupadas en component sets (no componentes duplicados
  sueltos); propiedades de componente (boolean, text, instance swap) en lugar de capas
  ocultas ad hoc; sin instancias desanexadas reconstruidas a mano; descripciones de
  componente rellenas; base components y organización por página/sección con criterio.
- **Candidatos a slot**: variantes cuyos valores son tipos de contenido
  (`Contenido=Imagen`, `Contenido=Lista`) o hijos alternativos en la misma zona encendidos
  por booleanos. Hallazgo `assisted`, con el recuento de instancias afectadas; cómo se
  migra está en `figma.md § 3-ter`.
- **Estructura**: Auto Layout en todo contenedor estructural; constraints coherentes;
  sin capas ocultas basura ni elementos sueltos fuera de frames.
- **Higiene de librería**: estilos y variables sin uso, duplicados de valor idéntico
  bajo nombres distintos, y estados de publicación incoherentes entre archivos.

### Informe

La auditoría regenera dos artefactos (⚙️ generados, no editar a mano):

- `reports/audit-report.json` — hallazgos estructurados para máquinas.
- `reports/audit-report.md` — informe legible: estado por archivo, estado del conjunto
  y, **por cada hallazgo: qué está mal, por qué importa y cómo corregirlo** paso a paso.

Cada hallazgo registra la regla evaluada, su origen (`skill` o `general`), severidad
(`critical` / `warning` / `info`), archivo y nodo o variable afectados, recomendación
accionable y **fixability**: `auto` (mecánico y determinista), `assisted` (requiere una
decisión de diseño) o `manual` (solo puede resolverlo una persona).

### Remediación asistida (opt-in, nunca automática)

Tras entregar el informe, ofrece al usuario que la IA aplique correcciones en Figma:

1. Propón un plan por lotes: primero los `auto` (renombrados según la convención
   acordada, scopes y descripciones, bindings a variables existentes cuando el candidato
   es inequívoco), después los `assisted` uno a uno con su decisión pendiente.
2. Cada lote se muestra y se aprueba **antes** de escribir en Figma (capacidad
   `apply-audit-mechanical-fixes`, aprobación por lote). Los cambios estructurales
   (crear o cambiar tokens y componentes, fusiones, migraciones) siguen las aprobaciones
   de "Gobierno agentic y confianza gradual": nunca entran en un lote mecánico.
3. En modo `preserve-existing`, ningún renombrado ni cambio estructural entra en un plan
   de fixes sin la decisión explícita de reestructuración; solo scopes y descripciones.
4. Tras aplicar los lotes, re-ejecuta la auditoría sobre lo corregido y actualiza ambos
   informes: los hallazgos resueltos pasan a `fixed` y los asumidos a `accepted`.

Si el entorno no dispone del MCP oficial de Figma, la auditoría queda **pendiente**: no
simules lecturas ni generes hallazgos inventados.

---

## Estructura

```
design-system/
├── design.md            ← este archivo: router + reglas + protocolo de sync (se edita a mano)
├── agent-manifest.json  ← entrada única para máquinas
├── docs/                ← para personas: tokens.md · assets.md · components.md y patterns.md (índice + secciones manuales) · components/<slug>.md y patterns/<slug>.md (una ficha por contrato; _plantilla.md es la forma de una ficha nueva)
├── tokens/              ← ⚙️ GENERADO: tokens.json (máquinas) · tokens.css (código, incl. tema oscuro)
├── css/                 ← components.css — único CSS del DS (átomos + patrones + capa de pantalla)
├── assets/              ← ⚙️ exportado de Figma: icons/ · fonts/
├── schemas/             ← para IA: _component.schema.json · index.json · relationships.json · governance/ · components/<slug>.schema.json
├── reports/             ← ⚙️ drift-report · audit-report · token-audit
├── proposals/           ← contrato de propuestas sujetas a revisión humana
├── sync/                ← volcados de Figma leídos por MCP (variables.json · components.json · icons.json): entrada de ds-sync.py
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
