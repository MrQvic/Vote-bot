#from functools import wraps
#
#def retry_vote(max_attempts=3):
#    def decorator(func):
#        @wraps(func)
#        def wrapper(*args, **kwargs):
#            attempts = 0
#            while attempts < max_attempts:
#                try:
#                    result = func(*args, **kwargs)
#                    if result:  # If vote successful
#                        return True
#                    attempts += 1
#                    if attempts < max_attempts:
#                        print(f"Retry attempt {attempts} for {func.__name__}")
#                        time.sleep(2)  # Brief delay between retries
#                except Exception as e:
#                    print(f"Error in {func.__name__}: {str(e)}")
#                    attempts += 1
#                    if attempts < max_attempts:
#                        print(f"Retry attempt {attempts} after error")
#                        time.sleep(2)
#            print(f"Failed after {max_attempts} attempts: {func.__name__}")
#            return False
#        return wrapper
#    return decorator
#
## Apply decorator to vote functions
#@retry_vote(max_attempts=3)
#def vote_minecraftservery(sb):
#    # ...existing code...
#
#@retry_vote(max_attempts=3)
#def vote_craftlist(sb):
#    # ...existing code...
#
#@retry_vote(max_attempts=3)
#def vote_minecraft_list(sb):
#    # ...existing code...
#
## Main execution remains the same
#with SB(**options) as sb:
#    sb.activate_cdp_mode()
#    # ...existing code...