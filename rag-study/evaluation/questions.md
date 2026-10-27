# Dataset de evaluación DSA — V1

## Objetivo

Comprobar si el sistema encuentra evidencia relevante y responde
correctamente usando el corpus.

Evaluaremos por separado:

- Recuperación: ¿encontró los fragmentos necesarios?
- Respuesta: ¿contestó correctamente y apoyándose en esos fragmentos?

Las respuestas pueden usar otras palabras. No exigimos una coincidencia
literal con la respuesta esperada.

Las rutas de los documentos son relativas a la carpeta rag-study.

## Q01 — Definición

Pregunta: ¿Qué significa que un stack sea LIFO?

Respuesta esperada:
El último elemento añadido es el primero en salir.

Documento fuente: corpus/stacks_queues.md
Secciones fuente: Qué son

Fragmentos de referencia:
- stacks_queues.md::0 — Qué son: definición de LIFO.

Evidencia necesaria:
La definición de LIFO.

Evidencia comprobada:
- La sección Qué son define LIFO como el último elemento que entra es el primero en salir.
- La sección Operaciones indica que push añade al tope y pop retira y devuelve el elemento del tope.

Criterio de respuesta correcta:
Explica que sale primero el último elemento añadido.
No confunde LIFO con FIFO.

Estado de la fuente:
El archivo existe; su contenido, formato Markdown y evidencia se han
comprobado directamente contra el documento fuente.

## Q02 — Comparación

Pregunta: ¿Cuándo conviene usar una queue frente a un stack?

Respuesta esperada:
Una queue conviene cuando necesitamos procesar por orden de llegada.
Por ejemplo, trabajos de impresión sin prioridades.
Un stack conviene cuando necesitamos procesar primero lo más reciente.
Por ejemplo, el botón «atrás» de navegación.

Documento fuente: corpus/stacks_queues.md
Secciones fuente: Cuándo usarlos

Fragmentos de referencia:
- stacks_queues.md::3 — Cuándo usarlos.

Evidencia necesaria:
El contraste entre procesar por orden de llegada y procesar primero lo más reciente, con un ejemplo de cada caso.

Evidencia comprobada:
- La sección Qué son contrasta LIFO y FIFO.
- La sección Cuándo usarlos relaciona un stack con el botón atrás de navegación y una queue con trabajos de impresión sin prioridades.

Criterio de respuesta correcta:
Relaciona la elección con el orden de procesamiento.
Los ejemplos respetan ese orden.

Estado de la fuente:
El archivo existe; su contenido, formato Markdown y evidencia se han
comprobado directamente contra el documento fuente.

## Q03 — Complejidad

Pregunta: ¿Cuál es la complejidad temporal de acceder por índice
a un array y a una linked list?

Respuesta esperada:
En un array con acceso directo, acceder por índice cuesta O(1).
En una linked list recorrida desde su primer nodo, cuesta O(n)
en el peor caso, porque hay que seguir los enlaces hasta la posición
solicitada.

Documentos fuente:
- corpus/arrays.md
- corpus/linked_lists.md

Secciones fuente:
Acceso por índice; Complejidad

Fragmentos de referencia:
- arrays.md::1 — Acceso por índice: explica el acceso directo sin recorrer los elementos anteriores.
- arrays.md::2 — Complejidad: establece el coste O(1).
- linked_lists.md::2 — Complejidad: establece O(n) en el peor caso y explica el recorrido.

Evidencia necesaria:
Una explicación del acceso directo en arrays y del recorrido de nodos
en linked lists.

Evidencia comprobada:
- En corpus/arrays.md, sección Complejidad: "Acceder a un índice válido cuesta O(1): el número de operaciones necesarias no crece con la cantidad de elementos del array."
- En corpus/linked_lists.md, sección Acceso por índice: "Para acceder a una posición, seguimos los enlaces desde la cabeza hasta llegar al nodo solicitado."
- En corpus/linked_lists.md, sección Complejidad: "Acceder por índice cuesta O(n) en el peor caso, siendo n el número de nodos: llegar al último requiere recorrer los anteriores."

Criterio de respuesta correcta:
Indica O(1) para el array y O(n) en el peor caso para la linked list.
Explica por qué sus costes son diferentes.

Estado de las fuentes:
Ambos archivos existen y su contenido y formato Markdown se han revisado.
La evidencia se ha comprobado manualmente contra los documentos fuente.
Se ha ejecutado una primera comparación de recuperación léxica,
registrada en retrieval_results.md. No se han evaluado respuestas generadas.

## Q04 — Ejercicio

Pregunta: Para comprobar si los paréntesis de una expresión están
balanceados, ¿qué estructura usaría y por qué?

Respuesta esperada:
Usaría un stack porque cada cierre corresponde a la apertura pendiente
más reciente.

Añadiría cada apertura al stack y retiraría una por cada cierre.
Si aparece un cierre con el stack vacío, la expresión no está balanceada.
Si quedan aperturas al terminar, tampoco está balanceada.

Alcance del ejercicio:
Se comprueban únicamente los paréntesis ( y ); se ignoran los demás
caracteres. La cadena vacía está balanceada.

Documento fuente: corpus/balanced_parentheses_exercise.md
Secciones fuente: Razonamiento

Fragmentos de referencia:
- balanced_parentheses_exercise.md::1 — Razonamiento.

Evidencia necesaria:
La justificación del uso de un stack, los pasos del algoritmo y las dos condiciones de error.

Evidencia comprobada:
- En la sección Razonamiento: "Usamos un stack porque cada cierre corresponde a la apertura pendiente más reciente: el orden LIFO permite retirarla primero."
- En la sección Ejemplos: (() deja una apertura pendiente y ()) contiene un cierre que aparece con el stack vacío.
- En la sección Enunciado: se ignoran los caracteres distintos de ( y ) y se considera balanceada la cadena vacía.

Criterio de respuesta correcta:
Justifica el uso de LIFO y explica las dos condiciones de error.

Estado de la fuente:
El archivo existe y su contenido y formato Markdown se han revisado.
La evidencia se ha comprobado manualmente contra el documento fuente.
Se ha ejecutado una primera comparación de recuperación léxica,
registrada en retrieval_results.md. No se han evaluado respuestas generadas.

## Q05 — Fuera de alcance

Pregunta: ¿Cómo implemento Dijkstra?

Respuesta esperada:
El corpus no contiene información suficiente para explicar una
implementación de Dijkstra. Grafos y Dijkstra quedan fuera del alcance
de esta versión.

Fragmentos de referencia: ninguno.

Documentos fuente: ninguno.
Evidencia relevante esperada: ninguna.

Criterio de respuesta correcta:
Reconoce la falta de evidencia en el corpus.
No presenta una implementación como si estuviera respaldada
por nuestros documentos.

Nota sobre recuperación:
El buscador podría devolver fragmentos por similitud.
Eso no significa que esos fragmentos permitan responder la pregunta.

## Estado del dataset

Estos cinco casos son un punto de partida, no una evaluación exhaustiva.

Se ha ejecutado una primera comparación de recuperación léxica el
27 de octubre de 2026. Sus resultados y límites están en retrieval_results.md.
Los cinco documentos del corpus inicial están redactados y revisados.
Q01, Q02, Q03 y Q04 tienen documentos fuente y evidencia comprobada
manualmente. Q05 es un caso fuera de alcance y no tiene fuente relevante.

La revisión documental por sí sola no mide la calidad del sistema.
La búsqueda por coincidencia de palabras está implementada en retrieval.py
y se han comparado tres preparaciones del texto, observando los tres
primeros resultados. Las referencias no son una lista exhaustiva de todos
los fragmentos útiles ni el único conjunto posible para responder.

Estas preguntas se están usando para desarrollo; la comparación no es una
validación independiente de generalización. No se ha implementado ni
evaluado la generación de respuestas y no hay un mecanismo de abstención.
