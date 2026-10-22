# GB Noodles · Microsites · Tokens en formato DTCG  _(espejo generado)_

> ⚙️ **Archivos generados — no editar a mano.** Los produce `scripts/tokens-dtcg.py` a partir
> de `design-system/tokens/tokens.json`. Regenerar con `python3 scripts/tokens-dtcg.py`.
> Esta carpeta está vacía hasta el primer sync desde Figma.

## Qué es y qué no es

Es un **tercer espejo** del mismo design system, escrito en el formato del *Design Tokens
Format Module* del Design Tokens Community Group, el borrador que suele llamarse «el estándar
W3C de tokens». Existe para que herramientas externas lean los tokens sin conocer el formato
propio del proyecto: Style Dictionary, Tokens Studio, importadores de otras plataformas.

La cadena de verdad no cambia:

```
Figma  →  tokens/tokens.json + tokens/tokens.css  →  tokens/w3c/*.tokens.json
(fuente)        (espejos del sync)                     (espejo del espejo)
```

**El código del proyecto no consume esta carpeta.** Las pantallas y `css/components.css`
siguen usando `var(--token)` de `tokens/tokens.css`. Esto es solo salida hacia fuera.

## Los modos, que es donde el formato se queda corto

El formato DTCG **no define modos ni temas**. Describe una estructura estática. Se resuelve
con la convención del ecosistema: **un archivo por modo**, y el consumidor combina.

Cada colección de Figma con más de un modo se convierte en un eje. Las de un solo modo caen
todas en `base.tokens.json`. `manifest.json` declara los ejes y deja escritas todas las
combinaciones válidas.

**Combina siempre `base.tokens.json` más un archivo de cada eje antes de resolver los alias.**
Un archivo de modo por sí solo tiene referencias colgando, porque apunta a la capa primitiva.

## Correspondencia con los niveles del DS

El formato no tiene opinión sobre capas: los niveles se expresan como grupos anidados más
alias encadenados. El nivel de componente, si el DS lo tiene, no se exporta cuando vive solo
dentro de Figma y nunca llega al código.

## Metadatos propios

Lo que el formato no contempla va en `$extensions`, bajo la clave del proyecto: el nombre
canónico de la variable en Figma, su identificador, sus scopes y la variable CSS equivalente.

## Avisos conocidos

- **El formato es un borrador**, no un estándar cerrado, y su versión vigente advierte de no
  tomarla como autoritativa. Se emite la sintaxis del borrador actual: color como objeto con
  `colorSpace` y `components`, y dimensiones como objeto con `value` y `unit`. Las herramientas
  antiguas que esperan `"#1bdea6"` y `"16px"` como cadenas no leerán esto tal cual.
- El generador **no inventa nada**. Avisa y deja fuera lo que no tiene equivalente en el
  formato (booleanos, cadenas sin tipo tipográfico) y lo que apunta a un alias inexistente.
- Avisa también de **huecos entre modos**: un token con valor en un modo y sin valor en otro.
  Eso es una desviación del DS, se corrige en Figma y se vuelve a correr el sync, nunca
  editando la salida.

## Comprobación

`python3 scripts/tokens-dtcg.py --check` no escribe y sale con código 1 si esta carpeta no
coincide con lo que saldría de `tokens.json`. Sirve para CI y para el gancho de pre-commit.
