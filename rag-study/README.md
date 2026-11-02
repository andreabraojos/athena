# RAG de estudio DSA

## Estado actual

El corpus inicial contiene cinco apuntes Markdown y la ingesta mínima está implementada en `ingest.py`.

Las cinco preguntas y sus respuestas esperadas están en `evaluation/questions.md`. Q01–Q04 tienen evidencia documental revisada; Q05 está fuera de alcance.

La primera fragmentación por secciones está implementada en `chunking.py`. La búsqueda por coincidencia de palabras está implementada en `retrieval.py`. Todavía no hay embeddings ni generación de respuestas, y este módulo no está integrado con Athena.

Se han comparado tres preparaciones de palabras sobre las cinco preguntas. Los resultados y sus límites están en [el informe de recuperación](evaluation/retrieval_results.md). Es una evaluación inicial de búsqueda, no de respuestas generadas ni de un sistema RAG completo.

## Ejecutar la ingesta

Desde la carpeta del proyecto Athena, con Python 3.9 o posterior:

```powershell
python rag-study/ingest.py
```

Solo se utiliza la biblioteca estándar. También puede ejecutarse indicando la ruta absoluta del script desde otra carpeta, porque la ubicación del corpus se calcula respecto a `ingest.py`.

La salida muestra la cantidad de documentos y, para cada uno, su nombre y la longitud del texto. Con el corpus actual deben aparecer cinco documentos, ordenados por nombre:

```text
arrays.md
balanced_parentheses_exercise.md
complexity.md
linked_lists.md
stacks_queues.md
```

## Contrato y decisiones

- `load_document(path)` recibe la ruta de un archivo y devuelve un diccionario con `source` y `text`.
- `load_corpus(corpus_dir)` recibe una carpeta y devuelve una lista de esos diccionarios.
- Se leen únicamente los archivos `*.md` directamente dentro de `corpus`, sin recorrer subcarpetas.
- El orden de carga es estable: las rutas se ordenan antes de leerlas.
- Se usa UTF-8 y los errores de lectura o codificación se propagan, sin omitir archivos silenciosamente.
- `source` es el nombre del archivo; el corpus actual es plano y sus nombres son únicos.
- El lector de texto de Python unifica los saltos de línea habituales. Conservamos el resto del contenido, incluidos espacios y párrafos; no añadimos una limpieza que no responde a un problema observado.
- `evaluation/questions.md` permanece fuera del corpus: sus respuestas esperadas sirven para corregir, no como fuente para el buscador.
- El módulo se mantiene dentro de `rag-study`; no se ha integrado con Athena.

## Comprobaciones realizadas

Se ha comprobado la lectura real de los cinco apuntes, la estructura `source`/`text`, la igualdad con el contenido leído en UTF-8 y la estabilidad del resultado en dos cargas consecutivas. La lista cargada no contiene `questions.md`.

Las comprobaciones de ingesta se ejecutaron durante la sesión; todavía no tienen una batería de pruebas persistente. Las pruebas persistentes de fragmentación se describen a continuación. La comparación inicial de recuperación está registrada en `evaluation/retrieval_results.md`; no hay métricas de respuestas generadas.

## Primera fragmentación por secciones

Elegimos secciones para conservar juntas las explicaciones técnicas del corpus. Es una baseline de diseño, no una mejora de recuperación demostrada. Los tamaños pueden variar y una sección puede depender de otra.

`chunk_document(document)` recibe un documento de la ingesta y devuelve una lista de fragmentos. Cada fragmento tiene:

- `chunk_id`: nombre del archivo y posición del fragmento desde cero, por ejemplo `arrays.md::2`.
- `source`: nombre del archivo original.
- `section`: título del apartado, sin el prefijo `## `.
- `text`: encabezado `##` y contenido del apartado, conservando los párrafos interiores.

`chunk_corpus(documents)` aplica esa función a cada documento y reúne sus fragmentos en una única lista plana mediante `extend`. Conserva el orden de los documentos y las secciones.

Cada línea que empieza exactamente por `## ` abre una sección. El título principal `#` y las líneas anteriores a la primera sección no forman fragmentos. En el corpus actual ese preámbulo solo contiene el título principal y líneas vacías. Los saltos de línea exteriores de cada fragmento se retiran; se conservan los espacios y párrafos interiores.

`section_lines` es el borrador de la sección actual; `chunks` acumula los fragmentos terminados. Guardamos el borrador antes de cada título nuevo y una vez más al acabar el documento.

Los identificadores son reproducibles para el mismo archivo y orden de secciones. Pueden cambiar si se inserta o reordena una sección. Dos apartados con el mismo título se distinguen por su posición.

Esta versión asume el Markdown sencillo de nuestros apuntes: no interpreta bloques de código para distinguir títulos reales de líneas que parezcan títulos dentro de ellos. No limita el tamaño ni añade solapamiento entre secciones.

## Ejemplo y pruebas reproducibles

Desde la carpeta del proyecto Athena:

```powershell
python -X utf8 rag-study/chunking.py
python -X utf8 -m unittest discover -s rag-study -p test_chunking.py -v
```

El ejemplo carga solo `arrays.md` y muestra tres fragmentos: Qué son, Acceso por índice y Complejidad, con su origen y texto. Las tres pruebas comprueban ese documento real, la reunión plana de fragmentos de dos documentos conservando su origen y un ejemplo con títulos repetidos y sin salto de línea final, para verificar que la última sección no se pierde.

Se trata de pruebas de fragmentación: por sí solas no miden si el buscador recupera los fragmentos necesarios ni si un modelo responde correctamente. La comparación de recuperación se realizó por separado y está registrada en `evaluation/retrieval_results.md`.

## Inspección del corpus completo — 19 de octubre de 2026

Para reproducir el informe desde la carpeta del proyecto Athena:

```powershell
python -X utf8 rag-study/inspect_chunks.py
```

La inspección carga exclusivamente `corpus`, verifica identificadores únicos, representación de todos los documentos y que cada texto de fragmento aparezca en su archivo de origen. También rechaza cargar el dataset conocido `questions.md` como documento del corpus.

El tamaño es `len(chunk["text"].split())`: un conteo aproximado de palabras por espacios que incluye encabezados y símbolos Markdown. No son tokens de un modelo.

Resultado observado con los cinco documentos actuales: 23 fragmentos.

| Documento | Fragmentos | Mínimo | Máximo |
|---|---:|---:|---:|
| arrays.md | 3 | 23 | 31 |
| balanced_parentheses_exercise.md | 5 | 25 | 152 |
| complexity.md | 6 | 45 | 153 |
| linked_lists.md | 3 | 35 | 48 |
| stacks_queues.md | 6 | 15 | 183 |

El menor es `stacks_queues.md::5`, Fuentes, con 15 palabras aproximadas. El mayor es `stacks_queues.md::2`, Complejidad y supuestos, con 183.

Observación manual para Q01: el fragmento Fuentes solo contiene enlaces; no contiene la definición de LIFO ni evidencia suficiente para explicarla. También se conserva en los experimentos posteriores de búsqueda; no se ha probado una variante que lo excluya.

El informe comprueba propiedades mecánicas del corpus fragmentado; no demuestra la calidad de la recuperación o de las respuestas. Las cifras son una instantánea y deben recalcularse si cambian los documentos.

## Búsqueda léxica y primera comparación — 27 de octubre de 2026

En `retrieval.py`:

- `tokenize` pasa el texto a minúsculas y extrae grupos con `re.findall(r"\w+", ...)`, conservando letras acentuadas, números y guiones bajos.
- `score_overlap` suma uno por cada palabra de la pregunta presente en el fragmento. Las repeticiones de la pregunta pueden sumar varias veces.
- `score_chunks` devuelve una lista de diccionarios con `chunk_id` y `score`. Conserva un `print` de diagnóstico para cada fragmento.
- `get_score` obtiene la puntuación de un resultado.
- `retrieve` ordena todos los resultados de mayor a menor puntuación mediante `sorted`. No descarta puntuaciones cero ni limita su cantidad. Los empates conservan el orden original.

Para comparar las variantes observamos los tres primeros resultados de cada pregunta, sin modificar sus referencias ni el corpus. La versión con espacios cubrió todas las referencias seleccionadas en 2/4 casos con respuesta; la expresión regular también en 2/4, pero con ganancias y pérdidas en casos distintos; añadir un filtro de palabras frecuentes redujo ese resultado a 1/4. Se retiró el filtro y se comprobó la restauración de la versión con expresión regular.

No son porcentajes de respuestas correctas ni una medida exhaustiva de relevancia. Q05 queda fuera de ese denominador: en todas las variantes devolvió 23 resultados con puntuación cero. No hay abstención ni generación de respuestas.

Las mediciones se ejecutaron durante la sesión del 27 de octubre y el detalle está en [el informe de recuperación](evaluation/retrieval_results.md). Las cinco preguntas se están usando para desarrollo, no como validación independiente. Las primeras pruebas guardadas del buscador se añadieron el 2 de noviembre, como se describe a continuación; el evaluador persistente de las cinco preguntas sigue pendiente.

## Pruebas del buscador — 2 de noviembre de 2026

`test_retrieval.py` contiene tres pruebas con `unittest`:

- `tokenize` convierte a minúsculas y separa los signos de puntuación y Markdown del ejemplo `¿Un **STACK** sigue LIFO?`.
- `score_overlap` cuenta las dos coincidencias aunque las palabras estén en posiciones distintas.
- `retrieve` devuelve los identificadores y puntuaciones en orden descendente, conservando también el resultado de puntuación cero del ejemplo.

Cada prueba compara `actual`, el valor devuelto por la función, con `expected`, el resultado calculado de antemano para el caso. `self.assertEqual(actual, expected)` falla si ambos valores son distintos. Una diferencia obliga a revisar el código y la expectativa; no justifica cambiar esta última únicamente para que la prueba pase.

Para ejecutar todas las pruebas de `rag-study`, desde la carpeta del proyecto Athena:

```powershell
python -X utf8 -B -m unittest discover -s rag-study -p "test_*.py" -v
```

Resultado comprobado el 2 de noviembre: seis pruebas pasan, tres de fragmentación y tres del buscador. El comando también se ejecutó desde la terminal de trabajo y devolvió `Ran 6 tests` y `OK`. Las líneas `example.md::0 0` y `example.md::1 2` proceden del `print` de diagnóstico en `score_chunks`, antes de ordenar; la prueba comprueba la lista devuelta después de ordenar.

Como comprobación adicional durante la sesión, se simularon en memoria versiones que dejan signos pegados, comparan palabras solo en la misma posición o no ordenan los resultados. Las pruebas correspondientes detectaron esos fallos, sin modificar el código del buscador.

Estas tres pruebas no cubren todos los casos límite ni miden la calidad de la recuperación de las cinco preguntas. El siguiente bloque es guardar un evaluador reproducible, sin cambiar todavía la búsqueda ni sus referencias.
