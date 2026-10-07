# GB Noodles · Microsites · Propuestas de cambio del DS

Aquí empieza **todo cambio no trivial** del design system: un token nuevo, un componente
nuevo, cambiar una variante, retirar algo. Primero se escribe, luego se decide, y solo
entonces se toca Figma o el código.

No es burocracia: es lo que evita tener la misma discusión tres veces y lo que deja por
escrito quién dijo que sí.

## Qué es trivial y qué no

| No hace falta propuesta | Sí hace falta |
|---|---|
| Corregir una descripción o una errata | Añadir, renombrar o retirar un token |
| Regenerar artefactos con el sync | Añadir, renombrar o retirar un componente o patrón |
| Arreglar un valor que incumple AA, con la corrección evidente | Cambiar variantes, estados o propiedades de un componente |
| | Cambiar la metodología, la nomenclatura o las colecciones |

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

## Cuando la propuesta es una retirada

Además de la propuesta, la retirada se anota en
[`../schemas/governance/lifecycle.json`](../schemas/governance/lifecycle.json) con la fecha,
la versión en que desaparece, el motivo y el sustituto. A partir de ahí,
`scripts/ds-lifecycle.py` avisa de quién lo sigue usando y, pasado el plazo, bloquea los
usos nuevos.
