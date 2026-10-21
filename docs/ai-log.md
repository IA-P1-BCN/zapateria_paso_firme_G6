# Bitácora de uso de IA

Se anota cada uso relevante de un agente: qué herramienta y modelo, qué se pidió, qué salió, qué se corrigió a mano y qué se aprendió. **También cuando la IA se equivoca.** Sin claves ni datos personales reales.

## Plantilla
```
### AAAA-MM-DD · T-XXX · <tema>
- Herramienta / modelo:
- Qué se pidió:
- Qué salió:
- Qué se corrigió a mano:
- Aprendizaje:
```

## Entradas

### 2026-10-21 · T-000 · Preparación del repo y herramientas
- Herramienta / modelo: Claude Code (Sonnet 5.5).
- Qué se pidió: leer el briefing y la app, crear las 16 historias de usuario en el Kanban, instalar OpenSpec, n8n-mcp y n8n-skills.
- Qué salió: 16 issues con criterios de aceptación como checklist; OpenSpec configurado en español; tres specs de base (`tienda-api`, `tienda-webhook`, `reglas-apartado`) escritas leyendo el código de la app.
- Qué se corrigió a mano: se eliminó la etiqueta `historia-de-usuario` y todas las HU se movieron a Backlog; se decidió dejar `.claude/` y `.mcp.json` en el repo para compartirlos.
- Aprendizaje: la guía de la app simplifica un detalle (los errores de validación devuelven `detail` como lista, no como texto); hay que fiarse del código y no de la guía. La búsqueda `q` es por subcadena, así que el flujo 3 debe buscar por trozos.
