from process_api.expressions.conditions import conditions
from process_api.utils.run_step import run_step


class ConditionModule:
    @staticmethod
    def register(api):
        api.add_module("condition", ConditionModule)

    @staticmethod
    async def perform(api, step, ctx=None, process=None, item=None):
        args = step.get("args")
        condition = args.get('condition')
        pass_step = args.get('pass_step')
        fail_step = args.get('fail_step')

        result = conditions.exec(condition, ctx, process, item)

        if result and pass_step:
            return await run_step(api, pass_step, ctx, process, item)

        if not result and fail_step:
            return await run_step(api, fail_step, ctx, process, item)


