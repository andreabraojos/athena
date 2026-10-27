# Experimentos de recuperación léxica — 27 de octubre de 2026

## Alcance y protocolo

Comparamos tres formas de preparar las palabras para el mismo buscador.
Se mantuvieron las cinco preguntas de `questions.md`, sus referencias,
los cinco documentos, sus 23 fragmentos y la regla de puntuación.

La puntuación suma uno por cada palabra de la pregunta que aparece en el
fragmento. Una palabra repetida en la pregunta puede sumar varias veces;
repetirla en el fragmento no añade puntos. No se compara su posición.
La misma preparación se aplica a preguntas y fragmentos.

`retrieve` devuelve los 23 resultados ordenados de mayor a menor
puntuación. Los empates conservan el orden original: documentos por nombre
y secciones según su posición. Para esta comparación observamos solo los
tres primeros resultados; no se añadió un filtro a `retrieve`.

La medida es cuántas referencias seleccionadas aparecen entre esos tres
resultados. Las referencias no son una lista exhaustiva de todos los
fragmentos útiles ni el único conjunto posible para responder. Esta
medida no determina por sí sola si se podría producir una respuesta correcta.

## Variantes

- V0: minúsculas y separación por espacios, `text.lower().split()`.
- V1: minúsculas y extracción con `re.findall(r"\w+", text.lower())`.
  Se conservan letras acentuadas, números y guiones bajos; los demás
  caracteres actúan como separadores. No son tokens de un modelo.
- V2: V1 seguida de un filtro que excluye estas palabras:
  `de`, `el`, `la`, `los`, `las`, `un`, `una`, `y`, `a`, `en`, `por`,
  `para`, `que`, `qué`, `es`.

V1 se probó después de observar problemas de signos y Markdown en V0.
V2 se probó después de observar coincidencias de palabras frecuentes en V1.
En cada paso cambió únicamente la preparación de palabras; no se cambiaron
las preguntas ni las referencias. Son experimentos de desarrollo sobre
estos cinco casos, no una validación independiente de generalización.

## Resultados observados

Cada fracción indica referencias recuperadas entre los tres primeros
resultados / referencias seleccionadas para el caso.

| Caso | V0: espacios | V1: expresión regular | V2: expresión regular y filtro |
|---|---:|---:|---:|
| Q01 — LIFO | 0/1 | 1/1 | 0/1 |
| Q02 — Queue frente a stack | 1/1 | 1/1 | 1/1 |
| Q03 — Array y linked list | 1/3 | 1/3 | 1/3 |
| Q04 — Paréntesis | 1/1 | 0/1 | 0/1 |
| Casos con todas sus referencias, Q01–Q04 | 2/4 | 2/4 | 1/4 |

Q05 no tiene referencias relevantes y no se incluye en esas fracciones.
En las tres variantes se devolvieron 23 resultados con puntuación cero.
Los tres primeros fueron `arrays.md::0`, `arrays.md::1` y `arrays.md::2`
por el desempate basado en el orden original, no por aportar evidencia.
No hay un mecanismo de abstención y no se generaron respuestas.

Posiciones de las referencias en la lista completa, contando desde uno:

| Caso y referencia | V0 | V1 | V2 |
|---|---:|---:|---:|
| Q01 — `stacks_queues.md::0` | 5 | 1 | 4 |
| Q02 — `stacks_queues.md::3` | 1 | 1 | 2 |
| Q03 — `arrays.md::1` | 14 | 15 | 10 |
| Q03 — `arrays.md::2` | 3 | 3 | 1 |
| Q03 — `linked_lists.md::2` | 16 | 18 | 5 |
| Q04 — `balanced_parentheses_exercise.md::1` | 3 | 5 | 6 |

## Decisión y límites

Conservamos V1, sin el filtro de palabras frecuentes, como versión
provisional. V2 empeoró la cobertura completa de referencias de 2/4 a 1/4.
V1 corrigió el caso de LIFO, pero perdió la referencia de Q04 entre los tres
primeros; no mejoró la cobertura completa global respecto a V0.

La restauración de V1 se ejecutó de nuevo y reprodujo sus resultados.
Las variantes de control se reconstruyeron en memoria sin modificar los
archivos del buscador. Las comprobaciones y la evaluación se ejecutaron
durante la sesión; todavía no hay un evaluador persistente ni pruebas de
recuperación guardadas. Las tres pruebas persistentes de fragmentación
pasaron, pero no miden la calidad de la búsqueda.

No se han evaluado generación de respuestas, latencia ni coste. No hay
embeddings ni integración con Athena. Antes de más cambios, el siguiente
paso es guardar pruebas de recuperación y un evaluador reproducible.
