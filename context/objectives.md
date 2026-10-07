<!-- vigencia
  autoridad: GB Foods (cliente)
  confirmado: ⬜ TODO — fecha ISO de la última vez que alguien dijo «esto sigue siendo verdad»
  estado: pendiente-de-confirmar
  Las reglas de PROPIEDAD no caducan (un identificador no cambia de naturaleza). Las de
  DECISIÓN sí: caducan a los 6 meses de «confirmado» y la auditoría avisa, no bloquea.
-->

# Objetivos y métricas — GB Noodles · Microsites

Para qué existe el proyecto y cómo sabremos si funcionó. Es la cara descendente de
[`synthesis.md`](./synthesis.md): allí una capacidad justifica **de qué evidencia nace**
(`research → touchpoint → feature`), aquí justifica **a qué sirve** (`feature → objetivo`).
Una capacidad que no responde a ninguna de las dos preguntas no debería estar en la fase.

**No confundir con el alcance.** «Que se pueda adjuntar un archivo» describe una capacidad:
eso es alcance y va en [`project-context.md`](./project-context.md). «Que dejen de rechazarse
solicitudes por documentación ilegible» describe un cambio: eso es un objetivo.

**Definir una métrica es una decisión y vive aquí. Medirla es un dato y vive fuera**: en una
medición de [`../analytics/`](../analytics/) (`A-… §D-n`) o, si la evidencia es cualitativa,
en una nota de [`../research/`](../research/) (`R-… §O-n`). Este documento nunca guarda una
serie de valores: guarda qué se mide, cómo y contra qué se compara.

Nada se inventa (regla 1). Un objetivo sin métrica es una intención, no un objetivo: se admite
`⬜ TODO` para no bloquear, pero queda listado como pendiente en cada revisión y nadie lo da
por medible. Los identificadores `OBJ-` y `M-` son estables (regla 5): se asignan una vez, no
se renumeran, y lo que deja de aplicar se marca *retirado* con fecha y motivo.

> Fuente de todo este documento salvo indicación: `noodles/context/traspaso-microsites.md` §3
> (2026-10-07). El proyecto no tiene módulo de investigación: los orígenes son lo que afirma el
> cliente, no evidencia con usuarios.

---

## Objetivos

Qué tiene que cambiar para alguien, no qué tiene que hacer el producto. Van en **dos niveles**,
y la diferencia no es de tamaño sino **de responsabilidad**:

> **El proyecto se compromete con el objetivo de producto y solo contribuye al de negocio.**

Un objetivo de negocio lo mueven diez cosas más —precio, competencia, estacionalidad, la
fuerza comercial—, así que atribuírselo al diseño es falso en los dos sentidos: cuelga
medallas que no toca y también fracasos que no toca. Separarlos es lo que permite decir con
cara seria «la tasa de rechazo bajó del 23 % al 6 %, que era nuestro compromiso; si eso movió
el coste del área, eso ya no lo controlamos solos».

### De negocio

Para qué le sirve esto al cliente. Suelen venir dados y el proyecto no los controla.

| ID | Objetivo | Origen | Se mide con | Dueño | Horizonte |
|---|---|---|---|---|---|
| OBJ-01 | Comunicar el mensaje nº1 del año, «natural noodles»: dar *reassurance* sobre la naturalidad de la fórmula | Cliente (traspaso §3) | ⬜ TODO | ⬜ TODO | ⬜ TODO |
| OBJ-02 | Consistencia de marca, gestión diaria más fácil y activación más rápida en todos los mercados («a scalable platform for Europe») | Cliente (traspaso §3) | ⬜ TODO | ⬜ TODO | ⬜ TODO |
| OBJ-03 | Posicionar en «natural noodles» (SEO/AEO) | Cliente (traspaso §3) | ⬜ TODO | ⬜ TODO | ⬜ TODO |

### De producto

Lo que **este encargo** se compromete a cambiar. Cada uno declara a qué objetivo de negocio
apunta.

| ID | Objetivo | Problema que ataca | Apunta a | Origen | Se mide con | Horizonte |
|---|---|---|---|---|---|---|
| OBJ-04 | La web funciona como **destino de campañas**: recibe los picos promocionales y el tráfico de social hacia recetas y concursos. La acción principal son las campañas activas; sin campaña, producto y después recetas | ⬜ TODO | OBJ-01 · OBJ-02 | Cliente (traspaso §3) | ⬜ TODO | ⬜ TODO |
| OBJ-05 | Las **recetas** generan tráfico recurrente; hay contenido de recetas en el lanzamiento (la bolsa de enero lleva un QR a recetas) | ⬜ TODO | ⬜ TODO | Cliente (traspaso §3) | ⬜ TODO | Lanzamiento, enero 2027 |
| OBJ-06 | Un **FAQ de naturalidad indexado** | ⬜ TODO | OBJ-03 | Cliente (traspaso §3) | ⬜ TODO | ⬜ TODO |

- **Apunta a** — el `OBJ-` de negocio al que sirve. Un objetivo de producto sin objetivo de
  negocio al que apuntar **no es inválido**: muy a menudo el cliente no lo ha dicho. Se marca
  `⬜ TODO` y el hueco queda visible, porque significa que se está diseñando sin saber para
  qué le sirve al negocio, y eso conviene saberlo.
- **Cuidado con el eco.** Si el objetivo de negocio dice «aumentar ingresos» y el de producto
  dice «aumentar ingresos», eso no es alineación: es la misma frase un escalón más abajo. El
  de producto tiene que ser algo que el diseño pueda mover y de lo que el equipo pueda
  responder.
- **Origen** — la nota o medición que sostiene que el problema existe (`R-… §O-n` ·
  `A-… §D-n`), o `⬜ TODO` si todavía es una suposición del equipo. Un objetivo sin origen no
  es inválido: es una apuesta, y conviene que se note.
- **Horizonte** — cuándo se espera ver el cambio. Sin fecha no hay forma de cerrar el bucle.

## Métricas

Una métrica es una definición, no un número. Si dos personas pueden calcularla distinto, aún
no está definida. La que tiene dueño, baseline y meta es lo que en una conversación de negocio
se llama **KPI**; la que solo tiene definición es de apoyo. No hacen falta dos vocabularios:
las columnas ya distinguen una de otra.

| ID | Métrica | Definición exacta | Mide | Lectura | Fuente | Baseline | Meta |
|---|---|---|---|---|---|---|---|
| M-01 | ⬜ TODO | ⬜ TODO | OBJ-… | ⬜ TODO | GA4 / GTM / data layer (según especificaciones del cliente) | ⬜ TODO | ⬜ TODO |

- **Definición exacta** — numerador, denominador, ventana temporal y a quién incluye.
- **Mide** — el `OBJ-` del que cuelga, de cualquiera de los dos niveles.
- **Lectura** — cada cuánto se puede leer y si es *adelantada* o *atrasada*. Las de negocio
  suelen ser atrasadas: te enteras en meses. **Cada objetivo de producto necesita al menos una
  métrica adelantada**, que se pueda leer en semanas, o no hay forma de corregir el rumbo
  mientras dura el proyecto.
- **Fuente** — de dónde sale el dato y quién puede sacarlo.
- **Baseline** — el valor de partida, citando la medición que lo tomó (`A-… §D-n`). Sin
  baseline no se puede afirmar que algo mejoró: marca `⬜ TODO` mientras no exista, y
  `🚫 No existe` si el proceso actual no deja medirlo.
- **Meta** — a dónde se quiere llegar y para cuándo.

## Fuera de objetivo

Lo que este proyecto **no** persigue, aunque parezca cercano. Es el documento al que se vuelve
cuando alguien propone algo razonable que no toca: frena el alcance con un argumento escrito
en vez de con una opinión.

| Qué queda fuera | Por qué | Decidido (fecha · quién) |
|---|---|---|
| Ser el hub diario de comunicación de la marca | «La web no es el centro de la comunicación»: es un destino de campañas | Cliente · fecha ⬜ TODO (traspaso §3) |
| Mr. Cheng's (SE/FI) | Fuera de alcance | ⬜ TODO (traspaso §2) |
