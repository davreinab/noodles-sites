# Capturas del wireframe UX (Figma)

Capturas de solo lectura del archivo de wireframes UX «Rediseño sites · GB Noodles»
(Figma `1YhsCqdqYCHlK4Y82IY5G3`), sección Desktop `565:13925` y sección Mobile `567:13926`,
tomadas el 2026-10-22 y 2026-10-23 para adaptar el design system y montar las pantallas de `UI/`.

Sirven para **estructura y contenido**, no para estilo: los grises del wireframe no son colores.
El estilo lo da el design system (`design-system/`). La descripción escrita de cada pantalla y sus
estados está en [`context/user-flow.md`](../../../context/user-flow.md); si una captura y ese texto
no coinciden, manda el texto (recoge las decisiones tomadas después).

Nombre de archivo: `<pantalla>-<desktop|mobile|movil>-NN-<capa>-<nodo>.png`, donde `NN` es el orden
de la sección de arriba abajo y `<nodo>` el id del frame en Figma (`396-6073` = `396:6073`). Sin
`NN`, es la pantalla completa.

| Carpeta | Pantalla | Nodos (desktop · móvil) |
|---|---|---|
| `desktop-general/` | Vista general y todas las pantallas desktop | sección `565:13925` |
| `mobile-general/` | Vista general y pantallas móviles | sección `567:13926` |
| `product-page/` | Ficha de producto y modales de etiqueta y alérgenos | `396:6073` · `396:12701`; modales `490:7469`, `490:11998` |
| `product-library/` | Catálogo con anclas | `396:5932` · `396:12565` |
| `recipe-library/` | Recetas: base, filtrada y sin resultados | `171:3808`, `483:5711`, `485:6064` · `486:13025`, `265:3948`, `486:14260` |
| `recipe-page/` | Receta y modal de compartir | `396:6290` (sin móvil) · modal `500:8062` / `502:16757` |
| `natural-formula/` | 100% Natural formula | `274:6354` · `319:2744` |
| `contest-library/` | Concursos | `190:3727` · `273:7157` |
| `contest-page/` | Página de concurso | `330:6557` · `361:8516` |
| `contest-result/` | Resultado: no ganas, ganas, límite | `490:13618`, `490:13957`, `490:13867` · `501:14641`, `501:15446`, `501:15170` |
| `faq/` | FAQ: base, con resultados, sin resultados | `428:10606`, `428:10962`, `495:14043` · `428:12306`, `501:14324`, `428:12490` |
| `legal/` | Política de privacidad | `377:8301` · `381:14542` |

Notas: en Figma, los resultados de concurso se llaman «Legal Page» y varias capas de FAQ y legal se
llaman «Prizes» (restos de plantilla). La captura móvil antigua `97:636` era la Home, no el catálogo:
la del catálogo es `product-library-mobile-real.png`.
