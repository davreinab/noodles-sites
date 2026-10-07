# Dirección visual — GB Noodles · Microsites

Fase entre la lógica (`context/`, wireframes) y el estilo (design system). Aquí se decide
**cómo debe verse y sentirse** el producto antes de crear un solo token. Es juicio humano:
elegir referencias y decir por qué importan. Lo que cambia respecto al moodboard clásico es
que todo queda **escrito para que lo lea un agente** en cada iteración posterior.

## Qué hay aquí

| Archivo | Qué es | Quién lo escribe |
|---|---|---|
| [`DESIGN.md`](./DESIGN.md) | La dirección codificada: tono, paleta (intención), tipografía (intención), patrones de interacción recurrentes, referencias seleccionadas. | Diseño, a mano. `✍️ manual` |
| [`references/`](./references/) | El moodboard: una imagen por referencia **más una nota** con el mismo nombre (`.md`) que dice qué destaca y qué se traslada. Sin nota, la referencia no cuenta. | Diseño; la descripción de la imagen puede generarla un modelo visual, la observación personal no. |
| [`references/_referencia.template.md`](./references/_referencia.template.md) | Plantilla de la nota de referencia. | — |

## Reglas

- **Una referencia = imagen + nota.** Nombre común: `NN-<slug>.png` y `NN-<slug>.md`. Una
  imagen sin nota no forma parte de la dirección.
- **De todas las referencias, una selección.** No toda referencia recogida merece ser
  dirección. `DESIGN.md § Referencias seleccionadas` lista solo las que mandan, con el motivo.
- **`DESIGN.md` describe intención, no valores.** Dice «acento cálido, poco saturado, un
  solo color de marca», no `#E07A3F`. Los valores nacen **en Figma** como tokens (regla 2 de
  `design-system/design.md`) y llegan al código por sync. `DESIGN.md` es lo que se lee antes
  de crearlos y lo que permite comprobar después que los tokens cumplen la intención.
- **El agente lo lee antes de proponer cualquier estilo**: antes del primer sync de un DS
  nuevo, antes de una pantalla de UI y antes de refinar por prompts. Si `DESIGN.md` está en
  `⬜ TODO`, no inventa una dirección: lo dice y pide referencias.
- **Se revisa cuando cambia la dirección**, no cuando cambia un token. Los cambios de valor
  van a Figma; los cambios de intención vienen aquí primero.
- Las imágenes son las únicas que viven fuera de `design-system/assets/`: son referencias
  externas, no assets del producto. No se usan en pantallas.
