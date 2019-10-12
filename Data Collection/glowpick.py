from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.Keys import Keys

driver = webdriver.Chrome('./chromedriver')
driver.get(
    'https://www.glowpick.com/search/result?query=%EB%A6%BD%EC%8A%A4%ED%8B%B1')
sleep(5)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
driver.execute_script("window.scrollTo(0, 200)")
driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
element = driver.find_element_by_tag_name('html')

element.send_keys(Keys.SPACE)
element = driver.find_element_by_tag_name('html')
element.click()
element.send_keys(Keys.SPACE)

elem = driver.find_element_by_class("button-link")
element.send_keys(Keys.ENTER)
SCROLL_PAUSE_TIME = 0.5

# # Get scroll height
# last_height = driver.execute_script("return document.body.scrollHeight")
# i = 0
# while True:
#     # Scroll down to bottom
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#     # Wait to load page
#     sleep(SCROLL_PAUSE_TIME)

#     # Calculate new scroll height and compare with last scroll height
#     new_height = driver.execute_script("return document.body.scrollHeight")
#     if new_height == last_height:
#         break
#     last_height = new_height
#     print(i)
#     i += 1


notices = soup.select('div.side-info')
# notices = soup.select('div.list-item meta')
print(len(notices))
# for n in notices:
#     a = n.get('content')
#     print(a)
