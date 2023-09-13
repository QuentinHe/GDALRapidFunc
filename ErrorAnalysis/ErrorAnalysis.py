# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/9/12 16:25
# @Author : Hexk
# @Descript : 常用的误差计算分析
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def mae(_validate, _predict):
    _result = mean_absolute_error(_validate, _predict)
    print(f'MAE:{_result}')
    return _result


def mse(_validate, _predict):
    _result = mean_squared_error(_validate, _predict)
    print(f'MSE:{_result}')
    return _result


def rmse(_validate, _predict):
    _result = np.sqrt(mean_squared_error(_validate, _predict))
    print(f'RMSE:{_result}')
    return _result
