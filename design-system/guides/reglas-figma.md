# Reglas duras en Figma

> Guía de `design-system/design.md`: se lee solo cuando la tarea lo pide (la tabla de «Enrutado» de `design.md` dice cuándo).

> Estas reglas dicen **qué** debe cumplirse. El **cómo** —orden de trabajo, llamadas,
> errores de la API que fallan en silencio y troceado por rendimiento— está en
> [`figma.md`](./figma.md), y se lee antes de escribir nada en el canvas.


## Protección de sistemas existentes

- Antes de escribir, determina el modo de adopción registrado en el encabezado de `design.md`. Si es
  `preserve-existing` o `pending-inspection`, las reglas estructurales de esta sección
  son referencia para el análisis, no instrucciones de migración.
- En un DS existente y operativo no cambies colecciones, modos, jerarquías, aliases,
  nombres, estilos, keys ni estructura de componentes sin una decisión explícita de
  reestructuración y un plan de migración aprobado.
- En modo `preserve-existing`, todos los documentos y artefactos generados reflejan la
  metodología y nomenclatura reales del DS. Las nuevas variables y componentes siguen
  esas convenciones para no crear dos arquitecturas dentro de la misma librería.
- Presenta las diferencias con este estándar como hallazgos, no como errores que deban
  corregirse automáticamente.
- Completar scopes y descripciones de variables sigue siendo obligatorio en cualquier
  modo, siempre que no cambie identidad, valor, alias, colección, modo ni key.

## Arquitectura de variables de color

- Para un DS nuevo o una reestructuración aprobada usa tres niveles:
  **`Primitive` → `Semantic` → `Components`**. No impongas esta arquitectura sobre un
  DS existente que el usuario haya decidido conservar.
- `Primitive` contiene valores base y nunca se consume directamente en componentes,
  patterns ni pantallas. Sus variables de color llevan `scopes: []` y se ocultan para
  publicación cuando la API lo permita. Solo `Semantic` puede referenciarlas.
- `Semantic` expresa intención y debe incluir como mínimo familias para `alert`,
  `success`, `error` e `info`, con los roles de fondo, texto, icono y borde que requiera
  cada estado. Todos los pares deben cumplir WCAG AA en cada modo.
- El diseñador decide cuántas familias de marca necesita: puede definir `primary`,
  `secondary` u otras. No fuerces un número cerrado.
- Las variables de `Components` solo se crean al construir componentes estructurales
  del catálogo del DS. **Nunca se crean variables específicas para patterns**: estos
  componen componentes y consumen semánticos o variables de los componentes existentes.
- Los aliases siguen siempre la cadena Components → Semantic → Primitive; no dupliques
  valores crudos entre niveles.

## Scopes y descripciones

- Define en cada variable el scope compatible más estrecho con su uso real. Nunca dejes
  `ALL_SCOPES`. Usa, según corresponda, fill de frame/shape, text fill, stroke, gap,
  radius, width/height o los scopes tipográficos admitidos por Figma.
- Cada variable debe tener una descripción breve de su propósito, dónde se usa y, si
  resulta útil, dónde no debe usarse.
- En un DS existente, scope y descripción son mejoras de metadatos permitidas, pero se
  aplican por lotes revisables y sin alterar ninguna propiedad estructural.

## Medidas y grids

- El sistema se basa en un **grid de 8 puntos**. Crea además los tamaños `2` y `4` para
  hairlines, microespaciado y ajustes que no puedan resolverse con 8. El resto de
  spacing, padding, gap y medidas discretas usa múltiplos de 8.
- El diseñador elige para cada breakpoint o pantalla el número de columnas, márgenes,
  gutter y ancho. Documenta la decisión y expresa esas medidas con el sistema de 8
  puntos; reserva 2 y 4 para las excepciones anteriores.

## Nomenclatura

- Ninguna página, frame, grupo, capa, componente, variante, propiedad o variable puede
  quedar sin nombre ni conservar nombres genéricos como "Frame", "Group" o "Rectangle".
- En proyectos nuevos usa una convención común: variables jerárquicas separadas por `/`,
  frames y capas en kebab-case o BEM, componentes con el nombre del catálogo y variantes
  `Propiedad=Valor`. Mantén exactamente el mismo vocabulario, idioma y casing en todas
  las páginas.
- En archivos existentes, inspecciona primero sus convenciones. Si chocan con el estándar
  del equipo, audita y acuerda la migración antes de renombrar; no impongas cambios de
  nomenclatura silenciosamente.

## Auto Layout y bindings

- Construye con Auto Layout todos los componentes, módulos, patterns, secciones y frames
  que representen páginas o pantallas. La obligación no aplica al nodo `PAGE` ni a
  primitivas gráficas sin estructura interna.
- Toda propiedad visual o estructural que Figma permita vincular debe tener una variable
  o estilo asociado: color, tipografía, spacing, gap, padding, radio, border/stroke,
  opacidad, ancho y altura.
- Solo una dimensión realmente líquida puede quedar sin variable de ancho o altura,
  según corresponda. Las propiedades que Figma no permita vincular y la geometría fija
  imprescindible deben quedar documentadas como excepciones técnicas.
- No uses valores locales como sustituto provisional. Si falta una variable o estilo,
  créalo, limita su scope y descríbelo antes de continuar.
- Los separadores se realizan como border del contenedor, no como líneas sueltas.
- Todo componente con icono lo expone como `INSTANCE_SWAP`, con un icono real de la
  galería como valor inicial; nunca uses un frame de color como sustituto.

## Iconos, capas, motion y elevación

- **Tamaños de icono:** variables `FLOAT` `icon/size/<nombre>` en la colección
  `Components` (p. ej. `icon/size/sm`, `md`, `lg`, `xl`), en múltiplos de 4, scope
  `WIDTH_HEIGHT`, code syntax `var(--icon-size-<nombre>)`. Toda instancia de icono dentro
  de un componente liga su ancho y alto a una de ellas; en CSS los `.icon` solo usan
  `--icon-size-*`. Los iconos siguen exponiéndose como `INSTANCE_SWAP`.
- **Capas (z-index):** colección `Layer` con variables `FLOAT` `layer/<nombre>` (p. ej.
  `base`, `sticky`, `overlay`, `drawer`, `modal`, `toast`), valores enteros crecientes con
  hueco entre niveles, descripción de qué elemento vive en cada capa, code syntax
  `var(--z-<nombre>)`. Figma no aplica z-index, pero la escalera se define aquí para que
  el código la consuma y la documentación la muestre.
- **Motion:** colección `Motion` con duraciones `FLOAT` en ms (`motion/duration/<nombre>`,
  p. ej. `fast`, `base`, `slow`) y easings `STRING` (`motion/easing/<nombre>`, con la
  curva `cubic-bezier(...)` como valor). Code syntax `var(--motion-duration-<nombre>)` y
  `var(--motion-easing-<nombre>)`. Se aplican en prototipos de Figma cuando el editor lo
  permita y siempre en CSS.
- **Elevación:** Figma no admite variables de sombra, así que se define como **effect
  styles** `elevation/<nivel>` (p. ej. `0`, `1`, `2`, `3`) cuyos colores de sombra
  referencian variables semánticas. El sync los serializa a `--elevation-<nivel>` en
  `tokens.css`. Si el DS decide no usar sombras, se documenta explícitamente en
  `tokens.md` § Elevation («sin elevación: separación por borde + superficie») y la
  auditoría marcará como error cualquier `box-shadow`.
- Estas cuatro familias forman parte del **primer sync**: si faltan en Figma, el informe
  de drift las lista como `foundation-missing` y el catálogo de componentes no se da por
  completo hasta que existan o se declaren no aplicables.

## Tipografía: puerta previa a componentes

- Antes de crear componentes o elementos visuales, comprueba que el diseñador ha definido
  familia, pesos, escala, line-height y comportamiento responsive.
- Si aún no existen estilos tipográficos, detén la creación visual y pide su definición.
  No inventes familias, estilos, escalas ni transformaciones responsive.
- El diseñador debe proporcionar las escalas Desktop y Mobile o una regla explícita para
  derivar una de otra. Cuando exista esa definición, crea automáticamente ambos grupos
  de estilos.
- Vincula a variables todas las propiedades tipográficas que Figma permita asociar y
  verifica los nombres reales de familia y estilo antes de crearlos.

## Documentación de tokens

- Al generar o sincronizar la documentación Markdown, regenera en la misma operación
  `tokens.md`, `tokens.json` y `tokens.css`. Son tres espejos del mismo estado de Figma,
  comparten fuentes y fecha de sync y no se editan a mano.
- `tokens.json` conserva colecciones, modos, aliases, scopes y descripciones, incluida la
  jerarquía Primitive → Semantic → Components. `tokens.css` es la salida consumible por
  código; componentes y pantallas solo consumen tokens semánticos o de componente.
- Revisa conjuntamente el diff de los tres artefactos en cada sincronización.

## Gobierno agentic y confianza gradual

- Los agentes pueden **leer**, recuperar contexto acotado, generar propuestas y ejecutar
  auditorías sin aprobación. Pueden aplicar cambios mecánicos solo cuando la fuente de
  verdad y el resultado sean deterministas y la política los marque como automáticos.
- Crear o cambiar tokens, componentes, contratos o primitivas requiere revisión humana.
  Publicar una librería de Figma requiere siempre aprobación explícita.
- Un agente nunca convierte una propuesta en cambio aprobado por sí mismo. Cada propuesta
  registra evidencia, impacto, aprobador requerido y estado.
- El scaffolding nace en **nivel 1** y tiene como objetivo alcanzar **nivel 2
  machine-readable** tras el primer sync verificado. Los archivos locales permiten
  recuperar contexto acotado sin exigir un servidor MCP personalizado del DS.

## Integración con Figma y portabilidad

- El **MCP oficial (nativo) de Figma es la única vía tanto de extracción como de
  escritura** en Figma; está contemplado desde el inicio. Úsalo para inspeccionar
  fuentes, crear o actualizar variables y componentes, validar bindings y ejecutar la
  sincronización. Antes de cualquier operación contra Figma, comprueba que el MCP está
  conectado y configurado y que tiene acceso a las fuentes registradas en el encabezado de `design.md`.
- El MCP no se usa solo en el primer sync: **mientras se trabaje sobre el DS**, es la vía
  para extraer de Figma la información que la tarea necesite y para **mantener
  actualizados los archivos del DS del proyecto** (`tokens.*`, contratos, `schemas/`,
  informes). Toda sesión de trabajo que cambie Figma termina ejecutando el protocolo de
  sync para que los artefactos locales reflejen el estado real.
- **La extracción es incremental por norma.** No se ofrece ni se ejecuta un volcado completo
  del DS en una sola tanda: se trocea por archivo y, cuando el archivo es grande, por página,
  empezando siempre por el que contiene variables y estilos. El coste en tokens de una lectura
  masiva es lo que impide terminar el sync, así que el troceado no es una preferencia del
  usuario sino parte del protocolo.
- El usuario puede pedir a la IA **crear componentes en Figma desde fuera de Figma**
  (desde la conversación o el código), usando el DS existente: sus tokens, estilos,
  convenciones y nomenclatura. Estas escrituras se ejecutan únicamente mediante el MCP
  oficial y conservan las aprobaciones de «Gobierno agentic y confianza gradual»; nunca
  se materializan por otra vía.
- Antes de escribir en Figma, carga y respeta las instrucciones oficiales de la
  integración Figma disponible en el entorno. Las operaciones que cambien tokens,
  componentes, contratos o la publicación de una librería conservan las aprobaciones
  definidas en este documento.
- `agent-manifest.json`, `tokens.json`, los contratos de `schemas/` y los informes son el
  **espejo local estructurado** del DS y el contexto portable para cualquier LLM. No
  reemplazan a Figma ni al MCP de Figma; permiten consultar el DS sin cargar toda la
  documentación y trabajar con sus artefactos locales.
- Un **MCP personalizado del DS no es necesario** para este flujo y esta skill no lo
  crea, configura ni exige. En el futuro podría añadirse como capa opcional para servir
  los mismos archivos locales a múltiples herramientas, pero no forma parte del
  scaffolding, del sync ni de los criterios de madurez.
- Si el LLM o herramienta actual no dispone del MCP oficial de Figma, no simules la
  conexión ni generes contenido supuestamente leído de Figma. Deja el primer sync
  pendiente e indica que debe ejecutarse desde un entorno que sí tenga esa integración.
- No conectes ni propongas servicios externos que el usuario no haya solicitado
  explícitamente. La arquitectura debe funcionar con Figma y los archivos locales.

---
