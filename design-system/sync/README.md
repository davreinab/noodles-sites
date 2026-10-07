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
- **Los artefactos no se editan a mano.** Si algo sale mal, se corrige el volcado (releyendo
  Figma) o se abre un hallazgo; nunca el resultado.
- Formato exacto de cada archivo: cabecera de los scripts de lectura en `design.md § Sync` y
  docstring de `scripts/ds-sync.py`.
