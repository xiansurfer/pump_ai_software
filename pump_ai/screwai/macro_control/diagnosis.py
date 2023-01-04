#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/3 15:11
# @Author  : 马赫
# @Email   : 1692303843@qq.com
# @FileName: diagnosis.py

from screwai.core.database import *
from screwai.core.draw_effici import *

import os
import pandas as pd
import scipy.optimize as opt
import pymysql



import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from screwai.core.base import *

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


db = db_connect()
# 使用 cursor() 方法创建一个游标对象 cursor
cur = db.cursor()

# 获取全部列名
sql_code = "select * from Production_Daily_Data_pcponly LIMIT 1"
cur.execute(sql_code)

# 列名列表
column_list = [i[0] for i in cur.description]
for i in column_list:
    print(i)
    pass

config = yaml_read('screwai/config/config.yaml')

# 对于待保存数据的文件夹，如果不存在则创建
makedirs(config['save_dir'])


focus_well = 'NB2'
focus_day = '2020-12-27'
focus_day = str(focus_day).split('T')[0]


