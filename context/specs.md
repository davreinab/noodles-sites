<!-- vigencia
  autoridad: ⬜ TODO — quién manda sobre este documento (cliente, negocio, legal, el equipo)
  confirmado: ⬜ TODO — fecha ISO de la última vez que alguien dijo «esto sigue siendo verdad»
  estado: pendiente-de-confirmar
  Las reglas de PROPIEDAD no caducan (un identificador no cambia de naturaleza). Las de
  DECISIÓN sí: caducan a los 6 meses de «confirmado» y la auditoría avisa, no bloquea.
-->

# Specs funcionales — GB Noodles · Microsites

Especificaciones normativas de los flujos principales. Formato OpenSpec:
- **Requisitos** — qué DEBE / NO DEBE hacer el sistema (sin detalles de implementación).
  Cada requisito lleva **Origen**: la user story de `synthesis.md` de la que nace.
- **Escenarios** — casos concretos verificables (Given / When / Then).

Referencia de pantallas y estados: [`user-flow.md`](./user-flow.md)
Referencia de reglas de negocio: [`business-rules.md`](./business-rules.md)
Referencia de origen (user stories, features, touchpoints): [`synthesis.md`](./synthesis.md)

---

> Requisitos derivados el 2026-10-07 del traspaso, [`business-rules.md`](./business-rules.md) y
> [`user-flow.md`](./user-flow.md); cada uno cita la user story de [`synthesis.md`](./synthesis.md) de la que nace.
> No se especifican las landing pages (fuera del proyecto) ni los temas de
> [`user-flow.md § Elementos sin definir`](./user-flow.md) (falta información).

## F-01 · Home y navegación común

### Requisitos
- R-01.1 El sistema DEBE llevar desde la Home a la acción principal del mercado: la campaña activa o, si no la hay, los productos y después las recetas. — **Origen:** US-01
- R-01.2 El sistema DEBE ocultar entero el módulo de promoción o concurso de la Home cuando no hay una promoción activa. — **Origen:** US-01
- R-01.3 El sistema NO DEBE mostrar más de 3 slides en el hero de la Home. — **Origen:** US-01
- R-01.4 El sistema DEBE mostrar en todas las páginas una navbar que se oculta al bajar y reaparece al subir. — **Origen:** US-01
- R-01.5 El sistema DEBE incluir en todas las páginas un footer común (logo, contacto y navegación) y un bottom footer con los legales del país. — **Origen:** US-11

### Escenarios

#### Escenario: Home con campaña activa
- **Dado** que el mercado tiene una campaña activa
- **Cuando** la persona abre la Home
- **Entonces** la acción principal lleva a la campaña y el módulo de promoción está visible

#### Escenario: Home sin campaña
- **Dado** que el mercado no tiene ninguna promoción activa
- **Cuando** la persona abre la Home
- **Entonces** el módulo de promoción no aparece y la acción principal lleva a los productos

#### Escenario: Navbar al hacer scroll
- **Dado** que la persona está en cualquier página
- **Cuando** baja por la página y después sube
- **Entonces** la navbar se oculta al bajar y reaparece al subir

## F-02 · Fórmula natural y FAQ

### Requisitos
- R-02.1 El sistema DEBE tener una página de la fórmula natural con su propio FAQ. — **Origen:** US-02
- R-02.2 El sistema DEBE presentar el mensaje natural a alto nivel y alineado con el envase. — **Origen:** US-02
- R-02.3 El sistema NO DEBE publicar claims de naturalidad o nutrición distintos de los del envase. — **Origen:** US-02
- R-02.4 El sistema DEBE tener una página FAQS indexable, con las preguntas y las respuestas presentes en el contenido de la página. — **Origen:** US-09

### Escenarios

#### Escenario: Respuesta indexable
- **Dado** que la página FAQS está publicada
- **Cuando** un buscador rastrea la página
- **Entonces** las preguntas y sus respuestas están en el contenido, aunque se muestren plegadas

#### Escenario: Claim del envase
- **Dado** que un claim aparece en la web
- **Cuando** se compara con el envase
- **Entonces** el texto y la cifra coinciden con los del envase

## F-03 · Catálogo de producto

### Requisitos
- R-03.1 El sistema DEBE organizar los productos por formato: Cups (líneas Original, Yakisoba y Rice), Bags y Sauces. — **Origen:** US-03
- R-03.2 El sistema DEBE permitir llegar a cada producto navegando en tres niveles: tipo, línea y sabor. — **Origen:** US-03

### Escenarios

#### Escenario: Llegar a un sabor
- **Dado** que la persona está en la Product library
- **Cuando** elige Cups, después Yakisoba y después un sabor
- **Entonces** llega a la ficha de ese producto

## F-04 · Ficha de producto

### Requisitos
- R-04.1 El sistema DEBE mostrar en la ficha las etiquetas, el nombre, los highlights y las imágenes 3D e interior del producto. — **Origen:** US-04
- R-04.2 El sistema DEBE mostrar los ingredientes jerarquizados y dar acceso a la imagen de la etiqueta del envase en un modal. — **Origen:** US-04
- R-04.3 El sistema DEBE mostrar los alérgenos en negrita. — **Origen:** US-04
- R-04.4 El sistema DEBE mostrar la nutrición de forma visual, con los valores y gráficos validados por el equipo de nutrición de GB Foods. — **Origen:** US-04
- R-04.5 El sistema NO DEBE publicar valores nutricionales sin la validación del equipo de nutrición de GB Foods. — **Origen:** US-04
- R-04.6 El sistema NO DEBE usar fotografía de producto inventada, imágenes que no sean de la marca ni imágenes generadas con IA. — **Origen:** US-04
- R-04.7 El sistema DEBE incluir la preparación con GIF o vídeo y un temporizador de 3 minutos. — **Origen:** US-05

### Escenarios

#### Escenario: Alérgenos
- **Dado** que un producto contiene trigo y soja
- **Cuando** la persona lee sus ingredientes
- **Entonces** «trigo» y «soja» aparecen en negrita

#### Escenario: Etiqueta del envase
- **Dado** que la persona está en la ficha de un producto
- **Cuando** pide ver la etiqueta del envase
- **Entonces** se abre un modal con la imagen de la etiqueta

#### Escenario: Temporizador
- **Dado** que la persona está en la preparación de un producto
- **Cuando** inicia el temporizador
- **Entonces** cuenta 3 minutos y avisa al terminar

## F-05 · Recetas

### Requisitos
- R-05.1 El sistema DEBE tener una librería de recetas y una página por receta. — **Origen:** US-06
- R-05.2 El sistema DEBE mostrar en cada receta la imagen principal, los ingredientes, la nutrición y los pasos. — **Origen:** US-06
- R-05.3 El sistema DEBE mostrar los productos de la marca que usa la receta como chips que enlazan a su ficha. — **Origen:** US-06
- R-05.4 El sistema NO DEBE mostrar vídeo en la receta en el lanzamiento. — **Origen:** US-06
- R-05.5 El sistema NO DEBE ofrecer un buscador de recetas por ingredientes. — **Origen:** US-06

### Escenarios

#### Escenario: Producto de una receta
- **Dado** que la receta usa Yatekomo Pollo
- **Cuando** la persona pulsa su chip
- **Entonces** llega a la ficha de Yatekomo Pollo

## F-06 · Concursos

### Requisitos
- R-06.1 El sistema DEBE admitir los tres modelos de concurso: estructura propia, iframe de la agencia o enlace externo. — **Origen:** US-07
- R-06.2 El sistema DEBE publicar las bases legales de cada concurso. — **Origen:** US-07
- R-06.3 El sistema NO DEBE publicar un concurso en iframe sin la revisión previa de protección de datos. — **Origen:** US-07
- R-06.4 El sistema DEBE permitir publicar concursos sin una página agregadora (la Contest library es opcional). — **Origen:** US-07

### Escenarios

#### Escenario: Bases legales
- **Dado** que un concurso está publicado
- **Cuando** la persona lo consulta
- **Entonces** puede llegar a sus bases legales

#### Escenario: Concurso en iframe
- **Dado** que un concurso es un iframe de la agencia
- **Cuando** se va a publicar
- **Entonces** no se publica hasta tener la revisión de protección de datos

## F-07 · Dónde comprar

### Requisitos
- R-07.1 El sistema DEBE incluir en la Home el acceso a dónde comprar el producto en el país de la web. — **Origen:** US-08

### Escenarios

#### Escenario: Dónde comprar
- **Dado** que la persona está en la Home de su mercado
- **Cuando** busca dónde comprar
- **Entonces** encuentra el acceso a los puntos de venta de su país

## F-08 · Feedback, contacto y legales

### Requisitos
- R-08.1 El sistema DEBE mostrar en todas las páginas la suggestion bubble, que lleva al formulario externo de Calidad. — **Origen:** US-10
- R-08.2 El sistema DEBE resolver el contacto con el formulario externo de GB Foods. — **Origen:** US-11
- R-08.3 El sistema DEBE publicar los legales propios de cada país: Privacy, Legal notice, Cookies, Lawful basis y Contest rules. — **Origen:** US-11

### Escenarios

#### Escenario: Sugerencia
- **Dado** que la persona está en cualquier página
- **Cuando** pulsa la suggestion bubble
- **Entonces** llega al formulario externo de Calidad

#### Escenario: Legales por país
- **Dado** que la persona está en la web de Bélgica
- **Cuando** abre la política de privacidad
- **Entonces** ve la de Bélgica, no la de otro país

## F-09 · Plataforma multimarca y multiidioma

### Requisitos
- R-09.1 El sistema DEBE publicar cada marca en su propia web, con dominio propio, sobre una plataforma común. — **Origen:** US-12
- R-09.2 El sistema DEBE permitir varios idiomas por marca donde haga falta (Aïki: NL principal y FR). — **Origen:** US-12
- R-09.3 El sistema DEBE permitir que el equipo de marketing de cada país gestione el contenido y active campañas sin intervención técnica. — **Origen:** US-12
- R-09.4 El sistema DEBE mantener la misma experiencia en todos los mercados, con las excepciones acordadas (Bélgica: tipografía, colores, textos y sello). — **Origen:** US-12
- R-09.5 El sistema DEBE medir con GA4, GTM y data layer desde el inicio, según las especificaciones del cliente. — **Origen:** US-12
- R-09.6 El sistema DEBE funcionar en móvil primero y ser responsive. — **Origen:** US-01
- R-09.7 El sistema DEBE cumplir un contraste mínimo de 4,5:1 en el texto (WCAG). — **Origen:** US-11

### Escenarios

#### Escenario: Idioma
- **Dado** que la persona está en la web de Aïki en neerlandés
- **Cuando** cambia a francés
- **Entonces** ve la misma página en francés

#### Escenario: Campaña nueva
- **Dado** que el equipo de marketing de Italia tiene una campaña nueva
- **Cuando** la publica en la web de Saikebon
- **Entonces** la campaña aparece en la Home de Saikebon sin intervención técnica
