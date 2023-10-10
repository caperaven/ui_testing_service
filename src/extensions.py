from src.globals import globals
import os
import sys
import importlib


def register_extensions(api):
    folder = globals["ext_folder"]
    files = os.listdir(folder)

    sys.path.append(folder)

    for file in files:
        if ".py" not in file:
            continue

        module_name = file.replace(".py", "")
        module = importlib.import_module(module_name)
        default_class = getattr(module, "DefaultModule", None)
        default_class.register(api)

