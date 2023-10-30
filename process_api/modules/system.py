import subprocess
from process_api.utils.run_step import run_step
from process_api.utils.get_value import get_value

processes = {}


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

    @staticmethod
    async def run_command(api, step, ctx=None, process=None, item=None):
        args = step.get("args")
        id = await get_value(args.get('id'), ctx, process, item)
        command = await get_value(args.get('command'), ctx, process, item)
        cmd_args = await get_value(args.get('args'), ctx, process, item)
        cwd = await get_value(args.get('cwd'), ctx, process, item)

        stack = [command]

        if cmd_args:
            stack.extend(cmd_args)

        process = subprocess.Popen(stack, cwd=cwd)
        processes[id] = process

    @staticmethod
    async def kill_process(api, step, ctx=None, process=None, item=None):
        args = step.get("args")
        id = await get_value(args.get('id'), ctx, process, item)

        if id in processes:
            process = processes[id]
            process.kill()
            del processes[id]
