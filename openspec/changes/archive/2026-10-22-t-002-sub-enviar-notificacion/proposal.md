# T-002 · SUB · Enviar notificación

**Historia:** HU-01 y HU-02 · **Responsable:** Charlotte (`Charlottedoulcet`) · **Tamaño:** M · **Fecha límite:** 2026-10-22
**Depende de:** T-001

## Por qué
Casi todos los flujos terminan enviando un mensaje (a la clienta o a Marisa). Si cada flujo montara su envío, repetiríamos nodos y cada mensaje fallaría de forma distinta cuando falta el correo. Un sub-workflow único da un solo punto donde se envía, se controla el fallo y se avisa a la tienda.

## Qué cambia
- Sub-workflow `SUB - Enviar notificación` con un contrato de entrada y salida fijo (ver diseño).
- Si el cliente no tiene correo, no falla: avisa a la tienda.
- Credencial `Correo salida` y variable con el correo de la tienda.

## Fuera de alcance
- El texto concreto de cada mensaje (lo escribe cada flujo).
- Otros canales (Telegram, WhatsApp): ver T-016 y T-017.

## Impacto
Desbloquea T-004, T-005, T-006, T-007, T-008, T-009, T-010 y T-011. Los demás pueden construir sus flujos llamándolo aunque aún no esté terminado (contrato fijado aquí).
