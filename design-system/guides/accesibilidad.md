# Borradores de accesibilidad  ♿  (la IA propone, una persona aprueba)

> Guía de `design-system/design.md`: se lee solo cuando la tarea lo pide (la tabla de «Enrutado» de `design.md` dice cuándo).

El contraste AA lo mide `ds-fidelity` desde el CSS; nadie lo escribe. El campo **Accesibilidad (rol,
nombre, estados y teclado)** de cada ficha es para lo que el color no cubre y ni Figma ni el CSS dicen:
cómo se comporta el componente para quien usa lector de pantalla o teclado. Rellenarlo a mano en cientos
de fichas no es realista, así que la IA redacta un borrador y una persona lo revisa en la library.

**Cuándo.** Cuando lo pidan («propón la accesibilidad de los componentes de la página Buttons») y al
verificar un componente contra su maestro si el campo está vacío. **Siempre por tandas, una página de
Figma cada vez**, nunca el DS entero de golpe:

```bash
python3 scripts/ds-text-proposal.py --missing accesibilidad --page "Buttons"   # qué falta en esa página
```

Cuenta como pendiente el campo vacío y también el que solo habla de contraste (lo que se apuntaba antes
de la 12.7.0): ese texto se reescribe entero, porque el contraste ya no va en la ficha.

**Qué escribir**, a partir del contrato (`api.props`, `api.events`, nombre, descripción, anatomía) y
del ejemplo de código, en líneas cortas:
- **Rol:** qué es para un lector de pantalla (botón, enlace, casilla, opción de un grupo, pestaña,
  diálogo, campo de texto…), con el elemento HTML nativo que lo da (`<button>`, `<a>`, `<input type=…>`).
- **Nombre:** de dónde sale (texto visible, `<label>` asociado, `aria-label`). Un icono sin texto
  siempre necesita nombre explícito.
- **Estados:** qué se anuncia al cambiar (seleccionado, expandido, inválido, cargando, deshabilitado)
  y con qué atributo (`aria-checked`, `aria-expanded`, `aria-invalid`, `aria-busy`, `disabled`).
- **Teclado y foco:** qué teclas lo operan, foco visible, dónde entra y sale el foco si abre algo.
- **No aplica:** si el componente es decorativo o solo informativo (sin interacción ni nombre propio),
  el texto es «No aplica.» seguido del motivo. La library ofrece también el botón **No aplica**.

Lo que no se pueda deducir no se inventa: se escribe como pregunta («¿abre en ventana nueva?»).

**Cómo se guarda.** Nunca en la ficha: en la propuesta de textos del componente, la misma que crea el
botón «Editar» de la library, una sola por componente:

```bash
python3 scripts/ds-text-proposal.py --component button --field accesibilidad \
  --text-file /tmp/a11y-button.md --reason "Borrador por tipo de componente" \
  --approver "<persona>" --origin ai
```

En la library aparece como «Pendiente de aprobación» + «Borrador de la IA». Cualquiera puede editarlo
desde ahí (deja de ser borrador de la IA) o marcarlo «No aplica»; al aprobarse se escribe en la ficha
como cualquier propuesta (`proposals/README.md`).
