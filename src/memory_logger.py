import csv
from datetime import datetime
from src.globals import globals
import concurrent.futures
import os
import asyncio


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

    async def save_to_file(self, file_name):
        new_file_name = file_name.replace(".log", ".memory.csv")

        with open(new_file_name, 'w', newline='') as csvfile:
            fieldnames = ['date_time', 'name', 'memory']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for item in self.memory:
                writer.writerow(item)

            csvfile.flush()

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

