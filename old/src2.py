from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import subprocess

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
    driver.get(f"https://www.minecraft-list.cz/server/goldskyblock-y5hf/vote?name={nick}")#/vote?name={nick}
    #time.sleep(30)
    possible = EC.presence_of_element_located((By.XPATH, "//button[text()='Odeslat']"))
    if not possible:
        logging.info("Minecraft List chyba, nejde hlasovat (možná už hlasoval?)")
        return False
    check_recaptcha_solved(driver, wait)
    try:
        gdpr = wait.until(EC.element_to_be_clickable((By.ID, 'tosgdpr')))
        gdpr.click()
        vote = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Odeslat']")))
        vote.click()
        # Vytvoření nového waitu s 2 sekundovým timeoutem
        short_wait = WebDriverWait(driver, 2)
        short_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".alert.alert-success")))
        logging.info("Hlasování na Minecraft Listu proběhlo úspěšně")
        return True

    except:
        logging.info("Minecraft List chyba, error při hlasování")
        return False
    
def vote_craftlist(wait) -> bool:
    logging.info("Hlasování na CraftListu")
    driver.get(f"https://craftlist.org/goldskyblock?nickname={nick}")
    time.sleep(2)
    try:
        text = driver.find_element(By.CSS_SELECTOR, ".btn.btn-block.btn-primary .row .col-12.col-md-8.text-center").text
    except:
        text = ""
    #print(text)
    if "NEXT POSSIBLE VOTE IN" in text:
        logging.info("CraftList chyba, nejde hlasovat (možná už hlasoval?)")
        return False
    check_recaptcha_solved(driver, wait)
    try:
        vote = wait.until(EC.element_to_be_clickable((By.NAME, '_submit')))
        vote.click()
        logging.info("Hlasování na CraftListu proběhlo úspěšně")
        return True

    except:
        logging.info("CraftList chyba, nejde hlasovat")
        return False
    
def vote_servery(wait) -> bool:
    driver.get(f"https://minecraftservery.eu/server/goldskyblock-1171/vote/{nick}")
    time.sleep(20)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logging.getLogger('selenium').setLevel(logging.INFO)

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
extension_path = os.path.abspath("nopecha.crx")
options.add_extension(extension_path)
options.add_argument("--headless=new")

# Inicializace driveru s automatickou instalací ChromeDriver
while True:
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        wait = WebDriverWait(driver, 70)

        driver.get(f"https://nopecha.com/setup#84o3kj1819c12tcw")

        vote_minecraft_list(wait)
        vote_craftlist(wait)
        #result = subprocess.run(["python", "other_script.py"], capture_output=True, text=True)
        #logging.info(f"Výstup z other_script.py: {result.stdout}")
        #subprocess.run(["python", "cloudflareBP.py"])

        time.sleep(1)
        driver.quit()

        # Wait for 2 hours (7200 seconds) before next iteration
        logging.info("Waiting 2 hours before next voting session...")
        time.sleep(7200)

    except Exception as e:
        logging.error(f"Došlo k chybě: {str(e)}")
        driver.quit()
        # Even if there's an error, wait 2 hours before retry
        time.sleep(7380)