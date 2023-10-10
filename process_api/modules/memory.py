import psutil

from process_api.utils.get_value import get_value


class MemoryModule:
    @staticmethod
    def register(api):
        api.add_module("memory", MemoryModule)

    @staticmethod
    async def get_process_memory(api, step, ctx=None, process=None, item=None):
        args = step.get("args")
        process_id = await get_value(args.get('id'), ctx, process, item)
        process = psutil.Process(process_id)
        memory_info = process.memory_full_info()
        return memory_info.uss / 1024 / 1024
