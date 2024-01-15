from process_api.modules.selenium.modules.selenium_wait import WaitModule


class AssertModule:

    @staticmethod
    def register(api):
        api.add_module("assert", AssertModule)

    @staticmethod
    async def members(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'assert members: {step["args"]}')
        args = step["args"]

        query = args.get("query", None)
        attributes = args.get("attributes", None)
        styles = args.get("styles", None)
        properties = args.get("properties", None)
        classes = args.get("classes", None)
        text_content = args.get("text_content", None)

        if attributes:
            attr_step = {
                "args": {
                    "query": query,
                    "attributes": attributes
                }
            }

            await WaitModule.attributes(api, attr_step, ctx, process, item)

        if styles:
            style_step = {
                "args": {
                    "query": query,
                    "properties": styles
                }
            }

            await WaitModule.style_properties(api, style_step, ctx, process, item)

        if properties:
            prop_step = {
                "args": {
                    "query": query,
                    "properties": properties
                }
            }

            await WaitModule.element_properties(api, prop_step, ctx, process, item)

        if classes:
            class_step = {
                "args": {
                    "query": query,
                    "classes": classes
                }
            }

            await WaitModule.has_class(api, class_step, ctx, process, item)

        if text_content:
            text_step = {
                "args": {
                    "query": query,
                    "value": text_content
                }
            }

            await WaitModule.text_content(api, text_step, ctx, process, item)

    @staticmethod
    async def attributes(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'assert attributes: {step["args"]}')
        await WaitModule.attributes(api, step, ctx, process, item)

    @staticmethod
    async def attribute_eq(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'assert attribute_eq: {step["args"]}')
        step["args"]["operator"] = "eq"
        await WaitModule.attribute(api, step, ctx, process, item)

    @staticmethod
    async def attribute_neq(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'assert attribute_neq: {step["args"]}')
        step["args"]["operator"] = "neq"
        await WaitModule.attribute(api, step, ctx, process, item)

    @staticmethod
    async def has_attribute(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'assert has_attribute: {step["args"]}')
        await WaitModule.has_attribute(api, step, ctx, process, item)

    @staticmethod
    async def has_not_attribute(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'assert has_not_attribute: {step["args"]}')
        await WaitModule.has_not_attribute(api, step, ctx, process, item)

    @staticmethod
    async def child_count_eq(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'assert child_count_eq: {step["args"]}')
        await WaitModule.child_count(api, step, ctx, process, item)

    @staticmethod
    async def child_count_neq(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'assert child_count_neq: {step["args"]}')
        step["args"]["operator"] = "neq"
        await WaitModule.child_count(api, step, ctx, process, item)

    @staticmethod
    async def style_property_eq(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'assert style_property_eq: {step["args"]}')
        await WaitModule.style_property(api, step, ctx, process, item)

    @staticmethod
    async def style_property_neq(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'assert style_property_neq: {step["args"]}')
        step["args"]["operator"] = "neq"
        await WaitModule.style_property(api, step, ctx, process, item)

    @staticmethod
    async def element_property_eq(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'assert element_property_eq: {step["args"]}')
        await WaitModule.element_property(api, step, ctx, process, item)

    @staticmethod
    async def element_property_neq(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'assert element_property_neq: {step["args"]}')
        step["args"]["operator"] = "neq"
        await WaitModule.element_property(api, step, ctx, process, item)

    @staticmethod
    async def text_content_eq(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'assert text_content_eq: {step["args"]}')
        await WaitModule.text_content(api, step, ctx, process, item)

    @staticmethod
    async def text_content_neq(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'assert text_content_neq: {step["args"]}')
        step["args"]["operator"] = "neq"
        await WaitModule.text_content(api, step, ctx, process, item)

    @staticmethod
    async def value_eq(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'assert value_eq: {step["args"]}')
        await WaitModule.text_value(api, step, ctx, process, item)

    @staticmethod
    async def value_neq(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'assert value_neq: {step["args"]}')
        step["args"]["operator"] = "neq"
        await WaitModule.text_value(api, step, ctx, process, item)

    @staticmethod
    async def has_class(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'assert has_class: {step["args"]}')
        await WaitModule.has_class(api, step, ctx, process, item)

    @staticmethod
    async def has_not_class(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'assert has_not_class: {step["args"]}')
        await WaitModule.has_not_class(api, step, ctx, process, item)

    @staticmethod
    async def element_exists(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'assert element_exists: {step["args"]}')
        await WaitModule.element(api, step, ctx, process, item)

    @staticmethod
    async def element_count_eq(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'assert element_count_eq: {step["args"]}')
        await WaitModule.element_count(api, step, ctx, process, item)

    @staticmethod
    async def element_count_neq(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'assert element_count_neq: {step["args"]}')
        step["args"]["operator"] = "neq"
        await WaitModule.element_count(api, step, ctx, process, item)

    @staticmethod
    async def element_not_exists(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'assert element_not_exists: {step["args"]}')
        step["args"]["present"] = False
        await WaitModule.element(api, step, ctx, process, item)





