## 1. Preparación
- [ ] 1.1 Comprobar qué modelos gratuitos están disponibles y elegir dos
- [ ] 1.2 Fijar el prompt de T-008 y los 9 correos
- [ ] 1.3 Crear la tabla vacía con las métricas

## 2. Ejecución
- [ ] 2.1 Pasar los 9 correos por el modelo A y anotar resultados y tiempos
- [ ] 2.2 Pasar los 9 correos por el modelo B y anotar resultados y tiempos

## 3. Análisis
- [ ] 3.1 Rellenar la tabla de acierto, JSON válido y latencia
- [ ] 3.2 Escribir la conclusión y el modelo elegido

## 4. Entrega
- [ ] 4.1 Añadir la tabla al README y los detalles a `docs/ai-log.md`
- [ ] 4.2 No guardar claves en ningún archivo

## 5. Cierre del change (obligatorio al terminar)
- [ ] 5.1 Validar: `openspec validate t-013-comparativa-modelos --strict`
- [ ] 5.2 Archivar con `/opsx:archive` (OpenCode: `/opsx-archive`) o `openspec archive t-013-comparativa-modelos`. Mueve el change a `openspec/changes/archive/` y **pasa los "ADDED Requirements" a `openspec/specs/`**, la fuente de verdad del comportamiento actual.
- [ ] 5.3 Incluir el archivo en la misma PR y cerrar el ticket (`Closes #N`)
