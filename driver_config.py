from selenium.webdriver.chrome.options import Options

def driver_delay(driver, delay=30):
    driver.implicitly_wait(delay)

def driver_options():
    options = Options()
    options.add_argument("--headless")

    return options
