# Paréntesis balanceados

## Enunciado

Dado un texto, decidir si sus paréntesis de apertura `(` y cierre `)` están balanceados.

Ignoramos los caracteres que no sean `(` o `)`. La cadena vacía está balanceada porque no hay aperturas ni cierres pendientes.

El resultado indica si los paréntesis están balanceados. Este ejercicio no comprueba la validez matemática del texto ni otros tipos de delimitadores.

## Razonamiento

Usamos un stack porque cada cierre corresponde a la apertura pendiente más reciente: el orden LIFO permite retirarla primero.

1. Empezamos con un stack vacío.
2. Al encontrar `(`, añadimos una apertura al stack.
3. Al encontrar `)`, comprobamos si el stack está vacío. Si está vacío, hay un cierre sin apertura correspondiente y el texto no está balanceado. Si hay una apertura, la retiramos.
4. Ignoramos los demás caracteres.
5. Si quedan aperturas en el stack al terminar, falta algún cierre y el texto no está balanceado. Si no quedan aperturas y no apareció un cierre sin apertura, está balanceado.

Comprobamos que el stack no esté vacío antes de retirar un elemento. Un cierre sin apertura es un caso inválido del ejercicio, no una razón para provocar una excepción de Python.

No basta con contar el mismo número de aperturas y cierres: también importa el orden, como muestra `)(`.

## Ejemplos

| Texto | ¿Balanceado? | Motivo |
|---|---|---|
| `""` (cadena vacía) | Sí | No hay aperturas ni cierres pendientes. |
| `abc` | Sí | Se ignoran las letras; no hay paréntesis pendientes. |
| `()` | Sí | El cierre corresponde a la apertura anterior. |
| `(())` | Sí | Se cierra primero la apertura más reciente. |
| `()()` | Sí | Ambos pares quedan cerrados. |
| `a + (b * c)` | Sí | Se ignoran los demás caracteres y el par queda cerrado. |
| `(()` | No | Queda una apertura sin cierre al terminar. |
| `())` | No | El último cierre aparece con el stack vacío. |
| `)(` | No | El primer cierre no tiene una apertura pendiente. |

## Complejidad

Sea n el número de caracteres del texto. Recorremos el texto una sola vez y cada apertura se añade y retira como máximo una vez.

Con las operaciones de stack descritas en `stacks_queues.md`, el tiempo total es O(n) en el peor caso, usando el coste amortizado de las operaciones si el stack se implementa con una lista de CPython.

El espacio adicional es O(n) en el peor caso: el stack puede acumular tantas aperturas pendientes como caracteres haya en el texto. La longitud del texto no mide solo los paréntesis; también contamos los caracteres que se examinan y se ignoran.

## Fuente conceptual

Este es un ejercicio didáctico original del corpus. Las definiciones de stack, LIFO y sus operaciones se explican en [Stacks y queues](stacks_queues.md).
