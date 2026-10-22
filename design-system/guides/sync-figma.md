# Sync desde Figma  ⚙️  (cómo se regeneran los artefactos)

> Guía de `design-system/design.md`: se lee solo cuando la tarea lo pide (la tabla de «Enrutado» de `design.md` dice cuándo).

**Cuándo:** cuando algo cambie en Figma (color, token nuevo, modo, componente) y, de
forma continua, **al cierre de cualquier sesión de trabajo sobre el DS** que haya tocado
Figma — la extracción vía MCP mantiene los archivos del DS del proyecto al día.
**No edites los archivos generados** — vuelve a generarlos y revisa el diff de git.

**Artefactos generados (no editar a mano):** `docs/tokens.md`, `tokens/tokens.json`,
`tokens/tokens.css`, la parte viva de cada ficha `docs/components/<slug>.md`/`docs/patterns/<slug>.md` y el
`## Índice` de `docs/components.md`/`docs/patterns.md`, los contratos
de `schemas/components/`, `assets/icons/` y `assets/fonts/`, `showcase/index.html` (secciones
`GENERATED`) y todo `reports/`. Llevan procedencia, versión y fecha del último sync. Los genera
`scripts/ds-sync.py` a partir de los volcados de `sync/` (ver `sync/README.md`); la única
escritura del agente es el volcado.

**Procedimiento (lo ejecuta cualquier LLM/agente con acceso al MCP oficial de Figma).**
Tiene dos mitades: **leer Figma** (solo el agente, por MCP, sin transformar nada) y **generar
los artefactos** (solo el script, determinista, sin leer Figma). La frontera es la carpeta
`sync/`: el agente vuelca ahí lo leído, el script parte de ahí. Mismo volcado → mismos
artefactos, con cualquier modelo.

1. **Comprobar el MCP.** Conectado, configurado y con acceso a las fuentes registradas; si no,
   detener el sync, informar y dejarlo pendiente. Consultar qué archivo gobierna tokens,
   componentes y patrones y leer solo los necesarios. Confirmar el modo de adopción: en
   `preserve-existing` no se transforma nada estructural.
1b. **Planificar la extracción por pasos.** Nunca se vuelca todo de una vez: se trocea para
   no agotar la sesión en tokens. El primer tramo es siempre **variables y estilos** y, si hay
   varias fuentes, se pregunta cuál las contiene y se empieza por ella. Después, **un archivo
   por tanda** en el orden variables y estilos → componentes → patrones → iconos; y si un
   archivo es grande, **una página por tanda**, listando antes las páginas y acordando cuáles
   quedan fuera. Entre tramo y tramo, un resumen de tres líneas y confirmación para seguir.
   **Cada lectura, además, va por trozos**: `use_figma` corta cada respuesta hacia los
   **20 KB** (`// truncated to 20kb`) y un DS mediano ya lo supera. Los dos scripts de lectura
   devuelven trozos de unos 14 KB y dicen dónde empieza el siguiente (`part.nextOffset`); se
   llaman en bucle hasta que sea `null`. **No pegues el JSON en el texto de la conversación ni
   lo resumas campo a campo: guárdalo en `sync/parts/` en la misma vuelta en que lo recibes,
   sin modificarlo.** La unión la hace el script, nunca el agente.
2. **Volcar variables y estilos → `sync/parts/variables-<NNN>.json`.** Ejecutar el script
   «lectura de variables y estilos» (abajo) sobre el archivo de tokens con `OFFSET = 0` y
   después con cada `part.nextOffset`, guardando cada respuesta tal cual. Si los tokens están
   repartidos en varios archivos, el mismo bucle en cada uno: cada trozo lleva su `fileKey`.
3. **Volcar componentes → `sync/parts/components-<NNN>.json`.** Ejecutar el script «lectura
   de componentes» (abajo) **una página por llamada** y, dentro de la página, por trozos igual
   que las variables, con `skipInvisibleInstanceChildren = false` (los iconos suelen estar
   ocultos por defecto). Todo `COMPONENT_SET` y todo `COMPONENT` suelto de las páginas leídas
   acaba en el volcado; ninguno se filtra a mano.
3b. **Unir y validar: `python3 scripts/ds-sync.py --merge`.** Une los trozos en
   `sync/variables.json` y `sync/components.json` por su posición (no por el nombre del
   archivo), los borra y valida el volcado: que ningún trozo llegó cortado, que no falta ni
   sobra ninguno, que no hay IDs repetidos y que todos los alias apuntan a una variable del
   volcado. Si algo falla no escribe nada y dice qué trozo volver a leer. `--check-dump` hace
   solo la validación. **Refresco puntual:** si solo ha cambiado un componente (una propiedad, una
   descripción, un renombre), no hace falta releer la página: el script de componentes con
   `NODE_IDS = ['<id>', …]` devuelve solo esos, el trozo lleva `part.refresh`, y `--merge` los sustituye
   por id en su página y lo anota en `partialRefresh.history` del volcado. Lo mismo con las variables:
   el script de variables con `VARIABLE_IDS = ['VariableID:…']` o `VARIABLE_NAMES = ['error/background/strong']`
   lee solo esas (una llamada, no las trescientas), `--merge` las sustituye o añade por id en
   `sync/variables.json`, resuelve sus alias contra el volcado completo (si apuntan a algo que no está,
   error y no se escribe) y avisa de las que no existan en Figma (`part.missing`); el `ds-sync.py` siguiente
   regenera `tokens.css`, `tokens.md`, showcase y library desde el volcado unido, igual que tras una
   relectura completa. **Sync incremental (lo normal cuando el volcado ya existe):** antes de releer
   nada, el «script de huellas de variables» (abajo) devuelve en una llamada `[id, huella]` de cada
   variable; se guarda en `sync/parts/fingerprints-001.json` y `python3 scripts/ds-sync.py --variables-diff`
   lo compara con el volcado: lista las cambiadas, las nuevas y las desaparecidas, imprime la línea
   `VARIABLE_IDS = [...]` para el refresco puntual y deja preparada la retirada de las desaparecidas
   (un trozo `refresh` con `part.removed`, que `--merge` aplica). Sin cambios, lo dice y no hay nada que
   leer. Una relectura completa solo hace falta la primera vez o si el volcado no tiene huellas de una
   versión anterior (el motor las calcula él mismo para volcados antiguos). Nunca se edita el volcado a
   mano. **Guardas:** `--merge` exige la cadena de
   variables entera (del trozo 0 hasta `nextOffset: null`, sin huecos, `read == total`); si está a medias y
   solo hay trozos de variables, error sin escribir nada; si además hay trozos de componentes (el merge viene
   de un refresco de componentes), aparta los de variables, conserva `variables.json` y sigue solo con los
   componentes, avisando. Y la generación se para si el `tokens.css` nuevo tendría más de un 10 % menos de
   tokens que el actual (`--allow-fewer-tokens` si la bajada es intencionada). Un trozo con `OFFSET = 0` empieza de cero ese archivo o esa página, así
   que releer algo es volver a pedirlo desde 0. El resultado es idéntico al de una lectura
   de una sola pasada.
3b'. **Piezas internas: lo que no es del sistema compartido.** Los archivos de Figma traen piezas de
   trabajo que no se construyen ni se verifican: contenido de ejemplo de los huecos (`swap/*`), fotogramas
   (`loading-spinner`), ejemplos (`ejemplo-tarjeta`), componentes que Figma no publica (nombre con «.» o
   «_») y retirados («deprecated» en el nombre o en la página, página «Documentation»). Hay **una sola
   definición** para toda la skill (`scripts/ds_common.py`): esos criterios, más `figma.published = false`
   si el script de lectura de componentes lo trae (Figma no siempre expone si un componente se publica;
   si no lo da, queda `null` y no cuenta) y la lista manual `internal.names` de
   `scripts/ds-library.config.json` (por nombre o por slug). El sync lo escribe en el contrato
   (`meta.internal: true` y `meta.internalReason`), y desde ahí: `ds-fidelity` no los cuenta como
   `unverified` y no emite sobre ellos avisos de CSS, tokens, ejemplo ni cobertura (resumen: «N contratos
   (M internos, no se verifican)»); el sync no emite `code-example-missing-or-stale` ni
   `icon-not-exposed-as-swap`, y `slug-collision` solo mira componentes no internos (si un interno y un
   compartido comparten slug, el contrato es del compartido); `variable-from-foreign-library` se mantiene
   en ellos pero como aviso; una pantalla que monte uno recibe `screen-uses-internal`, aparte de
   `screen-uses-unverified`, porque no debería estar ahí; sus fichas nuevas nacen con una nota de pieza
   interna y sin campos de criterio (las que ya existían se conservan); no se les proponen textos; la
   library los aparta en «Internos de Figma»; y `drift-report.json → internals` los lista con su motivo para
   revisar si alguno debería pasar a ser compartido.
3c. **Librerías ligadas: que todo apunte a la Foundations declarada.** Una copia antigua de Foundations
   (en Figma aparece como «Missing library») tiene los mismos nombres de variables con otras keys: el sync,
   las auditorías y las verificaciones comparan por nombre y no lo detectan, y un cambio publicado en
   Foundations no llega a los componentes. Desde la 12.12.0 los volcados llevan la **key** de cada
   variable, colección y estilo, y: (a) el «script de auditoría de librerías ligadas» (abajo) recorre un
   archivo de componentes y devuelve, por componente, las variables y estilos remotos cuya librería no es
   la declarada, comparando por la key de cada variable, no por la de su colección (las keys conocidas las
   imprime `python3 scripts/ds-sync.py --library-keys`); se guarda en
   `sync/library-audit/<fileKey>-<NNN>.json` y el sync abre un hallazgo **crítico**
   `variable-from-foreign-library` por componente (aviso `style-from-foreign-library` para estilos de
   texto, color, efecto o rejilla); (b) el script de lectura de componentes guarda las keys de lo que liga
   (`bindings.variableKeys`), así que una relectura o un refresco puntual también lo detecta sin auditoría.
   **Arreglo, en Figma, en cada archivo afectado:** Assets → Manage libraries → pestaña *This file* →
   en «Missing library» (o la librería equivocada) → **Swap library** → elegir la Foundations declarada
   y emparejar cada colección con la suya (mismos nombres); repetir para los estilos (texto, color,
   efecto, rejilla), que se intercambian aparte. Después, refresco puntual o relectura de las páginas
   tocadas y sync: el hallazgo desaparece. **Si no encuentras la variable ajena en el componente:** cada
   hallazgo trae, por variable, hasta seis sitios con el id del nodo, su nombre y la propiedad
   (`fills[0]`, `effects[1]`, `boundVariables.itemSpacing`…), y marca los que están dentro de una
   instancia anidada: esos enlaces los trae el componente de origen y se arreglan allí, no en este.
   Con el id se llega al nodo en Figma (`figma.getNodeByIdAsync`) y se descarta o confirma el falso
   positivo. **Notas para quien escriba scripts de reenlace:** (a) `paragraphSpacing` en un texto sin
   estilo no cambia con `setRangeBoundVariable`; lo que funciona es aplicar el estilo de texto de la
   Foundations a todo el texto. (b) No saques las variables «buenas» de `figma.teamLibrary` por
   nombre: si la copia antigua de Foundations sigue disponible con el mismo nombre, se cuela; usa las
   keys que imprime `--library-keys`.
4. **Exportar iconos → `assets/icons/` + `sync/icons.json`.** Exportar como SVG, mediante el MCP,
   cada icono de la galería (`Icon / <nombre>` → `<nombre-kebab>.svg`) y registrar
   `{ "name", "nodeId", "file", "usage" }` en `sync/icons.json`. Fuentes necesarias →
   `assets/fonts/`. No existe ningún otro `img/` ni `fonts/` en el proyecto.
5. **Generar: `python3 scripts/ds-sync.py`.** A partir de `sync/` regenera, siempre igual:
   `docs/tokens.md`, `tokens/tokens.json`, `tokens/tokens.css` (primitivos, alias resueltos,
   modo Dark bajo `[data-theme="dark"]`, modos de dispositivo bajo `@media`, elevación desde
   effect styles y **tipografía desde text styles**: por estilo,
   `--font-<estilo>-{family,size,weight,line-height,letter-spacing}`, con `AUTO` → `normal` y
   el tracking en porcentaje → `em`. Un estilo con el breakpoint en el nombre («Desktop XL /
   H1», «Mobile / H1») sigue siendo un estilo aparte con sus variables: el CSS de componentes
   elige cuál usar en cada `@media`. Si Figma no da un nombre de familia válido para la web o
   no se deduce el peso, se declara en `fontFamilyMap` de `ds-sync.config.json`; no se adivina); un `schemas/components/<slug>.schema.json` por componente, en cuatro capas: `api` (props con tipo
   y defecto sin nombres de Figma, estados de CSS aparte, eventos, slots y exclusiones a mano, iconos,
   tokens), `code` (enlace con HTML), `figma` (trazabilidad: keys y el nombre original de cada prop) y
   `docs`; un schema anterior a la 12.0.0 se migra solo conservando lo manual; el catálogo navegable
   `../library/src/patterns/` (un patrón por contrato, con su ejemplo, su ficha y su estado, generado por
   `scripts/ds-library.py` al cierre del sync); `schemas/index.json` y `relationships.json`; la
   **parte viva** de cada ficha `docs/components/<slug>.md`/`docs/patterns/<slug>.md` (bloque
   `GENERATED:<slug>`) y el `## Índice` de `docs/components.md`/`docs/patterns.md`, conservando la
   parte de criterio escrita a mano (que vive solo en la ficha; el schema la señala con `docs`)
   y creando la ficha con `⬜ TODO` si el componente es nuevo (su forma: `docs/<carpeta>/_plantilla.md`); `docs/assets.md`; las secciones `GENERATED` del
   `showcase/index.html`; `reports/drift-report.json` con los hallazgos
   (`icon-not-exposed-as-swap`, `foundation-missing`, `schema-without-component`,
   `missing-variable-description-or-scope`, `primitive-with-scopes`, `text-style-weight-unknown`,
   `code-example-missing-or-stale`, `verification-stale`…). Un primitivo con `scopes: []` **no** es un hallazgo:
   es lo que pide «Arquitectura de variables de color». Se reconoce por estar oculto al
   publicar, por su colección (`primitiveCollections` en la config) o por ser base de otros
   sin apuntar a nadie; lo que sí se marca es un primitivo con scopes y `lastSync` en
   `agent-manifest.json`. Con `--dry` muestra qué haría sin escribir. Devuelve error si hay
   hallazgos críticos. **Ningún componente sin schema; ningún schema sin componente.**
6. **Completar el criterio.** Para cada contrato nuevo, rellenar a mano en el `.md` lo que
   Figma no puede decir: Propósito, **Ejemplo de código** (snippet HTML con las clases reales
   de `css/components.css`; `ds-sync` lo copia al schema como `code.example` y
   `classes` en la siguiente ejecución), Accesibilidad y Cuándo usar. Propósito, Accesibilidad y
   Cuándo usar se escriben **solo** en el `.md`, nunca en el schema. Comprobar que todas las
   clases del ejemplo existen en `components.css` y viceversa, y que
   `patterns.md § Composición de pantalla` tiene sus tablas rellenas o marcadas `⬜ TODO` con
   fecha. Volver a ejecutar `ds-sync.py` para propagar los ejemplos al schema y al showcase.
   En el «Ejemplo de código», los iconos van con su ruta real (`../assets/icons/<nombre>.svg`) y las
   fotos siempre con `../assets/images/placeholder.svg`, nunca con fotos de `UI/`: el catálogo
   (`library/`) da ERROR si un icono no existe y muestra el placeholder si una foto no es del DS.
7. **Verificar.** `python3 scripts/token-audit.py --out design-system/reports/token-audit.json`
   con **cero errores** y `python3 scripts/ds-fidelity.py --out design-system/reports/fidelity.json`
   (avisos: lo que el CSS y los ejemplos no cuadran con el contrato, y cuántos contratos siguen sin verificar); abrir el showcase en el navegador como prueba visual de que tokens,
   componentes y ejemplos cuadran. Revisar la tabla componente → iconos detectados con el
   usuario. Después, `git diff` (incluye `sync/`, que muestra qué cambió en Figma) y commit.

En modo `preserve-existing`, la regeneración describe la arquitectura y nomenclatura
real de Figma. Las diferencias frente al estándar quedan en el informe de drift como
hallazgos informativos o decisiones aceptadas, no como órdenes de reestructuración. La
única escritura de mejora prevista sobre variables existentes es completar scopes y
descripciones mediante un lote previamente informado.

<details><summary>Script de lectura de variables y estilos (solo lectura; por trozos)</summary>

```js
// Se ejecuta con la herramienta de scripts del MCP oficial de Figma (`use_figma`), Plugin API.
// POR TROZOS: el MCP corta cada respuesta hacia los 20 KB, y un DS mediano ya lo supera. Cada
// llamada devuelve un trozo de unos 14 KB y dice dónde empieza el siguiente (part.nextOffset).
// Se llama con OFFSET = 0 y después con cada nextOffset, hasta que nextOffset sea null.
// Cada respuesta se guarda TAL CUAL en design-system/sync/parts/variables-<NNN>.json, en la misma
// vuelta en que llega. La unión la hace `python3 scripts/ds-sync.py --merge`, no el agente.
const OFFSET = 0;          // 0 en la primera llamada; después, el part.nextOffset de la anterior
const VARIABLE_IDS = [];   // REFRESCO PUNTUAL: ids de las variables nuevas o cambiadas (p. ej. ['VariableID:35077:12']).
const VARIABLE_NAMES = []; // …o sus nombres ('error/background/strong'). Con cualquiera de los dos, se leen SOLO esas
                           // (sin estilos), el trozo lleva part.refresh y `ds-sync.py --merge` las sustituye o añade por
                           // id en el volcado completo, resolviendo sus alias contra él. Vacíos = lectura completa.
const unesc = (s) => String(s || '').replace(/&nbsp;/g, ' ').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&amp;/g, '&'); // descripciones sin entidades HTML
const MAX_CHARS = 14000;   // tamaño máximo del trozo. No lo subas: por encima de ~20 KB el MCP corta

const collections = await figma.variables.getLocalVariableCollectionsAsync();
// Todas las variables de una vez (una llamada, no una por variable): de aquí salen nombres, alias y huellas.
const byId = new Map((await figma.variables.getLocalVariablesAsync()).map(v => [v.id, v]));
const textStyles = await figma.getLocalTextStylesAsync();
const effectStyles = await figma.getLocalEffectStylesAsync();
// Huella de una variable: FNV-1a de su forma canónica (claves ordenadas, números a 6 decimales). ds-sync.py calcula
// la misma en Python; comparar huellas es lo que permite el sync incremental (script de huellas, más abajo).
const numStr = (n) => Number.isInteger(n) ? String(n) : String(Math.round(n * 1e6) / 1e6);
const canon = (x) => x === null || x === undefined ? 'null' : typeof x === 'number' ? numStr(x) : typeof x === 'string' ? JSON.stringify(x)
  : typeof x === 'boolean' ? String(x) : Array.isArray(x) ? '[' + x.map(canon).join(',') + ']'
  : '{' + Object.keys(x).sort().map(k => JSON.stringify(k) + ':' + canon(x[k])).join(',') + '}';
const fnv = (str) => { let h = 0x811c9dc5; for (const ch of str) { h ^= ch.codePointAt(0); h = Math.imul(h, 16777619) >>> 0; } return h.toString(16).padStart(8, '0'); };
const huella = (e) => fnv(canon({ name: e.name, type: e.type, description: e.description, scopes: e.scopes, codeSyntax: e.codeSyntax, hiddenFromPublishing: e.hiddenFromPublishing, valuesByMode: e.valuesByMode }));
// Todo lo que hay que leer, en una lista plana y en orden fijo: un número basta para retomar.
const items = [];
const REFRESH = VARIABLE_IDS.length + VARIABLE_NAMES.length > 0;
let missing = [];
if (REFRESH) {
  // Solo las pedidas, por id o por nombre; lo que no exista en Figma se devuelve en part.missing para que avise.
  const wanted = new Set([...VARIABLE_IDS, ...VARIABLE_NAMES]);
  for (const col of collections) for (const id of col.variableIds) {
    const v = byId.get(id);
    if (v && (wanted.has(v.id) || wanted.has(v.name))) { items.push({ kind: 'variable', col, id }); wanted.delete(v.id); wanted.delete(v.name); }
  }
  missing = [...wanted];
} else {
  for (const col of collections) for (const id of col.variableIds) items.push({ kind: 'variable', col, id });
  for (const s of textStyles) items.push({ kind: 'text', s });
  for (const s of effectStyles) items.push({ kind: 'effect', s });
}

const out = { kind: 'variables', fileKey: figma.fileKey || null, fileName: figma.root.name, version: null,
  readAt: new Date().toISOString(), part: { offset: OFFSET, nextOffset: null, count: 0, total: items.length, refresh: REFRESH, missing },
  collections: [], textStyles: [], effectStyles: [] };
let size = JSON.stringify(out).length;
const colOut = new Map();

async function variable(id) {
  const v = byId.get(id) || await figma.variables.getVariableByIdAsync(id);
  if (!v) return null;
  const valuesByMode = {};
  for (const [modeId, val] of Object.entries(v.valuesByMode)) {
    if (val && typeof val === 'object' && val.type === 'VARIABLE_ALIAS') {
      const target = byId.get(val.id) || await figma.variables.getVariableByIdAsync(val.id);
      valuesByMode[modeId] = { type: 'alias', id: val.id, name: target ? target.name : null };
    } else {
      valuesByMode[modeId] = { type: 'value', value: val };
    }
  }
  const e = { id: v.id, name: v.name, type: v.resolvedType, description: unesc(v.description), scopes: v.scopes || [],
    codeSyntax: v.codeSyntax || {}, hiddenFromPublishing: v.hiddenFromPublishing, valuesByMode };
  e.h = huella(e);
  e.key = v.key || null; // key de librería: identifica la variable aunque otra librería tenga una con el mismo nombre
  return e;
}

for (let i = OFFSET; i < items.length; i++) {
  const it = items[i];
  let entry, newCol = null;
  if (it.kind === 'variable') {
    entry = await variable(it.id);
    if (entry && !colOut.has(it.col.id)) {
      newCol = { id: it.col.id, name: it.col.name, key: it.col.key || null, modes: it.col.modes.map(m => ({ modeId: m.modeId, name: m.name })),
        defaultModeId: it.col.defaultModeId, variables: [] };
    }
  } else if (it.kind === 'text') {
    const s = it.s;
    entry = { id: s.id, name: s.name, key: s.key || null, description: unesc(s.description), fontFamily: s.fontName?.family || null,
      fontStyle: s.fontName?.style || null, fontSize: s.fontSize, lineHeight: s.lineHeight,
      letterSpacing: s.letterSpacing, boundVariables: s.boundVariables || {} };
  } else {
    const s = it.s;
    entry = { id: s.id, name: s.name, key: s.key || null, description: unesc(s.description), effects: s.effects.map(e => ({ type: e.type,
      visible: e.visible, radius: e.radius, spread: e.spread || 0, offset: e.offset || null, color: e.color || null })) };
  }
  const add = (entry ? JSON.stringify(entry).length + 1 : 0) + (newCol ? JSON.stringify(newCol).length + 1 : 0);
  if (out.part.count > 0 && size + add > MAX_CHARS) { out.part.nextOffset = i; break; }
  if (entry && it.kind === 'variable') {
    if (newCol) { colOut.set(it.col.id, newCol); out.collections.push(newCol); }
    colOut.get(it.col.id).variables.push(entry);
  } else if (entry) {
    (it.kind === 'text' ? out.textStyles : out.effectStyles).push(entry);
  }
  size += add;
  out.part.count++;
}
return out;
```
</details>

<details><summary>Script de huellas de variables (solo lectura; una llamada: qué ha cambiado desde el último sync)</summary>

```js
// SYNC INCREMENTAL. Devuelve solo [id, huella] de cada variable del archivo: unos 11 KB para 300 variables, una
// llamada. Se guarda tal cual en design-system/sync/parts/fingerprints-<NNN>.json y
// `python3 scripts/ds-sync.py --variables-diff` lo compara con sync/variables.json y dice qué variables han
// cambiado, cuáles son nuevas y cuáles han desaparecido, con la línea VARIABLE_IDS lista para el refresco puntual.
// Si no cabe en una respuesta (part.nextOffset), se repite con OFFSET = part.nextOffset.
const OFFSET = 0;
const MAX_CHARS = 14000;
const numStr = (n) => Number.isInteger(n) ? String(n) : String(Math.round(n * 1e6) / 1e6);
const canon = (x) => x === null || x === undefined ? 'null' : typeof x === 'number' ? numStr(x) : typeof x === 'string' ? JSON.stringify(x)
  : typeof x === 'boolean' ? String(x) : Array.isArray(x) ? '[' + x.map(canon).join(',') + ']'
  : '{' + Object.keys(x).sort().map(k => JSON.stringify(k) + ':' + canon(x[k])).join(',') + '}';
const fnv = (str) => { let h = 0x811c9dc5; for (const ch of str) { h ^= ch.codePointAt(0); h = Math.imul(h, 16777619) >>> 0; } return h.toString(16).padStart(8, '0'); };
const unesc = (s) => String(s || '').replace(/&nbsp;/g, ' ').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&amp;/g, '&');
const all = await figma.variables.getLocalVariablesAsync();
const byId = new Map(all.map(v => [v.id, v]));
const cols = await figma.variables.getLocalVariableCollectionsAsync();
const ids = [];
for (const col of cols) for (const id of col.variableIds) ids.push(id);
const out = { kind: 'variable-fingerprints', fileKey: figma.fileKey || null, fileName: figma.root.name, readAt: new Date().toISOString(),
  part: { offset: OFFSET, nextOffset: null, count: 0, total: ids.length }, items: [] };
if (OFFSET === 0) { // keys de librería de colecciones y estilos (no cambian): --variables-diff las completa en el volcado
  out.collections = cols.map(c => ({ id: c.id, key: c.key || null, name: c.name }));
  out.styles = [...(await figma.getLocalTextStylesAsync()).map(s => ({ id: s.id, key: s.key || null, name: s.name, type: 'text' })),
                ...(await figma.getLocalEffectStylesAsync()).map(s => ({ id: s.id, key: s.key || null, name: s.name, type: 'effect' }))];
}
let size = JSON.stringify(out).length;
for (let i = OFFSET; i < ids.length; i++) {
  const v = byId.get(ids[i]);
  if (!v) continue;
  const valuesByMode = {};
  for (const [modeId, val] of Object.entries(v.valuesByMode)) {
    if (val && typeof val === 'object' && val.type === 'VARIABLE_ALIAS') { const t = byId.get(val.id); valuesByMode[modeId] = { type: 'alias', id: val.id, name: t ? t.name : null }; }
    else valuesByMode[modeId] = { type: 'value', value: val };
  }
  const h = fnv(canon({ name: v.name, type: v.resolvedType, description: unesc(v.description), scopes: v.scopes || [],
    codeSyntax: v.codeSyntax || {}, hiddenFromPublishing: v.hiddenFromPublishing, valuesByMode }));
  const item = [v.id, h, v.key || null];
  const add = JSON.stringify(item).length + 1;
  if (out.part.count > 0 && size + add > MAX_CHARS) { out.part.nextOffset = i; break; }
  out.items.push(item); size += add; out.part.count++;
}
return out;
```
</details>

<details><summary>Script de auditoría de librerías ligadas (solo lectura; por archivo de componentes, por trozos)</summary>

```js
// ¿Qué componentes ligan variables o estilos de una librería que NO es la Foundations declarada? Una copia
// antigua de Foundations («Missing library») tiene los mismos nombres y otras keys: el sync y las auditorías
// comparan por nombre y no lo ven, y un cambio publicado en Foundations no llega. Se ejecuta en cada archivo
// de componentes y patrones. Las keys conocidas las imprime `python3 scripts/ds-sync.py --library-keys`
// (necesita el volcado con keys: script de huellas + --variables-diff, o relectura con el script de la 12.12.0).
// Cada respuesta se guarda en design-system/sync/library-audit/<fileKey>-<NNN>.json; con part.nextOffset se
// repite con OFFSET = part.nextOffset. El sync siguiente abre un hallazgo crítico por componente afectado.
// Se compara por la key de cada VARIABLE, no por la de su colección: en un archivo reenlazado la API puede
// devolver la colección antigua para una variable que ya es de la Foundations publicada.
const KNOWN_VARIABLE_KEYS = [];   // ← pegar la salida de --library-keys
const KNOWN_STYLE_KEYS = [];      // ← ídem (estilos de texto y efecto de Foundations)
const OFFSET = 0;
const MAX_CHARS = 14000;
for (const p of figma.root.children) await p.loadAsync(); // loadAllPagesAsync no está en el MCP
const known = new Set(KNOWN_VARIABLE_KEYS), knownStyles = new Set(KNOWN_STYLE_KEYS);
const colCache = new Map(), varCache = new Map(), styleCache = new Map();
async function variableInfo(id) {
  if (varCache.has(id)) return varCache.get(id);
  let info = null;
  try {
    const v = await figma.variables.getVariableByIdAsync(id);
    if (v) {
      if (!colCache.has(v.variableCollectionId)) colCache.set(v.variableCollectionId, await figma.variables.getVariableCollectionByIdAsync(v.variableCollectionId));
      const c = colCache.get(v.variableCollectionId);
      info = { name: v.name, key: v.key || null, remote: !!v.remote, collectionKey: c ? c.key || null : null, collectionName: c ? c.name : null };
    }
  } catch {}
  varCache.set(id, info); return info;
}
async function styleInfo(id, type) {
  const k = type + id; if (styleCache.has(k)) return styleCache.get(k);
  let info = null;
  try { const s = await figma.getStyleByIdAsync(id); if (s) info = { name: s.name, key: s.key || null, remote: !!s.remote, type }; } catch {}
  styleCache.set(k, info); return info;
}
const roots = [];
for (const page of figma.root.children) for (const n of page.findAllWithCriteria({ types: ['COMPONENT', 'COMPONENT_SET'] }))
  if (!(n.type === 'COMPONENT' && n.parent && n.parent.type === 'COMPONENT_SET')) roots.push({ n, page: page.name });
// Todas las referencias a variables de un nodo, con la propiedad donde está (fills[0], strokes[1], effects[0],
// layoutGrids[0], boundVariables.<campo>, …), para poder localizar la ajena en Figma o descartar un falso positivo.
function refsOf(node) {
  const out = [];
  const add = (prop, b) => { if (b && b.id) out.push([prop, b.id]); };
  const walkBV = (prefix, bv) => { for (const [k, v] of Object.entries(bv || {})) { if (Array.isArray(v)) v.forEach((b, i) => add(`${prefix}.${k}[${i}]`, b)); else if (v && v.id) add(`${prefix}.${k}`, v); else if (v && typeof v === 'object') for (const [k2, b] of Object.entries(v)) add(`${prefix}.${k}.${k2}`, b); } };
  try { walkBV('boundVariables', node.boundVariables); } catch (e) {}
  for (const f of ['fills', 'strokes']) { let arr; try { arr = node[f]; } catch (e) { continue; } if (Array.isArray(arr)) arr.forEach((p, i) => { add(`${f}[${i}]`, p.boundVariables && p.boundVariables.color); }); }
  let eff; try { eff = node.effects; } catch (e) {}
  if (Array.isArray(eff)) eff.forEach((e, i) => walkBV(`effects[${i}]`, e.boundVariables));
  let grids; try { grids = node.layoutGrids; } catch (e) {}
  if (Array.isArray(grids)) grids.forEach((g, i) => walkBV(`layoutGrids[${i}]`, g.boundVariables));
  return out;
}
// Recorrido propio (no findAll) para saber si un nodo está DENTRO de una instancia anidada: sus enlaces los trae el
// componente de origen, no este, y el arreglo es en aquel componente.
function* walk(node, viaInstance) {
  yield [node, viaInstance];
  if ('children' in node) for (const c of node.children) yield* walk(c, viaInstance || node.type === 'INSTANCE');
}
const out = { kind: 'library-bindings', fileKey: figma.fileKey || null, fileName: figma.root.name, readAt: new Date().toISOString(),
  known: { collections: known.size, styles: knownStyles.size }, part: { offset: OFFSET, nextOffset: null, count: 0, total: roots.length }, components: [] };
let size = JSON.stringify(out).length;
for (let i = OFFSET; i < roots.length; i++) {
  const { n, page } = roots[i];
  const foreignVariables = new Map(), foreignStyles = new Map();
  for (const [node, viaInstance] of walk(n, false)) {
    for (const [prop, id] of refsOf(node)) {
      const v = await variableInfo(id);
      if (!v || !v.remote || known.has(v.key)) continue;
      if (!foreignVariables.has(v.name)) foreignVariables.set(v.name, { ...v, where: [] });
      const w = foreignVariables.get(v.name).where;
      if (w.length < 6) w.push({ nodeId: node.id, nodeName: node.name, prop, viaInstance });
    }
    for (const [prop, type] of [['textStyleId', 'text'], ['fillStyleId', 'paint'], ['strokeStyleId', 'paint'], ['effectStyleId', 'effect'], ['gridStyleId', 'grid']]) {
      if (!(prop in node)) continue; let id; try { id = node[prop]; } catch (e) { continue; } // un TEXT no tiene gridStyleId y lanza
      if (typeof id !== 'string' || !id) continue;
      const st = await styleInfo(id, type); if (st && st.remote && !knownStyles.has(st.key)) foreignStyles.set(type + ':' + st.name, st);
    }
  }
  const entry = (foreignVariables.size || foreignStyles.size)
    ? { id: n.id, name: n.name, page, foreignVariables: [...foreignVariables.values()], foreignStyles: [...foreignStyles.values()] } : null;
  const add = entry ? JSON.stringify(entry).length + 1 : 0;
  if (out.part.count > 0 && size + add > MAX_CHARS) { out.part.nextOffset = i; break; }
  if (entry) out.components.push(entry);
  size += add; out.part.count++;
}
return out;
```
</details>

<details><summary>Script de lectura de componentes (solo lectura; una página por llamada, por trozos)</summary>

```js
// Se ejecuta con la herramienta de scripts del MCP oficial de Figma (`use_figma`), que expone la
// Plugin API de Figma. Es independiente del LLM: cualquier agente conectado al MCP la tiene.
// Antes de ejecutarlo, leer la guía `figma-use` que sirve el propio MCP (recurso skill://figma/figma-use).
// UNA PÁGINA POR LLAMADA y, dentro de la página, POR TROZOS: el MCP corta cada respuesta hacia
// los 20 KB y una página con muchas variantes lo supera. Se llama con OFFSET = 0 y después con cada
// part.nextOffset, hasta que sea null; luego, la página siguiente.
// Cada respuesta se guarda TAL CUAL en design-system/sync/parts/components-<NNN>.json, en la misma
// vuelta en que llega. La unión la hace `python3 scripts/ds-sync.py --merge`, no el agente.
const PAGE_ID = '0:1';     // id de la página (listar antes con figma.root.children: solo nombre e id)
const OFFSET = 0;          // 0 en la primera llamada de cada página; después, el part.nextOffset
const NODE_IDS = [];       // REFRESCO PUNTUAL: ids de los componentes que han cambiado (p. ej. ['123:45']). Vacío =
                           // lectura completa de la página. Con ids, el trozo lleva part.refresh y `ds-sync.py --merge`
                           // sustituye solo esos componentes en el volcado, sin releer la página.
const MAX_CHARS = 14000;   // tamaño máximo del trozo. No lo subas: por encima de ~20 KB el MCP corta
figma.skipInvisibleInstanceChildren = false; // imprescindible: los iconos suelen estar ocultos por defecto
const page = await figma.getNodeByIdAsync(PAGE_ID);
await figma.setCurrentPageAsync(page);

const nameOf = async (id) => { try { const n = await figma.getNodeByIdAsync(id); return n ? n.name : null; } catch { return null; } };
// Las descripciones llegan de la Plugin API con entidades HTML (&gt;, &quot;, &nbsp;…): se devuelven como texto
// normal, para que leer dos veces lo mismo dé lo mismo que guarda el volcado.
const unesc = (s) => String(s || '').replace(/&nbsp;/g, ' ').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&amp;/g, '&');
const varName = async (id) => { try { const v = await figma.variables.getVariableByIdAsync(id); return v ? v.name : id; } catch { return id; } };

const colCache = new Map();
async function keyOf(id) { // key de la variable y de su colección: distingue la Foundations declarada de una copia con los mismos nombres
  try {
    const v = await figma.variables.getVariableByIdAsync(id); if (!v) return null;
    if (!colCache.has(v.variableCollectionId)) colCache.set(v.variableCollectionId, await figma.variables.getVariableCollectionByIdAsync(v.variableCollectionId));
    const c = colCache.get(v.variableCollectionId);
    return { key: v.key || null, remote: !!v.remote, collectionKey: c ? c.key || null : null, collectionName: c ? c.name : null };
  } catch { return null; }
}
async function bindings(root) {
  const vars = new Set(), styles = new Set(), variableKeys = {}, styleKeys = {};
  const nodes = [root, ...('findAll' in root ? root.findAll(() => true) : [])];
  const addVar = async (prop, id) => { const name = await varName(id); vars.add(`${prop}: ${name}`); if (!variableKeys[name]) variableKeys[name] = await keyOf(id); };
  for (const n of nodes) {
    const bv = n.boundVariables || {};
    for (const [prop, val] of Object.entries(bv)) {
      const list = Array.isArray(val) ? val : [val];
      for (const b of list) if (b && b.id) await addVar(prop, b.id);
    }
    for (const paint of [...(Array.isArray(n.fills) ? n.fills : []), ...(Array.isArray(n.strokes) ? n.strokes : [])])
      if (paint.boundVariables?.color?.id) await addVar('color', paint.boundVariables.color.id);
    if (n.type === 'TEXT' && typeof n.textStyleId === 'string' && n.textStyleId) {
      const s = await figma.getStyleByIdAsync(n.textStyleId); if (s) { styles.add(s.name); styleKeys[s.name] = { key: s.key || null, remote: !!s.remote, type: 'text' }; }
    }
  }
  return { variables: [...vars], textStyles: [...styles], variableKeys, styleKeys };
}

async function nestedInstances(root) {
  const out = [];
  for (const inst of root.findAll(n => n.type === 'INSTANCE')) {
    const main = await inst.getMainComponentAsync();
    const refs = inst.componentPropertyReferences || {};
    out.push({
      layer: inst.name,
      component: main ? main.name : 'unknown',
      componentSet: main && main.parent && main.parent.type === 'COMPONENT_SET' ? main.parent.name : null,
      exposedAs: refs.mainComponent || null,   // nombre de la prop INSTANCE_SWAP que lo controla, o null
      toggledBy: refs.visible || null,          // nombre de la prop BOOLEAN que lo muestra/oculta, o null
      visibleByDefault: inst.visible
    });
  }
  return out;
}

const roots = page.findAllWithCriteria({ types: ['COMPONENT', 'COMPONENT_SET'] })
  .filter(n => !(n.type === 'COMPONENT' && n.parent && n.parent.type === 'COMPONENT_SET'))
  .filter(n => NODE_IDS.length === 0 || NODE_IDS.includes(n.id));

const out = { kind: 'components', fileKey: figma.fileKey || null, readAt: new Date().toISOString(),
  page: { id: page.id, name: page.name }, part: { offset: OFFSET, nextOffset: null, count: 0, total: roots.length, refresh: NODE_IDS.length > 0 },
  components: [] };
let size = JSON.stringify(out).length;
for (let i = OFFSET; i < roots.length; i++) {
  const n = roots[i];
  const defs = n.componentPropertyDefinitions || {};
  const properties = [];
  for (const [name, d] of Object.entries(defs)) {
    const p = { name, kind: d.type, default: d.defaultValue ?? null };
    if (d.type === 'VARIANT') p.values = d.variantOptions || [];
    if (d.type === 'INSTANCE_SWAP') {
      p.defaultComponent = typeof d.defaultValue === 'string' ? await nameOf(d.defaultValue) : null;
      p.preferredValues = (d.preferredValues || []).map(v => ({ type: v.type, key: v.key }));
    }
    properties.push(p);
  }
  const sample = n.type === 'COMPONENT_SET' ? (n.defaultVariant || n.children[0]) : n;
  const entry = ({
    page: page.name, name: n.name, type: n.type, id: n.id, key: n.key || null,
    // true/false si Figma expone si se publica con la librería (los nombres con «.» o «_» no se publican); null si no lo da.
    // Los COMPONENT_SET no tienen esa propiedad y leerla puede lanzar: se protege con try/catch (12.20.3).
    published: (() => { try { return typeof n.hiddenFromPublishing === 'boolean' ? !n.hiddenFromPublishing : null; } catch (e) { return null; } })(),
    description: unesc(n.description),
    variantAxes: n.type === 'COMPONENT_SET' ? Object.fromEntries(Object.entries(n.variantGroupProperties || {}).map(([k, v]) => [k, v.values])) : {},
    variantCount: n.type === 'COMPONENT_SET' ? n.children.length : 1,
    properties,
    nestedInstances: await nestedInstances(sample),
    bindings: await bindings(sample),
    autoLayout: sample.layoutMode && sample.layoutMode !== 'NONE'
  });
  const add = JSON.stringify(entry).length + 1;
  if (out.part.count > 0 && size + add > MAX_CHARS) { out.part.nextOffset = i; break; }
  out.components.push(entry);
  size += add;
  out.part.count++;
}
return out;
```

Con esta salida, un componente **tiene icono** si alguna `properties[].kind === 'INSTANCE_SWAP'`
o alguna `nestedInstances[].component` pertenece a la familia de iconos del DS. Ambas cosas
se vuelcan al schema (`api.props`, `figma.nestedInstances`, `api.icons`, `relations.uses`).
Si un icono anidado no tiene `exposedAs`, el componente incumple la regla «icono =
`INSTANCE_SWAP`»: se registra igualmente en el schema y se abre hallazgo de auditoría.
</details>

---
