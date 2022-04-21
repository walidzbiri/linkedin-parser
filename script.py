from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import getpass


# chromeDriverPath = input('Chrome driver path (absolute): ')
driver = webdriver.Chrome('chromedriver.exe')

def login():
    driver.get("https://www.linkedin.com/login")
    time.sleep(3)
    usernametext = input('Enter your LinkedIn username: ')
    passwordText = getpass.getpass('Enter your LinkedIn password: ')

    username = driver.find_element_by_id('username')
    username.send_keys(usernametext)
    password = driver.find_element_by_id('password')
    password.send_keys(passwordText)

    log_in_button = driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button')
    log_in_button.click()

login()

## Get All Links on page
names = []
descriptions = []
companies = []
locations = []
profile_link = []

pageToScrapp = input('Le lien de la page à scrapper: ')
nbPagesToScrapp = int(input('Combien de pages voulez vous scrappez: '))


# first=pageToScrapp.split("&page=")[0]
# last=pageToScrapp.split("&page=")[1].split("&")[1]

for i in range(1,nbPagesToScrapp+1):
    driver.get(f'{pageToScrapp}&page={i}')
    time.sleep(1)

    listOfProfiles=driver.find_elements_by_css_selector(".reusable-search__entity-result-list.list-style-none>*")
    for profile in listOfProfiles:
        try:
            resumes=profile.find_element_by_css_selector(".entity-result__summary")
            if "chez" in resumes.text:
                companies.append(resumes.text.split('chez')[1])
            else:
                companies.append("non disponible")
            descriptions.append(profile.find_element_by_css_selector(".entity-result__primary-subtitle").text)
            locations.append(profile.find_element_by_css_selector(".entity-result__secondary-subtitle").text)
            names.append(profile.find_element_by_css_selector(".app-aware-link>span>span:first-of-type").text)
            profile_link.append(profile.find_element_by_css_selector('.app-aware-link').get_attribute("href"))
        except NoSuchElementException:
            print("SANS resume")
    print ("Next Page")
print ("All done !")

#for excel
import pandas as pd
df = pd.DataFrame(zip(names,descriptions,locations,companies, profile_link), columns=['Name','Description','Location','Company', 'Profile url'])
nomDuFichier = input('Le nom du fichier excel (sans extension): ')
df.to_excel(f'{nomDuFichier}.xlsx', index = False)