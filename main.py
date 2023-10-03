# Status codes
# 200 OK for a successful request with data.
# 201 Created for successful resource creation (e.g., after a POST request).
# 204 No Content for successful requests with no response body (e.g., after a DELETE request).
# 400 Bad Request for client errors (e.g., invalid input data).
# 401 Unauthorized for authentication errors.
# 403 Forbidden for authorization errors.
# 404 Not Found for resource not found errors.
# 500 Internal Server Error for server errors.

# 1. run this on my machine record a test and run it locally
# 2. run this on my machine record a test and run it on a remote machine - hosted on a server
# 3. daily execution of entire test suite remotely
#

import sys
from fastapi import FastAPI, Body, Query, HTTPException
from typing import Dict, Optional
from enum import Enum
from uvicorn import run
from src.globals import JsonType
from process_api import process_api
from process_api.modules.selenium import SeleniumModule
from process_api.modules.selenium.conversions import clean_google_recording, GoogleRecording
from src.json_identifier import identify_json
from src.test_runner import TestRunner

app = FastAPI()

SeleniumModule.register(process_api)
process_api.logger.set_level("error")

@app.get("/")
async def index():
    return {"message": "Hello, world!"}

@app.post("/convert_recording")
def convert_recording(recording_json: Dict = Body(...)):
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
    return await TestRunner.test(process_api, data, browser, json_type)

host_address = "127.0.0.1"
host_port = 8000

# read the host_address from args if it was defined using --host, and the same with port
if sys.argv.__contains__("--host"):
    host_address = sys.argv[sys.argv.index("--host") + 1]

if sys.argv.__contains__("--port"):
    host_port = sys.argv[sys.argv.index("--port") + 1]

run(app, host=host_address, port=host_port)
