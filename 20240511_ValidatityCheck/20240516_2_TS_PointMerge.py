# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/16 上午10:45
# @Author : Hexk
# @Descript : 合并两个区域的Point数据，区域外的那几个列填Delta_Ele
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadPoint2DataFrame as RPDF
import ReadRasterAndShape.ReadRaster as RR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'
if __name__ == '__main__':
    # other_point_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240516\6_TS_OtherRegionPoint\6_TS_OtherRegionPoint.shp"
    other_point_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240516\1_TS2_Point\1_TS2_Point.shp"
    region_point_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240516\5_TS_ClipRegionPoint_Modify\5_TS_ClipRegionPoint_Modify.shp"
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240516\7_TS_PointMerge'
    other_point_rpdf = RPDF.ReadPoint2DataFrame(other_point_path)
    region_point_rpdf = RPDF.ReadPoint2DataFrame(region_point_path)

    other_df = other_point_rpdf.ReadShapeFile()
    region_df = region_point_rpdf.ReadShapeFile()

    other_df['M5'] = other_df['Delta_Ele']
    other_df['M10'] = other_df['Delta_Ele']
    other_df['P5'] = other_df['Delta_Ele']
    other_df['P10'] = other_df['Delta_Ele']
    other_df['R5'] = other_df['Delta_Ele']
    other_df['R10'] = other_df['Delta_Ele']

    print(other_df.shape[0])
    print(region_df.shape[0])
    other_df = pd.concat([other_df, region_df]).drop_duplicates(['Segment_ID', 'Latitudes', 'Longitudes'],
                                                                keep='last').sort_values(
        'Segment_ID')
    print(other_df.shape[0])

    RPDF.DataFrameWriteShape(other_df, output_folder, '7_TS_PointMerge')
