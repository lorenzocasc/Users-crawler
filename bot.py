import time
from Utility import Utility
from selenium import webdriver
from secrets import username, password

login_url = "https://www.tripadvisor.com/RegistrationController?flow=sign_up_and_save&returnTo=%2F&fullscreen=true&flowOrigin=login&hideNavigation=true&isLithium=true"

driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
driver.get(login_url)
time.sleep(10)

# i need to click on the login button that has no id

button = driver.find_element_by_css_selector(".ui_button.w100p.regEmailContinue.newRegFormButtonStyles.roundedRegFormButton.emailButtonMargin")
button.click()

time.sleep(10)

driver.find_element_by_id("regSignIn.email").send_keys(username)
driver.find_element_by_id("regSignIn.password").send_keys(password)
