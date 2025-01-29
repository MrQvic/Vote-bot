from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging
import os

nick = "MrKvic_"

def check_recaptcha_solved(driver, wait) -> bool:
    try:
        # Přepnutí do iframe
        iframe = wait.until(EC.frame_to_be_available_and_switch_to_it(
            (By.XPATH, '//iframe[@title="reCAPTCHA"]')))
        logging.info("Přepnuto do reCAPTCHA iframe, čekám na vyřešení reCAPTCHA")

        # Kontrola checkboxu
        recaptcha_anchor = wait.until(EC.presence_of_element_located((By.ID, 'recaptcha-anchor')))
        wait.until(lambda driver: 'recaptcha-checkbox-checked' in recaptcha_anchor.get_attribute('class'))
        logging.info("reCAPTCHA checkbox označen")

        # Přepnutí zpět do hlavního kontextu
        driver.switch_to.default_content()
        return True

    except Exception as e:
        logging.error(f"Chyba při kontrole reCAPTCHA: {str(e)}")
        driver.switch_to.default_content()
        return False
    
def vote_minecraft_list(wait) -> bool:
    logging.info("Hlasování na Minecraft Listu")
    driver.get(f"https://www.minecraft-list.cz/server/goldskyblock-y5hf/vote?name={nick}")
    check_recaptcha_solved(driver, wait)
    try:
        gdpr = wait.until(EC.element_to_be_clickable((By.ID, 'tosgdpr')))
        gdpr.click()
        vote = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Odeslat']")))
        #if vote:
        #    logging.info("Hlasování na Minecraft Listu proběhlo úspěšně")
        #vote.click()
        return True

    except:
        logging.info("Minecraft List chyba, nejde hlasovat")
        return False
    
def vote_craftlist(wait) -> bool:
    logging.info("Hlasování na CraftListu")
    driver.get(f"https://craftlist.org/goldskyblock?nickname={nick}")
    check_recaptcha_solved(driver, wait)
    try:
        vote = wait.until(EC.element_to_be_clickable((By.NAME, '_submit')))
        if vote:
            logging.info("Hlasování na CraftListu proběhlo úspěšně")
        #vote.click()
        return True

    except:
        logging.info("CraftList chyba, nejde hlasovat")
        return False
    
def vote_minecraftservery(wait) -> bool:
    logging.info("Hlasování na Minecraft Servery")
    driver.get(f"https://minecraftservery.eu/server/goldskyblock-1171/vote/{nick}")
    time.sleep(10)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logging.getLogger('selenium').setLevel(logging.INFO)

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#extension_path = os.path.abspath("nopecha.crx")
#options.add_extension(extension_path)

# Inicializace driveru s automatickou instalací ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    wait = WebDriverWait(driver, 30)

    #vote_minecraft_list(wait)
    #vote_craftlist(wait)
    vote_minecraftservery(wait)

    time.sleep(5)
    driver.quit()

except Exception as e:
    logging.error(f"Došlo k chybě: {str(e)}")
    driver.quit()



#
    #vote_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-vote')))
    #driver.execute_script("arguments[0].click();", vote_button)
    #wait = WebDriverWait(driver, 30)

    ## Replace 'recaptcha-anchor' with the actual ID of the reCAPTCHA anchor element
    #iframe = wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iframe[@title="reCAPTCHA"]')))
    #logging.debug("Successfully switched to iframe")
    #recaptcha_anchor = wait.until(EC.presence_of_element_located((By.ID, 'recaptcha-anchor')))
#
    #wait.until(lambda driver: 'recaptcha-checkbox-checked' in recaptcha_anchor.get_attribute('class'))
    #logging.info("reCAPTCHA checkbox checked successfully.")
#
#
    #driver.switch_to.default_content()
    #driver.find_element(By.NAME, 'nickName').send_keys("nick")
    #print("hura2")