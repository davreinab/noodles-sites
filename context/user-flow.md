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
> **Wireframes Desktop completos:** sección `565:13925` de la página «🖥 Desktop» del archivo UX (leída el
> 2026-10-22): 26 pantallas y 4 modales, en escala de grises, sin enlaces de prototipo entre pantallas. Siete
> cabeceras de sección llevan la marca «Needs client feedback» (entre ellas Menu, Home, Natural formula y
> Products). Los textos y cifras del wireframe son de ejemplo salvo que una regla diga otra cosa. Las versiones
> **Wireframes móviles:** sección `567:13926` de la página «📱 Mobile» (leída el 2026-10-22): 22 pantallas a 375 px,
> la misma estructura que en desktop. Varias tienen el nombre cambiado en Figma (el menú y la Home se llaman
> «Products Library»; la Recipe page, «Product Page»): manda la cabecera de su grupo.
> **Desde el 2026-10-22 la estructura de los wireframes manda** sobre la del FigJam y la del traspaso cuando
> chocan (David Reina: «hay que adaptar lo que teníamos con la estructura analizada»). Los bloques «Estructura en
> el FigJam» se conservan como origen; donde difieren, vale el bloque «Estructura en el wireframe UX».

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
└── 💼 Legal information landing pages
    ├── Privacy policies
    ├── Legal notice
    ├── Cookie policies
    └── Lawful basis
```

En el tablero, Bags y Sauces no se despliegan en líneas; solo Cups llega a Original, Yakisoba y Rice, y las tres
desembocan en la misma Product page. El tablero incluye además «New product landing pages» y «Campaign
landing pages» con su plantilla: **no son de este proyecto** (David Reina, 2026-10-07) y no se recogen aquí.

**Transversales (todas las páginas):**
- ~~Navbar que se oculta al bajar y reaparece al subir~~ (traspaso; sustituido el 2026-10-22, ver abajo).
  - **Wireframe UX:** botón de menú, logo centrado y CTA «New 100% Natural Formula». Anotación en Figma
    (`396:5701`): «header flotante transparente, se queda sticky al scroll con fondo opaco».
    Decidido (David Reina, 2026-10-22: «hay que adaptar lo que teníamos con la estructura analizada»): manda el wireframe. Móvil: botón de menú y logo, sin el CTA.
  - **Menú** (`377:9923`): a pantalla completa, también en desktop. Claim, Products, Natural formula
    (etiqueta NEW), Recipes, Contests, FAQS, redes sociales y ©. En móvil, cada sección con flecha.
- Footer compartido (logo, contacto, navegación, sellos).
  - **Wireframe UX:** logo; enlaces Products, 100% Natural formula, Recipes, Contests, FAQS y dos
    «Campaign link»; «2025 Certified by» con sellos (EFSA, BREEAM: ver «Elementos sin definir»); caja de
    sugerencias («Do you have any ideas, complaints or cravings?» + «Send suggestions»); franja legal Legal
    notice, Privacy policy, Cookies policy, Legal basis, Contact y © GBFoods. En móvil, la caja de sugerencias va
    a todo el ancho encima del pie. Decidido (David Reina, 2026-10-22: «hay que adaptar lo que teníamos con la estructura analizada»): la franja legal añade **Contest rules** a lo que dibuja el wireframe,
    porque las bases son obligatorias ([`business-rules.md § Legal`](./business-rules.md)).
- Bottom footer legal (ver [`business-rules.md § Legal`](./business-rules.md)).
- ~~Suggestion bubble flotante~~ (sustituida el 2026-10-22, ver abajo).
  - Decidido (David Reina, 2026-10-22: «hay que adaptar lo que teníamos con la estructura analizada»): no hay burbuja; la vía de sugerencias es la caja del footer.

## Pantallas

### 1. Home
- Hero con slider (ver límite de slides en [`business-rules.md`](./business-rules.md)) y la
  naturalidad visible.
- Módulo de promo o concurso con vídeo y CTA; se oculta si no hay promoción.
- Fórmula natural.
- Productos (Cups, Bags y Sauces).
- Recetas, banner, FAQ, dónde comprar y suggestion box.

**Estructura en el wireframe UX** (`396:5700`): Hero (claim fijo «Welcome to the new era» y slider: NEW,
título, subtítulo, CTA y controles) · Concurso (arte de campaña, texto de premios, CTA y vídeo o imagen) ·
Fórmula natural (título e ingredientes eliminados, tachados, con su explicación) · Our products (Cups, Bags,
Sauces) · Recetas (4 cards y «See all recipes») · Banner de campaña (solo imagen) · FAQ («Still curious? See
all FAQS») · Where to buy (logos de distribuidores) · Footer. Anotaciones en Figma: el slider tiene hasta 3
slides y «pasa automáticamente» (`396:5702`; con pausa, ver [`business-rules.md § Componentes interactivos`](./business-rules.md));
el acordeón solo tiene una pregunta abierta (`396:5821`).

### 2. Natural formula page
Naturalidad ampliada, con FAQ propio.

**Estructura en el FigJam** (de arriba abajo; Navbar, Suggestion bubble, Footer y Bottom footer en todas):
- **Header:** claim de la nueva fórmula natural mejorada, imagen de los noodles con ingredientes y sello 100 % natural.
- **Natural ingredients:** imágenes de ingredientes, beneficio o proceso de cada ingrediente natural, ingredientes eliminados (tachados) y origen de los ingredientes.
- **Health care and properties:** beneficios de la nueva fórmula frente a la anterior, con cifras destacadas, y un claim de que comer rápido no tiene por qué ser comer mal.
- **Taste you can trust:** «Better for people, better for the planet». Infografía de propósito de marca en 4 bloques: 1) mejores noodles empiezan por mejor producción; 2) crecer con las comunidades locales; 3) innovación en cada receta; 4) receta más limpia, mismo sabor.
- **FAQS:** preguntas desplegables y CTA a todas las FAQS.
- **Crossnavigation:** «Try our new formula noodles», con las gamas (Cups + Bags).

**Estructura en el wireframe UX** (`274:6354`):
- **Header:** etiqueta «New improved formula», claim («100% natural. We cut the bullsh*t.»), texto y chips
  (Ready in 3', Real flavour, Full ingredient transparency), imagen.
- **«That's what we call an improvement»:** ingredientes sustituidos, cada uno con el de antes, el natural que lo
  reemplaza, el motivo y una imagen (aceite de palma → girasol, aromas artificiales → extractos vegetales,
  colorantes artificiales → cúrcuma y pimentón, potenciadores E621 → caldo de verduras); «We also removed»
  (conservantes, azúcar refinado, grasas hidrogenadas, OGM); «Ingredient origins», diagrama radial de
  ingrediente y país alrededor del sello «100% natural».
- **«Eating fast doesn't mean to eat unhealthy»:** cuatro cifras destacadas frente a la receta anterior.
- **«Taste you can trust»:** cuatro pilares numerados con imagen.
- **FAQ** propio y **banner** «Try our new formula noodles».
- Las cifras, los ingredientes y los orígenes son de ejemplo; todo claim debe coincidir con el envase
  ([`business-rules.md § Reglas generales`](./business-rules.md)).

### 3. Product library
Navegación en 3 niveles: tipo → línea → sabor.

**Estructura en el FigJam** (de arriba abajo; Navbar, Suggestion bubble, Footer y Bottom footer en todas):
- **Featured product:** imagen publicitaria del producto, claim o producto nuevo o fórmula mejorada.
- **Cups:** imagen, descripción y beneficios, gamas (Original, Yakisoba, Rice) y sabores.
- **Bags:** imagen, descripción y beneficios, gamas (Original, Yakisoba, Rice — con interrogante en el tablero) y sabores.
- **Sauces:** imagen, descripción y beneficios, y sabores.

**Estructura en el wireframe UX** (`396:5932`): hero con producto destacado (NEW) · barra de anclas Cups ·
Bags · Sauces · por formato, un bloque por línea (Yatekomo, Yakisoba) con packshot, descripción y rejilla
«Find your favourite flavour» con badges NEW, VEGAN y HOT! · Sauces como rejilla de productos. Los tres
niveles tipo → línea → sabor son **una sola página con anclas**, no un filtro. Decidido (David Reina, 2026-10-22: «hay que adaptar lo que teníamos con la estructura analizada»): manda el wireframe;
el patrón Product filter del DS y [`specs.md`](./specs.md) R-03 quedan ⬜ TODO — revisar. Móvil: anclas en
píldoras, sabores en rejilla de 2 columnas y salsas en carrusel horizontal.

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

**Estructura en el wireframe UX** (`396:6073`):
- **Hero:** volver a la línea («All Cups»), NEW, nombre, descripción, chips (100% natural ingredients, Ready in 3') y
  packshot sobre foto del producto.
- **Ingredients:** los componentes con su % del contenido y su composición; «View pack label» abre el modal de
  la etiqueta del envase (`490:7469`).
- **Nutritional information:** seis gráficos circulares (energía, proteína, hidratos, grasa, fibra, sal) con % y
  valor; «Main allergens» en tres tarjetas y «Check the detailed table», que abre el modal con los 14 alérgenos
  (`490:11998`, marca ● si está presente). Decidido (David Reina, 2026-10-22: «hay que adaptar lo que teníamos con la estructura analizada»): nutrición en gráficos circulares, como el wireframe
  (el Nutrition bar del DS queda ⬜ TODO — revisar). La etiqueta del envase sigue la estructura del wireframe
  pero con el formato europeo ([`business-rules.md § Catálogo de producto`](./business-rules.md)); el wireframe
  dibuja el de EE. UU. En móvil, los gráficos van en carrusel horizontal.
- **Preparation:** cuatro pasos, imagen o vídeo y temporizador de 3:00 (Empezar, Reiniciar). En móvil el
  temporizador va **entre el paso 2 y el 3**, justo en el paso de reposo de 3 minutos.
- **Recipes** con ese producto, **banner** y «Other products and flavours».

### 5. Recipe library
~~Sin buscador por ingredientes: con tan pocas recetas daría muchos resultados vacíos.~~ Sustituido el
2026-10-22 por el buscador del wireframe (ver abajo); los resultados vacíos tienen su estado.

**Estructura en el FigJam** (de arriba abajo; Navbar, Suggestion bubble, Footer y Bottom footer en todas):
- **Slim head:** título y claim de la sección, y herramientas de filtro, búsqueda u orden.
- **Grid:** reels o cards de receta con etiquetas, imagen, nombre, productos usados (noodles, salsa, rice, yakisoba…), número de ingredientes y tiempo de preparación (los dos últimos con interrogante).
- **Banner:** navegación cruzada («Know our products») o empuje a la suggestion box («Do you have your own custom recipes? Share them with us!», tono meme).

**Estructura en el wireframe UX** (`171:3808`; estados `483:5711` y `485:6064`): cabecera con buscador
(«Buscar receta o ingrediente») y chips de filtro · rejilla de 4 columnas (personas · minutos, nombre, chips
de producto) · paginación · banner · formulario «Do you have your own recipes with Yatekomo?» (texto libre y
«Enviar mi receta»). Decidido (David Reina, 2026-10-22: «hay que adaptar lo que teníamos con la estructura analizada»): buscador y filtros como el wireframe; deja sin efecto «sin buscador por
ingredientes». Móvil: chips en fila desplazable y rejilla de una columna.

### 6. Recipe page
- Imagen principal, ingredientes con los productos como chips, nutrición y pasos.
- Sin vídeo al principio.

**Estructura en el FigJam** (de arriba abajo; Navbar, Suggestion bubble, Footer y Bottom footer en todas):
- **Header:** imagen o vídeo, etiquetas, nombre de la receta y número de comensales.
- **Ingredients:** ingredientes con cantidades, productos de la marca que usa (con enlace) y utensilios necesarios.
- **Nutrition info:** beneficios nutricionales de la receta.
- **Steps:** tiempo de preparación y pasos (título y número; clip o imagen, o al menos texto).
- **Crossnavigation:** recetas relacionadas (cards); empuje a sugerencias («Have u try it already? … Tell us more!»); compartir la receta o guardarla para luego.

**Estructura en el wireframe UX** (`396:6290`): hero (volver «All Recipes», chips de los productos usados, nombre,
descripción, chips de tiempo y comensales, «Share recipe» que abre el modal de compartir `500:8062`, imagen) ·
Ingredients (cantidad e ingrediente, con el producto de la marca destacado) y «Recipe macros» por ración, con
«Ver tabla de alérgenos» (mismo modal de 14 alérgenos) · Step-by-step (pasos numerados, imagen opcional por
paso) · Other similar recipes · banner. Sin vídeo y sin utensilios. En móvil, «Share recipe» va junto a los chips
y las recetas similares en carrusel horizontal.

### 7. Contest library
Una página agregadora no es obligatoria.

**Estructura en el FigJam** (de arriba abajo; Navbar, Suggestion bubble, Footer y Bottom footer en todas):
- **Highlighted contest:** imagen y gráficos del concurso, nombre, premio, CTA de participar y fechas.
- **Other contests available** (todos los activos): lo mismo más el estado (abierto o cerrado).
- **Newsletter / social media** (con interrogante): claim para suscribirse y enterarse de productos y concursos nuevos; formulario o CTA externo.

**Estructura en el wireframe UX** (`190:3727`): título · Active contests (cards con imagen, «Available until», nombre y
chips de premios) · Closed contests (rejilla con «Cargar más») · «Don't miss a thing»: newsletter y redes.

### 8. Contest page
Tres modelos: estructura propia, iframe o enlace externo. Los concursos los organizan agencias
externas (p. ej. PS21).

**Estructura en el FigJam** (de arriba abajo; Navbar, Suggestion bubble, Footer y Bottom footer en todas):
- **Hero:** imagen y gráficos del concurso, nombre, CTA de participar (ancla al formulario) y cómo participar en una línea.
- **Prizes:** imagen y nombre o descripción del premio.
- **How to participate:** instrucciones o pasos, fecha límite, condiciones para ganar, formulario de participación y FAQS.
- **If it is an experience:** cómo lo vivieron otros (vídeos testimoniales o resumen, imágenes o posts de redes).
- **NL / social media:** claim para suscribirse o seguir, con enlaces o formulario.

**Estructura en el wireframe UX** (`330:6557`): hero (estado y fecha de cierre, nombre, texto, «Enter now», «Read the
rules», imagen) · Prizes (cuatro niveles de premio) · «Easy to participate, easy to win» (cuatro pasos y
«Winning conditions» con fechas de cierre y sorteo) · «Join it now»: formulario propio (datos personales,
prueba de compra con foto del ticket, consentimientos) · FAQ propio · «Real moments from past winners»
(vídeo y rejilla de la comunidad) · newsletter. Tres pantallas de resultado: ver **Estados**. El formulario,
los testimonios y la newsletter son temas sin definir (abajo).

### 9. FAQS
Página indexada.

**Estructura en el wireframe UX** (`428:10606`): título, buscador («Search for questions about our products») y lista
de preguntas en acordeón. Estados de búsqueda: ver **Estados**.

### 10. Legales
**Estructura en el wireframe UX** (`377:8301`): solo la política de privacidad, en una columna de lectura con «Back»,
apartados numerados, tabla de plazos de conservación y fecha de actualización. Las demás páginas legales: ⬜ TODO.

### 11. Contacto
Enlace externo.

### Elementos sin definir
~~Decisión de David Reina (2026-10-07): estos temas quedan sin definir.~~ **Levantados el 2026-10-22** (David
Reina, al adaptar el contexto a los wireframes): se definen como los dibuja el wireframe UX.
- **Sugerencias:** caja en el footer con «Send suggestions» (ver «Footer compartido»). Si abre un formulario propio
  o el externo de Calidad: ⬜ TODO — ver [`business-rules.md § Contacto`](./business-rules.md).
- **Recipe library:** buscador por receta o ingrediente, chips de filtro, número de resultados, «Clear filters» y
  paginación. Orden: no aparece en el wireframe (⬜ TODO).
- **Contest page:** formulario de participación propio, ganadores anteriores y contenido de la comunidad.
- **Catálogo:** badges NEW, VEGAN y HOT!. El moodboard del sabor y los packs no aparecen en el wireframe (⬜ TODO).
- **Recipe page:** comensales y compartir (redes y copiar enlace). Utensilios y guardar no aparecen (⬜ TODO).
- **Concursos:** newsletter y redes en la Contest library y la Contest page.
- **Footer:** sellos y certificados («2025 Certified by», EFSA y BREEAM en el wireframe). Cuáles: ⬜ TODO — GB Foods.
- **Recipe library:** formulario «Do you have your own recipes with Yatekomo?» para enviar recetas (nuevo en el
  wireframe; qué se hace con ellas: ⬜ TODO).

## Estados
- Home sin promoción activa: el módulo de promo o concurso se oculta.
- Modales (wireframe UX, 2026-10-22): etiqueta del envase (`490:7469`), tabla de 14 alérgenos (`490:11998`;
  `490:11911` es un duplicado) y compartir receta (redes y copiar enlace, `500:8062`).
- Recipe library (wireframe UX): con filtro aplicado, número de resultados y «Clear filters» (`483:5711`); sin
  resultados, mensaje y «our most popular ones» (`485:6064`).
- FAQS (wireframe UX): búsqueda con resultados (`428:10962`) y sin resultados, con preguntas sugeridas (`495:14043`).
- Contest page, resultado tras participar (wireframe UX; en Figma se llaman «Legal Page», nombre erróneo): no
  ganas, con un vale de descuento (`490:13618`); ganas, verificación por email (`490:13957`); superas el máximo
  de participaciones, con otro vale (`490:13867`). Los porcentajes de los vales son de ejemplo. Implica una
  mecánica de resultado inmediato y un límite de participaciones: ⬜ TODO — confirmar con GB Foods y la agencia.
- Estados de error y carga: ⬜ TODO (el wireframe no los dibuja).
