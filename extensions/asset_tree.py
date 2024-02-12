from telnetlib import EC

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from process_api.modules.selenium.automation.get import wait_for_element, get_element
from process_api.utils.set_value import set_property_on_path


class AssetTreeModule:
    @staticmethod
    def register(api):
        api.add_module("asset-tree", AssetTreeModule)

    @staticmethod
    async def test(api, step, ctx=None, process=None, item=None):
        args = step["args"]

        test = args.get("greeting1", "hello")
        value = args.get("greeting2", "world")

        await api.get_value(test, ctx, process, item)
        await api.get_value(value, ctx, process, item)

        return test + value

    @staticmethod
    async def locate_element(api, step, ctx=None, process=None, item=None):
        args = step["args"]

        query = args.get("query")
        element = await api.call("selenium", "get", args, ctx, process, item)

        print(f'element: {element}')
        driver = api.get_variable("driver")

        # Pass on 'item' values required to make search
        if driver is not None:

            parameters = {
                "id": args["element_id"],
                "type": args["element_type"]
            }
            # Execute the JavaScript function on the element
            driver.execute_script("arguments[0].viewInTree.apply(arguments[0], arguments[1])", element, [parameters])

            data_id_value = f"{args['element_type']}_{args['element_id']}"

            # Locate the new element by its data-id attribute
            new_element = await AssetTreeModule.find_tree_element(driver, data_id_value)

            element_info = None

            if new_element:
                element_info = {
                    "tag_name": new_element.tag_name,
                    "text": new_element.text,
                    "location": new_element.location,
                    "id": new_element.get_attribute("id"),
                    "data_id": new_element.get_attribute("data-id")
                    # Add more properties as needed
                }

                # select the new element
                new_element.click()
            else:
                print("New element not found.")

        # Save the element information to a variable for next_step to use
        if process is not None:
            set_property_on_path(process, "parameters.found_element", element_info["data_id"])

            print(f"Process info: {process}")

    @staticmethod
    async def find_tree_element(driver, data_id_value, timeout=10):
        """
        Find element by its data-id attribute value.
        """
        try:
            # Wait for the element to be visible
            element = await get_element(driver, f"[data-id='{data_id_value}']", timeout)
            return element
        except TimeoutException:
            print(f"Element with data-id '{data_id_value}' not found within {timeout} seconds.")
            return None
        except NoSuchElementException:
            print(f"Element with data-id '{data_id_value}' not found.")
            return None
