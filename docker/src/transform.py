import csv

def clean_posts(data: list) -> list:
    # As already know about schema, code is not flexible as it should
    cleaned = []
    for d in data:
        # 1. skip rows with missing/invalid salary
        if d != data[0]:
            try:
                name = str(d[0])
                age = int(d[1])
                promotion_score = float(d[2])
            except (ValueError, TypeError):
                continue                        # drop bad rows
        else:
            name=d[0]
            age=d[1]
            promotion_score=d[2]
        # 2. cast types
        cleaned.append([name,age,promotion_score])
        
    return cleaned

