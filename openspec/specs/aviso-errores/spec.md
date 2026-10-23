# aviso-errores Specification

## Purpose
TBD - created by archiving change t-007-flujo-08-error-workflow. Update Purpose after archive.

## Requirements

### Requirement: Aviso cuando un flujo falla
El workflow `08 - Error Workflow` SHALL enviar a Marisa un aviso con el nombre del flujo, el nodo que falló y el mensaje de error cuando cualquier flujo que lo tiene asignado termina con error.

#### Scenario: Fallo de un nodo
- **WHEN** un flujo con `08` asignado falla en un nodo HTTP
- **THEN** Marisa recibe un aviso con el nombre del flujo, el nombre del nodo y el error
- **AND** el aviso incluye el enlace a la ejecución

### Requirement: Sin datos sensibles
El aviso SHALL NOT incluir claves, tokens ni contraseñas.

#### Scenario: Error con cabecera de autenticación
- **WHEN** el texto del error contiene un valor de `X-API-Key`
- **THEN** el aviso muestra `[oculto]` en lugar del valor

### Requirement: Cobertura de todos los flujos
Cada flujo de n8n SHALL tener `08 - Error Workflow` como flujo de error, excepto el propio `08` y `SUB - Enviar notificación`, que `08` usa para avisar (asignárselo crearía un bucle de avisos).

#### Scenario: Flujo nuevo
- **WHEN** se crea un flujo nuevo
- **THEN** su ticket incluye la tarea de asignar `08 - Error Workflow`

#### Scenario: Sub-workflow de envío
- **WHEN** se configura `SUB - Enviar notificación`
- **THEN** no tiene flujo de error asignado
- **AND** un fallo suyo queda registrado en las ejecuciones de n8n
