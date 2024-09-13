from seleniumwire import webdriver
from selenium.webdriver.firefox.options import Options
import Turquoise_Logger

class SeleniumWireModule:
    def __init__(self):
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

        options.set_preference("browser.cache.disk.enable", False)
        options.set_preference("browser.cache.memory.enable", False)
        options.set_preference("browser.cache.offline.enable", False)
        options.set_preference("network.http.use-cache", False)

        # USER AGENT OPT
        # options.set_preference("intl.accept_languages", random.choice(localesList).lower())
        # options.set_preference('general.useragent.override', random.choice(userAgentList))

        profile_path = open('profile_path', 'r').read()

        driver = webdriver.Firefox(firefox_profile=profile_path, options=options)
        driver.implicitly_wait(10)
        log.debug(f'Webdriver is UP')

        self.log = log
        self.initial_url = initial_url
        self.driver = driver

    def healthcheck(self):
        '''1 Returns an int if dead and None if alive  
        2 Throws a WebDriverException if dead'''
        self.log.debug('Webdriver healthcheck going on')
        try:
            assert(self.driver.service.process.poll() == None)
            self.driver.service.assert_process_still_running()
            self.log.debug('The driver appears to be OK')
        except Exception as e:
            self.log.debug('The driver appears to be NOK')
            self.log.debug(f'{e}')
        
        return True

    def connection_attempt(self, attempts_count=2):
        '''Commits attempts_count connection attempts to the given initial_url'''
        error = None
        initial_url=self.initial_url

        while attempts_count:
            try:
                self.log.debug(f'Connect -> [{initial_url}]')
                self.driver.get(initial_url)
            except Exception as error:
                self.log.error(f'ERROR {error}')
            
            attempts_count -= 1

            if not error:
                attempts_num = attempts_count
                attempts_count = 0            
                self.log.debug(f'Realized in {attempts_num} attempts')
                is_connected = True
            elif attempts_count == 0:
                self.log.debug('Failed to connect')
                is_connected = False
            
        self.is_connected = is_connected

    def requests_vars_get(self):
        '''Outputs REQ (Request URL), STAT (Status Code) and CT (Content Type) within responses in requests'''
        print('\n' + 'Responses summary')
        if self.is_connected:
            for request in self.driver.requests:
                if request.response:
                    self.log.debug(f'REQ: {request.url}')
                    self.log.debug(f'STAT: {request.response.status_code}')
                    self.log.debug('CT:' +  request.response.headers['content-type'] + '\n')
        if not self.is_connected:
            self.log.debug('The driver is not available')

    def tearDown(self):
        self.driver.quit()

wm = SeleniumWireModule()
wm_is_up = wm.healthcheck()

if wm_is_up:
    is_connected = wm.connection_attempt()
    wm.requests_vars_get()

wm.tearDown()
