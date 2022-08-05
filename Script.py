from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from time import sleep
import json
import pandas as pd

# First get all the dynamicly load profiles href with selenium:



def get_profiles_href():

    driver = webdriver.Chrome()
    driver.get('http://www.nyshsfca.org/directory')

    href_list = []

    sleep(3)

    for i in range(27):

        selector = driver.find_element_by_tag_name('select')

        selector.click()

        sleep(3)

        options = selector.find_elements_by_tag_name('option')

        options[i].click()

        sleep(1)

        table = driver.find_elements_by_tag_name('tbody')[2]

        hrefs = table.find_elements_by_tag_name('a')

        sleep(0.5)

        for href in hrefs:

            href_text = href.get_attribute('href')

            print(href_text)

            href_list.append(href_text)

        sleep(0.5)

    driver.close()

    return href_list


# get_profiles_href()


# Next use bs4 to get the information from those hrefs:

def get_info(href_list : list):

    profiles = []

    for href in href_list:

        # Saving the Urls the have been scraped already so that the program doesn't have
        # to restart from zero each time it runs.

        with open('sites_scraped.json') as f:

            data = json.load(f)

        with open('sites_scraped.json', 'w') as f:

            if href not in data["Links"]:

                data["Links"].append(href)

                json.dump(data, f, indent=2)

            else:

                json.dump(data, f, indent=2)
            
                print("Already scraped")

                pass


        r = requests.get(href)
        soup = BeautifulSoup(r.text, 'html.parser')

        info = soup.find_all('div', class_ = 'fieldBody')

        output = {
            'First Name': info[2].text.replace('\n', '').replace('/n', ''),
            'Last Name': info[3].text.replace('\n', '').replace('/n', ''),
            'Membership level': info[1].text.replace('\n', '').replace('/n', ''),
            'E-mail': info[4].text.replace('\n', '').replace('/n', '') if len(info)>4 else 'Not available.',
            'Phone': info[5].text.replace('\n', '').replace('/n', '') if len(info)>5 else 'Not available.'
        }

        print(output)

        profiles.append(output)

    return profiles

def save(data):

    with open('High_school_couches.json', 'w') as f:

        json.dump(data, f, indent=2)

    df = pd.DataFrame(data, columns=['Membership level', 'First Name', 'Last Name', 'E-mail', 'Phone'])
    df.to_excel('High_school_couches.xls', index=True, columns=['Membership level', 'First Name', 'Last Name', 'E-mail', 'Phone'])


if __name__ == "__main__":

    save(get_info(get_profiles_href()))

