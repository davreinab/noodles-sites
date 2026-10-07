# DESIGN.md — dirección visual de GB Noodles · Microsites   ✍️ manual · ⬜ TODO 2026-10-07

> Escrito para que lo lea un agente antes de tocar estilo. Describe **intención**, no
> valores: los valores nacen en Figma como tokens y llegan por sync. Si una sección está en
> `⬜ TODO`, el agente no la rellena por su cuenta: pide referencias o decisión.

## Tono
Divertido, retador y maduro; nunca infantil ni de «comida barata». Se purga lo infantil, lo
«gamer» y el lenguaje de pereza. La transparencia se muestra grande, no en letra pequeña
(«anti-bullshit»). (Traspaso §4 y §5.)

## Paleta (intención)
Intención heredada de las landings de la Fase 1 (traspaso §9; referencia, no tokens finales):
el fondo amarillo es común a todas las marcas; cada marca redefine sus colores de marca con
los mismos nombres de token, así que los componentes no cambian. Un verde dedicado al claim
natural y un rojo para la pill «NUEVO». Bélgica (Aïki) es la excepción visual más marcada.

⬜ TODO — Cuántos colores de marca y qué papel tiene cada uno; temperatura y saturación;
relación fondo/superficie/texto; qué comunica el color de acento y dónde aparece; si la
marca usa **degradados** y dónde (si no se declaran aquí, no se usan); qué está prohibido.
Las **transparencias** lo están siempre (regla 7 de `design.md`): un tono sobre otro fondo es
un color opaco propio, no una opacidad. Contraste AA obligatorio en claro y oscuro (regla 8):
la intención debe ser alcanzable con ese límite.

## Tipografía (intención)
Dos familias (traspaso §9): una display condensada de titulares (Dirty Headline en las landings:
**hay que comprar la licencia** para uso comercial; Anton es la alternativa aprobada; no tiene
acentos y el cliente ha pedido una parecida que sí los tenga) y Archivo para el cuerpo. Escala
fluida.

⬜ TODO — Una familia o dos y por qué; carácter (geométrica, humanista, mono para datos…);
jerarquía esperada (cuántos niveles se necesitan de verdad); densidad de texto típica.

## Forma, espacio y ritmo
Heredado de las landings (traspaso §9): radios generosos y pills, bordes gruesos, **sombras
duras sin blur** con offset sólido del color de marca. Recursos de marca: fideos en SVG, la
«ball» del pack y texturas orgánicas o hechas a mano.

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
