---
type: Client Communications
title: Destilado del correo del cliente
description: Estado, cronología, insights, pendientes y riesgos del proyecto GB Noodles destilados de los correos (Gmail), informes de reunión (Read AI) y Google Chat. Se actualiza en cada revisión de correo.
tags: [context, correo, cliente, gmail, estado, pendientes, riesgos, cronologia]
timestamp: 2026-10-07
---

Lo que dicen los correos del proyecto, destilado. Fuente única para «¿en qué punto
estamos con el cliente?». Personas en [`stakeholders.md`](./stakeholders.md); alcance base en
[`project-context.md`](./project-context.md); lo acordado en [`proposal-agreements.md`](./proposal-agreements.md).
Se actualiza con la [skill `revisar-mails`](../.agents/skills/revisar-mails/SKILL.md).

> **Fiabilidad:** los informes de Read AI son resúmenes automáticos (paráfrasis, con
> errores de nombres); las citas literales entre comillas salen de correos escritos.
> «(ambiguo)» = no confirmado por escrito.

## Índice

1. [Estado actual](#1-estado-actual)
2. [Pendientes](#2-pendientes)
3. [Riesgos y fricciones](#3-riesgos-y-fricciones)
4. [Cronología](#4-cronología)
5. [Historia comercial](#5-historia-comercial)
6. [Insights de cliente y producto](#6-insights-de-cliente-y-producto)
7. [Enlaces](#7-enlaces)
8. [Revisiones](#8-revisiones)

---

## 1. Estado actual

*A 07/10/2026.*

- **Go-live de landings: 14/10/2026, solo España e Italia.** Martina: «SP and ITA need to
  go live on the 14/10 and are the priority.» *(06/10, «Design Status/progress URGENT»)*
- **Quedan 3 landings:** Yatekomo (ES), Saikebon (IT) y Aïki (BE, NL/FR). **Daisuki sale:**
  «At the end Daisuki will not be implemented as landing.» *(06/10)*
- **Estructura de las landings:** cerrada por el cliente el 06/10 y aplicada en el repo. La
  fuente de verdad es [`decisiones.md`](../../noodles/context/decisiones.md) §33 y la landing canónica
  `landing-yatekomo-demo-paises.html`.
- **Aïki:** traducciones NL/FR recibidas el 06/10; **faltan la fuente y los 3D** (los
  pide Julie Van Meerbeeck). No es prioridad del 14/10.
- La **v3 de Yatekomo** (vídeo IA a pantalla completa, 11 módulos) se publicó el 02/10 en
  GitHub Pages para la reunión interna de GB Foods con los países; la cabecera de vídeo
  queda **descartada** para el lanzamiento. Desde noviembre podría entrar el vídeo de la
  campaña de comunicación en cabecera (ambiguo).
- **Sites (Fase 2):** UX de mobile y desktop hecha (Aitor), pero **bloqueada a la espera de
  feedback del cliente**; GB Foods no había validado los wireframes a mediados de
  septiembre. Previsión interna de cierre: noviembre. *(weekly 29/09)*
- Reunión con el cliente prevista el **07/10**.

---

## 2. Pendientes

| Pendiente | Quién | Cuándo |
|---|---|---|
| Sustituir el vídeo provisional del CEO statement por el definitivo y montar el banner de Sayonara | Multiplica | 12–13/10 |
| Vídeo del CEO («Miranda's video») | GB Foods (Martina) | vie 09/10 |
| Imagen del concurso Sayonara + URL de la página de PS21 | GB Foods / PS21 | 09/10 (URL sin fecha) |
| Fuente de titulares que admita acentos: «Can we use a similar one that accepts accents?» | Multiplica propone, cliente valida | antes del 14/10 |
| Fuente de Aïki y 3D de las gamas | Julie Van Meerbeeck | sin fecha |
| Integrar las traducciones NL/FR de Aïki | Multiplica | tras el 14/10 |
| Logos en SVG / alta resolución (el de Aïki se ve pixelado) | GB Foods | sin fecha |
| Dudas del 30/09 sin respuesta explícita: texto del ticker, «We cut the bullshit», copy del formulario largo, sello (ambiguo si se resolvieron en la v3) | GB Foods | — |
| **Dónde se publica en producción** y sesión de infraestructura / entrega del repo con Pablo | Jordi + Enrique | sin fecha (bloquea el 14/10) |
| URL de Bélgica (landing propia o enlace a aiki.be/aiki_products/) | GB Foods | sin fecha |
| QR de los packs: confirmar la capa de redirección propuesta por Jordi | GB Foods | sin confirmar |
| Feedback de la UX de Sites | Sergio García | sin fecha |
| Respuesta técnica para unificar los 3 modelos de concurso (estructura propia / iframe / enlace) | Aitor + Jordi | sin fecha |

---

## 3. Riesgos y fricciones

- **Plazo del 14/10 muy justo:** estructura cerrada el 06/10 y assets clave el 09/10, lo que
  deja dos días laborables (12 y 13/10) para integrarlos.
- **Despliegue sin definir:** no consta en los correos dónde se aloja la landing en producción.
- **Feedback que no se cierra y cambios de criterio:** la cabecera pasó de vídeo integrado
  a versión conservadora, luego a pantalla completa y al final a estática. Enrique: «we need
  to close the feedback as soon as possible» (02/10); «i cannot asure that we can implement
  all as we have not enough time» (01/10).
- **Peticiones de un día para otro:** v3 pedida el 01/10 para el 02/10 a las 9:15.
- **Assets tarde o con poca calidad,** desde el kick off: no hay brand book, la agencia no
  envió imágenes ni pantone, logos pixelados, imágenes sin transparencia y fuentes sin
  licencia. Las imágenes generadas con IA **no valen para producción**.
- **Vídeo IA sin licencia:** Multiplica no tiene suscripción. La postura interna es que, si
  el cliente lo pide, aporte o pague la licencia.
- **Capacidad interna:** Cèlia pasa a un proyecto urgente (LEDs y buscador) y Aitor entra
  en CCMA y FIAT desde finales de octubre.
- **Presupuesto del cliente ajustado:** «dificultades en los mercados para poder absorber el
  coste del proyecto» (13/05). Por eso el proyecto se partió en fases.
- **El cliente ve GitHub Pages en directo:** todo lo que se sube a `main` se publica. Las
  imágenes que no son de la marca no se pueden publicar.

---

## 4. Cronología

| Fecha | Hito |
|---|---|
| 01/04 | Brief de Sergio: «a master website architecture that can be declinated by country». |
| 20/04 | Presentación de la propuesta: WordPress multisite, 5 marcas, 4 meses. |
| 23/04 – 11/05 | Iteraciones de la propuesta: assessment, migración de contenidos, landings pre-launch, recetas, marca alemana, mantenimiento. |
| 13/05 | El cliente no puede absorber el coste y pide dividir en Fase 1 (landing 2026) y Fase 2 (webs Q1 2027). |
| 19/05 | La propuesta original pasa a «pre-2026»; el foco son las landings. |
| 26/06 | Kick off. Landings a principios de septiembre, webs en enero. |
| 30/06 | Carpeta de Drive «Noodles - Landings». |
| 07/07 | Immersion interview con Martina: el objetivo es dar *reassurance* sobre la naturalidad. |
| 15/07 – 05/08 | Status semanales: dirección visual, feedback de Martina, IA de Sites. |
| 03 – 25/08 | Vacaciones de David; trabajo en local, sin subir nada hasta el 26/08. |
| 10 – 13/08 | URLs por país y QR (propuesta de capa de redirección de Jordi). |
| 08/09 | Sergio pide vídeo en el header y página selectora inicial. |
| 16/09 | Status: dos cabeceras de vídeo y tres modelos de concurso. |
| 22/09 | Entra Denis Ventura (desarrollo). |
| 29/09 | Martina envía los textos y la estructura finales (PPT «Landing comments_EU cross comments»). |
| 01 – 02/10 | Petición URGENT de la v3 con vídeo IA; se publica el 02/10. |
| 06/10 | Estructura «03» con cabecera estática, Daisuki fuera y go-live el 14/10 para ES e IT. |

---

## 5. Historia comercial

- **Propuesta inicial (20/04):** 90.000 € más unos 18.000 € de traducciones (Read AI);
  ahorro estimado del 35–40% frente a webs separadas. Requisitos obligatorios: WordPress,
  mobile-first, GDPR, seguridad y cloud de GB Foods, y GA4/GTM/data layer desde el inicio.
  SEO y estrategia de analítica, fuera.
- **Añadidos:** assessment como sección propia, migración de contenidos (100 h), 5 landings
  pre-launch, recetas posteriores al lanzamiento y la nueva marca alemana (Q1 2027).
- **Mantenimiento:** 1.950 €/mes para las 5 webs, revisable y **fuera del presupuesto del
  proyecto** (lo pidió el cliente).
- **Mr. Cheng's:** estaba en el brief y en la propuesta; luego quedó **fuera de alcance**.
- No aparece en los correos ni la aprobación formal ni los importes finales de las fases.
  El presupuesto vigente está en [`contexto-negocio.md`](../../noodles/context/contexto-negocio.md).

---

## 6. Insights de cliente y producto

- **Para qué existe la landing:** «to communicate and reassure consumers about the
  product's naturalness» (Martina, inmersión). Se llega por el QR del pack.
- **El mensaje natural va a alto nivel y alineado con el pack** por restricciones
  regulatorias; el detalle ampliado espera al PR de octubre.
- **Las recetas son el motor de tráfico** de las webs. Producir ese contenido no entra en el
  proyecto, pero la bolsa de enero llevará un QR a recetas.
- **Las webs funcionan como destino de campañas** (recetas, concursos, promos), no como hub diario.
- **Preferencias visuales del cliente:** foto real antes que ilustración, poco texto, claim
  nutricional grande y en verde, más peso para la gama CAP (unos 80% de las ventas) y la
  «ball» del pack en lugar de la hoja verde. «El client volia més força visual» (David, 03/08).
- **Homogeneidad entre mercados,** con Bélgica como excepción (tipografía, colores, textos
  y sello). Los textos base van en inglés y cada país manda su traducción.
- **URLs por país:** ES sustituye yatekomo.es; IT va en una subcarpeta de saikebon.it; BE
  sin confirmar. El QR debería apuntar a una capa de redirección controlada, con analítica
  (propuesta de Jordi, sin confirmar).
- **Suggestion box:** botón hacia el formulario externo de Calidad; si se unifica con el de
  contacto está por decidir.

---

## 7. Enlaces

- Prototipo y demos (público, lo ve el cliente): https://davreinab.github.io/noodles/
- Drive «Noodles - Landings»: https://drive.google.com/drive/folders/1S0CKkCh5p9jTmgFp-cgynDqNhs4tJvB1
- Deck del kick off: https://docs.google.com/presentation/d/1XRcCfMiO5cxs1W1CwFD-o40VkAKZ1AxhE_a7JcR9psg/edit
- Propuesta (versión «Old… pre-2026»): https://docs.google.com/presentation/d/1d6Y0SBaQCunp_D3dSP00_5LhxkzW0n0rWKVGTfEum80/edit
- Referencia de la Fase 1 que dio el cliente: https://www.harmony.info/es-es/
- Status semanal con el cliente: miércoles de 10:00 a 10:30 (Google Meet).
- Assets del 06/10 (traducciones ITA/SP, 3D de la sección 4, sello): enlace de SwissTransfer en el hilo «URGENT»; caduca.
- Figma de IA y wireframes: ver [`contexto-proyecto.md`](../../noodles/context/contexto-proyecto.md#arquitectura-de-información-y-wireframes-figma).

---

## 8. Revisiones

| Fecha | Quién | Buzón | Rango cubierto | Hilos |
|---|---|---|---|---|
| 2026-10-07 | David Reina (con Claude) | dreina@multiplica.com | 01/04/2026 – 06/10/2026 | 93 encontrados, 41 destilados (el resto, avisos de calendario y GitHub) |
