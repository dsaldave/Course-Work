from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import csv
import time




def initBrowser():
    chrome_options = Options()
    #chrome_options.add_argument("--headless") # change browser visibility
    chrome_options.add_argument("--window-size=1920x1080")
    #chrome_options.add_argument("user-agent=")
    chrome_options.add_argument("--start-maximized")

    path_to_chromedriver = './chromedriver' # change path as needed
    browser = webdriver.Chrome(executable_path = path_to_chromedriver, chrome_options = chrome_options)

    return browser  



browser = initBrowser()



def getPlantInfo(plant_url):
    browser.get(plant_url[1])
    plant_type = plant_url[0]
    try:
        common_name = browser.find_element_by_xpath("//p[@id='NetPS-PlantCommonName']").text
    except NoSuchElementException:
        common_name = "Not Given"
        pass
    try:
        botanic_name = browser.find_element_by_xpath("//p[@id='NetPS-PlantBotanicName']").text
    except NoSuchElementException:
        botanic_name = "Not Given"
        pass
    try:
        height = browser.find_element_by_xpath("//p[@id='NetPS-PlantHeight']").text.split("Height: ")[1].strip()
    except NoSuchElementException:
        height = "Not Given"
        pass
    try:
        spread = browser.find_element_by_xpath("//p[@id='NetPS-PlantSpread']").text.split("Spread: ")[1].strip()
    except NoSuchElementException:
        spread = "Not Given"
        pass
    try:
        sunlight = browser.find_element_by_class_name("NetPS-PlantLightIcon").get_attribute("title")
    except NoSuchElementException:
        sunlight = "Not Given"
        pass
    try:
        hardiness_zone = browser.find_element_by_xpath("//p[@id='NetPS-PlantHardiness']").text.split("Hardiness Zone: ")[1].strip()
    except NoSuchElementException:
        hardiness_zone = "Not Given"
        pass
    try:
        other_names = browser.find_element_by_xpath("//p[@id='NetPS-PlantOtherSpecies']").text.split("Other Names: ")[1].strip()
    except NoSuchElementException:
        other_names = "Not Given"
        pass
    try:
        full_info = browser.find_element_by_xpath("//div[@id='NetPS-PlantBox']").text
    except NoSuchElementException:
        full_info = "Not Given"
        pass

    return [plant_type, common_name, botanic_name, height, spread, sunlight, hardiness_zone, other_names, full_info]



# get all plants info
def main():
    with open("plants_data2.csv", "w") as output:
        writer = csv.writer(output)
        writer.writerow(['Plant Type', 'Common Name', 'Botanic Name', 'Height', 'Spread', 'Sunlight', 'Hardiness Zone', 'Other Names', 'Full Info'])
    browser.get("http://www.qscaping.com/20000011/Results/List")
    categories_url_list = [[category.text, category.get_attribute("href")] for category in browser.find_elements_by_xpath("//a[contains(@href, '/Results/List/pere')]")]
    for category_url in categories_url_list:
        browser.get(category_url[1])
        plants_url_list = [plant_url.get_attribute("href") for plant_url in browser.find_elements_by_xpath("//a[contains(@href, '/Plant/')]")]
        for plant_url in plants_url_list:
            print("Getting data for URL: {}".format(plant_url))
            plant_info = getPlantInfo(([category_url[0], plant_url]))
            with open("plants_data2.csv", "a") as output:
                writer = csv.writer(output)
                writer.writerow(plant_info)
            



main()


