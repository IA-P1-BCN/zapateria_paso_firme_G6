## Decisiones
1. **Un solo webhook y un Switch.** La app solo conoce una URL (`N8N_WEBHOOK_URL`). Alternativa descartada: un webhook por evento (la app no lo permite).
2. **Responder 200 enseguida** y procesar después. La app espera como máximo 5 s y no reintenta; si n8n tarda, el aviso se perdería.
3. **Cada flujo, un workflow aparte llamado con Execute Workflow.** Así cada persona edita su propio JSON y el Switch solo cambia una vez.
4. **Evento desconocido:** rama de salida que no hace nada; queda visible en la ejecución y no falla.
5. **Credenciales por nombre**, el mismo nombre en todas las instancias. Los JSON solo guardan el nombre, nunca el valor.

## Credenciales
| Nombre | Tipo | La usa |
|---|---|---|
| `Tienda API` | Header Auth (`X-API-Key`) | todos los flujos que llaman a la app |
| `Correo salida` | se decide en T-002 | SUB Enviar notificación |
| `Correo entrada` | IMAP | T-008 |
| `Modelo IA` | se decide en T-008 | T-008, T-013 |

## Riesgos
- URL de test frente a producción: la app solo avisa a `/webhook/` con el flujo **publicado**; durante el desarrollo se prueba con `/webhook-test/`.
- Dos instancias con el mismo flujo publicado: solo una debe tenerlo activo.
