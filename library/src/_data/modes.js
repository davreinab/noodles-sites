// Visual modes of the design system (light, dark, brand…), read from design-system/tokens/tokens.css at build time:
// the default mode is `:root { … }` and every other one is a `:root[data-theme="<key>"] { … }` block.
// The viewer shows its selector only when there are two or more.
import fs from "node:fs";
import path from "node:path";

const label = (k) => k.charAt(0).toUpperCase() + k.slice(1).replace(/[-_]+/g, " ");

export default function () {
  let css = "";
  try {
    css = fs.readFileSync(path.resolve("../design-system/tokens/tokens.css"), "utf8");
  } catch {
    /* sin tokens todavía */
  }
  const keys = [...new Set([...css.matchAll(/:root\[data-theme=["']?([\w-]+)["']?\]\s*\{/g)].map((m) => m[1]))];
  const light = keys.some((k) => /^(dark|oscuro)$/i.test(k)) ? "Light" : "Default";
  const list = keys.length ? [{ key: "", label: light }, ...keys.map((k) => ({ key: k, label: label(k) }))] : [];
  return { list, multiple: list.length >= 2 };
}
