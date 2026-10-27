# Stacks y queues

## Qué son

Un **stack** sigue LIFO (*Last In, First Out*): el último elemento que entra es el primero en salir.

Una **queue** sigue FIFO (*First In, First Out*): el primer elemento que entra es el primero en salir.

Si añadimos A, B y C en ese orden:

- Un stack los devuelve como C, B, A.
- Una queue los devuelve como A, B, C.

## Operaciones

En un stack:

- `push` añade un elemento al tope.
- `pop` retira y devuelve el elemento del tope.

En una queue:

- `enqueue` añade un elemento al final.
- `dequeue` retira y devuelve el elemento del principio.

Estos son los nombres conceptuales de las operaciones. En Python podemos implementarlas con los métodos indicados en la siguiente tabla.

## Complejidad y supuestos

El coste depende de la implementación. Suponemos listas de CPython y una `collections.deque` sin límite de capacidad.

Aquí, n representa el número de elementos de la estructura.

| Estructura en Python | Operación | Coste |
|---|---|---|
| Stack con `list` | `push` mediante `append` | O(1) amortizado |
| Stack con `list` | `pop` del último elemento | O(1) amortizado |
| Queue con `collections.deque` | `enqueue` mediante `append` | O(1) |
| Queue con `collections.deque` | `dequeue` mediante `popleft` | O(1) |

Una lista de Python reserva espacio adicional. Cuando ese espacio se agota, una inserción puede requerir ampliar el almacenamiento y trasladar las referencias de los elementos, con coste O(n).

Al retirar elementos, también puede ser necesario reducir el almacenamiento.

O(1) amortizado significa que, al repartir el trabajo total entre muchas operaciones, el coste por operación es constante. No significa que cada operación individual cueste siempre O(1).

Usar `pop(0)` sobre una lista cuesta O(n), porque desplaza los elementos restantes una posición.

Una `deque` permite añadir al final y retirar del principio sin desplazar todos los elementos.

## Cuándo usarlos

Usamos un stack cuando necesitamos procesar primero lo más reciente.

Por ejemplo, el botón «atrás» de navegación puede apoyarse en un stack: la página anterior más reciente es la primera a la que volvemos.

Usamos una queue cuando necesitamos procesar por orden de llegada.

Por ejemplo, los trabajos de impresión pueden procesarse mediante una queue, suponiendo que no haya prioridades: el primero solicitado es el primero atendido.

## Límites

Estas estructuras organizan el orden de procesamiento; no ordenan los elementos por su valor.

Antes de retirar un elemento, hay que gestionar el caso de estructura vacía.

En Python, `list.pop()` y `deque.popleft()` lanzan `IndexError` si la estructura está vacía. Añadir un elemento a una estructura vacía sí es válido.

## Fuentes

- Documentación de `collections.deque`: https://docs.python.org/3/library/collections.html#collections.deque
- Complejidades de las estructuras de CPython: https://wiki.python.org/moin/TimeComplexity