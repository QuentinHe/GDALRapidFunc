# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/18 下午1:50
# @Author : Hexk
# @Descript : 统计clip中点的结果。先按像元找点的结果。然后
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
    raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\Raster\TS2_UnClip'
    point_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240516\19_PointFormal\20240518_ClipPoint\20240518_ClipPoint.shp"
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\20240515_5_ClipPointExcel'
    clip_dem_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\Raster\Clip_Mask_SRTM_DEM.tif"

    point_rsdf = RSDF.ReadPoint2DataFrame(point_path)
    point_df = point_rsdf.ReadShapeFile()

    output_df = pd.DataFrame()
    # 先读栅格的值
    # 所有栅格值都写入了
    # 这一部分是Clip区域计算结果
    # 然后读取Predict的结果，这一点与TS1的应该是一样的，那不读取了
    raster_path_list, raster_name_list = PGF.PathGetFiles(raster_folder, '.tif')
    for raster_name_index, raster_name_item in enumerate(raster_name_list):
        file_name = raster_name_item.split('_')[-1]
        raster_rr = RR.ReadRaster(raster_path_list[raster_name_index])
        raster_data = raster_rr.ReadRasterFile()
        point_row, point_column = point_rsdf.PointMatchRasterRowColumn(raster_rr.raster_ds_geotrans)
        # 读点位置
        raster_value_list = RR.SearchRasterRowColumnData(point_row, point_column, raster_data)
        point_df[f'TS2_{file_name}'] = raster_value_list
        # 分箱统计
        bin_mean_list = []
        for i in range(1, 17):
            bin_mean_list.append(np.mean(point_df[point_df['Bin_50'] == float(i)][f'TS2_{file_name}']))
        output_df[f'TS2_{file_name}'] = bin_mean_list
    # 然后读取ICESat2对应的真值
    # 应该是M5 M10的分箱均值
    ctype_list = ['M5', 'M10', 'P5', 'P10', 'R5', 'R10']
    for ctype_index, ctype_item in enumerate(ctype_list):
        dh_list = []
        for i in range(1, 17):
            dh_list.append(np.mean(point_df[point_df['Bin_50'] == float(i)][f'{ctype_item}']))
        output_df[f'DH_{ctype_item}'] = dh_list
    # 输出，ICESat2未变的真值也不用处理之前做过了
    output_path = os.path.join(output_folder, '20240518_TS2_ClipRegionICESat2TrueConstract.xlsx')
    output_df.to_excel(output_path)

