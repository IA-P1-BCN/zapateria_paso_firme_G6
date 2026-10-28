# 👟 Zapatería Paso Firme · Automatizaciones con n8n (G6)

**[Español](#-español)** · **[English](#-english)**

---

## 🇪🇸 Español

### Qué es

Paso Firme es una zapatería de barrio cuyo servicio estrella son los **apartados**: el cliente reserva unos zapatos con un abono inicial (mínimo 5 €) y los paga poco a poco en un plazo de 90 días. La tienda ya tiene una app (FastAPI + SQLite) donde se registran apartados, abonos y ventas.

Este repositorio **no modifica la app**: construye con **n8n** todo lo que pasa a su alrededor (avisar a los clientes, registrar los pagos que llegan por Bizum o transferencia, cerrar la caja, recordar vencimientos, informar a Marisa, la dueña). El enunciado completo del proyecto está en [ENUNCIADO.md](ENUNCIADO.md).

### Flujos

| # | Flujo | Disparador | Ticket | Responsable |
|---|---|---|---|---|
| — | Base del webhook y credenciales | Webhook `/webhook/tienda` | T-001 | Charlotte |
| — | `SUB - Enviar notificación` | Llamado por otros flujos | T-002 | Charlotte |
| — | `SUB - Buscar apartado` | Llamado por otros flujos | T-003 | Anna |
| 1 | Confirmación de apartado | Evento `apartado.creado` | T-004 | Leandro |
| 2 | Recibo de abono | Evento `abono.registrado` | T-005 | Leandro |
| 5 | Cierre diario | Programado, 22:00 | T-006 | Leandro |
| 8 | Error Workflow | Error en cualquier flujo | T-007 | Charlotte |
| 3 | Abonos a distancia (Bizum y transferencia) | Correo del banco (IMAP) | T-008 | Anna |
| 6 | Recordatorios y vencimientos | Programado, 09:00 | T-009 | Charlotte |
| 4 | Venta grande | Evento `venta.registrada` | T-010 | Leandro |
| 7 | Informe mensual | Programado, día 1 a las 08:00 | T-011 | Charlotte |
| — | Migración del Excel de Marisa | Manual, una sola vez | T-012 | Anna |
| — | Comparativa de dos modelos gratuitos | — | T-013 | Anna y Charlotte |
| — | Asistente Marisa (Telegram con agente de IA) | Mensaje al bot de Marisa | T-017 | Charlotte |

El estado de cada ticket está en el [tablero Kanban](https://github.com/orgs/IA-P1-BCN/projects/41). Alcance: niveles **Esencial** y **Medio** del enunciado.

### Cómo funciona

| Pieza | Desde el navegador | Desde dentro de n8n |
|---|---|---|
| App de la tienda | http://localhost:8000 (API en `/docs`) | `http://tienda:8000` |
| n8n | http://localhost:5678 | — |
| Webhook de eventos | — | la app avisa a `http://n8n:5678/webhook/tienda` |

- La app avisa a n8n por **un único webhook**; un nodo **Switch** reparte por `evento` (`apartado.creado`, `abono.registrado`, `venta.registrada`…).
- n8n consulta y actúa sobre la app por su **API REST** con la cabecera `X-API-Key`.
- Los importes (`abonado`, `pendiente`, `precio`) los calcula siempre la app; los flujos no los recalculan.
- En el flujo 3 la IA **solo extrae** ordenante, importe y concepto del correo. Registrar, dudar o rechazar lo deciden nodos deterministas. Si algo es dudoso, no se registra nada y se pregunta a Marisa.

### 🚀 Cómo empezar

Necesitas [Git](https://git-scm.com/) y [Docker Desktop](https://www.docker.com/products/docker-desktop/) abiertos. Cada persona del equipo tiene **su propia instancia de n8n**.

```bash
git clone https://github.com/IA-P1-BCN/zapateria_paso_firme_G6.git paso-firme
cd paso-firme
cp .env.example .env        # y rellena los valores (ver tabla de variables)
docker compose up -d        # tienda en :8000, n8n en :5678
```

1. Abre http://localhost:5678 y crea tu cuenta local de n8n.
2. Crea las credenciales de la tabla siguiente, **con estos nombres exactos**.
3. Importa los flujos de [`workflows/`](workflows/) (menú del flujo → *Import from file*).
4. En los flujos que llaman a un sub-workflow (`SUB - …`), vuelve a elegirlo en el nodo *Execute Workflow*: su identificador interno cambia en cada instancia.
5. En cada flujo (salvo `08 - Error Workflow` y `SUB - Enviar notificación`), abre *Settings → Error workflow* y elige `08 - Error Workflow`: su identificador también cambia en cada instancia.

Para pararlo: `docker compose down`. Para borrar también los datos: `docker compose down -v`.

### Variables y credenciales (sin valores)

| Variable del `.env` | Para qué |
|---|---|
| `API_KEY` | Clave que la app exige en la cabecera `X-API-Key` |
| `N8N_WEBHOOK_URL` | Dónde avisa la app a n8n (valor de `.env.example`) |
| `N8N_EDITOR_BASE_URL` | URL pública/base de n8n usada por los flujos para construir enlaces (p. ej. confirmar solicitud) |
| `SEED` | `1` carga datos de ejemplo al arrancar; `0` arranca vacía (migración) |
| `EMAIL_TIENDA` | Buzón de la tienda: recibe los avisos a Marisa y es también el remitente de los correos |
| `UMBRAL_VENTA_GRANDE` | Importe en € a partir del cual una venta es "grande" (por defecto `80`) |
| `WEBHOOK_TOKEN` | Token que la app envía en `X-Webhook-Token` al avisar a n8n (vacío = no envía avisos) |
| `TELEGRAM_CHAT_ID_MARISA` | Identificador del chat de Telegram de Marisa: el único que atiende `Asistente Marisa` (T-017) |

Dentro de un flujo se leen con `{{ $env.NOMBRE }}`.

| Credencial de n8n | Tipo | Qué lleva |
|---|---|---|
| `Tienda API` | Header Auth | Cabecera `X-API-Key` con el valor de `API_KEY` |
| `Correo salida` | SMTP | Cuenta de correo de la tienda |
| `Correo entrada` | IMAP | La misma cuenta, para leer los avisos del banco |
| `Modelo IA` | Groq | Clave personal de https://console.groq.com |
| `Telegram Marisa` | Telegram | Token del bot de Marisa (se crea con BotFather; solo en la credencial, nunca en el repo) |
| `Telegram Clientes` | Telegram | Token del bot de clientes (se crea con BotFather; solo en la credencial, nunca en el repositorio) |
| `Acceso Marisa` | Basic Auth | Usuario y contraseña del formulario de confirmación de solicitudes (T-018) |

Los flujos solo guardan el **nombre** de la credencial. El `.env` y los valores de las credenciales no se suben nunca al repositorio.

### Protección de datos y seguridad del webhook (T-020)

**Autenticación del webhook:** la tienda envía los eventos a n8n mediante `POST` a `N8N_WEBHOOK_URL`, con la cabecera `X-Webhook-Token`. El token se configura mediante `WEBHOOK_TOKEN` en `.env`; no debe incluirse en la URL, en los JSON exportados ni en el repositorio. n8n comprueba la cabecera antes de aceptar el evento. Las peticiones sin token válido deben rechazarse. Si falta `WEBHOOK_TOKEN`, la aplicación omite el aviso y registra una advertencia; la operación de la tienda continúa.

**Datos que salen a servicios externos:**

| Servicio | Datos enviados | Finalidad |
|---|---|---|
| n8n (webhook local) | Tipo de evento y datos asociados al evento generado por la app; pueden incluir identificadores, nombres, conceptos e importes según el evento | Automatizar avisos y procesos de la tienda |
| Proveedor de IA Groq (flujo 03) | Asunto y cuerpo del correo bancario que supera el filtro, para extraer ordenante, importe y concepto | Ayudar a identificar pagos a distancia |
| Servicio de correo SMTP | Dirección del destinatario, asunto y cuerpo del mensaje | Enviar recibos y avisos |
| Buzón bancario IMAP | Acceso a los correos recibidos por la cuenta configurada | Detectar notificaciones de Bizum y transferencias |

Los datos que llegan a n8n pueden contener datos personales. El flujo 03 transmite a Groq el asunto y el cuerpo del correo que procesa; por tanto, en un entorno real podrían salir datos personales a ese proveedor. Usar datos ficticios en pruebas y limitar la información transmitida a la necesaria. Revisar las condiciones, la configuración de privacidad y la base jurídica aplicable antes de procesar datos reales. Esta documentación no sustituye una evaluación legal ni acredita por sí sola la existencia de consentimiento.

**Consentimiento e información:** informar a los clientes, antes de tratar sus datos, sobre las finalidades, los destinatarios o categorías de destinatarios, la conservación y sus derechos, según corresponda. No asumir que el uso de la app implica consentimiento válido para cualquier tratamiento o envío a terceros.

**Logs y credenciales:** no registrar tokens, claves, contraseñas, cuerpos completos de correos ni datos personales en mensajes de error. Guardar `.env` fuera del control de versiones y no exportar credenciales reales en los workflows. Los archivos de ejemplo deben usar datos ficticios. El token del webhook autentica la petición, pero no cifra el tráfico; para despliegues fuera de una red local controlada, utilizar HTTPS y controles de acceso adecuados.
### Contratos de los sub-workflows

#### `SUB - Buscar apartado` (T-003)

Busca el apartado de una persona a partir de un identificador o de un nombre escrito de cualquier manera (`JORGE M.`, `LUCIA GOMEZ`). Solo lee de la API y solo devuelve apartados en estado `activo`.

**Entrada** (*Execute Workflow*):

| Campo | Tipo | Ejemplo | Nota |
|---|---|---|---|
| `id` | número o texto | `12`, `#12` | Si es válido, se busca por id y se ignora `texto` |
| `texto` | texto | `JORGE M. apartado 2 bota` | Normalmente ordenante + concepto del pago |

**Salida:**

```json
{
  "resultado": "unico | varios | ninguno",
  "candidatos": [
    { "id": 2, "cliente": "Jorge Martín", "producto": "Bota alta mujer", "talla": "36",
      "precio": 119, "abonado": 40, "pendiente": 79, "fecha_limite": "2027-01-15", "estado": "activo" }
  ]
}
```

- El texto se compara sin mayúsculas, acentos ni puntuación, por trozos de 3 letras o más (`de`, `del`, `la`… se ignoran). Gana el apartado que coincide con más trozos; si empatan varios, `varios`.
- Un número en el texto (`#2`, `apartado 2`) solo se usa si ese apartado también coincide con algún trozo del nombre.
- Un id inexistente (404) o un apartado no activo devuelve `ninguno`. Cualquier otro error de la app (401, 500) **lanza error**, para no confundirlo con "no encontrado".
- Para que otro flujo lo llame, el sub-workflow tiene que estar **publicado** en esa instancia de n8n.

#### `SUB - Enviar notificación` (T-002)

Envía un correo de texto a una clienta o a la tienda (Marisa). Lo usan los flujos que avisan por correo. Usa la credencial `Correo salida` y la variable `EMAIL_TIENDA`. **Nunca lanza error al flujo que lo llama**: el resultado dice si se envió.

**Entrada** (*Execute Workflow*):

| Campo | Tipo | Ejemplo | Nota |
|---|---|---|---|
| `destinatario` | texto | `cliente`, `tienda` | `tienda` envía a `EMAIL_TIENDA` |
| `email` | texto | `carmen@example.com` | Solo para `cliente`; puede venir vacío o no venir |
| `asunto` | texto | `Tu apartado en Paso Firme` | |
| `mensaje` | texto | `Hola Carmen, hemos registrado tu apartado.` | Texto plano |
| `contexto` | texto | `Apartado 25 - Carmen Ruiz` | Opcional; identifica el apartado en el aviso a la tienda |

**Salida:**

```json
{ "enviado": true, "motivo": "" }
```

| `enviado` | `motivo` | Cuándo |
|---|---|---|
| `true` | `""` | Correo enviado a la clienta o a la tienda |
| `false` | `sin_email` | `cliente` sin `email`: no se envía a la clienta y se avisa a la tienda con el `contexto` |
| `false` | `error_envio` | Falló el servidor de correo, o `destinatario` no es `cliente` ni `tienda` |

- Quien lo llama no tiene que capturar errores: mira `enviado` y, si es `false`, `motivo`.
- Para que otro flujo lo llame, el sub-workflow tiene que estar **publicado** en esa instancia de n8n.

### Migración del Excel (T-012, una sola vez)

El flujo `Migración Excel` pasa a la app los apartados, abonos y ventas de las hojas de Marisa ([`data/excel_actual_apartados.csv`](data/excel_actual_apartados.csv) y [`data/excel_actual_ventas.csv`](data/excel_actual_ventas.csv)) y le envía por correo un informe con lo que no se ha cargado y por qué.

**Antes de ejecutarla:**

1. La tienda tiene que estar **vacía** y con el **webhook apagado**. Si no, cada apartado y cada venta antiguos dispararían sus avisos: confirmaciones a los clientes, aviso de venta grande… En el `.env` pon `SEED=0` y deja `N8N_WEBHOOK_URL=` vacío, y después:

   ```bash
   docker compose rm -sf tienda
   docker volume ls                          # busca el volumen que acaba en _tienda_data
   docker volume rm <carpeta>_tienda_data    # borra SOLO los datos de la tienda, no los de n8n
   docker compose up -d tienda
   ```

2. Copia los CSV a n8n, que no ve la carpeta `data/` del repositorio:

   ```bash
   docker compose exec n8n mkdir -p /home/node/.n8n-files/migracion
   docker compose cp data/excel_actual_apartados.csv n8n:/home/node/.n8n-files/migracion/
   docker compose cp data/excel_actual_ventas.csv n8n:/home/node/.n8n-files/migracion/
   ```

3. El informe se envía con `SUB - Enviar notificación`: impórtalo, publícalo y elígelo en el nodo *Enviar informe a Marisa* (su identificador cambia en cada instancia). Comprueba también que existen las credenciales `Tienda API` y `Correo salida` y que `EMAIL_TIENDA` tiene valor: es la dirección que recibe el informe.

**Ejecutarla:** abre el flujo en n8n y pulsa *Execute workflow*. Si se vuelve a ejecutar no duplica nada, porque antes de crear comprueba qué hay ya en la app.

**Al terminar:** vuelve a poner en el `.env` el `N8N_WEBHOOK_URL` de `.env.example` y reinicia la tienda (`docker compose up -d tienda`) para que los avisos vuelvan a llegar a n8n.

**Qué hace con los datos:**

| Caso | Qué pasa |
|---|---|
| Fechas `7/9/26`, importes `15€`, nombres en minúscula | Se normalizan (`2026-09-07`, `15`, `Carmen Ruiz`) |
| Varias filas del mismo cliente, modelo y talla | La primera es el apartado y las siguientes, sus abonos, en orden de fecha |
| Abono inicial menor de 5 € (Lucía Gómez) | No se carga ni el apartado ni sus abonos; va al informe |
| Ventas que son abonos (`abono inicial apartado`, `Abono Ana Torres mocasin`, `(apartado)`) | No se cargan como venta; dan la forma de pago de ese abono |
| Abonos sin forma de pago conocida | Se cargan como `efectivo` y el informe lo señala como suposición |
| Fila `TOTAL SEPTIEMBRE (a mano)` | Se ignora |
| Al final | Compara lo pendiente de cada apartado con la columna `resta` y los totales con el Excel |

Con los datos de ejemplo carga 7 apartados, 3 abonos posteriores y 6 ventas: 170,00 € en abonos y 213,85 € en ventas, igual que el Excel.

### Flujo 03 · Abonos por Bizum y transferencia (T-008)

El flujo `03 - Abonos a distancia` lee los avisos del banco que llegan al buzón de la tienda, saca con IA quién paga, cuánto y con qué concepto, y registra el abono en la app solo cuando está claro. Si no lo está, no registra nada y avisa a Marisa.

**Cómo decide:**

1. **Filtro sin IA:** solo sigue un correo con las líneas `Importe` y `Ordenante` del banco. La publicidad, los avisos de los propios flujos y los correos devueltos se ignoran sin llamar al modelo.
2. **Extracción con IA** (credencial `Modelo IA`, modelo `qwen/qwen3.8-27b` de Groq, elegido en T-013): el modelo solo copia `ordenante`, `importe` y `concepto`. Recibe únicamente el asunto y el texto del correo; los datos de prueba son ficticios.
3. **Validación en código:** el importe pasa a número (`10,00 EUR` → `10`); si no es positivo, el pago es dudoso.
4. **Búsqueda** con `SUB - Buscar apartado` (ordenante + concepto).
5. **Reglas (sin IA):** se registra solo si hay un único apartado activo, el pago trae concepto, está en plazo, no supera lo pendiente y ese apartado no tiene ya hoy un abono del mismo importe (posible duplicado). Si no, se pregunta a Marisa o se le avisa del rechazo, con el motivo y los apartados posibles.
6. **Registro:** `POST /api/apartados/{id}/abonos` con `forma_pago: bizum`. Las transferencias también se registran como `bizum` (la app no tiene `transferencia`) y Marisa recibe un aviso de que se ha hecho así. La app emite `abono.registrado` y el flujo 02 envía el recibo al cliente.

**Para ponerlo en marcha:**

- Credenciales `Correo entrada`, `Tienda API` y `Modelo IA`. Tras importarlo, elige `SUB - Buscar apartado` y `SUB - Enviar notificación` en sus nodos *Execute Workflow* y `08 - Error Workflow` en *Settings → Error workflow*.
- **Publícalo en una sola instancia de n8n.** Al publicarlo por primera vez solo procesa los correos que llegan desde ese momento.
- Para probar sin el buzón: copia los correos a n8n (`docker compose exec n8n mkdir -p /home/node/.n8n-files/correos` y `docker compose cp data/correos/. n8n:/home/node/.n8n-files/correos/`) y pulsa *Execute workflow* desde el disparador *Probar con los correos de ejemplo*.

**Resultados reales con los 9 correos de `data/correos/`** (datos de ejemplo de la app, prueba con el buzón real del 25/10/2026):

| Correo | Datos extraídos | Resultado |
|---|---|---|
| 01 Bizum Carmen Ruiz | `CARMEN RUIZ GARCIA` · 10 € · `zuecos` | Registrado en #1 (faltaban 19,50 €, ahora 9,50 €) |
| 02 Bizum `JORGE M.` | `JORGE M.` · 20 € · `apartado 2 bota` | Registrado en #2 (79 € → 59 €) |
| 03 Transferencia Lucía Gómez | `LUCIA GOMEZ PEREZ` · 12 € · `Liquidar mocasines` | Registrado en #3, que queda **liquidado**; aviso a Marisa de que consta como bizum |
| 04 Bizum `LAURA O.` | `LAURA O.` · 15 € · `deportivas` | No registrado: supera lo pendiente (10 €); aviso a Marisa |
| 05 Bizum `ROMERO D` | `ROMERO D` · 10 € · *(vacío)* | No registrado: sin concepto; aviso a Marisa con #11 como posible |
| 06 Bizum Paula Ramos | `PAULA RAMOS LEON` · 20 € · `zapatillas running…` | No registrado: fuera de plazo; aviso a Marisa |
| 07 Transferencia Antonio Fernández | `ANTONIO FERNANDEZ SOTO` · 25 € · `botas` | No registrado: ningún apartado coincide; aviso a Marisa |
| 08 Publicidad del banco | — (no llega al modelo) | Ignorado |
| 09 Bizum Silvia Cortés | `SILVIA CORTES` · 5 € · `abono sandalias` | Registrado en #24 |

Al volver a pasar los mismos 9 correos no se registra ningún abono: los que ya estaban registrados se avisan como posible pago duplicado o como fuera de lo pendiente.

### Comparativa de modelos de IA (T-013)

Para el flujo 03 se compararon dos modelos gratuitos de Groq en la misma tarea: sacar `ordenante`, `importe` y `concepto` de los avisos del banco.

**Cómo se hizo:**

- **Misma entrada para los dos:** el prompt de T-008 y los 9 correos de `data/correos/`, también la publicidad, para ver si el modelo se inventa datos. Temperatura 0.
- **Tres vueltas:** 27 respuestas por modelo.
- **Acierto:** cada campo se compara con lo que dice el correo; el importe, ya convertido a número.
- **JSON válido:** la respuesta entera es un objeto JSON, sin texto ni bloques de código alrededor.
- **Tiempo:** el que devuelve Groq para cada petición (`total_time`).
- **Datos enviados:** solo las instrucciones y el asunto y el texto del correo, unos 300-350 tokens por petición. No se envían remitente, cabeceras ni ningún dato de la tienda, y los correos de prueba son ficticios.

  <details><summary>Instrucciones exactas (mensaje de sistema, el mismo que usa el flujo 03)</summary>

  ```text
  Eres un extractor de datos. Lees un aviso de un banco sobre un pago recibido (Bizum o transferencia) y devuelves SOLO un objeto JSON, sin explicaciones ni bloques de código, con estos tres campos de texto:
  - "ordenante": lo que aparece en la línea "Ordenante", copiado tal cual.
  - "importe": lo que aparece en la línea "Importe", copiado tal cual (por ejemplo "10,00 EUR").
  - "concepto": lo que aparece en la línea "Concepto", copiado tal cual. Si esa línea está vacía o no existe, devuelve "".
  Reglas: no inventes ni completes datos, no corrijas nombres, no uses el texto de otras líneas para rellenar un campo. Si un dato no aparece, devuelve "".
  Ejemplo de respuesta: {"ordenante": "ANA PEREZ", "importe": "15,00 EUR", "concepto": "botas"}
  ```

  </details>
  <details><summary>Mensaje exacto del usuario, ejemplo con el correo 01</summary>

  ```text
  Asunto: Has recibido un Bizum de 10,00 €

  Hola, ZAPATERIA PASO FIRME:

  Has recibido un Bizum.

  Importe: 10,00 EUR
  Ordenante: CARMEN RUIZ GARCIA
  Concepto: zuecos

  El importe ya está disponible en tu cuenta terminada en 4821.

  Banco Ejemplo
  ```

  </details>

- **Para repetirla:** importa `workflows/Comparativa de modelos.json`, copia los correos a n8n (como en el flujo 03) y pulsa *Execute workflow*. Usa la credencial `Modelo IA`.

| Métrica | `openai/gpt-oss-20b` | `qwen/qwen3.8-27b` |
|---|---|---|
| Campos correctos | 81/81 | 81/81 |
| Correos con los tres campos bien | 27/27 | 27/27 |
| JSON válido | 27/27 | 27/27 |
| Publicidad sin datos inventados | 3/3 | 3/3 |
| Misma respuesta en las tres vueltas | 9/9 correos | 9/9 correos |
| Tiempo de respuesta: media / mediana / máximo | 0,175 / 0,153 / 0,337 s | 0,098 / 0,096 / 0,206 s |
| Tokens de respuesta (media) | 134 | 32 |

**Modelo elegido: `qwen/qwen3.8-27b`.** Los dos aciertan todo, así que la diferencia está en el coste. Qwen tarda casi la mitad y gasta unas 4 veces menos tokens de respuesta (`gpt-oss` razona antes de contestar), lo que deja más margen en los límites de la capa gratuita de Groq y menos riesgo de que la respuesta se corte. La muestra es pequeña (9 correos) y los dos lo hacen bien; no es una diferencia de calidad. El flujo 03 usa ya este modelo y da los mismos resultados con los 9 correos.

### Entrada del CSV del datáfono (T-019)

El flujo `Entrada CSV del datáfono` lee el CSV de cobros con tarjeta que exporta el datáfono, lo cuadra con las ventas y los abonos pagados con tarjeta que ya hay en la app y registra como venta con tarjeta los cobros que faltan. Le manda a Marisa un informe con lo que ha cargado, lo que ya estaba y lo que tiene que revisar ella.

**Cómo decide:**

- **Cobros válidos:** solo cuentan las líneas `VENTA` y `AUTORIZADA`. Las denegadas, las anuladas, la línea de totales y las repetidas (mismo número de operación) se ignoran.
- **Para que Marisa las revise, sin cargar nada:** las devoluciones (la app no tiene devoluciones) y las líneas con fecha, importe o número de operación ilegibles.
- **¿Ya está en la app?** Un cobro ya está si cuadra con una venta **o un abono** pagados con tarjeta el mismo día y por el mismo importe; cada registro de la app solo cuadra con un cobro. Hay que mirar también los abonos: un abono pagado con tarjeta pasa por el datáfono y no es una venta nueva.
- **Lo que falta** se carga como venta con tarjeta, con la fecha del cobro y el concepto `Cobro con tarjeta (datáfono, op. 000102)`. Por ese número de operación, si se vuelve a ejecutar no se duplica nada.

**Para ponerlo en marcha:**

- Copia el CSV a n8n: `docker compose exec n8n mkdir -p /home/node/.n8n-files/datafono` y `docker compose cp <fichero>.csv n8n:/home/node/.n8n-files/datafono/`. Formato: separador `;`, coma decimal y columnas `Fecha;Hora;Terminal;Nº operación;Tarjeta;Tipo;Estado;Importe`. El ejemplo ficticio está en [`data/datafono_octubre.csv`](data/datafono_octubre.csv).
- Necesita la credencial `Tienda API`. Tras importarlo, elige `SUB - Enviar notificación` en *Enviar informe a Marisa* y `08 - Error Workflow` en *Settings → Error workflow*.
- Se ejecuta a mano (*Ejecutar a mano*) o cada noche a las 22:30. **Publícalo en una sola instancia de n8n.**

**Resultados con `data/datafono_octubre.csv`** (tienda con los datos de la migración de T-012):

| Línea | Cobro | Resultado |
|---|---|---|
| op. 000101 | 01/10 · 79,90 € | Ya estaba: venta «Bota montaña T41» con tarjeta |
| op. 000102 | 01/10 · 24,50 € | **Cargado** como venta con tarjeta |
| op. 000201 | 02/10 · 12,00 € | Ya estaba: venta «Plantillas gel» con tarjeta |
| op. 000202 | 02/10 · 45,00 € · denegada | Ignorada |
| op. 000203 (dos veces) | 02/10 · 18,95 € | **Cargado una sola vez**. Ese día hay una venta de 18,95 €, pero en efectivo, así que no es este cobro |
| op. 000301 | 03/10 · 92,00 € | Ya estaba: venta «Botín piel negro T40» con tarjeta |
| op. 000401 | 04/10 · −12,00 € · devolución | Para que Marisa lo revise |
| op. 000501 | 05/10 · `3O,00` | Para que Marisa lo revise: importe ilegible |
| op. 000601 | 06/10 · 39,90 € · anulada | Ignorada |
| op. 000602 | 06/10 · 64,50 € | **Cargado** como venta con tarjeta |
| Totales | — | Ignorada |

Al ejecutarlo otra vez no carga nada: reconoce las tres ventas que cargó por su número de operación.

### Asistente de Telegram para Marisa (T-017)

Marisa pregunta por Telegram en lenguaje natural ("¿cuánto se recaudó esta semana?", "¿qué apartados vencen este mes?", "¿ya pagó Carmen?") y un agente de IA responde con datos de la API. Solo lee: no registra abonos ni cambia nada.

**Piezas** (todas en [`workflows/`](workflows/)):

- `Asistente Marisa`: bot propio (`Telegram Marisa`) → `¿Es chat privado?` → `¿Es Marisa?` → agente `Responder pregunta` (Groq `openai/gpt-oss-20b`, credencial `Modelo IA`, memoria de los 4 últimos intercambios) → `Enviar respuesta`.
- `SUB - Recaudado por periodo`: abonos y ventas de un periodo, sumados en céntimos por forma de pago.
- `SUB - Vencimientos por periodo`: apartados `activo` cuya `fecha_limite` cae en un periodo.
- Tercera herramienta, `Buscar apartado`: consulta `GET /api/apartados?q=` por cliente, producto, teléfono o número (cualquier estado).

**Cómo se mantiene el control:**

- **Solo responde a Marisa.** Un nodo determinista compara `chat.id` con `TELEGRAM_CHAT_ID_MARISA` y exige chat privado; si no coincide, no se consulta ni la API ni el modelo. Para la demo, pon el identificador real de Marisa (ella escribe una vez al bot) en vez del tuyo.
- **El modelo no calcula.** Elige un `periodo` de una lista (`hoy`, `esta_semana`, `este_mes`…); un nodo Code calcula las fechas (zona Europe/Madrid, semana de lunes a domingo) y otro suma el dinero. El modelo copia el texto resultante, que empieza por el rango de fechas usado.
- **Modelo caído:** Marisa recibe "Ahora mismo no puedo responder. Inténtalo de nuevo en unos minutos." sin cifras.
- Cada pregunta vuelve a consultar la herramienta: el prompt prohíbe reutilizar cifras de respuestas anteriores.

**Para ponerlo en marcha:**

- Crea el bot con BotFather y la credencial `Telegram Marisa`. Rellena `TELEGRAM_CHAT_ID_MARISA` en `.env` y reinicia n8n (`docker compose up -d n8n`).
- Telegram exige una URL pública HTTPS para el webhook: en local hace falta un túnel (por ejemplo `cloudflared tunnel --url http://localhost:5678`), que cambia en cada arranque.
- Tras importar, vuelve a elegir los dos `SUB - …` en las herramientas `Recaudado por periodo` y `Vencimientos por periodo`, y asigna `08 - Error Workflow`. **Publica los sub-workflows** cada vez que los cambies: el agente usa la versión publicada.
- Un bot solo admite un webhook: no uses el mismo bot que el asistente de clientes.
- Groq recibe nombres de clientes y datos de apartados; las pruebas se hicieron con datos ficticios. El plan gratuito limita los tokens por minuto.

### Solicitudes de apartado (T-018)

Un cliente puede pedir un apartado desde casa con un formulario. El apartado **no se crea hasta que paga el abono inicial**: la app exige al menos 5 € para crearlo y no se da por cobrado dinero que no ha llegado. Son dos flujos y una tabla de n8n:

1. **`Solicitudes de apartado`** (formulario público `/form/solicitud-apartado`): nombre, teléfono, correo (opcional), modelo, talla y comentario.
   - **Nueva:** se guarda como `pendiente` en la tabla `solicitudes_apartado` con un número de solicitud. Marisa recibe un aviso con el número y el enlace para confirmarla, y el cliente, si dejó correo, un acuse de recibo.
   - **Incompleta** (falta nombre, modelo o talla, o el teléfono o el correo no son válidos) o **repetida** (misma persona, modelo, talla y día): no se guarda y se avisa a Marisa.
   - No toca la app.
2. **`Confirmar solicitud de apartado`** (formulario `/form/confirmar-solicitud`, **protegido con usuario y contraseña**, credencial `Acceso Marisa`): cuando el cliente paga, Marisa rellena el número de solicitud, el precio, el abono inicial y la forma de pago.
   - Comprueba que la solicitud existe y está pendiente, que el abono es de al menos 5 € y no supera el precio, y que la forma de pago es válida.
   - Si todo está bien, crea el apartado (`POST /api/apartados`) y marca la solicitud como `confirmada`. La app emite `apartado.creado` y el flujo 01 manda la confirmación al cliente.
   - Una solicitud ya confirmada no crea otro apartado. Marisa recibe siempre un correo con el resultado.

**Para ponerlo en marcha:**

- En n8n, *Data tables* → crea la tabla `solicitudes_apartado` con estas columnas: `clave`, `cliente`, `telefono`, `email`, `producto`, `talla`, `comentario`, `fecha` y `estado` (texto), y `apartado_id` (número). Los flujos la buscan por nombre.
- Crea la credencial `Acceso Marisa` (*Basic Auth*) con el usuario y la contraseña de Marisa. Tras importar, elige `SUB - Enviar notificación` en los nodos de aviso y `08 - Error Workflow` en *Settings → Error workflow*.
- Los formularios solo funcionan con los flujos **publicados**, y en una sola instancia. Para probar sin formulario, cada flujo tiene un disparador manual con ejemplos.

**Resultados con los ejemplos de los propios flujos** (tienda con los datos de la migración de T-012):

| Prueba | Resultado |
|---|---|
| 4 solicitudes: Carmen (con correo), Pedro (sin correo), Ana sin modelo, Carmen repetida | Se guardan la nº 1 (Carmen) y la nº 2 (Pedro) como pendientes; Ana y la repetida no se guardan. 5 avisos: 4 a Marisa y el acuse de recibo a Carmen |
| 4 confirmaciones: nº 1 (89,90 €, 10 € por Bizum) dos veces, nº 2 con 3 € de abono, nº 99 | Se crea el **apartado #8** de Carmen y la nº 1 queda `confirmada`; la repetida, la de 3 € (mínimo 5 €) y la nº 99 (no existe) no crean nada. El flujo 01 manda la confirmación a Carmen |
| Las mismas solicitudes y confirmaciones otra vez | No se guarda ninguna solicitud ni se crea ningún apartado: «ya está confirmada (apartado #8)» |

### Panel movil para Marisa (T-021)

Panel de solo lectura para Marisa, servido como pagina HTML desde n8n (/webhook/panel-marisa), protegido con Basic Auth (credencial Acceso Marisa). Muestra el total cobrado hoy (ventas + abonos, con desglose por forma de pago), los apartados que vencen en los proximos 7 dias y el total pendiente de cobro. No modifica la app ni el frontend.

Para ponerlo en marcha:

- Importa workflows/21 - Panel movil para Marisa.json y publica el flujo.
- Crea/selecciona las credenciales Tienda API y Acceso Marisa.
- Abre https://<tu-dominio>/webhook/panel-marisa (o http://n8n:5678/webhook/panel-marisa desde dentro) e inicia sesion.

### Despliegue en la nube (T-022)

Sin crédito de pago, la **tienda** se publica en **Render** (plan gratuito). El despliegue de **n8n** con su base de datos en **Neon** está preparado pero **pendiente**: el equipo aún decide si usa Neon. Todo está descrito en [`render.yaml`](render.yaml) (el bloque de n8n está comentado). Cómo se hizo, paso a paso y para novatos: [docs/despliegue-nube.md](docs/despliegue-nube.md).

> ⏳ **Aviso: la primera carga tarda.** En el plan gratuito, Render duerme cada servicio tras 15 minutos sin visitas. La primera petición después lo despierta y tarda en contestar: **unos 30-60 s la tienda** (y hasta 1-2 min n8n, cuando esté). No es un error: hay que esperar y recargar. No se usa nada para mantenerlo despierto (ni pings, ni monitores externos, ni tareas programadas activas), porque agotaría las horas gratuitas del mes.

**Por qué no Vercel:** Vercel ejecuta cada petición en una función que se apaga al terminar y solo deja escribir en una carpeta temporal. Un apartado creado en una petición no existiría en la siguiente, así que la tienda (SQLite) no funcionaría, y n8n necesita un proceso que siga vivo.

#### Tienda en Render

**Demo:** https://paso-firme-tienda.onrender.com (API en `/docs`).

Es una **tienda de demostración**: Render gratis no tiene disco permanente, así que al dormirse o reiniciarse vuelve a los datos de ejemplo (`SEED=1`). Sirve para enseñarla, no para trabajar con datos reales.

1. Entra en [render.com](https://render.com) con GitHub (plan gratuito).
2. **New + → Web Service**. Si el repo de la organización no aparece, elige **Public Git Repository** y pega la URL del repo (es público). Cuando `render.yaml` esté en `dev`, también vale **New + → Blueprint**.
3. Configuración: nombre `paso-firme-tienda`, lenguaje **Docker**, rama `dev`, región **Frankfurt**, `Dockerfile Path` `./Dockerfile`, tipo de instancia **Free** y, en *Advanced*, `Health Check Path` `/`.
4. Variables de entorno:

   | Variable | Valor |
   |---|---|
   | `API_KEY` | una clave larga **nueva, solo para esta demo** |
   | `SEED` | `1` |
   | `TZ` | `Europe/Madrid` |
   | `PORT` | `8000` |

   Sin `N8N_WEBHOOK_URL` la tienda funciona igual y no intenta avisar a n8n.
5. **Deploy Web Service**. Cuando ponga *Live*: `https://<servicio>.onrender.com` (la tienda) y `/docs` (la API). Render sirve la URL solo por **HTTPS**.

La app pasa la `API_KEY` al navegador (`/config.js`) para que funcione la web: cualquiera que abra la página puede verla. Por eso es una clave aparte y los datos son ficticios.

#### n8n en la nube (pendiente)

Preparado para quien lo continúe: el bloque `paso-firme-n8n` de `render.yaml` (comentado) usa la imagen `n8nio/n8n:2.44.4` con flujos, credenciales y ejecuciones en **Neon** (Postgres que escala a cero), así que no se pierden aunque Render duerma. Se probó en local que n8n 2.44.4 arranca contra Neon y crea sus tablas.

1. **Neon:** proyecto en Frankfurt con una base `n8n` y un usuario `n8n`. Copia el *host* de la conexión **directa** (sin `-pooler`, porque n8n hace migraciones al arrancar), el usuario y la contraseña.
2. Descomenta el bloque de n8n en `render.yaml` (y `N8N_WEBHOOK_URL` y `WEBHOOK_TOKEN` en la tienda) y aplica el Blueprint.
3. Rellena en Render los secretos (nunca en el repo):

   | Servicio | Variable | Valor |
   |---|---|---|
   | tienda | `N8N_WEBHOOK_URL` | `https://<servicio-n8n>.onrender.com/webhook/tienda` |
   | tienda y n8n | `WEBHOOK_TOKEN` | el mismo valor en los dos (T-020) |
   | n8n | `N8N_HOST` | `<servicio-n8n>.onrender.com` |
   | n8n | `WEBHOOK_URL`, `N8N_EDITOR_BASE_URL` | `https://<servicio-n8n>.onrender.com/` |
   | n8n | `DB_POSTGRESDB_HOST`, `_DATABASE`, `_USER`, `_PASSWORD` | los de Neon |
   | n8n | `EMAIL_TIENDA` | el correo de la tienda |
   | n8n | `TELEGRAM_CHAT_ID_MARISA` | el chat de Telegram de Marisa |

   `N8N_ENCRYPTION_KEY` la genera Render. **Guárdala en un gestor de contraseñas**: sin ella no se pueden leer las credenciales de una copia de la base.
4. Abre la URL de n8n (espera a que despierte), crea la cuenta de propietaria, crea las credenciales con **los mismos nombres** que en local (la de la tienda apunta a `https://<servicio-tienda>.onrender.com`) e importa los JSON de `workflows/`. En cada nodo *Execute Workflow* vuelve a elegir el sub-workflow.
5. Publica los sub-workflows y los flujos que responden a personas (webhook `00`, formularios, panel, Telegram). Los programados (`05`, `06`, `07`, `Entrada CSV del datáfono`) y el de correo IMAP (`03`) se quedan **sin publicar** salvo que Marisa lo pida: con el servicio dormido no se ejecutarían y, despiertos, gastarían horas.

Limitación conocida: si n8n está dormido, el primer aviso de la tienda **se pierde** (la tienda espera 5 s y n8n tarda más en despertar; queda en su log como «No se pudo avisar a n8n»). Antes de una demo, abre primero n8n.

**Copias de seguridad de n8n**, sin tareas programadas: los flujos están versionados en `workflows/`; Neon guarda 6 horas de historial para restaurar la base a un momento (*Branches* → *Restore*), y se puede sacar una copia completa bajo demanda:

```bash
docker run --rm postgres:17 pg_dump "<cadena de conexión de Neon>" > copia-n8n.sql      # sacar copia
docker run --rm -i postgres:17 psql "<cadena de una base vacía>" < copia-n8n.sql          # restaurar
```

La copia no va al repo (lleva datos y credenciales cifradas) y para leer las credenciales hace falta la misma `N8N_ENCRYPTION_KEY`. La tienda no se copia: sus datos de demostración se regeneran solos.

#### CI

En cada PR que toca `workflows/`, la acción [`Validar flujos`](.github/workflows/validar-flujos.yml) comprueba que los JSON son exports válidos de n8n y que no llevan claves (Groq, tokens de Telegram, contraseñas escritas en un nodo, credenciales con datos, URL con usuario y contraseña). Si encuentra algo, la PR falla y marca el fichero. También avisa, sin fallar, de flujos exportados publicados o sin `08 - Error Workflow`. No llama a la tienda ni a n8n, así que no despierta nada. En local: `python .github/scripts/validar_flujos.py workflows`.

---

### Estructura del repositorio

| Ruta | Qué hay |
|---|---|
| `workflows/` | Flujos de n8n exportados en JSON, uno por flujo |
| `openspec/specs/` | Cómo funciona hoy el sistema (API, webhook, reglas del apartado) |
| `openspec/changes/` | Un change de OpenSpec por ticket: propuesta, diseño, spec y tareas |
| `docs/` | [Guía de la app](docs/guia-de-la-app.md), [guía del equipo](docs/guia-del-equipo.md), [ontología](docs/ontologia.md), mapas del proceso y [bitácora de IA](docs/ai-log.md) |
| `data/` | Excel antiguo de Marisa (CSV) y correos de ejemplo del banco |
| `backend/`, `frontend/` | App de la tienda (no se modifica) |
| `AGENTS.md` | Reglas para personas y agentes de IA |
| `ENUNCIADO.md` | Enunciado original del proyecto |

### Forma de trabajo

- **Gitflow:** `main` ← `dev` ← ramas `feat/T-XXX-…`. Las PR van siempre a `dev`, con revisión de otra persona.
- **Spec primero:** cada flujo es un change de OpenSpec; al terminar se archiva en la misma PR.
- Commits y PR en inglés con el ticket como scope: `feat(T-003): …`. Documentación en español.
- El uso de IA se anota en [`docs/ai-log.md`](docs/ai-log.md), errores incluidos. Detalle completo en [AGENTS.md](AGENTS.md).

### Equipo

| Persona | GitHub |
|---|---|
| Charlotte | [@Charlottedoulcet](https://github.com/Charlottedoulcet) |
| Leandro | [@Leandroletoile](https://github.com/Leandroletoile) |
| Anna | [@costanna](https://github.com/costanna) |

---

## 🇬🇧 English

### What it is

Paso Firme is a neighbourhood shoe shop whose key service is **layaway** (*apartado*): the customer reserves a pair of shoes with a down payment (at least €5) and pays the rest in instalments within 90 days. The shop already has an app (FastAPI + SQLite) to record layaways, payments and sales.

This repository **does not change the app**. It uses **n8n** to automate everything around it: notifying customers, recording payments that arrive by Bizum or bank transfer, closing the till, reminding customers of deadlines and reporting to Marisa, the owner. The full project brief (in Spanish) is in [ENUNCIADO.md](ENUNCIADO.md).

### Workflows

| # | Workflow | Trigger | Ticket | Owner |
|---|---|---|---|---|
| — | Webhook base and credentials | Webhook `/webhook/tienda` | T-001 | Charlotte |
| — | `SUB - Enviar notificación` (send notification) | Called by other workflows | T-002 | Charlotte |
| — | `SUB - Buscar apartado` (find layaway) | Called by other workflows | T-003 | Anna |
| 1 | Layaway confirmation | `apartado.creado` event | T-004 | Leandro |
| 2 | Payment receipt | `abono.registrado` event | T-005 | Leandro |
| 5 | Daily close | Scheduled, 22:00 | T-006 | Leandro |
| 8 | Error Workflow | Error in any workflow | T-007 | Charlotte |
| 3 | Remote payments (Bizum and transfer) | Bank email (IMAP) | T-008 | Anna |
| 6 | Reminders and expiries | Scheduled, 09:00 | T-009 | Charlotte |
| 4 | Large sale alert | `venta.registrada` event | T-010 | Leandro |
| 7 | Monthly report | Scheduled, 1st of the month at 08:00 | T-011 | Charlotte |
| — | Migration of Marisa's spreadsheet | Manual, run once | T-012 | Anna |
| — | Comparison of two free AI models | — | T-013 | Anna and Charlotte |
| — | Marisa's assistant (Telegram with an AI agent) | Message to Marisa's bot | T-017 | Charlotte |

Ticket status lives on the [Kanban board](https://github.com/orgs/IA-P1-BCN/projects/41). Scope: the brief's **Essential** and **Intermediate** levels.

### How it works

| Piece | From your browser | From inside n8n |
|---|---|---|
| Shop app | http://localhost:8000 (API at `/docs`) | `http://tienda:8000` |
| n8n | http://localhost:5678 | — |
| Event webhook | — | the app calls `http://n8n:5678/webhook/tienda` |

- The app notifies n8n through **a single webhook**; a **Switch** node routes on `evento` (`apartado.creado`, `abono.registrado`, `venta.registrada`…).
- n8n reads from and acts on the app through its **REST API**, using the `X-API-Key` header.
- Amounts (`abonado`, `pendiente`, `precio`) always come from the app; workflows never recalculate them.
- In workflow 3, AI **only extracts** payer, amount and reference from the email. Deterministic nodes decide whether to record, ask or reject. When in doubt, nothing is recorded and Marisa is asked.

### 🚀 Getting started

You need [Git](https://git-scm.com/) and [Docker Desktop](https://www.docker.com/products/docker-desktop/) running. Each team member runs **their own n8n instance**.

```bash
git clone https://github.com/IA-P1-BCN/zapateria_paso_firme_G6.git paso-firme
cd paso-firme
cp .env.example .env        # then fill in the values (see the variables table)
docker compose up -d        # shop on :8000, n8n on :5678
```

1. Open http://localhost:5678 and create your local n8n account.
2. Create the credentials in the table below, **with these exact names**.
3. Import the workflows from [`workflows/`](workflows/) (workflow menu → *Import from file*).
4. In workflows that call a sub-workflow (`SUB - …`), pick it again in the *Execute Workflow* node: its internal ID differs on every instance.
5. In every workflow (except `08 - Error Workflow` and `SUB - Enviar notificación`), open *Settings → Error workflow* and pick `08 - Error Workflow`: its ID also differs on every instance.

To stop: `docker compose down`. To also delete the data: `docker compose down -v`.

### Variables and credentials (no values)

| `.env` variable | Purpose |
|---|---|
| `API_KEY` | Key the app requires in the `X-API-Key` header |
| `N8N_WEBHOOK_URL` | Where the app notifies n8n (value from `.env.example`) |
| `SEED` | `1` loads sample data on start; `0` starts empty (migration) |
| `EMAIL_TIENDA` | Shop mailbox: receives the alerts to Marisa and is also the sender of the emails |
| `UMBRAL_VENTA_GRANDE` | Amount in € from which a sale counts as "large" (default `80`) |
| `WEBHOOK_TOKEN` | Token the app sends in `X-Webhook-Token` when notifying n8n (empty = no notifications) |
| `N8N_EDITOR_BASE_URL` | Public/base URL of n8n used by workflows to build links (e.g. confirm request) |
| `TELEGRAM_CHAT_ID_MARISA` | Telegram chat id of Marisa: the only chat served by `Asistente Marisa` (T-017) |

Inside a workflow they are read with `{{ $env.NAME }}`.

| n8n credential | Type | Contents |
|---|---|---|
| `Tienda API` | Header Auth | `X-API-Key` header with the `API_KEY` value |
| `Correo salida` | SMTP | Shop email account |
| `Correo entrada` | IMAP | Same account, to read bank notifications |
| `Modelo IA` | Groq | Personal key from https://console.groq.com |
| `Telegram Marisa` | Telegram | Token of Marisa's bot (created with BotFather; only in the credential, never in the repo) |
| `Telegram Clientes` | Telegram | Token of the customers' bot (created with BotFather; only in the credential, never in the repository) |
| `Acceso Marisa` | Basic Auth | Username and password for the request confirmation form (T-018) |

Workflows only store the credential **name**. The `.env` file and credential values are never committed.

### Data protection and webhook security (T-020)

**Webhook authentication:** the shop sends events to n8n using `POST` to `N8N_WEBHOOK_URL`, with the `X-Webhook-Token` header. Configure the token through `WEBHOOK_TOKEN` in `.env`; never put it in the URL, exported workflow JSON or the repository. n8n checks the header before accepting the event. Requests without a valid token must be rejected. If `WEBHOOK_TOKEN` is missing, the application logs a warning and skips the notification; the shop operation still completes.

**Data sent to external services:**

| Service | Data sent | Purpose |
|---|---|---|
| n8n (local webhook) | Event type and associated app event data; depending on the event, this may include identifiers, names, references and amounts | Automate shop notifications and processes |
| Groq AI provider (workflow 03) | Subject and body of bank emails that pass the filter, to extract payer, amount and reference | Help identify remote payments |
| SMTP email service | Recipient address, subject and message body | Send receipts and alerts |
| Bank mailbox via IMAP | Access to messages received by the configured account | Detect Bizum and bank transfer notifications |

Data reaching n8n may contain personal data. Workflow 03 sends the subject and body of each processed email to Groq; in a real environment, this could disclose personal data to that provider. Use fictitious data in tests and limit transmitted information to what is necessary. Review the provider's terms, privacy settings and the applicable legal basis before processing real data. This documentation is not a legal assessment and does not by itself establish valid consent.

**Consent and transparency:** inform customers, before processing their data, about purposes, recipients or categories of recipients, retention and their rights, as applicable. Do not assume that using the app constitutes valid consent for every processing activity or transfer to third parties.

**Logs and credentials:** do not log tokens, keys, passwords, full email bodies or personal data in error messages. Keep `.env` out of version control and do not export real credentials in workflow files. Sample files should use fictitious data. The webhook token authenticates requests but does not encrypt traffic; use HTTPS and suitable access controls for deployments beyond a controlled local network.
### Sub-workflow contracts

#### `SUB - Buscar apartado` (T-003)

Finds a person's layaway from an ID or from a name written in any form (`JORGE M.`, `LUCIA GOMEZ`). It only reads from the API and only returns layaways whose status is `activo`.

**Input** (*Execute Workflow*):

| Field | Type | Example | Note |
|---|---|---|---|
| `id` | number or text | `12`, `#12` | If valid, the search is by ID and `texto` is ignored |
| `texto` | text | `JORGE M. apartado 2 bota` | Usually the payment's payer + reference |

**Output:**

```json
{
  "resultado": "unico | varios | ninguno",
  "candidatos": [
    { "id": 2, "cliente": "Jorge Martín", "producto": "Bota alta mujer", "talla": "36",
      "precio": 119, "abonado": 40, "pendiente": 79, "fecha_limite": "2027-01-15", "estado": "activo" }
  ]
}
```

- Text is compared ignoring case, accents and punctuation, in chunks of 3+ letters (`de`, `del`, `la`… are skipped). The layaway matching the most chunks wins; a tie returns `varios`.
- A number in the text (`#2`, `apartado 2`) is only used if that layaway also matches part of the name.
- A missing ID (404) or a non-active layaway returns `ninguno`. Any other app error (401, 500) **raises an error**, so it is never mistaken for "not found".
- To be called from another workflow, the sub-workflow must be **published** on that n8n instance.

#### `SUB - Enviar notificación` (T-002)

Sends a plain-text email to a customer or to the shop (Marisa). Used by the workflows that notify by email. It uses the `Correo salida` credential and the `EMAIL_TIENDA` variable. It **never raises an error to its caller**: the result says whether the email was sent.

**Input** (*Execute Workflow*):

| Field | Type | Example | Note |
|---|---|---|---|
| `destinatario` | text | `cliente`, `tienda` | `tienda` sends to `EMAIL_TIENDA` |
| `email` | text | `carmen@example.com` | Only for `cliente`; may be empty or missing |
| `asunto` | text | `Tu apartado en Paso Firme` | |
| `mensaje` | text | `Hola Carmen, hemos registrado tu apartado.` | Plain text |
| `contexto` | text | `Apartado 25 - Carmen Ruiz` | Optional; identifies the layaway in the alert to the shop |

**Output:**

```json
{ "enviado": true, "motivo": "" }
```

| `enviado` | `motivo` | When |
|---|---|---|
| `true` | `""` | Email sent to the customer or to the shop |
| `false` | `sin_email` | `cliente` without `email`: nothing is sent to the customer and the shop is alerted with the `contexto` |
| `false` | `error_envio` | The mail server failed, or `destinatario` is neither `cliente` nor `tienda` |

- The caller does not need to catch errors: it checks `enviado` and, if `false`, `motivo`.
- To be called from another workflow, the sub-workflow must be **published** on that n8n instance.

### Spreadsheet migration (T-012, run once)

The `Migración Excel` workflow loads the layaways, payments and sales from Marisa's sheets ([`data/excel_actual_apartados.csv`](data/excel_actual_apartados.csv) and [`data/excel_actual_ventas.csv`](data/excel_actual_ventas.csv)) into the app, and emails her a report of what was not loaded and why.

**Before running it:**

1. The shop app must be **empty** and its **webhook switched off**. Otherwise every old layaway and sale would trigger its notifications: confirmations to customers, large-sale alert… In `.env` set `SEED=0` and leave `N8N_WEBHOOK_URL=` empty, then:

   ```bash
   docker compose rm -sf tienda
   docker volume ls                          # find the volume ending in _tienda_data
   docker volume rm <folder>_tienda_data     # deletes ONLY the shop data, not n8n's
   docker compose up -d tienda
   ```

2. Copy the CSV files into n8n, which cannot see the repository's `data/` folder:

   ```bash
   docker compose exec n8n mkdir -p /home/node/.n8n-files/migracion
   docker compose cp data/excel_actual_apartados.csv n8n:/home/node/.n8n-files/migracion/
   docker compose cp data/excel_actual_ventas.csv n8n:/home/node/.n8n-files/migracion/
   ```

3. The report is sent through `SUB - Enviar notificación`: import it, publish it and select it in the *Enviar informe a Marisa* node (its ID differs on every instance). Also check that the `Tienda API` and `Correo salida` credentials exist and that `EMAIL_TIENDA` is set: it is the address that receives the report.

**Running it:** open the workflow in n8n and click *Execute workflow*. Running it again does not duplicate anything, because it checks what is already in the app before creating.

**Afterwards:** put back in `.env` the `N8N_WEBHOOK_URL` from `.env.example` and restart the shop (`docker compose up -d tienda`) so notifications reach n8n again.

**What it does with the data:**

| Case | What happens |
|---|---|
| Dates `7/9/26`, amounts `15€`, lower-case names | Normalised (`2026-09-07`, `15`, `Carmen Ruiz`) |
| Several rows for the same customer, model and size | The first is the layaway and the rest its payments, in date order |
| Down payment under €5 (Lucía Gómez) | Neither the layaway nor its payments are loaded; it goes to the report |
| Sales that are layaway payments (`abono inicial apartado`, `Abono Ana Torres mocasin`, `(apartado)`) | Not loaded as sales; they give that payment's method |
| Payments with an unknown method | Loaded as `efectivo` (cash) and flagged in the report as an assumption |
| `TOTAL SEPTIEMBRE (a mano)` row | Ignored |
| At the end | Compares each layaway's outstanding amount with the `resta` column, and the totals with the spreadsheet |

With the sample data it loads 7 layaways, 3 later payments and 6 sales: €170.00 in payments and €213.85 in sales, matching the spreadsheet.

### Workflow 03 · Bizum and bank transfer payments (T-008)

The `03 - Abonos a distancia` workflow reads the bank notifications that reach the shop mailbox, uses AI to extract who pays, how much and the reference, and records the payment in the app only when it is clear. Otherwise it records nothing and alerts Marisa.

**How it decides:**

1. **Filter without AI:** only emails with the bank's `Importe` and `Ordenante` lines go on. Adverts, the workflows' own alerts and bounced emails are ignored without calling the model.
2. **AI extraction** (`Modelo IA` credential, Groq model `qwen/qwen3.8-27b`, chosen in T-013): the model only copies `ordenante`, `importe` and `concepto`. It receives just the subject and body of the email; test data is fictitious.
3. **Validation in code:** the amount becomes a number (`10,00 EUR` → `10`); if it is not positive, the payment is doubtful.
4. **Lookup** with `SUB - Buscar apartado` (payer + reference).
5. **Rules (no AI):** it records only if there is a single active layaway, the payment has a reference, it is within the deadline, it does not exceed the outstanding amount and that layaway has no payment of the same amount today yet (possible duplicate). Otherwise Marisa is asked, or told about the rejection, with the reason and the possible layaways.
6. **Recording:** `POST /api/apartados/{id}/abonos` with `forma_pago: bizum`. Transfers are also recorded as `bizum` (the app has no `transferencia`) and Marisa is told so. The app emits `abono.registrado` and workflow 02 sends the customer their receipt.

**To run it:**

- Credentials `Correo entrada`, `Tienda API` and `Modelo IA`. After importing, select `SUB - Buscar apartado` and `SUB - Enviar notificación` in their *Execute Workflow* nodes and `08 - Error Workflow` in *Settings → Error workflow*.
- **Publish it on a single n8n instance only.** When first published it only processes emails that arrive from then on.
- To test without the mailbox: copy the emails into n8n (`docker compose exec n8n mkdir -p /home/node/.n8n-files/correos` and `docker compose cp data/correos/. n8n:/home/node/.n8n-files/correos/`) and click *Execute workflow* from the *Probar con los correos de ejemplo* trigger.

**Actual results with the 9 emails in `data/correos/`** (the app's sample data, real mailbox test on 25/10/2026):

| Email | Extracted data | Result |
|---|---|---|
| 01 Bizum Carmen Ruiz | `CARMEN RUIZ GARCIA` · €10 · `zuecos` | Recorded on #1 (€19.50 outstanding, now €9.50) |
| 02 Bizum `JORGE M.` | `JORGE M.` · €20 · `apartado 2 bota` | Recorded on #2 (€79 → €59) |
| 03 Transfer Lucía Gómez | `LUCIA GOMEZ PEREZ` · €12 · `Liquidar mocasines` | Recorded on #3, now **paid off**; Marisa told it is recorded as bizum |
| 04 Bizum `LAURA O.` | `LAURA O.` · €15 · `deportivas` | Not recorded: exceeds the outstanding €10; Marisa alerted |
| 05 Bizum `ROMERO D` | `ROMERO D` · €10 · *(empty)* | Not recorded: no reference; Marisa alerted with #11 as possible |
| 06 Bizum Paula Ramos | `PAULA RAMOS LEON` · €20 · `zapatillas running…` | Not recorded: past the deadline; Marisa alerted |
| 07 Transfer Antonio Fernández | `ANTONIO FERNANDEZ SOTO` · €25 · `botas` | Not recorded: no layaway matches; Marisa alerted |
| 08 Bank advert | — (never reaches the model) | Ignored |
| 09 Bizum Silvia Cortés | `SILVIA CORTES` · €5 · `abono sandalias` | Recorded on #24 |

Running the same 9 emails again records no payment: the ones already recorded are reported as a possible duplicate or as exceeding the outstanding amount.

### AI model comparison (T-013)

For workflow 03, two free Groq models were compared on the same task: extracting `ordenante`, `importe` and `concepto` from the bank notifications.

**How it was done:**

- **Same input for both:** the T-008 prompt and the 9 emails in `data/correos/`, including the advert, to see whether the model makes data up. Temperature 0.
- **Three rounds:** 27 answers per model.
- **Accuracy:** each field is compared with what the email says; the amount after converting it to a number.
- **Valid JSON:** the whole answer is a JSON object, with no text or code fences around it.
- **Time:** the one Groq reports for each request (`total_time`).
- **Data sent:** only the instructions plus the email subject and body, about 300-350 tokens per request. No sender, headers or shop data are sent, and the test emails are fictitious.

  <details><summary>Exact instructions (system message, the same one workflow 03 uses)</summary>

  ```text
  Eres un extractor de datos. Lees un aviso de un banco sobre un pago recibido (Bizum o transferencia) y devuelves SOLO un objeto JSON, sin explicaciones ni bloques de código, con estos tres campos de texto:
  - "ordenante": lo que aparece en la línea "Ordenante", copiado tal cual.
  - "importe": lo que aparece en la línea "Importe", copiado tal cual (por ejemplo "10,00 EUR").
  - "concepto": lo que aparece en la línea "Concepto", copiado tal cual. Si esa línea está vacía o no existe, devuelve "".
  Reglas: no inventes ni completes datos, no corrijas nombres, no uses el texto de otras líneas para rellenar un campo. Si un dato no aparece, devuelve "".
  Ejemplo de respuesta: {"ordenante": "ANA PEREZ", "importe": "15,00 EUR", "concepto": "botas"}
  ```

  </details>
  <details><summary>Exact user message, example with email 01</summary>

  ```text
  Asunto: Has recibido un Bizum de 10,00 €

  Hola, ZAPATERIA PASO FIRME:

  Has recibido un Bizum.

  Importe: 10,00 EUR
  Ordenante: CARMEN RUIZ GARCIA
  Concepto: zuecos

  El importe ya está disponible en tu cuenta terminada en 4821.

  Banco Ejemplo
  ```

  </details>

- **To repeat it:** import `workflows/Comparativa de modelos.json`, copy the emails into n8n (as for workflow 03) and click *Execute workflow*. It uses the `Modelo IA` credential.

| Metric | `openai/gpt-oss-20b` | `qwen/qwen3.8-27b` |
|---|---|---|
| Correct fields | 81/81 | 81/81 |
| Emails with all three fields right | 27/27 | 27/27 |
| Valid JSON | 27/27 | 27/27 |
| Advert with no made-up data | 3/3 | 3/3 |
| Same answer in all three rounds | 9/9 emails | 9/9 emails |
| Response time: mean / median / max | 0.175 / 0.153 / 0.337 s | 0.098 / 0.096 / 0.206 s |
| Answer tokens (mean) | 134 | 32 |

**Chosen model: `qwen/qwen3.8-27b`.** Both get everything right, so the difference is cost. Qwen takes about half the time and uses roughly 4 times fewer answer tokens (`gpt-oss` reasons before answering), which leaves more room within Groq's free-tier limits and less risk of a cut-off answer. The sample is small (9 emails) and both do well; this is not a quality difference. Workflow 03 now uses this model and gives the same results with the 9 emails.

### Card terminal CSV import (T-019)

The `Entrada CSV del datáfono` workflow reads the card payments CSV exported by the card terminal, reconciles it with the card sales and card layaway payments already in the app, and records the missing charges as card sales. It emails Marisa a report with what it loaded, what was already there and what she needs to check.

**How it decides:**

- **Valid charges:** only `VENTA` + `AUTORIZADA` lines count. Declined and cancelled lines, the totals line and repeated lines (same operation number) are ignored.
- **For Marisa to check, nothing loaded:** refunds (the app has no refunds) and lines with an unreadable date, amount or operation number.
- **Already in the app?** A charge is already there if it matches a card sale **or a card layaway payment** on the same day for the same amount; each app record matches one charge only. Layaway payments must be checked too: a card layaway payment goes through the terminal and is not a new sale.
- **Missing charges** are loaded as card sales with the charge date and the concept `Cobro con tarjeta (datáfono, op. 000102)`. Thanks to that operation number, running it again duplicates nothing.

**To run it:**

- Copy the CSV into n8n: `docker compose exec n8n mkdir -p /home/node/.n8n-files/datafono` and `docker compose cp <file>.csv n8n:/home/node/.n8n-files/datafono/`. Format: `;` separator, decimal comma and columns `Fecha;Hora;Terminal;Nº operación;Tarjeta;Tipo;Estado;Importe`. The fictitious sample is [`data/datafono_octubre.csv`](data/datafono_octubre.csv).
- It needs the `Tienda API` credential. After importing, select `SUB - Enviar notificación` in *Enviar informe a Marisa* and `08 - Error Workflow` in *Settings → Error workflow*.
- It runs manually (*Ejecutar a mano*) or every night at 22:30. **Publish it on a single n8n instance only.**

**Results with `data/datafono_octubre.csv`** (shop with the T-012 migration data):

| Line | Charge | Result |
|---|---|---|
| op. 000101 | 01/10 · €79.90 | Already there: card sale "Bota montaña T41" |
| op. 000102 | 01/10 · €24.50 | **Loaded** as a card sale |
| op. 000201 | 02/10 · €12.00 | Already there: card sale "Plantillas gel" |
| op. 000202 | 02/10 · €45.00 · declined | Ignored |
| op. 000203 (twice) | 02/10 · €18.95 | **Loaded once**. There is an €18.95 sale that day, but in cash, so it is not this charge |
| op. 000301 | 03/10 · €92.00 | Already there: card sale "Botín piel negro T40" |
| op. 000401 | 04/10 · −€12.00 · refund | For Marisa to check |
| op. 000501 | 05/10 · `3O,00` | For Marisa to check: unreadable amount |
| op. 000601 | 06/10 · €39.90 · cancelled | Ignored |
| op. 000602 | 06/10 · €64.50 | **Loaded** as a card sale |
| Totals | — | Ignored |

Running it again loads nothing: it recognises the three sales it loaded by their operation number.

### Telegram assistant for Marisa (T-017)

Marisa asks in plain language on Telegram ("how much did we take this week?", "which layaways expire this month?", "has Carmen paid?") and an AI agent answers with data from the API. It is read-only: it does not register payments or change anything.

**Parts** (all in [`workflows/`](workflows/)):

- `Asistente Marisa`: own bot (`Telegram Marisa`) → `¿Es chat privado?` → `¿Es Marisa?` → agent `Responder pregunta` (Groq `openai/gpt-oss-20b`, `Modelo IA` credential, memory of the last 4 exchanges) → `Enviar respuesta`.
- `SUB - Recaudado por periodo`: payments and sales of a period, summed in cents by payment method.
- `SUB - Vencimientos por periodo`: `activo` layaways whose `fecha_limite` falls in a period.
- Third tool, `Buscar apartado`: `GET /api/apartados?q=` by customer, product, phone or number (any status).

**How control is kept:**

- **Only answers Marisa.** A deterministic node compares `chat.id` with `TELEGRAM_CHAT_ID_MARISA` and requires a private chat; otherwise neither the API nor the model is touched. For the demo, put Marisa's real id (she writes to the bot once) instead of yours.
- **The model does not calculate.** It picks a `periodo` from a list (`hoy`, `esta_semana`, `este_mes`…); a Code node computes the dates (Europe/Madrid, week from Monday to Sunday) and another sums the money. The model copies the resulting text, which starts with the date range used.
- **Model down:** Marisa gets "Ahora mismo no puedo responder. Inténtalo de nuevo en unos minutos." with no figures.
- Every question calls the tool again: the prompt forbids reusing figures from earlier answers.

**Setup:**

- Create the bot with BotFather and the `Telegram Marisa` credential. Fill `TELEGRAM_CHAT_ID_MARISA` in `.env` and restart n8n (`docker compose up -d n8n`).
- Telegram needs a public HTTPS URL for the webhook: locally you need a tunnel (for example `cloudflared tunnel --url http://localhost:5678`), which changes at every start.
- After importing, pick the two `SUB - …` workflows again in the `Recaudado por periodo` and `Vencimientos por periodo` tools, and assign `08 - Error Workflow`. **Publish the sub-workflows** every time you change them: the agent uses the published version.
- A bot only supports one webhook: do not reuse the customer assistant's bot.
- Groq receives customer names and layaway data; tests used fictitious data. The free plan limits tokens per minute.

### Layaway requests (T-018)

A customer can request a layaway from home through a form. The layaway **is not created until they pay the down payment**: the app needs at least €5 to create it, and money that has not arrived is never recorded as paid. It uses two workflows and an n8n data table:

1. **`Solicitudes de apartado`** (public form `/form/solicitud-apartado`): name, phone, email (optional), model, size and comment.
   - **New:** saved as `pendiente` in the `solicitudes_apartado` table with a request number. Marisa gets an alert with the number and the confirmation link, and the customer, if they left an email, an acknowledgement.
   - **Incomplete** (missing name, model or size, or an invalid phone or email) or **repeated** (same person, model, size and day): not saved, and Marisa is alerted.
   - It does not touch the app.
2. **`Confirmar solicitud de apartado`** (form `/form/confirmar-solicitud`, **protected with a username and password**, `Acceso Marisa` credential): when the customer pays, Marisa enters the request number, price, down payment and payment method.
   - It checks that the request exists and is pending, that the down payment is at least €5 and not above the price, and that the payment method is valid.
   - If everything is fine, it creates the layaway (`POST /api/apartados`) and marks the request as `confirmada`. The app emits `apartado.creado` and workflow 01 sends the customer the confirmation.
   - An already confirmed request does not create another layaway. Marisa always gets an email with the result.

**To run it:**

- In n8n, *Data tables* → create the `solicitudes_apartado` table with these columns: `clave`, `cliente`, `telefono`, `email`, `producto`, `talla`, `comentario`, `fecha` and `estado` (text), and `apartado_id` (number). The workflows look it up by name.
- Create the `Acceso Marisa` credential (*Basic Auth*) with Marisa's username and password. After importing, select `SUB - Enviar notificación` in the alert nodes and `08 - Error Workflow` in *Settings → Error workflow*.
- The forms only work with the workflows **published**, on a single instance. To test without the form, each workflow has a manual trigger with examples.

**Results with the workflows' own examples** (shop with the T-012 migration data):

| Test | Result |
|---|---|
| 4 requests: Carmen (with email), Pedro (no email), Ana without a model, Carmen repeated | Requests 1 (Carmen) and 2 (Pedro) are saved as pending; Ana's and the repeated one are not. 5 alerts: 4 to Marisa and the acknowledgement to Carmen |
| 4 confirmations: no. 1 (€89.90, €10 by Bizum) twice, no. 2 with a €3 down payment, no. 99 | **Layaway #8** is created for Carmen and no. 1 becomes `confirmada`; the repeated one, the €3 one (minimum €5) and no. 99 (does not exist) create nothing. Workflow 01 sends Carmen the confirmation |
| The same requests and confirmations again | No request is saved and no layaway is created: "ya está confirmada (apartado #8)" |

### Mobile panel for Marisa (T-021)

Read-only panel for Marisa, served as an HTML page from n8n (/webhook/panel-marisa), protected with Basic Auth (credential Acceso Marisa). Shows the total collected today (sales + layaway payments, by payment method), layaways expiring in the next 7 days and the total outstanding. Does not modify the app or frontend.

To run it:

- Import workflows/21 - Panel movil para Marisa.json and publish the workflow.
- Create/select the Tienda API and Acceso Marisa credentials.
- Open https://<your-domain>/webhook/panel-marisa (or http://n8n:5678/webhook/panel-marisa from inside) and sign in.

### Cloud deployment (T-022)

With no paid credit, the **shop** is published on **Render** (free plan). Deploying **n8n** with its database on **Neon** is prepared but **pending**: the team is still deciding whether to use Neon. Everything is described in [`render.yaml`](render.yaml) (the n8n block is commented out). How it was done, step by step for beginners (in Spanish): [docs/despliegue-nube.md](docs/despliegue-nube.md).

> ⏳ **Warning: the first load is slow.** On the free plan, Render puts each service to sleep after 15 minutes without traffic. The next request wakes it up and takes a while to answer: **about 30-60 s for the shop** (and up to 1-2 min for n8n, once deployed). It is not an error: wait and reload. Nothing is used to keep it awake (no pings, external monitors or active scheduled jobs), as that would use up the month's free hours.

**Why not Vercel:** Vercel runs each request in a function that stops when it finishes and only allows writing to a temporary folder. A layaway created in one request would not exist in the next, so the shop (SQLite) would not work, and n8n needs a long-running process.

#### Shop on Render

**Demo:** https://paso-firme-tienda.onrender.com (API at `/docs`).

It is a **demo shop**: free Render has no persistent disk, so when it sleeps or restarts it goes back to the sample data (`SEED=1`). It is for showing the app, not for real data.

1. Sign in to [render.com](https://render.com) with GitHub (free plan).
2. **New + → Web Service**. If the organisation's repo is not listed, choose **Public Git Repository** and paste the repo URL (it is public). Once `render.yaml` is on `dev`, **New + → Blueprint** also works.
3. Settings: name `paso-firme-tienda`, language **Docker**, branch `dev`, region **Frankfurt**, `Dockerfile Path` `./Dockerfile`, instance type **Free** and, under *Advanced*, `Health Check Path` `/`.
4. Environment variables:

   | Variable | Value |
   |---|---|
   | `API_KEY` | a long **new key, only for this demo** |
   | `SEED` | `1` |
   | `TZ` | `Europe/Madrid` |
   | `PORT` | `8000` |

   Without `N8N_WEBHOOK_URL` the shop works the same and does not try to notify n8n.
5. **Deploy Web Service**. When it shows *Live*: `https://<service>.onrender.com` (the shop) and `/docs` (the API). Render serves the URL over **HTTPS** only.

The app hands the `API_KEY` to the browser (`/config.js`) so the web page works: anyone who opens the page can see it. That is why it is a separate key and the data is fictitious.

#### n8n in the cloud (pending)

Ready for whoever continues: the `paso-firme-n8n` block in `render.yaml` (commented out) uses the `n8nio/n8n:2.44.4` image with workflows, credentials and executions in **Neon** (Postgres that scales to zero), so they are kept even when Render sleeps. It was tested locally that n8n 2.44.4 starts against Neon and creates its tables.

1. **Neon:** a project in Frankfurt with an `n8n` database and an `n8n` user. Copy the **direct** connection host (without `-pooler`, because n8n runs migrations on startup), the user and the password.
2. Uncomment the n8n block in `render.yaml` (and `N8N_WEBHOOK_URL` and `WEBHOOK_TOKEN` in the shop) and apply the Blueprint.
3. Fill in the secrets in Render (never in the repo):

   | Service | Variable | Value |
   |---|---|---|
   | shop | `N8N_WEBHOOK_URL` | `https://<n8n-service>.onrender.com/webhook/tienda` |
   | shop and n8n | `WEBHOOK_TOKEN` | the same value in both (T-020) |
   | n8n | `N8N_HOST` | `<n8n-service>.onrender.com` |
   | n8n | `WEBHOOK_URL`, `N8N_EDITOR_BASE_URL` | `https://<n8n-service>.onrender.com/` |
   | n8n | `DB_POSTGRESDB_HOST`, `_DATABASE`, `_USER`, `_PASSWORD` | the Neon ones |
   | n8n | `EMAIL_TIENDA` | the shop's email |
   | n8n | `TELEGRAM_CHAT_ID_MARISA` | Marisa's Telegram chat |

   Render generates `N8N_ENCRYPTION_KEY`. **Keep it in a password manager**: without it the credentials in a database backup cannot be read.
4. Open the n8n URL (wait for it to wake up), create the owner account, create the credentials with **the same names** as locally (the shop one points to `https://<shop-service>.onrender.com`) and import the JSON files from `workflows/`. In every *Execute Workflow* node pick the sub-workflow again.
5. Publish the sub-workflows and the workflows that answer people (webhook `00`, forms, panel, Telegram). Scheduled ones (`05`, `06`, `07`, `Entrada CSV del datáfono`) and the IMAP email one (`03`) stay **unpublished** unless Marisa asks: they would not run while the service sleeps and, awake, they would use hours.

Known limitation: if n8n is asleep, the shop's first notification **is lost** (the shop waits 5 s and n8n takes longer to wake up; it shows in the shop log as "No se pudo avisar a n8n"). Before a demo, open n8n first.

**n8n backups**, with no scheduled jobs: workflows are versioned in `workflows/`; Neon keeps 6 hours of history to restore the database to a point in time (*Branches* → *Restore*), and a full backup can be taken on demand:

```bash
docker run --rm postgres:17 pg_dump "<Neon connection string>" > copia-n8n.sql      # back up
docker run --rm -i postgres:17 psql "<empty database string>" < copia-n8n.sql        # restore
```

The backup does not go into the repo (it holds data and encrypted credentials) and reading the credentials needs the same `N8N_ENCRYPTION_KEY`. The shop is not backed up: its demo data regenerates itself.

#### CI

On every PR that touches `workflows/`, the [`Validar flujos`](.github/workflows/validar-flujos.yml) action checks that the JSON files are valid n8n exports and carry no keys (Groq, Telegram tokens, passwords written in a node, credentials with data, URLs with user and password). If it finds something, the PR fails and the file is flagged. It also warns, without failing, about workflows exported as published or without `08 - Error Workflow`. It does not call the shop or n8n, so it wakes nothing. Locally: `python .github/scripts/validar_flujos.py workflows`.

---

### Repository layout

| Path | Contents |
|---|---|
| `workflows/` | n8n workflows exported as JSON, one per workflow |
| `openspec/specs/` | How the system works today (API, webhook, layaway rules) |
| `openspec/changes/` | One OpenSpec change per ticket: proposal, design, spec and tasks |
| `docs/` | [App guide](docs/guia-de-la-app.md), [team guide](docs/guia-del-equipo.md), [ontology](docs/ontologia.md), process maps and [AI log](docs/ai-log.md) (in Spanish) |
| `data/` | Marisa's old spreadsheet (CSV) and sample bank emails |
| `backend/`, `frontend/` | Shop app (not modified) |
| `AGENTS.md` | Rules for people and AI agents |
| `ENUNCIADO.md` | Original project brief |

### How we work

- **Gitflow:** `main` ← `dev` ← `feat/T-XXX-…` branches. PRs always target `dev` and are reviewed by someone else.
- **Spec first:** each workflow is an OpenSpec change, archived in the same PR when done.
- Commits and PRs in English with the ticket as scope: `feat(T-003): …`. Documentation in Spanish.
- AI usage is logged in [`docs/ai-log.md`](docs/ai-log.md), mistakes included. Full details in [AGENTS.md](AGENTS.md).

### Team

| Person | GitHub |
|---|---|
| Charlotte | [@Charlottedoulcet](https://github.com/Charlottedoulcet) |
| Leandro | [@Leandroletoile](https://github.com/Leandroletoile) |
| Anna | [@costanna](https://github.com/costanna) |
