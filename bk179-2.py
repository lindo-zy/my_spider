# coding=utf-8
import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import pymssql


# 数据库连接
def getcon(sql, *args):
    host = 'localhost'
    user_name = 'sa'
    user_password = '123'
    database = 'work'
    conn = pymssql.connect(host, user_name, user_password, database)
    cursor = conn.cursor()

    cursor.execute(sql, *args)
    conn.commit()
    conn.close()


all_url = 'http://www.bk179.com/Volunteer/major.html'
# 模拟浏览器登陆
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36'}
# 解析爬取的网址
start_html = requests.get(all_url, headers=headers)  # 传入起始网址  headers
start_html.encoding = start_html.apparent_encoding  # 网页编码  自适应
soup = BeautifulSoup(start_html.text, 'lxml')  # 解析网页

# 本科的专业
ben__all_majors = soup.find_all('ul', id='zhuan')
for major in ben__all_majors:
    ben_majors = major.find_all('a')
    for major in ben_majors:
        ben_links = 'http://www.bk179.com/' + major['href']
        # 专业的名字
        ben_majors_names = major.get_text()
        print(ben_links, ben_majors_names)

        # 构造soup
        ben_html = requests.get(ben_links, headers=headers)  # 传入起始网址  headers
        ben_html.encoding = ben_html.apparent_encoding  # 网页编码  自适应
        ben_soup = BeautifulSoup(ben_html.text, 'lxml')

        # 获取子专业名字
        try:
            major_class = ben_soup.find_all('div', class_='major_mid_in')
            for k in major_class:
                for i in range(0, len(k.find_all('h4'))):
                    majors = k.find_all('h4')[i].get_text()
                    links = (k.find_all('p')[i]).find_all('a')
                    print(majors)
                    for link in links:
                        hrefs = 'http://www.bk179.com/' + link['href']
                        major_child = link.get_text()
                        print(major_child)

                        # majorsoup
                        major_html = requests.get(hrefs, headers=headers)  # 传入起始网址  headers
                        major_html.encoding = major_html.apparent_encoding  # 网页编码  自适应
                        major_soup = BeautifulSoup(major_html.text, 'lxml')

                        # zykc 主要课程
                        zykc = (major_soup.find_all('p', class_='mrp3')[0]).get_text()
                        print(zykc)

                        # jyfx 就业方向
                        jyfx = (major_soup.find_all('p', class_='mrp3')[1]).get_text()
                        print(jyfx)

                        # xxmk 学习门槛
                        xxmk = (major_soup.find_all('p', class_='mrp3')[2]).get_text()
                        print(xxmk)

                        # zyjs 专业介绍
                        zyjs = (major_soup.find_all('div', class_='major_div_in')[3]).get_text(strip=True)
                        print(zyjs)

                        # kyfx 考研方向
                        kyfx = (major_soup.find_all('div', class_='major_div_in')[4]).get_text(',', strip=True)
                        print(kyfx)

                        # kcsdzy 可从事的职业
                        kcsdzy = (major_soup.find_all('div', class_='major_div_in')[5]).get_text(',', strip=True)
                        print(kcsdzy)

                        # xjzy 相近专业
                        xjzy = (major_soup.find_all('div', class_='major_div_in')[6]).get_text(',', strip=True)
                        print(xjzy)

                        try:
                            args = (
                            '专科', ben_majors_names, majors, major_child, zykc, xxmk, jyfx, kyfx, zyjs, kcsdzy, xjzy,)

                            sql = "insert into bk179majors values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                            getcon(sql, args)
                        except Exception as e:
                            print(e)
        except Exception as e:
            print(e)
