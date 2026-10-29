## 1. Identidad
- [x] 1.1 Paleta y tipografía (modo claro y oscuro) con contraste AA comprobado

## 2. Web de la tienda
- [x] 2.1 Nueva hoja `frontend/css/styles.css` (solo estilos; HTML y JavaScript sin cambios)
- [x] 2.2 Probar las cuatro páginas en local (apartados, ficha, nuevo apartado, ventas) en móvil y escritorio

## 3. n8n
- [x] 3.1 Panel de Marisa (T-021) con la nueva paleta
- [x] 3.2 Formularios de solicitud y confirmación de apartado (T-018) con *Custom Form Styling*
- [x] 3.3 Correos: no aplica (texto plano desde `SUB - Enviar notificación`); paleta documentada
- [x] 3.4 Exportar los flujos cambiados a `workflows/` y pasar `validar_flujos.py`

## 4. Documentación
- [x] 4.1 Cabecera del README y paleta documentada para el resto del equipo
- [x] 4.2 Anotar en la sección propia de `docs/ai-log.md`

## 5. Cierre del change (obligatorio al terminar)
- [x] 5.1 Validar: `openspec validate t-023-diseno-zapateria-barrio --strict`
- [x] 5.2 Archivar con `/opsx:archive` (OpenCode: `/opsx-archive`) o `openspec archive t-023-diseno-zapateria-barrio`. Mueve el change a `openspec/changes/archive/` y **pasa los "ADDED Requirements" a `openspec/specs/`**, la fuente de verdad del comportamiento actual.
- [ ] 5.3 Incluir el archivo en la misma PR y cerrar el ticket (`Closes #67`)
