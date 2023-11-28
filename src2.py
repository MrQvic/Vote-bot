from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

# Use the webdriver in the same folder as the script
driver_path = 'chromedriver.exe'  # Update this with the filename of your webdriver executable
url = 'https://craftlist.org/skydropmc'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logging.getLogger('selenium').setLevel(logging.INFO)

options = webdriver.chrome.options.Options()
options.add_extension('nopecha.crx')


# Create a new instance of the webdriver
driver = webdriver.Chrome(options=options, executable_path=driver_path)

# Open the website
driver.get(url)

# Wait for the button to be clickable (you can adjust the timeout as needed)
wait = WebDriverWait(driver, 10)
vote_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-vote')))

driver.execute_script("arguments[0].click();", vote_button)

wait = WebDriverWait(driver, 30)

# Replace 'recaptcha-anchor' with the actual ID of the reCAPTCHA anchor element
iframe = wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iframe[@title="reCAPTCHA"]')))
logging.debug("Successfully switched to iframe")
recaptcha_anchor = wait.until(EC.presence_of_element_located((By.ID, 'recaptcha-anchor')))

wait.until(lambda driver: 'recaptcha-checkbox-checked' in recaptcha_anchor.get_attribute('class'))
logging.info("reCAPTCHA checkbox checked successfully.")


driver.switch_to.default_content()
driver.find_element(By.NAME, 'nickName').send_keys("nick")
#print("hura2")


# Optionally, you can wait for a few seconds to see the result
time.sleep(5)

# Close the browser window
driver.quit()