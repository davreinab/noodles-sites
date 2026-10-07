<!-- vigencia
  autoridad: GB Foods (cliente) — pendiente de validar la UX de Sites
  confirmado: ⬜ TODO — fecha ISO de la última vez que alguien dijo «esto sigue siendo verdad»
  estado: pendiente-de-confirmar
  Las reglas de PROPIEDAD no caducan (un identificador no cambia de naturaleza). Las de
  DECISIÓN sí: caducan a los 6 meses de «confirmado» y la auditoría avisa, no bloquea.
-->

# User flow — GB Noodles · Microsites

> Fuente: `noodles/context/traspaso-microsites.md` §7 (2026-10-07) y los prototipos UX de Aitor
> Espasa en Figma (`1YhsCqdqYCHlK4Y82IY5G3`; blueprints en el FigJam `cRgmGl36ELIUZNLUvC8KbW`).
> Las pantallas de UI se diseñan en «Noodles - sites» (`NfjwW15h6leh1MbJp0lYQO`, vacío a 2026-10-07).
> **El cliente no ha dado feedback** sobre los wireframes. Previsión interna de cierre: noviembre.

## Modelo conceptual
Una web por marca y mercado, todas con la misma estructura. La Home lleva a la acción
principal (la campaña activa). Sin campaña activa, lleva primero a producto y después a recetas.
Las campañas (concursos), los productos y las recetas se organizan como **librería → página**.

Sitemap:
- Home
- Natural formula page (naturalidad ampliada, con FAQ propio)
- Campaign pages: Contest library → Contest page; Recipe library → Recipe page
- Product library → Product page
- FAQS (página indexada)
- Legales
- Contacto (enlace externo, ver [`business-rules.md § Contacto`](./business-rules.md))

**Transversales (todas las páginas):**
- Navbar que se oculta al bajar y reaparece al subir.
- Footer compartido (logo, contacto, navegación, sellos).
- Bottom footer legal (ver [`business-rules.md § Legal`](./business-rules.md)).
- Suggestion bubble flotante.

## Pantallas

### 1. Home
- Hero con slider (ver límite de slides en [`business-rules.md`](./business-rules.md)) y la
  naturalidad visible.
- Módulo de promo o concurso con vídeo y CTA; se oculta si no hay promoción.
- Fórmula natural.
- Productos (Cups, Bags y Sauces).
- Recetas, banner, FAQ, dónde comprar y suggestion box.

### 2. Natural formula page
Naturalidad ampliada, con FAQ propio. Detalle: ⬜ TODO.

### 3. Product library
Navegación en 3 niveles: tipo → línea → sabor.

### 4. Product page
- Etiquetas, nombre y highlights.
- Imágenes: 3D e interior.
- Ingredientes jerarquizados y modal con la etiqueta del envase.
- Nutrición visual y alérgenos.
- Preparación con GIF o vídeo y un temporizador de 3 minutos.

### 5. Recipe library
Detalle: ⬜ TODO. Sin buscador por ingredientes: con tan pocas recetas daría muchos resultados vacíos.

### 6. Recipe page
- Imagen principal, ingredientes con los productos como chips, nutrición y pasos.
- Sin vídeo al principio.

### 7. Contest library
Una página agregadora no es obligatoria. Detalle: ⬜ TODO.

### 8. Contest page
Tres modelos: estructura propia, iframe o enlace externo. Los concursos los organizan agencias
externas (p. ej. PS21).

### 9. FAQS
Página indexada. Detalle: ⬜ TODO.

### 10. Legales
Detalle: ⬜ TODO.

### 11. Contacto
Enlace externo.

## Estados
- Home sin promoción activa: el módulo de promo o concurso se oculta.
- Modales de etiqueta, alérgenos, resultados de concurso y de búsqueda: están sin cargar en los
  flows de Figma (estado del diseño a 2026-10-07). Detalle: ⬜ TODO.
- Estados de vacío, error y carga: ⬜ TODO.
