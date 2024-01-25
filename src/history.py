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
    folder =  os.path.normpath(globals["log_folder"] + "/" + date)
    sub_folders = os.listdir(folder)
    save_folders_to_result(folder, sub_folders, result)
    return result

def save_folders_to_result(folder, folders, result):
    for sub_folder in folders:
        file = os.path.normpath(folder + "/" + sub_folder + "/test.summary.json")

        # check if the file exists
        if os.path.isfile(file):
            with open(file, "r") as json_file:
                data = json.load(json_file)
                file_path = data["log"]
                parts = file_path.split('\\logs\\')
                data["log"] = parts[1].replace("test.log", "").replace("#", "_35_")
                result.append(data)

            json_file.close()

        else:
            new_folder = os.path.normpath(folder + "/" + sub_folder)
            sub_folders = os.listdir(new_folder)
            save_folders_to_result(new_folder, sub_folders, result)

