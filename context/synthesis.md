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

> **Origen de esta cadena (2026-10-07):** el proyecto no tiene módulo de investigación. Los
> hallazgos salen de lo que afirma el cliente en el traspaso y de los perfiles definidos por el
> proyecto (hipótesis), y lo dicen en su prevalencia. Quedan fuera las landing pages y los temas
> sin definir de [`user-flow.md § Elementos sin definir`](./user-flow.md).

## Hallazgos
Lo que la evidencia dice **cruzando fuentes**. Una observación suelta (`R-… §O-n`) o un dato
suelto (`A-… §D-n`) son lo que vio una persona o midió una herramienta; un hallazgo es lo que
sostienen varios a la vez, con su prevalencia dicha en voz alta.

Es el escalón que falta entre registrar y decidir. Sin él se salta de «un participante dijo
esto» a «el producto tendrá esta pantalla», y por el camino se pierde cuánta gente, en qué
tarea y qué sigue sin saberse — que es justo lo que alguien preguntará dentro de seis meses.

| ID | Hallazgo | Prevalencia | Origen | Qué queda sin confirmar |
|---|---|---|---|---|
| H-01 | Las webs locales de cada país están dispersas y son inconsistentes, tienen muy poco tráfico y las incidencias tardan en resolverse. | 1 de 1 fuentes · voz del cliente · 0 usuarios consultados | Traspaso §2 · project-context § Problema actual | Volumen de tráfico y coste actual por país |
| H-02 | El relanzamiento con fórmula 100 % natural necesita dar *reassurance* sobre la naturalidad, y la transparencia tiene que mostrarse en grande, no en letra pequeña. | 2 de 2 fuentes (traspaso §3 y §4) · voz del cliente · 0 usuarios consultados | Traspaso §3, §4 · OBJ-01 | Si el público lo percibe como creíble |
| H-03 | Una parte del público quiere ver los ingredientes desglosados desde el primer impacto (P-01). | 1 de 1 fuentes · voz del cliente · 0 usuarios consultados (perfil hipótesis) | Traspaso §4 · users.md P-01 | Que el perfil exista y su peso en cada mercado |
| H-04 | Otra parte quiere comer en menos de 5 minutos algo equilibrado, busca recetas para «hackear» el noodle y saber dónde comprar (P-02). | 1 de 1 fuentes · voz del cliente · 0 usuarios consultados (perfil hipótesis) | Traspaso §4 · users.md P-02 | Que el perfil exista y su peso en cada mercado |
| H-05 | La web debe recibir los picos de campañas y el tráfico de social hacia recetas y concursos; sin campaña, la prioridad es producto y después recetas. | 1 de 1 fuentes · voz del cliente · 0 usuarios consultados | Traspaso §3 · OBJ-04 | Volumen y calendario de campañas por mercado |
| H-06 | Las recetas deben generar tráfico recurrente; la bolsa de enero lleva un QR a recetas. | 1 de 1 fuentes · voz del cliente · 0 usuarios consultados | Traspaso §3 · OBJ-05 | Cuántas recetas habrá en el lanzamiento |
| H-07 | Se quiere posicionar en «natural noodles» con un FAQ de naturalidad indexado. | 1 de 1 fuentes · voz del cliente · 0 usuarios consultados | Traspaso §3 · OBJ-03 · OBJ-06 | Preguntas y respuestas definitivas (las valida GB Foods) |
| H-08 | Cada marca y mercado necesita su web con dominio propio, varios idiomas donde toque (Aïki NL/FR) y autonomía del equipo de marketing para publicar y activar campañas. | 1 de 1 fuentes · voz del cliente · 0 usuarios consultados | Traspaso §2 · project-context § Qué debe permitir 1–4 · OBJ-02 | Papel de Daisuki (FR) y proceso editorial de cada país |
| H-09 | Hay obligaciones fijas por país: legales propios (Privacy, Legal notice, Cookies, Lawful basis, Contest rules), bases de los concursos publicadas, contacto por el formulario externo de GB Foods y feedback del consumidor hacia el formulario de Calidad. | 1 de 1 fuentes · voz del cliente · 0 usuarios consultados | Traspaso §5 · business-rules § Legal y § Contacto · proposal-agreements E-02 | Textos legales de cada país y unificación de los dos formularios |

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
| TP-01 | Llegar a la web | Desde el QR del pack, social o un buscador, la persona aterriza en la Home de su marca y mercado. | H-05 · H-08 |
| TP-02 | Comprobar que es natural | Quiere saber qué lleva y qué ya no lleva, y cómo ha cambiado la fórmula. | H-02 · H-03 |
| TP-03 | Elegir producto y sabor | Explora formatos (Cups, Bags, Sauces), líneas y sabores. | H-04 · H-05 |
| TP-04 | Prepararlo | Tiene el producto delante y quiere prepararlo bien y rápido. | H-04 |
| TP-05 | Buscar y cocinar una receta | Busca ideas para comer rápido con el producto. | H-04 · H-06 |
| TP-06 | Participar en una campaña | Llega por una promoción o concurso y quiere participar o ver resultados. | H-05 · H-09 |
| TP-07 | Comprarlo | Quiere saber dónde encontrar el producto en su país. | H-04 |
| TP-08 | Resolver una duda | Busca una respuesta, a menudo desde un buscador. | H-07 |
| TP-09 | Dar su opinión | Quiere enviar una sugerencia o queja de calidad. | H-09 |
| TP-10 | Consultar lo legal o contactar | Revisa privacidad, cookies o bases, o necesita contactar con la marca. | H-09 |
| TP-11 | Publicar y activar (equipo de marketing) | El equipo de cada país publica contenido y lanza campañas sin depender de terceros. | H-01 · H-08 |

## Features
Capacidades concretas que responden a uno o más touchpoints. Cada una se justifica en dos
sentidos: **Responde a** dice de qué evidencia nace, **Contribuye a** a qué objetivo sirve
([`objectives.md`](./objectives.md)). Una feature que no puede llenar ninguna de las dos
columnas es una feature que nadie pidió.

| ID | Feature | Responde a | Contribuye a | Decisión | Motivo |
|---|---|---|---|---|---|
| FT-01 | Home orientada a la acción principal: la campaña activa o, sin campaña, producto y después recetas | TP-01 | OBJ-04 | in fase 2 | Traspaso §3 y §7 |
| FT-02 | Página de la fórmula natural, con su FAQ | TP-02 | OBJ-01 | in fase 2 | Sitemap del traspaso §7 |
| FT-03 | Librería de producto con navegación en tres niveles (tipo → línea → sabor) | TP-03 | OBJ-04 | in fase 2 | Traspaso §7 |
| FT-04 | Ficha de producto con ingredientes jerarquizados, etiqueta del envase en modal, nutrición visual y alérgenos | TP-02 · TP-03 | OBJ-01 | in fase 2 | Traspaso §7 |
| FT-05 | Preparación con GIF o vídeo y temporizador de 3 minutos | TP-04 | ⬜ TODO | in fase 2 | Traspaso §7 |
| FT-06 | Librería y página de receta | TP-05 | OBJ-05 | in fase 2 | Traspaso §3 y §7 |
| FT-07 | Concursos con tres modelos (estructura propia, iframe o enlace externo); la librería es opcional | TP-06 | OBJ-04 | in fase 2 | Traspaso §7 |
| FT-08 | Dónde comprar por país | TP-07 | ⬜ TODO | in fase 2 | Traspaso §4 y §7 |
| FT-09 | FAQS como página indexada | TP-08 | OBJ-06 | in fase 2 | Traspaso §3 y §7 |
| FT-10 | Suggestion bubble hacia el formulario externo de Calidad | TP-09 | ⬜ TODO | in fase 2 | Traspaso §5 y §7 · E-02 |
| FT-11 | Legales por país y contacto externo | TP-10 | OBJ-02 | in fase 2 | Traspaso §5 y §7 |
| FT-12 | Navegación común: navbar que se oculta al bajar, footer y bottom footer legal | TP-01 | OBJ-02 | in fase 2 | Traspaso §7 |
| FT-13 | Plataforma multimarca y multiidioma con gestión autónoma del contenido | TP-11 | OBJ-02 | in fase 2 | Traspaso §2 · project-context |
| FT-14 | Medición con GA4, GTM y data layer desde el inicio | TP-11 | ⬜ TODO | in fase 2 | Traspaso §2 · restricciones del encargo |

## User stories
Una por necesidad, no por función. Formato: quién, en qué circunstancia, qué y para qué.

### US-01 · Ir directo a lo importante
- **Como** quien llega a la web, **cuando** llega desde el pack, social o un buscador, **quiero** ver primero la campaña activa o, si no hay, los productos y después las recetas **para** no perderse y actuar en segundos.
- **Feature:** FT-01 · FT-12
- **Criterio de éxito:** Desde la Home se alcanza la campaña activa (o la Product library si no la hay) con una sola acción.

### US-02 · Comprobar la naturalidad
- **Como** persona que quiere transparencia (P-01), **cuando** duda de si la nueva fórmula es de verdad natural, **quiero** ver de forma clara qué ingredientes lleva y cuáles se han quitado, y cómo ha mejorado la fórmula **para** decidir si confía en la marca.
- **Feature:** FT-02 · FT-04
- **Criterio de éxito:** Ingredientes, ingredientes eliminados y mejoras de la fórmula visibles sin desplegar nada y sin letra pequeña.

### US-03 · Encontrar mi sabor
- **Como** persona que explora el catálogo (P-02), **cuando** quiere elegir qué comprar, **quiero** filtrar por formato, línea y sabor **para** llegar a la ficha del producto que busca.
- **Feature:** FT-03
- **Criterio de éxito:** Cualquier ficha se alcanza en tres niveles como máximo y ningún filtro deja la lista vacía.

### US-04 · Saber qué como
- **Como** persona que va a comprar o ya tiene el producto (P-01 · P-02), **cuando** consulta un producto concreto, **quiero** ver sus ingredientes jerarquizados, alérgenos, nutrición y la etiqueta del envase **para** saber exactamente qué come.
- **Feature:** FT-04
- **Criterio de éxito:** Los alérgenos se distinguen en el texto y la etiqueta del envase se abre desde la ficha.

### US-05 · Prepararlo bien y rápido
- **Como** persona con poco tiempo (P-02), **cuando** tiene el producto delante, **quiero** seguir los pasos con apoyo visual y un temporizador **para** tenerlo listo en 3 minutos sin dudar.
- **Feature:** FT-05
- **Criterio de éxito:** Pasos visibles con GIF o vídeo y un temporizador de 3 minutos que avisa al terminar.

### US-06 · Hackear el noodle
- **Como** persona que busca ideas rápidas (P-02), **cuando** quiere variar, **quiero** encontrar recetas con los productos y ver ingredientes, nutrición y pasos **para** cocinar algo distinto en poco tiempo.
- **Feature:** FT-06
- **Criterio de éxito:** Desde cualquier receta se ve qué productos usa y se llega a su ficha.

### US-07 · Participar en una campaña
- **Como** quien llega por una promoción, **cuando** ve un concurso activo, **quiero** entender el premio, participar y consultar las bases **para** participar con confianza.
- **Feature:** FT-07 · FT-11
- **Criterio de éxito:** Desde el concurso se llega a participar y a las bases legales; un concurso cerrado muestra su estado.

### US-08 · Comprarlo
- **Como** persona que quiere el producto (P-02), **cuando** no sabe dónde lo venden en su país, **quiero** ver los distribuidores de su país **para** ir a comprarlo.
- **Feature:** FT-08
- **Criterio de éxito:** Los distribuidores mostrados son los del país de la web y enlazan a su sitio.

### US-09 · Resolver mi duda
- **Como** persona con una pregunta, **cuando** busca en Google o en la web, **quiero** encontrar la pregunta y su respuesta **para** resolverla sin contactar.
- **Feature:** FT-09 · FT-02
- **Criterio de éxito:** Las preguntas y respuestas están en el HTML de una página indexable.

### US-10 · Opinar
- **Como** persona que quiere hacer una sugerencia, **cuando** navega por cualquier página, **quiero** acceder siempre a la vía para enviarla **para** que la marca la reciba.
- **Feature:** FT-10
- **Criterio de éxito:** Desde cualquier página se llega al formulario de Calidad.

### US-11 · Saber mis derechos
- **Como** persona que consulta lo legal o quiere contactar, **cuando** está en cualquier página, **quiero** encontrar los textos legales de su país y el contacto **para** entender cómo se tratan sus datos y hablar con la marca.
- **Feature:** FT-11 · FT-12
- **Criterio de éxito:** Los cinco legales del país y el contacto están en el pie de todas las páginas.

### US-12 · Publicar sin depender de nadie
- **Como** equipo de marketing de un país, **cuando** tiene que lanzar contenido o una campaña, **quiero** publicar en la web de su marca y en su idioma sin intervención técnica **para** activar campañas rápido en su mercado.
- **Feature:** FT-13 · FT-14
- **Criterio de éxito:** ⬜ TODO — criterio a fijar con GB Foods (proceso editorial y tiempos)
