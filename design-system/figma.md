# GB Noodles · Microsites · Pintar en Figma — procedimiento y API

> **Qué es este archivo.** `design.md` dice **qué reglas cumplir** en Figma. Este dice **cómo
> hacerlo**: en qué orden, con qué llamadas y con qué errores conocidos de la API. Sin él, dos
> agentes pueden cumplir todas las reglas y entregar estructuras distintas.
>
> Se lee **antes de escribir nada en Figma**, junto a `design.md § Reglas duras en Figma`.

**Vía única:** el MCP oficial de Figma. `use_figma` ejecuta código en el contexto del archivo y
da acceso a toda la API de plugin. Las comprobaciones previas (identidad, acceso a las fuentes)
están en `design.md § Sync`.

---

## 1. El orden de trabajo

Siempre el mismo, y cada paso se confirma antes del siguiente.

1. **Leer antes de escribir.** Variables, estilos y componentes que ya existen. **Nunca se
   inventa un valor**: si no existe, se crea como variable primero (regla 2 de `design.md`).
2. **Comprobar qué se puede reutilizar.** Si el componente ya existe, se instancia; no se
   reconstruye. Buscar por nombre de catálogo antes de crear nada.
3. **Tipografía antes que componentes.** Es puerta previa: sin una tipografía aprobada para
   escritorio y móvil no se construyen componentes (`design.md § Tipografía`).
4. **Estructura antes que contenido.** Primero los frames y su Auto Layout; después los textos y
   los rellenos; al final los efectos y los bindings. Son tres llamadas, no una.
5. **Capturar y confirmar.** Una captura después de cada frame antes de seguir. Un error de
   estructura visto al tercer frame cuesta tres veces más.
6. **Declarar la accesibilidad antes de cerrar.** Rol, de dónde sale el nombre, qué se anuncia
   al cambiar de estado, qué teclas lo operan y qué se oculta por decorativo. No es un repaso
   posterior: si no se sabe responder, el componente no está terminado (regla 8b).
7. **Cerrar con el sync.** Toda sesión que cambie algo en Figma termina ejecutando el protocolo
   de `design.md § Sync`. Ningún componente se queda sin su contrato.

**Dimensiones.** No se inventan anchos ni altos. Las dimensiones estructurales salen de la
colección `Layout` y los espaciados de `Spacing`. Lo único que es dato de plataforma y no
decisión de diseño: en móvil, área segura superior 44 px e inferior 34 px, y objetivo táctil
mínimo 44 px en iOS y 48 px en Android.

---

## 2. Reglas de la API que fallan en silencio

Esto no es estilo: es cómo se comporta la API de Figma. Saltárselas no da error, da un
resultado incorrecto que nadie ve hasta que lo abre un diseñador.

### 2.1 · Las APIs async son obligatorias

Las versiones síncronas están deprecadas y **fallan en silencio**.

| Deprecado, no usar | Correcto, siempre |
|---|---|
| `figma.currentPage = x` | `await figma.setCurrentPageAsync(x)` |
| `figma.getNodeById(id)` | `await figma.getNodeByIdAsync(id)` |
| `figma.getVariableById(id)` | `await figma.variables.getVariableByIdAsync(id)` |
| `node.exportAsync(...)` sin await | `await node.exportAsync(...)` |
| `figma.loadFontAsync(...)` sin await | `await figma.loadFontAsync({family, style})` |

Regla simple: si el método acaba en `Async` o devuelve una promesa, lleva `await`.

### 2.2 · Los efectos necesitan `blendMode`, y `spread` no existe

Sin `blendMode` la sombra **no se aplica** y no avisa. `spread` solo existe en la API REST, no
en la de plugin: incluirlo invalida el efecto.

```javascript
// correcto
node.effects = [{ type: "DROP_SHADOW", color: {r:0,g:0,b:0,a:0.25},
                  offset: {x:0,y:4}, radius: 8, blendMode: "NORMAL", visible: true }];
```

| Tipo | Propiedades válidas |
|---|---|
| `DROP_SHADOW` · `INNER_SHADOW` | `type`, `color`, `offset`, `radius`, **`blendMode`**, `visible` |
| `LAYER_BLUR` · `BACKGROUND_BLUR` | `type`, `radius`, `visible` |

Recuerda que la elevación vive como **effect style**, no como variable (`design.md § Iconos,
capas, motion y elevación`).

### 2.3 · Las variables se bindean dentro del paint

`setBoundVariable("fills", v)` **no funciona**. El binding va dentro del objeto de relleno:

```javascript
const v = await figma.variables.getVariableByIdAsync(id);
node.fills = [{ type: "SOLID", color: {r:0.2,g:0.4,b:1},
                boundVariables: { color: { type: "VARIABLE_ALIAS", id: v.id } } }];
```

El color literal que se pone al lado es el de respaldo: el que manda es el binding. Y como pide
la regla 1 de `design.md`, **toda propiedad bindeable lleva su variable**.

### 2.4 · Los enums de tamaño no son los mismos

```javascript
frame.primaryAxisSizingMode  = "AUTO" | "FIXED";      // hug | fijo
frame.counterAxisSizingMode  = "AUTO" | "FIXED";
frame.layoutSizingHorizontal = "FILL" | "HUG" | "FIXED";
frame.layoutSizingVertical   = "FILL" | "HUG" | "FIXED";
```

Y `layoutSizing* = "FILL"` **solo surte efecto después de `appendChild`**. Antes se ignora sin
avisar.

### 2.6 · Instanciar un componente de librería puede colgar la sesión

Tres trampas seguidas, y las tres cuestan tiempo real:

1. **Resuelve primero en local.** Si el componente ya está en el archivo abierto, instáncialo
   por su `nodeId` sin pasar por la librería. Importar por clave algo que tienes al lado es la
   diferencia entre responder en dos segundos y esperar quince.
2. **Importar por clave puede colgarse para siempre.** Si Figma no resuelve el componente, la
   llamada no falla: se queda esperando. Ponle un límite de tiempo y falla rápido con un
   mensaje claro, en vez de agotar la sesión.
3. **Un conjunto de variantes no se importa igual.** `importComponentByKeyAsync` **falla** con
   la clave de un `COMPONENT_SET`. Para esos va `importComponentSetByKeyAsync`, y luego se
   instancia su `defaultVariant`.

Y si la clave no es válida, comprueba que no te deja instancias huérfanas a medio crear.

### 2.5 · Un frame en `AUTO` sin contenido colapsa a 0 px

Si un contenedor no tiene hijos con altura, se queda plano. Para controles de formulario, altura
fija desde la variable correspondiente, nunca un número suelto.

---

## 3. Rendimiento: por qué se trocea

Cada llamada a `use_figma` tiene un límite de tiempo y otro de tamaño de respuesta. Pasarse no
devuelve un error claro: devuelve una respuesta truncada o una sesión agotada.

### 3.1 · Tiempos

| Operación | Tiempo a pedir |
|---|---|
| Leer o modificar un nodo simple | 5 s (por defecto) |
| Crear entre 2 y 5 nodos con propiedades | 10 s |
| Frame complejo con hijos | 15 s |
| Cargar fuentes y crear textos | 15 s |
| Exportar imágenes | 20 s |
| Crear varias pantallas | 25 s |
| Más de 10 nodos | 30 s (máximo) |

**Pídelo explícitamente** siempre que haya carga de fuentes, exportación, bucles, iteración
sobre hijos o creación de varios nodos.

### 3.2 · Devuelve lo mínimo

Nunca devuelvas nodos enteros. Filtra a lo que necesitas:

```javascript
// mal: puede exceder el límite y truncarse
return figma.currentPage.findAll();
// bien
return figma.currentPage.findAll().map(n => ({ id: n.id, name: n.name, type: n.type }));
```

Nombres de variables cortos en scripts largos, y sin comentarios extensos dentro del código: lo
que explica el script va en la conversación, no dentro de él.

### 3.3 · Divide

Si una operación es grande, se parte en llamadas: primero la estructura, después el contenido,
al final estilos y efectos. Es la misma norma que el sync aplica a la lectura, por el mismo
motivo: una tanda enorme agota la sesión antes de terminar.

---

## 3-bis. Componer con slots

**El principio, y es el que se incumple:** las variantes manejan la lógica —tamaño, jerarquía,
estado—; los slots manejan el **contenido**. Un slot **nunca sustituye a una variante**: la
complementa, para no acabar creando una variante por cada tipo de contenido posible.

El síntoma de que falta un slot es una lista de variantes como `Contenido=Imagen`,
`Contenido=Lista`, `Contenido=Datos`. Esas tres se colapsan en un slot.

**Cómo se estructura.** El contenedor del slot es un frame con Auto Layout y nombre `slot-*`,
como cualquier otra capa (kebab-case, regla de nomenclatura). Dentro va **contenido por
defecto**, para que el componente no se vea vacío en la librería, y se declaran las
**instancias preferidas** que tienen sentido ahí.

| Componente | Qué va en slot | Qué sigue siendo variante |
|---|---|---|
| Card | cuerpo y zona de acciones | tamaño y estado |
| Modal | cabecera, cuerpo y pie | tamaño y tipo de pie |
| Fila de lista | contenido principal y accesorio | estado y densidad |
| Navegación | grupo de elementos | orientación y estado |

**En el contrato.** Cada slot se declara en `api.slots` del schema del componente: su nombre,
qué admite y cuál es su contenido por defecto. Si el archivo de Figma no soporta slots nativos,
se dice en el contrato y se compone con instancias anidadas; lo que no vale es dejarlo sin
declarar y que cada quien lo resuelva como pueda.

---

## 3-ter. Migrar a slots una librería que ya existe

La sección anterior dice cómo **construir** con slots. Esta, cómo **pasar** a slots una librería
que no los usa, que es el caso de adoptar el DS de un cliente. Todo se hace por `use_figma`, con
la API de plugin estándar: el MCP oficial lo permite sin herramientas aparte.

**Cuándo no se hace.** En modo `preserve-existing` no se migra nada: los candidatos se reportan
y ahí acaba. Migrar cambia la API de los componentes, así que exige la decisión de reestructurar
y una propuesta aprobada en `proposals/` antes de tocar el archivo.

**1. Detectar candidatos (solo lectura).** Dos síntomas, y la auditoría los reporta como
hallazgo `assisted` (`design.md § Auditoría del DS en Figma`):

- una propiedad de variante cuyos valores son tipos de contenido (`Contenido=Imagen`,
  `Contenido=Lista`, `Contenido=Datos`);
- varios hijos alternativos en la misma zona, cada uno encendido por una propiedad booleana.

Por cada candidato se anota qué zona sería el slot, qué variantes colapsa y cuántas instancias
lo usan en los archivos consumidores. Ese recuento es el impacto de la propuesta.

**2. Preparar la zona.** El frame que va a ser slot tiene que cumplir tres condiciones, y si no
las cumple se reestructura antes, en un paso aparte que también se captura:

- es **hijo directo** del componente (en un conjunto de variantes, hijo directo de cada variante);
- su `layoutMode` **no es `GRID`**;
- **no está dentro de otro slot**.

**3. Convertir.** La propiedad `SLOT` va en el dueño de las propiedades —el conjunto de variantes,
o el componente si va suelto— y el frame se enlaza en **cada variante**:

```js
const owner = await figma.getNodeByIdAsync(OWNER_ID);   // COMPONENT_SET o COMPONENT suelto
const key = owner.addComponentProperty('slot-contenido', 'SLOT', '',
  { description: 'Cuerpo de la card', preferredValues: [/* instancias preferidas */] });
const variants = owner.type === 'COMPONENT_SET' ? owner.children : [owner];
for (const v of variants) {
  const zona = v.children.find(n => n.type === 'FRAME' && n.name === 'slot-contenido');
  // Fusionar: asignar un objeto nuevo borraría los otros enlaces (p. ej. un booleano en visible)
  zona.componentPropertyReferences = { ...zona.componentPropertyReferences, slotContentId: key };
}
// Tras el enlace el frame se llama como la propiedad: por eso la propiedad lleva el prefijo slot-
return { key, variantIds: variants.map(v => v.id) };
```

**Al enlazar, Figma renombra el frame con el nombre de la propiedad.** Por eso **la propiedad se
llama igual que la capa, con el prefijo `slot-`** (`slot-contenido`): si se llamara `contenido`,
la capa perdería el prefijo y dejaría de cumplir la norma de la sección anterior. El
nodo sigue siendo `FRAME` dentro del componente y aparece como `SLOT` en las instancias. Las
instancias que ya existían reciben el slot sin hacer nada, con su contenido intacto.

`SLOT` no admite valor por defecto (de ahí el `''`): el contenido por defecto es lo que ya hay
dentro del frame. Para un slot nuevo, sin frame previo, `component.createSlot()` crea el nodo y
la propiedad a la vez; no recibe argumentos, nace como `Slot`, y renombrar el nodo renombra la
propiedad: se renombra a `slot-*` justo después de crearlo. Un slot no admite `layoutMode = 'GRID'`: Figma lo rechaza.

**4. Rellenar desde una instancia.** `setProperties()` **no admite slots**: falla con «Slot
component property values cannot be edited». Se busca el nodo `SLOT` dentro de la instancia y se le añade contenido
como a cualquier frame; `resetSlot()` lo devuelve al contenido por defecto.

**5. Las variantes que sobran no se borran en la misma pasada.** Borrar una variante deja
huérfanas sus instancias en los archivos consumidores. Se marcan como obsoletas en
`schemas/governance/lifecycle.json`, con el slot como sustituto, y se retiran cuando el
registro de retiradas lo permita.

**6. Cerrar.** Captura de cada componente migrado, una instancia de prueba rellenada y vaciada,
y el sync: el contrato pasa a declarar el slot en `api.slots` y la variante colapsada aparece como
obsoleta.

---

## 4. Lo que no se puede hacer por aquí

- **Comentarios.** Leer o escribir comentarios no existe en la API de plugin; va por la API REST
  y necesita un token aparte. Si hace falta, se dice, no se simula.
- **Variables por REST.** Leer variables por la API REST exige plan Enterprise. Por eso el sync
  las lee con `figma.variables.getLocalVariablesAsync()` dentro de `use_figma`.
- **Anotaciones.** Si la versión de Figma no las expone, se guarda el metadato con
  `node.setPluginData()` y se declara en el contrato del componente.

---

## 5. Lista de errores conocidos

Antes de dar por buena una sesión de canvas, repasa que no hayas hecho ninguna de estas:

- Usar una API síncrona existiendo la versión async.
- Omitir `blendMode` en una sombra, o incluir `spread`.
- Bindear con `setBoundVariable` en vez de hacerlo dentro del paint.
- Mezclar los enums de sizing, o poner `FILL` antes de `appendChild`.
- Dejar un frame en `AUTO` sin contenido.
- Dejar el tiempo por defecto en una operación larga.
- Devolver nodos completos.
- Dejar una capa sin nombre o con nombre genérico.
- Escribir un valor crudo existiendo variable.
- Crear un componente que ya existía en el sistema.
- Importar por clave un componente que ya estaba en el archivo, o importar un conjunto de variantes con la llamada de componente suelto.
- Rellenar un slot con `setProperties()`, nombrar una propiedad `SLOT` sin el prefijo `slot-`, o borrar en la misma pasada las variantes que un slot sustituye.
- Ligar a una misma propiedad `TEXT` textos de variantes con formato distinto (estilo, subrayado). Al ligarla, Figma unifica caracteres y pisa el formato de cada variante; y cualquier retoque posterior se propaga. Si las variantes difieren en formato, no se usa propiedad de texto; si comparten formato, el texto inicial debe coincidir con el valor por defecto de la propiedad *antes* de ligarla (aprendido en el Link, 2026-10-07).
- Pintar con variable un vector dentro de una instancia oculta sin pasar color base: puede renderizar el color base (negro) al mostrarse. Se resuelve el valor con `variable.resolveForConsumer(node)`, se usa como color base del paint ligado y se pinta con la instancia visible un momento (aprendido en Button y Chip, 2026-10-07).

## 6. Reenlazar instancias cuyo maestro desapareció

Cuando el sync marca un contrato `stale` con motivo «maestro no encontrado», el componente se borró
de la librería o se republicó con otra key. Las instancias que lo usaban en las pantallas de Figma
siguen vivas pero huérfanas: conservan el aspecto y pierden el vínculo. Para reenlazarlas:

1. **Buscar el sustituto por nombre** en las librerías disponibles (`figma.teamLibrary` o la búsqueda
   del MCP), y confirmar con el usuario cuál es: un nombre igual no garantiza el mismo componente.
2. **Comprobar que la variante coincide** (mismos ejes y valores en `variantProperties`). Si el
   sustituto no tiene la variante, se anota y no se fuerza.
3. **Reenlazar con `swapComponent`** sobre cada instancia, conservando propiedades de componente,
   textos, imágenes y tamaño: se leen antes del cambio y se vuelven a aplicar después, porque el swap
   no garantiza mantenerlos todos.
4. **Verificar después**: la instancia reenlazada se compara con el maestro nuevo (sección
   «Verificación contra el maestro» de `design.md`) y el contrato vuelve a `verified` solo si cuadra.
5. **Avisar antes de tocar** de todo lo que no cuadre (variantes ausentes, textos que se perderían,
   tamaños distintos). Reenlazar es escribir en Figma: entra en el techo de autonomía como cualquier
   otra escritura y nunca se hace en lote sin aprobación.
