# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/8/29 10:10
# @Author : Hexk

import matplotlib.pyplot as plt
import numpy as np


def DrawingOneScatter(_x_axis, _y_axis, _title, _x_label, _y_label, _degree=1, _scatter_label=None, _linear_label=None):
    """
    绘制一个散点图和散点拟合的结果曲线
    :param _linear_label:  拟合曲线的标签名称
    :param _scatter_label: 散点图的标签名称
    :param _x_axis: 散点图和拟合曲线对应的x轴数据
    :param _y_axis: 散点图和拟合曲线对应的y轴数据
    :param _title: 标题
    :param _x_label: x轴名称
    :param _y_label: y轴名称
    :param _degree: 拟合曲线的次数
    :return: 拟合曲线的结果
    """
    # 绘制散点图
    plt.scatter(_x_axis, _y_axis, color='royalblue', label=_scatter_label)
    plt.title(_title)
    plt.xlabel(_x_label)
    plt.ylabel(_y_label)
    # 拟合直线或二次曲线
    _linear_model = np.polyfit(_x_axis, _y_axis, _degree)
    _linear_model_fn = np.poly1d(_linear_model)
    plt.plot(_x_axis, _linear_model_fn(_x_axis), color="darkorange", label=_linear_label)
    plt.show()
    return _linear_model_fn


def DrawingOneLine(_x_axis, _y_axis, _title, _x_label, _y_label, _line_label=None):
    """
    绘制一个数列的折线图，要求_x_axis和_y_axis长度一致
    :param _x_axis: 折线图x轴坐标
    :param _y_axis: 折线图y轴坐标
    :param _title: 折线图标题
    :param _x_label: 折线图x轴标题
    :param _y_label: 折线图y轴标题
    :param _line_label: 折线标题
    :return: None
    """
    plt.plot(_x_axis, _y_axis, 'o--', c='royalblue', linewidth=1, label=_line_label)
    plt.legend()
    plt.title(_title)
    plt.xlabel(_x_label)
    plt.ylabel(_y_label)
    plt.show()
    return None


def DrawingTwoLine(_x_axis, _y1_axis, _y2_axis, _title, _x_label, _y_label, _y1_label=None, _y2_label=None):
    """
    绘制一个双折线图，用于对比两组数据在同一个维度上的差异
    :param _x_axis: 折线图x轴数据
    :param _y1_axis: 折线图y轴数据 1组
    :param _y2_axis: 折线图y轴数据 2组
    :param _title: 图像标题
    :param _x_label: 折线图x轴标题
    :param _y_label: 折线图y轴标题
    :param _y1_label: 折线图y轴数据标题 1组
    :param _y2_label: 折线图y轴数据标题 2组
    :return: None
    """
    plt.plot(_x_axis, _y1_axis, 'o--', c='darkorange', linewidth=1, label=_y1_label)
    plt.plot(_x_axis, _y2_axis, '^--', c='royalblue', linewidth=1, label=_y2_label)
    plt.legend()
    plt.title(_title)
    plt.xlabel(_x_label)
    plt.ylabel(_y_label)
    plt.show()
    return None


def DrawingFourLine(_x_axis, _y1_axis, _y2_axis, _y3_axis, _y4_axis, _title, _x_label, _y_label, _y1_label=None,
                    _y2_label=None, _y3_label=None, _y4_label=None):
    """
    绘制4组数据，y1y2为一组，y3y4为一组，用于分析前后对比
    :param _x_axis: x轴数据
    :param _y1_axis: y1数据
    :param _y2_axis: y2 Data
    :param _y3_axis: y3 Data
    :param _y4_axis: y4 Data
    :param _title: 图像标题
    :param _x_label: x轴标题
    :param _y_label: y轴标题
    :param _y1_label: 数据1标题
    :param _y2_label: 数据2标题
    :param _y3_label: 数据3标题
    :param _y4_label: 数据4标题
    :return: None
    """
    plt.plot(_x_axis, _y1_axis, 'o--', c='darkorange', linewidth=1, label=_y1_label)
    plt.plot(_x_axis, _y2_axis, 'o-', c='darkorange', linewidth=1, label=_y2_label)
    plt.plot(_x_axis, _y3_axis, '^--', c='dodgerblue', linewidth=1, label=_y3_label)
    plt.plot(_x_axis, _y4_axis, '^-', c='dodgerblue', linewidth=1, label=_y4_label)
    plt.legend()
    plt.title(_title)
    plt.xlabel(_x_label)
    plt.ylabel(_y_label)
    plt.show()
    return None


if __name__ == '__main__':
    y_axis = np.random.rand(20)
    x_axis = np.random.rand(20)
    # linear = DrawingOneScatter(x_axis, y_axis, 'Random List', 'X', 'Y', 1)
    # DrawingOneLine(x_axis, y_axis, 'Random List', 'X', 'Y', 'Broken Line')
