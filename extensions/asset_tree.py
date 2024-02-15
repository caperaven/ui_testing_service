from selenium.common import NoSuchElementException, TimeoutException
from process_api.modules.selenium.automation.get import get_element
from process_api.utils.set_value import set_property_on_path


class AssetTreeModule:
    @staticmethod
    def register(api):
        api.add_module("asset-tree", AssetTreeModule)

    @staticmethod
    async def locate_element(api, step, ctx=None, process=None, item=None):
        api.logger.info(f'perform locate_element: {step["args"]["query"]}')

        args = step["args"]
        element = await api.call("selenium", "get", args, ctx, process, item)
        driver = api.get_variable("driver")

        parameters = {
            "id": args["element_id"],
            "type": args["element_type"]
        }
        # Execute the JavaScript function on the element
        driver.execute_script("arguments[0].expandToEntity.apply(arguments[0], arguments[1])", element, [parameters])

        data_id_value = f"{args['element_type']}_{args['element_id']}"

        # Locate the new element by its data-id attribute
        new_element = await find_tree_element(driver, data_id_value)
        element_info = None

        if new_element:
            element_info = {
                "tag_name": new_element.tag_name,
                "text": new_element.text,
                "location": new_element.location,
                "id": new_element.get_attribute("id"),
                "data_id": new_element.get_attribute("data-id")
            }

            # select the new element
            new_element.click()
        else:
            print("New element not found.")

        # Save the element information to a variable for next_step to use
        set_property_on_path(process, "parameters.found_element", element_info["data_id"])


async def find_tree_element(driver, data_id_value, timeout=30):
    """
    Find element by its data-id attribute value.
    """
    try:
        element = await get_element(driver, f"[data-id='{data_id_value}']", timeout)
        return element
    except TimeoutException:
        print(f"Element with data-id '{data_id_value}' not found within {timeout} seconds.")
        return None
    except NoSuchElementException:
        print(f"Element with data-id '{data_id_value}' not found.")
        return None
