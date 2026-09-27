def judge(question, expects, answer, results) -> bool:
    return expects.lower().strip() in answer.lower()