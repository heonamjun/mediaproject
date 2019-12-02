

import requests
from selenium import webdriver
import pymysql
import re
from bs4 import BeautifulSoup
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath('/home/ubuntu'))

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext



while True:
    
    req = requests.get('https://www.apt2you.com/houseSaleSimpleInfo.do')

    req.encoding = 'euc-kr'

    html = req.text
    soup = BeautifulSoup(html,'html.parser')
    posts = soup.select('#content > div.inf_wrap > div.table_type1 > table > tbody > tr:nth-of-type(1) > td:nth-of-type(4) > a')

    latest = posts[0].text
    latest = re.sub("[\u3000\t\n\r]", "", latest)

    with open(os.path.join(BASE_DIR, 'latest.txt'), 'r+') as f_read:
        before = f_read.readline()
        if before != latest:  #db인서트 로직
            driver = webdriver.Chrome()
            driver.implicitly_wait(3)
            
            driver.get('https://www.apt2you.com/houseSaleSimpleInfo.do')
            
            driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[4]/table/tbody/tr[1]/td[4]/a').click()
            
            #dirver.find_element_by_xpath('//*[@id="laySale"]/div[2]/ul[1]/li[1]')
            
            html=driver.page_source
            
            soup = BeautifulSoup(html,'html.parser')
            
            notices = soup.select('#laySale > div.layer_content.h530 > ul > li')
                                  
            width = soup.select('#laySale > div.layer_content.h530 > div.table_type1')
                                
            width = soup.find_all("table")[3].find_all("tbody")[0].find_all("td")
            
            size=cleanhtml(width[0].get_text())[1:5]#사이즈 구하기
            
            money = cleanhtml(width[1].get_text())
            
            size = float(size)
            
            money =int(re.sub("[,]","",money))
            
            '''
            for ele in width:
                before=ele.get_text()
                
            before = re.sub("[\u3000\t\n\r]", " ", before)
            '''
                
            
            my=cleanhtml(str(notices[0]))
            my=re.sub("[\u3000\t\n\r]", " ", my)
            
            my= my[15:18]
            
            #db 접속 및 업데이터
            
            
            
            conn = pymysql.connect(host = 'localhost', user = 'root', password = 'root' ,db = 'my_db',port=3306)
            # host = DB주소(localhost 또는 ip주소), user = DB id, password = DB password, db = DB명
            
            curs = conn.cursor()
            
            sql = 'INSERT INTO apt (district, brand, minutes, price, space, score, aptname, apt_district, apt_url, apt_progress) VALUES ($s, %s, %s, %s, %s, %s, %s, %s, %s, %s);' # 실행 할 쿼리문 입력
            
            data= (None,None,None,money,size,my,None,None)
            
            curs.execute(sql,data)
            
        else:
            print("nothing")
            f_read.close()
    
    with open(os.path.join(BASE_DIR, 'latest.txt'), 'w+') as f_write:
        f_write.write(latest)
        f_write.close()
        
    time.sleep(60)
