from split_section import split_func, inverse_split_func

import matplotlib.pyplot as plt
import numpy as np

import scipy.optimize as opt

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False



def draw_single_well_efficiency(x, y, time_data, well_name, save_img=None):
    """泵效 单井控制图"""
    plt.figure(figsize=(10, 4), dpi=300)
    plt.xlim(0, 1.0)
    plt.ylim(-0.01, 200)

    plt.scatter(x, y, c=time_data)
    plt.colorbar()
    # plt.title('单井泵效控制图')
    plt.title(well_name + '单井泵效控制图')
    plt.xlabel('无因次举升压头')
    plt.ylabel('泵效(%)')
    
    
    # ##### 分区参考线 (曲线) #####

    # 第一个点是参数偏小区的左下角
    # 第二个点是参数偏小区的右上角
    # 第三个点是曲线的最右面的拟合控制点
    rect = np.array([
            [0.089, 70],
            [0.22,  95],
            [1,     101],
        ])
    
    popt, pcov = opt.curve_fit(split_func, xdata=rect[:, 0], ydata=rect[:, 1])
    a = popt[0]
    b = popt[1]
    
    x_aux = np.linspace(0, 1, num=100)
    # 推荐ab参数 -4.66825533,  0.04327136
    y_aux = split_func(x_aux, a, b) 
    
    plt.plot(x_aux, y_aux, color='red')


    # 漏失区+参数偏大区
    y1_start = 25  # 漏失区+参数偏大区的上界
    # 通过反函数计算漏失区上界与分区参考线的交点
    x1_start = inverse_split_func(y1_start, a, b)
    
    plt.plot([x1_start, 1], [y1_start, y1_start], c='red')
    
    x2_start = 0.3
    plt.plot([x2_start, x2_start], [0, y1_start], c='red')

    plt.text(0.1, 5, "漏失区", size = 10, alpha = 0.8)
    plt.text(0.6, 5, "参数偏大区", size = 10, alpha = 0.8)
    
    # 参数偏小区
    plt.plot([rect[0,0], rect[1,0]], [split_func(rect[0,0], a, b), split_func(rect[0,0], a, b)], c='red')
    plt.plot([rect[1,0], rect[1,0]], [split_func(rect[0,0], a, b), split_func(rect[1,0], a, b)], c='red')
    plt.text(rect[0,0]+0.02 , rect[0,1] + 5,
             "参数偏小区", size = 10, alpha = 0.8)
    
    
    if save_img is not None:
        plt.savefig(save_img, bbox_inches='tight')
    plt.close()

def draw_group_well_efficiency(x, y, one_day, save_img=None):
    """泵效 井群控制图"""
    plt.figure(figsize=(10, 4), dpi=300)
    plt.xlim(0, 1.0)
    plt.ylim(-0.01, 200)

    plt.scatter(x, y)
    plt.title(one_day + '井群泵效控制图')
    plt.xlabel('无因次举升压头')
    plt.ylabel('泵效(%)')
    
    # ##### 分区参考线 #####

    # 第一个点是参数偏小区的左下角
    # 第二个点是参数偏小区的右上角
    # 第三个点是曲线的最右面的拟合控制点
    rect = np.array([
            [0.089, 70],
            [0.22,  95],
            [1,     101],
        ])
    
    popt, pcov = opt.curve_fit(split_func, xdata=rect[:, 0], ydata=rect[:, 1])
    a = popt[0] 
    b = popt[1]
    
    x_aux = np.linspace(0, 1, num=100)
    # 推荐ab参数 -4.66825533,  0.04327136
    y_aux = split_func(x_aux, a, b) 
    
    plt.plot(x_aux, y_aux, color='red')


    # 漏失区+参数偏大区
    y1_start = 25
    x1_start = inverse_split_func(y1_start, a, b)
    
    plt.plot([x1_start, 1], [y1_start, y1_start], c='red')
    
    x2_start = 0.3
    plt.plot([x2_start, x2_start], [0, y1_start], c='red')

    plt.text(0.1, 5, "漏失区", size = 10, alpha = 0.8)
    plt.text(0.6, 5, "参数偏大区", size = 10, alpha = 0.8)
    
    # 参数偏小区
    plt.plot([rect[0,0], rect[1,0]], [split_func(rect[0,0], a, b), split_func(rect[0,0], a, b)], c='red')
    plt.plot([rect[1,0], rect[1,0]], [split_func(rect[0,0], a, b), split_func(rect[1,0], a, b)], c='red')
    plt.text(rect[0,0]+0.02 , rect[0,1] + 5,
             "参数偏小区", size = 10, alpha = 0.8)
        
    if save_img is not None:
        plt.savefig(save_img, bbox_inches='tight')
    plt.close()

def draw_single_well_torque(x, y, time_data, well_name, save_img=None):
    """扭矩 单井控制图"""
    plt.figure(figsize=(10, 4), dpi=300)
    plt.xlim(0, 1.0)
    plt.ylim(-0.01, 200)

    plt.scatter(x, y, c=time_data)
    plt.colorbar()
    plt.title(well_name + '单井扭矩控制图')
    plt.xlabel('无因次举升压头')
    plt.ylabel('扭矩(A)')
    
    # ##### 分区参考线 #####
    # 断脱区+定子脱胶区
    xy1 = [0.1, 0]
    xy2 = [1, 80]
    plt.plot([xy1[0], xy2[0]], [xy1[1], xy2[1]], c='red')
    
    xy3 = [0.38, 0]
    _x4 = 0.38
    xy4 = [_x4, np.interp(_x4, [xy1[0], xy2[0]], [xy1[1], xy2[1]])]
    
    plt.plot([xy3[0], xy4[0]], [xy3[1], xy4[1]], c='red')
    plt.text(0.3, 5, "断脱区", size = 10, alpha = 0.8)
    plt.text(0.6, 5, "定子脱胶区", size = 10, alpha = 0.8)
    
    # 扭矩正常区
    xy5 = [0, 60]
    xy6 = [1, 155]
    plt.plot([xy5[0], xy6[0]], [xy5[1], xy6[1]], c='red')
    plt.text(0.3, 50, "扭矩正常区", size = 10, alpha = 0.8)
    
    # 定子溶胀区+结蜡区
    _x7 = 0.38
    xy7 = [_x7, np.interp(_x7, [xy5[0], xy6[0]], [xy5[1], xy6[1]])]
    xy8 = [_x7, 200]
    plt.plot([xy7[0], xy8[0]], [xy7[1], xy8[1]], c='red')
    plt.text(0.1, 150, "定子溶胀区", size = 10, alpha = 0.8)
    plt.text(0.5, 150, "结蜡区", size = 10, alpha = 0.8)
    
    
    if save_img is not None:
        plt.savefig(save_img, bbox_inches='tight')
    plt.close()

def draw_group_well_torque(x, y, one_day, save_img=None):
    """扭矩 井群控制图"""
    plt.figure(figsize=(10, 4), dpi=300)
    plt.xlim(0, 1.0)
    plt.ylim(-0.01, 200)

    plt.scatter(x, y)
    plt.title(one_day + '井群扭矩控制图')
    plt.xlabel('无因次举升压头')
    plt.ylabel('扭矩(A)')

    
    # ##### 分区参考线 #####
    # 断脱区+定子脱胶区
    xy1 = [0.1, 0]
    xy2 = [1, 80]
    plt.plot([xy1[0], xy2[0]], [xy1[1], xy2[1]], c='red')
    
    xy3 = [0.38, 0]
    _x4 = 0.38
    xy4 = [_x4, np.interp(_x4, [xy1[0], xy2[0]], [xy1[1], xy2[1]])]
    
    plt.plot([xy3[0], xy4[0]], [xy3[1], xy4[1]], c='red')
    plt.text(0.3, 5, "断脱区", size = 10, alpha = 0.8)
    plt.text(0.6, 5, "定子脱胶区", size = 10, alpha = 0.8)
    
    # 扭矩正常区
    xy5 = [0, 60]
    xy6 = [1, 155]
    plt.plot([xy5[0], xy6[0]], [xy5[1], xy6[1]], c='red')
    plt.text(0.3, 50, "扭矩正常区", size = 10, alpha = 0.8)
    
    # 定子溶胀区+结蜡区
    _x7 = 0.38
    xy7 = [_x7, np.interp(_x7, [xy5[0], xy6[0]], [xy5[1], xy6[1]])]
    xy8 = [_x7, 200]
    plt.plot([xy7[0], xy8[0]], [xy7[1], xy8[1]], c='red')
    plt.text(0.1, 150, "定子溶胀区", size = 10, alpha = 0.8)
    plt.text(0.5, 150, "结蜡区", size = 10, alpha = 0.8)
    
    if save_img is not None:
        plt.savefig(save_img, bbox_inches='tight')
    plt.close()

