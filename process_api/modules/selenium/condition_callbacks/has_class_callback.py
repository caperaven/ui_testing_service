def has_class_callback(element, args):
    def _predicate(driver):
        classes = element.get_attribute("class")
        present = args.get("present", True)
        cls = args["classes"]

        # loop through array and see if the array item is in the classes text
        for c in cls:
            has_class = c in classes

            if has_class is True and present is False:
                return False

            if has_class is False and present is True:
                return False

        return True

    return _predicate
