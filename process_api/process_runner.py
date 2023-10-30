from process_api.utils.set_value import set_value
import os


class ProcessRunner:
    modules = {}

    def __init__(self):
        self.current_script_path = os.path.abspath(__file__)
        self.current_directory = os.path.dirname(self.current_script_path)

    async def run_step(self, api, step, ctx=None, process=None, item=None, callback=None):
        system_type = step.get('type')
        action = step.get('action')

        module = None
        if system_type in self.modules:
            module = self.modules[system_type]
        else:
            Exception(f"Module {system_type} not found.")

        if action is None:
            action = "perform"

        if hasattr(module, action):
            function = getattr(module, action)
            step["args"] = await inflate(api, step["args"], ctx, process, item)
            result = await function(api, step, ctx, process, item)

            args = step.get("args", None)

            if args is not None and "target" in args:
                await set_value(args.get('target'), result, ctx, process, item)

            if callback is not None:
                await callback(api, step, ctx, process, item)

            # perform the next step if there is one
            # and there was either no error or we are not breaking on error
            if "next_step" in step:
                if api.logger.error_count > 0 and api.break_on_error:
                    return result

                next_step_name = step["next_step"]
                api.logger.info(f'run step: "{next_step_name}"')
                next_step = process["steps"][next_step_name]
                next_step["name"] = next_step_name

                return await self.run_step(api, next_step, ctx, process, item, callback)

            return result
        else:
            api.logger.fatal(f"action '{action}' not found in the imported module '{system_type}'.")


async def inflate(api, args, ctx, process, item):
    if args is None:
        return None

    for key, value in args.items():
        if isinstance(value, str):
            args[key] = await api.get_value(value, ctx, process, item)

    return args
