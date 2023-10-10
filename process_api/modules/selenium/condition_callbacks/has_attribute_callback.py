def has_attribute_callback(element, args):
    def _predicate(driver):
        exp_attr = args["attr"]
        present = args.get("present", True)
        has_attribute = element.get_attribute(exp_attr) is not None
        return has_attribute == present

    return _predicate
