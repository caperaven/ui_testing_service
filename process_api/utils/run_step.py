# This is a utility function that runs a step in a process.
# If the step is a object it will run it as is, but if it is a string, it will look for the step in the process.
async def run_step(api, step, context, process, item):
    step_to_run = step

    if isinstance(step_to_run, str):
        step_to_run = process["steps"][step_to_run]

    await api.run(step_to_run, context, process, item)
