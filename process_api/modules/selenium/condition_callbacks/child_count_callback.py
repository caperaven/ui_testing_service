from process_api.modules.selenium.condition_callbacks.__eval import _eval
from selenium.webdriver.common.by import By


def child_count_callback(element, args):
    def _predicate(driver):
        count = args.get("count", 0)
        elements = element.find_elements(By.CSS_SELECTOR, "*")
        exp_count = len(elements)

        return _eval(args, count, exp_count)

    return _predicate

