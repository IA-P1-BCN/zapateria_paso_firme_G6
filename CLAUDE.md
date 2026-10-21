@AGENTS.md

# Notas solo para Claude Code

## Commands
```bash
docker compose up -d            # levanta la tienda (8000) y n8n (5678)
docker compose logs -f n8n      # ver logs de n8n
docker compose down             # parar (los datos se conservan en volúmenes)
openspec validate --specs       # validar las specs de base
openspec validate --changes     # validar los changes en curso
openspec list                   # changes activos
```
Comandos de OpenSpec en Claude: `/opsx:propose`, `/opsx:explore`, `/opsx:apply`, `/opsx:archive`.
Docker Desktop debe estar abierto. n8n NO se instala en el Mac: lo ejecuta Docker.

## Modo de aprendizaje
Charlotte está aprendiendo: explica el porqué de cada decisión. Pregunta el modo (mentor / implementer) al empezar la sesión; gana lo que diga aquí si hay conflicto con las reglas globales.

## Recordatorios
- Abre Claude desde la raíz `paso-firme` (para cargar `.mcp.json`, el plugin n8n y `/opsx:*`).
- `.env` no se sube nunca; `.env.example` sin valores reales (el repo es público).
