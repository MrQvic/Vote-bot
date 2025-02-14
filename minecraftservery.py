from seleniumbase import SB
import time

nick = "MrKvic_"

# Konfigurace pro headless mód
options = {
    "uc": True,
    "test": True,
    "locale_code": "en",
    "headless": False  # přidáno pro headless mód
}

def log(string):
    timer = "[" + time.strftime("%H:%M") + "]"
    print(timer, string)


def vote_minecraftservery(sb) -> bool:
    log("Entering MinecraftServery...")
    sb.uc_open_with_reconnect(f"https://minecraftservery.eu/server/goldskyblock-1171/vote/{nick}")
    try:
        #sb.sleep(7)
        sb.uc_gui_click_captcha()
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
    

with SB(**options) as sb:
    pokusy = 0
    #
    ## Vote on MinecraftServery
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
#
#with SB(**options) as sb:
#    url = f"https://minecraftservery.eu/server/goldskyblock-1171/vote/{nick}"
#    sb.uc_open_with_reconnect(url)
#    sb.uc_gui_click_captcha()
#    
#    # Přidáno čekání na načtení captchy
#    sb.sleep(2)
#    #sb.uc_gui_click_captcha()
#    
#    # Click the "Odeslat hlas" button
#    try:
#        sb.click("button:contains('Odeslat hlas')")
#    except Exception as e:
#        print("Could not find or click the 'Odeslat hlas' button")
#        print(e)