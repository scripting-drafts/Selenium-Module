from seleniumwire import webdriver
from selenium.webdriver.firefox.options import Options
import Turquoise_Logger


logg = Turquoise_Logger.Logger()
log = logg.logging()
initial_url = "https://www.google.com"

options = Options()
options.add_argument('--headless')
options.set_preference('dom.webnotifications.enabled', False)
options.set_preference('dom.push.enabled', False)
options.set_preference('dom.webdriver.enabled', False)
options.set_preference('useAutomationExtension', False)
options.set_preference('privacy.trackingprotection.enabled', True)
profile_path = open('profile_path', 'r').read()

driver = webdriver.Firefox(firefox_profile=profile_path, options=options)
driver.implicitly_wait(10)

def connection_attempts(initial_url=initial_url, attempts_count=2):
    '''Commits attempts_count connection attempts to the given initial_url'''
    error = None
    while attempts_count:
        try:
            driver.get(initial_url)
        except Exception as error:
            log.error(f'{error}')
        
        attempts_count -= 1

        if not error:
            attempts_num = attempts_count
            attempts_count = 0            
            log.debug(f'Realized in {attempts_num} attempts')
        elif attempts_count == 0:
            log.debug('Failed to connect')
        

def requests_vars_get():
    '''Outputs REQ (Request URL), STAT (Status Code) and CT (Content Type) within responses in requests'''
    for request in driver.requests:
        if request.response:
            log.error(
                f'REQ: {request.url}'
            )

            log.debug(
                f'STAT: {request.response.status_code}'
            )

            log.debug(
                'CT:' +  request.response.headers['content-type'] + '\n'
            )

connection_attempts()
requests_vars_get()

driver.quit()
