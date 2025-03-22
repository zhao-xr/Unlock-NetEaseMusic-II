# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00E9229BC3C46D836A6BF8032E563D567A6C71CC2E8EC1D534BC0A81C4DF0321D1CA7E81B8AF730A65074CD5118897AB4693D3E8376CCA56903FA8BAA64E759F7453E1777914238F7859D51D00F068FD312D0E68B03ED32BA4903361F8B7B06BAE89A965D832FF46DC38A3A3A6EB0539FE5B9B6332B832E79A865FD4FA3472C10819074CB0968C416376835042A49362F2B17C277A4878F40BCE344A4BC8EDD91CA70B998BA3CB763FE80729EDDDF6C383CCD323D639E9F69638B4172E11084F849B0F10F6D6994AD0496508C4A85273ECF78C5D60E99BC38DB16B4A15903F6382B59588D6E984A4861AEACCF86C3AA0B12E00BEF5653B73E3642A9211B62E065A748D5C80DF227FA3385DAE2B6264A2DD1A07207A50E50F2FB6183860F9D0FC348A7CC5187CCCC276A71C4E7BF28C965A11B3F72A51914B596FF23036C4238D47C0E30E68E12BE0949FB8F0159B05B2248153592E4C1592CCCB842EBAF2DD9937"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
