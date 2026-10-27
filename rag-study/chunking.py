from pathlib import Path

from ingest import load_document


def make_chunk(
    source: str, section: str, section_lines: list[str], index: int
) -> dict[str, str]:
    return {
        "chunk_id": f"{source}::{index}",
        "source": source,
        "section": section,
        "text": "\n".join(section_lines).strip("\n"),
    }


def chunk_document(document: dict[str, str]) -> list[dict[str, str]]:
    """Divide las secciones ## del corpus actual; omite el título principal."""
    chunks = []
    section = None
    section_lines = []

    for line in document["text"].splitlines():
        if line.startswith("## "):
            # Guardamos el apartado anterior antes de empezar el nuevo.
            if section is not None:
                chunk = make_chunk(
                    document["source"], section, section_lines, len(chunks)
                )
                chunks.append(chunk)

            section = line[3:].strip()
            section_lines = [line]
        elif section is not None:
            section_lines.append(line)

    # El último apartado no tiene otro título después que active su guardado.
    if section is not None:
        chunk = make_chunk(document["source"], section, section_lines, len(chunks))
        chunks.append(chunk)

    return chunks

def chunk_corpus(documents: list[dict[str, str]]) -> list[dict[str, str]]:
    all_chunks = []

    for document in documents:
        document_chunks = chunk_document(document)
        all_chunks.extend(document_chunks)

    return all_chunks



if __name__ == "__main__":
    path = Path(__file__).resolve().parent / "corpus" / "arrays.md"
    chunks = chunk_document(load_document(path))

    print(f"Fragmentos de {path.name}: {len(chunks)}")
    for chunk in chunks:
        print(f"\n{chunk['chunk_id']} | {chunk['source']} | {chunk['section']}")
        print(chunk["text"])
