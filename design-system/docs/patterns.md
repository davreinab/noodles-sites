# GB Noodles · Microsites · Patrones (componentes compuestos)

> Catálogo de **patrones (componentes compuestos)**, construidos a partir de los átomos de `components.md`. Cada patrón tiene su **ficha** en `patterns/<slug>.md` (este archivo es el índice más las secciones manuales), y cada ficha es un **contrato** con dos partes:
> - **Parte viva** (anatomía, medidas, variantes, tokens que consume) → se **sincroniza
>   desde Figma** (modelo B, ver `design.md`) en el bloque `GENERATED` de la ficha. No editar a mano.
> - **Parte de criterio** (cuándo usar, qué NO hace, accesibilidad) → se escribe a mano
>   una vez debajo del bloque, porque no es expresable como variable de Figma.
>
> Reglas duras: no se inventa un patrón que no esté aquí; los patrones se componen de átomos y consumen
> **tokens semánticos** de `tokens.css`, nunca primitivos ni hex.

**Estado:** 4 patrones sincronizados el 2026-10-07T14:34:50Z · una ficha por archivo en `patterns/<slug>.md` (este archivo solo guarda el índice y las secciones manuales).

---

## Índice

- [Navbar](patterns/navbar.md) · pattern · `navbar` · ⬜ 5 pendientes
- [Mobile menu](patterns/mobile-menu.md) · pattern · `mobile-menu` · ⬜ 5 pendientes
- [Product filter](patterns/product-filter.md) · pattern · `product-filter` · ⬜ 5 pendientes
- [Footer](patterns/footer.md) · pattern · `footer` · ⬜ 5 pendientes

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

## Composición de pantalla — reglas   ✍️ manual · ⬜ TODO 2026-10-07

> Cómo se **colocan** los componentes en una página. Es el tercer nivel del DS (tokens →
> componentes → composición) y el que evita que cada pantalla decida su propio espaciado.
> Toda medida citada aquí es un token de `tokens.css`; si falta, se crea en Figma primero.
> Las pantallas de `UI/` y el agente consultan esta sección antes de montar cualquier vista.

### Ritmo vertical
| Entre… | Token | Notas |
|---|---|---|
| secciones de página | ⬜ TODO (`--spacing-*`) | |
| bloques dentro de una sección | ⬜ TODO | |
| título de sección y su contenido | ⬜ TODO | |
| campos de un formulario | ⬜ TODO | |

### Contenedores y anchos
| Contenedor | Token `--layout-*` | Dónde se usa |
|---|---|---|
| página (max-width) | ⬜ TODO | |
| columna de lectura / prosa | ⬜ TODO | |
| panel lateral / drawer | ⬜ TODO | |
| modal | ⬜ TODO | |

### Grid y breakpoints
| Breakpoint | Ancho | Columnas | Gutter (token) | Margen (token) | Qué cambia |
|---|---|---|---|---|---|
| mobile | ⬜ TODO | | | | |
| tablet | ⬜ TODO | | | | |
| desktop | ⬜ TODO | | | | |

_Los breakpoints se declaran también en `scripts/token-audit.config.json` (`breakpoints`);
CSS no admite `var()` en `@media`, por eso son la única medida que vive como convención._

### Paneles, overlays y capas
| Elemento | Desktop | Mobile | Capa (`--z-*`) | Motion (`--motion-*`) |
|---|---|---|---|---|
| drawer / panel lateral | ⬜ TODO | | | |
| modal | ⬜ TODO | | | |
| toast | ⬜ TODO | | | |

### Flujo de contenido
- Orden de lectura y jerarquía de títulos por tipo de página: ⬜ TODO
- Dónde van las acciones primarias (cabecera, pie de panel, fin de formulario): ⬜ TODO
- Estados vacíos, carga y error a nivel de página: ⬜ TODO

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
