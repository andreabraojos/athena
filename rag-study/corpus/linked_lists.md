# Linked lists

## Qué son

Una linked list está formada por nodos.

Cada nodo contiene un dato y una referencia al siguiente nodo.
Los nodos no tienen que ocupar posiciones consecutivas de memoria.

En este apunte suponemos una lista simplemente enlazada y que
empezamos desde su primer nodo, llamado cabeza.

## Acceso por índice

Para acceder a una posición, seguimos los enlaces desde la cabeza
hasta llegar al nodo solicitado.

No podemos calcular su dirección mediante la fórmula de un array,
porque los nodos pueden estar repartidos por la memoria.

## Complejidad

Acceder por índice cuesta O(n) en el peor caso, siendo n el número
de nodos: llegar al último requiere recorrer los anteriores.

Acceder al primer nodo cuesta O(1), porque ya tenemos su referencia.