from process_api.modules.selenium.modules.selenium_wait import WaitModule


class AssertModule:

    @staticmethod
    def register(api):
        api.add_module("assert", AssertModule)

    @staticmethod
    async def attributes(api, step, ctx=None, process=None, item=None):
        await WaitModule.attributes(api, step, ctx, process, item)

    @staticmethod
    async def attribute_eq(api, step, ctx=None, process=None, item=None):
        step["args"]["operator"] = "eq"
        await WaitModule.attribute(api, step, ctx, process, item)

    @staticmethod
    async def attribute_neq(api, step, ctx=None, process=None, item=None):
        step["args"]["operator"] = "neq"
        await WaitModule.attribute(api, step, ctx, process, item)

    @staticmethod
    async def has_attribute(api, step, ctx=None, process=None, item=None):
        await WaitModule.has_attribute(api, step, ctx, process, item)

    @staticmethod
    async def has_not_attribute(api, step, ctx=None, process=None, item=None):
        await WaitModule.has_not_attribute(api, step, ctx, process, item)

    @staticmethod
    async def child_count_eq(api, step, ctx=None, process=None, item=None):
        await WaitModule.child_count(api, step, ctx, process, item)

    @staticmethod
    async def child_count_neq(api, step, ctx=None, process=None, item=None):
        step["args"]["operator"] = "neq"
        await WaitModule.child_count(api, step, ctx, process, item)

    @staticmethod
    async def style_property_eq(api, step, ctx=None, process=None, item=None):
        await WaitModule.style_property(api, step, ctx, process, item)

    @staticmethod
    async def style_property_neq(api, step, ctx=None, process=None, item=None):
        step["args"]["operator"] = "neq"
        await WaitModule.style_property(api, step, ctx, process, item)

    @staticmethod
    async def element_property_eq(api, step, ctx=None, process=None, item=None):
        await WaitModule.element_property(api, step, ctx, process, item)

    @staticmethod
    async def element_property_neq(api, step, ctx=None, process=None, item=None):
        step["args"]["operator"] = "neq"
        await WaitModule.element_property(api, step, ctx, process, item)

    @staticmethod
    async def text_content_eq(api, step, ctx=None, process=None, item=None):
        await WaitModule.text_content(api, step, ctx, process, item)

    @staticmethod
    async def text_content_neq(api, step, ctx=None, process=None, item=None):
        step["args"]["operator"] = "neq"
        await WaitModule.text_content(api, step, ctx, process, item)

    @staticmethod
    async def value_eq(api, step, ctx=None, process=None, item=None):
        await WaitModule.text_value(api, step, ctx, process, item)

    @staticmethod
    async def value_neq(api, step, ctx=None, process=None, item=None):
        step["args"]["operator"] = "neq"
        await WaitModule.text_value(api, step, ctx, process, item)

    @staticmethod
    async def has_class(api, step, ctx=None, process=None, item=None):
        await WaitModule.has_class(api, step, ctx, process, item)

    @staticmethod
    async def has_not_class(api, step, ctx=None, process=None, item=None):
        await WaitModule.has_not_class(api, step, ctx, process, item)

    @staticmethod
    async def element_exists(api, step, ctx=None, process=None, item=None):
        await WaitModule.element(api, step, ctx, process, item)

    @staticmethod
    async def element_count_eq(api, step, ctx=None, process=None, item=None):
        await WaitModule.element_count(api, step, ctx, process, item)

    @staticmethod
    async def element_count_neq(api, step, ctx=None, process=None, item=None):
        step["args"]["operator"] = "neq"
        await WaitModule.element_count(api, step, ctx, process, item)

    @staticmethod
    async def element_not_exists(api, step, ctx=None, process=None, item=None):
        step["args"]["present"] = False
        await WaitModule.element(api, step, ctx, process, item)





