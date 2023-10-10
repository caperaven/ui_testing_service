from process_api.modules.selenium.condition_callbacks.__eval import _eval


def style_property_callback(element, args):
    def _predicate(driver):
        prop = args['property']
        exp_value = args["value"]

        value = element.value_of_css_property(prop)
        return _eval(args, value, exp_value)

    return _predicate
