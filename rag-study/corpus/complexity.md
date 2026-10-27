# Complejidad

## Qué significa n

n representa el tamaño de la entrada o de la estructura que analizamos. Hay que indicar qué estamos contando.

- En un array, n puede ser su número de elementos.
- En una linked list, n puede ser su número de nodos.
- En el ejercicio de paréntesis, n es el número de caracteres del texto, incluidos los que se ignoran.

Para estos análisis suponemos que las operaciones básicas sobre elementos y referencias tienen coste constante.

## Qué describe Big O

Big O expresa una cota del crecimiento del coste al aumentar n. Podemos analizar el trabajo necesario o el espacio adicional utilizado.

No expresa un tiempo exacto en segundos. Para comparar tiempos reales necesitamos medir con entradas y condiciones concretas.

## O(1) y O(n)

O(1) significa que el coste está acotado por una constante independiente de n. No significa que se haga exactamente una operación.

Por ejemplo, un algoritmo que siempre realiza 100 operaciones tiene coste O(1).

Un recorrido que realiza una operación por cada uno de los n elementos tiene coste O(n): su trabajo crece linealmente con la cantidad de elementos.

| Cantidad de datos | A: siempre 100 operaciones, O(1) | B: una operación por dato, O(n) |
|---|---|---|
| 3 | 100 operaciones | 3 operaciones |
| 1.000 | 100 operaciones | 1.000 operaciones |

En este ejemplo, suponiendo operaciones de coste similar, B hace menos trabajo con 3 datos y A hace menos trabajo con 1.000 datos.

O(1) no garantiza ser más rápido que O(n) para cualquier tamaño de entrada. También importan las constantes y la implementación. Estas cantidades son un ejemplo didáctico, no resultados de una medición.

## Tiempo y espacio

La complejidad temporal describe el crecimiento del trabajo necesario.

La complejidad espacial describe el crecimiento de la memoria utilizada. En este corpus indicamos el espacio adicional, sin contar el almacenamiento del texto de entrada, cuando analizamos el ejercicio de paréntesis.

El ejercicio recorre el texto una vez: su tiempo es O(n) en el peor caso. Su stack puede acumular hasta n aperturas pendientes: su espacio adicional es O(n) en el peor caso.

Las complejidades de tiempo y espacio deben justificarse por separado.

## Peor caso y coste amortizado

El peor caso considera la entrada más costosa entre las del mismo tamaño.

En una linked list recorrida desde la cabeza, acceder al primer nodo cuesta O(1), pero llegar al último requiere recorrer los anteriores: O(n) en el peor caso.

El análisis amortizado reparte el trabajo total de una secuencia de operaciones entre ellas. No garantiza que cada operación individual tenga ese coste.

En una lista de CPython, append tiene coste O(1) amortizado. Muchas inserciones aprovechan el espacio reservado; algunas requieren ampliar el almacenamiento, con coste O(n).

El coste amortizado no es un promedio estadístico sobre entradas aleatorias.

## Supuestos y fuentes

Los costes dependen de la operación y de la implementación. Un nombre como stack o queue no basta para determinar el coste.

Los ejemplos concretos del corpus se desarrollan en:

- [Arrays](arrays.md).
- [Linked lists](linked_lists.md).
- [Stacks y queues](stacks_queues.md).
- [Paréntesis balanceados](balanced_parentheses_exercise.md).

Referencia para las operaciones de listas de CPython: [TimeComplexity, Python Wiki](https://wiki.python.org/moin/TimeComplexity).
