from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from time import sleep


# First get all the dynamicly load profiles href with selenium:



def get_profiles_href():

    driver = webdriver.Chrome()
    driver.get('http://www.nyshsfca.org/directory')

    href_list = []

    for i in range(27):

        table = driver.find_elements_by_tag_name('tbody')[2]

        hrefs = table.find_elements_by_tag_name('a')

        sleep(1)

        for href in hrefs:

            href_text = href.get_attribute('href')

            print(href_text)

            href_list.append(href_text)

        selector = driver.find_element_by_tag_name('select')

        selector.click()

        sleep(3)

        options = selector.find_elements_by_tag_name('option')

        options[i+1].click()

        sleep(1)
    
    driver.close()

    return href_list


# get_profiles_href()


# Next use bs4 to get the information from those hrefs:

def get_info(href_list : list):

    for href in href_list:

        r = requests.get(href)
        soup = BeautifulSoup(r.text, 'html.parser')

        info = soup.find_all('div', class_ = 'fieldBody')

        output = {
            'Membership level': info[1].text.replace('\n', '').replace('/n', ''),
            'First Name': info[2].text.replace('\n', '').replace('/n', ''),
            'Last Name': info[3].text.replace('\n', '').replace('/n', ''),
            'E-mail': info[4].text.replace('\n', '').replace('/n', ''),
            'Phone': info[5].text.replace('\n', '').replace('/n', '')
        }

        print(output)

        sleep(0.1)

get_info(['http://www.nyshsfca.org/Sys/PublicProfile/63081055/3774357'])
