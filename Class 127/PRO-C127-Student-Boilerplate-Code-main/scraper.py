from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

# NASA Exoplanet URL
START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"

# Webdriver
from selenium.webdriver.chrome.service import Service
service=Service (executable_path=r"C:\Users\gjoha\OneDrive\Documents\Out of School\Visual Studio Code\BYJUS\Python\Class 127\PRO-C127-Student-Boilerplate-Code-main\chromedriver-win64\chromedriver.exe")
options=webdriver.ChromeOptions()
browser=webdriver.Chrome(service=service, options=options)
browser.get(START_URL)

time.sleep(10)

planets_data = []

# Define Exoplanet Data Scrapping Method
def scrape():

    for i in range(1,2):
        while True:
            time.sleep(2)
            
        #print(f'Scrapping page {i+1} ...' )

            soup = BeautifulSoup(browser.page_source, "html.parser")

            #Checking the page number
            current_page_number = int(soup.find_all("input", attrs={"class", "page_num"})[0].get("value"))
            if current_page_number < i:
                browser.find_element(by=By.XPATH, value='/html/body/div[3]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()
            elif current_page_number > i:
                 browser.find_element(by=By.XPATH, value='/html/body/div[3]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/div[1]/div[2]/div[1]/div/nav/span[1]/a').click()
            else:
                break


            for x in soup.find_all("ul", attrs={"class", "exoplanet"}):
                li_tags = x.find_all("li")

                temp_list = []

                for index, li_tag in enumerate(li_tags):
                    if index == 0:
                        temp_list.append(li_tag.find_all("a")[0].contents[0])
                    else:
                        try:
                            temp_list.append(li_tag.contents[0])
                        except:
                            temp_list.append("")
                
                #Get hyperlink tag
                hyperlink_tag = li_tags[0]
                temp_list.append("https://exoplanets.nasa.gov"+hyperlink_tag.find_all("a", href = True)[0]["href"])


                planets_data.append(temp_list)

            browser.find_element(by=By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            print(f'Page{i} - Scrapping page...')


        
# Calling Method    
scrape()

# Define Header
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date", "hyperlink"]

# Define pandas DataFrame   
df = pd.DataFrame(planets_data, columns = headers)

# Convert to CSV
df.to_csv("updated_scraped.csv", index = True, index_label = "id")
    


