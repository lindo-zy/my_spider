#!/usr/bin/python3
# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pymssql


# 数据库连接
def getcon(sql, *args):
    host = 'localhost'
    user_name = 'sa'
    user_password = '123'
    database = 'bk197'
    conn = pymssql.connect(host, user_name, user_password, database)
    cursor = conn.cursor()

    cursor.execute(sql, *args)
    conn.commit()
    conn.close()


# 获取左边全部目录
def get_left_urls(enter_url, headers):
    enter_html = requests.get(enter_url, headers)
    enter_html.encoding = enter_html.apparent_encoding
    enter_soup = BeautifulSoup(enter_html.text, 'lxml')

    # 左边全部目录
    left_urls = (enter_soup.find_all('ul')[1]).find_all('a')
    left_links = []
    for left_url in left_urls:
        left_links.append('http://www.bk179.com/' + left_url['href'])
    print(left_links)

    count = 0
    for link in left_links:
        right_html = requests.get(link, headers)
        right_html.encoding = right_html.apparent_encoding
        right_soup = BeautifulSoup(right_html.text, 'lxml')

        # 右边一级目录名称 如 互联网/IT
        right_name = (right_soup.find('h5')).get_text()
        # print(right_name)

        right_child_names = right_soup.find_all(class_='major_div_in')
        for child in right_child_names:
            # 计算机软件
            child_name = (child.find('h2')).get_text()

            print(child_name)

            child_urls = child.find_all('a')

            for child_url in child_urls:
                child_link = 'http://www.bk179.com' + child_url['href']
                child_link_name = child_url.get_text()

                # 职业分类 软件工程师 软件测试工程师
                print(child_link_name)
                try:
                    # 遍历每个子项目的内容
                    final_html = requests.get(child_link, headers=headers)
                    final_html.encoding = final_html.apparent_encoding
                    final_soup = BeautifulSoup(final_html.text, 'lxml')
                    # 岗位定义
                    gwdy = (final_soup.find_all('p', class_='mrp3')[0]).get_text()
                    print(gwdy)

                    # 岗位薪资
                    gwxz = (final_soup.find('em')).get_text()
                    print(gwxz)

                    # 工作联系
                    gzlx = (final_soup.find_all('p', class_='mrp3')[1]).get_text()
                    print(gzlx)

                    # 职业介绍
                    zyjs = (final_soup.find_all('div', 'major_div_in')[2]).get_text(strip=True)
                    print(zyjs)

                    # 职业特点
                    zytd = (final_soup.find_all('div', 'major_div_in')[3]).get_text(strip=True)
                    print(zytd)

                    # 任职条件
                    rztj = (final_soup.find_all('div', 'major_div_in')[4]).get_text(strip=True)
                    print(rztj)

                    # 发展空间
                    fzkj = (final_soup.find_all('div', 'major_div_in')[5]).get_text(strip=True)
                    print(fzkj)

                    # 匹配专业
                    ppzy = (final_soup.find_all('div', 'major_div_in')[6]).get_text('|', strip=True)
                    print(ppzy)
                    try:
                        args = (right_name, child_name, child_link_name, gwdy, gwxz, gzlx, zyjs, zytd, rztj, fzkj, ppzy)

                        sql = "insert into test values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        getcon(sql, args)
                    except Exception as e:
                        print(e)
                except Exception as e:
                    print(e)


if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36'}
    enter_url = 'http://www.bk179.com/Jobplan/job.html'
    get_left_urls(enter_url, headers)
