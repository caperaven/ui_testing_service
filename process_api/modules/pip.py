import subprocess

from process_api.utils.get_value import get_value


class PipModule:
    @staticmethod
    def register(api):
        api.register_action("pip", PipModule)

    @staticmethod
    async def install(api, step, ctx=None, process=None, item=None):
        args = step["args"]
        package_name = await get_value(args.get("source"), ctx, process, item)

        try:
            # Run the pip install command
            subprocess.check_call(['pip', 'install', package_name])
            return True
        except subprocess.CalledProcessError as e:
            return f"An error occurred while installing {package_name}: {e}"
