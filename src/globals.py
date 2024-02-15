import enum
import os
import json
import platform
import sys

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

            for key, value in data.items():
                data[key] = value.replace("$root", globals["$root"])

            globals["before"] = data

    if os.path.exists(after_file):
        with open(after_file, "r") as f:
            data = json.load(f)

            for key, value in data.items():
                data[key] = value.replace("$root", globals["$root"])

            globals["after"] = data


## read the root.json file and return the root folder for the current operating system
def get_root():
    root_file = os.path.join(os.getcwd(), "config/root.json")
    operating_system = "windows"

    if sys.platform.startswith('linux'):
        operating_system = "linux"
    elif sys.platform.startswith('darwin'):
        operating_system = "mac"

    if os.path.exists(root_file):
        with open(root_file, "r") as f:
            data = json.load(f)
            return data[operating_system]


def get_default_page():
    default_page_file = os.path.join(os.getcwd(), "config/default_page.json")
    if os.path.exists(default_page_file):
        with open(default_page_file, "r") as f:
            data = json.load(f)
            return data


class JsonType(enum.Enum):
    SCHEMA = "schema"
    GOOGLE_RECORDING = "google_recording"
    SELENIUM_RECORDING = "selenium_recording"


template_folders = [
    os.path.join(os.getcwd(), "templates")
]

load_templates_config(template_folders)

globals = {
    "$root": get_root(),
    "log_folder": os.path.join(os.getcwd(), "logs"),
    "ext_folder": os.path.join(os.getcwd(), "extensions"),
    "templates_folders": template_folders,
    "config_folder": os.path.join(os.getcwd(), "config"),
    "stop_on_error": False,
    "default_page": get_default_page(),
}

load_before_after_config()
