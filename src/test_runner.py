import os


class TestRunner:
    @staticmethod
    async def test(api, data, browser, json_type):
        driver = await get_driver(api, browser)
        api.set_variable("driver", driver)

        try:
            method = getattr(TestRunner, json_type.value)
            return await method(api, data)
        finally:
            await api.call("selenium", "close_driver", {
                "driver": driver
            })

    @staticmethod
    async def schema(api, data):
        return await api.run_schema(data)

    @staticmethod
    async def google_recording(api, driver, data):
        pass

    @staticmethod
    async def selenium_recording(api, driver, data):
        pass


async def get_driver(api, browser):
    method = getattr(DriverFactory, browser)
    return await method(api)


class DriverFactory:
    @staticmethod
    async def chrome(api):
        current_directory = os.getcwd()
        full_chrome_path = os.path.join(current_directory, "./chrome/chromedriver.exe")
        full_chrome_path = os.path.normpath(full_chrome_path)

        driver = await api.call("selenium", "init_driver", {
            "browser": "chrome",
            "options": {
                "driver_path": full_chrome_path
            }
        })

        return driver

    @staticmethod
    async def firefox(api):
        pass

    @staticmethod
    async def safari(api):
        pass



# from process_api import process_api
# from process_api.modules.selenium import SeleniumModule
# import os
#
# SeleniumModule.register(process_api)
# process_api.logger.set_level("error")
#
# current_directory = os.getcwd()
# full_chrome_path = os.path.join(current_directory, "./../../../chrome/chromedriver.exe")
# full_chrome_path = os.path.normpath(full_chrome_path)
#
# driver = await process_api.call("selenium", "init_driver", {
#     "browser": "chrome",
#     "options": {
#         "driver_path": full_chrome_path
#     }
# })