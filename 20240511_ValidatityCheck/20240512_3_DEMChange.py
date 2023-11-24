# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/12 下午4:27
# @Author : Hexk
# @Descript :
import re

import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadRaster as RR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'
if __name__ == '__main__':
    region_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\20240512_1_ModifyRegionShape\20240512_2_CutRegion.shp"
    srtm_dem_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\Clip_SRTMDEM\SRTM_DEM_Clip.tif"
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    # 属性表字段支持中文
    gdal.SetConfigOption("SHAPE_ENCODING", "UTF-8")
    # 注册驱动
    ogr.RegisterAll()
    # 新建dataset，打开shp文件
    ds = ogr.Open(region_path)
    # 获取dataset的图层个数
    ds.GetLayerCount()
    # 获取第一个图层
    layer = ds.GetLayerByIndex(0)
    # 重置要素读取序列
    layer.ResetReading()
    # 获取当前图层由多少个矢量要素
    feature_num = layer.GetFeatureCount(0)
    feature = layer.GetFeature(0)
    feature_geom = str(feature.GetGeometryRef())  # 这个就是wkt
    # 如何根据wkt的范围，锁定到栅格的范围上
    # 1. wkt范围转列表
    # 2. 列表点根据geotransform转换到行列数
    # 3. 生成栅格

    # 获取geotransform
    strm_rr = RR.ReadRaster(srtm_dem_path)
    srtm_data = strm_rr.ReadRasterFile()
    raster_geotransform = strm_rr.raster_ds_geotrans  # (295315.30116342165, 29.999489275454824, 0.0, 3721078.5063580037, 0.0, -30.001324679067373)

    # wkt转列表
    feature_geom_x_list, feature_geom_y_list = [], []
    hollow_x_dict = dict()
    hollow_row_dict = dict()
    hollow_y_dict = dict()
    hollow_column_dict =dict()
    # 截取外括号
    feature_geom = feature_geom[feature_geom.index('('):]
    # 截取内括号
    feature_geom = feature_geom[1:-1]
    # 正则表达式切分字符串
    pattern = r"\((.*?)\)"
    match = re.findall(pattern, feature_geom)
    # print(len(match))   # 6, 0是外环，剩下的是空心内环
    # 按,切分字符串
    feature_list = match[0].split(',')
    for i in range(len(feature_list)):
        feature_x, feature_y = feature_list[i].split(' ')
        feature_geom_x_list.append(feature_x)
        feature_geom_y_list.append(feature_y)
    for i in range(len(match) - 1):
        hollow_x_dict[i] = []
        hollow_y_dict[i] = []
        hollow_feature_list = match[i + 1].split(',')
        for j in range(len(hollow_feature_list)):
            hollow_x, hollow_y = hollow_feature_list[j].split(' ')
            hollow_x_dict[i].append(hollow_x)
            hollow_y_dict[i].append(hollow_y)

    # 根据geotransform转到行列上
    feature_row, feature_column = [], []
    raster_origin_x = raster_geotransform[0]
    raster_origin_y = raster_geotransform[3]
    pixel_x = raster_geotransform[1]
    pixel_y = raster_geotransform[5]
    for index, item in enumerate(feature_geom_x_list):
        column = int(np.ceil((float(item) - raster_origin_x) / pixel_x))
        row = int(np.ceil((float(feature_geom_y_list[index]) - raster_origin_y) / pixel_y))
        feature_column.append(column)
        feature_row.append(row)
    # 获取空洞边缘的行列数
    for i in range(len(match) - 1):
        hollow_row_dict[i] = []
        hollow_column_dict[i] = []
        for index, item in enumerate(hollow_x_dict[i]):
            column = int(np.ceil((float(item) - raster_origin_x) / pixel_x))
            row = int(np.ceil((float(hollow_y_dict[i][index]) - raster_origin_y) / pixel_y))
            hollow_row_dict[i].append(row)
            hollow_column_dict[i].append(column)
    # 之后如何？
    # 找到一行的最左最右列，按列确定栅格像元。
    # 找到空洞的最右最右列，按列确定像元。
