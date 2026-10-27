# Arrays

## Qué son

Un array almacena elementos en posiciones consecutivas de memoria.

En este apunte suponemos elementos de tamaño fijo y acceso directo
por índice.

## Acceso por índice

Podemos calcular la dirección de un elemento mediante:

dirección = dirección inicial + índice × tamaño de cada elemento

Por eso no necesitamos recorrer los elementos anteriores.

## Complejidad

Acceder a un índice válido cuesta O(1): el número de operaciones
necesarias no crece con la cantidad de elementos del array.