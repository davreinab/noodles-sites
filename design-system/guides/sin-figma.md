# Diseñar sin Figma  ✏️  (modo repo)

> Guía de `design-system/design.md`: se lee solo cuando la tarea lo pide (la tabla de «Enrutado» de `design.md` dice cuándo).

`agent-manifest.json → sourceMode: "repo"`. La fuente es `design-system/source/` (formato en su `README.md`); el sync la
compila al mismo volcado que Figma, así que tokens, contratos, fichas y library salen igual y son exportables para desarrollo.

- **Tokens**: `source/tokens.json`, tres colecciones con la cadena Components → Semantic → Primitive. Los componentes usan
  tokens semánticos. `python3 scripts/ds-source.py --check` valida tipos, alias y ciclos.
- **Componentes**: `source/components/<slug>.json` con props, slots, eventos, estados, anatomía por capas e interacciones.
  Sin los límites de Figma; lo que Figma no expresa sale como «gap» en `python3 scripts/ds-source.py --figma-plan`.
- **No se editan a mano** los contratos, tokens ni fichas generadas: se edita la fuente y se ejecuta `ds-sync.py`.
  Descripción y criterio de uso de un componente siguen siendo propuesta con aprobación.
- **Menos lectura**: en modo repo no se leen las guías de Figma (`sync-figma`, `reglas-figma`, `auditoria-figma`); `design.md` es solo
  el router y las reglas duras. `python3 scripts/ds-budget.py` mide cuánto cuesta leer el proyecto y avisa si pasa del presupuesto.
- **Borrador y publicado**: sin publicación el DS es un borrador y se edita sin propuestas; la primera
  `ds-release.py --apply` lo declara publicado. Desde ahí, cambiar o retirar algo ya publicado exige propuesta aprobada
  (`ds-release.py --check`); añadir no.
- **Qué es componente**: se usa en 2+ pantallas, tiene variantes, estados o es interactivo. Si no, es una sección de
  pantalla y se queda en `UI/`. `ds-extract.py` propone con el motivo; decide una persona.
- **Desde prototipos**: los prototipos de diseño viven solo en `UI/`. `python3 scripts/ds-extract.py` deja un borrador en
  `source/_borrador/`; se propone, y con aprobación `--promote` lo pasa a la fuente. Tras el sync,
  `python3 scripts/ds-extract.py --verify` exige contrato, ficha `.md` y library para cada componente de `UI/`.
