# library/ · visor del design system

Catálogo navegable del design system de este proyecto: un patrón por componente y por
compuesto, agrupados por página de Figma, con vista previa de cada uno, la ficha, las relaciones
y el estado de verificación contra el maestro. Es un fork del Pattern Library de la empresa
(Eleventy 3 + Nunjucks); desde aquí lo mantiene la skill init-proyecto.

**Todo `src/patterns/` es generado** por `python3 scripts/ds-library.py` a partir de
`design-system/` (schemas, fichas y ejemplos). No se edita: se regenera en cada sync. El visor
(`src/_viewer/`, `src/assets/viewer/`, `lib/`) es plantilla fija de la skill.

## La portada: qué piden los componentes

La home no es un índice (para navegar está el menú): es un tablero. Arriba, el estado del sync
(versión publicada, último sync, cuándo se leyeron componentes y variables de Figma). Después, ocho
contadores que enlazan a su lista: propuestas pendientes, contratos por verificar, borradores de la
IA por revisar, fichas con criterio por escribir, contraste por debajo de AA, sin ejemplo de código,
avisos de fidelidad y retiradas en curso. Y la tabla «componentes que piden atención», una fila por
componente con una marca por asunto y enlace a su ficha. Se calcula en cada build desde
`design-system/` (`src/_data/dashboard.js`); no hay nada que regenerar. Si el informe de fidelidad
es anterior al último sync, lo avisa: `python3 scripts/ds-fidelity.py --out design-system/reports/fidelity.json`.

## Ver el catálogo

Hace falta Node.js (18 o superior) y npm. Solo para verlo: generar los archivos no necesita nada.

```bash
cd library
npm install     # una vez
npm start       # http://localhost:8080 con recarga automática
npm run build   # escribe _site/ (HTML plano, publicable en cualquier servidor)
```

Con `npm start`, un patrón que cambia de grupo o se retira sigue viéndose hasta reiniciar el
servidor: Eleventy no borra páginas en caliente. Tras un sync, reinicia `npm start` o usa
`npm run build`.

**Tras actualizar la skill, reinicia `npm start`.** Los archivos de datos (`src/_data/*.js`) y las
plantillas del visor se cargan como módulos de Node y Node los guarda en memoria: Eleventy dice que los
relee, pero sirve la versión anterior hasta reiniciar. No hay forma fiable de evitarlo con
`addWatchTarget`.

Las vistas previas cargan `design-system/tokens/tokens.css` y `design-system/css/components.css`
tal cual (vía `src/patterns/_base/base.css`), y los iconos de `design-system/assets/` se sirven en
`/assets/ds/`. Si un componente no tiene «Ejemplo de código» en su ficha, su vista previa lo dice.

## Editar la descripción de un componente

La ficha de cada componente tiene un botón **Editar** en la descripción y en cada campo del criterio de
diseño. Cambiar la descripción o el criterio de uso no es trivial, así que no se escribe el texto: se crea una **propuesta** en
`design-system/proposals/` que alguien tiene que aprobar (`design-system/proposals/README.md`).

- Con `npm start`, la propuesta se guarda directamente en el proyecto y la ficha pasa a mostrar el
  texto propuesto con la etiqueta «Pendiente de aprobación».
- Una sola propuesta por componente para todos sus textos: si ya hay una pendiente, el cambio se
  añade a esa; no se crea otra.
- Publicada como web estática no hay servidor: el botón descarga la propuesta para guardarla a mano.
- El campo de accesibilidad tiene además **No aplica** (componentes decorativos o solo informativos):
  pide el motivo y va a la misma propuesta. Un texto propuesto por la IA lleva la marca «Borrador de la
  IA» hasta que alguien lo edita.

El servidor que guarda las propuestas (`lib/proposals-server.js`) solo existe con `npm start` y solo
escribe en `design-system/proposals/`.

## Estados

`Ready` = contrato verificado contra su maestro de Figma · `In review` = verificado, pero el
maestro cambió después · `Draft` = sin verificar · `Deprecated` = retirado en
`schemas/governance/lifecycle.json`.
