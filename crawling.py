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
        search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='search-input-globalsearch-901d11d458']")))

except TimeoutException:
    print("Search Box Not Found")
    driver.quit()

#Check if it is enabled and displayed

if search_box.is_enabled() and search_box.is_displayed():

    actions = ActionChains(driver=driver)
    actions.move_to_element(search_box).perform()    

    #Sending the search query
    search_box.clear()
    try:
        search_box.send_keys("covid-19")
        search_box.send_keys(Keys.RETURN)
    except ElementNotInteractableException:
        print("Could not interact with the search box")
        driver.quit()

else:
    print("Search Box is not displayed")
    driver.quit()


# Wait for the search resuls to load
# Going for the first link
try:
    first_link=wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='cmp-skip-to-main__content']/ul/li/h3/div/a")))
    link_title = first_link.text
    print(link_title)
    # driver.execute_script("arguments[0].click()", first_link)

    # actions.move_to_element(first_link).perform()
    disease_window = driver.current_window_handle
    actions.key_down(Keys.CONTROL).click(first_link).key_up(Keys.CONTROL).perform()
    wait.until(EC.number_of_windows_to_be(2))
    driver.switch_to.window(driver.window_handles[1])

    try:

        # Wait for the page to laod and get the disease name and symptoms
        # disease_link = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="mayoform"]/div[5]/header/div/h1')))
        disease_link = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="mayoform"]/div[6]/header/div/h1')))
        
        disease_name = disease_link.text

        disease_symptoms_intro = driver.find_element(By.XPATH,'//*[@id="main-content"]/div[1]/div[1]/div[2]/p[5]').text
        print(disease_symptoms_intro)

        # first_list = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#main-content > div:nth-child(1) > div.content > div:nth-child(2) > ul:nth-child(12)')))
        first_list = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-content"]/div[1]/div[1]/div[2]/ul[1]')))
        # disease_symptoms_list = first_list.find_element(By.XPATH,'//*[contains(text(), "symptoms")]')
        disease_symptoms_list = driver.find_element(By.XPATH,'//*[contains(text(), "symptoms")]')

        # symptoms = disease_symptoms_list.find_elements(By.XPATH, '//*[contains(text(), "symptoms")]/following-sibling::ul[1]/li')
        symptoms = disease_symptoms_list.find_elements(By.XPATH, "//*[@id='main-content']/div[1]/div[1]/div[2]/ul[1]/li")
        # symptoms = symptoms[:symptoms.index(symptoms[-1])+1]
        
        disease_symptoms = [symptom.text for symptom in symptoms]

        """Finding the Diagnosis and Treatment"""
        #Switch to the new window for diagnosis and treatment.
        # driver.switch_to.window(disease_window)
        driver.switch_to.window(driver.window_handles[1])
        diagnosis_link = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="et_genericNavigation_diagnosis-treatment"]')))
        # diagnosis_link = wait.until(EC.presence_of_element_located((By.TAG_NAME, "a")))
        actions.click(diagnosis_link).perform()
        print("done")

        wait.until(EC.number_of_windows_to_be(2))
        print("done2.0")
        driver.switch_to.window(driver.window_handles[1])
        print("New window opened")

        diagnosis_all_text = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-content"]/div[1]/div[1]/div[2]')))
        diagnosis_elements = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[1]/div[1]/div[2]')
        diagnosis_elements = diagnosis_elements.find_elements(By.XPATH, '//*[@id="main-content"]/div[1]/div[1]/div[2]/*')
        diagnosis_sub_els = diagnosis_elements[:5]
        diagnosis_el = [diagnosis_content.text.replace("\n", " ") for diagnosis_content in diagnosis_sub_els]
        print("finished 2.0")

        treatment_sub_els = diagnosis_elements[7:9]
        treatment_el = [treatment_content.text.replace("\n", " ") for treatment_content in treatment_sub_els]
        # print(treatment_el)

        final_results = []
        result = {
            "disease_name" : disease_name,
            "disease_symptoms" : disease_symptoms,
            "diagnosis_text" : diagnosis_el,
            "treatment_text": treatment_el
        }
        final_results.append(result)
        print(final_results)
        print("finished")
        driver.back()

        if final_results:
            with open("Disease_results.txt", 'w') as f:
                for result in final_results:
                    f.write(f"{result['disease_name']}\n")
                    f.write(f"Symptoms: {', '.join(result['disease_symptoms'])}\n")
                    f.write(f"Diagnosis: {', '.join(result['diagnosis_text'])}")
                    f.write(f"Treatment: {', '.join(result['treatment_text'])}")
                    f.write('\n')
            
            with open("Disease_results.txt", "r") as f:
                contents = f.read()
                print(contents)

        driver.quit()


    except NoSuchElementException :
        print("No such Element Found")
        driver.quit()

except TimeoutException :
    print("Search Results not Found")
    driver.quit()

