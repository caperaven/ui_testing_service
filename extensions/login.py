from process_api.modules.selenium.automation.get import get_element
from process_api.modules.selenium.modules.selenium_wait import WaitModule
from process_api.modules.selenium.modules.selenium_perform import PerformModule

class LoginModule:
    @staticmethod
    def register(api):
        api.add_module("login", LoginModule)

    @staticmethod
    async def login(api, step, ctx=None, process=None, item=None):
        args = step["args"]
        username = args.get("username")
        password = args.get("password")
        driver = api.get_variable("driver")
        api.logger.info(f'Performing login for {username}...')

        await navigate_to_login(driver, api)
        await open_login(driver, api)
        await fill_in_username(driver, username)
        await fill_in_password(driver, password)
        await fill_stay_signed_in(driver, api)
        await wait_for_main_page(driver)


async def navigate_to_login(driver, api):
    await PerformModule.navigate(api, {
        "args": {
            "url": "${state.server}"
        }
    })

    await get_element(driver, "li[name='development_azure_account']", 30)


## click on the assure button to open login
async def open_login(driver, api):
    await WaitModule.window_count(api, {
        "args": {
            "count": 2
        }
    })

    driver.switch_to.window(driver.window_handles[1])


## find the username field and fill it in
async def fill_in_username(driver, username):
    query = "input[name='loginfmt']"
    element = await get_element(driver, query, 30)
    element.clear()
    element.send_keys(username)

    await click_next(driver)


## find the password field and fill it in
async def fill_in_password(driver, password):
    query = "input[name='passwd'][aria-required='true']"
    element = await get_element(driver, query, 30)
    element.clear()
    element.send_keys(password)

    await click_next(driver)


## click on the stay signed in checkbox
async def fill_stay_signed_in(driver, api):
    checkbox_query = "#KmsiCheckboxField"
    element = await get_element(driver, checkbox_query, 30)
    element.click()

    await click_next(driver)

    await WaitModule.window_count(api, {
        "args": {
            "count": 1,
            "timeout": 60
        }
    })


## click on the login button
async def click_next(driver):
    query = "#idSIButton9"
    element = await get_element(driver, query, 30)
    element.click()


async def wait_for_main_page(driver):
    driver.switch_to.window(driver.window_handles[0])
    query = "view-container"
    await get_element(driver, query, 60)
