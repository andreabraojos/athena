from pathlib import Path

from chunking import chunk_corpus
from ingest import load_corpus


def count_words(chunk: dict[str, str]) -> int:
    """Conteo aproximado por espacios; no cuenta tokens de un modelo."""
    return len(chunk["text"].split())


def inspect_corpus(corpus_dir: Path) -> None:
    documents = load_corpus(corpus_dir)
    chunks = chunk_corpus(documents)
    if not documents or not chunks:
        raise ValueError("Se necesitan documentos y fragmentos para inspeccionar.")

    source_texts = {document["source"]: document["text"] for document in documents}
    if "questions.md" in source_texts:
        raise ValueError("El dataset de evaluación debe quedar fuera del corpus.")
    if {chunk["source"] for chunk in chunks} != set(source_texts):
        raise ValueError("Los fragmentos no representan todos los documentos cargados.")
    ids = [chunk["chunk_id"] for chunk in chunks]
    if len(ids) != len(set(ids)):
        raise ValueError("Hay identificadores de fragmento repetidos.")
    for chunk in chunks:
        if chunk["text"] not in source_texts[chunk["source"]]:
            raise ValueError(f"El texto no coincide con su origen: {chunk['chunk_id']}")

    print(f"Documentos: {len(documents)} | Fragmentos: {len(chunks)}")
    print("Identificadores, representación de documentos y texto de origen: OK")
    print("Tamaños: palabras aproximadas por espacios, incluidos títulos y Markdown.")
    print("Documento | Fragmentos | Mínimo | Máximo")
    for document in documents:
        sizes = [
            count_words(chunk)
            for chunk in chunks
            if chunk["source"] == document["source"]
        ]
        print(f"{document['source']} | {len(sizes)} | {min(sizes)} | {max(sizes)}")

    smallest = min(chunks, key=count_words)
    largest = max(chunks, key=count_words)
    print(
        f"Menor: {smallest['chunk_id']} | {smallest['section']} | "
        f"{count_words(smallest)} palabras"
    )
    print(
        f"Mayor: {largest['chunk_id']} | {largest['section']} | "
        f"{count_words(largest)} palabras"
    )
    print("Esta inspección no mide recuperación ni calidad de respuestas.")


if __name__ == "__main__":
    inspect_corpus(Path(__file__).resolve().parent / "corpus")
