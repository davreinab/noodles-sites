<!-- vigencia
  autoridad: ⬜ TODO — quién manda sobre este documento (cliente, negocio, legal, el equipo)
  confirmado: ⬜ TODO — fecha ISO de la última vez que alguien dijo «esto sigue siendo verdad»
  estado: pendiente-de-confirmar
  Las reglas de PROPIEDAD no caducan (un identificador no cambia de naturaleza). Las de
  DECISIÓN sí: caducan a los 6 meses de «confirmado» y la auditoría avisa, no bloquea.
-->

# Usuarios — GB Noodles · Microsites

Para quién se diseña. Dos cosas distintas que conviene no mezclar:

- **Perfil** — *quién* es y en qué circunstancia usa esto. Existe siempre, haya o no cuentas.
- **Rol** — *qué le deja hacer el sistema*. Solo existe si el producto tiene autenticación o
  permisos diferenciados.

Un mismo rol puede contener perfiles que necesitan interfaces muy distintas: quien entra
tres veces al día desde el escritorio y se lo sabe de memoria, y quien entra dos veces al año
desde el móvil y no recuerda dónde estaba el botón, tienen los mismos permisos y no se diseña
igual para ellos. Si aquí solo se guarda el rol, esas dos personas son indistinguibles y el
producto acaba sirviendo a una de las dos por accidente, normalmente a la que el equipo tiene
más cerca.

Los identificadores `P-` son estables (regla 5). El vocabulario de esta página manda sobre
todos los documentos, wireframes y pantallas (regla 9).

---

## Perfiles

Quién usa el producto y en qué circunstancia. **Esto no son «personas» de manual**: no se
inventan nombres, edades, fotos ni aficiones. Lo que va aquí es lo que cambia una decisión de
diseño y se puede sostener con evidencia o declarar como hipótesis.

| ID | Perfil | Contexto de uso | Frecuencia | Restricciones | Rol | Estado |
|---|---|---|---|---|---|---|
| P-01 | **El Activista Urbano Consciente** («Lucas», 24, FR/BE). Usa Yuka y entiende la comida como un acto político; si la web esconde algo, se va | Móvil; ⬜ TODO resto | ⬜ TODO | Necesita ver los ingredientes desglosados de forma radical y transparente desde el primer impacto | — | `hipótesis` (traspaso §4) |
| P-02 | **La Pragmática de Alto Rendimiento** («Valentina», 29, ES/IT). Quiere comer en menos de 5 minutos algo equilibrado y sabroso; odia la estética infantil y los sorteos sin valor | Móvil; ⬜ TODO resto | ⬜ TODO | Le sirven un diseño maduro y urbano, recetas para «hackear» el noodle y el botón «dónde comprar» | — | `hipótesis` (traspaso §4) |

Público objetivo: 18 a 35 años, que llega sobre todo desde el móvil (traspaso §4). Los nombres
y edades son los de las personas definidas por el proyecto, no evidencia con usuarios.

**Principios UX derivados de estos perfiles** (traspaso §4):
- Anti-bullshit: la transparencia se muestra grande, no en letra pequeña.
- La nutrición como elemento visual (referentes: Huel, Oats Overnight).
- Recetas en vídeo vertical.
- Respetar la ley de Jakob y los patrones estándar de navegación.
- Accesibilidad WCAG con contraste de 4.5:1.
- Purgar lo infantil, lo «gamer» y el lenguaje de pereza.

- **Contexto de uso** — dónde, en qué dispositivo y en medio de qué otra cosa.
- **Frecuencia** — cada cuánto vuelve. Cambia más decisiones que ninguna otra columna:
  determina cuánto se puede dar por aprendido.
- **Restricciones** — lo que no puede hacer aunque tenga permiso: sin formación, sin tiempo,
  sin conexión estable, con el móvil en una mano.
- **Rol** — el rol de abajo que le corresponde, o `—` si el producto no tiene roles.
- **Estado** — obligatorio, una de dos:
  - `observado (R-… §O-n)` · `observado (A-… §D-n)` — hay evidencia que lo sostiene, y esa
    evidencia viene de los usuarios: la nota que se cita tiene `voice: usuario`, o es una
    lectura de analítica de lo que hace la gente de verdad.
  - `hipótesis` — el equipo cree que existe, pero nadie lo ha comprobado con usuarios. **Un
    perfil descrito por un stakeholder, por bien que lo conozca, es una hipótesis**: sabe
    cómo cree que trabaja su gente, que no siempre es cómo trabaja. Se cita igual la nota de
    origen; lo que cambia es lo que se puede afirmar con ella.

  Un perfil marcado como hipótesis es honesto y sirve igual para diseñar. Un perfil **sin
  estado** es una invención con aspecto de dato, y es la forma más común de saltarse la
  regla 1 sin que se note.

## Roles y permisos

**Aplica: ⬜ TODO** _(`sí` / `no` · si es `no`, indicar fecha y quién lo decidió)_

Qué le deja hacer el sistema a cada quien. **Solo aplica si el producto tiene autenticación o
permisos diferenciados.** Una web pública, una herramienta de un solo usuario o un sitio de
marca no tienen roles: se marca `Aplica: no` y esta sección se queda vacía. No se inventa una
jerarquía de permisos para rellenar el hueco.

### <Rol>
<Qué puede hacer y qué no. Los nombres de los roles son los que consume el modelo de datos
y los contratos del design system: un sinónimo es un error (regla 9).>
