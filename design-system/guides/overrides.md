# Overrides del DS  🧪  (probar un cambio antes de que esté en Figma)

> Guía de `design-system/design.md`: se lee solo cuando la tarea lo pide (la tabla de «Enrutado» de `design.md` dice cuándo).

Una pantalla a veces necesita un cambio de un componente que todavía no existe en Figma: un
tamaño nuevo, un estado, un espaciado. No se toca `css/components.css`, porque eso es lo que Figma
dicta, ni se escribe un `<style>` en la página (regla 1b). El cambio se escribe aparte:

- `UI/overrides/<id>.css`, donde `<id>` es el de una propuesta de cambio en `proposals/`
  (`<id>.proposal.json`, en `draft` o `approved`). Sin propuesta no hay override.
- Se enlaza con `<link>` **solo** desde las pantallas donde se prueba, después de `components.css`.
- Su CSS cumple las mismas reglas que el resto: valores con tokens, nada a mano.
- Vive mientras la propuesta esté pendiente. Cuando se aplica en Figma y se sincroniza, o se
  rechaza, el archivo sobra y se borra: el cambio ya viene por el sync, o no viene.

`scripts/token-audit.py` lo vigila: aviso por cada override vivo (diseño sabe qué pantallas no
siguen exactamente al DS), y error si no tiene propuesta, si su propuesta ya está `applied` o
`rejected`, o si alguien lo mete en la página como `<style data-ds-override>`.
