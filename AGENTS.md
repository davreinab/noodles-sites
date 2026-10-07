# gb-noodles-microsites

## Cómo responder (para cualquier persona del equipo, técnica o no)

Quien te habla es, normalmente, alguien de diseño o producto. No tiene por qué saber git,
terminal ni la estructura interna del repo. Por eso:

1. **Toda respuesta que cambie archivos o ejecute comprobaciones tiene cuatro partes**, en
   este orden y con estos nombres: **Qué pasó** (lo que acabas de hacer, en una o dos
   frases) · **Por qué importa** (qué cambia para el diseño o para desarrollo) · **Cómo se
   arregla** (el siguiente paso concreto, si hace falta; si no, «nada que arreglar») ·
   **Cómo se ve bien** (la señal de «listo»). Si no hay nada que corregir, la tercera parte
   lo dice así.
2. **Lenguaje claro.** Nada de jerga sin traducir: no digas «exit 1», di «la comprobación
   encontró errores». Traduce la salida de los scripts a frases: archivo, qué está mal, qué
   token o carpeta va en su lugar. Los nombres de archivo van entre comillas de código y
   solo cuando la persona tenga que abrirlos.
3. **Un pedido, una respuesta.** Si llegan varios pedidos en un mensaje, di en qué orden
   los harás y hazlos de uno en uno. Si un pedido es ambiguo, pregunta antes de tocar nada.
4. **Git es tuyo, la decisión es suya.** Antes de un commit muestra en una lista qué
   archivos cambian y por qué, y espera un «sí». Nunca hagas push sin pedirlo. Nunca pidas
   a la persona que ejecute git.

### Peticiones en lenguaje normal → qué haces

| Si te piden… | Haz | Y responde con |
|---|---|---|
| «¿cómo voy?» / «¿qué falta?» | `python3 scripts/token-audit.py`, `python3 scripts/context-audit.py`, `python3 scripts/research-index.py --check`, y cuenta los `⬜ TODO` de `context/` y `UX/direction/DESIGN.md` | Lista de huecos en lenguaje claro, agrupada por zona; sin muro técnico |
| «guarda» / «deja esto guardado» | Muestra qué archivos cambian y por qué; con el «sí», commit con mensaje claro. El hook `pre-commit` ejecuta las comprobaciones; si falla, explica qué y corrige | Qué se guardó y qué quedó fuera |
| «apunta esto» / contexto nuevo | `context/AGENTS.md § Distribución`: cada dato a su archivo; research siempre como nota nueva + índice | Dónde quedó cada cosa |
| «¿cuál es…?» / «¿qué dice el contexto sobre…?» | Abre el documento que indica `context/AGENTS.md § Enrutado`. Si el dato está en `⬜ TODO`, en `🚫 No existe` o no aparece, no lo deduzcas | «No lo sé, no está en el contexto» + dónde debería estar y qué haría falta |
| «hazme <pantalla / flujo / requisito / texto>» | Antes de empezar, comprueba en `context/` los datos de los que depende. Si falta alguno, para y avisa (`context/AGENTS.md` regla 1d) | «No se puede completar porque falta <dato> (<documento>)». Opciones: aportarlo ahora o hacer solo la parte que no depende de él, con el hueco marcado |
| «esto ya te lo dije» / segunda corrección de lo mismo | Regla «Correcciones repetidas» de abajo: se escribe en esa sesión | Dónde quedó escrito y que no se volverá a preguntar |
| «esto cambió respecto a la propuesta» / «esto ya no entra» / «hemos acordado que…» | `context/proposal-agreements.md § Cómo se cambia lo acordado`. **Pregunta siempre quién lo acordó y dónde antes de escribir nada**; si no hay acuerdo todavía, márcalo como pendiente de negociar, no lo apliques (regla 1e) | Qué cambió, dónde quedó registrado y qué documentos hay que revisar |
| «sincroniza el design system» / «cambió Figma» | `design-system/design.md § Sync desde Figma` | Qué tokens y componentes cambiaron, qué se regeneró, qué queda pendiente |
| «¿cómo debería verse?» / «dale estilo» | Lee `UX/direction/DESIGN.md` primero. Si está en `⬜ TODO`, pide referencias en vez de inventar | Qué dirección aplicaste y de qué referencia sale |
| «¿por qué hiciste esto?» | Cita la regla o el archivo de origen (`design.md` regla N, `patterns.md § Decisiones recurrentes`, `specs.md` R-xx) | La regla, en una frase, y dónde vive |

## Contexto funcional compartido

**Antes de leer, escribir o citar cualquier dato funcional, lee
[`context/AGENTS.md`](./context/AGENTS.md).** Es la **única fuente de verdad de las normas
de contexto**: router (qué documento abrir según la petición), reglas duras, tabla de
distribución (dónde va cada dato), protocolo de cambios y marcadores. No dupliques sus
reglas aquí; si algo cambia, se edita allí.

Lo mínimo que hay que saber sin abrirlo:

- La definición del producto, roles, reglas de negocio, modelo de datos, flujos, síntesis y
  specs viven en [`context/`](./context/). Es contexto común para UX, UI y design system:
  se consulta antes de cualquier decisión funcional y no se duplica en carpetas de
  implementación.
- Los datos brutos de investigación viven en [`research/`](./research/), una nota por
  fuente. En `context/` se citan, nunca se resumen. La cadena **nota → touchpoint → feature
  → user story → requisito** es obligatoria; lo que no tenga origen queda `⬜ TODO — origen`
  y no es normativo.
- **Nada se inventa.** Lo que falta se marca en el propio documento (`⬜ TODO` si nadie lo
  aportó, `🚫 No existe` si la persona confirmó que no existe). Si te preguntan por algo que
  está así marcado o no aparece, la respuesta es «no lo sé, no está en el contexto» y dónde
  debería estar. Nunca una estimación.
- **Si un pedido depende de un dato que falta, no se completa: se avisa antes de empezar.**
  «Esta petición no se puede completar porque falta <dato>, que debería estar en
  <documento>». Después se ofrece aportar el dato o hacer solo la parte que no depende de él
  dejando el hueco marcado. Nunca se rellena el hueco para poder terminar.
- Research se consulta por `research/index.json`, no releyendo las notas. Tras crear o
  modificar una nota: `python3 scripts/research-index.py`.

### Correcciones repetidas se convierten en reglas

Si el usuario corrige lo mismo **dos veces** (en dos pantallas, dos sesiones o dos
revisiones), ya no es un gusto puntual: es una regla no escrita, y se escribe **en esa misma
sesión**, antes de seguir:

- Si afecta a estilo, componentes, composición o layout → nueva fila en
  [`design-system/docs/patterns.md § Decisiones recurrentes`](./design-system/docs/patterns.md),
  con fecha, la regla en una frase, dónde se corrigió cada vez y a qué aplica. Si la regla
  implica una medida o un color, nace como token en Figma y se sincroniza; si afecta a un
  componente, se promueve a su contrato.
- Si afecta a lógica, contenido, roles o reglas de negocio → el documento de `context/`
  que corresponda por la tabla de distribución, citando la corrección como origen.

No esperes a la tercera. Una decisión registrada es normativa: las pantallas y agentes la
consultan como cualquier otra regla, y una corrección que ya está escrita no se vuelve a
preguntar.

### Distribución de contexto nuevo

Cuando el usuario aporte contexto nuevo, se coloca según la tabla **Distribución** de
[`context/AGENTS.md`](./context/AGENTS.md): cada dato a un solo archivo, sin duplicar;
research siempre como nota nueva en `research/` + índice; ningún `.md` nuevo en `context/`
sin confirmación explícita.

## Antes de tocar UI o el design system

**Antes de crear un componente nuevo, comprueba qué permite el encargo** en
[`context/proposal-agreements.md § Restricciones del encargo`](./context/proposal-agreements.md).
Hay encargos que solo permiten **componer** con lo que ya existe en el design system, o que
piden entregar lo nuevo sin color. Son límites negociados, no reglas del sistema, así que no
están en `design.md` y un agente que solo lea las reglas del DS no los verá. Si hay
restricción y el trabajo la incumple, se dice antes de empezar: cambiarla es una
renegociación, no una decisión de diseño.

**Antes de proponer cualquier estilo, lee [`UX/direction/DESIGN.md`](./UX/direction/DESIGN.md).**
Es la dirección visual escrita (tono, paleta e tipografía como intención, patrones de
interacción, referencias seleccionadas). Se lee antes del primer sync de un DS nuevo, antes
de cada pantalla de UI y antes de refinar por prompts. Si está en `⬜ TODO`, no inventes una
dirección: dilo y pide referencias. Los valores concretos no salen de ahí: nacen en Figma
como tokens.

Si el producto tiene superficie móvil, lee también
[`UX/mobile-environment.md`](./UX/mobile-environment.md) antes de cualquier pantalla móvil:
es la especificación del entorno que se simula con tecnologías web.

**Lee después [`design-system/design.md`](./design-system/design.md).** Es la **única fuente de
verdad** de las reglas del design system GB Noodles · Microsites (índice + reglas duras + Modelo B + protocolo
de sync). No dupliques sus reglas aquí; si algo cambia, se edita en `design.md`.

`design.md` funciona como **router**: te dice qué archivo abrir según la tarea
(`tokens.md`, el índice `components.md` o `patterns.md` y, desde ahí, solo la ficha
`docs/components/<slug>.md` o `docs/patterns/<slug>.md` de cada componente que vayas a usar). No
los leas todos por defecto.

**Si eres una IA y necesitas el DS como datos estructurados**, empieza siempre por
[`design-system/agent-manifest.json`](./design-system/agent-manifest.json). Es el router
para recuperar solo tokens, componentes, relaciones, políticas o capacidades relevantes,
sin cargar el sistema entero. Los `.md` son para personas; los JSON son contratos para
máquinas y ambos se sincronizan juntos.

**Antes de colocar componentes en una pantalla**, lee `patterns.md § Composición de
pantalla` (sigue en ese archivo; las fichas de patrón viven aparte en `docs/patterns/`): ritmo vertical entre secciones, anchos de contenedor, grid y breakpoints,
comportamiento de paneles y escalera de capas. Toda decisión de layout es una consulta a
esa sección, no una elección propia. Si la regla que necesitas no está escrita, se añade
allí primero (y su medida nace como token en Figma) y después se usa.

**Antes de cada commit**, el hook `.githooks/pre-commit` ejecuta las verificaciones de los
módulos activos —valores crudos y estructura del DS, secciones obligatorias de `context/`, e
índices de research y analítica— y rechaza el commit si alguna falla. Las ejecuta todas aunque
una falle, para que veas de una vez todo lo que hay que arreglar.

**Solo cuando el proyecto está conectado a un repositorio remoto.** Sin remoto (alguien que
trabaja en local), el hook deja pasar el commit y avisa de que las comprobaciones están
apagadas. Se activan solas en cuanto se conecta (`git remote add …`). Si el proyecto ni
siquiera tiene git, al crearlo o clonarlo hay que ejecutar `git config core.hooksPath
.githooks` para que el hook exista. Puedes lanzarlas a mano en cualquier momento:

```bash
python3 scripts/token-audit.py      # diseño visual y design system
python3 scripts/ds-fidelity.py      # ¿el CSS y las fichas cuadran con el maestro de Figma? (avisos)
python3 scripts/context-audit.py    # documentos funcionales de context/
python3 scripts/research-index.py --check
```

Si falla, corrige el valor crudo (en Figma → sync, o en la clase de `components.css`), el
archivo mal colocado o el índice; nunca el script, el hook ni su configuración. Saltar el
hook con `--no-verify` exige anotar el motivo en el mensaje de commit. Las plantillas de CI
de `ci/` ejecutan lo mismo en el remoto; se activan solo cuando el equipo lo pide. Las excepciones justificadas (hairlines de borde,
utilidades de accesibilidad) ya están en `scripts/token-audit.config.json`; añadir una
nueva requiere anotar el motivo en `design.md`.

Para **wireframes de UX**, ver [`UX/wireframes/AGENTS.md`](./UX/wireframes/AGENTS.md) — usan su
propio kit de paleta `--wf-*`, no los tokens del DS (ver "Alcance" en `design.md`).

## No indexar (prototipo interno)

Es un prototipo interno: **no debe indexarse en buscadores**. Todo HTML nuevo que se
publique debe llevar, en el `<head>`, justo tras el `<meta charset>`:

```html
<meta name="robots" content="noindex, nofollow" />
```
