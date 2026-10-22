// Servidor local de propuestas: solo existe mientras corre `npm start` en el ordenador de alguien.
// El visor publicado como web estática no lo tiene, y entonces el botón descarga la propuesta.
//   GET  /__ds/ping      → { ok: true }
//   POST /__ds/proposal  → { slug, field, text, reason, approver } → crea o edita la propuesta pendiente
// Escribe solo en design-system/proposals/ y después regenera el índice y el catálogo.
import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { textProposal, isPending, belongsTo } from "../src/assets/viewer/proposal.js";

const SLUG_RE = /^[\w-]+$/;

// El .json generado de cada patrón lleva «sheet.edit.current»: los textos vigentes, sacados del repo por
// scripts/ds-library.py. Se leen de ahí para no fiarse del valor que mande el navegador.
const findPatternJson = (dir, slug) => {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) {
      const hit = findPatternJson(p, slug);
      if (hit) return hit;
    } else if (e.name === `${slug}.json` && path.basename(dir) === slug) return p;
  }
  return null;
};

const send = (res, status, body) => {
  res.writeHead(status, { "Content-Type": "application/json; charset=utf-8" });
  res.end(JSON.stringify(body));
};

const readBody = (req) =>
  new Promise((resolve, reject) => {
    let raw = "";
    req.on("data", (c) => {
      raw += c;
      if (raw.length > 200_000) reject(new Error("demasiado grande"));
    });
    req.on("end", () => resolve(raw));
    req.on("error", reject);
  });

export function proposalsMiddleware(projectRoot) {
  const ds = path.join(projectRoot, "design-system");
  const dir = path.join(ds, "proposals");
  return async (req, res, next) => {
    if (!req.url.startsWith("/__ds/")) return next();
    if (req.method === "GET" && req.url === "/__ds/ping") return send(res, 200, { ok: true });
    if (req.method !== "POST" || req.url !== "/__ds/proposal") return send(res, 404, { ok: false, error: "no existe" });
    try {
      const edit = JSON.parse(await readBody(req));
      edit.origin = "person"; // lo que llega del visor lo ha escrito una persona
      if (!SLUG_RE.test(edit.slug || "")) return send(res, 400, { ok: false, error: "componente no válido" });
      if (!String(edit.reason || "").trim()) return send(res, 400, { ok: false, error: "falta el motivo del cambio" });
      const pj = findPatternJson(path.join(projectRoot, "library", "src", "patterns"), edit.slug);
      const info = pj && (JSON.parse(fs.readFileSync(pj, "utf8")).sheet || {}).edit;
      if (!info) return send(res, 404, { ok: false, error: "ese componente no está en el catálogo" });
      if (!Object.prototype.hasOwnProperty.call(info.current || {}, edit.field || "description"))
        return send(res, 400, { ok: false, error: "ese campo no se puede editar" });
      // Solo las pendientes, que viven sueltas en la raíz de proposals/ (las decididas están en subcarpetas).
      let existing = null, existingFile = null;
      for (const f of fs.readdirSync(dir).filter((x) => x.endsWith(".proposal.json"))) {
        try {
          const p = JSON.parse(fs.readFileSync(path.join(dir, f), "utf8"));
          if (belongsTo(p, edit.slug) && isPending(p)) { existing = p; existingFile = f; break; }
        } catch { /* una propuesta ilegible no bloquea; la marcará proposals-index */ }
      }
      const p = textProposal(existing, info, edit, new Date().toISOString());
      const file = existingFile || `${p.id}.proposal.json`;
      fs.writeFileSync(path.join(dir, file), JSON.stringify(p, null, 2) + "\n");
      for (const script of ["proposals-index.py", "ds-library.py"]) {
        const r = spawnSync("python3", [path.join(projectRoot, "scripts", script)], { cwd: projectRoot, encoding: "utf8" });
        if (r.status !== 0 && script === "proposals-index.py") console.warn(`[propuestas] ${script}: ${r.stdout}${r.stderr}`);
      }
      console.log(`[propuestas] ${existing ? "editada" : "creada"} design-system/proposals/${file}`);
      return send(res, 200, { ok: true, created: !existing, id: p.id, file: `design-system/proposals/${file}` });
    } catch (e) {
      return send(res, 500, { ok: false, error: String(e.message || e) });
    }
  };
}
