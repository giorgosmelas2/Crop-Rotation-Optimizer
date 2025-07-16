def machinery_evaluation(required_machinery: list[str], missing_machinery: list[str]) -> float:
    for machinery in required_machinery:
        if machinery in missing_machinery:
            return 0.0  
    return 1.0