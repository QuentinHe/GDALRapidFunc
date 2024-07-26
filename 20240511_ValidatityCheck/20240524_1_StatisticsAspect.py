# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/24 上午10:17
# @Author : Hexk
# @Descript :
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadPoint2DataFrame as RPDF
import ReadRasterAndShape.ReadRaster as RR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'
if __name__ == '__main__':
    point_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\1_PreTest_ICESat-2PointData\11_MergePoint\SRTM_Bin_50\SRTM_Bin_50.shp'
    aspect_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240516\20_Aspect\20240524_AspectLevel.tif"
    point_rpdf = RPDF.ReadPoint2DataFrame(point_path)
    point_df = point_rpdf.ReadShapeFile()
    aspect_rr = RR.ReadRaster(aspect_path)
    aspect_data = aspect_rr.ReadRasterFile()
    point_row, point_column = point_rpdf.PointMatchRasterRowColumn(aspect_rr.raster_ds_geotrans)
    aspect_list = RR.SearchRasterRowColumnData(point_row, point_column, aspect_data)
    point_df['Aspect_L'] = aspect_list
    for i in range(9):
        # print(len(point_df[point_df['Aspect'] == float(i)]))
        print(len(point_df[point_df['Aspect_L'] == float(i)]))
