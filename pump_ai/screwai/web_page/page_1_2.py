#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/28 23:23
# @Author  : 路鑫
# @Email   : 497347297@qq.com
# @FileName: page_1_2.py

import dash
from dash.dependencies import Input, Output
from dash import dcc, html, dash_table,callback_context
import dash_bootstrap_components as dbc
import pandas as pd
import pymysql
import arrow as ar
from datetime import  datetime

class page_1_2():
    def __init__(self):
        self.head_style = {
            # 'position':'fixed',
            'left':'50%',
            'font-size':'30px',
            'text-align':'center'
        }

        self.tltle_style = {
            'margin-top':'40px',
            'font-size':'30px',
        }

        self.wellinput_lable_style = {
            'display':'inline-block',
            'margin-top':'115px'
        }
        self.wellinput_style = {
            'width': '10rem',
            'height': '2.5rem',
            'margin-right': '30px',
            'margin-top': '105px',
            # 'margin-left': '100px',
            'font-size': '22px',
            # 'display': 'inline-block'
        }

        self.dateinput_lable_style = {
            # 'margin-left': '300px',
            'margin-top': '115px'
        }

        self.dateinput_style = {
            'width': '10rem',
            'height': '2.5rem',
            'margin-right': '30px',
            'margin-top': '115px',
            # 'margin-left': '100px',
            'font-size': '22px',
            # 'display': 'inline-block',
            "z-index":"999"
        }

    def page_layoutset(self):
        layout = [
            html.Div('螺杆泵AI数据表单',style=self.head_style),
            html.Div('数据查询',
                     style=self.tltle_style),


            dbc.Label('请输入井名:', id='label1',
                      ),
            dbc.Input(type='text', children='wellbore', id='wellbore',
                     ),

            dbc.Label('请输入起止日期:', id='label2',
                      style={'margin-left':'20px'}),
            dcc.DatePickerRange(
                id='dt_range',
                start_date=ar.get(2017, 1, 1).date(),
                end_date_placeholder_text='选择日期',
                display_format='Y-MM-DD',
                month_format='Y-MM',
                first_day_of_week=1,
                min_date_allowed=ar.get(2017, 1, 1).date(),
                max_date_allowed=ar.get(2021, 12, 31).date(),

            ),

            html.Button('确认', id='btn1', n_clicks=0,
                        style={'height':'3rem',
                               'margin-left':'10px'}),
            html.Div([
                dbc.Label('', id='message')
            ]),
            # html.Div(
            #     dbc.Container(id='table', fluid=True,),
            # style={'overflow':'scroll','weight':'650px','height':'525px',
            #        'margin-top': '150px',}),
            dbc.Container(id='table', fluid=True,
                          )

        ]

        return layout

    '日期转字符'
    def date_convert(self,date):
        try:
            return datetime.strftime(date, '%Y-%m-%d')
        except:
            return ''

    """
    para:井名，开始日期，结束日期
    return:data
    func:从数据库中获取对应井名及时间段数据，形成dataframe
    """
    def table_data_get(self,wellname, start_data, end_date):
        db = pymysql.connect(host='120.48.13.79',
                             user='root',
                             password='59a7f02b0113ee9b',
                             database='sinopecdatabase')
        cursor = db.cursor()
        sql = "select * from dpr where " \
              "`Wellbore` = '%s' AND `Production Date` " \
              "BETWEEN '%s' AND '%s'" % (wellname, start_data, end_date)
        cursor.execute(sql)
        data = pd.DataFrame(cursor.fetchall())
        if not data.empty:

            sql_col = 'DESC dpr'
            cursor.execute(sql_col)
            col = pd.DataFrame(cursor.fetchall())[0]
            data.columns = col

            # 处理日期格式
            date_col_list = ['Production Date', 'Last Gauge Date',
                             'Gas Test Date', 'LastWorkoverDate', 'PBHP Date']
            for date_col in date_col_list:
                data[date_col] = data[date_col]. \
                    map(lambda x: self.date_convert(x))

            # 处理浮点小数位
            float_col_list = ['Liquid Rate', 'Oil Rate', 'Gas Rate', 'GOR', 'TP', 'CP',
                              'PBHP', 'Pump Efficiency', 'Last Gauge BFPD']
            for float_col in float_col_list:
                data[float_col] = data[float_col].map(lambda x: round(x, 3))
            print(len(data.columns[0]))
            # 设置layout
            layout = dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in data.columns],
                data=data.to_dict('records'),
                export_columns='visible',
                export_format='xlsx',
                export_headers='display',

                style_data={
                    'lineHeight': '8px'
                },
                style_cell={'textAlign': 'center'},
                # 数据附加样式，数据偶数行浅灰底色

                # 表头样式：浅灰底色，黑字，加粗
                style_header={
                    'fontWeight': 'bold',
                },
                fixed_rows={'headers':True},
                page_size=100,
                style_data_conditional=[{'if':{'column_id':f'{column}'},
                                         'width':f'{130*(len(column)/10)}px'}
                                        for column in data.columns]

            )
        else:
            layout = html.Label('无匹配数据数据，请重新选择',
                                style={'font-size': '22px'})
        return layout

    def flash_layout(self,app):
        @app.callback(
            Output('table', 'children'),
            [Input('dt_range', 'start_date')],
            [Input('dt_range', 'end_date')],
            [Input('wellbore', 'value')],
            [Input('btn1', 'n_clicks')],
            [Input('table', 'children')]

        )
        def liquid_data_get(start, end, well, btn, table):
            changed_id = [p['prop_id'] for p in callback_context.triggered][0]
            if 'btn1' in changed_id and start and end and well:
                layout = self.table_data_get(well, start, end)
                return layout
            elif ('btn1' in changed_id) and \
                    ((end == None) or (well == None) or (well == '')):
                layout = html.Label('缺少参数，请输入参数',
                                    style={'font-size': '22px'})
                return layout
            else:
                if table:
                    return table
                else:
                    layout = html.Label('')
                    return layout
app = dash.Dash()
app.layout = html.Div(page_1_2().page_layoutset())
page_1_2().flash_layout(app)
app.run_server(port=8050)