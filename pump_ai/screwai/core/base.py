#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/3 21:12
# @Author  : 马赫
# @Email   : 1692303843@qq.com
# @FileName: base.py
import pymysql
import pandas as pd
import yaml
import missingno as msno
import pickle
import os
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def makedirs(path):
    """
    保证path这个文件或文件夹路径存在，如果没有则创建该路径
    path 可以为文件或文件夹
    """
    # 通过是否有.xxx后缀判断是文件或文件夹
    # 如果是文件则去除文件名
    # 如果是文件夹则直接判断该文件夹是否存在并创建
    if os.path.splitext(path)[1] != '':
        # 这个是文件
        path = os.path.split(path)[0]

    if not os.path.isdir(path):
        os.makedirs(path)


# 常用函数

def yaml_read(yaml_path, encoding='utf-8'):
    """
    yaml配置读取器，
    输入yaml文件路径
    返回变量与值的字典
    """
    with open(yaml_path, encoding=encoding) as f:
        _info_yaml = f.read()
    info_yaml = yaml.load(_info_yaml, Loader=yaml.FullLoader)
    return info_yaml


def miss(data):
    # 缺失值可视化
    msno.matrix(data, labels=True)
    plt.show()


def pickle_save(path, content):
    """
    保存py变量
    """
    # 如果不存在该路径，则创建文件夹
    makedirs(path)
    with open(path, 'transformer') as f:
        pickle.dump(content, f)


def pickle_load(path):
    """
    读取py变量
    """
    with open(path, 'rb') as f:
        content = pickle.load(f)
    return content


def calc_pump_dp(df):
    """
    计算螺杆泵生产压差

    :param df: pd.DataFrame, [N, M]
    :return: pd.Series, (N,)
    """
    rou = 0.88  # 密度 g/cm^3
    g = 9.8  # 重力加速度 m/s^2

    # Depth_m	下泵深度(m)
    # FL_above_Pump	沉没度
    # TP_psig	油管压力(psi)
    # CP_psig	套管压力(psi)
    hp = df['Depth_m']  # 下泵深度(m)
    hs = df['FL_above_Pump']  # 沉没度(m)

    # P(MPa) = 10^-3 * rou(g/cm^3) * g(m/s^2) * h(m)
    Pres_p = 1e-3 * rou * g * hp  # 下泵压力
    Pres_s = 1e-3 * rou * g * hs  # 沉没压力

    # psi 与 psig 一样
    # 1 psig = 0.00689 MPa
    tp = df['TP_psig'] * 0.00689
    cp = df['CP_psig'] * 0.00689

    pump_inlet_pressure = Pres_p + tp
    pump_outlet_pressure = Pres_s + cp

    pump_dp = pump_inlet_pressure - pump_outlet_pressure

    return pump_dp
