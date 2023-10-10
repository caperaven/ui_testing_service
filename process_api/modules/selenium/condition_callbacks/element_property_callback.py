from process_api.modules.selenium.condition_callbacks.__eval import _eval


def element_property_callback(element, args):
    def _predicate(driver):
        prop = args["property"]
        exp_value = args["value"]
        value = element.get_property(prop)

        return _eval(args, value, exp_value)

    return _predicate
