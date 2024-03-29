import os
import importlib
from src.globals import globals
import inspect


def register_extensions(api):
    folder = globals["ext_folder"]

    for file in os.listdir(folder):
        if file.endswith('.py') and file != '__init__.py':
            module_name = os.path.splitext(file)[0]
            module_path = os.path.join(folder, file)

            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            for name, obj in inspect.getmembers(module, inspect.isclass):
                if name[0].isupper() and hasattr(obj, 'register') and callable(obj.register):
                    obj.register(api)

