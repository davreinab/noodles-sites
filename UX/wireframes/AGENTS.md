# Wireframes — Reglas técnicas

Reglas de implementación de los HTML de esta carpeta. Para contexto de producto, ver
[`../../context/`](../../context/) — sigue siempre
[`business-rules.md`](../../context/business-rules.md).

### Escritura de archivos HTML
- Siempre usar Python `open().write()` para escribir archivos. **Nunca** bash heredoc —
  trunca los paths SVG.

### Paleta
- Solo tokens `--wf-*` del kit de wireframing de Multiplica (grises + estados). Nada de la
  marca del producto ni de los tokens del DS. La dirección visual
  ([`../direction/DESIGN.md`](../direction/DESIGN.md)) **no** se aplica aquí: los wireframes
  son lógica y estructura, no estilo.

### Móvil
- Si [`../mobile-environment.md`](../mobile-environment.md) dice `Aplica: sí`, todo
  wireframe móvil se construye dentro del contenedor con las dimensiones y zonas seguras
  que declara ese archivo, y respeta sus gestos y navegación. Léelo antes de empezar.

<!-- A medida que los wireframes evolucionen, documentar aquí (este archivo es vivo):
     estructura CSS de cada página, patrones de modal/panel, escalera de z-index,
     mecanismo de animación, reglas de propagación entre páginas y gotchas. -->
