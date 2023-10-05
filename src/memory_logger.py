from datetime import datetime
from src.globals import globals

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

    def save_to_file(self, file_name):
        import csv

        new_file_name = file_name.replace(".log", ".memory.csv")

        with open(new_file_name, 'w', newline='') as csvfile:
            fieldnames = ['date_time', 'name', 'memory']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for item in self.memory:
                writer.writerow(item)