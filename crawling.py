# selenium 3
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

from sklearn.feature_extraction.text import TfidfVectorizer


#Spinning up the driver
driver = webdriver.Chrome(ChromeDriverManager().install())

wait = WebDriverWait(driver=driver, timeout=15)
driver.get("https://www.mayoclinic.org/diseases-conditions")

#Identify the name of the website we are currently crawling
title = driver.title
print(title)

#Waiting for the search Bar to become visible
search_box = None
try:
    search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='search-input-globalsearch-901d11d458']")))

    #Check if it is enabled and displayed
    if search_box.is_enabled() and search_box.is_displayed():

        actions = ActionChains(driver=driver)
        actions.move_to_element(search_box).perform()    

        #Sending the search query
        search_box.clear()
        try:
            search_box.send_keys("Pneumonia")
            search_box.send_keys(Keys.RETURN)

            # Wait for the search resuls to load
            # Going for the first link
            try:
                first_link=wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='cmp-skip-to-main__content']/ul/li/h3/div/a")))
                link_title = first_link.text
                # print(link_title)

                actions.key_down(Keys.CONTROL).click(first_link).key_up(Keys.CONTROL).perform()
                wait.until(EC.number_of_windows_to_be(2))
                driver.switch_to.window(driver.window_handles[1])

                try:
                    """ Get the disease name and symptoms"""
                    disease_link = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="mayoform"]/div[6]/header/div/h1')))
                    disease_name = disease_link.text
                    # print(disease_name)

                    disease_symptoms_intro = driver.find_element(By.XPATH,'//*[@id="main-content"]/div[1]/div[1]/div[2]/p[5]').text
                    # print(disease_symptoms_intro)

                    first_list = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-content"]/div[1]/div[1]/div[2]/ul[1]')))
                    disease_symptoms_list = driver.find_element(By.XPATH,'//*[contains(text(), "symptoms")]')
                    symptoms = disease_symptoms_list.find_elements(By.XPATH, "//*[@id='main-content']/div[1]/div[1]/div[2]/ul[1]/li")
                    disease_symptoms = [symptom.text for symptom in symptoms]
                    disease_symptoms_text = [disease_symptoms_intro, disease_symptoms]

                    """Finding the Diagnosis and Treatment"""
                    #Switch to the new window for diagnosis and treatment.
                    driver.switch_to.window(driver.window_handles[1])
                    diagnosis_link = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="et_genericNavigation_diagnosis-treatment"]')))
                    actions.click(diagnosis_link).perform()
                    print("diagnosis link clicked")

                    wait.until(EC.number_of_windows_to_be(2))
                    driver.switch_to.window(driver.window_handles[1])
                    print("New window opened")

                    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-content"]/div[1]/div[1]/div[2]')))
                    diagnosis_elements = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[1]/div[1]/div[2]')
                    diagnosis_elements = diagnosis_elements.find_elements(By.XPATH, '//*[@id="main-content"]/div[1]/div[1]/div[2]/*')
                    diagnosis_sub_els = diagnosis_elements[:5]
                    diagnosis_el = [diagnosis_content.text.replace("\n", " ") for diagnosis_content in diagnosis_sub_els]
                    
                    treatment_sub_els = diagnosis_elements[7:9]
                    treatment_el = [treatment_content.text.replace("\n", " ") for treatment_content in treatment_sub_els]
                    # print(treatment_el)

                    """Mounting Disease Results"""
                    final_results = []
                    result = {
                        "disease_name" : disease_name,
                        "disease_symptoms" : disease_symptoms_text[1],
                        "diagnosis_text" : diagnosis_el,
                        "treatment_text": treatment_el
                    }
                    final_results.append(result)
                    # print(final_results)
                    print("finished getting results")
                    driver.back()

                    if final_results:
                        with open("Disease_results.txt", 'w') as f:
                            for a_result in final_results:
                                f.write(f"{a_result['disease_name']}\n")
                                f.write(f"Symptoms: {', '.join(a_result['disease_symptoms'])}\n")
                                f.write(f"Diagnosis: {', '.join(a_result['diagnosis_text'])}\n")
                                f.write(f"Treatment: {', '.join(a_result['treatment_text'])}")
                                f.write('\n')
                        
                        """Using TF-IDF technique to process the texts."""
                        with open("Disease_results.txt", "r") as f:
                            contents = f.read()
                            print(contents)

                        vectorizer = TfidfVectorizer()
                        transform_vectors = vectorizer.fit_transform([contents])

                        print("Document Transform: ", transform_vectors.toarray())
                        print("Feature Names: ", vectorizer.get_feature_names_out())


                    else :
                        print("No results")
                        driver.quit()

                    driver.quit()


                except NoSuchElementException :
                    print("No such Element Found")
                    driver.quit()

            except TimeoutException :
                print("Search Results not Found")
                driver.quit()

        except ElementNotInteractableException:
            print("Could not interact with the search box")
            driver.quit()

    else:
        print("Search Box is not displayed")
        driver.quit()

except TimeoutException:
    print("Search Box Not Found")
    driver.quit()
