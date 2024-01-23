from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from process_api.modules.selenium.condition_callbacks import element_callback, element_usable_callback, light_and_shadow_dom_callback


async def get(driver, args):
    query = args.get("query", args.get("element", None))

    # If query is not provided, construct it from the structure
    if query is None:
        for key in args:
            if key != "query":
                query = key
                continue

    timeout = args.get("timeout", 10)
    ctx = args.get("context", driver)
    element = await get_element(ctx, query, timeout)

    if "attribute" in args:
        return element.get_attribute(args["attribute"])

    if "property" in args:
        return element.get_property(args["property"])

    return element



async def get_element(driver, query, timeout):
    if isinstance(query, WebElement):
        return query

    if isinstance(query, list):
        query = " ".join(query)

    if ' ' in query:
        return await get_element_on_path(driver, query, timeout)
    else:
        wait = WebDriverWait(driver, timeout, poll_frequency=0.1)

        element = wait.until(element_callback(None, {
            "query": query,
            "present": True
        }))

        return wait.until(element_usable_callback(element))



async def get_element_on_path(driver, query, timeout):
    queries = query.split(" ")
    wait = WebDriverWait(driver, timeout, poll_frequency=0.1)
    element = driver
    shadow_root = None

    for query in queries:
        if query == ">":
            continue

        element = wait.until(light_and_shadow_dom_callback(element, shadow_root, query))

        if element is None:
            return None

        shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)

    return element
