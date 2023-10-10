from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from process_api.modules.selenium.automation.wait import wait


class DriverActions:
    @staticmethod
    async def init(browser, options=None):
        browser_fn = getattr(DriverActions, browser)

        if browser_fn is None:
            raise Exception(f"browser {browser} is not supported")

        driver = await browser_fn(options)

        if "goto" in options:
            url = options["goto"]
            driver.get(url)

        if "wait" in options:
            await wait(driver, {
                "query": options["wait"]
            })

        return driver

    @staticmethod
    async def close(driver):
        driver.close()

    @staticmethod
    async def chrome(options):
        opt = webdriver.ChromeOptions()
        opt.add_argument("start-maximized")
        opt.add_argument("ignore-certificate-errors")

        if options is not None and "arguments" in options:
            for arg in options["arguments"]:
                opt.add_argument(arg)

        driver_path = options["driver_path"]
        chrome_service = ChromeService(driver_path)
        driver = webdriver.Chrome(service=chrome_service, options=opt)
        driver.get("about:blank")

        return driver

    @staticmethod
    async def firefox(options):
        opts = webdriver.FirefoxOptions()

        if options is not None and "arguments" in options:
            for arg in options["arguments"]:
                opts.add_argument(arg)

        driver = webdriver.Firefox(options=opts)
        driver.maximize_window()
        driver.get("about:blank")
        return driver

    @staticmethod
    async def edge(options):
        pass

    @staticmethod
    async def safari(options):
        driver = webdriver.Safari()
        driver.maximize_window()
        driver.get("about:blank")
        return driver
