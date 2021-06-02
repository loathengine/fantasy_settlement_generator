import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


options = Options()
options.binary = FirefoxBinary()
options.headless = False
#options.add_argument = '-P "Default User"'
options.profile = "/home/loath-engine/.mozilla/firefox/tzpeca6w.Default User"

driver = webdriver.Firefox(executable_path='driver/geckodriver', options=options)
driver.firefox_profile.path
driver.set_window_position(0, 0)
driver.set_window_size(1024, 1098)
#driver.get('http://fantasycities.watabou.ru/?size=22&seed=1865174529&hub=0&random=0&elevation=1&green=1&farms=1&citadel=1&urban_castle=1&plaza=1&temple=1&walls=1&shantytown=1&river=1&coast=1&sea=1.222333673025637')
driver.get('http://fantasycities.watabou.ru/')
cookies = driver.get_cookies()
for cookie in cookies:
    print(cookie)

print("Headless Firefox Initialized")
#time.sleep(8)
#screenshot = driver.save_screenshot('web/cities/' + str(seed) + '.png')
#driver.get("http://google.com/")
#driver.quit()




#import os

#from selenium import webdriver

#fp = webdriver.FirefoxProfile()

#fp.set_preference("browser.download.folderList",2)
#fp.set_preference("browser.download.manager.showWhenStarting",False)
#fp.set_preference("browser.download.dir", os.getcwd())
#fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")

#browser = webdriver.Firefox(firefox_profile=fp)
#browser.get("http://pypi.python.org/pypi/selenium")
#browser.find_element_by_partial_link_text("selenium-2").click()


