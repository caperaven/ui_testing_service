import json
import os
from src.globals import globals


def get_dates():
    result = []

    folder = globals["log_folder"]
    for folder_name in os.listdir(folder):
        result.append(folder_name)

    return result


def get_summary(date):
    result = []
    folder = globals["log_folder"] + "/" + date
    sub_folders = os.listdir(folder)

    for sub_folder in sub_folders:
        file = os.path.normpath(folder + "/" + sub_folder + "/test.summary.json")

        # check if the file exists
        if os.path.isfile(file):
            with open(file, "r") as json_file:
                data = json.load(json_file)
                file_path = data["log"]
                parts = file_path.split('\\logs\\')
                data["log"] = parts[1].replace("test.log", "").replace("#", "_35_")
                result.append(data)

    return result