import pymysql
import pandas as pd


class Database():
    def __init__(self):
        # 打开数据库连接
        db = pymysql.connect(host='120.48.13.79',
                             user='demo',
                             password='cupb@706',
                             database='demo')
        #建立游标
        self.cursor = db.cursor()
    def query(self, table, Wellbore, Date, columns=None):
        #不指定columns即查询全部列
        if columns is None:
            self.cursor.execute('SHOW COLUMNS FROM %s'%(table))
            res = self.cursor.fetchall()
            df = pd.DataFrame(res)
            columns_list = df[0].values
        #若指定columns即按照指定的columns查询
        else:
            columns_list = columns
        #拼接sql语句中要查询的列
        columns_sql = ''
        for i in range(len(columns_list) - 1):
            columns_sql += ("`%s`" + ',') % (columns_list[i])
        columns_sql += "`%s`" % (columns_list[-1])
        #形成sql语句
        sql = "select %s from %s where `Wellbore`='%s' " \
              "and `Date` Between '%s' and '%s'" \
              % (columns_sql, table, Wellbore, Date[0], Date[1])
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        #若查询到即返回结果，查询不到返回None
        if res:
            df = pd.DataFrame(res, columns=columns_list)
            return df
        else:
            return None

database = Database()

# failed_info = pd.read_csv('F:\pythonproject\workover_data_process\keyword_source_find\_НКТ_коррозия.csv')
# for i in range(len(failed_info)):
#     Wellbore = 'NB'+failed_info.loc[i]['Wellbore']
#     Date = [failed_info.loc[i]['Open_Date'],
#             failed_info.loc[i]['Fail_Date']]
#     df = database.query(table='Production_Daily_Data_pcponly',
#                         Wellbore=Wellbore,
#                         Date=Date,
#                         columns=['Wellbore','Date']
#                         )

    