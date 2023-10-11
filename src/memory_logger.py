import csv
from datetime import datetime
from src.globals import globals
import os
import json

class MemoryLogger:
    def __init__(self):
        self.memory = []

    async def log(self, name):
        api = globals["api"]

        memory = await api.call("memory", "get_process_memory", {
            id: globals["process_id"]
        })

        self.memory.append({
            "name": name,
            "memory": memory,
            "date_time": datetime.now()
        })

    async def clear(self):
        self.memory = []

    async def ensure_path(self, file_name):
        path = os.path.dirname(file_name)
        if not os.path.exists(path):
            os.makedirs(path)

    async def save_to_file(self, file_name, test_schema):
        new_file_name = file_name.replace(".log", ".memory.csv")

        with open(new_file_name, 'w', newline='') as csv_file:
            fieldnames = ['date_time', 'name', 'memory']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for item in self.memory:
                writer.writerow(item)

            csv_file.flush()

        schema_file = new_file_name.replace(".memory.csv", ".schema.json")
        with open(schema_file, 'w') as schema_file:
            json.dump(test_schema, schema_file, indent=4)

    async def save_graph(self, file_name):
        api = globals["api"]

        await api.call("data", "set_data", {
            "name": "memory",
            "data": self.memory
        })

        graph_file = file_name.replace(".log", ".memory.png")

        await api.call("data", "plot", {
            "name": "memory",
            "field": "memory",
            "title": "Memory Usage",
            "xtitle": "Time",
            "ytitle": "Memory (MB)",
            "file": graph_file
        })

        await api.call("data", "unload", {
            "name": "memory"
        })

