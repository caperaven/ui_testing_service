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

        # load the file as json and add it to the result
        with open(file, "r") as json_file:
            data = json.load(json_file)
            result.append(data)

    return result