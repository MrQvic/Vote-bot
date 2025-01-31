from seleniumbase import SB
import configparser
import time
import os
import random

# Načtení konfigurace
config = configparser.ConfigParser()
config.read("config.ini")
nick = config["DEFAULT"]["nick"]
nopecha_key = config["DEFAULT"]["nopecha_key"]

# Základní konfigurace
options = {
    "uc": True,
    "test": True,
    "locale_code": "en",
    "headless": True,
    "extension_dir": os.path.join(os.path.dirname(__file__), "data", "addons", "nopecha")
}
extension_settings = f"https://nopecha.com/setup#awscaptcha_auto_open=false|awscaptcha_auto_solve=false|awscaptcha_solve_delay=true|awscaptcha_solve_delay_time=1000|disabled_hosts=|enabled=true|funcaptcha_auto_open=false|funcaptcha_auto_solve=false|funcaptcha_solve_delay=true|funcaptcha_solve_delay_time=1000|geetest_auto_open=false|geetest_auto_solve=false|geetest_solve_delay=true|geetest_solve_delay_time=1000|hcaptcha_auto_open=false|hcaptcha_auto_solve=true|hcaptcha_solve_delay=true|hcaptcha_solve_delay_time=3000|key={nopecha_key}|keys=|lemincaptcha_auto_open=false|lemincaptcha_auto_solve=false|lemincaptcha_solve_delay=true|lemincaptcha_solve_delay_time=1000|perimeterx_auto_solve=false|perimeterx_solve_delay=true|perimeterx_solve_delay_time=1000|recaptcha_auto_open=false|recaptcha_auto_solve=true|recaptcha_solve_delay=true|recaptcha_solve_delay_time=2000|textcaptcha_auto_solve=false|textcaptcha_image_selector=|textcaptcha_input_selector=|textcaptcha_solve_delay=true|textcaptcha_solve_delay_time=100|turnstile_auto_solve=false|turnstile_solve_delay=true|turnstile_solve_delay_time=1000"

def log(string):
    timer = "[" + time.strftime("%H:%M") + "]"
    print(timer, string)

def click_cookie_button(sb):
    try:
        sb.click("button:contains('Yes, I will share')")
        log("Clicked the cookie button.")
    except:
        log("Unable to click the cookie button.")

def already_voted_craftlist(sb) -> bool:
    try:
        log("Checking if already voted on CraftList.")
        vote_button = sb.find_element("button:contains('Hlasovat')", timeout=4)
        #vote_button = sb.wait_for_element('//*[@id="voteModal"]/div/div/div[3]/a/span/span[1]', timeout=10)
        #if( "Další možný hlas za" in vote_button.text):
        #    log("Already voted on CraftList.")
        #    return True
        #log("Craftlis - Why am I here?")
        #log(vote_button.text)
        log("Vote on CraftList is available.")
        return False
    except:
        log("Cannot vote on CraftList.")
        return True
    
def click_recaptcha_checkbox(sb):
    try:
        # Switch to recaptcha iframe
        sb.switch_to_frame('iframe[title="reCAPTCHA"]')
        #log("Switched to reCAPTCHA iframe")

        # Wait for checkbox and click it
        sb.wait_for_element('#recaptcha-anchor', timeout=10)
        checkbox = sb.find_element('#recaptcha-anchor')
        checkbox.click()
        
        # Switch back to default content
        sb.switch_to_default_content()
        
        return True

    except Exception as e:
        log(f"Error clicking reCAPTCHA checkbox: {str(e)}")
        sb.switch_to_default_content()
        return False

def check_recaptcha_solved(sb) -> bool:
    try:
        # Switch to recaptcha iframe
        sb.switch_to_frame('iframe[title="reCAPTCHA"]')
        #log("Switched to reCAPTCHA iframe")

        # Wait for checkbox and check if solved
        sb.wait_for_element('#recaptcha-anchor', timeout=10)
        checkbox = sb.find_element('#recaptcha-anchor')
        
        # Check if recaptcha is solved
        is_solved = 'recaptcha-checkbox-checked' in checkbox.get_attribute('class')
        
        # Switch back to default content
        sb.switch_to_default_content()
        
        return is_solved

    except Exception as e:
        log(f"Error checking reCAPTCHA: {str(e)}")
        sb.switch_to_default_content()
        return False
    
def wait_for_recaptcha(sb, timeout=60) -> bool:
    start_time = time.time()
    click_recaptcha_checkbox(sb)
    while time.time() - start_time < timeout:
        if check_recaptcha_solved(sb):
            log("reCAPTCHA solved!")
            return True
        log("Waiting for reCAPTCHA to be solved...")
        sb.sleep(2)
    log(f"Timeout after {timeout} seconds - reCAPTCHA not solved")
    return False

def vote_craftlist(sb) -> bool:
    log("Entering CraftList...")
    sb.open(f"https://craftlist.org/goldskyblock?nickname={nick}")
    try:
        if not already_voted_craftlist(sb):
            click_cookie_button(sb)
            if wait_for_recaptcha(sb, timeout=90):
                log("Proceeding with vote...")
                sb.click("button:contains('Hlasovat')")
                log("Vote on CraftList probably successful")
                return False
            else:
                log("Failed to solve reCAPTCHA")
                return False
        else:
            log("Already voted on CraftList.")
            return True
    except Exception as e:
        log(f"Craftlist - Error: {str(e)}")
        return False
    
def vote_minecraft_list(sb) -> bool:
    try:
        log("Voting on Minecraft List...")
        sb.open(f"https://www.minecraft-list.cz/server/goldskyblock-y5hf/vote?name={nick}")
        if wait_for_recaptcha(sb, timeout=90):
            log("Proceeding with vote on Minecraft List...")
            sb.click("#tosgdpr")
            sb.click("button:contains('Odeslat')")
            sb.sleep(50)
            log("Successfully voted on Minecraft List!")
            return True
    except Exception as e:
        log(f"Minecraft list - Error: {str(e)}")

def vote_minecraftservery(sb) -> bool:
    log("Entering MinecraftServery...")
    sb.open(f"https://minecraftservery.eu/server/goldskyblock-1171/vote/{nick}")
    try:
        sb.sleep(5)
        sb.click("button:contains('Odeslat hlas')")
        try:
            popup = sb.find_element("//div[contains(@class,'notification')]", timeout=2)
            log(popup.text) #-> "Pole captcha je povinné" / "Hlasovat můžete až v 24:00" / ???
            if "Hlasovat můžete až v" in popup.text:
                log("Already voted on MinecraftServery.")
                return True
            elif "Pole captcha je povinné" in popup.text:
                log("Captcha bypass unsucessful.")
                return False
            else:
                log("Unknown error popup.")
                
                return False
        except Exception as e:
            log("MinecrafServery - No popup found - probably successful vote.")
            return False
    except Exception as e:
        log("Could not find or click the 'Odeslat hlas' button")
        log(e)
        return False

while True:
    try:
        with SB(**options) as sb:
            sb.activate_cdp_mode()
            sb.open(extension_settings)
            sb.open("https://nopecha.com/setup#84o3kj1819c12tcw")

            pokusy = 0

            # Vote on MinecraftServery
            while pokusy <= 3:
                try:
                    pokusy += 1
                    log("MinecraftServery - Attempt " + str(pokusy))
                    MCvoted = vote_minecraftservery(sb)
                    if MCvoted:
                        break
                    elif not MCvoted and pokusy == 3:
                        log("Failed to vote on MinecraftServery.")
                except Exception as e:
                    log(f"MinecraftServery - Error: {str(e)}")

            pokusy = 0
#
            while pokusy <= 3:
                try:
                    pokusy += 1
                    log("CraftList - Attempt " + str(pokusy))
                    Cvoted = vote_craftlist(sb) 
                    if Cvoted:
                        break
                    elif not Cvoted and pokusy == 3:
                        log("Failed to vote on CraftList.")
                except Exception as e:
                    log(f"CraftList - Error: {str(e)}")
#
            pokusy =0
            # Vote on Minecraft List
            while pokusy < 3:
                try:
                    pokusy += 1
                    log("Minecraft list - Attempt " + str(pokusy))
                    if vote_minecraft_list(sb):
                        break
                    else:
                        log("Failed to vote on Minecraft List.")
                except Exception as e:
                    log(f"Minecraft List - Error: {str(e)}")

    except Exception as e:
        log(f"Main loop Error: {str(e)}")

    print("Sleeping for 2 hours...")
    time.sleep(random.uniform(7500, 8000))
