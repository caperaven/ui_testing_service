from process_api.modules.selenium.condition_callbacks.__eval import _eval


def selected_callback(element, args):
    def _predicate(driver):
        exp_value = args.get("value", False)
        value = element.is_selected()

        return _eval(args, value, exp_value)

    return _predicate
