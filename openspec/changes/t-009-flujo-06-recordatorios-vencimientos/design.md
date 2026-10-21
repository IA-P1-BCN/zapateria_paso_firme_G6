## Decisiones
1. **Hora:** 09:00 en `Europe/Madrid`. A confirmar con Marisa.
2. **Se piden los apartados `estado=activo`** y el filtro por `fecha_limite` se hace en un nodo Code (la app no filtra por fecha límite). Fechas comparadas como `aaaa-mm-dd` en Madrid.
3. **Recordatorios:** `fecha_limite` = hoy + 7 días, y = hoy + 1 día. Dos avisos por apartado como máximo, uno por tipo.
4. **Sin avisos duplicados:** se guarda en los datos estáticos del workflow qué (apartado, tipo) ya se avisó. Solo una instancia de n8n debe tener el flujo activo.
5. **El evento `apartado.vencido` no dispara nada en la entrada** (rama NoOp en T-001). Si lo hiciera, el cliente recibiría el aviso dos veces: uno de este flujo y otro de la rama del evento.
6. **Vencimiento:** activo con `fecha_limite` < hoy → `POST /api/apartados/{id}/vencer`. La respuesta trae `{apartado, vale}`; el código y el importe del vale salen de ahí, no se calculan. Si la app responde 422 (ya no estaba activo), se sigue con el siguiente sin error.
7. **Lista a Marisa:** se envía un único mensaje con los apartados vencidos hoy (cliente, producto, talla). Si no hay ninguno, no se envía nada.
