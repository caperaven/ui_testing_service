from process_api.utils.run_step import run_step
from process_api.utils.get_value import get_value


class SystemModule:

    @staticmethod
    def register(api):
        api.add_module("system", SystemModule)

    @staticmethod
    async def template(api, step, ctx=None, process=None, item=None):
        args = step.get("args")
        schema = await get_value(args.get('schema'), ctx, process, item)
        process = await get_value(args.get('process', 'main'), ctx, process, item)
        parameters = await get_value(args.get('parameters'), ctx, process, item)

        schema = api.process_templates.get_template(schema)
        return await api.schema_runner.run_process(api, schema, process, ctx, parameters)
