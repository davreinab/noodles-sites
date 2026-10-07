<!-- ⚙️ ARCHIVO GENERADO por scripts/ds-release.py — NO EDITAR A MANO.
     Cada entrada la escribe una publicación; el criterio se añade en la propuesta,
     no aquí. Ver design.md § Publicar una versión. -->

# GB Noodles · Microsites · Design System — Registro de cambios

Versiona el **sistema de diseño**, no la herramienta que lo genera. Semántico:

- **Mayor:** desaparece o se renombra algo que alguien podía estar usando (token, componente,
  variante, estado, propiedad). Rompe a quien lo consuma.
- **Menor:** se añade algo. Nadie se rompe.
- **Parche:** cambian valores o descripciones, sin tocar la estructura.

Cada salto mayor lleva su ruta de actualización: qué usar en lugar de lo retirado.

> ⬜ Sin publicaciones todavía. La primera la crea `python3 scripts/ds-release.py --apply`.
