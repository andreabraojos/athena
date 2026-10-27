import re


def tokenize(text: str) -> list[str]:
    tokens = re.findall(r"\w+", text.lower())
    return tokens

def score_overlap(
    query_tokens: list[str],
    chunk_tokens: list[str],
) -> int:
    matches = 0
    for word in query_tokens:
        if word in chunk_tokens:
            matches += 1

    return matches

def score_chunks(
    query: str,
    chunks: list[dict[str, str]],
) -> list[dict]:
    query_tokens = tokenize(query)
    results = []
    for chunk in chunks:
        chunk_tokens = tokenize(chunk["text"])
        score = score_overlap(query_tokens, chunk_tokens)
        diccionario = { "chunk_id" : chunk["chunk_id"],
                             "score" : score}
        results.append(diccionario)
        print(chunk["chunk_id"], score)
    return results

def get_score(result: dict) -> int:
    return result["score"]

def retrieve(
        query: str,
        chunks: list[dict[str, str]],
) -> list[dict]:
    results = score_chunks(query, chunks)
    ranked_results = sorted(results, key=get_score, reverse=True)
    return ranked_results