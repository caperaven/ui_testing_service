from process_api.modules.selenium.condition_callbacks.__eval import _eval


def element_properties_callback(element, args):
    def _predicate(driver):
        properties = args["properties"].keys()

        for prop in properties:
            exp_value = args["properties"][prop]
            value = element.get_property(prop)

            if _eval(args, value, exp_value) is False:
                return False

        return True

    return _predicate
