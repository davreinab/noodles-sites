// Viewer: search, variants, widths, tabs and copy. No dependencies.
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  // Visual mode: the selector under the search box sets data-theme on every component preview (same origin).
  // The choice is kept in localStorage; preview.njk reads it before painting, so a new tab or a reload keeps it.
  const modeSel = $("[data-mode]");
  if (modeSel) {
    const MODE = "pl-mode";
    let saved = "";
    try {
      saved = localStorage.getItem(MODE) || "";
    } catch (e) {
      /* storage unavailable */
    }
    if ([...modeSel.options].some((o) => o.value === saved)) modeSel.value = saved;
    const paint = (frame) => {
      try {
        const root = frame.contentDocument.documentElement;
        if (modeSel.value) root.setAttribute("data-theme", modeSel.value);
        else root.removeAttribute("data-theme");
      } catch (e) {
        /* no access to the document */
      }
    };
    const frames = () => $$("iframe[data-frame], iframe[data-fit]");
    frames().forEach((f) => f.addEventListener("load", () => paint(f)));
    frames().forEach((f) => {
      if (f.contentDocument?.readyState === "complete") paint(f);
    });
    modeSel.addEventListener("change", () => {
      try {
        localStorage.setItem(MODE, modeSel.value);
      } catch (e) {
        /* storage unavailable */
      }
      frames().forEach(paint);
    });
  }

  // Sidebar scroll: every page is a new document, so keep the scroll of the
  // menu across navigations and make sure the current page stays visible.
  const nav = $("[data-nav]");
  if (nav) {
    const KEY = "pl-nav-scroll";
    try {
      const saved = sessionStorage.getItem(KEY);
      if (saved !== null) nav.scrollTop = Number(saved);
    } catch (e) {
      /* storage unavailable */
    }
    $("[aria-current=page]", nav)?.scrollIntoView({ block: "nearest" });
    addEventListener("pagehide", () => {
      try {
        sessionStorage.setItem(KEY, String(nav.scrollTop));
      } catch (e) {
        /* storage unavailable */
      }
    });
  }

  // Sidebar search: filters the tree and opens groups that have matches.
  const search = $("[data-search]");
  if (search) {
    const groups = $$("[data-tree-group] > details");
    const wasOpen = new Map(groups.map((d) => [d, d.open]));
    let filtering = false;
    search.addEventListener("input", () => {
      const q = search.value.trim().toLowerCase();
      if (q && !filtering) groups.forEach((d) => wasOpen.set(d, d.open));
      filtering = !!q;
      let total = 0;
      $$("[data-tree-all]").forEach((li) => {
        li.hidden = !!q;
      });
      $$("[data-tree-item]").forEach((li) => {
        const hit = li.textContent.toLowerCase().includes(q);
        li.hidden = !hit;
        if (hit) total++;
      });
      // Inside out: a group is shown if it contains a visible pattern.
      [...$$("[data-tree-group]")].reverse().forEach((g) => {
        const visible = !!$("[data-tree-item]:not([hidden])", g);
        g.hidden = !visible;
        const d = $(":scope > details", g);
        d.open = q ? visible : wasOpen.get(d);
      });
      $$("[data-level-group]").forEach((g) => {
        g.hidden = !$("[data-tree-item]:not([hidden])", g);
      });
      $("[data-search-empty]").hidden = total > 0;
    });
  }

  // "View all" pages: every preview iframe grows to its content (same origin)
  $$("[data-fit]").forEach((f) => {
    const fitOne = () => {
      const doc = f.contentDocument;
      if (!doc || !doc.documentElement) return;
      // Se mide el contenido, no el marco: el alto del documento nunca baja del alto del iframe, así que sin este
      // reinicio un contenido que se acorta (otra variante, otro ancho) dejaba el marco tan alto como el anterior.
      f.style.height = "0px";
      f.style.height = Math.max(doc.documentElement.scrollHeight, 60) + "px";
    };
    f.addEventListener("load", () => {
      fitOne();
      try {
        new ResizeObserver(fitOne).observe(f.contentDocument.body);
      } catch (e) {
        /* no access to the document */
      }
    });
  });

  const frame = $("[data-frame]");
  if (!frame) return;
  const wrap = $("[data-frame-wrap]");
  const readout = $("[data-width]");
  const openLink = $("[data-open]");

  // Automatic iframe height (same origin)
  let inner;
  const fit = () => {
    const doc = frame.contentDocument;
    if (!doc || !doc.documentElement) return;
    // Se mide el contenido, no el marco (ver arriba): al volver de «Todas las variantes» a un ejemplo corto, el
    // documento ya no puede reclamar el alto del marco anterior.
    frame.style.height = "0px";
    frame.style.height = Math.max(doc.documentElement.scrollHeight, 120) + "px";
  };
  const attach = () => {
    inner?.disconnect();
    fit();
    try {
      inner = new ResizeObserver(fit);
      inner.observe(frame.contentDocument.body);
    } catch (e) {
      /* no access to the document */
    }
  };
  frame.addEventListener("load", attach);
  if (frame.contentDocument?.readyState === "complete") attach();

  // Readout of the real width
  new ResizeObserver(() => {
    readout.textContent = Math.round(frame.clientWidth) + " px";
  }).observe(frame);

  // Variants
  const setVariant = (key, href, push = true) => {
    $$("[data-variant-link]").forEach((a) => a.setAttribute("aria-current", String(a.dataset.variantLink === key)));
    $$("[data-variant-panel]").forEach((p) => {
      p.hidden = p.dataset.variantPanel !== key;
    });
    frame.style.height = "120px"; // altura mínima mientras carga la variante nueva; al cargar se ajusta al contenido
    frame.src = href;
    openLink.href = href;
    if (push) {
      const u = new URL(location.href);
      u.searchParams.set("v", key);
      history.replaceState(null, "", u);
    }
  };
  $$("[data-variant-link]").forEach((a) =>
    a.addEventListener("click", (e) => {
      if (e.metaKey || e.ctrlKey || e.shiftKey) return;
      e.preventDefault();
      setVariant(a.dataset.variantLink, a.href);
    }),
  );
  const initial = new URL(location.href).searchParams.get("v");
  if (initial) {
    const a = $(`[data-variant-link="${CSS.escape(initial)}"]`);
    if (a) setVariant(initial, a.href, false);
  }

  // Preset widths
  const widthButtons = $$("[data-set-width]");
  widthButtons.forEach((b) =>
    b.addEventListener("click", () => {
      const w = b.dataset.setWidth;
      wrap.style.width = w === "full" ? "" : Number(w) + 2 + "px"; // +2 for the border
      widthButtons.forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
    }),
  );
  // When dragged by hand, no preset width stays marked
  wrap.addEventListener("pointerdown", (e) => {
    const r = wrap.getBoundingClientRect();
    if (e.clientX > r.right - 20 && e.clientY > r.bottom - 20)
      widthButtons.forEach((x) => x.setAttribute("aria-pressed", "false"));
  });

  // Accessible tabs
  const tabs = $$("[role=tab]");
  const selectTab = (t) => {
    tabs.forEach((x) => {
      const on = x === t;
      x.setAttribute("aria-selected", String(on));
      x.tabIndex = on ? 0 : -1;
      document.getElementById(x.getAttribute("aria-controls")).hidden = !on;
    });
    t.focus();
  };
  tabs.forEach((t, i) => {
    t.addEventListener("click", () => selectTab(t));
    t.addEventListener("keydown", (e) => {
      if (e.key === "ArrowRight") selectTab(tabs[(i + 1) % tabs.length]);
      if (e.key === "ArrowLeft") selectTab(tabs[(i - 1 + tabs.length) % tabs.length]);
    });
  });

  // Copy the visible block of the panel
  $$("[data-copy]").forEach((b) =>
    b.addEventListener("click", async () => {
      const panel = document.getElementById(b.dataset.copy);
      const pre = $$("pre", panel).find((p) => !p.hidden);
      if (!pre) return;
      try {
        await navigator.clipboard.writeText(pre.textContent);
        b.textContent = "Copied";
      } catch (e) {
        const range = document.createRange();
        range.selectNodeContents(pre);
        getSelection().removeAllRanges();
        getSelection().addRange(range);
        b.textContent = "Selected";
      }
      setTimeout(() => {
        b.textContent = "Copy";
      }, 1600);
    }),
  );
})();
