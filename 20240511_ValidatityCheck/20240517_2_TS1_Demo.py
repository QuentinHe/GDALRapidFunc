# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/17 下午8:40
# @Author : Hexk
# @Descript : 统计clip区域icesat2点的数目比例
import PathOperation.PathGetFiles as PGF
import PathOperation.PathFilesOperation as PFO
import XGBoostRegression.IntegrationXGBoostRegression as IXGBR
import ReadRasterAndShape.ReadPoint2DataFrame as RSDF
import ReadRasterAndShape.ReadRaster as RR
import numpy as np
import ErrorAnalysis.ErrorAnalysis as EA
import os
import pandas as pd
import matplotlib.pyplot as plt

from RasterAnalysis.RasterClipByShape import RasterClipByShape

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'
if __name__ == '__main__':
    point_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\20240515_4_ClipPoint\20240515_SRTM_Point.shp'
    point_rsdf = RSDF.ReadPoint2DataFrame(point_path)
    point_df = point_rsdf.ReadShapeFile()
    for i in range(1, 17):
        print(len(point_df[point_df['Bin_50'] == float(i)])/point_df.shape[0])
