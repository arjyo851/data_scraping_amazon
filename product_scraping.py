from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import sys

next_page=''
chrome_driver_path = Service(r"C:\Users\KIIT\Desktop\python_code\my_python_code\selenium\chromedriver.exe")
op = webdriver.ChromeOptions()
url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"


def scrape_amazon(max_pages):
    page_number=1
    driver = webdriver.Chrome(service=chrome_driver_path,options=op)
    driver.get(url)
    while page_number <= max_pages:
        scrape_page(driver)
        driver.get(next_page)
        driver.implicitly_wait(5)
        page_number += 1

# task 1
def scrape_page(driver):
    product_link = []
    product_name = []
    product_price = []
    product_ratings = []
    product_reviews = []
    product_reviews = []

    #task 2
    product_description = []
    product_asin = []
    
    Manufacturer = []

    items = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))
    for item in items:
        if(len(item.text.split('₹')[1])>0):
            product_price.append(item.text.split('₹')[1])

        print("\n")
        name = item.find_element_by_xpath('.//span[@class="a-size-medium a-color-base a-text-normal"]')
        product_name.append(name.text)

        data_asin = item.get_attribute("data-asin")
        product_asin.append(data_asin)

        

        ratings_box = item.find_elements(By.XPATH, './/div[@class="a-row a-size-small"]/span')
        if ratings_box != []:
                ratings = ratings_box[0].get_attribute('aria-label')
                reviews = ratings_box[1].get_attribute('aria-label')
        else:
                ratings, reviews = 0, 0
        product_ratings.append(ratings)
        product_reviews.append(str(reviews))
        
        

        link = item.find_element(By.XPATH, './/a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]').get_attribute("href")
        product_link.append(link)

    

    [product_link,product_description,Manufacturer]=another_page(driver,product_link,product_description,Manufacturer)

    #delete this and change to csv
    print(len(product_link))
    print("\n")
    
    print(len(product_description))
    print("\n")
    print(len(Manufacturer))
    print("\n")
    
    df = pd.DataFrame({'link': product_link,
                   'name': product_name,
                   'price': product_price,
                   'ratings': product_ratings,
                   'reviews': product_reviews,
                   'asin': product_asin,
                   'description': product_description,
                   'manufacturer': Manufacturer})
    df.to_csv('amazon_data.csv')
    global next_page
    next_page = driver.find_element(By.XPATH,'//a[@class ="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]').get_attribute("href")


def another_page(driver,product_link,product_description,Manufacturer):
    for item in product_link:
        driver.get(item)
        driver.implicitly_wait(0.5)

        try:
            description = item.find_element(By.XPATH, './/div[@class="a-unordered-list a-vertical a-spacing-mini""]"]').text
            product_description.append(description)
        except:
            product_description.append('')
        try:
            manufacturer = item.find_element(By.XPATH, './/span[@class="a-list-item"][1]').text
            Manufacturer.append(manufacturer)
        except:
            Manufacturer.append('')
        driver.back()
    return product_link,product_description,Manufacturer
    
scrape_amazon(1)