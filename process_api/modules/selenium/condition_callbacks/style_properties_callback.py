from process_api.modules.selenium.condition_callbacks.__eval import _eval


def style_properties_callback(element, args):
    def _predicate(driver):
        properties = args["properties"].keys()

        for prop in properties:
            exp_value = args["properties"][prop]
            value = element.value_of_css_property(prop)

            if not _eval(args, value, exp_value):
                return False

        return True

    return _predicate
