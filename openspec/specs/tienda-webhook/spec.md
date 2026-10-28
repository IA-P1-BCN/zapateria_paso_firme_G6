# tienda-webhook Specification

## Purpose
Los avisos que la app envía a n8n cuando pasa algo en la tienda. Fuente: `backend/services/n8n.py`, `backend/controllers/` y `docs/guia-de-la-app.md`. Es la entrada de los flujos de n8n que reaccionan a eventos.

## Requirements

### Requirement: Envoltorio común del aviso
Cuando `N8N_WEBHOOK_URL` y `WEBHOOK_TOKEN` están configuradas, el sistema SHALL enviar cada aviso como un `POST` JSON a `N8N_WEBHOOK_URL` con la cabecera `X-Webhook-Token` y la forma `{"evento": "<nombre>", "datos": {...}}`, tanto si la acción viene de la pantalla como de la API.

#### Scenario: n8n lee el aviso
- **WHEN** el nodo Webhook de n8n recibe el aviso
- **THEN** el contenido está dentro de `body`, así que se lee `{{ $json.body.evento }}` y `{{ $json.body.datos... }}`

### Requirement: Eventos emitidos
El sistema SHALL emitir exactamente cuatro eventos: `apartado.creado`, `abono.registrado`, `venta.registrada` y `apartado.vencido`.

#### Scenario: Apartado creado
- **WHEN** se crea un apartado
- **THEN** se envía `apartado.creado` con `datos` = el apartado (`id`, `fecha`, `cliente`, `telefono`, `email`, `producto`, `talla`, `precio`, `fecha_limite`, `estado`, `abonado`, `pendiente`)

#### Scenario: Abono registrado
- **WHEN** se registra un abono
- **THEN** se envía `abono.registrado` con `datos` = el apartado ya actualizado MÁS `importe` (lo abonado ahora)
- **AND** `datos.estado` es `activo` si aún queda pendiente, o `liquidado` si `pendiente` es 0

#### Scenario: El abono inicial no genera `abono.registrado`
- **WHEN** se crea un apartado (con su abono inicial)
- **THEN** solo se envía `apartado.creado`; no se envía `abono.registrado`

#### Scenario: Venta registrada
- **WHEN** se registra una venta directa
- **THEN** se envía `venta.registrada` con `datos` = `{id, fecha, concepto, importe, forma_pago}`

#### Scenario: Apartado vencido
- **WHEN** se vence un apartado
- **THEN** se envía `apartado.vencido` con `datos` = `{"apartado": {...}, "vale": {id, codigo, apartado_id, fecha, importe, usado}}`

### Requirement: El estado viaja dentro de los datos
El sistema SHALL incluir en `datos.estado` el estado del apartado DESPUÉS de la acción, de modo que un IF o Switch pueda decidir sin consultar nada más.

#### Scenario: Apartado nacido liquidado
- **WHEN** se crea un apartado con abono inicial igual al precio
- **THEN** `apartado.creado` llega con `estado` = `liquidado` y `pendiente` = 0

### Requirement: Envío único, sin reintentos
El sistema SHALL enviar el aviso una sola vez, después de responder a quien hizo la acción, con un tiempo máximo de espera de 5 segundos, y SHALL NOT reintentar ni comprobar si n8n lo procesó.

#### Scenario: n8n está apagado o el flujo sin publicar
- **WHEN** n8n no responde o contesta con error (por ejemplo 404 por flujo sin publicar)
- **THEN** el aviso se pierde y la app solo escribe `No se pudo avisar a n8n` en su log
- **AND** la acción en la tienda (crear apartado, abonar...) se completa igualmente

#### Scenario: Los flujos programados no dependen del aviso
- **WHEN** un flujo programado (cierre diario, vencimientos, informe mensual) necesita datos
- **THEN** los pide a la API y no espera haber recibido un evento

### Requirement: Dirección del webhook
El sistema SHALL enviar el aviso a la URL configurada en `N8N_WEBHOOK_URL` únicamente cuando `WEBHOOK_TOKEN` esté configurado. Si `N8N_WEBHOOK_URL` está vacía, no envía nada; si falta `WEBHOOK_TOKEN`, registra una advertencia y omite el aviso.

#### Scenario: Flujo no publicado
- **WHEN** el flujo con el Webhook no está publicado
- **THEN** la URL de producción responde 404 y no se ejecuta nada
- **AND** para ver avisos mientras se construye el flujo se usa temporalmente `/webhook-test/tienda`
