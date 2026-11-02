import unittest

from retrieval import retrieve, score_overlap, tokenize


class RetrievalTests(unittest.TestCase):
    def test_tokenize_normalizes_case_and_punctuation(self):
        actual = tokenize("¿Un **STACK** sigue LIFO?")
        expected = ["un", "stack", "sigue", "lifo"]

        self.assertEqual(actual, expected)

    def test_score_overlap_ignores_word_position(self):
        actual = score_overlap(
            ["stack", "lifo"],
            ["lifo", "un", "stack"]
        )
        expected = 2

        self.assertEqual(actual, expected)

    def test_retrieve_orders_by_score_descending(self):
        query = "stack lifo"

        chunks = [
            {"chunk_id": "example.md::0", "text": "queue fifo"},
            {"chunk_id": "example.md::1", "text": "stack lifo"},
        ]

        actual = retrieve(query, chunks)
        expected = [
            {"chunk_id": "example.md::1", "score": 2},
            {"chunk_id": "example.md::0", "score": 0},
        ]

        self.assertEqual(actual, expected)