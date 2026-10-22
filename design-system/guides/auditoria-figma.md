# Auditoría del DS en Figma  🔍  (informe + remediación asistida)

> Guía de `design-system/design.md`: se lee solo cuando la tarea lo pide (la tabla de «Enrutado» de `design.md` dice cuándo).

**Cuándo:** al registrar por primera vez las fuentes de Figma, tras cambios grandes en
el DS, o cuando el usuario pida "auditar el design system". La auditoría es de **solo
lectura** y no requiere aprobación; cualquier corrección posterior sí. No confundir con
el informe de drift: el drift compara Figma con los artefactos generados; la auditoría
evalúa la calidad del **propio Figma**.

### Alcance multi-archivo

El DS puede repartirse entre varios archivos. Antes de evaluar nada:

1. Enumera todas las fuentes registradas en el encabezado de `design.md` y determina el **rol real** de cada una
   (tokens, estilos, componentes, patrones, iconos, documentación) leyendo su contenido;
   el rol declarado por el usuario tiene prioridad y las discrepancias se reportan.
2. Evalúa cada archivo **solo contra las reglas propias de su rol**. Que un archivo
   contenga únicamente variables y ningún componente **no es un hallazgo**: la cobertura
   se evalúa sobre el conjunto.
3. El informe final consolida el conjunto: cobertura global (tokens, tipografía,
   componentes, patrones, iconos), dependencias entre archivos (qué librerías se
   publican y quién las consume), duplicidades y contradicciones entre archivos. Solo es
   hallazgo de cobertura lo que falte en **todo** el conjunto, no en un archivo suelto.

### Qué se comprueba

**A. Estándares propios del equipo** — las "Reglas duras" y "Reglas duras en Figma" de
este documento, aplicadas según el modo de adopción registrado en el encabezado de `design.md`: con
`preserve-existing` o `pending-inspection`, las desviaciones estructurales se reportan
como hallazgos informativos, nunca como órdenes de corrección.

**B. Buenas prácticas generales de DS en Figma**, como mínimo:

- **Nomenclatura**: ninguna página, frame, grupo, capa, componente, variante o variable
  sin nombre o con nombre genérico ("Frame 123", "Group 7", "Rectangle 40"); una sola
  convención coherente (idioma, casing, separadores, jerarquía `/`, variantes
  `Propiedad=Valor`) en todo el conjunto de archivos, no solo dentro de cada uno.
- **Vinculación a estilos/variables**: todo color, texto, efecto, radio, spacing y
  tipografía ligado a una variable o estilo; se reporta cualquier valor local,
  hardcodeado o estilo desanexado, con la variable/estilo candidato cuando exista.
- **Componentización**: variantes agrupadas en component sets (no componentes duplicados
  sueltos); propiedades de componente (boolean, text, instance swap) en lugar de capas
  ocultas ad hoc; sin instancias desanexadas reconstruidas a mano; descripciones de
  componente rellenas; base components y organización por página/sección con criterio.
- **Candidatos a slot**: variantes cuyos valores son tipos de contenido
  (`Contenido=Imagen`, `Contenido=Lista`) o hijos alternativos en la misma zona encendidos
  por booleanos. Hallazgo `assisted`, con el recuento de instancias afectadas; cómo se
  migra está en `figma.md § 3-ter`.
- **Estructura**: Auto Layout en todo contenedor estructural; constraints coherentes;
  sin capas ocultas basura ni elementos sueltos fuera de frames.
- **Higiene de librería**: estilos y variables sin uso, duplicados de valor idéntico
  bajo nombres distintos, y estados de publicación incoherentes entre archivos.

### Informe

La auditoría regenera dos artefactos (⚙️ generados, no editar a mano):

- `reports/audit-report.json` — hallazgos estructurados para máquinas.
- `reports/audit-report.md` — informe legible: estado por archivo, estado del conjunto
  y, **por cada hallazgo: qué está mal, por qué importa y cómo corregirlo** paso a paso.

Cada hallazgo registra la regla evaluada, su origen (`skill` o `general`), severidad
(`critical` / `warning` / `info`), archivo y nodo o variable afectados, recomendación
accionable y **fixability**: `auto` (mecánico y determinista), `assisted` (requiere una
decisión de diseño) o `manual` (solo puede resolverlo una persona).

### Remediación asistida (opt-in, nunca automática)

Tras entregar el informe, ofrece al usuario que la IA aplique correcciones en Figma:

1. Propón un plan por lotes: primero los `auto` (renombrados según la convención
   acordada, scopes y descripciones, bindings a variables existentes cuando el candidato
   es inequívoco), después los `assisted` uno a uno con su decisión pendiente.
2. Cada lote se muestra y se aprueba **antes** de escribir en Figma (capacidad
   `apply-audit-mechanical-fixes`, aprobación por lote). Los cambios estructurales
   (crear o cambiar tokens y componentes, fusiones, migraciones) siguen las aprobaciones
   de "Gobierno agentic y confianza gradual": nunca entran en un lote mecánico.
3. En modo `preserve-existing`, ningún renombrado ni cambio estructural entra en un plan
   de fixes sin la decisión explícita de reestructuración; solo scopes y descripciones.
4. Tras aplicar los lotes, re-ejecuta la auditoría sobre lo corregido y actualiza ambos
   informes: los hallazgos resueltos pasan a `fixed` y los asumidos a `accepted`.

Si el entorno no dispone del MCP oficial de Figma, la auditoría queda **pendiente**: no
simules lecturas ni generes hallazgos inventados.

---
