import json
from process_api.utils.register_module import register_module

# Purpose: SchemaRunner class
# Run processes using a json file to define the intent.
# You can register schemas and templates to be used in the json file.
# Templates define reusable processes.
# You can also add a schema to the store if you want to use a greater schema to call other processes.


async def process_parameters(process, parameters):
    parameters_def = process.get("parameters_def")
    schema_parameters = {}

    for parameter_name in parameters_def.keys():
        parameter = parameters_def[parameter_name]
        data_type = parameter.get("type", "string")
        required = parameter.get("required", False)

        value = parameters.get(parameter_name, None)

        if value is None and required:
            raise Exception(f"Parameter '{parameter_name}' is required.")

        if data_type == "string" and isinstance(value, str) is False:
            raise Exception(f"Parameter '{parameter_name}' must be a string.")

        if data_type == "number" and isinstance(value, int) is False:
            raise Exception(f"Parameter '{parameter_name}' must be a number.")

        if data_type == "boolean" and isinstance(value, bool) is False:
            raise Exception(f"Parameter '{parameter_name}' must be a boolean.")

        if data_type == "object" and isinstance(value, dict) is False:
            raise Exception(f"Parameter '{parameter_name}' must be an object.")

        if data_type == "array" and isinstance(value, list) is False:
            raise Exception(f"Parameter '{parameter_name}' must be an array.")

        schema_parameters[parameter_name] = value

    process["parameters"] = schema_parameters


async def run_process(api, schema, process_name, ctx=None, parameters=None, item=None, callback=None):
    process = schema.get(process_name, None)

    # make a copy of the process
    process = process.copy()

    if "parameters_def" in process:
        await process_parameters(process, parameters)
        del process["parameters_def"]

    start_step = process["steps"]["start"]
    start_step["name"] = "start"
    api.logger.info('run step: "start"')
    return await api.run(start_step, ctx, process, item, callback)


async def run_schema(api, schema, ctx=None, parameters=None, callback=None):
    api.logger.info(f'run schema: "{schema.get("id", "unknown")}"')

    sequence = schema.get('sequences', None)
    required_modules = schema.get('required_modules', None)

    if required_modules is not None:
        for module_path in required_modules:
            register_module(api, module_path)

    if sequence is not None:
        result = None
        for process in sequence:
            api.logger.info(f'run process: "{process["process"]}"')
            result = await run_process(api, schema, process["process"], ctx, parameters, None, callback)

        return result

    elif "main" in schema:
        api.logger.info(f'run process: "main"')
        return await run_process(api, schema, "main", ctx, parameters, None, callback)


async def load_json(file_path):
    try:
        file = open(file_path, 'r')
        json_data = json.load(file)
        file.close()

        return json_data
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


class SchemaRunnerManager:
    templates = {}
    schemas = {}

    async def run_from_file(self, api, filename, ctx=None, parameters=None):
        schema = await load_json(filename)
        return await self.run_schema(api, schema, ctx, parameters)

    async def run_schema(self, api, schema, ctx=None, parameters=None, callback=None):
        return await run_schema(api, schema, ctx, parameters, callback)

    async def run_process(self, api, schema, process_name, ctx=None, parameters=None):
        return await run_process(api, schema, process_name, ctx, parameters)

    async def add_schema(self, schema):
        name = schema.get('id')
        self.schemas[name] = schema

    async def remove_schema(self, name):
        del self.schemas[name]

    async def clear_schemas(self):
        self.schemas = {}

    async def add_template(self, template):
        name = template.get('id')
        self.templates[name] = template

    async def remove_template(self, name):
        del self.templates[name]

    async def clear_templates(self):
        self.templates = {}

