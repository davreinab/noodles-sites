<!-- vigencia
  autoridad: ⬜ TODO — quién manda sobre este documento (cliente, negocio, legal, el equipo)
  confirmado: ⬜ TODO — fecha ISO de la última vez que alguien dijo «esto sigue siendo verdad»
  estado: pendiente-de-confirmar
  Las reglas de PROPIEDAD no caducan (un identificador no cambia de naturaleza). Las de
  DECISIÓN sí: caducan a los 6 meses de «confirmado» y la auditoría avisa, no bloquea.
-->

# Glosario — GB Noodles · Microsites

Cómo se llaman las cosas en este proyecto. Un término por fila: **el que manda**, los
sinónimos que quedan descartados y dónde se usa.

Existe porque la cadena de trazabilidad que impone esta carpeta se rompe en silencio si el
vocabulario baila. Si el touchpoint dice *pasajero*, la feature dice *cliente* y el
componente se llama *usuario*, la cadena **parece** trazada y no ata nada: cada eslabón es
correcto por separado y nadie detecta que hablan de lo mismo. Es la regla 9 —vocabulario
único— con un sitio donde vivir.

**Qué entra:** cualquier término del dominio que tenga más de una forma posible de decirse,
y todo nombre de entidad, estado o rol que ya esté fijado en
[`data-model.md`](./data-model.md) y [`users.md`](./users.md) — aquí no se redefine, se
enlaza (regla 2): esta tabla dice cuál es la palabra que manda, no qué campos tiene.

**Qué no entra:** términos de oficio que significan lo mismo en cualquier proyecto
(«componente», «token», «wireframe»). Esto es el vocabulario de este cliente y este producto,
no un diccionario de diseño.

## Términos

| Término | Qué es | Sinónimos descartados | Dónde manda | Fuente |
|---|---|---|---|---|
| Cup | Formato vaso (~80% de las ventas). La «girosu» es su imagen destacada | CAP | Catálogo de producto, Product library | Traspaso §12 |
| Bag | Formato bolsa; se lanza en enero de 2027 | — | Catálogo de producto | Traspaso §12 |
| Sauce | Formato salsa | — | Catálogo de producto | Traspaso §5 |
| Original / Yakisoba / Rice | Líneas de la gama Cup | Originals | Catálogo de producto | Traspaso §5 y §12 (el traspaso usa «Original» y «Originals»: ⬜ TODO — confirmar cuál manda) |
| Suggestion box | Botón hacia el formulario externo de Calidad | Babelbox, ticket de ideas | Home, transversales | Traspaso §12 |
| Landing «03» | La estructura final de las landings de la Fase 1 | Demo países | Histórico Fase 1 | Traspaso §12 |
| PS21 | Agencia externa de concursos | — | Concursos | Traspaso §12 |
| Days you can trust | Marca corporativa de GB Foods | — | Footer, sellos | Traspaso §12 |

- **Término** — la palabra que se usa. En singular y tal como la dice el cliente, no como la
  diría el equipo.
- **Sinónimos descartados** — las otras formas que circulan. Se listan precisamente para que
  quien las encuentre sepa a qué apuntan y no cree una tercera.
- **Dónde manda** — en qué documentos, pantallas o contratos del design system aparece. Sirve
  para saber qué hay que revisar el día que el término cambie.
- **Fuente** — quién lo fijó y cuándo, o la nota de research donde el cliente lo dijo
  (`R-… §O-n`). Un término decidido por el equipo sin más también vale: se anota así.

> Cuando el cliente use dos palabras para la misma cosa y no esté claro cuál manda, **no se
> elige en silencio** (regla 10): se pregunta, y la respuesta se anota aquí con su fecha.
