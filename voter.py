from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime, timedelta

################ VARIABLES ######################
key = "eabnivyuu0"                              #your nopeCHA key
chromepath = "C:\driver\chromedriver.exe"       #path to chromedriver
nick = "MrKvic_"                                #your minecraft username
#################################################

def log(string):
  timer = "[" + time.strftime("%H:%M") + "]"
  print(timer, string)

def key_set():
    driver.get(f'https://nopecha.com/setup#{key}')

def end():
    driver.close()
    driver.quit()

def can_on_czechcraft():
    string = None
    try:
        driver.get("https://czech-craft.eu/server/skydrop/vote/")
        foo = driver.find_element(By.ID, "username")
        return bool(foo), string
    except ConnectionError:
        log("Cant reach czechcraft website")
    except NoSuchElementException:
        string = driver.find_element(By.CSS_SELECTOR, ".alert.alert-error").text
        return False, string
    except Exception as e:
        print(e)
        print("error in can_on_czechcraft")
        return False, string

def vote_czechcraft():
    try:
        driver.get("https://czech-craft.eu/server/skydrop/vote/")
        time.sleep(12)
        driver.find_element(By.ID, "username").send_keys(nick)
        driver.find_element(By.ID, "privacy").click()
        driver.find_element(By.CSS_SELECTOR, "button.button").click()
        log("vote_czechcraft - code execution ok")
        return True
    except NoSuchElementException:
        print("NoSuchElementException in vote_czechcraft")
    except ElementClickInterceptedException:
        log("Captcha solution failed")
    except Exception as e:
        print(e)
        print("error in vote_czechcraft")
        return False

def can_on_craftlist():
    text = None
    try:
        driver.get("https://craftlist.org/skydropmc")
        text = driver.find_element(By.CSS_SELECTOR, ".btn.btn-block.btn-vote").text
        foo = bool(text == "Hlasovat za server")
        return foo, text
    except ConnectionError:
        log("Cant reach craftlist website")
    except NoSuchElementException:
        return False, text
    except Exception as e:
        print (e)
        print("error in can_on_craftlist")
        return False, text

def vote_craftlist():
    try:
        driver.get("https://craftlist.org/skydropmc")
        time.sleep(12)
        driver.find_element(By.CSS_SELECTOR, '.btn.btn-block.btn-vote').location_once_scrolled_into_view
        #driver.execute_script("window.scrollTo(0, 200)") 
        driver.find_element(By.CSS_SELECTOR, '.btn.btn-block.btn-vote').click()
        driver.find_element(By.ID, 'frm-voteForm-nickName').send_keys(nick)
        driver.find_element(By.NAME, '_submit').click()
        log("vote_craftlist - code execution ok")
        return True
    except ElementClickInterceptedException:
        log("Captcha solution failed")
    except Exception as e:
        print(e)
        print("error in vote_craftlist")
        return False

def pokusy():
    driver.get("https://czech-craft.eu/server/skydrop/vote/")
    foo = None
    try:
        foo = driver.find_element(By.CSS_SELECTOR, ".alert.alert-error")
    except:
        pass
    return bool(foo)

#DEFAULT OPTIONS
options = Options()
options.add_argument('--start-maximized')
options.add_argument('--no-sandbox')
options.add_argument('--disable-infobars')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option('excludeSwitches', ['enable-logging']) #disable error logging
options.add_argument("load-extension=C:\\Users\\adula\\AppData\\Local\\Google\\Chrome\\User Data\\Default\Extensions\\dknlfmjaanfblgfdfebhijalfmhmjjjo\\0.2.3_0")
options.add_argument("--headless=chrome")

czech_variable = 0
list_variable = 0

log("Script started")

while(True):
    #VARIABLE OPTIONS
    options.arguments.remove("load-extension=C:\\Users\\adula\\AppData\\Local\\Google\\Chrome\\User Data\\Default\Extensions\\dknlfmjaanfblgfdfebhijalfmhmjjjo\\0.2.3_0")
    driver = webdriver.Chrome(options=options, service=Service(chromepath))
    print( driver.service.is_connectable())

    can_on_list, list_time = can_on_craftlist()
    can_on_czech, czech_time = can_on_czechcraft()

    #if (list_time != "Hlasovat za server") and (list_time != None) and (czech_time != None):
    #    list_time = list_time[20:28]
    #    czech_time = czech_time[54:62]
    #    print(list_time.time.strftime("%H:%M"))

    #print(time.strftime("%D:%H:%M"))
    print( driver.service.is_connectable())
    end()
    print( driver.service.is_connectable())


    options.add_argument("load-extension=C:\\Users\\adula\\AppData\\Local\\Google\\Chrome\\User Data\\Default\Extensions\\dknlfmjaanfblgfdfebhijalfmhmjjjo\\0.2.3_0")
    driver = webdriver.Chrome(options=options, service=Service(chromepath))

    key_set()

    if can_on_list:
        czech_variable = 0
        vote_craftlist()
        time.sleep(5)
        fail, text = can_on_craftlist()
        if fail == False:
            log("Craftlist vote successful!")
        else:
            log("Craftlits vote unsuccessful, trying again..")
            list_variable += 1
            if list_variable == 5:
                log("Voting on craftlist failed 5 times in a row, check you setup or if your nopeCHA token is valid")
                end()
                break
                
            end()
            continue


    if can_on_czech:
        list_variable = 0
        vote_czechcraft()
        time.sleep(5)
        fail2, text2 = can_on_czechcraft()
        if fail2 == False:
            log("Czechcraft vote successful!")
        else:
            log("Czechcraft vote unsuccessful, trying again..")
            czech_variable += 1
            if czech_variable == 5:
                log("Voting on czechcraft failed 5 times in a row, check you setup or if your nopeCHA token is valid")
                end()
                break
            end()
            continue
    

    end()
    log("Vote on both servers ok, waitin until next voting is possible")
    print("---------------------------------------------------------------------------")
    time.sleep(7200)