# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/17 14:07
# @Author : Hexk
# @Descript : 该部分需要实现两个板块的内容，一是拟合季节变化曲线，二是恢复实际月份的真实值。
import numpy as np
import os
import matplotlib.pyplot as plt
import pylab as pl

from scipy.optimize import leastsq

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def func1(t, p):
    a, b, c, d, f1, f2 = p
    return a + b * t + c * np.cos(2 * np.pi / 1 * t + f1) + d * np.cos(2 * np.pi / 0.5 * t + f2)


def func2(x, p):
    A, b = p
    return x * A + b


def residuals2(p, y, x):
    return y - func2(x, p)


def residuals1(p, y, t):
    return y - func1(t, p)


def fitting_fuc(t, a, b, c, d, f1, f2):
    # return -5.11105049 + 1.36478155 * month + -0.41108949 * np.cos(2 * np.pi / 1 * month + -0.07192904) + -0.52877265 * np.cos(
    #     2 * np.pi / 0.5 * month + 1.02537251)
    return a + b * t + c * np.cos(2 * np.pi / 1 * t + f1) + d * np.cos(
        2 * np.pi / 0.5 * t + f2)


if __name__ == '__main__':
    # # 此时已经获得了Xi，通过Xi迭代得到xi
    # y = [-5.030599, -4.890615, -4.37426, -4.330191, -5.0253897, -4.772563, -3.1004138, -3.2170641, -4.3840275,
    #      -4.4213157, -4.22892, -4.686167]
    # Original observations
    y = [-5.489159, -4.7322955, -4.215822, -4.955174, -5.1895475, -4.800235, -2.8687067, -3.3249526, -4.525074,
         -4.374856, -4.230046, -4.6678014]
    # 3 month average of Original obersvation
    # y = [-4.9630853, -4.8124255, -4.6344305, -4.786847833, -4.981652167, -4.286163067, -3.664631433, -3.5729111,
    #      -4.074960867, -4.376658667, -4.424234467, -4.7956688]
    fitting_y_list = []
    t = np.arange(1 / 12, 13 / 12, 1 / 12)

    t_int = np.arange(1, 13)
    p0 = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    # p0 = [1, 0.5]
    plsq = leastsq(residuals1, p0, args=(y, t))
    print(f'拟合结果：{plsq[0]}')
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    pl.plot(t, y, marker='+', label=u"3 months average of Original Observations")
    # pl.plot(month, fitting_y_list, marker='^', label=u"Origin Observations")
    pl.plot(t, func1(t, plsq[0]), label=u"Recovered observations")
    pl.legend()
    pl.show()
    for i in t:
        fitting_y_list.append(fitting_fuc(i, plsq[0][0], plsq[0][1], plsq[0][2], plsq[0][3], plsq[0][4], plsq[0][5]))
    print(fitting_y_list)
