def calculate_sum(a: int , b: int , expression: str):
    if expression == "sum":
        return a+b
    elif expression == "subtract":
        return a - b
    elif expression == "multiply":
        return a*b
    elif expression == "divide":
        return a / b
    elif expression == "floor divison":
        return a//b
    else:
        return "your {expression} is not available"
