## Decisiones
1. **Se validan las reglas de la app antes de enviar** (abono inicial >= 5 €, producto con stock).
2. **Solicitud dudosa o incompleta: no se crea** y se avisa a Marisa.
3. **Evitar duplicados**: misma persona, producto y día.
   - **Cómo queda (2026-10-26, Anna):** canal: formulario de n8n. La app exige un abono inicial de 5 € para crear un apartado y cobrarlo queda fuera, así que se separa en dos pasos: la solicitud se guarda como `pendiente` en la tabla de n8n `solicitudes_apartado` (sin tocar la app) y el apartado se crea cuando Marisa confirma, en un formulario protegido, que el cliente ha pagado el abono. "Producto con stock" no se valida: la app no tiene stock.


4. **Formulario publico sin freno:** no hay limite de envios ni captcha, y se guardan nombre y telefono sin aviso de privacidad. Queda vinculado con T-020 (proteccion de datos) para anadir aviso de privacidad y medidas anti-abuso.
5. **Limite conocido (fallo entre pasos):** si "Crear apartado" tiene exito pero "Marcar como confirmada" falla, una segunda confirmacion podria crear otro apartado. Se acepta como limite del diseno: no hay transaccion distribuida entre la app y la tabla de n8n.
