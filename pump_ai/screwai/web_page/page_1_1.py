#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/28 22:37
# @Author  : 路鑫
# @Email   : 497347297@qq.com
# @FileName: page_1_1.py

from dash import Input, Output, dcc, html, State
from dash import callback_context
import pymysql
import pandas as pd
import plotly.graph_objs as go


class page_1_1():
    def __init__(self):
        self.wellname_defult = 'NB1'

    """
    设置page_1_1的layout
    """
    def page_layoutset(self):
        """
        页面内容函数,接受页码和png图片文件名,返回页面的children内容
        """
        layout = [
            #________________产量数据layout________________
            html.H1(
                children='螺杆泵生产数据曲线',
                style=dict(textAlign='center')
            ),
            html.Div(
                children='copyright:中国石油大学(北京)采油采气工艺课题组',
                style=dict(textAlign='right')
            ),
            html.H2(children='产量数据', ),
            html.Label('请输入井名:', id='label1'),
            dcc.Input(children='wellbore', id='wellinput1',
                      value=self.wellname_defult),
            html.Button('确认', id='btn1', n_clicks=0),
            dcc.Checklist(
                options=[{'label': '产液', 'value': 'Liquid Rate'},
                         {'label': '产油', 'value': 'Oil Rate'},
                         {'label': '产气', 'value': 'Gas Rate'}],
                value=['Liquid Rate', 'Oil Rate', 'Gas Rate'],
                id='check1'),

            dcc.Graph(id='graph1'),
            dcc.Slider(
                id='year-slider1',
                min=2017,
                max=2021,
                value=2018,
                marks={'2017': '2017', '2018': '2018', '2019': '2019', '2020': '2020',
                       '2021': '2021'},
                step=None
            ),
            # ________________产量数据layout________________
            html.Hr(),
            # ________________压力数据layout________________
            html.H2(children='压力数据'),
            html.Label('请输入井名:', id='label2'),
            dcc.Input(children='wellbore', id='wellinput2',
                      value=self.wellname_defult),
            html.Button('确认', id='btn2', n_clicks=0),
            dcc.Checklist(
                options=[{'label': '油压', 'value': 'TP'},
                         {'label': '套压', 'value': 'CP'},
                         {'label': '井底流压', 'value': 'PBHP'}],
                value=['TP', 'CP', 'PBHP'],
                id='check2'),
            dcc.RadioItems(
                options=[{'label': 'atm', 'value': 1},
                         {'label': 'psi', 'value': 14.695},
                         {'label': 'MPa', 'value': 0.1}],
                value=1, id='radio1'),
            dcc.Graph(id='graph2'),
            dcc.Slider(
                id='year-slider2',
                min=2017,
                max=2021,
                value=2018,
                marks={'2017': '2017', '2018': '2018', '2019': '2019', '2020': '2020',
                       '2021': '2021'},
                step=None
            ),
            html.Hr(),
            # ________________压力数据layout________________

            # ________________液面数据layout________________
            html.H2(children='液面数据'),
            html.Label('请输入井名:', id='label3'),
            dcc.Input(children='wellbore', id='wellinput3',
                      value=self.wellname_defult),
            html.Button('确认', id='btn3', n_clicks=0),
            dcc.Checklist(
                options=[{'label': '下泵深度', 'value': 'Pump Depth'},
                         {'label': '动液面', 'value': 'Dynamic level'},
                         {'label': '沉没度', 'value': 'Submergence'}],
                value=['Pump Depth', 'Dynamic level', 'Submergence'],
                id='check3'),
            dcc.Graph(id='graph3'),
            dcc.Slider(
                id='year-slider3',
                min=2017,
                max=2021,
                value=2018,
                marks={'2017': '2017', '2018': '2018', '2019': '2019', '2020': '2020',
                       '2021': '2021'},
                step=None
            ),
            # ________________液面数据layout________________
        ]

        return layout

    """
    产量数据请求
    根据井名，字段名，结束日期向服务器请求数据，并返回数据字典
    """
    def liquid_plot(self,wellname,check,endyear=2018):
        db = pymysql.connect(host='120.48.13.79',
                             user='root',
                             password='59a7f02b0113ee9b',
                             database='sinopecdatabase')
        cursor = db.cursor()
        unit_dic = {'Liquid Rate':'Liquid Rate(m3/day)',
                    'Oil Rate':'Oil Rate(t/day)','Gas Rate':'Gas Rate(m3/day)'}
        endyear = int(endyear)
        basic_select = ['Wellbore','Production Date']
        select_col = basic_select+check
        select_str = ''
        for item in select_col:
            select_str+="`%s`"%(item)+','
        select_str = select_str.strip(',')

        sql = "select %s FROM dpr " \
              "WHERE Wellbore = '%s'" % (select_str,wellname)

        cursor.execute(sql)
        data = pd.DataFrame(cursor.fetchall(),
                            columns=select_col)
        data['Production Date'] = pd.to_datetime(data['Production Date'],
                                                 format='%Y-%m-%d')
        data = data[data['Production Date'].dt.year<endyear]
        data_list = [{'x': data['Production Date'], 'y': data[col],
                   'type': 'scatter', 'name': unit_dic[col]} for col in check]
        data_dic = dict(
            data=data_list,
            layout=go.Layout(
                title='%s井流量数据'%(wellname),
                xaxis=dict(title='Production Date'),
                yaxis=dict(title='Rate'),
            )
        )

        return data_dic

    """
    压力数据请求
    根据井名，字段名，结束日期向服务器请求数据，并返回数据字典
    """
    def pressure_plot(self,wellname, check, pre_conver, endyear=2018):
        db = pymysql.connect(host='120.48.13.79',
                             user='root',
                             password='59a7f02b0113ee9b',
                             database='sinopecdatabase')
        cursor = db.cursor()
        endyear = int(endyear)

        basic_select = ['Wellbore', 'Production Date']
        select_col = basic_select + check

        select_str = ''
        for item in select_col:
            select_str += "`%s`" % (item) + ','
        select_str = select_str.strip(',')

        sql = "select %s FROM dpr " \
              "WHERE Wellbore = '%s'" % (select_str, wellname)

        cursor.execute(sql)
        data = pd.DataFrame(cursor.fetchall(),
                            columns=select_col)
        data['Production Date'] = pd.to_datetime(data['Production Date'],
                                                 format='%Y-%m-%d')

        data = data[data['Production Date'].dt.year < endyear]
        data[check] = data[check] * pre_conver
        data_list = [{'x': data['Production Date'], 'y': data[col],
                      'type': 'scatter', 'name': col} for col in check]
        data_dic = dict(
            data=data_list,
            layout=go.Layout(
                title='%s井压力数据' % (wellname),
                xaxis=dict(title='Production Date'),
                yaxis=dict(title='Pressure'),
            )
        )
        return data_dic

    """
    液面数据请求
    根据井名，字段名，结束日期向服务器请求数据，并返回数据字典
    """
    def depth_plot(self,wellname, check, endyear=2018):
        db = pymysql.connect(host='120.48.13.79',
                             user='root',
                             password='59a7f02b0113ee9b',
                             database='sinopecdatabase')
        cursor = db.cursor()
        endyear = int(endyear)

        basic_select = ['Wellbore', 'Production Date']
        select_col = basic_select + check

        select_str = ''
        for item in select_col:
            select_str += "`%s`" % (item) + ','
        select_str = select_str.strip(',')

        sql = "select %s FROM dpr " \
              "WHERE Wellbore = '%s'" % (select_str, wellname)

        cursor.execute(sql)
        data = pd.DataFrame(cursor.fetchall(),
                            columns=select_col)
        data['Production Date'] = pd.to_datetime(data['Production Date'],
                                                 format='%Y-%m-%d')
        data = data[data['Production Date'].dt.year < endyear]
        data_list = [{'x': data['Production Date'], 'y': data[col],
                      'type': 'scatter', 'name': col} for col in check]
        data_dic = dict(
            data=data_list,
            layout=go.Layout(
                title='%s井液面数据' % (wellname),
                xaxis=dict(title='Production Date'),
                yaxis=dict(title='Depth'),
            )
        )
        return data_dic

    """
    传入主程序app对象，对页面进行刷新
    """
    def flash_layout(self,app):
        # ________________产量数据刷新________________
        @app.callback(
            Output('graph1', 'figure'),
            [Input('wellinput1', 'value')],
            [Input('btn1', 'n_clicks')],
            [Input('check1', 'value')],
            [Input('year-slider1', 'value')],
            [Input('graph1', 'figure')],
        )
        def liquid_data_get(wellname, bt1, check1, year,fig):
            changed_id = [p['prop_id'] for p in callback_context.triggered][0]
            if 'btn1' in changed_id or 'year-slider1' in changed_id or 'check1' in changed_id:
                data_dic = self.liquid_plot(wellname, check1, year)
            else:
                if fig:
                    data_dic = fig
                else:
                    data_dic = self.liquid_plot(self.wellname_defult, check1, year)

            return data_dic
        # ________________产量数据刷新________________

        # ________________压力数据刷新________________
        @app.callback(
            Output('graph2', 'figure'),
            [Input('wellinput2', 'value')],
            [Input('btn2', 'n_clicks')],
            [Input('check2', 'value')],
            [Input('year-slider2', 'value')],
            [Input('radio1', 'value'),],
            [Input('graph2', 'figure')],
        )
        def pressure_data_get(wellname, bt2, check1, year, pre_conver,fig):
            changed_id = [p['prop_id'] for p in callback_context.triggered][0]
            if ('btn2' in changed_id) or \
                    ('year-slider2' in changed_id) or \
                    ('check2' in changed_id):
                data_dic = self.pressure_plot(wellname, check1, pre_conver, year)
            else:
                if fig:
                    data_dic = fig
                else:
                    data_dic = self.pressure_plot(self.wellname_defult, check1,
                                               pre_conver, year, )
            return data_dic
        # ________________压力数据刷新________________

        # ________________液面数据刷新________________
        @app.callback(
            Output('graph3', 'figure'),
            [Input('wellinput3', 'value')],
            [Input('btn3', 'n_clicks')],
            [Input('check3', 'value')],
            [Input('year-slider3', 'value')],
            [Input('graph3', 'figure')]
        )
        def pressure_data_get(wellname, bt3, check3, year,fig):
            changed_id = [p['prop_id'] for p in callback_context.triggered][0]
            if 'btn3' in changed_id or 'year-slider3' in changed_id or 'check3' in changed_id:
                data_dic = self.depth_plot(wellname, check3, year, )
            else:
                if fig:
                    data_dic = fig
                else:
                    data_dic = self.depth_plot(self.wellname_defult, check3, year, )

            return data_dic
        # ________________液面数据刷新________________

