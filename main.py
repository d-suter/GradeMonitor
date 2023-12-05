from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json
import logging
import traceback
from parse_grades import parse_grades
from otp import generate_otp
from webhook import send_discord_message

logging.basicConfig(level=logging.INFO)

def main():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    service = ChromeService(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    def perform_login():
        logging.info("Opening login page.")
        driver.get('https://gibz.zg.ch/login/sls/auth?cmd=auth-t')
        time.sleep(1)

        logging.info("Entering username.")
        username_input = driver.find_element(By.NAME, 'userid')
        username_input.send_keys(config['username'])
        time.sleep(1)

        logging.info("Entering password.")
        password_input = driver.find_element(By.NAME, 'password')
        password_input.send_keys(config['password'])
        time.sleep(1)

        logging.info("Submitting the login form.")
        login_button = driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-primary')
        login_button.click()
        time.sleep(3)

        otp_code = generate_otp(config['otp_secret'])
        logging.info(f"Generated OTP: {otp_code}")
        otp_input = driver.find_element(By.NAME, 'challenge')
        otp_input.send_keys(otp_code)

        logging.info("Submitting OTP.")
        otp_button = driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-primary')
        otp_button.click()

        time.sleep(3)

    perform_login()

    try:
        while True:
            current_url = driver.current_url
            if current_url.startswith('https://gibz.zg.ch'):

                #Navigating to the 'Noten' page.
                noten_button = driver.find_element(By.ID, 'menu21311')
                noten_button.click()
                time.sleep(2)

                #Navigating back to the 'Start' page
                start_button = driver.find_element(By.ID, 'menu1')
                start_button.click()
                time.sleep(2)

                # Check for new grades
                page_source = driver.page_source
                new_grades = parse_grades(page_source)

                if new_grades:
                    send_discord_message(config['discord_webhook_url'], new_grades)
                else:
                    logging.info("No new grades found.")
            else:
                logging.info("Not on the correct page, logging in again.")
                perform_login()

            time.sleep(60)

    except Exception as e:
        logging.error(f"An error occurred: {traceback.format_exc()}")
    finally:
        driver.quit()

if __name__ == "__main__":
    while True:
        main()
        logging.info("Restarting the process after an error or browser closure.")
        time.sleep(10)
