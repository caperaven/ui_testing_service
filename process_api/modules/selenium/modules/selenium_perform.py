from selenium.webdriver import Keys
from process_api.utils.utils import replace_server_url
from process_api.modules.selenium.automation.wait import get_element
import copy
import uuid


class PerformModule:

    @staticmethod
    def register(api):
        api.add_module("perform", PerformModule)

    @staticmethod
    async def navigate(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'perform navigate: {step["args"]["url"]}')
        step["args"]["url"] = replace_server_url(step["args"]["url"], api.state)
        await api.call("selenium", "goto", step["args"], ctx, process, item)

    @staticmethod
    async def close_window(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'perform close_window')
        await api.call("selenium", "close_driver", step, ctx, process, item)

    @staticmethod
    async def refresh(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'perform refresh')
        driver = api.variables["driver"]
        driver.refresh()

    @staticmethod
    async def click(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'perform click on {step["args"].get("query")}')
        args = copy.deepcopy(step["args"])
        args["action"] = "click"
        await api.call("selenium", "perform", args, ctx, process, item)

    @staticmethod
    async def dbl_click(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'perform dbl_click on {step["args"].get("query")}')
        args = copy.deepcopy(step["args"])
        args["action"] = "double_click"
        await api.call("selenium", "perform", args, ctx, process, item)

    @staticmethod
    async def context_click(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'perform context_click on {step["args"].get("query")}')
        args = copy.deepcopy(step["args"])
        args["action"] = "context_click"
        await api.call("selenium", "perform", args, ctx, process, item)

    @staticmethod
    async def click_sequence(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'perform click_sequence')
        args = step["args"]

        sequence = args["sequence"]
        for query in sequence:
            args = copy.deepcopy(step["args"])
            args["query"] = query
            args["action"] = "click"
            api.logger.info(f'click on {query}')
            await api.call("selenium", "perform", args, ctx, process, item)

    @staticmethod
    async def dbl_click_sequence(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'perform dbl_click_sequence')
        args = step["args"]

        sequence = args["sequence"]
        for query in sequence:
            args = copy.deepcopy(step["args"])
            args["query"] = query
            args["action"] = "double_click"
            api.logger.info(f'dbl_click on {query}')
            await api.call("selenium", "perform", args, ctx, process, item)

    @staticmethod
    async def press_key(api, step, ctx=None, process=None, item=None):
        args = copy.deepcopy(step["args"])
        key_value = args["key"].upper()

        api.logger.info(f'perform press_key {key_value} on {args.get("query")}')

        element = await api.call("selenium", "get", args, ctx, process, item)
        key = getattr(Keys, key_value)
        element.send_keys(key)

    @staticmethod
    async def print_screen(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'perform print_screen')

        args = copy.deepcopy(step["args"])
        args["folder"] = api.variables.get("folder", "./")
        args["action"] = "print_screen"
        await api.call("selenium", "perform", args, ctx, process, item)

    @staticmethod
    async def select_option(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'perform select_option {step["args"]}')

        args = copy.deepcopy(step["args"])
        args["action"] = "select_option"
        await api.call("selenium", "perform", args, ctx, process, item)

    @staticmethod
    async def switch_to_window(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'perform switch_to_window {step["args"]}')

        args = copy.deepcopy(step["args"])
        args["action"] = "switch_to_window"
        await api.call("selenium", "perform", args, ctx, process, item)

    @staticmethod
    async def switch_to_frame(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'perform switch_to_frame {step["args"]}')

        args = copy.deepcopy(step["args"])
        args["action"] = "switch_to_frame"
        await api.call("selenium", "perform", args, ctx, process, item)

    @staticmethod
    async def switch_to_default(api, step, ctx=None, process=None, item=None):
        if "args" in step:
            args = copy.deepcopy(step["args"])
        else:
            args = {}

        api.logger.info(f'perform switch_to_default {step["args"]}')

        args["action"] = "switch_to_default"
        await api.call("selenium", "perform", args, ctx, process, item)

    @staticmethod
    async def switch_to_tab(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'perform switch_to_tab {step["args"]}')

        args = copy.deepcopy(step["args"])
        args["action"] = "switch_to_tab"
        await api.call("selenium", "perform", args, ctx, process, item)

    @staticmethod
    async def type_text(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'perform type_text {step["args"]}')

        args = copy.deepcopy(step["args"])
        args["action"] = "type_text"
        await api.call("selenium", "perform", args, ctx, process, item)

    @staticmethod
    async def clear(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'perform clear {step["args"]}')

        args = copy.deepcopy(step["args"])
        args["action"] = "clear"
        await api.call("selenium", "perform", args, ctx, process, item)

    @staticmethod
    async def hover_over_element(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'perform hover_over_element {step["args"]}')

        args = copy.deepcopy(step["args"])
        args["action"] = "hover_over_element"
        await api.call("selenium", "perform", args, ctx, process, item)

    @staticmethod
    async def move_to(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'perform move_to {step["args"]}')

        args = copy.deepcopy(step["args"])
        args["action"] = "move_to"
        await api.call("selenium", "perform", args, ctx, process, item)

    @staticmethod
    async def move_by(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'perform move_by {step["args"]}')

        args = copy.deepcopy(step["args"])
        args["action"] = "move_by"
        await api.call("selenium", "perform", args, ctx, process, item)

    @staticmethod
    async def drag_and_drop(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'perform drag_and_drop {step["args"]}')

        driver = api.get_variable("driver")

        args = copy.deepcopy(step["args"])
        args["action"] = "drag_and_drop"
        args["target"] = await get_element(driver, args["target"], 10)
        await api.call("selenium", "perform", args, ctx, process, item)

    @staticmethod
    async def drag_and_drop_by(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'perform drag_and_drop_by {step["args"]}')

        args = copy.deepcopy(step["args"])
        args["action"] = "drag_and_drop_by"
        await api.call("selenium", "perform", args, ctx, process, item)

    @staticmethod
    async def drag_and_drop_by_offset(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'perform drag_and_drop_by_offset {step["args"]}')

        args = copy.deepcopy(step["args"])
        args["action"] = "drag_and_drop_by_offset"
        await api.call("selenium", "perform", args, ctx, process, item)

    @staticmethod
    async def set_uuid_variables(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'perform set_uuid_variables {step["args"]}')

        args = copy.deepcopy(step["args"])
        variables = args["variables"]

        for variable in variables:
            value = uuid.uuid4()
            await api.set_value(variable, str(value), ctx, process, item)

    @staticmethod
    async def properties_to_variables(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'perform properties_to_variables {step["args"]}')

        args = step["args"].copy()

        queries = args.keys()

        for query in queries:
            if query == "step":
                continue

            element = await api.call("selenium", "get", args, ctx, process, item)
            if element is not None:
                element_def = args[query]
                properties = element_def.keys()

                for prop in properties:
                    attr = element.get_property(prop)
                    prop = element_def[prop]
                    await api.set_value(prop, attr, ctx, process, item)

    # @staticmethod
    # async def drag_and_drop_by(api, step, ctx=None, process=None, item=None):
    #     api.logger.info(f'perform drag_and_drop_by {step["args"]}')
    #
    #     args = copy.deepcopy(step["args"])
    #     args["action"] = "drag_and_drop_by"
    #     await api.call("selenium", "perform", args, ctx, process, item)
    #
    # @staticmethod
    # async def drag_and_drop_by_offset(api, step, ctx=None, process=None, item=None):
    #     api.logger.info(f'perform drag_and_drop_by_offset {step["args"]}')
    #
    #     args = copy.deepcopy(step["args"])
    #     args["action"] = "drag_and_drop_by_offset"
    #     await api.call("selenium", "perform", args, ctx, process, item)
