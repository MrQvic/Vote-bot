from seleniumbase import SB
import configparser
import time
import os
from utils import log, SLEEP_INTERVAL
from voters import vote_craftlist, vote_minecraft_list, vote_minecraftservery

# Načtení konfigurace
config = configparser.ConfigParser()
config.read("config.ini")
nick = config["DEFAULT"]["nick"]
nopecha_key = config["DEFAULT"]["nopecha_key"]

extension_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "addons", "nopecha"))
options = {
    "uc": True,
    "test": True,
    "locale_code": "en",
    "headless": True,
    "extension_dir": extension_path
}

extension_settings = f"https://nopecha.com/setup#awscaptcha_auto_open=false|awscaptcha_auto_solve=false|awscaptcha_solve_delay=true|awscaptcha_solve_delay_time=1000|disabled_hosts=|enabled=true|funcaptcha_auto_open=false|funcaptcha_auto_solve=false|funcaptcha_solve_delay=true|funcaptcha_solve_delay_time=1000|geetest_auto_open=false|geetest_auto_solve=false|geetest_solve_delay=true|geetest_solve_delay_time=1000|hcaptcha_auto_open=false|hcaptcha_auto_solve=true|hcaptcha_solve_delay=true|hcaptcha_solve_delay_time=3000|key={nopecha_key}|keys=|lemincaptcha_auto_open=false|lemincaptcha_auto_solve=false|lemincaptcha_solve_delay=true|lemincaptcha_solve_delay_time=1000|perimeterx_auto_solve=false|perimeterx_solve_delay=true|perimeterx_solve_delay_time=1000|recaptcha_auto_open=false|recaptcha_auto_solve=true|recaptcha_solve_delay=true|recaptcha_solve_delay_time=2000|textcaptcha_auto_solve=false|textcaptcha_image_selector=|textcaptcha_input_selector=|textcaptcha_solve_delay=true|textcaptcha_solve_delay_time=100|turnstile_auto_solve=false|turnstile_solve_delay=true|turnstile_solve_delay_time=1000"

while True:
    try:
        with SB(**options) as sb:
            sb.activate_cdp_mode()
            sb.open(extension_settings)

            log("Starting voting process...")
            MCvoted = vote_minecraftservery(sb, nick)
            Cvoted = vote_craftlist(sb, nick) 
            MLvoted = vote_minecraft_list(sb, nick)

    except KeyboardInterrupt:
        log("Script interrupted by user")
        break
    except Exception as e:
        log(f"Main loop Error: {str(e)}")

    print("Sleeping for 2 hours...")
    time.sleep(SLEEP_INTERVAL)