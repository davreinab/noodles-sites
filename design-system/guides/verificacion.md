# Verificación contra el maestro  ✅  (antes de usar un componente en una pantalla)

> Guía de `design-system/design.md`: se lee solo cuando la tarea lo pide (la tabla de «Enrutado» de `design.md` dice cuándo).

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
2. **Comparar con el CSS** de las clases del contrato (`code.classes` en
   `css/components.css`): mismos tokens, mismos modificadores por variante, mismas medidas.
3. **Corregir el CSS** donde no cuadre. Un token distinto del que liga el maestro es un error, no
   una interpretación.
4. **Actualizar la ficha** (`docs/components/<slug>.md` o `docs/patterns/<slug>.md`): ejemplo con las
   clases reales y una muestra por variante comprobada; propósito y accesibilidad si faltan. **El
   «Ejemplo de código» cubre cada valor de cada eje de variante y cada propiedad booleana del contrato**
   (la library enseña ese ejemplo, y una muestra parcial es una muestra sesgada): si alguno no sale, o se
   añade al ejemplo (el campo «Ejemplo de código» de la ficha `.md`), o se declara con su motivo en
   `ds-fidelity.config.json → coverageIgnore.components.<slug>` (`{"eje=valor": "motivo", …}`, o una lista
   si no hace falta motivo): esa es la justificación, queda en git y se puede revisar. Mientras la
   cobertura no esté cubierta ni justificada, **la verificación no está completa**: `ds-fidelity.py`
   lo avisa como `variant-not-in-example` y la ficha de la library lo dice en su cabecera. Para que
   `ds-fidelity` sepa qué clase representa cada valor se usa la convención `.<base>--<valor>`; lo que no
   se deduce así se declara en `ds-fidelity.config.json → modifiers.<slug>` (`{"propiedad": {"valor":
   ".clase"}}`; en las booleanas el valor es `true`), nunca editando el schema, que es un archivo
   generado. **No todo estado es una clase.** `modifiers` admite también:
   un atributo en el elemento raíz (`"[data-state=\"running\"]"`); un atributo o una clase en un elemento
   interno (`{"target": ".field__control", "add": "[aria-invalid=\"true\"]"}`, con un selector CSS simple:
   etiqueta, `.clase`, `#id` o `[atributo]`, sin combinadores; se aplica al primero que case); y una parte
   interna que se muestra u oculta (`{"target": ".modal__footer", "presence": true}`: la muestra `true` es el
   ejemplo tal cual y la `false`, el ejemplo sin ese elemento). La galería «Todas las variantes» pinta cada
   estado sobre el elemento que toque y no puede haber dos valores del mismo atributo; la cobertura cuenta
   un estado como visible si algún elemento que case lo lleva. En un ejemplo con **un único control**
   (`input`, `select`, `textarea` o `button`), las booleanas `disabled`, `error` o `invalid` y `required` se
   deducen solas (`[disabled]`, `[aria-invalid="true"]`, `[required]`); con más de un control no se deduce.
   Un estado que no se puede pintar por su naturaleza (el desplegado de un `<select>` nativo) se declara en
   `coverageIgnore.components.<slug>` con su motivo, y la galería lo enseña en su nota. Una variante sin forma
   conocida de representarla queda «sin comprobar» (informativo). Si un
   estado cambia la **estructura** del componente y no solo el estilo (un campo relleno que lleva un
   badge de código además del texto), declararlo en `code.stateAnatomy` del schema
   (`when`: selector del caso en la pantalla; `require`: lo que debe existir dentro; `why`: la frase
   del aviso). Es un bloque manual que el sync conserva, y es lo único que permite detectar en una
   pantalla un marcado con clases válidas pero incompleto.
5. **Marcar `verified`** en el schema: `meta.verification = { "status": "verified", "date": "YYYY-MM-DD",
   "figmaVersion": <el meta.anatomyHash actual>, "variantsChecked": ["type=negative, state=default", …],
   "by": "<persona o agente>" }`. Relanzar `ds-sync.py` para que el ejemplo pase al schema.

`scripts/ds-fidelity.py` comprueba después lo que de esto se puede contrastar sin abrir Figma: tokens
que el maestro liga y el CSS no usa, variantes declaradas sin modificador CSS, clases del ejemplo que no
existen, imágenes externas en los ejemplos, variantes del contrato que el ejemplo no muestra, pantallas
que usan contratos sin verificar y, en las pantallas, la anatomía por estado que declara
`code.stateAnatomy`. Resume
cuántos contratos están en cada estado. Todo nace como aviso; el proyecto decide qué sube a error en
`scripts/ds-fidelity.config.json`. **El contraste AA** (`contrast-below-aa`) mide cada pareja
texto/fondo del CSS de cada componente en claro y oscuro y avisa en cada commit; la library la enseña en
rojo. AA sigue siendo obligatorio: un aviso de contraste se arregla en Figma con propuesta, no se ignora.
No bloquea por defecto porque el arreglo suele ser un color de marca. Si el proyecto quiere bloquear, lo
sube a `"error"` en `severity`; entonces una pareja que se está arreglando puede ir a `contrastExceptions`
atada a su propuesta (aviso mientras esté pendiente, error en cuanto se aplica o se rechaza). El contraste
no se apunta a mano en la ficha.

Si un maestro desaparece de la librería (se borró o se republicó con otra key), el sync lo marca
`stale` con motivo «maestro no encontrado». Cómo reenlazar las instancias huérfanas en Figma está en
`figma.md § 6`.

## Informe de cierre de pantallas

Dos normas para cualquier pantalla, flujo o landing que se genere en `UI/`:

1. **Cada componente del DS que se coloca en una pantalla lleva `data-ds="<slug>"` en su elemento raíz.**
   Es lo que permite saber con certeza qué piezas usa la pantalla; una clase sola también se detecta, pero
   es una pista, no una declaración. Se cuenta **por elemento**, no por componente: con diez botones y uno
   marcado, quedan nueve por marcar. También cuenta el HTML que escribe un script (un icono que cambia al
   pulsar). Y el `data-ds` tiene que ser el del elemento: `<section class="faq" data-ds="faq-list">` se avisa
   (`screen-data-ds-mismatch`), porque el slug existe pero ese elemento no es esa pieza.
2. **Al terminar una pantalla o un flujo se ejecuta el informe y se entrega**:
   `python3 scripts/screen-report.py UI/<pantalla>.html [más archivos o carpetas]`. Sale de los datos (el
   HTML, los contratos, las propuestas y `token-audit.py`), nunca de memoria. Por pantalla cuenta:
   componentes del DS con su estado (verificado, sin verificar, obsoleto) y si llevan `data-ds`; piezas
   internas de Figma; módulos nuevos señalizados; overrides enlazados y el estado de su propuesta; clases
   que `components.css` no define (huecos del DS o módulos sin señalizar) y los errores y avisos de
   `token-audit`. Termina con «Lo accionable». Quien lo entrega resume ese bloque: qué contratos hay que
   verificar, dónde falta `data-ds`, qué piezas internas hay que sustituir, qué overrides siguen vivos y
   qué clases ajenas quedan.

La marca que el proyecto use para «nuevo módulo» (algo que aún no es del DS) se declara en
`scripts/screen-report.config.json → newModuleClasses`; vacía por defecto. `ds-fidelity.py` avisa de las pantallas
con elementos sin `data-ds` (`screen-without-data-ds`, una línea por pantalla con el número y la lista) y de los
`data-ds` que no corresponden al elemento (`screen-data-ds-mismatch`).
