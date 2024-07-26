# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/16 上午10:21
# @Author : Hexk
# @Descript : 补充实验2，调整Point点中的H_Li实测结果。依然设置成6种。
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadPoint2DataFrame as RPDF
import ReadRasterAndShape.ReadRaster as RR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    original_point_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240516\4_TS_ClipRegionPoint\4_TS_ClipRegionPoint.shp"
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240516\5_TS_ClipRegionPoint_Modify'
    original_point_rpdf = RPDF.ReadPoint2DataFrame(original_point_path)
    original_point_df = original_point_rpdf.ReadShapeFile()
    original_point_df['M5'] = original_point_df['Delta_Ele'] - 5
    original_point_df['M10'] = original_point_df['Delta_Ele'] - 10
    original_point_df['P5'] = original_point_df['Delta_Ele'] + 5
    original_point_df['P10'] = original_point_df['Delta_Ele'] + 10
    random5_list = [np.random.uniform(-5, 5) for i in range(original_point_df.shape[0])]
    original_point_df['R5'] = original_point_df['Delta_Ele'] + random5_list
    random10_list = [np.random.uniform(-10, 10) for i in range(original_point_df.shape[0])]
    original_point_df['R10'] = original_point_df['Delta_Ele'] + random10_list
    RPDF.DataFrameWriteShape(original_point_df, output_folder, '5_TS_ClipRegionPoint_Modify')
