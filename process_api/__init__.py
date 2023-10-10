"""
This library is dual-licensed under the MIT License for open-source and free usage
and a separate commercial license for closed-source and commercial use.
See LICENSE-MIT.txt and LICENSE-COMMERCIAL.txt for details.
"""

from process_api.process_runner import ProcessRunner
from process_api.schema_runner import SchemaRunnerManager
from process_api.modules import register
from process_api.process_logger import ProcessLogger
from process_api.process_templates import ProcessTemplates
import traceback

# This class is a wrapper around the ProcessRunner class.
# It is used to make the process_runner module more accessible.
# Since process steps can be called from anywhere in the code, including other modules,
# use the process variable to call process steps.
# The process api is the heart of the system that enables me to define modules.
# Those modules have functions and we need a way to call those functions to execute the intent.
class ProcessAPI:

    variables = {}
    break_on_error = False

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ProcessAPI, cls).__new__(cls)

        return cls.instance

    def __init__(self):
        self.process_runner = ProcessRunner()
        self.schema_runner = SchemaRunnerManager()
        self.process_templates = ProcessTemplates()
        self.logger = ProcessLogger()

    def set_variable(self, name, value):
        self.variables[name] = value

    def get_variable(self, name):
        return self.variables.get(name)

    def delete_variable(self, name):
        if name in self.variables:
            del self.variables[name]

    # This method is used to add a module to the process api.
    # The module is a class that contains functions that can be called from the process steps.
    # If you want to execute a step on a module but them module has not been registered yet,
    # you will get an error.
    def add_module(self, name, module):
        self.process_runner.modules[name] = module

    def add_template(self, template):
        self.process_templates.add_template(template)

    def load_templates_from_folder(self, folder):
        self.process_templates.load_from_folder(folder)

    # This method is used to call a process step.
    # You need to define the module using the step type for example "console"
    # You need to define the function name using the step action for example "log".
    # If you do not define a action, it will assume the action name is "perform"
    # You can pass arguments to the function using the step args.
    # In addition, if required by the step, you need to also define the context (ctx), process and item.
    async def call(self, step_type, step_action, step_args=None, ctx=None, process=None, item=None):
        if step_action is None:
            step_action = "perform"

        step = {
            "type": step_type,
            "action": step_action,
            "args": step_args
        }

        return await self.run(step, ctx, process, item)

    # This method is used to call a process step.
    # In this case you pass on a dictionary that defines the step, including the type, action and args.
    async def run(self, step, ctx=None, process=None, item=None, callback=None):
        try:
            return await self.process_runner.run_step(self, step, ctx, process, item, callback)
        except TimeoutError as e:
            self.logger.critical(str(e))
            self.logger.error(traceback.format_exc())
        except Exception as e:
            self.logger.critical(str(e))
            self.logger.error(traceback.format_exc())

    # This method is used to load a process schema definition from file and execute the schema as a whole.
    async def run_from_file(self, api, filename, ctx=None, parameters=None):
        return await self.schema_runner.run_from_file(api, filename, ctx, parameters)

    async def run_schema(self, schema, ctx=None, parameters=None, callback=None):
        return await self.schema_runner.run_schema(self, schema, ctx, parameters, callback)


process_api = ProcessAPI()
call = process_api.call
register(process_api)