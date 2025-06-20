import requests
from datetime import datetime
from utils import retry, log, click_cookie_button, wait_for_recaptcha

def already_voted_craftlist(sb) -> bool:
    try:
        sb.find_element("button:contains('Hlasovat')", timeout=4)
        log("Vote on CraftList is available.")
        return False
    except:
        log("Cannot vote on CraftList - probably already voted.")
        return True

def already_voted_minecraft_list(nick):
    try:
        response = requests.get(f'https://www.minecraft-list.cz/api/server/goldskyblock-y5hf/player/{nick}/next-vote')
        data = response.json()
        next_vote_str = data['next_vote_at']
        next_vote = datetime.strptime(next_vote_str, '%Y-%m-%d %H:%M:%S')
        
        if next_vote <= datetime.now():
            return False  # Not voted yet
        else:
            return True  # Already voted
    except Exception as e:
        log(f"Error checking Minecraft List vote status: {str(e)}")
        return False
    
@retry(max_attempts=3, service_name="Minecraft List")
def vote_minecraft_list(sb, nick) -> bool:
    try:
        log("Entering Minecraft List...")
        if already_voted_minecraft_list(nick):
            log("Already voted on Minecraft List.")
            return True
        sb.open(f"https://www.minecraft-list.cz/server/goldskyblock-y5hf/vote?name={nick}")
        if wait_for_recaptcha(sb, timeout=90):
            log("Proceeding with vote on Minecraft List...")
            sb.click("#tosgdpr")
            sb.click("button:contains('Odeslat')")
            alert = sb.wait_for_element('//*[@id="about"]/div/div[1]/div', timeout=10)
            if "Tvůj hlas bude zpracován" in alert.text:
                log("Successfully voted on Minecraft List!")
                return True
            elif "Již si hlasoval. Znovu můžeš hlasovat" in alert.text:
                log("Already voted on Minecraft List!")
                return True
            else:
                log("Unknown alert message. How did we get here?")
                return False
    except Exception as e:
        log(f"Minecraft list - Error: {str(e)}")
        return False
    
@retry(max_attempts=3, service_name="CraftList")  
def vote_craftlist(sb, nick) -> bool:
    log("Entering CraftList...")
    sb.open(f"https://craftlist.org/goldskyblock?nickname={nick}")
    try:
        if already_voted_craftlist(sb):
            return True

        click_cookie_button(sb)
        if wait_for_recaptcha(sb, timeout=90):
            log("Proceeding with vote...")
            sb.click("button:contains('Hlasovat')")
            log("Vote on CraftList probably successful")
            return True
    except Exception as e:
        log(f"Craftlist - Error: {str(e)}")
        return False

@retry(max_attempts=3, service_name="MinecraftServery")
def vote_minecraftservery(sb, nick) -> bool:
    log("Entering MinecraftServery...")
    sb.uc_open_with_reconnect(f"https://minecraftservery.eu/server/goldskyblock-1171/vote/{nick}")
    try:
        sb.sleep(7)
        sb.click("button:contains('Odeslat hlas')")
        try:
            popup = sb.find_element("//div[contains(@class,'notification')]", timeout=2)
            if "Hlasovat můžete až v" in popup.text:
                log("Already voted on MinecraftServery.")
                return True
            elif "byl úspěšně odeslán" in popup.text:
                log("Vote on MinecraftServery successful.")
                return True
            elif "Pole captcha je povinné" in popup.text:
                log("Captcha bypass unsucessful.")
                return False
            else:
                log("Unknown error popup.")
                return False
        except Exception as e:
            log("MinecrafServery - No popup found - probably successful vote.")
            return True
    except Exception as e:
        log("Could not find or click the 'Odeslat hlas' button")
        log(e)
        return False