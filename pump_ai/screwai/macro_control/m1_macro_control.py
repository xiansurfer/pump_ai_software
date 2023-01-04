#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/3 21:59
# @Author  : 马赫
# @Email   : 1692303843@qq.com
# @FileName: m1_macro_control.py


import numpy as np
import pandas as pd
import warnings


warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

from screwai.core.draw_effici import *
from screwai.core.config import *
from screwai.core.database import *
from screwai.core.base import *

db = db_connect()
cur = db.cursor()

# 获取全部列名
sql_code = "select * from Production_Daily_Data_pcponly LIMIT 1"
cur.execute(sql_code)

# 列名列表
column_list = [i[0] for i in cur.description]
for i in column_list:
    # print(i)
    pass

# print(len(column_list))


# %% time
# ==================== 宏观控制图核心算法 ====================
"""
单井——泵效+扭矩，井群——泵效+扭矩
关注的井，和日期

输入:
focus_well = 'NB2'
focus_day = '2020-12-27'

输出:
在macro_control_chart_dir文件夹保存图片
"""
focus_well = 'NB1'
focus_day = '2020-12-27'

focus_day = str(focus_day).split('T')[0]

# ========== 关注某个单井 ==========


# 获取数据
db = db_connect()
cur = db.cursor()
sql_code = "select * from Production_Daily_Data_pcponly where `Wellbore` = '%s'" % focus_well
cur.execute(sql_code)

df = pd.DataFrame(cur.fetchall())

# 修改列名
df.columns = column_list
# 将日期列转化为时间格式
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

# 关注某个泵型号
# df = df.loc[df['Pump_Model'] == 'TP 75-1000']
df = df.loc[df['Pump_Model'] == 'TP 145-1000']


# xy计算规则
# 第一版 无因次举升压头=[泵效 + (油管压力 - 套管压力)*10] / max(FL from Surface)
# x_data = (df['Efficiency %'] + (df['TP_psig'] - df['CP_psig']) * 10) / df['Prod_FL_From_Surface_m'].max()
# 第二版 沉默度/下泵深度
# x_data = df['Prod_FL_From_Surface_m'] / df['Depth_m']
# 第三版x轴，用螺杆泵生产压差
x_data = calc_pump_dp(df)

# y坐标
y_efficiency = df['Efficiency %']
y_torque = df['Amps_Torq']

# 3D的第二个横坐标，这里用转速
RPM = df['SPM/RPM']

# 强行泵效按照转速归一化
# y_efficiency = y_efficiency / RPM * 100
# 从RMP任意转速归一化到100转速
y_efficiency = 1- (100 / RPM) * (1 - y_efficiency)


time_data = df['Date']
time_data = (time_data - time_data.iloc[0]).dt.days

# 画单井泵效
draw_single_well_efficiency(x_data, y_efficiency,
                            time_data, well_name=focus_well,
                            save_img=config['macro_control_chart_dir'] + '/单井泵效控制图')
# 画单井扭矩
draw_single_well_torque(x_data, y_torque,
                        time_data, well_name=focus_well,
                        save_img=config['macro_control_chart_dir'] + '/单井扭矩控制图')

# # 画3D
# fig = plt.figure(figsize=(8, 8))
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(x_data, RPM, y_efficiency, marker='x', color='blue', s=40, label='class 1')
# plt.title('单井-泵效')
# ax.set_xlabel('无因次举升压头')
# ax.set_ylabel('转速')
# ax.set_zlabel('泵效')
# plt.show()

#%%
# ========== 关注井群的某天 ==========

db = db_connect()
cur = db.cursor()
sql_code = "select * from Production_Daily_Data_pcponly where `Date` = '%s'" % focus_day
cur.execute(sql_code)

df = pd.DataFrame(cur.fetchall())
# 修改列名
df.columns = column_list
# 将日期列转化为时间格式
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')


# 关注某个泵型号
df = df.loc[df['Pump_Model'] == 'TP 75-1000']



# xy计算规则

# 第一版 无因次举升压头=[泵效 + (油管压力 - 套管压力)*10] / max(FL from Surface)
# x_data = (df['Efficiency %'] + (df['TP_psig'] - df['CP_psig']) * 10) / df['Prod_FL_From_Surface_m'].max()
# 第二版 沉默度/下泵深度
# x_data = df['Prod_FL_From_Surface_m'] / df['Depth_m']
# 第三版x轴，用螺杆泵生产压差
x_data = calc_pump_dp(df)

# y坐标
y_efficiency = df['Efficiency %']
y_torque = df['Amps_Torq']

# 3D的第二个横坐标，这里用转速
RPM = df['SPM/RPM']

# 强行泵效按照转速归一化
# y_efficiency = y_efficiency / RPM * 100
# 从RMP任意转速归一化到100转速
y_efficiency = 1- (100 / RPM) * (1 - y_efficiency)



# 画井群控制泵效
draw_group_well_efficiency(x_data, y_efficiency,
                           one_day=focus_day,
                           save_img=config['macro_control_chart_dir'] + '/井群泵效控制图')
# 画井群控制扭矩
draw_group_well_torque(x_data, y_torque,
                       one_day=focus_day,
                       save_img=config['macro_control_chart_dir'] + '/井群扭矩控制图')

## 3D图
# fig = plt.figure(figsize=(8, 8))
# ax = fig.add_subplot(111, projection='3d')
#
# ax.scatter(x_data, RPM, y_efficiency, marker='x', color='blue', s=40, label='class 1')
#
# plt.title('井群-泵效')
# ax.set_xlabel('无因次举升压头')
# ax.set_ylabel('转速')
# ax.set_zlabel('泵效')
#
# plt.show()


# #%% 转速异常井分析
# df['SPM/RPM'].hist()
# plt.show()
#
# a = df.loc[df['SPM/RPM'] == df['SPM/RPM'].max()]
# a.to_csv('转速异常井.csv', encoding='utf_8_sig')

# %%
pump_dp = calc_pump_dp(df)
pump_dp.plot()
plt.show()
df.to_excel('NB1.xlsx', encoding='utf_8_sig')


