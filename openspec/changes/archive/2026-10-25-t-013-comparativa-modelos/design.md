## Decisiones
1. **Misma tarea, mismo prompt, mismos 9 correos** para los dos modelos, para que la comparación sea justa.
2. **Candidatos** (gratuitos de OpenCode, a confirmar disponibilidad): `opencode/deepseek-v4.1-flash-free`, `nemotron-3-ultra-free`, `mimo-v2.6-flash-free`.
   - **Decidido (2026-10-25, Anna):** se comparan dos modelos gratuitos de Groq, `openai/gpt-oss-20b` (el que usaba el flujo 03) y `qwen/qwen3.8-27b`, porque el flujo 03 ya usa la credencial de Groq y así la comparación pasa por la misma API.
3. **Métricas:** campos correctos (ordenante, importe, concepto), formato JSON válido, tiempo de respuesta, y qué datos se envían al modelo.
4. **Datos enviados:** se documenta si el modelo recibe el correo entero o solo el texto necesario; son datos de prueba ficticios.
5. **Se elige un modelo y se justifica**, aunque la diferencia sea pequeña.
