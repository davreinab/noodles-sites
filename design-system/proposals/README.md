# GB Noodles · Microsites · Propuestas de cambio del DS

Aquí empieza **todo cambio no trivial** del design system: un token nuevo, un componente
nuevo, cambiar una variante, retirar algo. Primero se escribe, luego se decide, y solo
entonces se toca Figma o el código.

No es burocracia: es lo que evita tener la misma discusión tres veces y lo que deja por
escrito quién dijo que sí.

## Cuándo empiezan a hacer falta

Mientras el design system **no se ha publicado** es un borrador: se edita sin propuestas, porque no hay nadie
que dependa de él. La primera `python3 scripts/ds-release.py --apply` fija la línea base y lo declara
publicado (`ds-release.py --check` dice en qué estado está). **Desde ahí**, cambiar o retirar algo ya publicado
necesita una propuesta aprobada que lo cite en `affectedResources` (la ruta del token o el slug del componente).
**Añadir algo nuevo no necesita propuesta**: sube la versión menor y nadie se rompe. `ds-release.py --check` lo
comprueba contra la línea base; `proposalsEnforcement` del `agent-manifest.json` decide si una propuesta que falta
es aviso (`warn`, por defecto) o error (`error`, falla el commit).

## Qué es trivial y qué no

| No hace falta propuesta | Sí hace falta |
|---|---|
| Corregir una errata de ortografía que no cambia el sentido | Renombrar, retirar o cambiar el valor de un token ya publicado |
| Regenerar artefactos con el sync | Renombrar o retirar un componente o patrón ya publicado |
| Arreglar un valor que incumple AA, con la corrección evidente | Quitar o cambiar variantes, estados o propiedades de un componente ya publicado |
| Añadir un token, componente, variante o propiedad nuevos (sube la versión menor) | **Cambiar la descripción o el criterio de uso** de un componente o patrón: qué es, cuándo usarlo, qué no hace, accesibilidad |
| | Cambiar la metodología, la nomenclatura o las colecciones |

La descripción y el criterio de uso son lo que leen diseño, desarrollo y la IA para decidir
cuándo poner un componente y cuándo no. Cambiarlos cambia cómo se usa el sistema, aunque en
Figma no se mueva un píxel: por eso necesitan propuesta y una persona que apruebe. Da igual
dónde se edite (Figma, la ficha o el visor): sin propuesta aprobada no se escribe.

## Cómo se escribe

Un archivo por propuesta, `<fecha>-<slug>.json`, que valide contra
[`_proposal.schema.json`](./_proposal.schema.json). Los campos obligatorios son los que
obligan a pensar: qué cambia, con qué evidencia, a quién afecta, cómo se migra y quién aprueba.

- **`evidence`** — por qué hace falta. Pantallas, capturas de uso, notas de research.
- **`impact`** — qué se rompe y dónde. Si afecta a algo publicado, sale del informe de
  cobertura y del de deriva.
- **`migration`** — qué hace quien ya lo estaba usando. `null` solo si de verdad no aplica.
- **`requiredApprover`** — una persona, no un equipo.
- **`decision`** — se rellena al aprobar o rechazar, con fecha. No se borra una propuesta
  rechazada: el historial de lo que se decidió no hacer también vale.

## Estados

`draft` → `approved` | `rejected` → `applied`

Una propuesta pasa a `applied` cuando el cambio está en Figma **y** sincronizado al repo.

**Cada propuesta vive en la carpeta de su estado**, para ver de un vistazo qué falta por decidir:

| Dónde | Estado |
|---|---|
| `proposals/` (sueltas en la raíz) | ⏳ pendientes de decisión: `draft` o `approved` sin aplicar |
| `proposals/aplicadas/` | ✅ `applied` |
| `proposals/rechazadas/` | ❌ `rejected` |

Mientras una propuesta está pendiente, su cambio se puede probar en pantallas con un
**override** (`UI/overrides/<id>.css`, ver `guides/overrides.md`); al aplicarse o
rechazarse, el override sobra y `token-audit` lo dice.

Cada vez que se crea una propuesta o cambia su estado, se ejecuta
`python3 scripts/proposals-index.py`: mueve el archivo a su carpeta y regenera el índice de abajo
(`--check` solo comprueba que todo esté en su sitio y al día; es lo que lanzan el hook de commit y
la CI).

## Cuando la propuesta sale de la library

En la ficha de cada componente del visor (`library/`), la descripción y cada campo del criterio de
diseño (propósito, cuándo usar…) tienen un botón **Editar**. No cambia el texto: crea una propuesta
`<fecha>-<slug>-textos.proposal.json` (`proposedChange.kind: "component-text"`) con, por cada campo
tocado, el texto actual y el propuesto; el motivo va como evidencia y se pide quién aprueba.

- **Una sola propuesta por componente para todos sus textos.** Editar otro campo del mismo
  componente añade el cambio a la propuesta pendiente; no abre otra.

- **Volver a editar un campo** cambia su texto propuesto en esa misma propuesta y anota la edición en
  `proposedChange.history`. Si estaba `approved` y
  aún sin aplicar, editarla la devuelve a `draft` y borra la decisión: lo aprobado era otro texto.
- **Mientras está pendiente,** la library enseña el texto propuesto con su estado, y el texto
  vigente de Figma queda a la vista debajo.
- **La IA usa la misma propuesta.** `python3 scripts/ds-text-proposal.py` crea o actualiza la
  propuesta de textos de un componente con la misma forma que la library (borradores de accesibilidad,
  `guides/accesibilidad.md`). Cada cambio guarda su `origin`: `ai` (la library lo marca
  «Borrador de la IA») o `person`; cuando una persona lo edita, pasa a `person`.
- **«No aplica»** en el campo de accesibilidad también es un cambio de criterio: va como propuesta con
  el texto «No aplica.» y el motivo como evidencia.
- **Con `npm start`** la propuesta se guarda sola aquí y se regeneran el índice y el catálogo. **Con la
  library publicada** como web, el botón la descarga y hay que guardarla en esta carpeta (si ya había
  una para ese componente, sustituyéndola).
- **Al aprobarla,** la IA escribe cada `changes[].proposed` en su sitio: `where: "figma"` es la
  descripción del componente en Figma (por el MCP oficial; después relee ese componente con
  `NODE_IDS` y `ds-sync.py --merge`); `where: "ficha"` es el campo del mismo nombre en la ficha del
  componente (`docs/components/<slug>.md`, debajo del bloque generado). Luego ejecuta el sync,
  rellena `decision.appliedAt` y la pasa a `applied`.

## Cuando la propuesta es una retirada

Además de la propuesta, la retirada se anota en
[`../schemas/governance/lifecycle.json`](../schemas/governance/lifecycle.json) con la fecha,
la versión en que desaparece, el motivo y el sustituto. A partir de ahí,
`scripts/ds-lifecycle.py` avisa de quién lo sigue usando y, pasado el plazo, bloquea los
usos nuevos.

## Índice por estado

<!-- ⚙️ GENERATED:start:index -->

_0 propuestas. Este bloque lo genera `scripts/proposals-index.py`: no se edita a mano._

### ⏳ Pendientes de decisión (0)

Ninguna.

### ✅ Aplicadas (0)

Ninguna.

### ❌ Rechazadas (0)

Ninguna.

<!-- ⚙️ GENERATED:end:index -->
