from selenium.webdriver.common.by import By
from process_api.utils.run_step import run_step


# In this module we ask questions about the dom
# The result is always a boolean and executes either the pass or fail step as defined.
# You must define a pass or fail step in the test.
# NB: All step names must start with "has_"

class QueryModule:

    @staticmethod
    def register(api):
        api.add_module("query", QueryModule)

    @staticmethod
    async def has_element(api, step, ctx=None, process=None, item=None, callback=None):
        api.logger.info(f'has_element {step["args"].get("query")}')

        args = step["args"]
        query = args.get("query", None)
        pass_step = args.get("pass_step", None)
        fail_step = args.get("fail_step", None)

        driver = api.variables["driver"]

        try:
            found_element = driver.find_element(By.CSS_SELECTOR, query)
        except:
            pass

        if found_element and pass_step:
            return await run_step(api, pass_step, ctx, process, item)

        if fail_step:
            return await run_step(api, fail_step, ctx, process, item)
