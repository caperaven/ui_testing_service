# this is a class that allows you to create a queue of tasks that can be executed in a separate thread
import uuid
import asyncio
from datetime import datetime


class TaskQueue:
    def __init__(self):
        self.queue = []
        self.statuses = {}
        self.running = False

    async def add(self, fn, *args, **kwargs):
        task_id = str(uuid.uuid4())

        self.queue.append({
            "id": task_id,
            "fn": fn,
            "args": args,
            "kwargs": kwargs
        })

        self.statuses[task_id] = {
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
            status["status"] = "complete"
            status["end_time"] = datetime.now()
            status["duration"] = get_time_format(status["start_time"], status["end_time"])

            # call self recursively to run the next task
            await self.run_first_task()

    async def remove(self, task_id):
        del self.statuses[task_id]


def get_time_format(start_time, end_time):
    duration = end_time - start_time
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = duration.microseconds // 1000  # Convert microseconds to milliseconds

    formatted_duration = "{:02}:{:02}:{:02}:{:03}".format(hours, minutes, seconds, milliseconds)
    return formatted_duration
