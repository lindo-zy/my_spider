import requests
from bs4 import BeautifulSoup
import re
import pymssql
import json


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


# 入口网址
enter_url = 'http://www.diyigaokao.com/register'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
enter_html = requests.get(enter_url, headers=headers)
enter_html.encoding = enter_html.apparent_encoding
enter_soup = BeautifulSoup(enter_html.text, 'lxml')

# 获取所有省份
ls = []
all_provice = enter_soup.find_all('optgroup')
for provie in all_provice:
    ls.append(provie.get_text('\n').split('\n'))

ps = []
for i in ls:

    for j in i:
        # print(j)
        ps.append(j)
        # 构造uid传入 获取json
        pr_url = 'http://www.diyigaokao.com/comdata/getCitiesByPid/' + str(j) + '?provinceName=' + str(j) + ''
        # print(pr_url)
        pr_html = requests.get(pr_url, headers=headers)
        pr_html.encoding = pr_html.apparent_encoding
        pr_soup = BeautifulSoup(pr_html.text, 'lxml')
        adds = (str(pr_soup.body.string).replace('[', '').replace(']', '').replace('{', '')).split('}')

        for i in adds:
            temp = '{' + i.lstrip(',') + '}'
            result = json.loads(temp)
            try:
                # 对应的市区
                cityName = result['cityName']
                cityID = result['id']
                # print(cityName, cityID)
            except Exception as e:
                print('')

            # 对应的区县
            dis_url = 'http://www.diyigaokao.com/comdata/getDistrictsByCid/' + str(cityID) + '?cityId=' + str(
                cityID) + ''
            dis_html = requests.get(dis_url, headers=headers)
            dis_html.encoding = dis_html.apparent_encoding
            dis_soup = BeautifulSoup(dis_html.text, 'lxml')

            areas = (str(dis_soup.body.string).replace('[', '').replace(']', '').replace('{', '')).split('}')

            for k in areas:
                k_temp = '{' + k.lstrip(',') + '}'
                k_result = json.loads(k_temp)
                try:
                    # 对应的市区
                    disName = k_result['districtName']
                    # 唯一的
                    disID = k_result['id']
                    # print(disName, disID)
                except Exception as e:
                    print('')

                school_url = 'http://www.diyigaokao.com/comdata/getHighSchoolByDid/' + str(
                    disID) + '?districtId=' + str(disID) + ''
                school_html = requests.get(school_url, headers=headers)
                school_html.encoding = school_html.apparent_encoding
                school_soup = BeautifulSoup(school_html.text, 'lxml')

                schools = (str(school_soup.body.string).replace('[', '').replace(']', '').replace('{', '')).split('}')

                for s in schools:
                    s_temp = '{' + s.lstrip(',') + '}'
                    s_result = json.loads(s_temp)

                    if len(s_result) == 0:
                        schoolName = '其他'
                        schoolID = '0'
                    else:
                        schoolName = s_result['schoolName']
                        schoolID = s_result['id']
                    # print(s_result, len(s_result))
                    print(j, cityName, cityID, disName, disID, schoolName, schoolID)

                    try:
                        # 省份，城市，城市ID，区县，区县ID，学校，学校ID

                        args = (j, cityName, cityID, disName, disID, schoolName, schoolID)

                        sql = 'insert into schools VALUES (%s,%s,%s,%s,%s,%s,%s)'
                        getcon(sql, args)
                    except  Exception as e:
                        print(e)
