from process_api.modules.selenium.condition_callbacks.__eval import _eval


def window_count_callback(element, args):
    def _predicate(driver):
        count = args.get("count", 0)
        length = len(driver.window_handles)

        return _eval(args, count, length)

    return _predicate

