## 1. Preparación
- [x] 1.1 Elegir proveedor y dominio

## 2. Despliegue
- [ ] 2.1 Docker Compose en el servidor con HTTPS
- [ ] 2.2 Variables y credenciales en el servidor
- [ ] 2.3 Copias de seguridad

## 3. CI
- [x] 3.1 Acción de GitHub que valida los JSON y busca claves

## 4. Entrega
- [x] 4.1 Anotar en la sección propia de `docs/ai-log.md`

## 5. Cierre del change (obligatorio al terminar)
- [ ] 5.1 Validar: `openspec validate t-022-despliegue-cloud --strict`
- [ ] 5.2 Archivar con `/opsx:archive` (OpenCode: `/opsx-archive`) o `openspec archive t-022-despliegue-cloud`. Mueve el change a `openspec/changes/archive/` y **pasa los "ADDED Requirements" a `openspec/specs/`**, la fuente de verdad del comportamiento actual.
- [ ] 5.3 Incluir el archivo en la misma PR y cerrar el ticket (`Closes #N`)
