#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/3 21:08
# @Author  : 马赫
# @Email   : 1692303843@qq.com
# @FileName: database.py
import pandas as pd
import pymysql


def db_connect():
    db = pymysql.connect(host='120.48.13.79',
                         user='sinopec_usage',
                         password='myiJ2WkCVA4OPggC',
                         database='sinopecdatabase')
    return db



class Database():
    def __init__(self):
        self.cursor = None
        self.connect()

    def connect(self):
        # 打开数据库连接
        db = db_connect()
        # 建立游标
        self.cursor = db.cursor()

    def query(self, Wellbore, Date, columns=None, table='production_daily_data'):
        # 每次查询都先连接，避免超时
        self.connect()
        # 不指定columns即查询全部列
        if columns is None:
            self.cursor.execute('SHOW COLUMNS FROM %s' % (table))
            res = self.cursor.fetchall()
            df = pd.DataFrame(res)
            columns_list = df[0].values
        # 若指定columns即按照指定的columns查询
        else:
            columns_list = columns
        # 拼接sql语句中要查询的列
        columns_sql = ''
        for i in range(len(columns_list) - 1):
            columns_sql += ("`%s`" + ',') % (columns_list[i])
        columns_sql += "`%s`" % (columns_list[-1])
        # 形成sql语句
        sql = "select %s from %s where `Wellbore`='%s' " \
              "and `Date` Between '%s' and '%s'" \
              % (columns_sql, table, Wellbore, Date[0], Date[1])
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        # 若查询到即返回结果，查询不到返回None
        if res:
            df = pd.DataFrame(res, columns=columns_list)
            return df
        else:
            return None
