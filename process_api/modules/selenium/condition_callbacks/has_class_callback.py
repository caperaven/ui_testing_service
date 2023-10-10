def has_class_callback(element, args):
    def _predicate(driver):
        classes = element.get_attribute("class")
        present = args.get("present", True)
        cls = args["class"]
        has_class = cls in classes
        return has_class == present

    return _predicate
