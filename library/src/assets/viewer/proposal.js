// Propuesta de cambio de textos de un componente, editada desde el visor.
// Módulo compartido: lo usan el servidor local (lib/proposals-server.js) y el navegador (proposal-ui.js),
// así la propuesta sale igual se guarde en el proyecto o se descargue.
//
// Regla del design system: cambiar la descripción o el criterio de uso de un componente no es trivial
// (proposals/README.md). Por eso el visor nunca escribe el texto: escribe una propuesta.
// Una sola propuesta pendiente por componente: si ya hay una, se edita esa.

// «description» vive en Figma; el resto de campos son los del criterio de diseño de la ficha y se
// identifican por su etiqueta («Propósito», «Cuándo usar / qué NO hace»…).
export const fieldInfo = (field) =>
  field === "description"
    ? { label: "descripción", where: "figma" }
    : { label: `«${field}»`, where: "ficha" };

export const KIND = "component-text";

export const isPending = (p) => p && (p.status === "draft" || p.status === "approved");

export const belongsTo = (p, slug) =>
  p && p.proposedChange && p.proposedChange.kind === KIND && p.proposedChange.component === slug;

/**
 * @param {object|null} existing  propuesta pendiente de ese componente, o null
 * @param {object} ds             { slug, name, fileKey, nodeId, current: { description } }
 * @param {object} edit           { field, text, reason, approver, origin? }  origin: "person" (defecto) o "ai"
 * @param {string} now            fecha ISO
 */
export function textProposal(existing, ds, edit, now) {
  const today = now.slice(0, 10);
  const field = String(edit.field || "description");
  // Un borrador de la IA queda marcado hasta que una persona lo edita (entonces pasa a «person»).
  const origin = edit.origin === "ai" ? "ai" : "person";
  const p = existing
    ? JSON.parse(JSON.stringify(existing))
    : {
        id: `${today}-${ds.slug}-textos`,
        status: "draft",
        summary: "",
        evidence: [],
        affectedResources: [],
        proposedChange: {
          kind: KIND,
          component: ds.slug,
          name: ds.name,
          figma: { fileKey: ds.fileKey || null, nodeId: ds.nodeId || null },
          changes: [],
          history: [],
        },
        impact: {},
        migration: null,
        requiredApprover: "",
        decision: null,
      };
  const pc = p.proposedChange;
  pc.changes = pc.changes || [];
  pc.history = pc.history || [];

  // Editar una propuesta ya aprobada y aún sin aplicar la reabre: lo aprobado era otro texto.
  if (p.status === "approved") {
    p.status = "draft";
    pc.history.push({ at: now, action: "reopened", note: "editada después de aprobarse: vuelve a pendiente", previousDecision: p.decision || null });
    p.decision = null;
  }

  const text = String(edit.text || "").replace(/\r\n/g, "\n").trim();
  const current = String((ds.current || {})[field] || "").trim();
  const i = pc.changes.findIndex((c) => c.field === field);
  if (text === current) {
    if (i >= 0) pc.changes.splice(i, 1);
  } else if (i >= 0) {
    pc.changes[i].proposed = text;
    pc.changes[i].origin = origin;
  } else {
    pc.changes.push({ field, where: fieldInfo(field).where, current, proposed: text, origin });
  }
  pc.history.push({ at: now, action: origin === "ai" ? "drafted" : existing ? "edited" : "created", field, origin });

  const reason = String(edit.reason || "").trim();
  if (reason) p.evidence.push({ type: origin === "ai" ? "ai-draft" : "library-edit", at: now, field, note: reason });

  if (edit.approver && String(edit.approver).trim()) p.requiredApprover = String(edit.approver).trim();

  const fields = pc.changes.map((c) => fieldInfo(c.field).label);
  p.summary = fields.length
    ? `Cambiar ${fields.join(" y ")} de ${ds.name || ds.slug}. Texto propuesto desde la library; pendiente de aprobación.`
    : `Sin cambios: el texto propuesto para ${ds.name || ds.slug} coincide con el actual.`;
  p.affectedResources = [
    ...(pc.changes.some((c) => c.where === "figma") && ds.nodeId ? [`Figma ${ds.nodeId} (description)`] : []),
    `design-system/schemas/components/${ds.slug}.schema.json`,
    `design-system/docs/components/${ds.slug}.md`,
  ];
  p.impact = {
    summary: `Cambia cómo se describe ${ds.name || ds.slug} y, con ello, cuándo lo usan diseño, desarrollo y la IA. No cambia estructura, variantes ni estilos.`,
    components: [ds.slug],
  };
  return p;
}
