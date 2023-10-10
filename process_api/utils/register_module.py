# This registers a module based on a string value.
# For example, we can use the following string to register the data module:
# "process_api.modules.data:DataModule"
# In the schemas we can define what modules are required for this schema to function.
# Before running the schema we can make sure that the module is registered.

def register_module(api, path):
    parts = path.split(':')
    py_module = __import__(parts[0], fromlist=[parts[1]])
    cls = getattr(py_module, parts[1])
    instance = cls()
    instance.register(api)
