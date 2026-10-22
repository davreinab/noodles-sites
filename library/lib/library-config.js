// Forked from the company's Pattern Library (Eleventy 3 + Nunjucks). Owned by the init-proyecto skill since 12.1.0.
// Library-wide configuration shared by the viewer data (src/_data/patterns.js) and the asset build
// (lib/assets.js). It lives outside src/_data/ on purpose: every file in there becomes Eleventy data.

// Levels, in cascade order: the asset build bundles styles level by level in this order.
export const LEVELS = [
  { key: "atoms", label: "Atoms", description: "Smallest pieces: buttons, fields, labels." },
  { key: "molecules", label: "Molecules", description: "Small groups of atoms with a single purpose." },
  { key: "organisms", label: "Organisms", description: "Complete, self-contained sections of the interface." },
  { key: "modules", label: "Modules", description: "Funnel steps or blocks that combine organisms." },
  { key: "templates", label: "Templates", description: "Page structure without real content." },
  { key: "pages", label: "Pages", description: "Full screens with realistic content." },
];

// Statuses, ordered from least to most finished. A pattern shows the lowest status among
// itself and everything it includes; the cascade passes through patterns without a status.
export const STATUSES = [
  { key: "deprecated", label: "Deprecated", bg: "#d36d27", fg: "#000000" },
  { key: "draft", label: "Draft", bg: "#ececec", fg: "#000000" },
  { key: "in-review", label: "In review", bg: "#fcd12e", fg: "#000000" },
  { key: "ready", label: "Ready", bg: "#2d5e2e", fg: "#ffffff" },
];
