#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/4 8:43
# @Author  : 马赫
# @Email   : 1692303843@qq.com
# @FileName: config.py
from screwai.core.base import *

# core.config.py所在目录
core_path = os.path.dirname(__file__)
# config.yaml路径
config_path = os.path.abspath(os.path.join(core_path, "../config/"))
main_config_name = os.path.abspath(
    os.path.join(config_path, "config.yaml/")
)

# 加载主配置信息
config = yaml_read(main_config_name)

# =============== 1.程序数据保存总路径 ===============
data_dir = os.path.abspath(
    os.path.join(config_path, config['data_dir'])
)

# 更新数据总路径的绝对路径
config['data_dir'] = data_dir


# =============== 2.重要不可变数据总路径 ===============
important_dir = os.path.abspath(
    os.path.join(data_dir, config['important_dir'])
)
config['important_dir'] = important_dir


# =============== 3.程序统计信息保存分路径 ===============
info_save_dir = os.path.abspath(
    os.path.join(data_dir, config['info_save_dir'])
)
config['info_save_dir'] = info_save_dir

# =============== 4.其他保存数据总路径 ===============

othe_save_dir = os.path.abspath(
    os.path.join(data_dir, config['othe_save_dir'])
)
config['othe_save_dir'] = othe_save_dir

# =============== 5.宏观控制图总路径 ===============

macro_control_chart_dir = os.path.abspath(
    os.path.join(data_dir, config['macro_control_chart_dir'])
)
config['macro_control_chart_dir'] = macro_control_chart_dir




if __name__ == '__main__':
    for i in config:
        print(i, '\t', config[i])


# 配置信息自动初始化
for i in config.keys():
    # 对于目录而言，如果不存在，则递归建立
    if i[-4:] == '_dir':
        new_dir = config[i]
        # 确保该文件夹存在
        makedirs(new_dir)
        # print(i, new_dir)



