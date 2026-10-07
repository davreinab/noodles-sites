<!-- vigencia
  autoridad: GB Foods (cliente) — Martina Colombo decide contenido y estructura (ver stakeholders.md)
  confirmado: ⬜ TODO — fecha ISO de la última vez que alguien dijo «esto sigue siendo verdad»
  estado: pendiente-de-confirmar
  Las reglas de PROPIEDAD no caducan (un identificador no cambia de naturaleza). Las de
  DECISIÓN sí: caducan a los 6 meses de «confirmado» y la auditoría avisa, no bloquea.
-->

# Project Context — GB Noodles · Microsites

## Qué es
**GB Noodles · Microsites** (Fase 2). Nombre público: ⬜ TODO.

Brand websites de las marcas de noodles de GB Foods en Europa sobre una **plataforma única
(WordPress multisite)**, con dominios independientes por marca, multi-idioma/región y autonomía
para el equipo de marketing, y un sistema de diseño modular por marca.

GB Foods relanza sus noodles en Europa con una **fórmula 100% natural** (de ~30% a 100%
ingredientes naturales, −20% sal, −80% grasas saturadas, sin aditivos, conservantes, aceite de
palma ni glutamato; «100% great taste»).

El proyecto se divide en dos fases:

- **Fase 1 — Landings** (otro repo, `noodles`): HTML estático y temporal, publicado desde el QR
  del pack. Go-live el 14/10/2026 en ES e IT. **Se sustituyen por los microsites.**
- **Fase 2 — Microsites** (este repo): webs de marca completas.

**Sustituye** a las webs locales actuales de cada país (ver tabla de marcas) y a las landings
de la Fase 1.

**Marcas y mercados**

| Marca | País | Web actual | Notas |
|---|---|---|---|
| Yatekomo | ES | yatekomo.es (se sustituye) | Marca canónica de ejemplo en Figma |
| Saikebon | IT | saikebon.it (landing en subcarpeta) | |
| Aïki | BE | aiki.be | Bilingüe **NL (principal) / FR**; visualmente la más distinta |
| Daisuki | FR | daisuki.food | **Sin landing** en Fase 1 (decisión del cliente, 06/10/2026); papel en Fase 2: ⬜ TODO — por confirmar |
| Nueva marca | DE | daisuki.de | Q1 2027, misma estructura |

**Superficies:** web responsive, mobile-first (el público llega sobre todo desde el móvil).

**Técnica:** WordPress multisite (reutilizando la base o el tema de gallinablanca.es, que es
adaptable pero no reutilizable al 100%), responsive y mobile-first, GDPR, estándares de
seguridad de GB Foods y despliegue en su cloud (Azure/CDN). GA4, GTM y data layer desde el
inicio, con las especificaciones del cliente.

Fuente: `noodles/context/traspaso-microsites.md` §2 (2026-10-07).

## Problema actual
- Cada país tiene una web local gestionada por partners: dispersa e inconsistente.
- Muy poco tráfico.
- Lentitud para resolver incidencias.

## Qué debe permitir
1. Publicar las webs de cada marca desde una plataforma única (WordPress multisite), con dominio
   propio por marca.
2. Gestionar varios idiomas y regiones por marca (p. ej. Aïki en NL y FR).
3. Que el equipo de marketing gestione el contenido con autonomía.
4. Activar campañas (sabores nuevos, productos, concursos) en todos los mercados.
5. Publicar contenido de producto (Cups, Bags, Sauces) y de recetas.
6. Explicar la fórmula natural con un FAQ indexable.
7. Medir con GA4, GTM y data layer desde el inicio, según las especificaciones del cliente.

Páginas y módulos: [`user-flow.md § Pantallas`](./user-flow.md).

## Usuarios
Detalle en [`users.md`](./users.md).

| Perfil | Descripción |
|--------|-------------|
| P-01 · El Activista Urbano Consciente | FR/BE. Necesita ver los ingredientes desglosados con transparencia radical desde el primer impacto. |
| P-02 · La Pragmática de Alto Rendimiento | ES/IT. Quiere comer en menos de 5 minutos algo equilibrado y sabroso; busca recetas y dónde comprar. |

## Alcance

### Fase 1 — Landings
Fuera de este repo (`noodles`). Se sustituye por la Fase 2.

### Fase 2 — Microsites
**Entra:** brand websites de Yatekomo (ES), Saikebon (IT), Aïki (BE, NL/FR) y la nueva marca de
Alemania (DE), sobre WordPress multisite, con el sitemap de [`user-flow.md`](./user-flow.md).
Papel de Daisuki (FR): ⬜ TODO — por confirmar.

**No entra:** Mr. Cheng's (SE/FI). Exclusiones del encargo en
[`proposal-agreements.md § Qué entra y qué no`](./proposal-agreements.md).
