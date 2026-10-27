# T-018 · Entrada automática de solicitudes de apartado

**Historia:** HU-13 · **Responsable:** sin asignar · **Tamaño:** M · **Fecha límite:** sin fecha (extra: si hay tiempo)
**Depende de:** T-001, T-002

## Por qué
Algunos clientes piden un apartado por un formulario o por Telegram. Marisa tiene que teclearlo a mano en la app.

## Qué cambia
- Formulario o mensaje que crea un apartado en la app tras validar los datos.

## Fuera de alcance
- Cobrar el abono inicial.
- Aprobar solicitudes sin revisar.

## Impacto
Escribe en la app (`POST /api/apartados`). Extra (nivel Avanzado/Experto): se construye solo si el nivel Esencial y Medio están cerrados y queda tiempo.
