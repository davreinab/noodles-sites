# Integración continua — plantillas (no activas)

Estas plantillas ejecutan en CI las **mismas verificaciones** que el hook `pre-commit`
(`scripts/token-audit.py`, `scripts/context-audit.py` y `scripts/research-index.py --check`). La skill las deja aquí
**sin activar**: conectar un servicio externo requiere que el equipo lo pida (regla 7 de la
skill). Activar una es mover el archivo a su sitio y hacer commit; no hace falta más.

| Proveedor del remoto | Archivo | Dónde va |
|---|---|---|
| GitHub | [`github-verify.yml`](./github-verify.yml) | `.github/workflows/verify.yml` |
| Bitbucket | [`bitbucket-pipelines.yml`](./bitbucket-pipelines.yml) | `bitbucket-pipelines.yml` en la raíz |
| Otro (GitLab, Azure…) | — | Copia los tres comandos de cualquiera de los dos archivos a su formato |

Cuándo se activa: en cuanto el proyecto tenga remoto (`git remote add …`), el agente
propone mover la plantilla que corresponda al proveedor y espera el OK. No se activa sola.

Qué comprueba el pipeline: exactamente lo mismo que antes de cada commit local. Si algo
pasa en local y falla en CI, la causa es que alguien saltó el hook con `--no-verify`.
