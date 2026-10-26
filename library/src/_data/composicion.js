// Reglas de composición de pantalla: se leen de design-system/docs/patterns.md (§ Composición de pantalla) en cada build, así que la
// library muestra siempre lo que dice el documento. No se escribe nada aquí.
import fs from "node:fs";
import path from "node:path";
import MarkdownIt from "markdown-it";

const md = new MarkdownIt({ html: false, linkify: true });
md.core.ruler.push("demote-headings", (state) => {
  for (const t of state.tokens) {
    if (t.type === "heading_open" || t.type === "heading_close") t.tag = "h" + Math.min(6, Number(t.tag[1]) + 1);
  }
});

export default function () {
  let text = "";
  try {
    text = fs.readFileSync(path.resolve("..", "design-system", "docs", "patterns.md"), "utf8");
  } catch (e) {
    return { found: false, pending: 0, preset: false, html: "" };
  }
  const m = text.match(/^## Composición de pantalla([^\n]*)\n([\s\S]*?)(?=^## |$(?![\s\S]))/m);
  if (!m) return { found: false, pending: 0, preset: false, html: "" };
  const pending = (m[2].match(/⬜ TODO/g) || []).length;
  return {
    found: true,
    pending,
    preset: /norma de la base inicial/.test(m[1]),
    html: md.render(m[2]),
  };
}
