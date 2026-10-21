# tienda-api Specification

## Purpose
La API REST de la app de la tienda, que es lo que usa n8n para consultar y actuar. Fuente: `backend/routes/`, `backend/controllers/`, `backend/middleware/` y `docs/guia-de-la-app.md`. Desde n8n la app se llama `http://tienda:8000`, nunca `localhost`.

## Requirements

### Requirement: Autenticación por cabecera
El sistema SHALL exigir la cabecera `X-API-Key` con el valor de `API_KEY` en todas las rutas `/api/...`.

#### Scenario: Falta la clave o es incorrecta
- **WHEN** una petición a `/api/...` no lleva `X-API-Key` o su valor no coincide
- **THEN** la app responde 401 con `detail` = `Falta la cabecera X-API-Key o no es válida`

#### Scenario: La app no tiene clave configurada
- **WHEN** `API_KEY` está vacía en el entorno de la app
- **THEN** todas las peticiones a `/api/...` responden 401

### Requirement: Endpoints disponibles
El sistema SHALL ofrecer los endpoints `GET /api/apartados`, `GET /api/apartados/resumen`, `GET /api/apartados/{id}`, `POST /api/apartados`, `POST /api/apartados/{id}/abonos`, `POST /api/apartados/{id}/vencer`, `GET /api/abonos`, `GET /api/ventas`, `POST /api/ventas`, `GET /api/vales` y `GET /api/excel`.

#### Scenario: Códigos de respuesta de éxito
- **WHEN** se crea un apartado, un abono o una venta
- **THEN** la app responde 201
- **AND** `POST /api/apartados/{id}/vencer` y los `GET` responden 200

### Requirement: Consulta de apartados con filtros
El sistema SHALL listar apartados filtrando por `estado` (`activo`, `liquidado`, `vencido`) y buscando con `q`, ordenados por `fecha_limite`. Sin `pagina` SHALL devolver todos los resultados; el total va en la cabecera `X-Total-Count`.

#### Scenario: Búsqueda por texto
- **WHEN** se consulta `/api/apartados?q=Carmen`
- **THEN** devuelve los apartados cuyo `cliente`, `producto` o `telefono` CONTIENEN el texto, o cuyo id es exactamente ese valor (se admite `#12`)

#### Scenario: La búsqueda es por subcadena
- **WHEN** se busca `q=Jorge M.` y el cliente se llama `Jorge Martín`
- **THEN** no hay coincidencia, porque el texto buscado no es una subcadena del nombre
- **AND** los flujos deben buscar por trozos (nombre, apellido) y no con el texto bruto del correo

#### Scenario: No existe filtro por fecha límite
- **WHEN** un flujo necesita los apartados que vencen en una fecha concreta
- **THEN** debe pedir los `activo` y filtrar `fecha_limite` por su cuenta (por ejemplo en un nodo Code)

### Requirement: Un apartado incluye importes calculados por la app
El sistema SHALL devolver `abonado` y `pendiente` calculados a partir de los abonos, y el detalle (`GET /api/apartados/{id}`) SHALL añadir la lista `abonos` y el `vale` (o `null`).

#### Scenario: Los importes no se recalculan fuera de la app
- **WHEN** un flujo necesita cuánto falta por pagar
- **THEN** usa el campo `pendiente` que devuelve la app y no lo calcula

### Requirement: Consulta de abonos y ventas por fechas
El sistema SHALL devolver abonos y ventas entre `desde` y `hasta` (formato `AAAA-MM-DD`, ambas incluidas); si faltan, no limita ese extremo. Las ventas SHALL admitir `orden` (`asc` o `desc`).

#### Scenario: Total del día por forma de pago
- **WHEN** un flujo pide `abonos` y `ventas` con `desde` = `hasta` = hoy
- **THEN** cada elemento trae su `forma_pago`, de modo que el flujo puede sumar por efectivo, tarjeta y bizum
- **AND** el abono inicial de un apartado nuevo aparece como un abono más

### Requirement: Errores con forma `{"detail": ...}`
El sistema SHALL devolver 404 con `Apartado no encontrado` si el apartado no existe, y 422 con un texto en `detail` cuando una regla del negocio no se cumple.

#### Scenario: Error de validación de datos
- **WHEN** falta un campo obligatorio, un tipo es incorrecto o `precio` no es mayor que 0
- **THEN** la app responde 422, pero `detail` es una LISTA de objetos (formato por defecto de FastAPI), no un texto
- **AND** los flujos no deben asumir que `detail` es siempre un texto

### Requirement: Fecha original solo para migraciones
El sistema SHALL aceptar el campo opcional `fecha` al crear apartados, abonos y ventas para conservar la fecha de datos antiguos; si no se envía, usa hoy.

#### Scenario: Migrar un apartado antiguo
- **WHEN** se crea un apartado con `fecha` = 2026-08-15
- **THEN** el apartado y su abono inicial llevan esa fecha y `fecha_limite` es 2026-11-13
