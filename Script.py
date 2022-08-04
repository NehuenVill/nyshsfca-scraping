from base64 import encode
from selenium import webdriver
import json
from time import sleep


# First get all the dynamicly load profiles href with selenium:

driver = webdriver.Chrome()

driver.get('http://www.nyshsfca.org/directory')

def get_profiles_href():

    href_list = []


    for i in range(19):

        table = driver.find_element_by_tag_name('tbody')

        hrefs = table.find_elements_by_tag_name('a')

        sleep(3)

        for href in hrefs:

            href_text = href.get_attribute('href')

            print(href_text)

            href_list.append(href_text)

            sleep(0.1)

        selector = driver.find_element_by_tag_name('select')

        selector.click()

        sleep(5)

        options = selector.find_elements_by_tag_name('option')

        options[i+1].click()

        sleep(2)
    
    driver.close()

    return href_list


get_profiles_href()

# Next use bs4 to get the information from those hrefs: