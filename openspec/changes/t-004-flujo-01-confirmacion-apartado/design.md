## Decisiones
1. **No se recalcula nada.** Se usan `precio`, `abonado`, `pendiente` y `fecha_limite` tal como llegan en `datos`.
2. **Formato:** importes con coma decimal y `€` (`79,90 €`), fecha `dd/mm/aaaa`. Formatear solo para mostrar.
3. **El evento solo se envía una vez, por la app y sin reintentos**, así que el flujo debe responder deprisa y no depender de nada externo salvo el envío.
4. **Apartado liquidado desde el alta** (`datos.estado` = `liquidado`): mensaje distinto, sin hablar de pendiente.
