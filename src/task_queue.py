# this is a class that allows you to create a queue of tasks that can be executed in a separate thread
import uuid
from datetime import datetime
from src.globals import globals
import os
import json


class TaskQueue:
    def __init__(self):
        self.queue = []
        self.statuses = {}
        self.running = False

    async def add(self, name, fn, *args, **kwargs):
        task_id = str(uuid.uuid4())

        self.queue.append({
            "id": task_id,
            "fn": fn,
            "args": args,
            "kwargs": kwargs
        })

        self.statuses[task_id] = {
            "name": name,
            "status": "queued",
            "start_time": None,
            "end_time": None,
            "duration": None,
        }

        return task_id

    async def run_first_task(self):
        if len(self.queue) == 0:
            self.running = False
            return

        logger = globals["api"].logger
        memory_logger = globals["memory_logger"]
        logger.clear_log()
        await memory_logger.clear()

        self.running = True
        task = self.queue.pop(0)
        task_id = task["id"]

        fn = task["fn"]
        args = task["args"]
        kwargs = task["kwargs"]

        status = self.statuses[task_id]
        status["status"] = "running"
        status["start_time"] = datetime.now()

        try:
            await fn(*args, **kwargs)
        finally:
            status = self.statuses[task_id]

            date_folder = datetime.today().strftime('%Y-%m-%d')
            time_stamp = datetime.now().strftime('%H-%M-%S')
            test_name = status["name"]

            path = f"{globals['log_folder']}/{date_folder}/{time_stamp}_{test_name}/test.log"

            if globals["api"].logger.error_count > 0:
                path = f"{globals['log_folder']}/{date_folder}/ERROR_{time_stamp}_{test_name}/test.log"

            log_file_path = os.path.normpath(path)

            status["end_time"] = datetime.now()
            status["duration"] = get_time_format(status["start_time"], status["end_time"])
            status["log"] = log_file_path
            status["error_count"] = globals["api"].logger.error_count
            status["status"] = "complete"
            status["memory_diff"] = memory_logger.difference()

            if status["error_count"] > 0:
                status["status"] = "error"

            await memory_logger.ensure_path(log_file_path)
            await memory_logger.save_to_file(log_file_path)
            await memory_logger.save_graph(log_file_path)

            save_schema_to_file(log_file_path, args[1])
            save_summary_to_file(log_file_path, status)

            logger.info(f"Task {task_id} completed in {status['duration']}")
            logger.save_to_file(log_file_path)

            # call self recursively to run the next task
            await self.run_first_task()

    async def remove(self, task_id):
        del self.statuses[task_id]


def save_schema_to_file(file_name, test_schema):
    schema_file = file_name.replace(".log", ".schema.json")
    with open(schema_file, 'w') as schema_file:
        json.dump(test_schema, schema_file, indent=4)


def save_summary_to_file(file_name, summary):
    summary["start_time"] = summary["start_time"].strftime("%Y-%m-%d %H:%M:%S")
    summary["end_time"] = summary["end_time"].strftime("%Y-%m-%d %H:%M:%S")

    summary_file = file_name.replace(".log", ".summary.json")
    with open(summary_file, 'w') as summary_file:
        json.dump(summary, summary_file, indent=4)

def get_time_format(start_time, end_time):
    duration = end_time - start_time
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = duration.microseconds // 1000  # Convert microseconds to milliseconds

    formatted_duration = "{:02}:{:02}:{:02}:{:03}".format(hours, minutes, seconds, milliseconds)
    return formatted_duration
