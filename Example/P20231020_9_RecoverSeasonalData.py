# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/20 10:51
# @Author : Hexk
# @Descript :
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def SeasonalFunc(month, parameters):
    """
    对整幅影像进行该季节性变化处理？
    如何处理？
    处理不了。
    可以。
    局部增益。
    每一层拟合一个函数
    :param month:
    :param parameters:
    :return:
    """
    month_normalization = month / 12
    a, b, c, d, f1, f2 = parameters
    return a + b * month_normalization + c * np.cos(2 * np.pi / 1 * month_normalization + f1) + d * np.cos(
        2 * np.pi / 0.5 * month_normalization + f2)


def RecoverFunc(x, a, b):
    return a * x + b


if __name__ == '__main__':
    # 只算SRTM部分
    # 需要先对原始结果值进行季节性函数运算一遍
    # 再三个月求一次平均
    # 再对平均结果进行增益函数得到最后的结果
    # 用最后结果来表示个体的季节性变化

    pass
