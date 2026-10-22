// Edición de textos desde la ficha (descripción y criterio de diseño). Nunca cambia el texto: crea o edita
// LA propuesta pendiente del componente (una sola, con todos sus cambios de texto). Con `npm start` la
// guarda en design-system/proposals/; publicada como web estática, la descarga para guardarla allí.
import { textProposal } from "./proposal.js";

const dataEl = document.querySelector("[data-edit-data]");
if (dataEl) {
  const data = JSON.parse(dataEl.textContent);
  const KEY = "pl-approver";
  let local = false;
  const ping = fetch("/__ds/ping", { cache: "no-store" })
    .then((r) => r.ok && r.json())
    .then((j) => { local = !!(j && j.ok); })
    .catch(() => { local = false; });

  for (const block of document.querySelectorAll("[data-edit-block]")) {
    const field = block.dataset.editBlock;
    if (!Object.prototype.hasOwnProperty.call(data.current, field)) continue;
    const $ = (s) => block.querySelector(s);
    const openBtn = $("[data-edit-open]");
    const naBtn = $("[data-edit-na]");
    const textField = $("[data-edit-textfield]");
    const reasonLabel = $("[data-edit-reason-label]");
    let mode = "edit"; // «edit» o «na» (marcar el campo como «No aplica», también como propuesta)
    const view = $("[data-edit-view]");
    const form = $("[data-edit-form]");
    const status = $("[data-edit-status]");
    const hint = $("[data-edit-hint]");
    const submit = $("[data-edit-submit]");
    const shown = () => (field in (data.proposed || {}) ? data.proposed[field] : data.current[field]) || "";

    const close = () => {
      form.hidden = true;
      view.hidden = false;
      openBtn.hidden = false;
      if (naBtn) naBtn.hidden = false;
      (mode === "na" && naBtn ? naBtn : openBtn).focus();
    };

    const open = async (m) => {
      mode = m;
      await ping;
      submit.textContent = local ? "Guardar propuesta" : "Descargar propuesta";
      hint.textContent =
        (data.pending
          ? "Este componente ya tiene una propuesta de textos pendiente: el cambio se añade a esa, no se crea otra." +
            (data.pending.status === "approved" ? " Estaba aprobada: al editarla vuelve a pendiente de aprobación." : "")
          : "Se creará la propuesta de textos de este componente. El texto vigente no cambia hasta que se apruebe.") +
        (local ? "" : " Esta library no puede escribir en el proyecto: se descargará para guardarla en design-system/proposals/.");
      textField.hidden = mode === "na";
      reasonLabel.textContent = mode === "na" ? "Por qué no aplica" : "Por qué cambia";
      form.elements.reason.placeholder = mode === "na"
        ? "Por ejemplo: es decorativo, no se puede enfocar ni lleva texto"
        : "Qué problema resuelve o de dónde sale el cambio";
      form.elements.text.value = mode === "na" ? "No aplica." : shown();
      form.elements.reason.value = "";
      let saved = "";
      try { saved = localStorage.getItem(KEY) || ""; } catch { /* sin almacenamiento */ }
      form.elements.approver.value = (data.pending && data.pending.requiredApprover) || saved;
      status.textContent = "";
      view.hidden = true;
      form.hidden = false;
      openBtn.hidden = true;
      if (naBtn) naBtn.hidden = true;
      (mode === "na" ? form.elements.reason : form.elements.text).focus();
    };
    openBtn.hidden = false;
    openBtn.addEventListener("click", () => open("edit"));
    if (naBtn) {
      naBtn.hidden = false;
      naBtn.addEventListener("click", () => open("na"));
    }
    $("[data-edit-cancel]").addEventListener("click", close);
    form.addEventListener("keydown", (e) => { if (e.key === "Escape") close(); });

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const edit = { slug: data.slug, field, text: form.elements.text.value, reason: form.elements.reason.value, approver: form.elements.approver.value };
      if (edit.text.trim() === shown().trim()) {
        status.textContent = "No has cambiado el texto.";
        return;
      }
      try { localStorage.setItem(KEY, edit.approver.trim()); } catch { /* sin almacenamiento */ }
      submit.disabled = true;
      if (local) {
        status.textContent = "Guardando…";
        try {
          const r = await fetch("/__ds/proposal", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(edit) });
          const j = await r.json();
          if (!j.ok) throw new Error(j.error || "error");
          status.textContent = `${j.created ? "Propuesta creada" : "Propuesta actualizada"} en ${j.file}. Actualizando la ficha…`;
          setTimeout(() => location.reload(), 1800);
        } catch (err) {
          status.textContent = `No se ha podido guardar: ${err.message}`;
          submit.disabled = false;
        }
        return;
      }
      const p = textProposal(data.pending, data, edit, new Date().toISOString());
      data.pending = p; // varias ediciones seguidas sin servidor acumulan en la misma propuesta
      data.proposed = Object.fromEntries((p.proposedChange.changes || []).map((c) => [c.field, c.proposed]));
      const name = `${p.id}.proposal.json`;
      const url = URL.createObjectURL(new Blob([JSON.stringify(p, null, 2) + "\n"], { type: "application/json" }));
      const a = Object.assign(document.createElement("a"), { href: url, download: name });
      document.body.append(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
      status.textContent = `Descargada ${name}. Guárdala en design-system/proposals/ del proyecto, sustituyendo la anterior si ya estaba.`;
      submit.disabled = false;
    });
  }
}
