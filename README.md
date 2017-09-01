
## some-project-of-python

文件夹 web_server 中的程序执行将实现一个简单的web服务

文件夹 douban_movies_top250 中的程序执行获取豆瓣网中top250的电影信息




### 备份

```python


# /pinpaigongyu/pn/2/?minprice=600_1000
# /pinpaigongyu/pn/{page}/?minprice={min_rent}_{max_rent}

#-*- coding:utf-8 _*_

from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import csv

url = "http://gz.58.com/pinpaigongyu/pn/{page}/?minprice=600_1000"

# 已完成的页数序号，初始为0
page = 0

# 打开rent.csv文件
# csv_file = open("rent.csv", mode="r")
# 创建writer对象，指定文件与分隔符隔开
# csv_writer = csv.writer(csv_file, delimiter=',')

while True:
    page += 1
    print("fetch:", url.format(page=page))
    response = requests.get(url.format(page=page))
    html = BeautifulSoup(response.text, 'html.parser')
    house_list = html.select(".list > li")

    # 循环在读不到的房源时结束
    if not house_list:
        break

    for house in house_list:
        house_title = house.select("h2")[0].string.encode("utf-8")
        house_url = urljoin(url, house.select("a")[0]["href"])
        house_info_list = house_title.split()


        # 如果第二列是公寓名则取第一列作为地址
        house_info = str(house_info_list[1])
        if "公寓" in house_info_list or "青年社区" in house_info_list:
            house_location = house_info_list[0]
        else:
            house_location = house_info_list[1]

        house_money = house.select(".money")[0].select("b")[0].string.encode("utf-8")
        # 写一行数据
        # csv_writer.writerow([house_title, house_location, house_money, house_url])
        with open('rent.csv', encoding="utf-8", mode="w") as f:
            f_csv = csv.writer(f)
            f_csv.writerow([house_title, house_location, house_money, house_url])

# 关闭文件
# csv_file.close()

```
