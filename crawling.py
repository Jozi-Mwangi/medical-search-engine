# selenium 3
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException


#Spinning up the driver
driver = webdriver.Chrome(ChromeDriverManager().install())

wait = WebDriverWait(driver=driver, timeout=15)
driver.get("https://www.mayoclinic.org/diseases-conditions")

# This helps us identify the name of the website we are currently crawling
title = driver.title
print(title)

#Waiting for the search Bar to become visible
search_box = None
try:
        search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='ctl03$ctl00$searchTerm']")))

except TimeoutException:
    print("Search Box Not Found")
    driver.quit()

#Check if it is enabled and displayed

if search_box.is_enabled() and search_box.is_displayed():
    driver.execute_script("arguments[0].scrollIntoView(true);", search_box)
    search_box.clear()

    #Sending the search query
    try:
        search_box.send_keys("Malaria")
        search_box.send_keys(Keys.RETURN)
    except ElementNotInteractableException:
        print("Could not interact with the search box")
        driver.quit()

else:
    print("Search Box is not displayed")
    driver.quit()
# driver.implicitly_wait(20)
# search_box.send_keys("Malaria")
# search_box.send_keys(Keys.RETURN)

# driver.implicitly_wait(10)

# #Finding links to the disease
# links = driver.find_elements(By.XPATH,'//*[@id="b7b1c41a35e845c7afa0570b78c9ea93"]/div/ol')
# link=links.find_element(By.XPATH, '//*[@id="b7b1c41a35e845c7afa0570b78c9ea93"]/div/ol/li[1]/h3/a')

# results = []
# print(link.get_attribute("class"))

# link.click()

# driver.implicitly_wait(30)
# disease_name = driver.find_element(By.TAG_NAME, "h1")
# print(disease_name.text)
# symptoms = driver.find_element(By.CSS_SELECTOR, ".section-summary li")
# symptoms = [s.text for s in symptoms]
# curing_methods = driver.find_element(By.CSS_SELECTOR, ".treatment-summary li")
# curing_methods = [c.text for c in curing_methods]

# result = {
#     "disease_name" : disease_name,
#     "symptoms" : symptoms,
#     "curing_methods" : curing_methods,
# }

# results.append(result)
# print(results)

driver.quit()   