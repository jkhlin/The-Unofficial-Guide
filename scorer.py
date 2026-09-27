def judge(question, expects, answer, results) -> bool:
    return expects.lower().strip() in answer.lower()

def retrieval_hits(expects, results) -> bool:
    return any(expects.lower().strip() in chunk["text"].lower() for chunk in results)