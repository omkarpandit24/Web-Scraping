from selenium import webdriver
from time import sleep

driver = webdriver.Chrome('C:/Omkar/TA/Web Scraping/Selenium/chromedriver')

driver.get('https://www.google.com')

#search tag using id
search_bar = driver.find_element_by_id('lst-ib')

#input data
search_bar.send_keys('Web scraping is an excellent skill to have.')

#submit the form

search_bar.submit()

sleep(10)

driver.close()




