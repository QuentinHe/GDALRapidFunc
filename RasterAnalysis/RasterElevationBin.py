# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/9/9 11:05
# @Author : Hexk
# @Descript : 首先分析Point点在DEM上的高程分布范围，并统计高程间隔为50 100 150 200时的每个高程箱中有多少个点
# 1. 读取Point DF
# 2. 获取点对应位置的行列号
# 3. 获取DEM的值
# 4. 统计DEM范围
# 5. 切分范围统计点数目
# ---
# 统计完毕 大概5400~6100进行划分，5400以下和6100以上
# ---
# 对DEM进行重分类
# 间隔50 100 150 200

import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadPoint2DataFrame as RSDF
import ReadRasterAndShape.ReadRaster as RR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    input_shape_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\ICESat2\7_Remove_Slope_Data\NASA_2019\NASA_2019.shp'
    input_raster_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\0_BaseDEM\NASA_DEM\NASA_DEM.tif'
    # 读取shp文件，并以df格式返回
    shape_rsdf = RSDF.ReadPoint2DataFrame(input_shape_path)
    shape_df = shape_rsdf.ReadShapeFile()
    # 读取栅格文件
    raster_rr = RR.ReadRaster(input_raster_path)
    raster_data = raster_rr.ReadRasterFile()
    # 获取point在raster上的列行数
    point_row, point_column = shape_rsdf.PointMatchRasterRowColumn(raster_rr.raster_ds_geotrans)
    # 获取点在raster上的值
    raster_point_value = RR.SearchRasterRowColumnData(raster_data, point_row, point_column)
    # 如何统计？
    bins = np.arange(5000, 6600, 50)
    elevation = pd.cut(raster_point_value, bins)
    print(pd.value_counts(elevation, sort=False))
    # 分割线大概在5400~6100
