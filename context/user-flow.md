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

### Árbol de navegación (FigJam)
> Fuente: FigJam «GB Noodles · IA & page structure» (`cRgmGl36ELIUZNLUvC8KbW`), extraído el 2026-10-07. Las etiquetas van tal cual en el tablero (inglés); los emojis son los sellos del tablero.

```
Noodle Site
├── 🏠 Home page
├── 🍜 Product Library
│   ├── Product type: Cups
│   │   ├── Product line: Original Noodles ── Flavours ─┐
│   │   ├── Product line: Yakisoba Noodles ── Flavours ─┼── Product page
│   │   └── Product line: Rice ────────────── Flavours ─┘
│   ├── Product type: Bags
│   └── Product type: Sauces
├── 💚 Nature fórmula page
├── 🍳 Recipe Library ── Recipe page
├── Contest Library ── 🏆 Contest page ── Contest rules
├── GBfoods Contact page (external link)
├── FAQS
├── 💼 Legal information landing pages
│   ├── Privacy policies
│   ├── Legal notice
│   ├── Cookie policies
│   └── Lawful basis
├── ⭐ New product landing pages
└── 🔥 Campaign landing pages
```

En el tablero, Bags y Sauces no se despliegan en líneas; solo Cups llega a Original, Yakisoba y Rice, y las tres
desembocan en la misma Product page. Las landings de producto nuevo y de campaña comparten la plantilla
«Landing Pages» (ver § 12).

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
Naturalidad ampliada, con FAQ propio.

**Estructura en el FigJam** (de arriba abajo; Navbar, Suggestion bubble, Footer y Bottom footer en todas):
- **Header:** claim de la nueva fórmula natural mejorada, imagen de los noodles con ingredientes y sello 100 % natural.
- **Natural ingredients:** imágenes de ingredientes, beneficio o proceso de cada ingrediente natural, ingredientes eliminados (tachados) y origen de los ingredientes.
- **Health care and properties:** beneficios de la nueva fórmula frente a la anterior, con cifras destacadas, y un claim de que comer rápido no tiene por qué ser comer mal.
- **Taste you can trust:** «Better for people, better for the planet». Infografía de propósito de marca en 4 bloques: 1) mejores noodles empiezan por mejor producción; 2) crecer con las comunidades locales; 3) innovación en cada receta; 4) receta más limpia, mismo sabor.
- **FAQS:** preguntas desplegables y CTA a todas las FAQS.
- **Crossnavigation:** «Try our new formula noodles», con las gamas (Cups + Bags).

### 3. Product library
Navegación en 3 niveles: tipo → línea → sabor.

**Estructura en el FigJam** (de arriba abajo; Navbar, Suggestion bubble, Footer y Bottom footer en todas):
- **Featured product:** imagen publicitaria del producto, claim o producto nuevo o fórmula mejorada.
- **Cups:** imagen, descripción y beneficios, gamas (Original, Yakisoba, Rice) y sabores.
- **Bags:** imagen, descripción y beneficios, gamas (Original, Yakisoba, Rice — con interrogante en el tablero) y sabores.
- **Sauces:** imagen, descripción y beneficios, y sabores.

### 4. Product page
- Etiquetas, nombre y highlights.
- Imágenes: 3D e interior.
- Ingredientes jerarquizados y modal con la etiqueta del envase.
- Nutrición visual y alérgenos.
- Preparación con GIF o vídeo y un temporizador de 3 minutos.

**Estructura en el FigJam** (de arriba abajo; Navbar, Suggestion bubble, Footer y Bottom footer en todas):
- **Head:** imagen clara del producto, badges (new!, hot!, new formula!, vegan!), nombre del sabor y gama, y moodboard del sabor (imágenes de contexto, paleta de color del sabor, recursos visuales).
- **Banner:** promoción o campaña activa de ese producto, si la hay, para no alterar la cabecera.
- **Product detail info:** ingredientes, ingredientes que ya no lleva la fórmula, beneficios principales (proteína, pocas grasas…) y alérgenos, con acceso a un detalle o tabla en modal.
- **Consumer guide:** guía visual paso a paso, apoyada con vídeo corto o GIF vertical (con interrogante) y temporizador (con interrogante).
- **Recipes:** cards o reels de recetas; otros productos que combinan bien, quizá salsas (con interrogantes).
- **Crossnavigation:** otros sabores, gamas o packs sugeridos según el producto, y sabores o productos nuevos destacados.

### 5. Recipe library
Sin buscador por ingredientes: con tan pocas recetas daría muchos resultados vacíos.

**Estructura en el FigJam** (de arriba abajo; Navbar, Suggestion bubble, Footer y Bottom footer en todas):
- **Slim head:** título y claim de la sección, y herramientas de filtro, búsqueda u orden.
- **Grid:** reels o cards de receta con etiquetas, imagen, nombre, productos usados (noodles, salsa, rice, yakisoba…), número de ingredientes y tiempo de preparación (los dos últimos con interrogante).
- **Banner:** navegación cruzada («Know our products») o empuje a la suggestion box («Do you have your own custom recipes? Share them with us!», tono meme).

### 6. Recipe page
- Imagen principal, ingredientes con los productos como chips, nutrición y pasos.
- Sin vídeo al principio.

**Estructura en el FigJam** (de arriba abajo; Navbar, Suggestion bubble, Footer y Bottom footer en todas):
- **Header:** imagen o vídeo, etiquetas, nombre de la receta y número de comensales.
- **Ingredients:** ingredientes con cantidades, productos de la marca que usa (con enlace) y utensilios necesarios.
- **Nutrition info:** beneficios nutricionales de la receta.
- **Steps:** tiempo de preparación y pasos (título y número; clip o imagen, o al menos texto).
- **Crossnavigation:** recetas relacionadas (cards); empuje a sugerencias («Have u try it already? … Tell us more!»); compartir la receta o guardarla para luego.

### 7. Contest library
Una página agregadora no es obligatoria.

**Estructura en el FigJam** (de arriba abajo; Navbar, Suggestion bubble, Footer y Bottom footer en todas):
- **Highlighted contest:** imagen y gráficos del concurso, nombre, premio, CTA de participar y fechas.
- **Other contests available** (todos los activos): lo mismo más el estado (abierto o cerrado).
- **Newsletter / social media** (con interrogante): claim para suscribirse y enterarse de productos y concursos nuevos; formulario o CTA externo.

### 8. Contest page
Tres modelos: estructura propia, iframe o enlace externo. Los concursos los organizan agencias
externas (p. ej. PS21).

**Estructura en el FigJam** (de arriba abajo; Navbar, Suggestion bubble, Footer y Bottom footer en todas):
- **Hero:** imagen y gráficos del concurso, nombre, CTA de participar (ancla al formulario) y cómo participar en una línea.
- **Prizes:** imagen y nombre o descripción del premio.
- **How to participate:** instrucciones o pasos, fecha límite, condiciones para ganar, formulario de participación y FAQS.
- **If it is an experience:** cómo lo vivieron otros (vídeos testimoniales o resumen, imágenes o posts de redes).
- **NL / social media:** claim para suscribirse o seguir, con enlaces o formulario.

### 9. FAQS
Página indexada. Detalle: ⬜ TODO.

### 10. Legales
Detalle: ⬜ TODO.

### 11. Contacto
Enlace externo.

### 12. Landing pages (producto nuevo y campaña)
Plantilla «Landing Pages» del FigJam, compartida por las landings de producto nuevo y de campaña.

**Estructura en el FigJam** (de arriba abajo; Navbar, Suggestion bubble, Footer y Bottom footer en todas):
- **Hero section:** render o imagen clara del producto, nombre (Yatekomo), claim «The Only 100% Natural», CTA «Discover how» (lleva a Natural formula details) y sello verde natural.
- **Brand moodboard** (extensión del hero, se puede saltar con el CTA principal): imágenes y claims de marca; ejemplos del tablero: «We call out the bullshit», «We make food we'd feed our families proudly».
- **Natural formula details:** ventajas de la nueva fórmula: 1) 100 % ingredientes naturales («de 30 % a 100 %», con tachado) y lista de ingredientes con imagen; 2) mejor perfil nutricional: −20 % sal y −80 % grasas saturadas; 3) «Big on flavour, short on ingredients»: sin aditivos, conservantes, aceite de palma ni glutamato. Cierre: «Better formula, same flavour: Don't believe it? Go try it by yourself and tell us» (lleva a la suggestion box).
- **Products and flavours:** «Find the flavour that fits you the most». Original («Stick to the basics…») y Yakisoba («Twist it with a more authentic Asian flavour…»), una al lado de otra con un render de cada una y sin navegación; sabores disponibles (no packs: nombre, color o ingrediente) y ventaja de la Cup: lista en 3 minutos.
- **Brand purpose:** el mismo bloque «Taste you can trust» de la Natural formula page (4 bloques).
- **Suggestion box:** «Any feedback, suggestion or idea for us? Share it here!», con formulario (email y texto libre).
- **Footer:** logo, contacto y sellos de salud y certificados alimentarios.

Las secciones de referencia del tablero (hero, moodboard, propósito de marca, productos y sabores,
fórmula natural) y el bloque «To keep in mind» contienen solo imágenes de referencia, sin texto.

### Pendiente de decidir (FigJam frente al resto del contexto)
Lo que el FigJam propone y choca o va más allá de lo ya acordado. No se resuelve aquí: se lleva a
`synthesis.md` como decisión cuando el cliente o el equipo lo confirmen.
- **Suggestion box:** en la landing es un formulario propio (email y texto); en [`business-rules.md § Contacto`](./business-rules.md) es un enlace al formulario externo de Calidad.
- **Recipe library:** el tablero pide filtro, búsqueda y orden; la regla vigente descarta el buscador por ingredientes (los filtros por etiqueta o producto no están decididos).
- **Contest page:** el tablero dibuja formulario de participación propio y testimonios; el traspaso admite tres modelos (estructura propia, iframe, enlace externo).
- **Product page:** badges «hot!» y «vegan!» y moodboard del sabor, que no existen todavía en el design system; también la navegación cruzada y los packs.
- **Recipe page:** comensales, utensilios y compartir o guardar la receta, sin componente en el design system.
- **Contest library y Contest page:** bloque de newsletter o redes, sin regla ni componente.
- **Footer:** el tablero pide sellos de salud y certificados alimentarios; los aporta GB Foods (pendiente).

## Estados
- Home sin promoción activa: el módulo de promo o concurso se oculta.
- Modales de etiqueta, alérgenos, resultados de concurso y de búsqueda: están sin cargar en los
  flows de Figma (estado del diseño a 2026-10-07). Detalle: ⬜ TODO.
- Estados de vacío, error y carga: ⬜ TODO.
