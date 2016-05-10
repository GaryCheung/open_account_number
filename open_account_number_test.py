from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

'''
driver = webdriver.Chrome()
driver.get('http://www.python.org')
#assert "python" in driver.title
element = driver.find_element_by_name("q")
element.send_keys("pycon")
element.send_keys(Keys.RETURN)
print(driver.page_source)
'''

def get_more_data(weeks):
    driver = webdriver.Chrome()
    driver.get('http://www.chinaclear.cn/cms-webapp/wcm/toErveyWeek_mzkb.action')
    web_data = []
    for i in range(1,weeks+1):
        element = driver.find_element_by_class_name("prev")
        element.click()
        web_data.append(driver.page_source)
        #print('-----------------------------',i,'---------------------------------','\n',web_data)
    return web_data





