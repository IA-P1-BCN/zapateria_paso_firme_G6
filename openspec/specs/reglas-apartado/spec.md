# reglas-apartado Specification

## Purpose
Reglas del negocio del sistema de apartados de Paso Firme **tal y como las aplica hoy la app** (`backend/config.py`, `backend/models/apartado.py`, `backend/models/abono.py`). Los flujos de n8n NO las reimplementan: las consultan y respetan sus resultados.

## Requirements

### Requirement: Abono inicial mínimo
El sistema SHALL exigir, al crear un apartado, un abono inicial de al menos 5 €, que no supere el precio, y un precio mayor que 0.

#### Scenario: Abono inicial por debajo del mínimo
- **WHEN** se crea un apartado con `abono_inicial` menor que 5
- **THEN** la app responde 422 con `detail` = `El abono inicial mínimo es de 5 €`
- **AND** no se crea el apartado

#### Scenario: Abono inicial superior al precio
- **WHEN** se crea un apartado con `abono_inicial` mayor que `precio`
- **THEN** la app responde 422 con `detail` = `El abono inicial no puede superar el precio`

### Requirement: Plazo de 90 días
El sistema SHALL calcular `fecha_limite` como la fecha del apartado más 90 días.

#### Scenario: Fecha límite al crear
- **WHEN** se crea un apartado con fecha 2026-10-20
- **THEN** `fecha_limite` es 2027-01-18

### Requirement: Formas de pago válidas
El sistema SHALL aceptar únicamente las formas de pago `efectivo`, `tarjeta` y `bizum` en apartados, abonos y ventas.

#### Scenario: Forma de pago desconocida
- **WHEN** se registra un abono, venta o apartado con `forma_pago` distinta de las tres válidas
- **THEN** la app responde 422 con `detail` = `Forma de pago no válida: {forma_pago}`

### Requirement: Un abono solo se admite en un apartado activo y en plazo
El sistema SHALL rechazar un abono si el apartado no está `activo`, si la fecha del abono es posterior a `fecha_limite`, si el importe no es mayor que 0 o si supera lo pendiente. Las comprobaciones se hacen en este orden y se devuelve la primera que falla.

#### Scenario: Apartado ya liquidado o vencido
- **WHEN** se registra un abono en un apartado con estado `liquidado` o `vencido`
- **THEN** la app responde 422 con `detail` = `El apartado está {estado} y no admite abonos`

#### Scenario: Apartado fuera de plazo que sigue activo
- **WHEN** se registra un abono en un apartado `activo` cuya `fecha_limite` ya pasó
- **THEN** la app responde 422 con `detail` = `El plazo del apartado ha vencido`

#### Scenario: Importe mayor que lo pendiente
- **WHEN** se registra un abono con `importe` mayor que `pendiente`
- **THEN** la app responde 422 con `detail` = `El importe supera lo pendiente ({pendiente} €)`
- **AND** no se registra el abono

#### Scenario: Último día del plazo
- **WHEN** se registra un abono el mismo día de `fecha_limite`
- **THEN** el abono se acepta (solo se rechaza si la fecha es posterior)

### Requirement: Liquidación automática
El sistema SHALL poner el apartado en estado `liquidado` cuando lo pendiente llega a 0 €, sin intervención de nadie.

#### Scenario: El abono cubre lo pendiente
- **WHEN** se registra un abono igual a `pendiente`
- **THEN** el apartado pasa a `liquidado` y `pendiente` es 0

#### Scenario: Abono inicial igual al precio
- **WHEN** se crea un apartado con `abono_inicial` igual a `precio`
- **THEN** el apartado nace con estado `liquidado`

### Requirement: Vencimiento solo por petición
El sistema SHALL marcar un apartado como `vencido` únicamente cuando alguien llama a `POST /api/apartados/{id}/vencer`, y solo si está `activo` y hoy es posterior a `fecha_limite`. Al vencer, SHALL generar un vale por el importe abonado con código `VALE-` seguido del id con 5 cifras.

#### Scenario: Vencer un apartado fuera de plazo
- **WHEN** se llama a `vencer` sobre un apartado `activo` con `fecha_limite` anterior a hoy
- **THEN** el estado pasa a `vencido`
- **AND** se crea un vale con `importe` igual a lo `abonado` y `codigo` `VALE-{id:05d}` (por ejemplo `VALE-00016`)

#### Scenario: Apartado que todavía está en plazo
- **WHEN** se llama a `vencer` sobre un apartado cuya `fecha_limite` es hoy o posterior
- **THEN** la app responde 422 con `detail` = `El apartado no vence hasta el {fecha_limite}`

#### Scenario: Apartado ya cerrado
- **WHEN** se llama a `vencer` sobre un apartado `liquidado` o `vencido`
- **THEN** la app responde 422 con `detail` = `El apartado ya está {estado}`

#### Scenario: El plazo pasa y nadie lo vence
- **WHEN** la `fecha_limite` de un apartado `activo` ya pasó y nadie llama a `vencer`
- **THEN** el apartado sigue `activo` (la app nunca lo vence sola)
