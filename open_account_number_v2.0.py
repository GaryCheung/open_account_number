from bs4 import BeautifulSoup
import requests
from datetime import date,datetime
import pymysql
import time
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def get_more_data(weeks):
    driver = webdriver.Chrome()
    driver.get('http://www.chinaclear.cn/cms-webapp/wcm/toErveyWeek_mzkb.action')
    web_data = []
    web_data.append(driver.page_source)
    for i in range(1,weeks+1):
        element = driver.find_element_by_class_name("prev")
        element.click()
        web_data.append(driver.page_source)
        #print('-----------------------------',i,'---------------------------------','\n',web_data)
    return web_data


def delete_today_data(config):
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            # 执行sql语句，插入记录
            sql = "DELETE FROM new_investor"
            cursor.execute(sql)
            # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
        connection.commit()
    finally:
        connection.close()
    print('Executed on-----------',present_date,'\n','-----------------------delete success!----------------','\n')

def get_new_investor(web_data):
    lenghth = len(web_data)
    for i in range(1,lenghth+1):
        soup = BeautifulSoup(web_data[i-1],'lxml')
        new_investor = soup.select('#settlementList > table > tbody > tr > td > table > tbody > tr:nth-of-type(2) > td:nth-of-type(2) > p > span')
        new_personal_investor = soup.select('#settlementList > table > tbody > tr > td > table > tbody > tr:nth-of-type(3) > td:nth-of-type(2) > p > span')
        period = soup.select('body > div.SettlementTitle > h2')
        for investors,new_personals,periods in zip(new_investor, new_personal_investor, period):
            investor = investors.get_text()
            new_personal = new_personals.get_text()
            periods = re.findall(r'(\w*[0-9]+\.*[0-9]+)\w*',periods.get_text())
            periods = periods[0] + '.' + periods[1] + '--' + periods[2] + '.' + periods[3]
            print(periods)
            connection = pymysql.connect(**config)
            try:
                with connection.cursor() as cursor:
                # 执行sql语句，插入记录
                 sql = 'INSERT INTO new_investor (import_date, new_investor, new_personal, period) VALUES (%s, %s, %s, %s)'
                 cursor.execute(sql, (present_date, investor, new_personal, periods))
                # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
                connection.commit()
            finally:
                connection.close()
            time.sleep(1)

config = {
    'host':'127.0.0.1',
    'port':3306,
    'user':'root',
    'password':'19860112',
    'db':'new_investor',
    'charset':'utf8'
}

present_date = datetime.now().date()

weeks = 20
delete_today_data(config)
web_data = get_more_data(weeks)
get_new_investor(web_data)
