from pathlib import Path


def load_document(path: Path) -> dict[str, str]:
    source = path.name
    text = path.read_text(encoding="utf-8")

    diccionario = {"source": source, "text": text}

    return diccionario

def load_corpus(corpus_dir: Path) -> list[dict[str, str]]:
    paths = sorted(corpus_dir.glob("*.md"))
    documents = []

    for path in paths:
        document = load_document(path)
        documents.append(document)

    return documents


if __name__ == "__main__":
    corpus_dir = Path(__file__).resolve().parent / "corpus"
    documents = load_corpus(corpus_dir)

    print(f"Documentos cargados: {len(documents)}")
    for document in documents:
        print(f"{document['source']}: {len(document['text'])} caracteres")
