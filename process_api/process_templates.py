import copy
import json
import os
from src.globals import globals
from src.os_path import get_os_path


class ProcessTemplates:
    def __init__(self):
        self.templates = {}

    def add_template(self, template):
        id_value = template["id"]
        self.templates[id_value] = template

    def get_template(self, id):

        template = self.templates.get(id, None)

        if template is not None:
            return copy.deepcopy(template)

    def remove_template(self, id):
        del self.templates[id]

    def clear(self):
        self.templates = {}

    def load_from_file(self, filename):
        with open(filename) as json_file:
            data = json.load(json_file)
            self.add_template(data)

    def load_from_folder(self, folder):
        folder = folder.replace("$root", globals["$root"])
        folder = get_os_path(folder)

        if os.path.exists(folder) is False:
            return

        for filename in os.listdir(folder):
            if filename.endswith(".json"):
                self.load_from_file(os.path.join(folder, filename))
