# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/11 下午2:01
# @Author : Hexk
# @Descript : 计算ICESat-2 Point的标准差。我怀疑也是很大的。
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadPoint2DataFrame as RSDF
import ReadRasterAndShape.ReadRaster as RR
import RasterAnalysis.RasterClipByShape as RS
import time

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    merge_point_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\1_PreTest_ICESat-2PointData\11_MergePoint\SRTM_Bin_50\SRTM_Bin_50.shp"
    output_csv_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\3_PreTest_CSV\7_TestCSV'
    point_rsdf = RSDF.ReadPoint2DataFrame(merge_point_path)
    point_df = point_rsdf.ReadShapeFile()

    bin_length_list = []
    point_std = []
    for i in range(int(point_df['Bin_50'].min()), int(point_df['Bin_50'].max()) + 1):
        temp_df = point_df[point_df["Bin_50"] == float(i)]
        bin_length_list.append(temp_df.shape[0])
        bin_std = temp_df['Delta_Ele'].abs().std()
        point_std.append(bin_std)

    csv_dict = {
        f'point_count': bin_length_list,
        f'point_std': point_std,
    }
    csv_df = pd.DataFrame(csv_dict)
    df = pd.DataFrame()
    df = pd.concat([df, csv_df], axis=1)
    times = time.strftime('%Y_%m_%d_%H%M%S', time.localtime())
    output_path = os.path.join(output_csv_folder, f'ICESat2_Std_{times}.csv')
    df.to_csv(output_path)

