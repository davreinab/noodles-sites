# GB Noodles · Microsites — Brand websites de las marcas de noodles de GB Foods en Europa sobre un WordPress multisite común, con un sistema de diseño modular por marca.

Fase 2 del relanzamiento «natural noodles» de GB Foods: webs de marca para Yatekomo (ES),
Saikebon (IT), Aïki (BE) y la nueva marca de Alemania, que sustituyen a las webs locales de
cada país y a las landings de la Fase 1. Público de 18 a 35 años, que llega sobre todo desde el móvil.

> Prototipo interno. Sus páginas HTML deben declarar `noindex, nofollow`.

## Mapa del repositorio

| Carpeta | Qué contiene | Empieza por |
|---|---|---|
| [`research/`](./research/) | Base de conocimiento de investigación: una nota Markdown por fuente (entrevistas, desk research, benchmarks…), con metadatos de fuente, fecha, canal y confianza. `index.json` es el índice consultable (generado). | [`research/README.md`](./research/README.md) |
| [`analytics/`](./analytics/) | Base de conocimiento cuantitativa: una nota por medición, con métrica, periodo, segmento y tamaño de muestra. Se separa de `research/` porque una medición se repite y una entrevista no. Puede marcarse `Aplica: no`. | [`analytics/README.md`](./analytics/README.md) |
| [`context/`](./context/) | Contexto funcional compartido: definición del producto, lo comprometido en el encargo, objetivos y métricas, reglas, perfiles de usuario, glosario, modelo de datos, flujos, síntesis (hallazgos → touchpoints → features → user stories) y specs trazadas a su origen. Sus normas (qué documento abrir, dónde va cada dato, qué no se inventa) están en `context/AGENTS.md`. | [`context/AGENTS.md`](./context/AGENTS.md) · [`context/project-context.md`](./context/project-context.md) |
| [`UX/`](./UX/) | Dirección visual (`direction/`: moodboard anotado + `DESIGN.md`), entorno móvil simulado si aplica, y wireframes HTML navegables con sus reglas. | [`UX/direction/DESIGN.md`](./UX/direction/DESIGN.md) · [`UX/wireframes/AGENTS.md`](./UX/wireframes/AGENTS.md) |
| [`design-system/`](./design-system/) | Sistema de diseño GB Noodles · Microsites: tokens, componentes y patrones. Fuente de verdad en Figma; los artefactos se generan por sync. | [`design-system/design.md`](./design-system/design.md) |
| [`UI/`](./UI/) | Pantallas de UI aplicando el design system (marca GB Noodles · Microsites, tokens reales). | — |
| [`scripts/`](./scripts/) | Herramientas sin dependencias: motor del sync del design system (`ds-sync.py`, de los volcados de Figma a todos los artefactos), auditoría del design system (`token-audit.py`), fidelidad de los contratos a su maestro de Figma (`ds-fidelity.py`), auditoría de los documentos funcionales (`context-audit.py`) e índice de las bases de evidencia (`research-index.py`, que sirve a `research/` y a `analytics/`). Las cuatro primeras las ejecuta el hook `.githooks/pre-commit` antes de cada commit. | `python3 scripts/token-audit.py` |
| [`ci/`](./ci/) | Plantillas de integración continua (GitHub, Bitbucket) que ejecutan lo mismo que el hook. No activas hasta que el equipo lo pida. | [`ci/README.md`](./ci/README.md) |

Cada carpeta relevante tiene su propia documentación; este README solo orienta y
enruta — el detalle de cada capa vive en su carpeta y no se duplica aquí.

## Dos capas visuales, no confundir

- **Wireframes (`UX/wireframes/`)** — estética de wireframe, paleta propia del kit de
  Multiplica (`--wf-*`). Foco en estructura y comportamiento, no en marca.
- **UI (`UI/` + `design-system/`)** — diseño final con la marca GB Noodles · Microsites y los tokens
  del design system.

Las reglas que separan ambas capas están en
[`design-system/design.md`](./design-system/design.md) (sección "Alcance").

## Cómo pedir las cosas (sin saber git ni terminal)

Se trabaja hablando con el asistente de IA en lenguaje normal. No hace falta saber
programar, usar la terminal ni «hacer commit»: eso lo hace el asistente y te pide
confirmación antes de guardar. Toda respuesta que cambie algo llega en cuatro partes:
**qué pasó · por qué importa · cómo se arregla · cómo se ve bien**. Si falta alguna, pídela.

| Dices | Pasa |
|---|---|
| «¿cómo voy?» | Ejecuta las comprobaciones y te lista qué falta, por zona, en lenguaje claro |
| «apunta que…» | Coloca el dato en el documento que le corresponde (te dice cuál) |
| «¿cuál es…?» | Te lo lee del contexto. Si no está, te dice «no lo sé» y dónde debería estar; nunca se lo inventa |
| «hazme…» y falta un dato | Te avisa antes de empezar: «no se puede completar porque falta X». Tú decides si lo aportas o si hace solo lo que no depende de ese dato |
| «esto ya te lo dije» | Lo escribe como regla para no volver a preguntarlo |
| «esto cambió respecto a la propuesta» | Te pregunta **quién lo acordó y dónde**, lo escribe en el registro de cambios y marca lo que había quedado afectado. Si todavía no está acordado con la otra parte, lo deja marcado como pendiente de negociar en vez de aplicarlo |
| «guarda» | Te muestra qué archivos cambian y, con tu «sí», lo guarda en git |
| «cambió Figma» / «sincroniza» | Trae los cambios del design system y te dice qué se regeneró |
| «¿cómo debería verse?» | Lee la dirección visual escrita en `UX/direction/DESIGN.md`; si está vacía, te pide referencias |
| «¿por qué hiciste esto?» | Te cita la regla o el archivo de donde sale la decisión |

Si una respuesta suena a sistema («exit 1», «token», «hook»), pide: «en lenguaje claro».

## Instrucciones para agentes de IA

El contexto operativo para agentes vive en `AGENTS.md` (raíz y por carpeta). Los archivos
`CLAUDE.md` y `GEMINI.md` son solo punteros a `AGENTS.md` para las herramientas que buscan
ese nombre; cualquier otra herramienta debe leer `AGENTS.md` directamente.
