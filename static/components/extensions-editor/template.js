export const newTemplate = `class DefaultModule:
    @staticmethod
    def register(api):
        api.add_module("__name__", DefaultModule)

    @staticmethod
    async def sample_function(api, step, ctx=None, process=None, item=None):
        args = step["args"]

        value1 = args.get("value1", 0)
        value2 = args.get("value2", 0)

        value1 = await api.get_value(value1, ctx, process, item)
        value2 = await api.get_value(value2, ctx, process, item)
        return value1 + value2
`