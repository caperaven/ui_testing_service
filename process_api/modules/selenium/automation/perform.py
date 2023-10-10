import time
import os
from selenium.common import StaleElementReferenceException
from selenium.webdriver import Keys, ActionChains
from process_api.modules.selenium.automation.get import get_element
from selenium.webdriver.support.ui import Select

async def perform(driver, args):
    timeout = args.get("timeout", 10)
    context = args.get("context", driver)
    query = args.get("query", None)

    # not all actions require an element
    if query is not None:
        element = await get_element(context, query, timeout)
    else:
        element = None

    action = args["action"]
    chain = ActionChains(driver)
    count = args.get("count", 1)

    if element is not None:
        await Actions.scroll_into_view(driver, element, chain, args)

    for i in range(count):
        try:
            await Actions.__dict__[action](driver, element, chain, args)
        except StaleElementReferenceException:
            time.sleep(1)
            await Actions.__dict__[action](driver, element, chain, args)
            pass


class Actions:
    @staticmethod
    async def click(driver, element, chain, args=None):
        element.click()

    @staticmethod
    async def double_click(driver, element, chain, args=None):
        action = chain.double_click(element)
        action.perform()

    @staticmethod
    async def context_click(driver, element, chain, args=None):
        action = chain.context_click(element)
        action.perform()

    @staticmethod
    async def clear(driver, element, chain, args=None):
        element.clear()

    @staticmethod
    async def type_text(driver, element, chain, args):
        element.clear()
        time.sleep(0.1)
        element.send_keys(args["value"])
        time.sleep(0.25)
        element.send_keys(Keys.ENTER)

    @staticmethod
    async def hover(driver, element, chain, args=None):
        chain.move_to_element(element).perform()

    @staticmethod
    async def key_down(driver, element, chain, args=None):
        key = args.get("key")

        if key is not None:
            chain.key_down(key).perform()

        keys = args.get("keys")
        if keys is not None:
            for key in keys:
                chain.key_down(key).perform()

    @staticmethod
    async def key_up(driver, element, chain, args=None):
        key = args["key"]
        chain.key_up(key).perform()

    @staticmethod
    async def scroll_into_view(driver, element, chain, args):
        driver.execute_script("arguments[0].scrollIntoView();", element)

    @staticmethod
    async def move_to(driver, element, chain, args):
        # get target position
        x = args["x"]
        y = args["y"]

        # move to target
        chain.move_to_element(element).click_and_hold(element).move_by_offset(x, y).release().perform()

    @staticmethod
    async def move_by(driver, element, chain, args):
        # get current position
        current_x = element.location["x"]
        current_y = element.location["y"]

        # get target position
        x = args["x"]
        y = args["y"]

        # calculate offset
        offset_x = current_x + x
        offset_y = current_y + y

        # move to target
        element.move_by_offset(offset_x, offset_y).perform()

    @staticmethod
    async def drag_and_drop(driver, element, chain, args):
        target = args["target"]
        element.drag_and_drop(target)

    @staticmethod
    async def drag_and_drop_by(driver, element, chain, args):
        x = args.get("x", 0)
        y = args.get("y", 0)
        element.drag_and_drop_by(x, y)

    @staticmethod
    async def drag_and_drop_by_offset(driver, element, chain, args):
        x = args.get("x", 0)
        y = args.get("y", 0)
        element.drag_and_drop_by_offset(x, y)

    @staticmethod
    async def send_keys(driver, element, chain, args):
        keys = args["keys"]
        element.send_keys(keys)

    @staticmethod
    async def hover_over_element(driver, element, chain, args):
        action = ActionChains(driver)
        action.move_to_element(element).perform()

    @staticmethod
    async def switch_to_window(driver, element, chain, args):
        index = args.get("index", None)

        window_handles = driver.window_handles
        if index is not None:
            return driver.switch_to.window(window_handles[index])

    @staticmethod
    async def switch_to_frame(driver, element, chain, args):
        driver.switch_to.frame(element)

    @staticmethod
    async def switch_to_default(driver, element, chain, args):
        driver.switch_to.default_content()

    @staticmethod
    async def switch_to_tab(driver, element, chain, args):
        index = args.get("index", 0)
        driver.switch_to.window(driver.window_handles[index])

    @staticmethod
    async def print_screen(driver, element, chain, args):
        file = args.get("file", "untitled.png")
        folder = args.get("folder", "./")
        file = os.path.join(folder, file)
        driver.get_screenshot_as_file(file)

    @staticmethod
    async def select_option(driver, element, chain, args):
        select = Select(element)
        select.select_by_value(args["value"])
