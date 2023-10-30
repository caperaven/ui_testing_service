from process_api.modules.selenium.automation import DriverActions, goto, get, set, wait, perform
from process_api.utils.get_value import get_value
from process_api.modules.selenium.modules import register as register_modules
from process_api.modules.selenium.conversions.clean_google_recording import clean_google_recording
from process_api.modules.selenium.conversions.from_google_recording import GoogleRecording


class SeleniumModule:
    @staticmethod
    def register(api):
        api.add_module("selenium", SeleniumModule)
        register_modules(api)

    @staticmethod
    async def init_driver(api, step, ctx=None, process=None, item=None):
        args = step["args"]
        browser = await get_value(args.get("browser"), ctx, process, item)
        options = await get_value(args.get("options"), ctx, process, item)
        driver = await DriverActions.init(browser, options)

        api.set_variable("driver", driver)

        return driver

    @staticmethod
    async def close_driver(api, step, ctx=None, process=None, item=None):
        selenium_driver = api.get_variable("driver")
        await DriverActions.close(selenium_driver)
        api.delete_variable("driver")

    @staticmethod
    async def goto(api, step, ctx=None, process=None, item=None):
        args = step["args"]
        selenium_driver = api.get_variable("driver")
        url = await get_value(args.get("url"), ctx, process, item)

        await goto(selenium_driver, url)

        if "wait" in args:
            api.logger.info(f'waiting for {args["wait"]}')
            await wait(selenium_driver, {
                "query": args["wait"]
            })

    @staticmethod
    async def get(api, step, ctx=None, process=None, item=None):
        selenium_driver = api.get_variable("driver")

        args = step["args"]
        if "wait" in args:
            api.logger.info(f'waiting for {args["wait"]}')
            await wait(selenium_driver, {
                "query": args["wait"]
            })

        return await get(selenium_driver, step["args"])

    @staticmethod
    async def set(api, step, ctx=None, process=None, item=None):
        selenium_driver = api.get_variable("driver")

        args = step["args"]
        if "wait" in args:
            api.logger.info(f'waiting for {args["wait"]}')
            await wait(selenium_driver, {
                "query": args["wait"]
            })

        return await set(selenium_driver, step["args"])

    @staticmethod
    async def wait(api, step, ctx=None, process=None, item=None):
        selenium_driver = api.get_variable("driver")
        return await wait(selenium_driver, step["args"])

    @staticmethod
    async def perform(api, step, ctx=None, process=None, item=None):
        selenium_driver = api.get_variable("driver")
        await perform(selenium_driver, step["args"])

        args = step["args"]
        if "wait" in args:
            api.logger.info(f'waiting for {args["wait"]}')
            await wait(selenium_driver, {
                "query": args["wait"]
            })

    @staticmethod
    async def run_google_recording(api, step, ctx=None, process=None, item=None):
        args = step["args"]
        recording_json = await get_value(args["recording"], ctx, process, item)
        clean_recording_json = clean_google_recording(recording_json)
        converter = GoogleRecording(clean_recording_json)
        schema_json = converter.to_json()
        await api.run_schema(schema_json, ctx, process)

