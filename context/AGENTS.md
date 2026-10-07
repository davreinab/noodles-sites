# Contexto funcional — GB Noodles · Microsites · Normas de `context/`

> **Router** del contexto funcional. Corto a propósito: se lee siempre antes de leer, escribir
> o citar cualquier documento de esta carpeta, y decide **qué archivo abrir**. No copies aquí
> el contenido de los demás.

Esta carpeta es la **única fuente de verdad de lo funcional** del producto: qué es, para
quién, qué reglas lo gobiernan, qué datos maneja, qué pantallas y estados tiene, de qué
necesidad nace cada capacidad y qué debe hacer el sistema. La consumen UX, UI, el design
system y desarrollo. Los datos brutos de investigación **no** viven aquí: viven en
[`../research/`](../research/) y aquí se citan.

---

## Enrutado — qué documento abrir según la petición

| Si la petición trata de… | Lee | No leas el resto |
|---|---|---|
| qué es el producto, qué sustituye, **qué debe permitir**, **alcance** | `project-context.md` | — |
| qué se ha **comprometido**: entregables, qué queda fuera, quién hace qué, restricciones del encargo | `proposal-agreements.md` | — |
| «¿esto entra en el proyecto?» · «¿esto lo hacemos nosotros?» | `proposal-agreements.md` primero; si choca con otro documento, **gana este** | no empieces a diseñarlo para comprobarlo |
| **quién** usa el producto: perfil, contexto de uso, frecuencia · y qué puede hacer cada **rol**, si los hay | `users.md` (detalle) · `project-context.md § Usuarios` (tabla resumen) | — |
| una **regla de negocio**, validación, límite, plazo, política | `business-rules.md` | user-flow / specs |
| **cómo se llama** algo aquí, si dos palabras son lo mismo, qué término manda | `glossary.md` | — |
| una **entidad**, un campo, un enum, el estado de un dato | `data-model.md` | — |
| qué **pantallas** hay, cómo se navega, **estados** de pantalla (vacío, error, carga) | `user-flow.md` | — |
| qué dice la evidencia **cruzando fuentes**: un **hallazgo** y su prevalencia | `synthesis.md` | no releas las notas: el hallazgo ya las cita |
| de qué necesidad nace algo: **touchpoint, feature, user story** | `synthesis.md` | — |
| **para qué** existe el proyecto, un **objetivo**, una **métrica**, un baseline, qué queda **fuera de objetivo** | `objectives.md` | — |
| qué **DEBE / NO DEBE** hacer el sistema, un requisito, un escenario | `specs.md` (y su **Origen** en `synthesis.md`) | — |
| el **resultado de la última auditoría** de estos documentos | `reports/context-audit.json` ⚙️ generado; no se edita a mano | — |
| lo que dijo un usuario, un dato de una entrevista, un benchmark | `../research/index.json` primero; después solo la nota y la unidad `O-n` que necesites | no leas todas las notas |
| una **cifra**: cuántos, cuánto tarda, qué porcentaje, el **baseline** de una métrica | `../analytics/index.json` primero; después solo la medición y la unidad `D-n` que necesites | no leas todas las mediciones |
| «apunta esto» / contexto nuevo | sección **Distribución** abajo | — |
| una pregunta cuya respuesta está en `⬜ TODO`, en `🚫 No existe` o no aparece | nada: la respuesta es «no lo sé, no está en el contexto» + dónde debería estar (regla 1c) | no busques la respuesta fuera del repo |
| **cualquier pedido** (requisito, flujo, wireframe, pantalla, texto) | primero los documentos de los que depende; si falta un dato, aviso de que no se puede completar y por qué, antes de empezar (regla 1d) | no empieces a construir para «ver hasta dónde llegas» |
| «¿esto ya se decidió?» antes de proponer algo funcional | el documento de la fila que corresponda, buscando la regla; si no está escrita, no está decidida | — |
| una pantalla o un componente necesita una regla que **no está escrita** | se escribe primero aquí (en su documento) y después se usa; nunca al revés | — |
| **cambió una regla, un rol o un dato** | sección **Cambios** abajo | — |
| comprobar que la carpeta está completa antes de un commit | `python3 scripts/token-audit.py` (comprueba que existen los documentos y sus secciones obligatorias) | — |

> Carga solo el documento que la tarea necesita. Los documentos se enlazan entre sí en vez
> de repetirse: si una regla de negocio afecta a una pantalla, `user-flow.md` la cita, no la
> copia.

---

## Reglas duras (no negociables)

1. **Nada se inventa, y lo que falta se marca.** Cuando al generar o completar contexto
   falte un dato, se deja escrito en el propio `.md`, en la sección exacta donde iría, con
   uno de dos marcadores: `⬜ TODO` si nadie lo ha aportado todavía, o `🚫 No existe` si la
   persona confirmó que ese dato no existe o no aplica (con fecha y quién lo dijo). Nunca se
   rellena con suposiciones, ejemplos «razonables», valores por defecto ni datos de otros
   proyectos. Un hueco visible vale más que un dato falso.
1b. **Lo marcado como inexistente no se rellena después.** Un `🚫 No existe` es una
   afirmación de la persona, no un pendiente: la IA no puede sustituirlo por un dato propio,
   deducirlo de otros documentos ni «completarlo» aunque se lo pidan de forma indirecta.
   Solo la persona puede convertirlo en dato, y entonces se anota el cambio (sección
   **Cambios**).
1c. **Sinceridad ante lo que no está.** Si la persona pregunta por una información que en
   `context/` está en `⬜ TODO`, en `🚫 No existe` o simplemente no aparece, la respuesta es
   «no lo sé, no está en el contexto» seguida de dónde debería estar y qué haría falta para
   tenerlo. No se responde con una estimación ni con lo que «suele ser» en otros productos.
1d. **Una petición que depende de un dato que falta no se completa: se avisa.** Vale para
   cualquier pedido, no solo para preguntas: un requisito, un flujo, un wireframe, una
   pantalla, una tabla de datos, un texto. Antes de empezar, la IA comprueba en `context/`
   los datos de los que depende el pedido. Si alguno está en `⬜ TODO`, en `🚫 No existe` o
   no aparece, lo dice **antes de hacer nada**: «esta petición no se puede completar porque
   falta <dato>, que debería estar en <documento § sección>». Después ofrece dos salidas y
   deja elegir: que la persona aporte el dato ahora, o hacer solo la parte que no depende de
   él, dejando el hueco marcado con `⬜ TODO` en el entregable y en el documento de contexto.
   Lo que nunca hace es rellenar el hueco por su cuenta para poder terminar.
1e. **Lo acordado es la autoridad más alta.** Lo que está en `proposal-agreements.md` —los
   entregables, lo que queda fuera, las responsabilidades de la otra parte y las restricciones
   del encargo— gana sobre cualquier otro documento de esta carpeta. Si un requisito, una
   pantalla o una propuesta de diseño choca con eso, el que cede es el otro. Cambiar lo
   acordado **no es una decisión de diseño: es una renegociación**, se anota en el registro de
   cambios de ese documento con fecha y quién la acordó, y una IA puede proponerla pero nunca
   aplicarla por su cuenta.
2. **Un dato, un archivo.** Cada dato vive en el único documento que le corresponde por la
   tabla de **Distribución**. Si otro documento lo necesita, lo enlaza; no lo copia. Si el
   mismo dato aparece en dos sitios, uno de los dos está mal.
3. **La evidencia se cita, nunca se resume.** Ningún documento de `context/` reinterpreta
   una entrevista, un informe, un benchmark ni una medición. Se cita la nota y la unidad:
   `R-… §O-n` para research, `A-… §D-n` para analítica. La línea entre las dos: si el valor
   se va a volver a medir con el mismo método es analítica, si es un testimonio irrepetible
   es research. La cadena de trazabilidad va en un solo sentido y es obligatoria:
   **nota o medición → hallazgo → touchpoint → feature → user story → requisito.**
   El **hallazgo** es el eslabón que cruza fuentes y declara su prevalencia: sin él se salta
   de lo que dijo una persona a lo que tendrá el producto, y por el camino se pierde cuánta
   gente, en qué tarea y qué sigue sin saberse.
4. **Cada requisito tiene Origen.** Un requisito de `specs.md` sin **Origen** resuelto a una
   user story existente no es normativo. Se admite `⬜ TODO — origen` para no bloquear, pero
   queda listado como pendiente en cada revisión y nadie construye sobre él como si fuera
   firme.
5. **Los identificadores son estables.** `H-`, `TP-`, `FT-`, `US-`, `F-`, `R-`, `A-`, `P-`,
   `E-`, `OBJ-` y `M-` se asignan una vez
   y no se renumeran ni se reutilizan. Lo que deja de aplicar se marca como *retirado* con
   fecha y motivo; no se borra, porque otros documentos lo citan.
6. **Los encabezados de las plantillas son fijos.** Las secciones con las que nace cada
   documento no se renombran ni se eliminan: son las que la auditoría comprueba y las que el
   resto de carpetas enlazan. Se puede añadir una sección; no quitar una.
7. **Ningún documento nuevo sin confirmación.** Crear un `.md` más en `context/` exige el
   acuerdo explícito de la persona, con nombre y propósito. Única excepción: las **notas de
   research**, que se crean siempre como nota nueva en `../research/` (una por fuente) y
   después se propaga a `synthesis.md` lo que aporten.
8. **Los requisitos se escriben para poder comprobarse.** Una frase por requisito, con
   **DEBE**, **NO DEBE** o **PUEDE**, sin detalles de implementación. Cada requisito lleva al
   menos un escenario **Dado / Cuando / Entonces** verificable.
9. **Vocabulario único.** Los nombres de entidades, estados y roles son los de
   `data-model.md` y `users.md`, y el término que manda para cualquier cosa del dominio está
   en `glossary.md`. Todos los documentos, wireframes, pantallas y contratos del design
   system usan exactamente esos nombres. Un sinónimo es un error, y además es un error que no
   se ve: si cada eslabón de la cadena usa una palabra distinta, la trazabilidad **parece**
   correcta y no ata nada.
10. **Las contradicciones no se resuelven en silencio.** Si dos notas de research, dos
    reglas o una regla y un requisito chocan, se lleva a `synthesis.md` como decisión
    explícita (qué se decidió, por qué, con qué origen) o se pregunta a la persona. Nunca se
    elige una versión callando la otra.
11. **Las correcciones repetidas se escriben.** Si la persona corrige lo mismo dos veces en
    lógica, contenido, roles o reglas, es una regla no escrita: se añade en esa misma sesión
    al documento que corresponda, citando la corrección como origen (ver `AGENTS.md` raíz
    § Correcciones repetidas). No se vuelve a preguntar.
12. **El contexto no sale de este proyecto.** Lo aprendido aquí es de este cliente y este
    producto. No se reutiliza en otros repos ni se completa con lo que se sabía de otro
    proyecto. Lo que sea una lección de método, no de producto, se propone al catálogo de
    la skill, no se anota aquí.
13. **Desarrollo consume versiones, no borradores.** Lo que se entrega a desarrollo es el
    estado de `context/` en un commit etiquetado (`context-vN`), no la rama de trabajo. Antes
    de etiquetar, cero `⬜ TODO — origen` en los requisitos que entran en esa versión, o se
    listan explícitamente como fuera de alcance.

---

## Distribución — dónde va cada dato

Cada dato va a **un solo archivo**. Cuando la persona aporte contexto, en el brief o en
cualquier momento posterior, se coloca sin pedir permiso según esta tabla y se le dice dónde
quedó. Si un dato no encaja en ninguna fila, se pregunta ofreciendo los documentos
candidatos y la opción de crear uno nuevo (regla 7).

| Dato | Archivo | Sección |
|---|---|---|
| Qué es, nombre público, qué sustituye | `project-context.md` | Qué es |
| Proceso actual y sus dolores | `project-context.md` | Problema actual |
| Qué debe permitir hacer el producto (capacidades) | `project-context.md` | Qué debe permitir |
| Perfil de usuario: quién es, contexto, frecuencia, restricciones · y su rol si lo hay | `project-context.md` (tabla resumen) + `users.md` (detalle) | Usuarios / Perfiles · Roles y permisos |
| Qué entra y qué no en el producto (capacidades de la fase) | `project-context.md` | Alcance |
| Entregable comprometido y su formato | `proposal-agreements.md` | Entregables |
| Exclusión acordada («queda fuera de este proyecto…») | `proposal-agreements.md` | Qué entra y qué no |
| Lo que hace la otra parte, y de qué depende el proyecto | `proposal-agreements.md` | Responsabilidades y dependencias |
| Muestra, segmentos y modalidad de research comprometidos | `proposal-agreements.md` | Research acordado |
| Límite negociado sobre cómo se puede diseñar o construir | `proposal-agreements.md` | Restricciones del encargo |
| Un cambio de lo acordado en una reunión posterior | `proposal-agreements.md` | Registro de cambios |
| Regla de negocio, validación, política | `business-rules.md` | Reglas generales / Reglas por área |
| Plazo, importe, cupo, vigencia, umbral | `business-rules.md` | Condiciones y límites |
| El término que manda para una cosa, y los sinónimos descartados | `glossary.md` | tabla |
| Entidad, campo, enum, estado de un dato | `data-model.md` | Entidades principales |
| Pantalla, navegación, estado de pantalla | `user-flow.md` | Pantallas / Estados |
| Entrevista, observación, benchmark, informe | `../research/<fecha>-<slug>.md` (nota nueva desde `_nota.template.md`) + `python3 scripts/research-index.py` | Observaciones `O-n` |
| Cifra de analítica, consulta a base de datos, embudo, tiempo de proceso, resultado con porcentajes | `../analytics/<fecha>-<slug>.md` (medición nueva desde `_medicion.template.md`) + `python3 scripts/research-index.py --dir analytics` | Datos `D-n` |
| Lo que la evidencia sostiene cruzando fuentes, con su prevalencia | `synthesis.md` | Hallazgos |
| Touchpoint, feature, user story | `synthesis.md` | Touchpoints / Features / User stories, cada uno con su origen y el objetivo al que sirve |
| Objetivo del proyecto, métrica, baseline, meta, lo que queda fuera de objetivo | `objectives.md` | Objetivos / Métricas / Fuera de objetivo |
| Requisito funcional, escenario | `specs.md` | Requisitos con **Origen** → `US-…` / Escenarios |
| Decisión que resuelve una contradicción | `synthesis.md` | junto a las filas afectadas, con fecha y motivo |
| Descripción corta del proyecto | `../README.md` | cabecera |
| Dirección visual, tono, referencias | `../UX/direction/` | no es contexto funcional |
| Color, medida, componente | Figma → `../design-system/` | no es contexto funcional |

---

## Cambios — cuando algo que ya estaba escrito cambia

> **Si lo que cambia es algo acordado** (un entregable, una exclusión, el research
> comprometido, una restricción del encargo), no basta con esto: ver
> [`proposal-agreements.md § Cómo se cambia lo acordado`](./proposal-agreements.md). Ahí hace
> falta además **quién lo acordó y dónde**, y si todavía nadie lo ha negociado no se aplica:
> se marca (regla 1e).

1. Se cambia **solo en su archivo** (regla 2) y se anota en la misma línea o sección la
   fecha y el origen del cambio (quién lo dijo, en qué sesión o nota).
2. Se buscan los documentos que lo citan (`grep` del identificador o del término) y se
   revisan: un requisito cuya regla de negocio cambió puede dejar de ser válido. Lo que
   quede afectado y sin decidir se marca `⬜ TODO — revisar` con la referencia al cambio.
3. Si el cambio invalida un identificador, se marca *retirado* (regla 5); no se borra.
4. Se avisa a la persona de qué cambió, qué documentos quedaron afectados y qué queda por
   decidir, en lenguaje claro y en las cuatro partes de siempre.

---

## Marcadores

| Marcador | Significa |
|---|---|
| `⬜ TODO` | Nadie lo ha aportado todavía. No se inventa. Si alguien pregunta por ello, la respuesta es «no lo sé». |
| `🚫 No existe (fecha · quién)` | La persona confirmó que ese dato no existe o no aplica. Solo ella puede cambiarlo; la IA nunca lo rellena. |
| `⬜ TODO — origen` | El requisito existe pero aún no traza a una user story. No es normativo. |
| `⬜ TODO — kickoff` | Lo acordado se compromete a **producir** este dato más adelante (p. ej. «los indicadores de éxito se definen en el kickoff»). No es que nadie lo haya aportado: es una obligación con fecha, y se lista como pendiente hasta que se cumpla. |
| `⬜ TODO — revisar` | Un cambio en otro documento puede haberlo invalidado. Pendiente de decisión. |
| *retirado (fecha · motivo)* | Un identificador que dejó de aplicar. Se conserva porque otros lo citan. |

<!-- Este archivo es la fuente de las normas de contexto. Si una norma cambia, se cambia aquí
     y no se duplica en AGENTS.md raíz ni en otras carpetas: ellas enlazan a este archivo. -->
