#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/4 8:19
# @Author  : 马赫
# @Email   : 1692303843@qq.com
# @FileName: d1_info_statistics.py

# 宏观控制图全局信息统计分析

from screwai.core.config import *

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

# =============== 01-故障原因特征 ===============
print('=============== 01-故障原因特征 ===============')
# 读取故障原因特征数据
well_label = pd.read_excel(config['important_dir'] + '/分析数据/01-故障原因特征.xlsx')

# 1. 修井目的缺失填充为当前时刻仍然存活，标记为'alive'。同时去除字符串前后多余字符
well_label.iloc[:, 5] = well_label.iloc[:, 5].apply(lambda x: 'alive' if x is np.nan else str(x).strip())

# 2. 生产厂家缺失，标记为'unknown'。同时去除字符串前后多余字符，和大小写差异导致厂家名称不同
# 注意：'centrilift' 和 'centrlift'是两个不同的厂家，疑似山寨
well_label['生产厂家'] = well_label['生产厂家'].apply(lambda x: 'unknown' if x is np.nan else x.lower().strip())

# 3. 删除未投产的井数据
null_idx = well_label[well_label['开井日期'].isna() & well_label['躺井日期'].isna()].index
well_label.drop(null_idx, inplace=True)

# 4. 删除免修期显著不合理的数据
null_idx = well_label[(well_label['免修期（无故障运转时间）'] > 20000) | (well_label['免修期（无故障运转时间）'] < 0)].index
well_label.drop(null_idx, inplace=True)

# 5. 开井日期缺失，填充上一次躺井日期
open_date_missing_idx = well_label[well_label['开井日期'].isna()].index
well_label.loc[open_date_missing_idx, '开井日期'] = well_label.loc[open_date_missing_idx - 1, '躺井日期'].values

# 6. 一般意义上讲，免修期缺失代表仍然存活，
# 但由于 '开井日期' 缺失，导致免修期缺失，这里根据物理意义进行补充计算
temp_data = well_label.loc[open_date_missing_idx, '躺井日期'] - well_label.loc[open_date_missing_idx, '开井日期']
well_label.loc[open_date_missing_idx, '免修期（无故障运转时间）'] = temp_data.dt.days
well_label.loc[:, '免修期（无故障运转时间）'] = well_label.loc[:, '免修期（无故障运转时间）'].astype('float')

# 7. 免修期统计，对于统计时间仍然工作的井，认为其免修期为全部免修期记录的90%分位数
temp_idx = well_label[well_label['免修期（无故障运转时间）'].isna()].index
alive_quantile = well_label['免修期（无故障运转时间）'].quantile(0.9)
well_label.loc[temp_idx, '免修期（无故障运转时间）'] = alive_quantile

# print(well_label)

print('总记录数', well_label.shape[0])
print('总井数', len(pd.value_counts(well_label.iloc[:, 0])))
print('当前时间无故障总井数', (well_label.iloc[:, 5] == 'alive').sum())

# =============== 02-故障标签统计 ===============
print('=============== 02-故障标签统计 ===============')

purpose_list = well_label.iloc[:, 5]
purpose_list_statistics = pd.value_counts(purpose_list)

_top_purpose = 10

print('\n最多出现的%s个修井目的\n' % _top_purpose)
for num, purpose in enumerate(purpose_list_statistics.index[:_top_purpose]):
    print('%s\t%s' % (purpose_list_statistics[purpose], purpose))

print('\n最少出现的%s个修井目的\n' % _top_purpose)

for num, purpose in enumerate(purpose_list_statistics.index[-_top_purpose:]):
    print('%s\t%s' % (purpose_list_statistics[purpose], purpose))

# 信息保存
# _save_path = config['info_save_dir'] + '/02-top-故障频率统计-自动生成版.xlsx'
# pd.DataFrame(purpose_list_statistics).to_excel(_save_path)


# =============== 03-厂家分析 ===============
print('=============== 03-厂家分析 ===============')

well_label['免修期（无故障运转时间）'].hist()
# plt.ylim(ymax=100)
plt.show()

manufacturers_box = well_label.groupby('生产厂家')
manufacturers_info = manufacturers_box['免修期（无故障运转时间）'].describe().sort_values(by="count", ascending=False)
manufacturers_info = manufacturers_info[manufacturers_info['count'] > 100]
manufacturers_info = manufacturers_info.round(0).astype('int')
print(manufacturers_info)

# _save_path = config['info_save_dir'] + '/03-生产厂家寿命分箱-自动生成版.xlsx'
# pd.DataFrame(manufacturers_info).to_excel(_save_path)


# =============== 04-单井厂家对比 ===============
print('=============== 04-单井厂家对比 ===============')
# 各井用不同生产厂家的螺杆泵生存期统计

well_box = well_label.groupby('井号')

# 各井用不同生产厂家的螺杆泵生存期统计
well_manufacturers_mean_life_df = []
for well_name, well_data in well_box:
    i_well_mans_mean = well_data.groupby('生产厂家')['免修期（无故障运转时间）'].agg('mean').astype('int')
    i_well_mans_mean.rename(well_name, inplace=True)
    well_manufacturers_mean_life_df.append(i_well_mans_mean)
    # break

well_manufacturers_mean_life_df = pd.DataFrame(well_manufacturers_mean_life_df)
# 选择使用次数超过100次的生产厂家进行分析
well_manufacturers_mean_life_df = well_manufacturers_mean_life_df[manufacturers_info.index]
print(well_manufacturers_mean_life_df)


def trim_mean(scores):
    scores1 = scores[~np.isnan(scores)].values
    if len(scores1) >= 3:
        scores2 = np.sort(scores1)
        scores2 = scores2[1:-1].mean()

    elif len(scores1) >= 1:
        scores2 = scores1.mean()
    else:
        scores2 = None
    return scores2


# 求取截断（最值的）平均寿命
well_life_trim_mean = well_manufacturers_mean_life_df.apply(trim_mean, axis=1)
# 缺失值填补平均值
well_life_trim_mean[well_life_trim_mean.isna()] = well_life_trim_mean.mean()
# 将各井平均寿命并入单井厂家对比表
well_manufacturers_mean_life_df['trim_mean'] = well_life_trim_mean

# _save_path = config['info_save_dir'] + '/04-单井厂家对比-自动生成版.xlsx'
# pd.DataFrame(well_manufacturers_mean_life_df).to_excel(_save_path)
