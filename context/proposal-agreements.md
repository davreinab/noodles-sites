<!-- vigencia
  autoridad: acuerdo GB Foods ↔ Multiplica (alcance y presupuesto: Sergio García ↔ Alex Castellote)
  confirmado: ⬜ TODO — fecha ISO de la última vez que alguien dijo «esto sigue siendo verdad»
  estado: pendiente-de-confirmar
  Las reglas de PROPIEDAD no caducan (un identificador no cambia de naturaleza). Las de
  DECISIÓN sí: caducan a los 6 meses de «confirmado» y la auditoría avisa, no bloquea.
-->

# Propuesta y acuerdos — GB Noodles · Microsites

Lo que se ha **comprometido**: qué se entrega, hasta dónde llega el trabajo, quién hace cada
cosa y bajo qué restricciones. Su primer origen suele ser la propuesta comercial; a partir de
ahí crece con lo que se vaya acordando, que es lo normal.

**No es la propuesta.** Es lo vigente hoy. La propuesta es la primera entrada del registro de
cambios del final, no el contenido de este archivo.

**No confundir con `project-context.md`.** Aquel describe **el producto** —qué es, qué debe
permitir, qué entra en la fase—; este describe **el encargo**: la porción de trabajo sobre ese
producto que alguien acordó y que tiene fecha, precio y límites. Un producto dura más que un
encargo: habrá una fase siguiente, un contrato nuevo, un addendum, y `project-context.md`
seguirá siendo el mismo.

> **Regla: lo acordado es la autoridad más alta del contexto.** Si un requisito, una pantalla
> o una propuesta de diseño choca con algo de este documento, gana este documento. Cambiarlo
> **no es una decisión de diseño: es una renegociación**, y se anota abajo con fecha y quién
> la acordó. Una IA puede proponer el cambio; no puede aplicarlo.

Lo que **no** entra aquí: el calendario y la duración de las fases —envejecen en cuanto se
mueve una fecha y no cambian ninguna decisión de diseño— y el argumentario de venta. Entra el
compromiso, no la frase que lo vendía.

---

## Fuente

- **Propuesta inicial, 20/04/2026** (WordPress multisite para 5 marcas). Versión y documento
  firmado: ⬜ TODO — no consta en el repo.
- **División en dos fases, 13/05/2026**, a petición del cliente (ver registro de cambios).
- Extraído de `noodles/context/traspaso-microsites.md` §6 (2026-10-07), que condensa el repo
  de la Fase 1. Detalle de correos en [`correo-cliente.md`](./correo-cliente.md).
- **No hay importes confirmados por escrito para cada fase.**

## Entregables

Qué se ha prometido entregar y en qué forma. El formato importa tanto como el contenido: un
documento funcional «en el formato acordado» puede no ser `specs.md` —que tiene su propio
formato— sino una exportación a partir de él.

| ID | Entregable | Formato | Estado |
|---|---|---|---|
| E-01 | Webs completas de marca sobre WordPress multisite con una librería de componentes | ⬜ TODO | comprometido (Fase 2, Q1 2027) |
| E-02 | Pop-up de feedback del consumidor | ⬜ TODO | comprometido (Fase 2, acuerdo 13/05/2026) |
| E-03 | Migración de contenidos (100 h en la propuesta inicial) | ⬜ TODO | ⬜ TODO — revisar: incluido en la propuesta del 20/04; su reparto tras la división en fases no consta |
| E-04 | Assessment | ⬜ TODO | ⬜ TODO — revisar: igual que E-03 |
| E-05 | Iconografía e ilustración específicas | ⬜ TODO | opcional (se cotiza aparte) |
| E-06 | Mantenimiento (1.950 €/mes para las 5 webs, revisable) | ⬜ TODO | opcional (fuera del presupuesto del proyecto) |

- **Formato** — en qué se entrega y dónde se acordó. `⬜ TODO — kickoff` si la propuesta se
  compromete a acordarlo más adelante.
- **Estado** — `comprometido` · `opcional` (contratable aparte, no incluido) · `entregado
  (fecha)` · *retirado (fecha · motivo)*.

## Qué entra y qué no

### Entra
- Propuesta inicial: 5 marcas y 6 combinaciones de mercado e idioma.
- Sitemap: [`user-flow.md § Pantallas`](./user-flow.md), según el traspaso del 2026-10-07. Que
  esa lista esté **cerrada**: ⬜ TODO — el cliente no ha validado la UX de Sites.

### No entra
Según el traspaso (§6); las palabras literales del acuerdo: ⬜ TODO.
- Producir el contenido de recetas.
- Fotografía o variantes de pack multimarca, salvo presupuesto extra.
- SEO y estrategia de analítica.
- Crear marcas nuevas.
- Mr. Cheng's (SE/FI).

## Responsabilidades y dependencias

Lo que hace la otra parte, y qué pasa si no lo hace. Una dependencia externa sin dueño
escrito es un bloqueo que aparece el día que bloquea.

| Qué | Quién | Si no ocurre |
|---|---|---|
| Feedback y validación de la UX de Sites | GB Foods (Martina Colombo) | Bloquea el desarrollo |
| Assets de marca: logos vectoriales originales, fuentes, fotos (no hay brand book) | GB Foods | Se trabaja con placeholders y se prevé un swap |
| Traducciones de los textos base (en inglés) | Cada país | ⬜ TODO |
| Fichas técnicas de producto por país (plantilla o Excel compartido) | GB Foods (cada país) | ⬜ TODO |
| Validación de los gráficos nutricionales | Equipo de nutrición de GB Foods | ⬜ TODO |
| Especificaciones de GA4, GTM y data layer | GB Foods | ⬜ TODO |
| Infraestructura y despliegue en el cloud de GB Foods (Azure/CDN) | GB Foods (sesión con Pablo pendiente) | No consta el destino de producción |
| Formularios externos de contacto y de Calidad | GB Foods | ⬜ TODO |
| Organización de concursos | Agencias externas (p. ej. PS21) | ⬜ TODO |

## Research acordado

Cuánta investigación se ha comprometido y con qué forma: muestra, segmentos, modalidad, quién
capta a los participantes, qué se entrega de cada sesión.

Importa más de lo que parece: cuando [`synthesis.md § Hallazgos`](./synthesis.md) declare la
prevalencia de un hallazgo —«5 de 12 participantes»—, **el denominador sale de aquí**. Sin el
alcance escrito, la prevalencia no tiene contra qué compararse.

⬜ TODO — el traspaso no menciona research comprometido. El módulo de investigación no está activo en este repo (decisión 2026-10-07 · David Reina).

## Restricciones del encargo

Lo que este encargo **puede y no puede hacer**, aunque técnicamente fuera posible. Son límites
negociados, no reglas del sistema: por eso viven aquí y no en `design.md`, cuyas reglas
describen el design system y no el trabajo que se hace sobre él.

Ejemplos del tipo de restricción que va aquí: que solo se puedan componer componentes
existentes y no crear nuevos; que lo nuevo se entregue sin color; que no se toque cierta
parte del producto; que se use una tecnología concreta.

- Plataforma: WordPress multisite, reutilizando la base o el tema de gallinablanca.es.
- GDPR y estándares de seguridad de GB Foods; despliegue en su cloud (Azure/CDN).
- GA4, GTM y data layer desde el inicio, con las especificaciones del cliente.
- Responsive y mobile-first.
(Fuente: traspaso §2.)

## Cómo se cambia lo acordado

Tres cosas hacen que un cambio sea **efectivo**, y si falta una el cambio no existe para el
proyecto:

1. **Que esté escrito aquí.** Un cambio dicho en una reunión y no escrito no existe: los
   agentes leen archivos, no actas. Es lo que más se rompe en la práctica.
2. **Que conste quién lo acordó y dónde.** Por la regla 1e esto es una renegociación, y un
   cambio sin contraparte no es un cambio: es un deseo.
3. **Que se propague.** Lo que citaba el compromiso anterior se marca `⬜ TODO — revisar`,
   porque un requisito escrito bajo el alcance viejo puede haber dejado de ser válido.

Y hay **dos casos que no se tratan igual**:

**Ya está acordado.** Hubo reunión, correo o acta. Se cambia la fila afectada, se añade una
línea al registro con los cuatro datos, y se marca lo que la citaba. Ya es efectivo.

**Todavía no está acordado.** Alguien ha detectado que algo no cuadra —«el research ha sacado
un flujo que no estaba en la lista»—. Eso **no es un cambio, es una propuesta de cambio**: la
fila afectada se marca `⬜ TODO — revisar` con el motivo, queda visible y listada hasta que
alguien lo negocie, y **el registro de abajo no se toca**, porque ahí solo entra lo acordado.

La distinción es justo por donde se cuela el alcance: alguien detecta una necesidad real, se
pone a resolverla, y tres semanas después nadie sabe si eso estaba contratado.

> **Una IA no aplica un cambio aquí solo porque se lo pidan.** Si alguien dice «quita esa
> página del alcance» sin más, la respuesta no es hacerlo: es preguntar **quién lo acordó y
> dónde**. Sin eso, la regla 1e sería decorativa — bastaría con pedirlo para saltársela.

## Registro de cambios

Solo crece, y solo entra **lo acordado**. La propuesta original es la primera fila; cada
acuerdo posterior añade otra.

Aquí el estado actual no basta, porque la pregunta que llega tres meses después no es «¿qué
alcance tenemos?» sino «¿por qué estamos haciendo esto, si no estaba en la propuesta?». Para
responder eso hace falta la **secuencia**, no la foto.

| Fecha | Qué cambió | Quién lo acordó | Dónde se acordó |
|---|---|---|---|
| 2026-04-20 | Versión inicial: WordPress multisite con librería de componentes, 5 marcas y 6 combinaciones de mercado e idioma, 4 meses; 90.000 € + ~18.000 € de traducciones (según el resumen de Read AI); incluye 100 h de migración de contenidos y un assessment | ⬜ TODO | Propuesta inicial |
| 2026-05-13 | El cliente no puede absorber el coste en 2026: se divide en Fase 1 (landing 2026) y Fase 2 (webs completas en Q1 2027, con pop-up de feedback del consumidor), cada una con presupuesto propio. Presupuesto total de referencia ~95.860 €, pago fraccionado (25% al entregar el diseño). Iconografía e ilustración se cotizan aparte. Sin importes por fase confirmados por escrito | GB Foods ↔ Multiplica (⬜ TODO — quién exactamente) | ⬜ TODO |
