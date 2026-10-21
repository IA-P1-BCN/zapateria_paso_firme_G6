# Ontología del dominio — Zapatería Paso Firme

Vocabulario único del proyecto. Specs, flujos, mensajes y tickets usan **estos nombres**. Fuente: la app (`backend/models/`) y `openspec/specs/`.

## Entidades

### Cliente
Persona que aparta o compra. En la app no es una tabla propia: sus datos viajan dentro del apartado (`cliente`, `telefono`, `email`).
- El `email` puede faltar: los flujos no deben fallar, avisan a la tienda.
- Para buscarla se usa `q` por subcadena (nombre o apellido), nunca el texto bruto de un correo.

### Producto
Zapatos apartados o vendidos. Tampoco es tabla: `producto` (modelo) y `talla` dentro del apartado.

### Apartado
Reserva de un producto con abono inicial.
| Campo | Significado |
|---|---|
| `id` | Número del apartado |
| `fecha` | Día de alta |
| `precio` | Precio del producto (> 0) |
| `fecha_limite` | `fecha` + 90 días |
| `estado` | `activo`, `liquidado` o `vencido` |
| `abonado` / `pendiente` | Calculados por la app. **Nunca se recalculan fuera.** |

**Ciclo de vida**
```
(alta con abono inicial ≥ 5 €) ──► activo ──► liquidado   (pendiente llega a 0, automático)
                                      │
                                      └────► vencido      (alguien llama a /vencer tras fecha_limite; genera Vale)
```
Excepción: si `abono_inicial` = `precio`, el apartado nace `liquidado`.

### Abono
Pago parcial de un apartado. Tiene `importe`, `fecha` y `forma_pago`. El abono inicial se guarda como un abono más, pero solo emite el evento `apartado.creado`.

### Venta
Venta directa, sin apartado: `concepto`, `importe`, `fecha`, `forma_pago`.

### Vale
Crédito por lo abonado cuando un apartado vence. Código `VALE-{id:05d}` (ejemplo `VALE-00016`). Campos: `importe`, `usado`.

### Forma de pago
`efectivo`, `tarjeta` o `bizum`. Cualquier otra se rechaza.

## Conceptos de los flujos

### Evento
Aviso de la app a n8n: `apartado.creado`, `abono.registrado`, `venta.registrada`, `apartado.vencido`. Llega en `$json.body` con `evento` y `datos`.

### Notificación
Mensaje que sale de n8n hacia una persona (cliente o Marisa). Siempre pasa por el sub-workflow `SUB - Enviar notificación`.

### Pago a distancia
Abono que llega por Bizum o transferencia y se detecta en un correo del banco. De él se extrae `{ordenante, importe, concepto}` (la IA solo extrae).

### Pago dudoso
Pago a distancia que no se puede asignar con seguridad (varios apartados posibles, sin concepto, cliente desconocido). **No se registra nada**: se pregunta a Marisa.

### Cierre diario
Resumen nocturno: ventas y abonos del día, por forma de pago, más el total.

### Aviso de error
Mensaje a Marisa cuando un flujo falla: nombre del flujo, paso y error, sin claves.

## Personas
| Rol | Qué hace |
|---|---|
| **Marisa** | Dueña. Recibe avisos, cierre, informes; decide los casos dudosos |
| **Dependienta** | Da de alta apartados, abonos y ventas en la app |
| **Cliente** | Recibe confirmaciones, recibos, recordatorios y vales |

## Reglas de lenguaje
- Se dice **apartado** (no reserva), **abono** (no pago parcial), **pendiente** (no deuda), **liquidado** (no pagado).
- Estados siempre en minúscula y sin traducir: `activo`, `liquidado`, `vencido`.
