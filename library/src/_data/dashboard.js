// Home dashboard: what the design system's components are asking for today.
// It reads the repo at build time (contracts, proposals, lifecycle, sync dumps, fidelity report) and the
// generated catalogue (src/patterns/**.json, written by scripts/ds-library.py). Nothing here is stored:
// `npm start` rebuilds it on every change, so the home never goes stale and `ds-library.py --check`
// has nothing to compare. Everything is per component: the project-wide governance stays out on purpose.
import fs from "node:fs";
import path from "node:path";
import { loadFidelity, CODES } from "../../lib/fidelity.js";

const LIB = path.resolve("src/patterns");
const DS = path.resolve("../design-system");

const readJson = (p, fallback = null) => {
  try {
    return JSON.parse(fs.readFileSync(p, "utf8"));
  } catch {
    return fallback;
  }
};
const mtime = (p) => {
  try {
    return fs.statSync(p).mtime.toISOString();
  } catch {
    return null;
  }
};
const isDir = (p) => {
  try {
    return fs.statSync(p).isDirectory();
  } catch {
    return false;
  }
};

const MONTHS = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"];
const fmtDate = (iso, withTime = false) => {
  if (!iso) return null;
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return String(iso);
  const date = `${d.getDate()} ${MONTHS[d.getMonth()]} ${d.getFullYear()}`;
  if (!withTime || !/T/.test(String(iso))) return date;
  const hh = String(d.getHours()).padStart(2, "0");
  const mm = String(d.getMinutes()).padStart(2, "0");
  return `${date} · ${hh}:${mm}`;
};
const daysSince = (iso) => {
  if (!iso) return null;
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return null;
  return Math.max(0, Math.floor((Date.now() - d.getTime()) / 86400000));
};
const agoLabel = (iso) => {
  const n = daysSince(iso);
  if (n === null) return "";
  if (n === 0) return "hoy";
  if (n === 1) return "hace 1 día";
  return `hace ${n} días`;
};

// ── the catalogue: one entry per component, with its url in the viewer ──
function walkPatterns() {
  const out = [];
  if (!isDir(LIB)) return out;
  for (const level of fs.readdirSync(LIB)) {
    const levelDir = path.join(LIB, level);
    if (!isDir(levelDir) || level.startsWith("_")) continue;
    const walk = (dir, segments, groupTitle) => {
      const name = segments[segments.length - 1];
      const own = path.join(dir, `${name}.json`);
      if (segments.length && fs.existsSync(own) && fs.existsSync(path.join(dir, `${name}.njk`))) {
        const meta = readJson(own, {});
        if (!meta || typeof meta !== "object" || !meta.ds || !meta.ds.slug) return;
        out.push({
          slug: meta.ds.slug,
          title: meta.title || name,
          url: `/patterns/${level}/${segments.join("/")}/`,
          level,
          group: groupTitle || "",
          status: meta.status || null,
          kind: meta.ds.kind || "component",
          verification: meta.ds.verification || "unverified",
          interno: segments.includes("internos-de-figma"),
          parte: segments.includes("partes-de-otro-componente"),
          sheet: meta.sheet && typeof meta.sheet === "object" ? meta.sheet : null,
        });
        return;
      }
      const g = readJson(path.join(dir, "_group.json"), null);
      const title = g && g.title ? g.title : segments.length ? name : "";
      for (const child of fs.readdirSync(dir)) {
        const p = path.join(dir, child);
        if (isDir(p) && !child.startsWith("_")) walk(p, [...segments, child], segments.length ? title : title);
      }
    };
    walk(levelDir, [], "");
  }
  return out;
}

export default function () {
  const comps = walkPatterns();
  const bySlug = new Map(comps.map((c) => [c.slug, c]));
  const manifest = readJson(path.join(DS, "agent-manifest.json"), {}) || {};
  const sourceByKey = new Map((manifest.figmaSources || []).map((s) => [s.fileKey, s.name]));

  // ── contracts ──
  for (const c of comps) {
    const sch = readJson(path.join(DS, "schemas", "components", `${c.slug}.schema.json`), null);
    c.contract = sch;
    const meta = (sch && sch.meta) || {};
    const ver = meta.verification || {};
    c.verStatus = ver.status || "unverified";
    c.verDate = ver.date || null;
    c.verReason = ver.reason || null;
    c.staleSince = ver.staleSince || null;
    c.figmaPage = meta.figmaPage || (c.sheet && c.sheet.figma && c.sheet.figma.page) || "";
    c.fileName = sourceByKey.get((sch && sch.figma && sch.figma.fileKey) || "") || "";
    c.hasExample = !!(sch && sch.code && sch.code.example);
    c.lifecycle = (meta.lifecycle && meta.lifecycle.status) || "active";
  }

  // ── proposals: pending = draft (waiting for a decision) + approved (waiting to be applied) ──
  const propDir = path.join(DS, "proposals");
  const proposals = [];
  if (isDir(propDir)) {
    for (const f of fs.readdirSync(propDir)) {
      if (!f.endsWith(".proposal.json")) continue;
      const p = readJson(path.join(propDir, f), null);
      if (!p || !p.id) continue;
      const pc = p.proposedChange && typeof p.proposedChange === "object" ? p.proposedChange : {};
      const slugs = []
        .concat(pc.component || [], pc.components || [])
        .filter((s) => typeof s === "string" && bySlug.has(s));
      const changes = Array.isArray(pc.changes) ? pc.changes : [];
      proposals.push({
        id: p.id,
        file: `design-system/proposals/${f}`,
        status: p.status,
        date: /^\d{4}-\d{2}-\d{2}/.test(p.id) ? p.id.slice(0, 10) : null,
        summary: p.summary || "",
        approver: p.requiredApprover || "",
        kind: pc.kind || "",
        isText: pc.kind === "component-text",
        byAI: changes.some((ch) => ch && ch.origin === "ai"),
        fields: changes.map((ch) => ch && ch.field).filter(Boolean),
        components: slugs.map((s) => ({ slug: s, title: bySlug.get(s).title, url: bySlug.get(s).url })),
      });
    }
  }
  const pendingProposals = proposals.filter((p) => p.status === "draft").sort((a, b) => (b.date || "").localeCompare(a.date || ""));
  const approvedProposals = proposals.filter((p) => p.status === "approved").sort((a, b) => (b.date || "").localeCompare(a.date || ""));
  const propsByComp = new Map();
  for (const p of [...pendingProposals, ...approvedProposals]) for (const c of p.components) propsByComp.set(c.slug, (propsByComp.get(c.slug) || []).concat(p));

  // ── lifecycle: retirements in progress ──
  const lc = readJson(path.join(DS, "schemas", "governance", "lifecycle.json"), {}) || {};
  const policy = lc.policy || {};
  const retirements = (lc.deprecations || []).map((e) => {
    const c = bySlug.get(e.id) || null;
    const since = e.since ? new Date(e.since) : null;
    const block = since && Number.isFinite(policy.blockNewUsageFromDay) ? new Date(since.getTime() + policy.blockNewUsageFromDay * 86400000) : null;
    return {
      slug: e.id,
      title: c ? c.title : e.id,
      url: c ? c.url : null,
      since: e.since || null,
      sinceLabel: fmtDate(e.since),
      replacement: e.replacement || null,
      replacementUrl: e.replacement && bySlug.has(e.replacement) ? bySlug.get(e.replacement).url : null,
      blocksFrom: block ? fmtDate(block.toISOString()) : null,
      reason: e.reason || "",
    };
  });

  // ── fidelity report: warnings per component (the screen-level ones are not about a component) ──
  const fidPath = path.join(DS, "reports", "fidelity.json");
  const { report: fid, byComp: fidByComp } = loadFidelity(fidPath, new Set(bySlug.keys()));

  // ── per-component flags ──
  const FLAG = {
    stale: { key: "stale", label: "verificación caducada", tone: "bad" },
    unverified: { key: "unverified", label: "sin verificar", tone: "warn" },
    proposal: { key: "proposal", label: "propuesta pendiente", tone: "info" },
    approved: { key: "approved", label: "propuesta aprobada sin aplicar", tone: "bad" },
    ai: { key: "ai", label: "borrador de la IA por revisar", tone: "info" },
    todo: { key: "todo", label: "criterio por escribir", tone: "warn" },
    contrast: { key: "contrast", label: "contraste bajo AA", tone: "bad" },
    example: { key: "example", label: "sin ejemplo de código", tone: "warn" },
    retired: { key: "retired", label: "retirado", tone: "muted" },
    fidelity: { key: "fidelity", label: "aviso de fidelidad", tone: "warn" },
  };
  const counts = {};
  for (const k of Object.keys(FLAG)) counts[k] = 0;
  let contrastPairs = 0;
  const attention = [];
  const notes = [];
  for (const c of comps) {
    const flags = [];
    const sh = c.sheet || {};
    const manual = Array.isArray(sh.manual) ? sh.manual : [];
    const todoFields = manual.filter((m) => m && m.todo && !m.na && !m.proposed).map((m) => m.label);
    const aiFields = manual.filter((m) => m && m.proposedByAI).map((m) => m.label);
    const contrastFail = Number((sh.contrast && sh.contrast.fail) || 0);
    const myProps = propsByComp.get(c.slug) || [];
    if (!c.interno) {
      if (c.verStatus === "stale") flags.push({ ...FLAG.stale, detail: c.verReason || "" });
      else if (c.verStatus !== "verified") flags.push({ ...FLAG.unverified, detail: "" });
      if (myProps.some((p) => p.status === "approved")) flags.push({ ...FLAG.approved, detail: myProps.filter((p) => p.status === "approved").map((p) => p.id).join(", ") });
      if (myProps.some((p) => p.status === "draft")) flags.push({ ...FLAG.proposal, detail: myProps.filter((p) => p.status === "draft").map((p) => p.id).join(", ") });
      if (aiFields.length) flags.push({ ...FLAG.ai, detail: aiFields.join(" · ") });
      if (todoFields.length) flags.push({ ...FLAG.todo, label: `criterio por escribir (${todoFields.length})`, detail: todoFields.join(" · ") });
      if (contrastFail > 0) {
        flags.push({ ...FLAG.contrast, label: `contraste bajo AA (${contrastFail})`, detail: (sh.contrast && sh.contrast.label) || "" });
        contrastPairs += contrastFail;
      }
      if (!c.hasExample && !c.parte) flags.push({ ...FLAG.example, detail: "" });
      if (c.lifecycle === "deprecated") flags.push({ ...FLAG.retired, detail: "" });
      // los avisos piden algo; las notas informativas (severity info) no: van aparte y no cuentan como «pide atención»
      const fw = (fidByComp.get(c.slug) || { warnings: [] }).warnings;
      if (fw.length) flags.push({ ...FLAG.fidelity, label: `fidelidad (${fw.length})`, detail: fw.map((f) => f.title).join(" · "), items: fw });
      const fn = (fidByComp.get(c.slug) || { notes: [] }).notes;
      if (fn.length) notes.push({ slug: c.slug, title: c.title, url: c.url, group: c.group, items: fn });
    }
    for (const f of flags) counts[f.key] += 1;
    if (flags.length) attention.push({ slug: c.slug, title: c.title, url: c.url, group: c.group, level: c.level, kind: c.kind, flags, weight: flags.length });
  }
  const toneRank = { bad: 0, info: 1, warn: 2, muted: 3 };
  attention.sort((a, b) => {
    const ta = Math.min(...a.flags.map((f) => toneRank[f.tone])), tb = Math.min(...b.flags.map((f) => toneRank[f.tone]));
    return ta - tb || b.weight - a.weight || a.title.localeCompare(b.title);
  });

  // ── sync state ──
  const compsDump = readJson(path.join(DS, "sync", "components.json"), {}) || {};
  const varsDump = readJson(path.join(DS, "sync", "variables.json"), {}) || {};
  const history = ((compsDump.partialRefresh || {}).history || []).slice().reverse();
  const sinceFull = compsDump.readAt ? history.filter((h) => h.at && h.at > compsDump.readAt) : [];
  const visible = comps.filter((c) => !c.interno);
  const verified = visible.filter((c) => c.verStatus === "verified").length;
  const byFile = {};
  for (const c of visible) byFile[c.fileName || "sin archivo"] = (byFile[c.fileName || "sin archivo"] || 0) + 1;

  const lists = {
    unverified: attention.filter((a) => a.flags.some((f) => f.key === "unverified" || f.key === "stale")),
    todo: attention.filter((a) => a.flags.some((f) => f.key === "todo")),
    ai: attention.filter((a) => a.flags.some((f) => f.key === "ai")),
    contrast: attention.filter((a) => a.flags.some((f) => f.key === "contrast")),
    example: attention.filter((a) => a.flags.some((f) => f.key === "example")),
    fidelity: attention.filter((a) => a.flags.some((f) => f.key === "fidelity")),
  };
  const fidMtime = mtime(fidPath);

  return {
    generatedAt: fmtDate(new Date().toISOString(), true),
    ds: {
      name: manifest.designSystem || "",
      fromRepo: manifest.sourceMode === "repo",
      version: manifest.version || null,
      versionedAt: fmtDate(manifest.versionedAt),
      lastSync: fmtDate(manifest.lastSync, true),
      lastSyncAgo: agoLabel(manifest.lastSync),
      componentsReadAt: fmtDate(compsDump.readAt, true),
      componentsReadAgo: agoLabel(compsDump.readAt),
      variablesReadAt: fmtDate(varsDump.readAt, true),
      variablesReadAgo: agoLabel(varsDump.readAt),
      refreshesSinceFull: sinceFull.length,
      recentRefreshes: history.slice(0, 5).map((h) => ({ at: fmtDate(h.at, true), what: (h.scope || h.what || "").slice(0, 140) })),
      sources: (manifest.figmaSources || []).map((s) => ({ name: s.name, role: (s.role || "").split("(")[0].trim() })),
    },
    totals: {
      components: visible.length,
      atoms: visible.filter((c) => c.kind === "component").length,
      patterns: visible.filter((c) => c.kind === "pattern").length,
      internos: comps.length - visible.length,
      verified,
      verifiedPct: visible.length ? Math.round((verified / visible.length) * 100) : 0,
      byFile: Object.entries(byFile).sort((a, b) => b[1] - a[1]),
      attention: attention.length,
      clean: visible.length - attention.length,
    },
    counts: { ...counts, contrastPairs, proposals: pendingProposals.length, approved: approvedProposals.length, retirements: retirements.length },
    proposals: { pending: pendingProposals, approved: approvedProposals, textPending: pendingProposals.filter((p) => p.isText).length, otherPending: pendingProposals.filter((p) => !p.isText).length },
    retirements,
    policy: { blockNewUsageFromDay: policy.blockNewUsageFromDay ?? null, minNoticeDays: policy.minNoticeDays ?? null },
    attention,
    notes,
    lists,
    fidelity: fid
      ? { errors: fid.errors || 0, warnings: fid.warnings || 0, byCheck: Object.entries(fid.byCheck || {}).sort((a, b) => b[1] - a[1]).map(([code, n]) => ({ code, n, info: (fid.findings || []).some((f) => f.code === code) && (fid.findings || []).filter((f) => f.code === code).every((f) => f.severity === "info"), title: (CODES[code] || [code, ""])[0], why: (CODES[code] || [code, ""])[1] })), at: fmtDate(fidMtime, true), ago: agoLabel(fidMtime), olderThanSync: !!(fidMtime && manifest.lastSync && fidMtime < manifest.lastSync) }
      : null,
  };
}
