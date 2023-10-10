
def _eval(args, value1, value2):
    operator = args.get("operator", "eq")

    if operator == "eq":
        return value1 == value2
    elif operator == "neq":
        return value1 != value2
    elif operator == "gt":
        return value1 > value2
    elif operator == "gte":
        return value1 >= value2
    elif operator == "lt":
        return value1 < value2
    elif operator == "lte":
        return value1 <= value2
    elif operator == "in":
        return value1 in value2
    elif operator == "nin":
        return value1 not in value2
    elif operator == "startswith":
        return value1.startswith(value2)
    elif operator == "endswith":
        return value1.endswith(value2)
