// Walks src/patterns/, renders every variant and computes the relations.
// Convention: src/patterns/<level>/[<group>/...]<name>/<name>.njk  (macro `render(data)`)
//             src/patterns/<level>/[<group>/...]<name>/<name>.json (title, description, variants)
// Intermediate folders without <folder>.njk are groups and build the sidebar tree.
import fs from "node:fs";
import path from "node:path";
import nunjucks from "nunjucks";
import beautify from "js-beautify";
import MarkdownIt from "markdown-it";
import { LEVELS, STATUSES } from "../../lib/library-config.js";

const ROOT = path.resolve("src/patterns");

// Markdown docs: no raw HTML; headings are demoted two levels so `#` becomes <h3>
// (the page already has <h1> for the pattern and <h2> for the "Documentation" section).
const demote = (state) => {
  for (const t of state.tokens) {
    if (t.type === "heading_open" || t.type === "heading_close") t.tag = "h" + Math.min(6, Number(t.tag[1]) + 2);
  }
};
const md = new MarkdownIt({ html: false, linkify: true });
md.core.ruler.push("demote-headings", demote);
// The sheet fields are short texts written one idea per line («**Rol:** …» / «**Nombre:** …»):
// a single line break is kept as a break, so four lines read as four lines and not as one paragraph.
const mdSheet = new MarkdownIt({ html: false, linkify: true, breaks: true });
mdSheet.core.ruler.push("demote-headings", demote);

// Design-system sheet (written by scripts/ds-library.py): the hand-written fields of the ficha are
// Markdown; render them here so the template only lays them out.
const renderSheet = (sheet) => {
  if (!isObject(sheet)) return null;
  return {
    ...sheet,
    manual: (sheet.manual || []).map((f) => ({
      ...f,
      html: f.todo ? "" : mdSheet.render(f.md || ""),
      proposedHtml: f.proposed !== undefined ? mdSheet.render(f.proposed || "") : "",
    })),
    notesHtml: sheet.notes ? mdSheet.render(sheet.notes) : "",
  };
};

// Detects {% from "..." import %}, {% import "..." %} and {% include "..." %}
const DEPENDENCY_RE = /{%-?\s*(?:from|import|include)\s+["']([^"']+)["']/g;

// `order` (number, default 0) and `hidden` (boolean) in pattern JSON and in _group.json.
// Lower order first; ties fall back to alphabetical (folders) or authoring order (variants).
const orderOf = (value, where) => {
  if (value === undefined) return 0;
  if (typeof value === "number" && Number.isFinite(value)) return value;
  console.warn(`[patterns] Ignoring non-numeric order ${JSON.stringify(value)} in ${where}`);
  return 0;
};

const isObject = (v) => v !== null && typeof v === "object" && !Array.isArray(v);

const slug = (s) =>
  String(s)
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");

const camel = (s) => s.replace(/-([a-z0-9])/g, (_, c) => c.toUpperCase());

const formatHtml = (html) =>
  beautify
    .html(html, {
      indent_size: 2,
      wrap_line_length: 0,
      preserve_newlines: false,
      end_with_newline: false,
      inline: [],
      unformatted: ["svg"],
    })
    .trim();

export default function () {
  const env = new nunjucks.Environment(new nunjucks.FileSystemLoader(ROOT, { noCache: true }), {
    autoescape: true,
    trimBlocks: true,
    lstripBlocks: true,
  });

  // An id a template builds other ids or ARIA references from has no fixed fallback, so two copies on one
  // page cannot collide. A missing one throws, and the error shows in the preview (DEC-008, DEC-024).
  env.addGlobal("required", (value, what) => {
    if (value === undefined || value === null || value === "") throw new Error(`${what} is required`);
    return value;
  });

  const list = [];
  const byPatternId = new Map();

  // A pattern is a folder that contains <folder>.njk. Any other folder is a group
  // and can nest to any depth (atoms/buttons/button/button.njk).
  const isDir = (p) => fs.statSync(p).isDirectory();

  const buildPattern = (level, segments, hiddenByAncestor = false) => {
    const name = segments[segments.length - 1];
    const rel = segments.join("/");
    const dir = path.join(ROOT, level.key, ...segments);
    const tplFile = path.join(dir, `${name}.njk`);
    const jsonFile = path.join(dir, `${name}.json`);
    let meta = {};
    let metaError = null;
    if (fs.existsSync(jsonFile)) {
      try {
        meta = JSON.parse(fs.readFileSync(jsonFile, "utf8"));
      } catch (e) {
        metaError = `Invalid JSON in ${level.key}/${rel}/${name}.json: ${e.message}`;
      }
      // Valid JSON of the wrong shape (null, an array, a string...) is an error too, not a crash.
      if (!metaError && !isObject(meta)) {
        meta = {};
        metaError = `${level.key}/${rel}/${name}.json must contain a JSON object`;
      } else if (!metaError && meta.variants !== undefined && !isObject(meta.variants)) {
        metaError = `"variants" in ${level.key}/${rel}/${name}.json must be an object`;
      }
    }

    const docFile = path.join(dir, `${name}.md`);
    let docHtml = "";
    if (fs.existsSync(docFile)) {
      const docSource = fs.readFileSync(docFile, "utf8");
      if (/^\uFEFF?\s*---\s*\r?\n/.test(docSource)) {
        console.warn(
          `[patterns] ${level.key}/${rel}/${name}.md starts with front matter, which is not supported (DEC-014): move title/description/status to ${name}.json`,
        );
      }
      docHtml = md.render(docSource);
    }
    const ownStatus = meta.status ? STATUSES.find((st) => st.key === slug(meta.status)) : null;
    if (meta.status && !ownStatus) {
      console.warn(
        `[patterns] Unknown status "${meta.status}" in ${level.key}/${rel} (known: ${STATUSES.map((st) => st.label).join(", ")})`,
      );
    }

    const templatePath = `${level.key}/${rel}/${name}.njk`;
    const source = fs.readFileSync(tplFile, "utf8");
    const deps = [...new Set([...source.matchAll(DEPENDENCY_RE)].map((m) => m[1]))];
    const url = `/patterns/${level.key}/${rel}/`;
    const alias = camel(name);

    const rawVariants = isObject(meta.variants) && Object.keys(meta.variants).length ? meta.variants : { default: {} };

    const item = {
      id: `${level.key}/${rel}`,
      name,
      path: segments,
      level: level.key,
      levelLabel: level.label,
      title: meta.title || name,
      description: meta.description || "",
      order: orderOf(meta.order, `${level.key}/${rel}`),
      hidden: meta.hidden === true || hiddenByAncestor,
      ownStatus: meta.status || "",
      ownStatusKey: ownStatus ? ownStatus.key : "",
      status: meta.status || "",
      statusKey: slug(meta.status || ""),
      inheritedFrom: null,
      docHtml,
      sheet: renderSheet(meta.sheet),
      templatePath,
      source: source.trim(),
      usage: `{% from "${templatePath}" import render as ${alias} %}\n{{ ${alias}({ ... }) }}`,
      deps,
      url,
      variants: [], // filled in a second pass, once every pattern is loaded (data $refs may point anywhere)
      dataRefs: [],
      _ctx: { rel, metaError, rawVariants, defaults: meta.defaults, title: meta.title || name },
    };
    list.push(item);
    byPatternId.set(item.id, item);
    return { type: "pattern", key: name, order: item.order, item };
  };

  // Returns the child nodes of a folder (groups and patterns). Empty groups are skipped.
  const scan = (level, segments, hiddenByAncestor = false) => {
    const dir = path.join(ROOT, level.key, ...segments);
    const nodes = [];
    for (const entry of fs.readdirSync(dir).sort()) {
      if (entry.startsWith(".") || entry.startsWith("_")) continue;
      const child = path.join(dir, entry);
      if (!isDir(child)) continue;
      const childSegments = [...segments, entry];
      if (fs.existsSync(path.join(child, `${entry}.njk`))) {
        nodes.push(buildPattern(level, childSegments, hiddenByAncestor));
        continue;
      }
      // Optional _group.json: { "title": "Buttons", "order": 1, "hidden": false }
      let group = {};
      const groupFile = path.join(child, "_group.json");
      if (fs.existsSync(groupFile)) {
        try {
          group = JSON.parse(fs.readFileSync(groupFile, "utf8"));
          if (!isObject(group)) {
            console.warn(
              `[patterns] ${level.key}/${childSegments.join("/")}/_group.json must contain a JSON object; ignoring it`,
            );
            group = {};
          }
        } catch (e) {
          console.warn(`[patterns] Invalid JSON in ${level.key}/${childSegments.join("/")}/_group.json: ${e.message}`);
        }
      }
      const hidden = group.hidden === true || hiddenByAncestor;
      const children = scan(level, childSegments, hidden);
      if (!children.length) continue;
      nodes.push({
        type: "group",
        key: entry,
        id: `${level.key}/${childSegments.join("/")}`,
        url: `/patterns/${level.key}/${childSegments.join("/")}/`,
        title: group.title || entry.charAt(0).toUpperCase() + entry.slice(1).replace(/-/g, " "),
        order: orderOf(group.order, `${level.key}/${childSegments.join("/")}/_group.json`),
        hidden,
        children,
        count: children.reduce((n, c) => n + (c.type === "group" ? c.count : 1), 0),
      });
    }
    return nodes.sort((x, y) => x.order - y.order || x.key.localeCompare(y.key));
  };

  // What the menu, home page and "View all" pages show: hidden patterns and groups are left out
  // (their own pages are still built and they can still be included by other patterns).
  const visibleTree = (nodes) =>
    nodes.flatMap((n) => {
      if (n.type === "pattern") return n.item.hidden ? [] : [n];
      if (n.hidden) return [];
      const children = visibleTree(n.children);
      if (!children.length) return [];
      return [{ ...n, children, count: children.reduce((c, x) => c + (x.type === "group" ? x.count : 1), 0) }];
    });

  const flatGroups = (nodes, depth = 0) =>
    nodes.flatMap((n) =>
      n.type === "group"
        ? [{ title: n.title, url: n.url, count: n.count, depth }, ...flatGroups(n.children, depth + 1)]
        : [],
    );

  // ---- Variant data: `defaults`, `$ref` and rendering -------------------------------------------
  // A variant's data = deepMerge(resolve(pattern.defaults), resolve(variant)). Any object may carry
  // `"$ref": "<target>"` (plus sibling keys that override the referenced data):
  //   "_shared/plans.json#/basic"      a JSON file under src/patterns/, with an optional JSON pointer
  //   "organisms/coverage-card#basic"  a variant of another pattern (no fragment = its first variant)
  //   "molecules/stepper#step-2/steps" one property of that variant's data (JSON pointer after the variant)
  // Objects merge deeply; arrays and scalars are replaced (DEC-017).
  const isPlain = (v) => v !== null && typeof v === "object" && !Array.isArray(v);
  const deepMerge = (base, over) => {
    if (!isPlain(base) || !isPlain(over)) return over;
    const out = { ...base };
    for (const k of Object.keys(over)) out[k] = k in base ? deepMerge(base[k], over[k]) : over[k];
    return out;
  };

  const sharedCache = new Map();
  const readShared = (target) => {
    const file = path.resolve(ROOT, target);
    if (!file.startsWith(ROOT + path.sep)) throw new Error(`$ref "${target}" points outside src/patterns/`);
    if (!sharedCache.has(file)) {
      if (!fs.existsSync(file)) throw new Error(`$ref file not found: ${target}`);
      try {
        sharedCache.set(file, JSON.parse(fs.readFileSync(file, "utf8")));
      } catch (e) {
        throw new Error(`Invalid JSON in ${target}: ${e.message}`, { cause: e });
      }
    }
    return sharedCache.get(file);
  };

  const pointer = (doc, fragment, ref) => {
    if (!fragment) return doc;
    if (!fragment.startsWith("/"))
      throw new Error(`$ref "${ref}": the fragment of a JSON file must be a JSON pointer like #/name`);
    let node = doc;
    for (const raw of fragment.slice(1).split("/")) {
      const key = raw.replace(/~1/g, "/").replace(/~0/g, "~");
      if (node === null || typeof node !== "object" || !(key in node))
        throw new Error(`$ref "${ref}": "${fragment}" not found`);
      node = node[key];
    }
    return node;
  };

  const orderedEntries = (p) =>
    Object.entries(p._ctx.rawVariants)
      .map(([key, value], i) => {
        const valid = isObject(value);
        const raw = valid ? value : {};
        return { key, raw, valid, i, order: orderOf(raw._order, `${p.id} variant "${key}"`) };
      })
      .sort((a, b) => a.order - b.order || a.i - b.i);

  const withStack = (key, stack, fn) => {
    if (stack.includes(key)) throw new Error(`Circular $ref: ${[...stack, key].join(" -> ")}`);
    return fn([...stack, key]);
  };

  const variantData = (p, entry, stack, refs) => {
    const { _title, _order, ...rest } = entry.raw;
    const { defaults } = p._ctx;
    if (defaults !== undefined && !isPlain(defaults)) throw new Error(`"defaults" in ${p.id} must be an object`);
    return deepMerge(resolveValue(defaults ?? {}, stack, refs), resolveValue(rest, stack, refs));
  };

  const loadRef = (ref, stack, refs) => {
    const hash = ref.indexOf("#");
    const target = hash === -1 ? ref : ref.slice(0, hash);
    const fragment = hash === -1 ? "" : ref.slice(hash + 1);
    const direct = stack.length === 1; // only direct references are listed under Relations
    if (target.endsWith(".json")) {
      if (direct) refs.add(`file:${target}`);
      return withStack(`${target}#${fragment}`, stack, (next) =>
        resolveValue(pointer(readShared(target), fragment, ref), next, refs),
      );
    }
    const other = byPatternId.get(target);
    if (!other) throw new Error(`$ref "${ref}": no pattern "${target}"`);
    if (other._ctx.metaError) throw new Error(other._ctx.metaError);
    const slash = fragment.indexOf("/");
    const variantKey = slash === -1 ? fragment : fragment.slice(0, slash);
    const subPointer = slash === -1 ? "" : fragment.slice(slash);
    const entries = orderedEntries(other);
    const entry = variantKey
      ? entries.find((e) => e.key === variantKey || slug(e.key) === slug(variantKey))
      : entries[0];
    if (!entry)
      throw new Error(
        `$ref "${ref}": ${target} has no variant "${variantKey}" (has: ${entries.map((e) => e.key).join(", ")})`,
      );
    if (direct) refs.add(`pattern:${other.id}`);
    return withStack(`${other.id}#${entry.key}`, stack, (next) =>
      pointer(variantData(other, entry, next, refs), subPointer, ref),
    );
  };

  const resolveValue = (value, stack, refs) => {
    if (Array.isArray(value)) return value.map((v) => resolveValue(v, stack, refs));
    if (!isPlain(value)) return value;
    const { $ref, ...rest } = value;
    const own = Object.fromEntries(Object.entries(rest).map(([k, v]) => [k, resolveValue(v, stack, refs)]));
    if ($ref === undefined) return own;
    if (typeof $ref !== "string") throw new Error(`$ref must be a string, got ${JSON.stringify($ref)}`);
    const target = loadRef($ref, stack, refs);
    if (!Object.keys(own).length) return target; // plain reference: arrays and scalars pass through
    if (!isPlain(target)) throw new Error(`$ref "${$ref}" is not an object, so it cannot take extra keys`);
    return deepMerge(target, own);
  };

  const makeVariants = (p) => {
    const { rel, metaError, title } = p._ctx;
    const refs = new Set();
    const seen = new Set();
    const variants = orderedEntries(p).map((entry) => {
      // Two variant keys can slug to the same value; a duplicate would be a fatal output conflict.
      let key = slug(entry.key) || "default";
      if (seen.has(key)) {
        let n = 2;
        while (seen.has(`${key}-${n}`)) n++;
        console.warn(
          `[patterns] ${p.id}: variant "${entry.key}" has the same slug as an earlier variant; using "${key}-${n}" for its URL`,
        );
        key = `${key}-${n}`;
      }
      seen.add(key);
      let data = {};
      let html;
      let error = metaError || (entry.valid ? null : `Variant "${entry.key}" of ${p.id} must be a JSON object`);
      if (!error) {
        try {
          data = variantData(p, entry, [`${p.id}#${entry.key}`], refs);
          html = env.renderString(`{% from "${p.templatePath}" import render %}{{ render(data) }}`, { data });
        } catch (e) {
          error = e.message;
        }
      }
      if (error) {
        html = `<pre style="color:#a00;white-space:pre-wrap;font:13px/1.5 monospace">Render error: ${nunjucks.lib.escape(error)}</pre>`;
      }
      return {
        key,
        title: entry.raw._title || entry.key,
        data,
        dataJson: JSON.stringify(data, null, 2),
        html: formatHtml(html),
        error,
        previewUrl: `/preview/${p.level}/${rel}/${key}/`,
        level: p.level,
        patternTitle: title,
      };
    });
    const dataRefs = [...refs].map((r) => {
      if (r.startsWith("file:")) return { type: "file", path: r.slice(5) };
      const target = byPatternId.get(r.slice(8));
      return {
        type: "pattern",
        id: target.id,
        title: target.title,
        url: target.url,
        level: target.level,
        levelLabel: target.levelLabel,
      };
    });
    return { variants, dataRefs };
  };

  const trees = new Map();
  for (const level of LEVELS) {
    if (!fs.existsSync(path.join(ROOT, level.key))) continue;
    trees.set(level.key, scan(level, []));
  }

  for (const p of list) Object.assign(p, makeVariants(p));
  for (const p of list) delete p._ctx; // only after all: $refs read other patterns' context

  // Relations: what each pattern uses and where it is used.
  const byTemplate = new Map(list.map((p) => [p.templatePath, p]));
  const ref = (p) => ({ id: p.id, title: p.title, url: p.url, level: p.level, levelLabel: p.levelLabel });
  for (const p of list) {
    p.uses = p.deps
      .map((d) => byTemplate.get(d))
      .filter(Boolean)
      .map(ref);
    p.missing = p.deps.filter((d) => !byTemplate.has(d));
    p.usedBy = [];
  }
  for (const p of list) {
    for (const u of p.uses) byTemplate.get(list.find((x) => x.id === u.id).templatePath).usedBy.push(ref(p));
  }

  // Status cascade: lowest known status among the pattern and everything it uses (transitively).
  const rank = (key) => STATUSES.findIndex((st) => st.key === key);
  const byId = new Map(list.map((p) => [p.id, p]));
  const effective = new Map();
  const resolve = (p, trail = new Set()) => {
    if (effective.has(p.id)) return effective.get(p.id);
    if (trail.has(p.id)) return { key: p.ownStatusKey, from: null }; // dependency cycle
    trail.add(p.id);
    let best = { key: p.ownStatusKey, from: null };
    for (const u of p.uses) {
      const dep = resolve(byId.get(u.id), trail);
      if (dep.key && (!best.key || rank(dep.key) < rank(best.key))) {
        best = { key: dep.key, from: dep.from || byId.get(u.id) };
      }
    }
    trail.delete(p.id);
    effective.set(p.id, best);
    return best;
  };
  for (const p of list) {
    const { key, from } = resolve(p);
    // Only patterns with a status of their own display one; the cascade still passes through the others.
    if (p.ownStatusKey && key !== p.ownStatusKey) {
      p.status = STATUSES.find((st) => st.key === key).label;
      p.statusKey = key;
      p.inheritedFrom = { title: from.title, url: from.url, status: from.ownStatus };
    }
  }

  // `items` follows the tree (order, then alphabetical), so the home page honours `order` too.
  const treeItems = (nodes) => nodes.flatMap((n) => (n.type === "pattern" ? [n.item] : treeItems(n.children)));
  const levels = LEVELS.map((l) => {
    const tree = visibleTree(trees.get(l.key) || []);
    return { ...l, items: treeItems(tree), tree };
  }).filter((l) => l.items.length);
  for (const l of levels) l.groups = flatGroups(l.tree);

  // "View all" pages: one per level and one per group, listing every pattern below it.
  const viewAll = [];
  const collect = (nodes) => nodes.flatMap((n) => (n.type === "pattern" ? [n.item] : collect(n.children)));
  const walkGroups = (level, nodes, crumbs) => {
    for (const n of nodes) {
      if (n.type !== "group") continue;
      viewAll.push({
        url: n.url,
        title: n.title,
        level: level.key,
        levelLabel: level.label,
        crumbs,
        nodes: n.children,
        count: n.count,
      });
      walkGroups(level, n.children, [...crumbs, { title: n.title, url: n.url }]);
    }
  };
  for (const l of levels) {
    l.url = `/patterns/${l.key}/`;
    viewAll.push({
      url: l.url,
      title: l.label,
      level: l.key,
      levelLabel: l.label,
      crumbs: [],
      nodes: l.tree,
      count: collect(l.tree).length,
      description: l.description,
    });
    walkGroups(l, l.tree, []);
  }

  return {
    levels,
    viewAll,
    statuses: STATUSES,
    list,
    variants: list.flatMap((p) => p.variants),
    count: list.filter((p) => !p.hidden).length,
  };
}
