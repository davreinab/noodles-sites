<!-- vigencia
  autoridad: ⬜ TODO — quién manda sobre este documento (cliente, negocio, legal, el equipo)
  confirmado: ⬜ TODO — fecha ISO de la última vez que alguien dijo «esto sigue siendo verdad»
  estado: pendiente-de-confirmar
  Las reglas de PROPIEDAD no caducan (un identificador no cambia de naturaleza). Las de
  DECISIÓN sí: caducan a los 6 meses de «confirmado» y la auditoría avisa, no bloquea.
-->

# Síntesis — GB Noodles · Microsites

Traducción progresiva de la evidencia a unidades de diseño. Cada fila cita la anterior:

**nota de [`../research/`](../research/) o medición de [`../analytics/`](../analytics/) →
hallazgo → touchpoint → feature → user story → requisito.**

Nada se inventa: lo que no tenga origen trazable se marca `⬜ TODO`.

Las features se cruzan además con [`objectives.md`](./objectives.md): la evidencia dice de
dónde viene una capacidad, el objetivo dice para qué la queremos. Las dos cosas se piden.

## Hallazgos
Lo que la evidencia dice **cruzando fuentes**. Una observación suelta (`R-… §O-n`) o un dato
suelto (`A-… §D-n`) son lo que vio una persona o midió una herramienta; un hallazgo es lo que
sostienen varios a la vez, con su prevalencia dicha en voz alta.

Es el escalón que falta entre registrar y decidir. Sin él se salta de «un participante dijo
esto» a «el producto tendrá esta pantalla», y por el camino se pierde cuánta gente, en qué
tarea y qué sigue sin saberse — que es justo lo que alguien preguntará dentro de seis meses.

| ID | Hallazgo | Prevalencia | Origen | Qué queda sin confirmar |
|---|---|---|---|---|
| H-01 | ⬜ TODO | ⬜ TODO | ⬜ TODO | ⬜ TODO |

- **Prevalencia** — en cuántas de las fuentes que podían mostrarlo aparece, y sobre cuántas.
  «5 de 8 participantes», «2 de 2 informes del último trimestre». Sin denominador no es
  prevalencia, es una impresión.
- **Di de quién es la voz.** Si el hallazgo no se apoya en usuarios, la prevalencia lo dice:
  «3 de 3 stakeholders lo creen · 0 usuarios consultados». Es el campo `voice` de las notas, y
  cambia lo que el hallazgo puede sostener: que alguien *cuente* que los usuarios se pierden
  no es lo mismo que *verlos* perderse. No invalida el hallazgo —trabajar sin acceso a
  usuarios es normal—, pero tiene que notarse aquí, porque de aquí para abajo ya no se nota.
- **Origen** — todas las unidades que lo sostienen, de las dos bases: `R-… §O-n` y
  `A-… §D-n`. Un hallazgo con una sola fuente es legítimo, pero entonces se dice: es un
  indicio, no un patrón.
- **Qué queda sin confirmar** — la parte que la evidencia no cubre. Se escribe aquí para que
  no desaparezca al convertirse en touchpoint. Si no queda nada sin confirmar, `—`.
- **Las contradicciones se resuelven aquí, no en silencio** (regla 10). Si dos notas chocan,
  el hallazgo dice qué se decidió, por qué y con qué origen — o queda `⬜ TODO` hasta
  preguntarlo.

## Touchpoints
Momentos del journey en los que el producto debe estar presente. Aún no son funciones
ni pantallas.

| ID | Momento del journey | Descripción | Origen (hallazgo) |
|---|---|---|---|
| TP-01 | ⬜ TODO | ⬜ TODO | H-… |

## Features
Capacidades concretas que responden a uno o más touchpoints. Cada una se justifica en dos
sentidos: **Responde a** dice de qué evidencia nace, **Contribuye a** a qué objetivo sirve
([`objectives.md`](./objectives.md)). Una feature que no puede llenar ninguna de las dos
columnas es una feature que nadie pidió.

| ID | Feature | Responde a | Contribuye a | Decisión | Motivo |
|---|---|---|---|---|---|
| FT-01 | ⬜ TODO | TP-… | OBJ-… | in / out fase 1 | ⬜ TODO |

## User stories
Una por necesidad, no por función. Formato: quién, en qué circunstancia, qué y para qué.

### US-01 · <título corto>
- **Como** <rol>, **cuando** <circunstancia>, **quiero** <capacidad> **para** <valor esperado>.
- **Feature:** FT-…
- **Criterio de éxito:** <cómo se comprueba que la necesidad queda cubierta>
