# selenium 3
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


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
        search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='azureSiteSearchTerm']")))

except TimeoutException:
    print("Search Box Not Found")
    driver.quit()

#Check if it is enabled and displayed

if search_box.is_enabled() and search_box.is_displayed():

    """This code below is problematic"""
    # driver.execute_script("arguments[0].scrollIntoView(true);", search_box)
    
    actions = ActionChains(driver=driver)
    actions.move_to_element(search_box).perform()    

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

# Wait for the search resuls to load
try:
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='b7b1c41a35e845c7afa0570b78c9ea93']/div/p")))
except TimeoutException :
    print("Search Results not Found")
    driver.quit()

# Going for the first link
try:
    first_link = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="b7b1c41a35e845c7afa0570b78c9ea93"]/div/ol/li[1]/h3/a')))
    link_title = first_link.text
    print(link_title)
    actions.move_to_element(first_link).click().perform()

    # Wait for the page to laod and get the disease name and symptoms
    disease_link = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="mayoform"]/div[5]/header/div/h1')))
    disease_name = disease_link.text
    print(disease_name)

    disease_symptoms_intro = driver.find_element(By.XPATH,'//*[@id="main-content"]/div[1]/div[1]/div[2]/p[5]').text
    print(disease_symptoms_intro)

    first_list = driver.find_element(By.CSS_SELECTOR, '#main-content > div:nth-child(1) > div.content > div:nth-child(2) > ul:nth-child(12)')
    disease_symptoms_list = first_list.find_element(By.XPATH,'//*[contains(text(), "symptoms")]')
    symptoms = disease_symptoms_list.find_elements(By.XPATH, '//*[contains(text(), "symptoms")]/following-sibling::ul[1]/li')

    disease_symptoms = []
    for symptom in symptoms:
        disease_symptoms.append(symptom.text)
        if symptom == symptom.find_element(By.TAG_NAME,'li')[1]:
            break
    # disease_symptoms = [symptom.text for symptom in symptoms]

    print(disease_symptoms)


    # print(disease_symptoms_intro)
    # print(disease_symptoms)



except NoSuchElementException :
    print("No such Element Found")
    driver.quit()

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