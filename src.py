from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import configparser
import os

config = configparser.ConfigParser()
config.read("config.ini")
nick = config["DEFAULT"]["nick"]
key = config["DEFAULT"]["key"]

path = os.path.dirname(__file__)
chromepath = path + "\\chromedriver.exe"
addon = path + "\\nopecha.crx"

def log(string):
    timer = "[" + time.strftime("%H:%M") + "]"
    print(timer, string)

def voteCzechCraft():
    driver.get("https://czech-craft.eu/server/skydrop/vote/")
    try:
        driver.find_element(By.ID, "privacy")
    except:
        try:
            driver.find_element(By.CSS_SELECTOR, ".alert.alert-error")
            log("CzechCraft - odhlasovano")
        except:
            log("Czechcraft - nefunguje stranka")
        return True

    try:
        time.sleep(3)
        WebDriverWait(driver, 180).until(EC.invisibility_of_element((By.CSS_SELECTOR,"iframe[title='recaptcha challenge expires in two minutes']")))
        driver.find_element(By.ID, "privacy").click()
        driver.find_element(By.ID, "username").send_keys(nick)

        driver.find_element(By.CSS_SELECTOR, "button.button").click() #vote button

        log("CzechCraft - hlasovani v poradku")
        return True
    except Exception as exc:
        #print(exc)
        log("CzechCraft - pri hlasovani doslo k chybe!")
        return False

def voteCraftList():
    driver.get("https://craftlist.org/skydropmc")
    try:
        driver.find_element(By.CSS_SELECTOR, '.btn.btn-vote').location_once_scrolled_into_view
        text = driver.find_element(By.CSS_SELECTOR, ".btn.btn-vote").text
    except:
        log("Craftlist - nefunguje stranka")
        return True

    if (text != "HLASOVAT ZA SERVER") and (text != "HLASOVAŤ ZA SERVER"):
        log("CraftList - odhlasovano")
        return True
    else:
        time.sleep(3)
        try:
            WebDriverWait(driver, 180).until(EC.invisibility_of_element((By.CSS_SELECTOR,"iframe[title='recaptcha challenge expires in two minutes']")))
            driver.find_element(By.CSS_SELECTOR, '.btn.btn-vote').click()
            driver.find_element(By.ID, 'frm-voteForm-nick').send_keys(nick)
            driver.find_element(By.NAME, '_submit').click() #vote button
            log("CraftList - hlasovani v poradku")
            return True
        except Exception as exc:
            log("CraftList - pri hlasovani doslo k chybe!")
            #log(exc)
            return False

#DEFAULT OPTIONS
options = Options()
options.add_argument('--start-maximized')
#options.add_argument('--no-sandbox')
options.add_argument('--disable-infobars')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option('excludeSwitches', ['enable-logging']) #disable error logging
options.add_extension(addon)
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--headless=new")

CZflag = 0
CRflag = 0

log("Script inicializovan")

while(True):
    
    driver = webdriver.Chrome(options=options, service=Service(chromepath))
    driver.get(f"https://nopecha.com/setup#{key}")
    if CZflag < 2: #TODO - neres to takovym obfuskovanim, ale zjisti kdyz stranka nejede!
        if CRflag == 0:
            if voteCzechCraft() == False:
                CZflag += 1
                driver.quit()
                continue
    else:
        log("CzechCraft stranka pravdepodobne nefunguje, nebo nelze vyresit Captcha!")

    if(CRflag < 2):
        if(voteCraftList() == False):
            CRflag += 1
            driver.quit()
            continue
    else:
        log("CraftList stranka pravdepodobne nefunguje, nebo nelze vyresit Captcha!")

    #log("Zkusim hlasovat znovu pro kontrolu")
    #voteCzechCraft()
    #voteCraftList()

    CZflag = 0
    CRflag = 0
    driver.quit()
    print("####################################")
    time.sleep(7200)
old.py