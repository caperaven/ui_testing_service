import enum
import os
import json

SCHEMA = "schema"
SELENIUM = "selenium"
GOOGLE_RECORDING = "google_recording"
SELENIUM_RECORDING = "selenium_recording"


def load_templates_config(collection):
    config_file = os.path.join(os.getcwd(), "config/templates.json")

    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            data = json.load(f)

            for key, value in data.items():
                result = f"{key} | {value}"
                collection.append(result)


def load_before_after_config():
    before_file = os.path.join(os.getcwd(), "config/before.json")
    after_file = os.path.join(os.getcwd(), "config/after.json")

    if os.path.exists(before_file):
        with open(before_file, "r") as f:
            data = json.load(f)
            globals["before"] = data

    if os.path.exists(after_file):
        with open(after_file, "r") as f:
            data = json.load(f)
            globals["after"] = data


class JsonType(enum.Enum):
    SCHEMA = "schema"
    GOOGLE_RECORDING = "google_recording"
    SELENIUM_RECORDING = "selenium_recording"


template_folders = [
    os.path.join(os.getcwd(), "templates")
]

load_templates_config(template_folders)

globals = {
    "log_folder": os.path.join(os.getcwd(), "logs"),
    "ext_folder": os.path.join(os.getcwd(), "extensions"),
    "templates_folders": template_folders,
    "config_folder": os.path.join(os.getcwd(), "config"),
    "stop_on_error": False
}

load_before_after_config()
