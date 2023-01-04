

def split_func(x, a, b):
    """
    宏观控制图的分割曲线

    Parameters
    ----------
    x : TYPE float
        DESCRIPTION. 自变量
    a : TYPE float
        DESCRIPTION. 系数
    b : TYPE float
        DESCRIPTION. 系数

    Returns
    -------
    y : TYPE float
        DESCRIPTION. 因变量
    """
    
    y = a / (x + b) - a / b
    return y


def inverse_split_func(y, a, b):
    """
    宏观控制图的分割曲线
    split_func()的反函数

    Parameters
    ----------
    y : TYPE float
        DESCRIPTION. 因变量
    a : TYPE float
        DESCRIPTION. 系数
    b : TYPE float
        DESCRIPTION. 系数

    Returns
    -------
    x : TYPE float
        DESCRIPTION. 自变量
    """
    x = a * b / (b * y + a) - b
    return x
