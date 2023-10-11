# Status codes
# 200 OK for a successful request with data.
# 201 Created for successful resource creation (e.g., after a POST request).
# 204 No Content for successful requests with no response body (e.g., after a DELETE request).
# 400 Bad Request for client errors (e.g., invalid input data).
# 401 Unauthorized for authentication errors.
# 403 Forbidden for authorization errors.
# 404 Not Found for resource not found errors.
# 500 Internal Server Error for server errors.
import asyncio
import json
# 1. run this on my machine record a test and run it locally
# 2. run this on my machine record a test and run it on a remote machine - hosted on a server
# 3. daily execution of entire test suite remotely
#

import sys
import threading
import mimetypes
from fastapi import FastAPI, Body, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Optional
from uvicorn import run
from src.globals import JsonType
from process_api import process_api
from process_api.modules.selenium import SeleniumModule
from process_api.modules.data import DataModule
from process_api.modules.selenium.conversions import clean_google_recording, GoogleRecording
from src.json_identifier import identify_json
from src.test_runner import TestRunner
from src.task_queue import TaskQueue
from src.globals import globals
from src.memory_logger import MemoryLogger
from src.extensions import register_extensions
from process_api.utils.get_value import get_value
from process_api.utils.set_value import set_value

app = FastAPI()
queue = TaskQueue()

SeleniumModule.register(process_api)
DataModule.register(process_api)

process_api.logger.set_level("info")
process_api.break_on_error = True
process_api.get_value = get_value
process_api.set_value = set_value

globals["queue"] = queue
globals["api"] = process_api
globals["memory_logger"] = MemoryLogger()

register_extensions(process_api)
process_api.process_templates.load_from_folder(globals["templates_folder"])

@app.post("/convert_recording")
async def convert_recording(recording_json: Dict = Body(...)):
    json_type = identify_json(recording_json)

    if json_type == JsonType.GOOGLE_RECORDING:
        clean_recording_json = clean_google_recording(recording_json)
        converter = GoogleRecording(clean_recording_json)
        return converter.to_json()

    if json_type == JsonType.SELENIUM_RECORDING:
        return {"message": "Recording not supported YET, but stay tuned"}

    return {"message": "Recording not supported"}

@app.post("/test")
async def test(data: Dict = Body(...), browser: Optional[str] = Query("chrome")):
    json_type = identify_json(data)
    test_id = data.get("id", "unknown")
    job_id = await queue.add(test_id, TestRunner.test, process_api, data, browser, json_type)

    if queue.running is False:
        threading.Thread(target=run_in_new_loop).start()

    return {"job_id": job_id}


@app.get("/test_status")
async def test_status(job_id: str):
    if job_id not in queue.statuses:
        raise HTTPException(status_code=404, detail="Job not found")

    return queue.statuses[job_id]


@app.delete("/test_status")
async def test_status(job_id: str):
    if job_id not in queue.statuses:
        raise HTTPException(status_code=404, detail="Job not found")

    await queue.remove(job_id)


@app.get("/status")
async def status(only_errors: Optional[bool] = Query(False)):
    if only_errors is False:
        return queue.statuses

    result = {}
    # from the statuses dict, only return the ones that have errors
    for key, value in queue.statuses.items():
        if value["status"] == "complete" and value["error_count"] > 0:
            result[key] = value

    return result


@app.get("/log")
async def log(job_id: str):
    if job_id not in queue.statuses:
        raise HTTPException(status_code=404, detail="Job not found")

    status = queue.statuses[job_id]

    if status["status"] != "complete":
        raise HTTPException(status_code=400, detail="Job not complete")

    log_file_path = status["log"]

    result = []

    with open(log_file_path, "r") as file:
        for line in file:
            line = line.replace("\n", "")
            line = line.replace("\r", "")
            line = line.replace("\t", "    ")
            result.append(line)

    return result


def run_in_new_loop():
    # Create a new event loop
    loop = asyncio.new_event_loop()
    # Set the loop as the default for this context
    asyncio.set_event_loop(loop)
    # Run the async function in the loop
    loop.run_until_complete(queue.run_first_task())
    # Close the loop after the task is done
    loop.close()


host_address = "127.0.0.1"
host_port = 8000

# read the host_address from args if it was defined using --host, and the same with port
if sys.argv.__contains__("--host"):
    host_address = sys.argv[sys.argv.index("--host") + 1]

if sys.argv.__contains__("--port"):
    host_port = sys.argv[sys.argv.index("--port") + 1]

mimetypes.add_type("application/javascript", ".js")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/", StaticFiles(directory="static"), name="static")

run(app, host=host_address, port=host_port)
