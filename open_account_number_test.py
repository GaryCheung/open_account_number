from bs4 import BeautifulSoup
import requests

url = 'http://www.chinaclear.cn/cms-webapp/wcm/getManuscriptByTitle_mzkb.action?weekflag=prevWeek'
web_data = requests.get(url)
soup = BeautifulSoup(web_data.text,'lxml')
print(soup)