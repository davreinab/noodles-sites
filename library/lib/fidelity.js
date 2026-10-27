// Avisos de fidelidad (scripts/ds-fidelity.py → design-system/reports/fidelity.json) explicados para quien los lee en el tablero y en la ficha:
// qué es cada uno, por qué importa y qué hacer (esto último lo escribe el propio script en `suggestion`). Los avisos de severidad `info` son NOTAS:
// no son un fallo ni piden nada, y no cuentan como «pide atención».
import fs from "node:fs";

export const CODES = {
  "token-not-used": ["El CSS no usa un token que el maestro sí liga", "El componente puede verse distinto del diseño."],
  "variant-without-css": ["Una variante del contrato no tiene CSS", "Si alguien la elige, se verá igual que la normal."],
  "example-class-missing": ["El ejemplo usa una clase que no existe en el CSS", "La muestra no se verá como debería."],
  "example-external-image": ["El ejemplo carga una imagen de fuera", "Se rompe sin conexión y no forma parte del sistema."],
  "example-placeholder-ellipsis": ["El ejemplo usa «…» como contenido", "La vista previa sale vacía."],
  "variant-not-in-example": ["El ejemplo no muestra todas las variantes", "Lo que no se ve en el ejemplo no se puede revisar."],
  "variant-coverage-unchecked": ["No se puede comprobar si una variante sale en el ejemplo", "No es un fallo: la herramienta no sabe cómo se pinta esa variante. Si importa, se declara en ds-fidelity.config.json."],
  "example-without-data-ds": ["El ejemplo no marca su elemento raíz con data-ds", "Sin la marca no se sabe qué contrato es cada bloque cuando se usa en una pantalla."],
  "screen-uses-unverified": ["Una pantalla usa un componente sin verificar", "Hay que compararlo con su maestro antes de usarlo."],
  "screen-uses-internal": ["Una pantalla usa una pieza interna de Figma", "Las piezas internas no forman parte del sistema compartido."],
  "screen-state-anatomy": ["Una pantalla monta un estado incompleto", "El contrato dice qué debe llevar ese estado."],
  "screen-without-data-ds": ["Elementos de una pantalla sin data-ds", "Sin la marca no se sabe qué contrato es cada bloque."],
  "screen-data-ds-mismatch": ["Un data-ds que no corresponde al elemento", "La marca nombra otro componente."],
  "contrast-below-aa": ["Contraste por debajo de AA", "El texto puede ser difícil de leer; AA es obligatorio."],
};

const textos = (code) => CODES[code] || [code, ""];

// {report, byComp: Map(slug → {warnings: [...], notes: [...]})}. Cada elemento: {code, title, why, severity, value, suggestion}.
export function loadFidelity(file, knownSlugs) {
  let report = null;
  try {
    report = JSON.parse(fs.readFileSync(file, "utf8"));
  } catch {
    return { report: null, byComp: new Map() };
  }
  const byComp = new Map();
  for (const f of Array.isArray(report.findings) ? report.findings : []) {
    const slug = f.property;
    if (!slug || (knownSlugs && !knownSlugs.has(slug))) continue;
    const [title, why] = textos(f.code);
    const item = { code: f.code, title, why, severity: f.severity, value: f.value, suggestion: f.suggestion || "" };
    const cur = byComp.get(slug) || { warnings: [], notes: [] };
    (f.severity === "info" ? cur.notes : cur.warnings).push(item);
    byComp.set(slug, cur);
  }
  return { report, byComp };
}
