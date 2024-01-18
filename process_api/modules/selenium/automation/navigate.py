async def goto(driver, url):
    if driver.current_url != url:
        driver.get(url)