from seleniumbase import SB

nick = "MrKvic_"

# Konfigurace pro headless mód
options = {
    "uc": True,
    "test": True,
    "locale_code": "en",
    "headless": True  # přidáno pro headless mód
}
with SB(**options) as sb:
    url = f"https://minecraftservery.eu/server/goldskyblock-1171/vote/{nick}"
    sb.activate_cdp_mode(url)
    
    # Přidáno čekání na načtení captchy
    sb.sleep(2)
    #sb.uc_gui_click_captcha()
    
    # Click the "Odeslat hlas" button
    try:
        sb.click("button:contains('Odeslat hlas')")
    except Exception as e:
        print("Could not find or click the 'Odeslat hlas' button")
        print(e)