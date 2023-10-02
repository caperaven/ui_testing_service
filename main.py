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

import threading
import os
import time

from fastapi import FastAPI, Body, Query, HTTPException
from typing import Dict, Optional
from enum import Enum
from uvicorn import run
from process_api import process_api
from process_api.modules.selenium import SeleniumModule
from process_api.modules.selenium.conversions import clean_google_recording, GoogleRecording

SCHEMA = "schema"
SELENIUM = "selenium"
GOOGLE_RECORDING = "google_recording"
SELENIUM_RECORDING = "selenium_recording"

app = FastAPI()


@app.get("/")
async def index():
    return {"message": "Hello, world!"}

@app.get("/testinfo")
async def test_info(uuid: str):
    return "test not in queue"


    return {"message": "... what is going on with that test"}


async def put_template(recording_json: Dict = Body(...)):
    pass


async def del_template(id: str):
    pass


async def clear_templates():
    pass

@app.post("/convert_recording")
def convert_recording(recording_type: str, recording_json: Dict = Body(...)):
    if recording_type == GOOGLE_RECORDING:
        clean_recording_json = clean_google_recording(recording_json)
        converter = GoogleRecording(clean_recording_json)
        return converter.to_json()

    if recording_type == SELENIUM_RECORDING:
        return {"message": "Recording not supported YET, but stay tuned"}

    return {"message": "Recording not supported"}


@app.post("/test")
async def test(data: Dict = Body(...)):
    # 1. figure out what type of recording it is (schema, selenium, chrome)
    # 2. convert it to a schema
    # 3. create uuid for process
    # 4. start running a process
    # 5. return uuid
    pass
