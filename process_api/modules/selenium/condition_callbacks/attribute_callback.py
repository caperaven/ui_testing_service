from process_api.modules.selenium.condition_callbacks.__eval import _eval


def attribute_callback(element, args):
    def _predicate(driver):
        value = element.get_attribute(args["attr"])
        exp_value = args["value"]
        return _eval(args, value, exp_value)

    return _predicate
