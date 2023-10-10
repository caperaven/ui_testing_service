import time
from selenium.webdriver.support.ui import WebDriverWait
import copy

from process_api.modules.selenium.condition_callbacks import attribute_callback, attributes_callback, \
    style_property_callback, style_properties_callback, element_property_callback, element_properties_callback,\
    selected_callback, child_count_callback, window_count_callback, element_count_callback, has_attribute_callback, \
    has_class_callback, element_callback


async def wait_for_element_details(api, step, callback, ctx=None, process=None, item=None):
    args = copy.deepcopy(step["args"])
    step_args = {
        "element": args.get("query")
    }

    element = await api.call("selenium", "get", step_args, ctx, process, item)

    timeout = args.get("timeout", 10)
    selenium_driver = api.get_variable("driver")
    WebDriverWait(selenium_driver, timeout).until(callback(element, args))


class WaitModule:

    @staticmethod
    def register(api):
        api.add_module("wait", WaitModule)

    @staticmethod
    async def time(api, step, ctx=None, process=None, item=None):
        args = copy.deepcopy(step["args"])
        timeout = args.get("timeout", 1)
        time.sleep(timeout)

    @staticmethod
    async def is_ready(api, step, ctx=None, process=None, item=None):
        step["args"]["attr"] = "data-ready"
        step["args"]["value"] = "true"
        await WaitModule.attribute(api, step, ctx, process, item)

    @staticmethod
    async def element(api, step, ctx=None, process=None, item=None):
        args = copy.deepcopy(step["args"])
        await api.call("selenium", "get", args, ctx, process, item)

    @staticmethod
    async def attribute(api, step, ctx=None, process=None, item=None):
        await wait_for_element_details(api, step, attribute_callback, ctx, process, item)

    @staticmethod
    async def attributes(api, step, ctx=None, process=None, item=None):
        await wait_for_element_details(api, step, attributes_callback, ctx, process, item)

    @staticmethod
    async def style_property(api, step, ctx=None, process=None, item=None):
        await wait_for_element_details(api, step, style_property_callback, ctx, process, item)

    @staticmethod
    async def style_properties(api, step, ctx=None, process=None, item=None):
        await wait_for_element_details(api, step, style_properties_callback, ctx, process, item)

    @staticmethod
    async def element_property(api, step, ctx=None, process=None, item=None):
        await wait_for_element_details(api, step, element_property_callback, ctx, process, item)

    @staticmethod
    async def element_properties(api, step, ctx=None, process=None, item=None):
        await wait_for_element_details(api, step, element_properties_callback, ctx, process, item)

    @staticmethod
    async def text_content(api, step, ctx=None, process=None, item=None):
        step["args"]["property"] = "textContent"
        await wait_for_element_details(api, step, element_property_callback, ctx, process, item)

    @staticmethod
    async def text_value(api, step, ctx=None, process=None, item=None):
        step["args"]["property"] = "value"
        await wait_for_element_details(api, step, element_property_callback, ctx, process, item)

    @staticmethod
    async def selected(api, step, ctx=None, process=None, item=None):
        await wait_for_element_details(api, step, selected_callback, ctx, process, item)

    @staticmethod
    async def child_count(api, step, ctx=None, process=None, item=None):
        await wait_for_element_details(api, step, child_count_callback, ctx, process, item)

    @staticmethod
    async def element_count(api, step, ctx=None, process=None, item=None):
        await wait_for_element_details(api, step, element_count_callback, ctx, process, item)

    @staticmethod
    async def window_count(api, step, ctx=None, process=None, item=None):
        args = copy.deepcopy(step["args"])
        timeout = args.get("timeout", 10)
        selenium_driver = api.get_variable("driver")
        WebDriverWait(selenium_driver, timeout).until(window_count_callback(None, args))

    @staticmethod
    async def idle(api, step, ctx=None, process=None, item=None):
        step_args = {
            "element": "body[idle]"
        }

        element = await api.call("selenium", "get", step_args, ctx, process, item)

    @staticmethod
    async def has_attribute(api, step, ctx=None, process=None, item=None):
        step["args"]["present"] = True
        await wait_for_element_details(api, step, has_attribute_callback, ctx, process, item)

    @staticmethod
    async def has_not_attribute(api, step, ctx=None, process=None, item=None):
        step["args"]["present"] = False
        await wait_for_element_details(api, step, has_attribute_callback, ctx, process, item)

    @staticmethod
    async def has_class(api, step, ctx=None, process=None, item=None):
        step["args"]["present"] = True
        await wait_for_element_details(api, step, has_class_callback, ctx, process, item)

    @staticmethod
    async def has_not_class(api, step, ctx=None, process=None, item=None):
        step["args"]["present"] = False
        await wait_for_element_details(api, step, has_class_callback, ctx, process, item)

