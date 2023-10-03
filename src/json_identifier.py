from src.globals import JsonType


def identify_json(json_data):
    if "steps" in json_data:
        return JsonType.GOOGLE_RECORDING

    if "tests" in json_data:
        return JsonType.SELENIUM_RECORDING

    return JsonType.SCHEMA
