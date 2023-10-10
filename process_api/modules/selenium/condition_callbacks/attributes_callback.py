from process_api.modules.selenium.condition_callbacks.__eval import _eval


def attributes_callback(element, args):
    def _predicate(driver):
        attributes = args["attributes"].keys()

        for attribute in attributes:
            exp_value = args["attributes"][attribute]
            value = element.get_attribute(attribute)

            if not _eval(args, value, exp_value):
                return False

        return True
    return _predicate
