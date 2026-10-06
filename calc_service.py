def safe_calc(expr:str):
    try:
        res = eval(expr)
        return True, str(res)
    except:
        return False, "Calculation error"
