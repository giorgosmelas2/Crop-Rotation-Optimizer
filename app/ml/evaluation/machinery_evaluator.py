def machinery_evaluation(required_machinery: list[str], missing_machinery: list[str]) -> float:
    """
    Check whether the farmer has all the machinery required for a given crop. 
    1.0 means farmer has all of the required machinery and 0.0 means farmer hasn't got some of them
    """
    
    for machinery in required_machinery:
        if machinery in missing_machinery:
            return 0.0  
    return 1.0