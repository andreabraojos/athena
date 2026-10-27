import unittest
from pathlib import Path

from chunking import chunk_corpus, chunk_document
from ingest import load_document


class ChunkingTests(unittest.TestCase):
    def test_arrays_sections_match_the_real_document(self):
        path = Path(__file__).resolve().parent / "corpus" / "arrays.md"
        document = load_document(path)
        chunks = chunk_document(document)

        self.assertEqual(
            [chunk["section"] for chunk in chunks],
            ["Qué son", "Acceso por índice", "Complejidad"],
        )
        self.assertEqual(
            [chunk["chunk_id"] for chunk in chunks],
            ["arrays.md::0", "arrays.md::1", "arrays.md::2"],
        )
        for chunk in chunks:
            self.assertEqual(chunk["source"], "arrays.md")
            self.assertIn(chunk["text"], document["text"])

        self.assertEqual(
            chunks[-1]["text"],
            "## Complejidad\n\n"
            "Acceder a un índice válido cuesta O(1): el número de operaciones\n"
            "necesarias no crece con la cantidad de elementos del array.",
        )

    def test_corpus_is_flat_and_keeps_each_documents_origin(self):
        documents = [
            {"source": "one.md", "text": "## Nota\nUno.\n## Final\nDos."},
            {"source": "two.md", "text": "## Nota\nTres."},
        ]

        chunks = chunk_corpus(documents)

        self.assertEqual(
            [
                (chunk["chunk_id"], chunk["source"], chunk["section"], chunk["text"])
                for chunk in chunks
            ],
            [
                ("one.md::0", "one.md", "Nota", "## Nota\nUno."),
                ("one.md::1", "one.md", "Final", "## Final\nDos."),
                ("two.md::0", "two.md", "Nota", "## Nota\nTres."),
            ],
        )

    def test_repeated_titles_and_last_section_without_final_newline(self):
        document = {
            "source": "example.md",
            "text": "# Ejemplo\n\n## Nota\n\nPrimera.\n\n## Nota\n\nÚltima.",
        }

        self.assertEqual(
            chunk_document(document),
            [
                {
                    "chunk_id": "example.md::0",
                    "source": "example.md",
                    "section": "Nota",
                    "text": "## Nota\n\nPrimera.",
                },
                {
                    "chunk_id": "example.md::1",
                    "source": "example.md",
                    "section": "Nota",
                    "text": "## Nota\n\nÚltima.",
                },
            ],
        )


if __name__ == "__main__":
    unittest.main()
