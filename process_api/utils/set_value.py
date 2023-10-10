from process_api.utils.prefixes import CONTEXT_PREFIX, PROCESS_PARAMETERS_PREFIX, PROCESS_DATA_PREFIX, ITEM_PREFIX


# set a value on a path for a given context, process, or item
# depending on the prefix of the path string (e.g. $c{, $p{, $d{, $i{) the value will be set on the context,
# process parameters, process data, or item
async def set_value(path, value, context, process, item):
    if path is None:
        return

    # if the path starts with $c{, then it is a context variable
    if path.startswith(CONTEXT_PREFIX) and context is not None:
        set_property_on_path(context, path[3:-1].split("."), value)
        return

    # if the path starts with $p{, then it is a process parameters variable
    if path.startswith(PROCESS_PARAMETERS_PREFIX) and process is not None:
        # set the parameters property if it does not exist
        if not hasattr(process, "parameters"):
            process["parameters"] = {}

        set_property_on_path(process["parameters"], path[3:-1].split("."), value)

    # if the path starts with $d{, then it is a process data variable
    if path.startswith(PROCESS_DATA_PREFIX) and process is not None:
        # set the data property if it does not exist
        if not hasattr(process, "data"):
            process["data"] = {}

        set_property_on_path(process["data"], path[3:-1].split("."), value)

    # if the path starts with $i{, then it is an item variable
    if path.startswith(ITEM_PREFIX) and item is not None:
        set_property_on_path(item, path[3:-1].split("."), value)


# set a property on a path for a given object.
# this is a recursive function and it will create dictionaries as needed
def set_property_on_path(obj, path, value):
    if obj is None or path is None or len(path) == 0:
        return

    if len(path) == 1:
        if isinstance(obj, dict):
            obj[path[0]] = value
        else:
            setattr(obj, path[0], value)
        return

    if isinstance(obj, dict):
        if obj.get(path[0]) is None:
            obj[path[0]] = {}
    else:
        if getattr(obj, path[0]) is None:
            setattr(obj, path[0], {})

    set_property_on_path(obj[path[0]], path[1:], value)