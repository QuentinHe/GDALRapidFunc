# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/13 9:24
# @Author : Hexk
# @Descript :
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadPoint2DataFrame as RSDF

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def ShapeFieldMean(_shape_path, _field, _classify_field=None):
    """
    统计字段的平均值， 如果包含分类字段，则先分类后再统计均值
    :param _shape_path: shape point 矢量文件路径
    :param _field: 计算字段
    :param _classify_field: 分类字段，默认为None
    :return: field_total_mean, level_mean； 数和list
    """
    shape_rsdf = RSDF.ReadPoint2DataFrame(_shape_path)
    shape_df = shape_rsdf.ReadShapeFile()
    # 字段的总体平均值
    _field_total_mean = np.mean(shape_df[_field])
    if _classify_field is None:
        return _field_total_mean
    elif _classify_field is not None:
        # 进行分类统计
        level_dict = dict()
        for i in range(int(np.min(shape_df[_classify_field])), int(np.max(shape_df[_classify_field])) + 1):
            level_dict[i] = []
        for index, item in enumerate(shape_df[_classify_field]):
            level_dict[int(item)].append(shape_df[_field][index])
        _level_mean = [np.mean(level_dict[i]) for i in level_dict]
        return _field_total_mean, _level_mean


if __name__ == '__main__':
    shape_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231009\0_BasePoint\NASA_2019_Bin_50\NASA_2019_Bin_50_month1\NASA_2019_Bin_50_month1.shp"
    tm, lm = ShapeFieldMean(shape_path, 'Delta_Ele', _classify_field='Bin_50')
    print(tm, lm)
