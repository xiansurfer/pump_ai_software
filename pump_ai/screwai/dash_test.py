"""
此应用程序使用内联样式参数和导航组件。
Location用于跟踪当前位置，回调使用呈现适当页面内容的当前位置。
激活的菜单根据当前路径名自动设置每个导航链接。
"""
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, State

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


# 搜索栏函数
def search_top():
    search_bar = dbc.Row(
        [
            dbc.Col(dbc.Input(type="search", placeholder="Sear111ch")),
            dbc.Col(
                dbc.Button(
                    "Search", color="primary", className="ms-2", n_clicks=0
                ),
                width="auto",
            ),
        ],
        className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
        align="center",
    )
    return search_bar


# 导航栏函数
def navbar_top():
    PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
    navbar = dbc.Navbar(    # 导航栏
        dbc.Container(      # 容器
            [
                html.A(
                    # 使用row和col控制logo和brand
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                            dbc.Col(dbc.NavbarBrand("首页", className="ms-2")),
                        ],
                        align="center",
                        className="g-0",	# gutter=0
                    ),
                    href="/",
                    style={"textDecoration": "none"},
                ),
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                dbc.Collapse(   # 三横向
                    search_top(),   # 调用搜索函数
                    id="navbar-collapse",
                    is_open=False,
                    navbar=True,
                ),
            ]
        ),
        color="dark",
        dark=True,
    )
    return navbar


# 侧边栏的样式参数，位置固定和固定宽度
SIDEBAR_STYLE = {
    "position": "fixed",	# 位置固定，只占用限定的宽度，
    "top": '4rem',		# 给导航栏预留出位置
    "left": 0,
    "bottom": 0,
    "width": "14rem",	# 侧边栏宽度
    "padding": "1rem 1rem",		# 内边距
    "background-color": "#f8f9fa",	# 很浅的灰色  #ffffff为全白   #000000为全黑
}

# 主要内容的样式
CONTENT_STYLE = {
    "margin-left": "14rem",		# 给侧边栏留出左侧位置
    "margin-right": "1rem",
    "padding": "2rem 1rem",
}

# 侧边栏函数
def sidebar_left():
    sidebar = html.Div(
        [
            html.H2("主选单",
                    className="display-10",
                    style={'text-align':'center', 'color':'#1E90FF'}),
            html.Hr(),
            html.P("带有导航链接的简单侧栏布局", className="lead"),

            # 可折叠菜单
            dbc.Accordion(
                [
                    dbc.AccordionItem(
                        [
                            dbc.Nav(
                                [
                                    # active="exact" 在当前路径名匹配 href 时自动切换活动状态
                                    dbc.NavItem(dbc.NavLink("Nav 1-1", href="/", active="exact")),
                                    dbc.NavItem(dbc.NavLink("Nav 1-2", href="/page-1", active="exact")),
                                    dbc.NavItem(dbc.NavLink("Nav 1-3", href="/page-2", active="exact")),
                                ],
                                vertical=True,  # 垂直排列
                                pills=True,  # 胶囊
                            ),
                        ],
                        title="菜单项 1", item_id='item-1',
                    ),
                    dbc.AccordionItem(
                        [
                            dbc.Nav(
                                [
                                    # active="exact" 在当前路径名匹配 href 时自动切换活动状态
                                    dbc.NavItem(dbc.NavLink("Nav 2-1", href="/page2-1", active="exact")),
                                    dbc.NavItem(dbc.NavLink("Nav 2-2", href="/page2-2", active="exact")),
                                    dbc.NavItem(dbc.NavLink("Nav 2-3", href="/page2-3", active="exact")),
                                ],
                                vertical=True,  # 垂直排列
                                pills=True,  # 胶囊
                            ),
                        ],
                        title="菜单项 2",item_id='item-2',
                    ),
                    dbc.AccordionItem(
                        [
                            dbc.Nav(
                                [
                                    # active="exact" 在当前路径名匹配 href 时自动切换活动状态
                                    dbc.NavItem(dbc.NavLink("Nav 3-1", href="/page3-1", active="exact")),
                                    dbc.NavItem(dbc.NavLink("Nav 3-2", href="/page3-2", active="exact")),
                                    dbc.NavItem(dbc.NavLink("Nav 3-3", href="/page3-3", active="exact")),
                                ],
                                horizontal=True,  # 垂直排列
                                pills=True,  # 胶囊
                            ),
                        ],
                        title="菜单项 3", item_id='item-3',
                    ),
                ],
                # 页面加载，折叠所有菜单
                # start_collapsed=True,
                # 页面加载，首先打开菜单项
                active_item='item-2',
            ),
        ],
        style=SIDEBAR_STYLE,
    )
    return sidebar


# 内容页面
content = html.Div(id="page-content", style=CONTENT_STYLE,)


# 登录模态框体函数
def login_modal_body():
    email_input = html.Div(
        [
            dbc.Label("用户名", html_for="login-username"),
            dbc.Input(type="text", id="login-username", placeholder="请输入 username"),
            dbc.FormText(
                "",
                color="secondary",
            ),
        ],
        className="mb-3",  # margin-bottom 1rem
    )

    password_input = html.Div(
        [
            dbc.Label("密码", html_for="login-password"),
            dbc.Input(
                type="password",
                id="login-password",
                placeholder="请输入密码",
            ),
            dbc.FormText(
                "", color="secondary"
            ),
        ],
        className="mb-3",
    )

    # 将两个div以列表的形式放入Form中
    form = dbc.Form([email_input, password_input])

    return form



# 登录模态框函数
def login_modal():
    modal = html.Div(
        [
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("欢迎使用本系统，请先登录..."),
                                    close_button=False),    # 屏蔽关闭叉号
                    dbc.ModalBody(
                        # 调用登录输入函数
                        login_modal_body()
                    ),
                    dbc.ModalFooter(
                        dbc.Button(
                            "登录",
                            id="login",
                            className="ms-auto",
                            n_clicks=0,
                        )
                    ),
                ],
                id="modal-centered",
                centered=True,      # 垂直居中模态
                is_open=True,       # 页面加载就出现
                keyboard=False,     # 屏蔽ESC
                backdrop="static",  # 静态背景
            ),
        ]
    )

    return modal


# 主页布局
app.layout = html.Div([dcc.Location(id="url"), navbar_top(), sidebar_left(), content, login_modal()])


# 页面公用函数
def page_content(page, png_file):
    """
    页面内容函数,接受页码和png图片文件名,返回页面的children内容
    """
    result = [
        html.P(f"这是{page}的内容!"),
        html.Img(src=f'/assets/images/{png_file}.png'),
    ]
    return result


# 路由回调函数，会调用page_content()页面公用函数
@app.callback(Output("page-content", "children"),
              [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return page_content('首页', '01')
    elif pathname == "/page-1":
        return page_content('第一页', '02')
    elif pathname == "/page-2":
        return page_content('第二页', '03')
    # 如果用户试图访问其他页面，则返回404消息
    return html.Div(
        [
            html.H1("404: 找不到", className="text-danger"),
            html.Hr(),
            html.P(f"路径 {pathname} 没注册..."),
        ]
    )


# 导航栏小屏幕折叠开关
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# 模态框回调函数
@app.callback(
    Output("modal-centered", "is_open"),
    Input("login", "n_clicks"),
    State("modal-centered", "is_open"),
    State("login-username", "value"),
    State("login-password", "value"),
)
def toggle_modal(n, is_open, username, password):
    # 用户名6位，密码包含123
    if n and len(username)==6 and ('123' in password):
        return not is_open
    else:
        return not is_open
    return is_open



if __name__ == "__main__":
    app.run_server(port=8056, debug=True)
