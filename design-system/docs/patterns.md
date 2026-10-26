# GB Noodles · Microsites · Patrones (componentes compuestos)

> Catálogo de **patrones (componentes compuestos)**, construidos a partir de los átomos de `components.md`. Cada patrón tiene su **ficha** en `patterns/<slug>.md` (este archivo es el índice más las secciones manuales), y cada ficha es un **contrato** con dos partes:
> - **Parte viva** (anatomía, medidas, variantes, tokens que consume) → se **sincroniza
>   desde Figma** (modelo B, ver `design.md`) en el bloque `GENERATED` de la ficha. No editar a mano.
> - **Parte de criterio** (cuándo usar, qué NO hace, accesibilidad) → se escribe a mano
>   una vez debajo del bloque, porque no es expresable como variable de Figma.
>
> Reglas duras: no se inventa un patrón que no esté aquí; los patrones se componen de átomos y consumen
> **tokens semánticos** de `tokens.css`, nunca primitivos ni hex.

**Estado:** 39 patrones sincronizados el 2026-10-23T09:38:30Z · una ficha por archivo en `patterns/<slug>.md` (este archivo solo guarda el índice y las secciones manuales).

---

## Índice

- [Navbar](patterns/navbar.md) · pattern · `navbar` · ✅ criterio completo
- [Mobile menu](patterns/mobile-menu.md) · pattern · `mobile-menu` · ✅ criterio completo
- [Footer](patterns/footer.md) · pattern · `footer` · ✅ criterio completo
- [FAQ list](patterns/faq-list.md) · pattern · `faq-list` · ⬜ 4 pendientes
- [Legal table](patterns/legal-table.md) · pattern · `legal-table` · ⬜ 4 pendientes
- [Legal page](patterns/legal-page.md) · pattern · `legal-page` · ⬜ 5 pendientes
- [Hero](patterns/hero.md) · pattern · `hero` · ✅ criterio completo
- [Marquee](patterns/marquee.md) · pattern · `marquee` · ✅ criterio completo
- [Promo](patterns/promo.md) · pattern · `promo` · ✅ criterio completo
- [Natural formula](patterns/natural-formula.md) · pattern · `natural-formula` · ✅ criterio completo
- [Product categories](patterns/product-categories.md) · pattern · `product-categories` · ✅ criterio completo
- [Recipes](patterns/recipes.md) · pattern · `recipes` · ✅ criterio completo
- [Banner](patterns/banner.md) · pattern · `banner` · ✅ criterio completo
- [FAQ](patterns/faq.md) · pattern · `faq` · ✅ criterio completo
- [Where to buy](patterns/where-to-buy.md) · pattern · `where-to-buy` · ✅ criterio completo
- [Library](patterns/library.md) · pattern · `library` · ✅ criterio completo
- [Product filter](patterns/product-filter.md) · pattern · `product-filter` · ✅ criterio completo
- [Library hero](patterns/library-hero.md) · pattern · `library-hero` · ✅ criterio completo
- [Product line](patterns/product-line.md) · pattern · `product-line` · ✅ criterio completo
- [Library head](patterns/library-head.md) · pattern · `library-head` · ✅ criterio completo
- [Recipe submit](patterns/recipe-submit.md) · pattern · `recipe-submit` · ✅ criterio completo
- [Contest library](patterns/contest-library.md) · pattern · `contest-library` · ⬜ 2 pendientes
- [Newsletter](patterns/newsletter.md) · pattern · `newsletter` · ⬜ 4 pendientes
- [Product hero](patterns/product-hero.md) · pattern · `product-hero` · ✅ criterio completo
- [Product details](patterns/product-details.md) · pattern · `product-details` · ✅ criterio completo
- [Preparation](patterns/preparation.md) · pattern · `preparation` · ✅ criterio completo
- [Recipe hero](patterns/recipe-hero.md) · pattern · `recipe-hero` · ✅ criterio completo
- [Recipe ingredients](patterns/recipe-ingredients.md) · pattern · `recipe-ingredients` · ✅ criterio completo
- [Recipe steps](patterns/recipe-steps.md) · pattern · `recipe-steps` · ✅ criterio completo
- [Natural hero](patterns/natural-hero.md) · pattern · `natural-hero` · ⬜ 2 pendientes
- [Natural improvement](patterns/natural-improvement.md) · pattern · `natural-improvement` · ⬜ 2 pendientes
- [Natural stats](patterns/natural-stats.md) · pattern · `natural-stats` · ⬜ 2 pendientes
- [Natural pillars](patterns/natural-pillars.md) · pattern · `natural-pillars` · ⬜ 2 pendientes
- [Contest hero](patterns/contest-hero.md) · pattern · `contest-hero` · ⬜ 3 pendientes
- [Contest prizes](patterns/contest-prizes.md) · pattern · `contest-prizes` · ⬜ 2 pendientes
- [Contest how-to](patterns/contest-how-to.md) · pattern · `contest-how-to` · ⬜ 3 pendientes
- [Contest form](patterns/contest-form.md) · pattern · `contest-form` · ⬜ 4 pendientes
- [Contest community](patterns/contest-community.md) · pattern · `contest-community` · ⬜ 2 pendientes
- [Contest result](patterns/contest-result.md) · pattern · `contest-result` · ⬜ 5 pendientes

## Cómo rellenar una ficha

Cada ficha nace con el bloque generado y cuatro campos de criterio en `⬜ TODO` (su forma exacta:
`patterns/_plantilla.md`). Se escriben una vez, a mano, y el sync los conserva:

- **Propósito:** para qué sirve y qué problema resuelve.
- **Ejemplo de código:** snippet HTML mínimo con las clases reales de `components.css`, en su variante
  por defecto; una línea por variante o estado relevante si cambia el markup. Es la referencia que
  copian pantallas y agentes, y el sync lo copia al schema (`code.example`). Su elemento raíz
  lleva `data-ds="<slug>"`: la marca que une pantalla, contrato y maestro de Figma. Los iconos con
  su ruta real (`../assets/icons/<nombre>.svg`) y las fotos siempre con
  `../assets/images/placeholder.svg`, nunca fotos de `UI/`: el catálogo da error si un icono no
  existe y muestra el placeholder si una foto no es del DS.
- **Accesibilidad (rol, nombre, estados y teclado):** lo que el color no cubre. El contraste AA no se
  escribe aquí: es obligatorio siempre, lo mide `ds-fidelity` desde el CSS (`contrast-below-aa`) y la
  library lo enseña en la ficha. Si el patrón es decorativo o solo informativo, «No aplica.» y el
  motivo. La IA puede proponer un borrador (`guides/accesibilidad.md`). Aquí va el *rol* (button, textbox, checkbox, dialog… o «decorativo»); *de dónde sale su nombre* (texto visible,
  etiqueta asociada o atributo explícito: un icono sin texto siempre necesita nombre explícito); *qué se
  anuncia al cambiar de estado* (seleccionado, expandido, inválido, ocupado… un estado que solo se ve
  por color no existe para quien no ve); *teclado* (qué teclas lo operan; si no se puede usar sin
  ratón, no está terminado); *foco* (dónde entra, dónde sale, si queda atrapado a propósito) y *qué se
  oculta al lector* (partes decorativas o redundantes).
- **Cuándo usar / qué NO hace:** el límite del patrón; lo que parece suyo y es de otro.

## Nota de cambios · fase 5 (2026-10-23)

- **Nuevos** (fichas a mano, sin volcado de Figma todavía; el bloque GENERATED queda vacío hasta el sync): contest-library, newsletter, contest-hero, contest-prizes, contest-how-to, contest-form, contest-community, contest-result. CSS en `css/components.css`, en los bloques de fase 5 al final del archivo.
- **Actualizados:** library-head (booleanos Search y Filters: `library-head--no-search` y `library-head--no-filters`; por defecto se ven, así que Recipes no cambia).
- **Decisión abierta (⬜):** el maestro de la Contest library dibuja la cabecera y los concursos en crema; el patrón lo hace blanco para no encadenar dos secciones crema (norma de composición). Lo decide David Reina.
- **Pendiente:** textos, mecánica de resultado inmediato, límite de participaciones, condiciones legales, premios, fechas del concurso y texto de consentimiento: ⬜ TODO, a confirmar con GB Foods y la agencia. Ninguno de estos datos está inventado en las fichas.

## Nota de cambios · fase 6 (2026-10-23)

- **Nuevos** (fichas a mano, sin volcado de Figma; el bloque GENERATED queda vacío hasta el sync): faq-list (Default, Results, Empty) y legal-page. CSS en `css/components.css`, en el bloque «FASE 6 · FAQ Y LEGALES».
- **Actualizados:** library-head (nueva propiedad Align: Left por defecto o Center, `library-head--center`; el buscador se centra y el título queda a la izquierda). El bloque GENERATED aún no la lista: se añade en el próximo sync.
- **Decisión:** la columna de lectura de la FAQ es `--layout-reading` (720 px) y no los 808 px del wireframe, porque no hay token de 808 y la columna de lectura del DS es 720.
- **Pendiente:** todas las respuestas de la FAQ y los textos legales de GB Foods (⬜ TODO). Las fichas no inventan texto.

## Catálogo propuesto (⬜ por definir en Figma)

## Composición de pantalla — reglas   ✍️ manual · 2026-10-07

> Cómo se **colocan** los componentes en una página. Es el tercer nivel del DS (tokens →
> componentes → composición) y el que evita que cada pantalla decida su propio espaciado.
> Toda medida citada aquí es un token de `tokens.css`; si falta, se propone y, aprobada la propuesta, se crea en Figma primero.
> Las pantallas de `UI/` y el agente consultan esta sección antes de montar cualquier vista.
> Las secciones de referencia son los patrones `Pattern / *` de Figma (fase 6).

### Ritmo vertical
| Entre… | Token | Notas |
|---|---|---|
| secciones de página | `--layout-section-y` (96 / 80 / 64 px) | Es el padding superior e inferior de cada sección; las secciones se apilan sin hueco y se separan por el cambio de fondo (page → card → brand → inverse → natural). Dos secciones seguidas no repiten fondo. |
| bloques dentro de una sección | `--space-48` desktop · `--space-32` mobile | Cabecera → contenido → enlace final. |
| título de sección y su contenido | `--space-32` desktop · `--space-24` mobile | Título y entradilla entre sí: `--space-16`. |
| cards de una rejilla o carrusel | `--layout-gutter` en horizontal · `--space-48` entre filas | Product, Recipe y Contest card. |
| ítems de una lista (FAQ, pasos) | `--space-16` (Accordion item) · `--space-32` (Step) | |
| campos de un formulario | `--space-24` | Etiqueta, campo y error van dentro del componente Field. |

### Contenedores y anchos
| Contenedor | Token `--layout-*` | Dónde se usa |
|---|---|---|
| página (max-width) | `--layout-frame` con `--layout-margin` a cada lado; contenido hasta `--layout-content-max` | Todas las secciones. Las franjas a sangre (Marquee, Product filter) ignoran el margen. |
| columna de lectura / prosa | `--layout-reading` (720 px, máximo) | Legales, respuestas del FAQ y textos largos de Natural formula y FAQS. En móvil manda el ancho de la columna. |
| panel lateral / drawer | no se usa en microsites | El menú móvil es a pantalla completa (Mobile menu). |
| modal | anchos del componente Modal: M 560 · L 880 · Full (móvil) | M: alérgenos y resultado de concurso; L: etiqueta del envase y búsqueda. |

### Grid y breakpoints
| Breakpoint | Ancho | Columnas | Gutter (token) | Margen (token) | Qué cambia |
|---|---|---|---|---|---|
| mobile | 375 (hasta 768) | 4 | `--layout-gutter` 16 | `--layout-margin` 24 | Todo apilado; carruseles con scroll horizontal y la siguiente card asomando; rejillas a 1 columna; Navbar con menú. |
| tablet | 768 (hasta 1024) | 8 | `--layout-gutter` 24 | `--layout-margin` 40 | Rejillas a 2 columnas; hero y bloques de dos columnas pasan a apilados. |
| desktop | 1440 | 12 | `--layout-gutter` 24 | `--layout-margin` 64 | Rejillas a 3-4 columnas; bloques en dos columnas (texto + media). |

_Los breakpoints se declaran también en `scripts/token-audit.config.json` (`breakpoints`);
CSS no admite `var()` en `@media`, por eso son la única medida que vive como convención._

### Paneles, overlays y capas
| Elemento | Desktop | Mobile | Capa (`--z-*`) | Motion (`--motion-*`) |
|---|---|---|---|---|
| drawer / panel lateral | no se usa | Mobile menu a pantalla completa | `--layer-modal` | entra con `--motion-duration-slow` + `--motion-easing-standard` |
| modal | centrado, M o L, sobre `--color-surface-overlay` | Full | velo `--layer-overlay` · diálogo `--layer-modal` | `--motion-duration-slow` + `--motion-easing-standard` |
| toast | abajo a la derecha | abajo centrado, ancho de columna | `--layer-toast` | `--motion-duration-base`; se cierra solo a los 6 s salvo Error |
| navbar | fija arriba, transparente; opaca al hacer scroll (R-01.6) | igual | `--layer-sticky` | `--motion-duration-base` |
| suggestion bubble | abajo a la derecha | igual, se pliega a icono | `--layer-floating` | `--motion-duration-fast` |

_Las capas se llaman `--layer-*` en este proyecto (no `--z-*`). Todo movimiento respeta
`prefers-reduced-motion`._

### Flujo de contenido
- Orden de lectura y jerarquía de títulos por tipo de página:
  - **Home** (wireframe UX `1YhsCqdqYCHlK4Y82IY5G3`, nodos 396:5700 desktop y 97:636 mobile): Navbar · Hero · Promo (solo con campaña activa) · Natural formula · Product categories · Recipes · Banner (solo con campaña) · FAQ · Where to buy · Footer (con la caja de sugerencias). Sin campaña, el CTA del Hero lleva a producto y después a recetas. Marquee y Suggestion bubble no están en el wireframe de la Home. Fondos: crema · amarillo con trama · verde · crema · blanco · crema · blanco · amarillo con trama · tinta (nunca dos cremas seguidos; ver Decisiones recurrentes).
  - **Product page:** Product hero · Product details · Preparation · Recipes (que usan el producto) · Where to buy.
  - **Recipe page:** Recipe hero · Product details (valores de la receta) · Preparation sin Timer y con Step Media=True · Recipes relacionadas.
  - **Libraries (producto, receta, concurso):** Library con la card y el filtro que toquen.
  - **Natural formula page y FAQS:** cabecera + texto en columna de lectura + FAQ (en FAQS, un bloque por categoría).
  - Un solo `h1` por página (claim del hero, nombre del producto o de la receta, título de la librería); cada sección abre con `h2`; las cards usan `h3`.
- Dónde van las acciones primarias (cabecera, pie de panel, fin de formulario): la acción principal de la página está en el hero (Button L en desktop, M en móvil); en cada sección, una sola acción al final o junto al título (Link «Ver todos»); en el Modal, en el pie alineada a la derecha (a todo el ancho en Full); en formularios, al final y a la izquierda. En la Navbar, el CTA es «New 100% Natural Formula» (wireframe UX); «Dónde comprar» queda en el Product hero y como sección Where to buy.
- Estados vacíos, carga y error a nivel de página: los filtros solo muestran opciones con resultados, así que la librería no queda vacía (regla de negocio); si una sección no tiene contenido (sin promoción, sin recetas del producto) se oculta entera, sin mensaje. La carga de «Ver más» y del vídeo muestra el estado en el propio botón. Los errores de carga se avisan con Alert inline Error y una acción de reintentar en el lugar del contenido; nunca página en blanco.

## Capa de pantalla — composiciones y utilidades   ✍️ manual

_(composiciones por página y utilidades `u-*` de `components.css`; se documenta aquí
cada clase de layout que consuman las pantallas — regla 1b de design.md. Cada composición
lleva su **Ejemplo de código** con el markup de la página, igual que los componentes.)_

## Decisiones recurrentes   ✍️ manual

> Regla 13 de `design.md`: lo que el usuario corrige **dos veces** se escribe aquí en esa
> misma sesión y pasa a ser normativo. Una fila por decisión. Si la decisión implica una
> medida o un color, se crea el token en Figma y se sincroniza; si afecta a un componente,
> se promueve a su contrato y aquí queda el enlace. Antes de proponer un cambio visual,
> consulta esta tabla: lo que ya está decidido no se vuelve a preguntar.

| Fecha | Regla (una frase, en imperativo) | Origen (dónde se corrigió, dos veces como mínimo) | Aplica a | Estado |
|---|---|---|---|---|
| _YYYY-MM-DD_ | _Ej.: «Las acciones primarias de un panel van siempre en el pie, alineadas a la derecha.»_ | _UI/<pantalla>.html (sesión 2026-…) · UI/<otra-pantalla>.html (revisión PR #12)_ | _paneles y drawers_ | _vigente · promovida a token `--…` · promovida al contrato «…»_ |
| 2026-10-07 | Ningún nombre técnico lleva diéresis, tildes ni otros diacríticos: modos, variables, estilos, componentes, capas, slugs y selectores van en ASCII («Aiki», no «Aïki»). La grafía de marca se conserva solo en textos visibles y descripciones. | David Reina: slug `logo-aïki` → `logo-aiki` (sesión 2026-10-07) · modo de marca «Aïki» → «Aiki» y regla general (misma sesión) | Figma (variables, modos, estilos, componentes, capas) y repo (slugs, `[data-brand]`) | vigente · aplicada en Figma y en el sync |
| 2026-10-07 | El foco es un contorno de 2 px (`--border-width-thin`) pegado por fuera del componente, sin hueco y siguiendo su forma (mismo radio), en el color `*/focus-ring` del componente; el borde propio no cambia de grosor (los campos mantienen el fino). Nunca queda espacio entre el borde y el contenido: los medios dentro de una card los recorta la propia card. En CSS: `outline: var(--border-width-thin) solid var(--<componente>-focus-ring); outline-offset: 0` en `:focus-visible`. | David Reina: revisión de estados focus («demasiados borders, demasiado duros, sin espacio entre el foco y el componente» y «no pueden haber gaps entre borde y contenido», sesión 2026-10-07) | Todos los componentes con estado Focus y los que se creen | vigente · aplicada en Figma (31 variantes Focus) |
| 2026-10-07 | Todos los botones de una misma talla miden lo mismo de alto (Button e Icon button: M 48 px, L 64 px; Icon button con `--icon-button-size-*`), y el texto de un botón va siempre en una sola línea: si no cabe, se acorta el texto, nunca se parte. | David Reina: Timer, «Pausar» e Icon button de reiniciar a distinta altura; «norma para todos los botones… el texto nunca irá a dos líneas» (sesión 2026-10-07) | Button, Icon button y cualquier componente que los combine (Timer, Navbar, Modal, Hero) | vigente · aplicada en Figma y en components.css · recogida en las fichas de Button e Icon button |
| 2026-10-08 | **No puede haber dos secciones seguidas con fondo crema** (`color/surface/page`). Entre dos cremas va otro fondo del DS: blanco (`color/surface/card`), amarillo (`color/surface/brand`, con la trama de fideos `Decoration / Noodle texture` como en las landings), verde natural o tinta. Se comprueba con las secciones que se ocultan (sin promoción, sin campaña): si al ocultar una quedan dos cremas juntas, se cambia el fondo de la siguiente. | David Reina: «una norma. no puede haber dos fondo crema seguidos» (sesión 2026-10-08) | Composición de todas las pantallas; en la Home: Hero crema · Promo amarillo con trama · Natural formula verde · Product categories crema · Recipes blanco · Banner crema · FAQ blanco · Where to buy amarillo con trama · Footer tinta | vigente · aplicada en Figma (Promo, FAQ) y en components.css |
