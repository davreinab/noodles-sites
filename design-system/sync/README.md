# `sync/` — volcados de Figma (entrada del motor de sync)

Aquí deja el agente **lo que lee de Figma por el MCP oficial**, tal cual, en JSON. Es la
única entrada de `scripts/ds-sync.py`, que a partir de estos archivos regenera de forma
determinista todos los artefactos ⚙️ del design system (tokens, docs, schemas, índice,
relaciones, assets, showcase y drift). Mismo volcado → mismo resultado, con cualquier LLM.

| Archivo | Qué contiene | Cómo se obtiene |
|---|---|---|
| `variables.json` | Colecciones, modos y variables (valor por modo, alias, scopes, descripción), text styles y effect styles | Script «lectura de variables y estilos» de `design.md § Sync`, una ejecución por archivo de tokens |
| `components.json` | Páginas y componentes: propiedades completas, ejes de variante, instancias anidadas (incluidas invisibles), bindings | Script «lectura de componentes» de `design.md § Sync`, una ejecución por página; el agente acumula las páginas |
| `icons.json` | Iconos exportados a `../assets/icons/`: `[{ "name", "nodeId", "file", "usage" }]`. Opcional | Al exportar los SVG con el MCP, el agente registra cada uno aquí |
| `parts/*.json` | Los trozos tal como llegan del MCP, mientras dura la lectura | Cada respuesta de los scripts de lectura, guardada sin tocar. `ds-sync.py --merge` los une en `variables.json` y `components.json` y los borra |

Reglas:

- **Por trozos, porque el MCP corta.** `use_figma` corta cada respuesta hacia los 20 KB. Los
  scripts de lectura devuelven trozos de unos 14 KB con su posición; el agente guarda cada uno
  en `parts/` en la misma vuelta en que llega, sin modificarlo y sin pegarlo en la conversación.
  La unión es del script: es determinista y comprueba que no falte ni sobre ningún trozo.
- **Solo escribe aquí el agente, y solo con datos leídos del MCP.** Nada se rellena a mano ni
  se inventa: si Figma no da un dato, el campo va vacío o `null` y el motor escribe `unknown`.
- **Se sobreescriben en cada sync, no en cada tanda.** Son la foto de Figma en ese momento; se
  versionan en git para poder ver qué cambió en Figma entre dos syncs
  (`git diff design-system/sync/`). Como la extracción va **por tramos** (un archivo por tanda
  y, si es grande, una página por tanda — ver `design.md § Sync`, paso 1b), cada tanda
  **acumula** sobre lo ya volcado en ese mismo ciclo: `--merge` añade las colecciones de cada
  archivo de tokens y cada página a `pages[]` sin tocar lo de las tandas anteriores. Releer un
  archivo o una página desde `OFFSET = 0` sustituye solo eso.
- **Un volcado a medias se declara.** Mientras falten fuentes o páginas acordadas, el resumen
  al usuario dice cuáles y el paso queda abierto. Los artefactos generados con un volcado
  parcial describen solo lo leído; no se presentan como el DS completo.
- **Un componente suelto se refresca con `NODE_IDS`** en el script de lectura (`design.md § Sync`,
  paso 3): el trozo lleva `part.refresh` y `ds-sync.py --merge` sustituye solo esos componentes por
  id en su página, anotándolo en `partialRefresh.history`. No se edita la entrada del volcado a mano.
- **Una variable suelta se refresca con `VARIABLE_IDS` o `VARIABLE_NAMES`** en el script de variables:
  lee solo esas, `--merge` las sustituye o añade por id en `variables.json` y resuelve sus alias contra
  el volcado completo; avisa de las que no existen en Figma. Una variable nueva cuesta una llamada.
- **Sync incremental: primero pregunta qué ha cambiado.** El «script de huellas de variables» (`design.md`
  § Sync) devuelve en una llamada `[id, huella]` de cada variable; se guarda en `parts/fingerprints-001.json`
  y `python3 scripts/ds-sync.py --variables-diff` lo compara con `variables.json`: dice las cambiadas, las
  nuevas y las desaparecidas, imprime la línea `VARIABLE_IDS` para el refresco puntual y prepara la retirada
  de las desaparecidas (`part.removed`, la aplica `--merge`). Sin cambios, no hay nada que releer. La
  relectura completa queda para la primera vez.
- **Librerías ligadas.** `library-audit/<fileKey>-<NNN>.json` es la salida del «script de auditoría de
  librerías ligadas» (`design.md § Sync`, 3c): qué componentes ligan variables o estilos de una librería
  que no es la Foundations declarada. El sync abre un hallazgo crítico por componente mientras esté ahí;
  se vuelve a ejecutar tras arreglarlo en Figma (Swap library).
- **Un volcado de variables a medias no llega a los artefactos.** `--merge` exige la cadena entera
  (trozo 0 … `nextOffset: null`, `read == total`): a medias, error sin escribir (o, si el merge viene de
  un refresco de componentes, aparta esos trozos y conserva `variables.json`). Y `ds-sync.py` se niega a
  escribir un `tokens.css` con más de un 10 % menos de tokens que el actual salvo `--allow-fewer-tokens`.
- **Los artefactos no se editan a mano.** Si algo sale mal, se corrige el volcado (releyendo
  Figma) o se abre un hallazgo; nunca el resultado.
- Formato exacto de cada archivo: cabecera de los scripts de lectura en `design.md § Sync` y
  docstring de `scripts/ds-sync.py`.
