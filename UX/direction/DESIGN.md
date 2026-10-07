# DESIGN.md — dirección visual de GB Noodles · Microsites   ✍️ manual · ⬜ TODO 2026-10-07

> Escrito para que lo lea un agente antes de tocar estilo. Describe **intención**, no
> valores: los valores nacen en Figma como tokens y llegan por sync. Si una sección está en
> `⬜ TODO`, el agente no la rellena por su cuenta: pide referencias o decisión.

## Tono
Divertido, retador y maduro; nunca infantil ni de «comida barata». Se purga lo infantil, lo
«gamer» y el lenguaje de pereza. La transparencia se muestra grande, no en letra pequeña
(«anti-bullshit»). (Traspaso §4 y §5.)

## Paleta (intención)
Los microsites no heredan código ni tokens de las landings: el DS se define desde cero con el
estándar del proyecto (decisión de David Reina, 2026-10-07). Se conservan solo los **colores de
marca**, que son de la marca y no del código. El fondo amarillo es común a todas las marcas; cada marca redefine sus colores de marca con
los mismos nombres de token, así que los componentes no cambian. Un verde dedicado al claim
natural y un rojo para la pill «NUEVO». Bélgica (Aïki) es la excepción visual más marcada.

⬜ TODO — Cuántos colores de marca y qué papel tiene cada uno; temperatura y saturación;
relación fondo/superficie/texto; qué comunica el color de acento y dónde aparece; si la
marca usa **degradados** y dónde (si no se declaran aquí, no se usan); qué está prohibido.
Las **transparencias** lo están siempre (regla 7 de `design.md`): un tono sobre otro fondo es
un color opaco propio, no una opacidad. Contraste AA obligatorio en claro y oscuro (regla 8):
la intención debe ser alcanzable con ese límite.

## Tipografía (intención)
Dos familias: una display condensada en mayúsculas para titulares y labels (Anton, provisional:
Dirty Headline exige licencia comercial y no tiene acentos; el cliente ha pedido una parecida que
sí los tenga) y Archivo para el cuerpo. Escalas Desktop y Mobile explícitas, definidas en Figma
(2026-10-07).

⬜ TODO — Una familia o dos y por qué; carácter (geométrica, humanista, mono para datos…);
jerarquía esperada (cuántos niveles se necesitan de verdad); densidad de texto típica.

## Forma, espacio y ritmo
Definido desde cero en Figma (2026-10-07): grid de 8, radios 8/16/24 y pill, bordes de 2 y 4,
sombras duras sin blur como recurso de marca (elevation/1-2) y una suave para capas flotantes
(elevation/3). Recursos de marca: fideos en SVG, la «ball» del pack y texturas orgánicas o hechas
a mano. Los componentes base (botones, inputs, iconos, fideos) pueden partir de las landings; los
complejos se definen de nuevo.

⬜ TODO — Radios (rectos, suaves, redondos), densidad (compacta / aireada), uso de bordes
frente a fondos para separar, sombras sí o no y para qué. Todo múltiplo de 4 (regla 8-point).

## Patrones de interacción recurrentes
⬜ TODO — Cómo se comportan las cosas que se repiten: dónde van las acciones primarias,
cómo se confirma una acción destructiva, cómo se muestran estados vacíos, carga y error,
cómo se navega entre niveles. Lo que aquí se decida alimenta
`design-system/docs/patterns.md § Composición de pantalla` cuando existan tokens.

## Movimiento
⬜ TODO — Cuánto y para qué (orientar, confirmar, nunca decorar). Duraciones y easings
nacerán como tokens `motion/*` en Figma.

## Referencias seleccionadas
- Huel y Oats Overnight — la nutrición como elemento visual (traspaso §4). Aún sin nota en
  [`references/`](./references/).
- ⬜ TODO — el resto. Una línea por referencia: `NN-slug` — qué se traslada al producto y qué no.

| Ref. | Qué se traslada | Qué NO se traslada |
|---|---|---|
| | | |

## Decisiones tomadas
_(fecha · decisión · motivo. Cuando una decisión de aquí se convierte en token o en regla de
`patterns.md`, se anota el enlace.)_
