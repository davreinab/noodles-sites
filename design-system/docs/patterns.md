# GB Noodles · Microsites · Patrones (componentes compuestos)

> Catálogo de **patrones (componentes compuestos)**, construidos a partir de los átomos de `components.md`. Cada patrón tiene su **ficha** en `patterns/<slug>.md` (este archivo es el índice más las secciones manuales), y cada ficha es un **contrato** con dos partes:
> - **Parte viva** (anatomía, medidas, variantes, tokens que consume) → se **sincroniza
>   desde Figma** (modelo B, ver `design.md`) en el bloque `GENERATED` de la ficha. No editar a mano.
> - **Parte de criterio** (cuándo usar, qué NO hace, accesibilidad) → se escribe a mano
>   una vez debajo del bloque, porque no es expresable como variable de Figma.
>
> Reglas duras: no se inventa un patrón que no esté aquí; los patrones se componen de átomos y consumen
> **tokens semánticos** de `tokens.css`, nunca primitivos ni hex.

**Estado:** 18 patrones sincronizados el 2026-10-07T18:41:16Z · una ficha por archivo en `patterns/<slug>.md` (este archivo solo guarda el índice y las secciones manuales).

---

## Índice

- [Navbar](patterns/navbar.md) · pattern · `navbar` · ✅ criterio completo
- [Mobile menu](patterns/mobile-menu.md) · pattern · `mobile-menu` · ✅ criterio completo
- [Product filter](patterns/product-filter.md) · pattern · `product-filter` · ✅ criterio completo
- [Footer](patterns/footer.md) · pattern · `footer` · ✅ criterio completo
- [Hero](patterns/hero.md) · pattern · `hero` · ✅ criterio completo
- [Marquee](patterns/marquee.md) · pattern · `marquee` · ✅ criterio completo
- [Promo](patterns/promo.md) · pattern · `promo` · ✅ criterio completo
- [Natural formula](patterns/natural-formula.md) · pattern · `natural-formula` · ✅ criterio completo
- [Product carousel](patterns/product-carousel.md) · pattern · `product-carousel` · ✅ criterio completo
- [Recipes](patterns/recipes.md) · pattern · `recipes` · ✅ criterio completo
- [Banner](patterns/banner.md) · pattern · `banner` · ✅ criterio completo
- [FAQ](patterns/faq.md) · pattern · `faq` · ✅ criterio completo
- [Where to buy](patterns/where-to-buy.md) · pattern · `where-to-buy` · ✅ criterio completo
- [Product hero](patterns/product-hero.md) · pattern · `product-hero` · ✅ criterio completo
- [Product details](patterns/product-details.md) · pattern · `product-details` · ✅ criterio completo
- [Preparation](patterns/preparation.md) · pattern · `preparation` · ✅ criterio completo
- [Recipe hero](patterns/recipe-hero.md) · pattern · `recipe-hero` · ✅ criterio completo
- [Library](patterns/library.md) · pattern · `library` · ✅ criterio completo

## Cómo rellenar una ficha

Cada ficha nace con el bloque generado y cuatro campos de criterio en `⬜ TODO` (su forma exacta:
`patterns/_plantilla.md`). Se escriben una vez, a mano, y el sync los conserva:

- **Propósito:** para qué sirve y qué problema resuelve.
- **Ejemplo de código:** snippet HTML mínimo con las clases reales de `components.css`, en su variante
  por defecto; una línea por variante o estado relevante si cambia el markup. Es la referencia que
  copian pantallas y agentes, y el sync lo copia al schema (`source.code.example`).
- **Accesibilidad (pares AA verificados):** los pares texto/fondo comprobados en claro y oscuro; el
  *rol* (button, textbox, checkbox, dialog… o «decorativo»); *de dónde sale su nombre* (texto visible,
  etiqueta asociada o atributo explícito: un icono sin texto siempre necesita nombre explícito); *qué se
  anuncia al cambiar de estado* (seleccionado, expandido, inválido, ocupado… un estado que solo se ve
  por color no existe para quien no ve); *teclado* (qué teclas lo operan; si no se puede usar sin
  ratón, no está terminado); *foco* (dónde entra, dónde sale, si queda atrapado a propósito) y *qué se
  oculta al lector* (partes decorativas o redundantes).
- **Cuándo usar / qué NO hace:** el límite del patrón; lo que parece suyo y es de otro.

## Catálogo propuesto (⬜ por definir en Figma)

## Composición de pantalla — reglas   ✍️ manual · 2026-10-07

> Cómo se **colocan** los componentes en una página. Es el tercer nivel del DS (tokens →
> componentes → composición) y el que evita que cada pantalla decida su propio espaciado.
> Toda medida citada aquí es un token de `tokens.css`; si falta, se crea en Figma primero.
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
| navbar | fija arriba, se oculta al bajar | igual | `--layer-sticky` | `--motion-duration-base` |
| suggestion bubble | abajo a la derecha | igual, se pliega a icono | `--layer-floating` | `--motion-duration-fast` |

_Las capas se llaman `--layer-*` en este proyecto (no `--z-*`). Todo movimiento respeta
`prefers-reduced-motion`._

### Flujo de contenido
- Orden de lectura y jerarquía de títulos por tipo de página:
  - **Home:** Navbar · Hero · Promo (solo con campaña activa) · Marquee · Natural formula · Product carousel · Recipes · Banner · FAQ · Where to buy · Footer · Suggestion bubble. Sin campaña, el CTA del Hero lleva a producto y después a recetas.
  - **Product page:** Product hero · Product details · Preparation · Recipes (que usan el producto) · Where to buy.
  - **Recipe page:** Recipe hero · Product details (valores de la receta) · Preparation sin Timer y con Step Media=True · Recipes relacionadas.
  - **Libraries (producto, receta, concurso):** Library con la card y el filtro que toquen.
  - **Natural formula page y FAQS:** cabecera + texto en columna de lectura + FAQ (en FAQS, un bloque por categoría).
  - Un solo `h1` por página (claim del hero, nombre del producto o de la receta, título de la librería); cada sección abre con `h2`; las cards usan `h3`.
- Dónde van las acciones primarias (cabecera, pie de panel, fin de formulario): la acción principal de la página está en el hero (Button L en desktop, M en móvil); en cada sección, una sola acción al final o junto al título (Link «Ver todos»); en el Modal, en el pie alineada a la derecha (a todo el ancho en Full); en formularios, al final y a la izquierda. «Dónde comprar» es la acción recurrente (Navbar y Product hero).
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
