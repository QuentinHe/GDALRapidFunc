# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/9/18 10:17
# @Author : Hexk
# @Descript : 根据shp的df进行多元非线性回归，使用sklearn进行数据集切分，同时可以拿着tif文件进行预测。
import matplotlib
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
from sklearn import datasets
import seaborn as sns
import matplotlib.pyplot as plt
import ReadRasterAndShape.ReadPoint2DataFrame as RSDF
from sklearn import model_selection
from sklearn.linear_model import LinearRegression
import os

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def MultivariateLinearRegression(_input_path, _variant_field, _result_field, _train_size, _level_field=None):
    """
    根据输入DF，输入的变量，输入结果字段，训练集大小，和是否按照等级分类训练进行多元线性拟合回归
    :param _input_path: 输入文件路径
    :param _variant_field: 输入DF的训练字段
    :param _result_field: 输入DF的结果字段
    :param _train_size: 设定训练集的大小
    :param _level_field: 是否按照等级分等级训练。
    :return: a_list 拟合截距 b_list 回归系数
    """

    def LinearRegressionProcess(_df):
        """
        集合了整个分类训练和模拟过程
        :param _df: 输入DF
        :return: 单次训练的截距和回归系数
        """
        x_list = _df[_variant_field]
        y_list = _df[_result_field]
        x_train, x_test, y_train, y_test = model_selection.train_test_split(x_list, y_list, train_size=_train_size)
        # 多元线性拟合
        model = LinearRegression()
        model.fit(x_train, y_train)
        _a = model.intercept_
        _b = model.coef_
        print(f'拟合截距:{_a}, 回归系数:{_b}')
        score = model.score(x_test, y_test)
        print(score)
        y_pred = model.predict(x_test)
        plt.plot(range(len(y_pred)), y_pred, label="predict", color='darkorange')
        plt.plot(range(len(y_test)), y_test, label='verification', color='royalblue')
        plt.legend()
        plt.xlabel('The Numbers of Test Sample')
        plt.ylabel('Delta Elevation')
        plt.show()
        return _a, _b

    input_rsdf = RSDF.ReadPoint2DataFrame(_input_path)
    input_df = input_rsdf.ReadShapeFile()
    input_df = RSDF.DataFrameFormatConvert(input_df, int_field=['Segment_ID', 'Bin_50', 'Bin_100', 'Bin_150', 'Bin_200',
                                                                'Aspect'],
                                           float_field=['Latitudes', 'Longitudes', 'H_Li', 'DEM_H', 'Delta_H', 'Proj_X',
                                                        'Proj_Y',
                                                        'Slope', 'Undulation', 'Elevation', 'Delta_Ele'])
    _a_list = []
    _b_list = []
    # 若_level_field不为None，说明是按等级进行分段拟合
    if _level_field is not None:
        max_bin_level = max(input_df[_level_field])
        min_bin_level = min(input_df[_level_field])
        for level in range(min_bin_level, max_bin_level + 1):
            level_df = input_df.loc[input_df[_level_field] == level]
            a, b = LinearRegressionProcess(level_df)
            _a_list.append(a)
            _b_list.append(b)
    # 若是None则是整体拟合
    else:
        a, b = LinearRegressionProcess(input_df)
        _a_list.append(a)
        _b_list.append(b)

    return _a_list, _b_list


if __name__ == '__main__':
    input_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20230916\1_FilterOutliers\1_FilterOutliers\NASA_2019_Bin_50\NASA_2019_Bin_50.shp'
    a_list, b_list = MultivariateLinearRegression(input_path, ['Undulation', 'Aspect', 'Slope'], 'Delta_Ele', 0.7,
                                                  _level_field='Bin_50')
    # 尝试利用这个结果得到一副NASA_DEM 2019 BIN 50的高程差影像，并进行分析。



