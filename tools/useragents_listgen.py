# Originally developed @ https://github.com/scripting-drafts/User-Agent-Scraper/
from selenium import webdriver
from sys import argv

script, input_file = argv
userAgents = open(input_file, 'w')

profile = webdriver.FirefoxProfile()
profile.set_preference("dom.webdriver.enabled", False)
profile.set_preference('useAutomationExtension', False)
profile.set_preference('privacy.trackingprotection.enabled', True)
profile.set_preference("browser.cache.disk.enable", False)
profile.set_preference("browser.cache.memory.enable", False)
profile.set_preference("browser.cache.offline.enable", False)
profile.set_preference("network.http.use-cache", False)
profile.update_preferences()
driver = webdriver.Firefox(profile)

driver.get("https://developers.whatismybrowser.com/useragents/explore/")
driver.find_element_by_link_text('Phone').click()
phones = driver.find_elements_by_class_name('useragent')
for phone in phones:
    userAgents.write(phone.text + '\n')
driver.back()
driver.find_element_by_link_text('Computer').click()
computers = driver.find_elements_by_class_name('useragent')
for computer in computers:
    userAgents.write(computer.text + '\n')
driver.back()
driver.find_element_by_link_text('Tablet').click()
tablets = driver.find_elements_by_class_name('useragent')
for tablet in tablets:
    userAgents.write(tablet.text + '\n')
driver.back()
driver.find_element_by_link_text('Android').click()
androids = driver.find_elements_by_class_name('useragent')
for android in androids:
    userAgents.write(android.text + '\n')
driver.back()
driver.find_element_by_link_text('iOS').click()
iOSes = driver.find_elements_by_class_name('useragent')
for iOS in iOSes:
    userAgents.write(iOS.text + '\n')
driver.back()
driver.find_element_by_link_text('Windows').click()
windows = driver.find_elements_by_class_name('useragent')
for window in windows:
    userAgents.write(window.text + '\n')

driver.quit()
