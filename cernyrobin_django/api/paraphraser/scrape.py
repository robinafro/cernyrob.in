from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ChromeOptions

import time

def open_webpage_and_input_text(input_text):
    # create a new instance of the webdriver
    options = ChromeOptions()
    options.add_argument("--headless=chrome")
    driver = webdriver.Chrome(options=options)

    # navigate to the webpage you want to open
    driver.get("https://zerogpt.com/paraphraser")

    # wait for the text area element to load
    wait_time_seconds = 60
    wait = WebDriverWait(driver, wait_time_seconds)
    cookie_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "css-47sehv")))
    cookie_button.click()

    # find the text area element
    text_area = wait.until(EC.presence_of_element_located((By.TAG_NAME, "textarea")))

    # input the text into the text area
    text_area.send_keys(input_text)

    # selection dropdown field
    select_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "paraphraser-tone")))

    # create a Select object for the drop-down menu
    dropdown = Select(select_element)

    # select a value in the drop-down menu by visible text
    dropdown.select_by_visible_text("Teenager")

    # submit button
    button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "scoreButton")))
    button.click()

    # wait for the paraphrased text to load
    result_text = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "result-text")))

    prev_text = None
    while True:
        if prev_text == result_text.text:
            break
        prev_text = result_text.text
        
        time.sleep(2)

    result = {"success": True, "result": result_text.text}

    # when you're done, close the webdriver
    driver.quit()

    return result