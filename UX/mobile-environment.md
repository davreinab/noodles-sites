# Entorno móvil simulado — GB Noodles · Microsites   ✍️ manual

**Aplica:** sí — web responsive mobile-first; el público llega sobre todo desde el móvil
(traspaso §2 y §4, 2026-10-07).

> Cuando aplica, los wireframes y pantallas móviles se construyen con **tecnologías web**,
> simulando el entorno, y no en nativo: el ciclo de iteración es el de la web. Este archivo es
> la **especificación del entorno** dentro del cual se interpretan todas las peticiones
> móviles. El agente lo lee antes de crear o modificar cualquier pantalla móvil.

## Plataforma de referencia
⬜ TODO — iOS, Android o ambas; cuál manda si difieren.

## Dimensiones de pantalla de referencia
| Uso | Ancho × alto (px CSS) | Notas |
|---|---|---|
| Base de diseño | ⬜ TODO (p. ej. 390 × 844) | |
| Mínimo soportado | ⬜ TODO | |
| Máximo (tablet si aplica) | ⬜ TODO | |

Zonas seguras: ⬜ TODO (barra de estado, notch, barra de gestos; alturas en px).

## Gestos y comportamiento táctil
⬜ TODO — Qué gestos se esperan (tap, long-press, swipe para volver o borrar, pull to
refresh) y qué hace cada uno. Área táctil mínima (44 px iOS / 48 px Android; múltiplo de 4).

## Navegación
⬜ TODO — Patrón principal (tab bar, drawer, pila con volver), dónde vive el título, cómo se
vuelve, cómo se cierra un modal o una hoja inferior. Convenciones de la plataforma que se
respetan y cuáles se rompen a propósito.

## Teclado, formularios y estados
⬜ TODO — Qué pasa al abrir el teclado; tipos de teclado por campo; estados de carga, vacío,
error y sin conexión.

## Cómo se simula en HTML
- Un contenedor con las dimensiones base, centrado, con las zonas seguras dibujadas.
- Interacciones táctiles simuladas con eventos de puntero; sin hover como único estado.
- Los wireframes usan la paleta `--wf-*`; las pantallas de UI, los tokens del DS. Las medidas
  móviles (anchos, zonas seguras, áreas táctiles) nacen como tokens `--layout-*` en Figma
  cuando exista el DS.
