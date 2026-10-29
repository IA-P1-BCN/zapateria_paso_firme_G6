# identidad-visual Specification

## Purpose
Aspecto común de zapatería de barrio (papel kraft, cuero, costuras) en todo lo que ven Marisa y sus clientes: la web de la tienda, el panel de Marisa y los formularios de apartado. Solo cambia el aspecto, nunca el comportamiento ni los datos.

## Requirements

### Requirement: Identidad visual común
La web de la tienda, el panel de Marisa y los formularios de apartado SHALL usar la misma paleta y tipografía de zapatería de barrio.

#### Scenario: Mismas señas en todas partes
- **WHEN** se abren la web de la tienda, el panel de Marisa y un formulario de apartado
- **THEN** los tres usan los mismos colores de fondo, primario y acento y la misma letra en los títulos

### Requirement: Solo cambia el aspecto
El cambio de diseño SHALL NOT modificar el HTML, el JavaScript ni el comportamiento de la web de la tienda, ni los datos que leen o escriben los flujos.

#### Scenario: La web funciona igual
- **WHEN** se crea un apartado, se registra un abono y se descarga el Excel con el nuevo diseño
- **THEN** el resultado es el mismo que antes del cambio

### Requirement: Legible
Los textos SHALL tener un contraste de al menos 4,5:1 con su fondo, en modo claro y en modo oscuro.

#### Scenario: Contraste comprobado
- **WHEN** se comprueba el contraste de cada pareja de colores de texto y fondo
- **THEN** todas llegan al menos a 4,5:1
