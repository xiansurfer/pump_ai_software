#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/25 22:09
# @Author  : 马赫
# @Email   : 1692303843@qq.com
# @FileName: screwai_app.py


import sys
sys.path.append('web_page')

from web_page.page_1_1 import page_1_1
from web_page.page_1_2 import page_1_2
import pandas as pd
import plotly.graph_objs as go
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, State,callback_context
import pymysql
# ================== 页面设计参数 ==================

# 菜单目录，一级菜单，二级菜单，url相对链接
# ['level1', 'level2', 'url', 'func']
MENU_INFO = [
    ['数据湖', '生产数据曲线', '/', 'page_1_1'],  # 第一页菜单是url首页路由
    ['数据湖', '生产数据表单', '/page_1_2', 'page_1_2'],
    ['数据湖', '1.3', '/page_1_3', 'page_1_3'],

    ['智能生产', '2.1', '/page_2_1', 'page_2_1'],
    ['智能生产', '2.2', '/page_2_2', 'page_2_2'],

    ['宏观控制', '3.1', '/page_3_1', 'page_3_1'],
    ['宏观控制', '3.2', '/page_3_2', 'page_3_2'],
]
MENU_INFO = pd.DataFrame(MENU_INFO,
                         columns=['level1', 'level2', 'url', 'func'])

# 重要页面标签id参数
HTML_ID = {
    'content': 'page-content',  # 网页内容id
    'url': 'url',  # url链接id
}

# 侧边栏的样式参数，位置固定和固定宽度
SIDEBAR_STYLE = {
    "position": "fixed",  # 位置固定，只占用限定的宽度，
    "top": '0rem',  # 上方留出位置
    "left": 0,
    "bottom": 0,
    "width": "14rem",  # 侧边栏宽度
    "padding": "1rem 1rem",  # 内边距
    "background-color": "#f8f9fa",  # 很浅的灰色  #ffffff为全白   #000000为全黑
    "z-index":"999"
}

# 主要内容的样式
CONTENT_STYLE = {
    "margin-left": "14rem",  # 给侧边栏留出左侧位置
    "margin-right": "1rem",
    "padding": "2rem 1rem",
}

"""用于测试页面"""


# def page_1_1(*args):
#     """
#     页面内容函数,接受页码和png图片文件名,返回页面的children内容
#     """
#     print('成功运行page_1_1', args)
#
#     result = [
#         html.P(f"这是{args}的内容!"),
#     ]
#     return result

def liquid_plot(wellname,check,endyear=2018):
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
# 路由回调函数，会调用page_content()页面公用函数

def sidebar_left():
    """
    侧边栏菜单函数
    TODO 可能后期需要传入的全局变量
    MENU_INFO: 从全局变量传入的菜单信息矩阵
    :return:
    """

    # 双层循环，构建两级菜单

    dbc_menu_list = []
    level1_list = pd.unique(MENU_INFO['level1'])
    for num, level1_name in enumerate(level1_list):
        level_1 = level1_name  # 一级菜单名
        # 矩阵 ['level1', 'level2', 'url', 'func']
        level1_df = MENU_INFO[MENU_INFO['level1'] == level1_name]

        # 同属于一级菜单下的二级菜单
        item_list = []
        for j in range(len(level1_df)):
            _single_menu = level1_df.iloc[j]
            level_2 = _single_menu[1]  # 二级菜单名
            url = _single_menu[2]  # url

            # 封装item二级菜单，菜单名，超链接，设为激活状态
            # active="exact" 在当前路径名匹配 href 时自动切换活动状态
            item = dbc.NavLink("%s" % level_2, href="%s" % url, active="exact")
            item_list.append(item)

        # horizontal=True,  # 垂直排列
        # pills=True,  # 胶囊
        item_list = dbc.Nav(item_list, horizontal=True, pills=True)

        menu = dbc.AccordionItem(item_list, title=level_1, item_id='item-%s' % (num + 1))
        dbc_menu_list.append(menu)

    sidebar = html.Div(
        [
            # 主选单部件
            html.H2("螺杆泵AI系统", className="display-10",
                    style={'text-align': 'center', 'color': '#1E90FF'}),

            # 水平分割线部件
            html.Hr(),

            # 可折叠菜单
            dbc.Accordion(
                dbc_menu_list,

                # 默认折叠所有菜单
                # start_collapsed=True

                # 默认打开指定一个菜单项
                active_item='item-1'
            )
        ],
        style=SIDEBAR_STYLE,
    )

    return sidebar


def page_error(text='未知异常'):
    """
    异常页面返回模板
    :param text: str
    :return: 页面
    """
    return html.Div(
        [
            html.H1("Error: ", className="text-danger"),
            html.Hr(),
            html.H1(text, className="text-danger"),

        ]
    )


# 主程序
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
# 内容页面
content = html.Div(id="%s" % HTML_ID['content'], style=CONTENT_STYLE)
# 主页布局
app.layout = html.Div([
    dcc.Location(id="%s" % HTML_ID['url']),  # 超链接调用方式
    sidebar_left(),  # 侧边栏部件
    content
])


# 路由转发页面函数
@app.callback(Output("%s" % HTML_ID['content'], "children"),
              [Input("%s" % HTML_ID['url'], "pathname")],
              [Input("%s" % HTML_ID['content'], "children")])
def render_page_content(pathname,*args):
    # TODO 添加额外传入参数
    # pathname = '/'
    # args = []

    menu = MENU_INFO[MENU_INFO['url'] == pathname]
    if len(menu) == 1:
        # 获取函数名的字符串
        page_func = menu['func'].values[0]
        # 将page_func转为函数名
        try:
            page_func = eval(page_func)
            layout = page_func().page_layoutset()
            return layout

        except Exception as e:
            text = '当前页面没有做好或出现其他问题' + pathname

        return page_error(text)

    elif len(menu) > 1:
        # 返回报错，提示一个url指向多个函数
        text = '一个url指向多个函数' + pathname
        return page_error(text)

    else:
        text = '404页面不存在' + pathname
        return page_error(text)

page_1_1().flash_layout(app)
page_1_2().flash_layout(app)

if __name__ == "__main__":
    app.run_server(port=8057, debug=False)
