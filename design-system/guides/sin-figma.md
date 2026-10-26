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

## Empezar con la base y pasar a Figma más tarde

- **La base inicial.** Un proyecto nuevo que diseña en el repo puede empezar con una base ya construida: unas cuatro docenas de
  componentes y todos los tokens, con su ficha completa (propósito, ejemplo, accesibilidad, cuándo usar). Lo dice `starterBase` en
  `agent-manifest.json`: `basic` si se cargó, `none` si se empezó vacío, `not-applicable` si el proyecto ya tenía design system cuando
  existía la opción. La base no se carga a posteriori ni en un proyecto que ya usaba init-proyecto: no la pidas ni la copies.
- **Cámbiala por la tuya.** Los valores de relleno (la escala de marca y las dos familias tipográficas) llevan `placeholder: true` en
  `source/tokens.json`. Cambia esos valores por los reales de la marca, quita la marca `placeholder` y todo lo demás se adapta, porque los
  componentes solo usan tokens semánticos. `ds-release.py` no publica mientras quede alguno.
- **Qué piezas son tuyas.** Los componentes de la base son un punto de partida, no un estándar: edítalos en `source/components/` y en
  `css/components.css`, o quita los que no necesites (borra su archivo de `source/components/`, su ficha y su sección del CSS) antes de publicar.
- **Pasar a Figma más tarde.** Cuando el sistema esté listo para vivir en Figma: (1) `python3 scripts/ds-source.py --figma-plan` escribe el plan
  (`reports/figma-plan.json`) con colecciones, variables, componentes y lo que Figma no puede expresar; (2) un agente lo construye en Figma con
  las skills de Figma y el MCP oficial; (3) se registran las fuentes de Figma en `agent-manifest.json → figmaSources` y se verifica el MCP;
  (4) `python3 scripts/ds-source.py --switch-to-figma` cambia `sourceMode` a `figma` y deja `source/` como histórico; (5) el primer sync leyendo
  Figma hace caducar la verificación de cada contrato, y hay que volver a pasar el protocolo de verificación contra el maestro. Desde ese momento
  Figma es la fuente de verdad y lo que se haya diseñado solo en el repo, por encima de lo que Figma puede expresar, se pierde: el plan lo lista.
