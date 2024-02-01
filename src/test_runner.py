import os
import sys
from src.globals import globals


class TestRunner:
    @staticmethod
    async def test(api, data, json_type):
        if "skip" in data:
            api.logger.info("Skipping: " + data["skip"])
            return "skipped"

        method = getattr(TestRunner, json_type.value)
        return await method(api, data)

    @staticmethod
    async def schema(api, data):
        return await api.run_schema(data, None, None, run_callback)

    @staticmethod
    async def google_recording(api, driver, data):
        pass

    @staticmethod
    async def selenium_recording(api, driver, data):
        pass


async def run_callback(api, step, ctx, process, item):
    step_name = step.get("name")

    ## Ignore query steps as they are not part of what we want to log memory for
    if step_name.startswith("has_"):
        return

    await globals["memory_logger"].log(step_name)


async def get_driver(api, browser):
    method = getattr(DriverFactory, browser)
    return await method(api)


class DriverFactory:
    @staticmethod
    async def chrome(api):
        current_directory = os.getcwd()

        driver_file = "chrome/chromedriver"

        if not sys.platform.startswith('darwin'):
            driver_file += ".exe"

        full_chrome_path = os.path.join(current_directory, driver_file)
        full_chrome_path = os.path.abspath(full_chrome_path)

        return await api.call("selenium", "init_driver", {
            "browser": "chrome",
            "options": {
                "driver_path": full_chrome_path
            }
        })

    @staticmethod
    async def firefox(api):
        return await api.call("selenium", "init_driver", {
            "browser": "firefox",
            "options": {
                "arguments": ["--no-sandbox", "--disable-dev-shm-usage"],
            }
        })

    @staticmethod
    async def safari(api):
        return await api.call("selenium", "init_driver", {
            "browser": "safari",
            "options": {}
        })
