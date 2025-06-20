import time
from functools import wraps

VOTE_TIMEOUT = 90
SLEEP_INTERVAL = 7200  # 2 hours
MAX_RETRY_ATTEMPTS = 3

def retry(max_attempts=MAX_RETRY_ATTEMPTS, service_name=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            name = service_name or func.__name__.replace('vote_', '').replace('_', ' ').title()
            
            for attempt in range(1, max_attempts + 1):
                try:
                    log(f"{name} - Attempt {attempt}")
                    success = func(*args, **kwargs)
                    if success:
                        return True
                    elif attempt == max_attempts:
                        log(f"Failed to vote on {name} after {max_attempts} attempts.")
                        return False
                except Exception as e:
                    log(f"{name} - Error on attempt {attempt}: {str(e)}")
                    if attempt == max_attempts:
                        log(f"Failed to vote on {name} after {max_attempts} attempts.")
                        return False
            
            return False
        return wrapper
    return decorator

def log(string):
    timer = "[" + time.strftime("%H:%M") + "]"
    print(timer, string)

def click_cookie_button(sb):
    try:
        sb.click("button:contains('Yes, I will share')")
        log("Clicked the cookie button.")
    except:
        log("Unable to click the cookie button.")
    
def click_recaptcha_checkbox(sb):
    try:
        sb.switch_to_frame('iframe[title="reCAPTCHA"]')
        sb.wait_for_element('#recaptcha-anchor', timeout=10)
        checkbox = sb.find_element('#recaptcha-anchor')
        checkbox.click()
        sb.switch_to_default_content()
        return True
    except Exception as e:
        log(f"Error clicking reCAPTCHA checkbox: {str(e)}")
        sb.switch_to_default_content()
        return False

def check_recaptcha_solved(sb) -> bool:
    try:
        sb.switch_to_frame('iframe[title="reCAPTCHA"]')
        sb.wait_for_element('#recaptcha-anchor', timeout=10)
        checkbox = sb.find_element('#recaptcha-anchor')
        is_solved = 'recaptcha-checkbox-checked' in checkbox.get_attribute('class')
        sb.switch_to_default_content()
        return is_solved
    except Exception as e:
        log(f"Error checking reCAPTCHA: {str(e)}")
        sb.switch_to_default_content()
        return False
    
def wait_for_recaptcha(sb, timeout=60) -> bool:
    start_time = time.time()
    click_recaptcha_checkbox(sb)
    log("Waiting for reCAPTCHA to be solved...")
    while time.time() - start_time < timeout:
        if check_recaptcha_solved(sb):
            log("reCAPTCHA solved!")
            return True
        sb.sleep(1)
    log(f"Timeout after {timeout} seconds - reCAPTCHA not solved")
    return False