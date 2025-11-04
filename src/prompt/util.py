from num2words import num2words

def lenght_to_string(lenght: int) -> str:
    unit = "meter" if lenght == 1 else "meters"
    return f"{num2words(lenght)} {unit}"

