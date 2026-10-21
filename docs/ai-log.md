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

### 2026-10-21 · T-000 · Specs de base leyendo el código de la app
- Herramienta / modelo: Claude Code (Sonnet 5.5).
- Qué se pidió: describir cómo funciona hoy la app (API, webhook y reglas de apartado) como specs verificables.
- Qué salió: `tienda-api`, `tienda-webhook` y `reglas-apartado`, validadas con `openspec validate --specs`.
- Qué se corrigió a mano: pendiente de revisión por la pareja contra la app.
- Aprendizaje: la guía de la app simplifica un detalle (los errores de validación devuelven `detail` como lista, no como texto); hay que fiarse del código y no de la guía. La búsqueda `q` es por subcadena y no ignora acentos, así que el flujo 3 debe buscar por trozos. Al vencer, la app devuelve `{apartado, vale}`.

### 2026-10-21 · T-000 · Reglas para los agentes y herramientas
- Herramienta / modelo: Claude Code (Sonnet 5.5).
- Qué se pidió: `AGENTS.md` y `CLAUDE.md` con prohibiciones y convenciones de n8n, e instalar OpenSpec, `n8n-mcp` y n8n-skills.
- Qué salió: ocho prohibiciones (sin credenciales en JSON, no recalcular importes, la IA no decide dinero…), forma de trabajo con OpenSpec y archivado obligatorio de cada change.
- Qué se corrigió a mano: se decidió que documentos y tickets van en español y commits y PR en inglés, con el ID del ticket como scope.
- Aprendizaje: Claude Code no lee `AGENTS.md` por sí solo; `CLAUDE.md` lo importa con `@AGENTS.md`.

### 2026-10-21 · T-000 · Creación masiva de tickets: la IA se equivocó
- Herramienta / modelo: Claude Code (Sonnet 5.5).
- Qué se pidió: 22 tickets de GitHub, uno por change, como sub-issue de su historia, con etiquetas, tamaño y fecha.
- Qué salió: los 22 tickets (#17…#39), pero el script tenía fallos: `declare -A` (no existe en el bash de macOS), un tipo `Date` que la API rechaza, y algunos tickets quedaron sin estado ni tamaño porque el proyecto ya los había añadido solo.
- Qué se corrigió a mano: se detectó al comprobar el tablero y se repasó ticket por ticket.
- Aprendizaje: comprobar siempre el resultado en GitHub después de una operación masiva; crear de uno en uno con pausa evita bloqueos.
