# GB Noodles · Microsites DS · `schemas/` — representación estructurada para IA

Estos JSON son contratos legibles por máquina del design system GB Noodles · Microsites. El agente
entra por `../agent-manifest.json` y carga únicamente el recurso y las dependencias que
necesita; no debe leer todo el sistema por defecto.

- **La documentación Markdown** (`../design.md` y `../docs/*.md`) es para **personas**.
  `../tokens/tokens.json` representa los tokens para máquinas y los JSON de esta carpeta
  representan contratos de componentes para **IA**.
- Ambos describen el mismo DS y **deben mantenerse sincronizados**: Figma → sync →
  `docs/tokens.md` / `tokens/tokens.json` / `tokens/tokens.css` → contratos y schemas.
- **Cada dato tiene un solo dueño.** Lo que sale de Figma (propiedades, variantes, iconos,
  tokens) lo escribe `ds-sync.py` en los dos lados a la vez desde el mismo volcado. El
  **criterio escrito a mano** (propósito, accesibilidad, cuándo usar, qué no hace) vive
  **solo** en su ficha `../docs/components/<slug>.md` o `../docs/patterns/<slug>.md`: el schema no lo
  copia, lo señala con `source.docs` (`file` + `section`). Única excepción, sincronizada por
  el script: el «Ejemplo de código» del `.md` se copia a `source.code.example`.
- Aquí solo hay tres archivos sueltos (`_component.schema.json`, `index.json`,
  `relationships.json`) y dos carpetas: `governance/` (reglas del sistema) y `components/`
  (un contrato por componente). Nada más se coloca en esta raíz.

## Reglas de contenido

- Nada se inventa. Lo no determinable en la fuente se marca con el string `"unknown"`.
- Se prefiere estructura y `enum` sobre texto libre.
- Todo dato sincronizado incluye procedencia, fecha y versión cuando estén disponibles.
- Los aliases conservan su referencia y también el valor final resuelto.

## Estructura del folder

| Archivo | Qué es |
|---|---|
| `_component.schema.json` | Contrato que valida todos los JSON de componentes y patterns. |
| `index.json` | Registro y router de componentes con ruta, tipo y dependencias. |
| `relationships.json` | Relaciones componente↔componente (usa / compone / relacionado). |
| `governance/policies.json` | Normas comprobables y su severidad. |
| `governance/constraints.json` | Restricciones de tokens, layout, nombres y composición. |
| `governance/capabilities.json` | Acciones automáticas y acciones que requieren aprobación humana. |
| `governance/maturity.json` | Nivel agentic alcanzado y criterios pendientes. |
| `components/<slug>.schema.json` | Contrato para máquinas por componente o pattern: lo comprobable (API, iconos, tokens, relaciones) y `source.docs`, que apunta a su criterio en el `.md`. Referencia el meta-schema con `"$schema": "../_component.schema.json"`. |

## Sincronización

Cuando cambie el DS en Figma, regenera los datos derivados, valida todos los contratos y
actualiza el informe de drift. La parte de criterio solo cambia mediante revisión humana, y
solo en el `.md`.
