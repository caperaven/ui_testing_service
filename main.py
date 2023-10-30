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
import os.path
# 1. run this on my machine record a test and run it locally
# 2. run this on my machine record a test and run it on a remote machine - hosted on a server
# 3. daily execution of entire test suite remotely
#

import sys
import threading
import mimetypes
import io
from fastapi import FastAPI, Body, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
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
from src.history import get_dates, get_summary

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
globals["server"] = "https://localhost"

process_api.state = globals

register_extensions(process_api)

for folder in globals["templates_folders"]:
    if " | " not in folder:
        process_api.process_templates.load_from_folder(folder)
    else:
        parts = folder.split(" | ")
        new_folder = parts[1]
        process_api.process_templates.load_from_folder(new_folder)


@app.get("/server_list")
async def server_list():
    file = os.path.normpath(globals["config_folder"] + "\\servers.json")
    with open(file, "r") as json_file:
        data = json.load(json_file)

    return data


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
async def test(data: Dict = Body(...), browser: Optional[str] = Query("chrome"),
               server: Optional[str] = Query("https://localhost")):
    json_type = identify_json(data)
    test_id = data.get("id", "unknown")
    process_api.state["server"] = server
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


@app.delete("/status")
async def del_status(status_filter: Optional[str] = Query(None)):
    if status_filter is None:
        queue.statuses = {}
        return

    keys = list(queue.statuses.keys())

    for key in keys:
        value = queue.statuses[key]
        if status_filter == value["status"]:
            await queue.remove(key)


# get the log of a test that was run
@app.get("/log")
async def log(job_id: str):
    if job_id.__contains__("\\"):
        log_file_path = get_log_file_path(job_id)
    else:
        if job_id not in queue.statuses:
            raise HTTPException(status_code=404, detail="Job not found")

        status = queue.statuses[job_id]

        if status["status"] != "complete" and status["status"] != "error":
            raise HTTPException(status_code=400, detail="Job not complete")

        log_file_path = status["log"]

    result = []
    log_file_path = os.path.normpath(log_file_path)

    with open(log_file_path, "r") as file:
        for line in file:
            line = line.replace("\n", "")
            line = line.replace("\r", "")
            line = line.replace("\t", "    ")
            result.append(line)

    return result


# get the memory chart
@app.get("/memory_data")
async def memory_data(job_id: str):
    if job_id.__contains__("\\"):
        file = get_log_file_path(job_id).replace(".log", ".memory.csv")
    else:
        if job_id not in queue.statuses:
            raise HTTPException(status_code=404, detail="Job not found")

        status = queue.statuses[job_id]

        if status["status"] != "complete" and status["status"] != "error":
            raise HTTPException(status_code=400, detail="Job not complete")

        file = status["log"].replace(".log", ".memory.csv")

    result = []

    with open(file, "r") as file:
        for line in file:
            line = line.replace("\n", "")
            line = line.replace("\r", "")
            line = line.replace("\t", "    ")
            result.append(line)

    return result


# get the schema of a test that was run
@app.get("/memory_graph")
async def memory_graph(job_id: str):
    if job_id.__contains__("\\"):
        file = get_log_file_path(job_id).replace(".log", ".memory.png")
    else:
        if job_id not in queue.statuses:
            raise HTTPException(status_code=404, detail="Job not found")

        status = queue.statuses[job_id]

        if status["status"] != "complete" and status["status"] != "error":
            raise HTTPException(status_code=400, detail="Job not complete")

        file = status["log"].replace(".log", ".memory.png")

    # load the image and return it as a base64 string
    with open(file, "rb") as file:
        image = file.read()

    return StreamingResponse(io.BytesIO(image), media_type="image/png")


@app.get("/test_schema")
async def test_schema(job_id: str):
    if job_id.__contains__("\\"):
        file = get_log_file_path(job_id).replace(".log", ".schema.json")
    else:
        if job_id not in queue.statuses:
            raise HTTPException(status_code=404, detail="Job not found")

        status = queue.statuses[job_id]

        if status["status"] != "complete" and status["status"] != "error":
            raise HTTPException(status_code=400, detail="Job not complete")

        file = status["log"].replace(".log", ".schema.json")

    with open(file, "r") as json_file:
        data = json.load(json_file)

    return data


@app.get("/history")
async def history(date: Optional[str] = Query(None)):
    if date is None:
        return get_dates()

    return get_summary(date)


@app.get("/templates")
async def templates():
    result = []

    for folder in globals["templates_folders"]:
        if " | " not in folder:
            search_folder = os.path.normpath(folder)
            get_template_files(None, search_folder, result)
        else:
            parts = folder.split(" | ")
            prefix = parts[0]
            search_folder = os.path.normpath(parts[1])
            get_template_files(prefix, search_folder, result)

    return result


def get_template_files(prefix, folder, result):
    for file in os.listdir(folder):
        if file.endswith(".json"):
            if prefix is None:
                result.append(file)
            else:
                result.append(prefix + " | " + file)


@app.put("/template")
async def template_put(name: str, data: Dict = Body(...)):
    if " | " in name:
        template_folder = find_folder_for_prefix(name.split(" | ")[0])
        name = name.split(" | ")[1]
    else:
        template_folder = os.path.normpath(globals["templates_folders"][0])

    file = os.path.normpath(template_folder + "\\" + name)

    with open(file, "w") as json_file:
        json.dump(data, json_file, indent=2)

    return {"message": "Template saved"}


@app.get("/template")
async def template_get(name: str):
    if " | " in name:
        template_folder = find_folder_for_prefix(name.split(" | ")[0])
        name = name.split(" | ")[1]
    else:
        template_folder = os.path.normpath(globals["templates_folders"][0])

    file = os.path.normpath(template_folder + "\\" + name)

    with open(file, "r") as json_file:
        data = json.load(json_file)

    return data


def find_folder_for_prefix(prefix):
    for search_folder in globals["templates_folders"]:
        if search_folder.startswith(prefix):
            return search_folder.split(" | ")[1]

    return None


@app.get("/extensions")
async def templates():
    result = []
    folder = os.path.normpath(globals["ext_folder"])
    for file in os.listdir(folder):
        if file.endswith(".py"):
            result.append(file)

    return result


@app.put("/extension")
async def extension_put(name: str, data: Dict = Body(...)):
    folder = os.path.normpath(globals["ext_folder"])
    file = os.path.normpath(folder + "\\" + name)

    with open(file, "w") as file:
        file.write(data["content"])

    return {"message": "extension saved"}


@app.get("/extension")
async def extension_get(name: str):
    folder = os.path.normpath(globals["ext_folder"])
    file = os.path.normpath(folder + "\\" + name)

    with open(file, "r") as file:
        data = file.read()

    return {
        "content": data
    }


@app.get("/test_bundles")
async def test_bundles_get():
    file = os.path.normpath(globals["config_folder"]) + "\\test_bundles.json"

    with open(file, "r") as file:
        data = json.load(file)

    result = []
    for key, value in data.items():
        result.append(key)

    return result


@app.get("/before_bundles")
async def before_bundles_get():
    result = ["None"]

    if "before" in globals:
        result.extend(globals["before"].keys())

    return result


@app.post("/queue_before")
async def queue_before_post(bundle: str, browser: Optional[str] = Query("chrome")):
    if bundle == "None":
        return

    if "before" not in globals:
        return

    if bundle not in globals["before"]:
        return

    before_bundle = globals["before"][bundle]
    test_files = os.listdir(before_bundle)

    for test_file in test_files:
        if test_file.endswith(".json"):
            with open(os.path.normpath(before_bundle + "\\" + test_file), "r") as json_file:
                data = json.load(json_file)

            test_id = data["id"]
            await queue.add(test_id, TestRunner.test, process_api, data, browser, JsonType.SCHEMA)


@app.get("/queue_after")
async def queue_after_post(bundle: str, browser: Optional[str] = Query("chrome")):
    if bundle == "None":
        return

    if "after" not in globals:
        return

    if bundle not in globals["after"]:
        return

    after_bundle = globals["after"][bundle]
    test_files = os.listdir(after_bundle)

    for test_file in test_files:
        if test_file.endswith(".json"):
            with open(os.path.normpath(after_bundle + "\\" + test_file), "r") as json_file:
                data = json.load(json_file)

            test_id = data["id"]
            await queue.add(test_id, TestRunner.test, process_api, data, browser, JsonType.SCHEMA)


@app.post("/queue_bundle")
async def queue_bundle_post(bundle: str, browser: Optional[str] = Query("chrome"),
                            stop_on_error: Optional[bool] = Query(False)):
    await queue_before_post(bundle, browser)

    file = os.path.normpath(globals["config_folder"]) + "\\test_bundles.json"

    globals["stop_on_error"] = stop_on_error

    with open(file, "r") as file:
        data = json.load(file)

    bundle_folder = data[bundle]
    test_files = os.listdir(bundle_folder)

    for test_file in test_files:
        if test_file.endswith(".json"):
            with open(os.path.normpath(bundle_folder + "\\" + test_file), "r") as json_file:
                data = json.load(json_file)

            test_id = data["id"]
            await queue.add(test_id, TestRunner.test, process_api, data, browser, JsonType.SCHEMA)

    await queue_after_post(bundle, browser)


@app.post("/run_queue")
async def run_queue():
    if queue.running is False:
        threading.Thread(target=run_in_new_loop).start()


def get_log_file_path(job_id: str):
    return globals["log_folder"] + "\\" + job_id.replace("_35_", "#") + "\\test.log"


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
