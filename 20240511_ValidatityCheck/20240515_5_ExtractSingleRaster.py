# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/15 下午2:38
# @Author : Hexk
# @Descript : 提取Predict的值

import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import PathOperation.PathGetFiles as PGF
import ReadRasterAndShape.ReadRaster as RR
import ReadRasterAndShape.ReadPoint2DataFrame as RSDF

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    predect_raster_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\20240515_2_ClipRaster\Clip_Mask_B50_Predict.tif"
    point_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\20240515_4_ClipPoint\20240515_SRTM_Point.shp"
    reclassify_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\20240515_2_ClipRaster\Clip_Reclassify_B50_Predict.tif"

    point_rpdf = RSDF.ReadPoint2DataFrame(point_path)
    point_df = point_rpdf.ReadShapeFile()

    raster_rr = RR.ReadRaster(predect_raster_path)
    raster_data = raster_rr.ReadRasterFile()
    point_row, point_column = point_rpdf.PointMatchRasterRowColumn(raster_rr.raster_ds_geotrans)
    raster_value_list = RR.SearchRasterRowColumnData(point_row, point_column, raster_data)
    temp_df = pd.DataFrame(raster_value_list, columns=[f'Predict'])
    point_df = pd.concat([point_df, temp_df], axis=1)

    temp_dict = dict()
    bin_predict_mean_list = []
    bin_original_mean_list = []
    # bin_dict = dict()
    for i in range(int(min(point_df[f'Bin_50'])), int(max(point_df[f'Bin_50'])) + 1):
        temp_df = point_df[point_df[f'Bin_50'] == float(i)]
        bin_predict_mean_list.append(temp_df[f'Predict'].mean())
        bin_original_mean_list.append(temp_df[f'Delta_Ele'].mean())
    temp_dict[f'Predict_Mean'] = bin_predict_mean_list
    temp_dict[f'Delta_Ele_Mean'] = bin_original_mean_list
    df = pd.DataFrame(temp_dict)
    print(df)
