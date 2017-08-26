
# -*- coding:utf-8-*-

# re是python的正则表达式模块
# csv模块是python的内置模块，直接import csv就可调用。csv模块主要就两个函数
# 1.csv.reader()  读取csv文件数据
# 2.csv.writer()  写入csv文件数据

import requests
from bs4 import BeautifulSoup
import re
import csv

header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# https://movie.douban.com/top250?start=0
# https://movie.douban.com/top250?start=25
# ...
# https://movie.douban.com/top250?start=225
# 每个页面显示25部电影

url_list = ['https://movie.douban.com/top250?start=%d' % index for index in range(0, 250, 25)]

# url = 'https://movie.douban.com/top250?start=0'


# BeautifulSoup解析器
#
# from bs4 import BeautifulSoup
#
# #根据HTML网页字符串创建BeautifulSoup对象
# soup = BeautifulSoup(
#                     html_doc,    #HTML文档字符串
#                     'html_parser',    #HTML解析器
#                     from_encoding='utf-8'    #HTML文档的编码
#                     )
#

def movie_list(url):
    response = requests.get(url, header)
    response.encoding = 'utf-8'
    html = BeautifulSoup(response.text, 'html.parser')
    data = html.find('ol', {'class': 'grid_view'})
    movies_list = data.find_all('li')
    movies = []
    for m in movies_list:

        # 通过find_all()得到的所有符合条件的结果和select()一样都是列表list
        # find()只返回第一个符合条件的结果，所以find()后面可以直接接.text或者get_text()来获得标签中的文本。

        rank = m.find('em').get_text()  # 获得电影排名
        m_name = m.find('img')['alt']  # 获取电影名字
        info = m.find('p').get_text() #获得电影的基本信息（导演、主演、拍摄国家、电影类型）

        # 正则表达式
        # \s 匹配空字符
        # . 匹配任意字符
        # * 匹配前面的子表达式零次或多次
        # ? 匹配前面的子表达式零次或一次，或指明一个非贪婪限定符

        # re.macth和re.search匹配得到的是match对象，re.findall得到的是一个列表。

        director = re.findall('导演:\s(.*?)\s', info)[0]  # 导演
        starring = re.findall('主演:\s(.*?)\s', info) # 主演
        if len(starring) == 0:
            starring = '佚名'
        else:
            starring = starring[0]
        # python中字符串前面加上r， 表示原生字符串
        year = re.search(r'\d{4}', info).group()  # 获取年份
        area_list = re.findall('\s/\s(.*?)\s/\s', info)
        # area = re.search(r'\/\n{*}\n\/', info)
        if len(area_list) > 1:
            area = area_list[1]
        else:
            area = area_list[0]
        grade = m.select('span.rating_num')[0].get_text() # 评分
        quote_l = m.select('span.inq') # 简介
        if len(quote_l) == 0:
            quote = ''
        else:
            quote = quote_l[0].get_text()

        tup = (rank, m_name, director, starring, year, area, grade, quote)
        movies.append(tup)
    return movies

# 将内容保存到csv文件中
def save_data():
    headers = ['排名', '名字', '导演', '主演', '年份', '地区', '评分', '简介']
    # with open('/Users/mocokoo/Documents/py_file/douban_movie_top250.csv', encoding='UTF-8', mode='w') as f:
    with open('douban_movie_top250.csv', encoding='UTF-8', mode='w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        for url in url_list:
            data_list = movie_list(url)
            for data in data_list:
                f_csv.writerow(data)


if __name__ == '__main__':
    save_data()
