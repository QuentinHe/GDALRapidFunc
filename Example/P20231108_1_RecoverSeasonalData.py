# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/8 15:47
# @Author : Hexk
# @Descript : 重新恢复季节性数据，选择了部分冰川

import time
import numpy as np
import pandas as pd
import pylab as pl
from matplotlib import pyplot as plt
from osgeo import gdal, ogr, osr
import os

from scipy.optimize import leastsq

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def SeasonalParametersFitting(_seasonal_y):
    print(''.center(30, '*'))
    print('正在拟合'.center(30, ' '))

    def SeasonalFunc(month, parameters):
        """
        对整幅影像进行该季节性变化处理？
        如何处理？
        处理不了。
        可以。
        局部增益。
        每一层拟合一个函数
        :param month: 月份 1~12
        :param parameters: 6个参数，该参数是通过最小二乘得到
        :return:
        """
        month_normalization = month / 12
        a, b, c, d, f1, f2 = parameters
        return a + b * month_normalization + c * np.cos(2 * np.pi / 1 * month_normalization + f1) + d * np.cos(
            2 * np.pi / 0.5 * month_normalization + f2)

    # 残差函数
    def ResidualsFunc(p, y, t):
        return y - SeasonalFunc(t, p)

    # 月份值
    _t = np.arange(1 / 12, 13 / 12, 1 / 12)
    # 初始化定义参数
    _origin_parameters = np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5])
    # 拟合后的参数结果
    plsq = leastsq(ResidualsFunc, _origin_parameters, args=(_seasonal_y, _t))
    print(f'拟合Parameters结果：{plsq[0]}')
    # 拟合后的y值
    fitting_y_list = []
    for i in _t:
        fitting_y_list.append(SeasonalFunc(i, plsq[0]))
    print(fitting_y_list)
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    # plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    # pl.plot(_t, _seasonal_y, marker='+', label=u"3 months average of Original Observations")
    # # pl.plot(month, fitting_y_list, marker='^', label=u"Origin Observations")
    # pl.plot(_t, SeasonalFunc(_t, plsq[0]), label=u"Recovered observations")
    # pl.legend()
    # pl.show()

    return plsq[0], fitting_y_list


if __name__ == '__main__':
    origin_excel_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231108_7_Analysis_Excel\20231108_21_MonthSum.xlsx"
    output_excel_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231108_7_Analysis_Excel'
    times = time.strftime('%Y_%m_%d_%H%M%S', time.localtime())
    origin_excel_df = pd.read_excel(origin_excel_path)
    # 选择所有包含Mean的列
    select_columns = [i for i in origin_excel_df.columns if 'Mean' in i]
    select_df = origin_excel_df[select_columns]
    select_metadata_df = origin_excel_df[['ID', 'Glaciers_Name', 'PixelNums']]
    # 拿出不符合顺序的列
    month10 = select_df.pop('Month10_Mean')
    month11 = select_df.pop('Month11_Mean')
    month12 = select_df.pop('Month12_Mean')
    # 重新拼接
    select_df = pd.concat([select_df, month10, month11, month12], axis=1)
    # 生成存储拟合参数和拟合后结果的字典
    fitting_parameters_dict = dict(
        a=[],
        b=[],
        c=[],
        d=[],
        f1=[],
        f2=[]
    )
    fitting_data_dict = dict()
    for index, item in enumerate(select_df.columns):
        fitting_data_dict[index + 1] = []
    # 逐行读取df，拟合结果
    for row in select_df.itertuples():
        origin_y_list = []
        for index, item in enumerate(row):
            if index:
                origin_y_list.append(item)
            else:
                continue
        parameters_list, fitting_y_list = SeasonalParametersFitting(origin_y_list)
        for index, item in enumerate(fitting_parameters_dict):
            fitting_parameters_dict[item].append(parameters_list[index])
        for index, item in enumerate(fitting_data_dict):
            fitting_data_dict[item].append(fitting_y_list[index])
    parameters_df = pd.DataFrame(fitting_parameters_dict)
    fitting_y_df = pd.DataFrame(fitting_data_dict)
    fitting_result_df = pd.concat([select_metadata_df, fitting_y_df], axis=1)
    output_parameters_excel_path = os.path.join(output_excel_folder, f'20231108_21_RecoverSeasonalChange_Parameters_{times}.xlsx')
    output_fitting_excel_path = os.path.join(output_excel_folder, f'20231108_21_RecoverSeasonalChange_FittingData_{times}.xlsx')
    parameters_df.to_excel(output_parameters_excel_path)
    fitting_result_df.to_excel(output_fitting_excel_path)

