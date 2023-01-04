#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/4 8:44
# @Author  : 马赫
# @Email   : 1692303843@qq.com
# @FileName: dash_test.py
from screwai.core.config import *
from screwai.core.database import *
print('ssss')
print(config)


db = db_connect()
cur = db.cursor()

# 获取全部列名
sql_code = "select * from Production_Daily_Data_pcponly LIMIT 1"
cur.execute(sql_code)
# 列名列表
column_list = [i[0] for i in cur.description]


focus_well = 'NB1'
# Date = ['2019-01-01', '2020-12-31']


sql_code = "select * from Production_Daily_Data_pcponly where `Wellbore` = '%s'" % focus_well

# sql_code = """SELECT
#  *
# FROM
#  production_daily_data_pcponly
# WHERE
#  Date BETWEEN '2019-01-01' AND '2020-12-31'
# and Wellbore = 'NB1'"""

db = db_connect()
cur = db.cursor()
cur.execute(sql_code)

df = pd.DataFrame(cur.fetchall())
# 修改列名
df.columns = column_list
# 将日期列转化为时间格式
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
print(df)
print(df.shape)

# df.to_csv('NB1.csv', encoding='utf_8_sig')
