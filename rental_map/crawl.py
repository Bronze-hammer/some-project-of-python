
# /pinpaigongyu/pn/2/?minprice=600_1000
# /pinpaigongyu/pn/{page}/?minprice={min_rent}_{max_rent}

#-*- coding:utf-8 _*_

from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import time
import csv

url = "http://gz.58.com/pinpaigongyu/pn/{page}/?minprice=600_1000"

# 已完成的页数序号，初始为0
page = 0

with open('rent.csv', encoding="utf-8", mode="w") as f:
    while True:
        page += 1
        print('fetch:', url.format(page=page))
        response = requests.get(url.format(page=page))
        response.encoding = 'utf-8'
        html = BeautifulSoup(response.text, 'html.parser')
        houses = html.find('ul', {'class': 'list'})
        # 循环在读不到的房源时结束
        if not houses:
            break
        house_list = houses.find_all('li')
        for house in house_list:
            house_title = house.find('h2').get_text()
            house_url = urljoin(url, house.find('a')['href'])
            house_info_list = house_title.split()


            # 如果第二列是公寓名则取第一列作为地址
            if "公寓" in house_info_list[1] or "青年社区" in house_info_list[1]:
                house_location = house_info_list[0]
            else:
                house_location = house_info_list[1]

            house_money = house.find('b').get_text()
            # 写一行数据
            # csv_writer.writerow([house_title, house_location, house_money, house_url])
            # with open('rent.csv', encoding="utf-8", mode="w") as f:
            f_csv = csv.writer(f)
            f_csv.writerow([house_title, house_location, house_money, house_url])
            if page % 60 == 0:
                time.sleep(3)
