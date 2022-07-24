from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC


chrome_driver_path = Service(r"C:\Users\KIIT\Desktop\python_code\my_python_code\selenium\chromedriver.exe")
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=chrome_driver_path,options=op)
url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
driver.get(url)



items = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))
# task 1
product_link = []
product_name = []
product_price = []
product_ratings = []
product_reviews = []
product_reviews = []

#task 2
product_description = []
product_asin = []
product_product_description = []
Manufacturer = []

for item in items:
   name = item.find_element_by_xpath('.//span[@class="a-size-medium a-color-base a-text-normal"]')
   product_name.append(name.text)

   data_asin = item.get_attribute("data-asin")
   product_asin.append(data_asin)

#    product_link=driver.find_elements(By.CSS_SELECTOR, ".s-line-clamp-2 a")
#    for i in product_link:
#         product_link.append(i.get_attribute("href"))
#    whole_price = item.find_elements(By.XPATH, './/span[@class="a-price-whole"]')
#    fraction_price = item.find_elements(By.XPATH,'.//span[@class="a-price-fraction"]')
#    if whole_price != [] and fraction_price != []:
#         price = '.'.join([whole_price[0].text, fraction_price[0].text])
#    else:
#         price = 0
#    product_price.append(price)

   ratings_box = item.find_elements(By.XPATH, './/div[@class="a-row a-size-small"]/span')
   if ratings_box != []:
        ratings = ratings_box[0].get_attribute('aria-label')
        reviews = ratings_box[1].get_attribute('aria-label')
   else:
        ratings, reviews = 0, 0
   product_ratings.append(ratings)
   product_reviews.append(str(reviews))


products_url=driver.find_elements(By.CSS_SELECTOR, ".s-line-clamp-2 a")
for i in products_url:
    product_link.append(i.get_attribute("href"))

products_price=driver.find_elements(By.CSS_SELECTOR, ".a-price")
for i in products_price:
    if(i.get_attribute("data-a-color") == "price"):
        product_price.append(i.text)
#delete this and change to csv
print(product_link)
print(product_name)
print(product_price)
print(product_ratings)
print(product_reviews)
# task2
print(product_asin)

global next_page
next_page = driver.find_element_by_xpath('//li[@class ="a-selected"]/following-sibling::a').get_attribute("href")
