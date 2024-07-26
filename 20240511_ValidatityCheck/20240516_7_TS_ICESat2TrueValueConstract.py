# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/16 下午7:40
# @Author : Hexk
# @Descript : 统计全区域所有icesat2点的真值对比
import PathOperation.PathGetFiles as PGF
import PathOperation.PathFilesOperation as PFO
import XGBoostRegression.IntegrationXGBoostRegression as IXGBR
import ReadRasterAndShape.ReadPoint2DataFrame as RSDF
import ReadRasterAndShape.ReadRaster as RR
import numpy as np
import ErrorAnalysis.ErrorAnalysis as EA
import os
import pandas as pd

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'
if __name__ == '__main__':
    raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\Raster\TS1_UnClip'
    output_csv_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\20240515_5_ClipPointExcel'
    region_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\0_PreTest_BaseData\1_GlaciersRegion\1_GlaciersRegion.shp"
    reclassify_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\2_PreTest_PredictData\1_Inter\3_MaskData\Mask_SRTM_2019_Bin_50\Mask_SRTM_2019_Bin_50\Reclassify\Reclassify.tif"
    # icesat_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240516\7_TS_PointMerge\7_TS_PointMerge.shp"
    icesat_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\1_PreTest_ICESat-2PointData\11_MergePoint\SRTM_Bin_50\SRTM_Bin_50.shp'
    dem_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\4_BaseSRTMDEM'
    srtm_dem_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\Clip_SRTMDEM\SRTM_DEM_Clip.tif"

    raster_path_list, raster_name_list = PGF.PathGetFiles(raster_folder, '.tif')
    dem_path_list, dem_name_list = PGF.PathGetFiles(dem_folder, '.tif')

    point_rsdf = RSDF.ReadPoint2DataFrame(icesat_path)
    point_df = point_rsdf.ReadShapeFile()
    reclassify_rr = RR.ReadRaster(reclassify_path)
    reclassify_data = reclassify_rr.ReadRasterFile()
    output_df = pd.DataFrame()
    for raster_name_index, raster_name_item in enumerate(raster_name_list):
        file_name = raster_name_item.split('_')[-1]
        temp_rr = RR.ReadRaster(raster_path_list[raster_name_index])
        temp_data = temp_rr.ReadRasterFile()
        point_row, point_column = point_rsdf.PointMatchRasterRowColumn(temp_rr.raster_ds_geotrans)
        value_list = RR.SearchRasterRowColumnData(point_row, point_column, temp_data)
        point_df[f'TS1_{file_name}'] = value_list
        bin_list = []
        for i in range(int(min(point_df['Bin_50'])), int(max(point_df['Bin_50'])) + 1):
            bin_mean = point_df[point_df['Bin_50'] == i][f'TS1_{file_name}'].mean()
            bin_list.append(bin_mean)
        output_df[f'TS1_{file_name}'] = bin_list

    for dem_name_index, dem_name_item in enumerate(dem_name_list):
        file_name = dem_name_item.split('_')[-1]
        temp_rr = RR.ReadRaster(dem_path_list[dem_name_index])
        temp_data = temp_rr.ReadRasterFile()
        point_row, point_column = point_rsdf.PointMatchRasterRowColumn(temp_rr.raster_ds_geotrans)
        value_list = RR.SearchRasterRowColumnData(point_row, point_column, temp_data)
        point_df[f'DEM_{file_name}'] = value_list
    point_df['DEM_M5'] = point_df['H_Li'] - point_df['DEM_Minus5']
    point_df['DEM_M10'] = point_df['H_Li'] - point_df['DEM_Minus10']
    point_df['DEM_P5'] = point_df['H_Li'] - point_df['DEM_Plus5']
    point_df['DEM_P10'] = point_df['H_Li'] - point_df['DEM_Plus10']
    point_df['DEM_R5'] = point_df['H_Li'] - point_df['DEM_Random5']
    point_df['DEM_R10'] = point_df['H_Li'] - point_df['DEM_Random10']
    ctype_list = ['M5', 'M10', 'P5', 'P10', 'R5', 'R10']
    for index, item in enumerate(ctype_list):
        ctype_bin_list = []
        for i in range(int(min(point_df['Bin_50'])), int(max(point_df['Bin_50'])) + 1):
            bin_mean = point_df[point_df['Bin_50'] == i][f'DEM_{item}'].mean()
            ctype_bin_list.append(bin_mean)
        output_df[f'DH_{item}'] = ctype_bin_list
    true_list = []
    for i in range(int(min(point_df['Bin_50'])), int(max(point_df['Bin_50'])) + 1):
        bin_mean = point_df[point_df['Bin_50'] == i][f'Delta_Ele'].mean()
        true_list.append(bin_mean)
    output_df[f'DH_True'] = true_list
    # dem_rr = RR.ReadRaster(srtm_dem_path)
    # dem_data = dem_rr.ReadRasterFile()
    # point_row, point_column = point_rsdf.PointMatchRasterRowColumn(dem_rr.raster_ds_geotrans)
    # value_list = RR.SearchRasterRowColumnData(point_row, point_column, dem_data)
    # point_df['SRTM_DEM']

    output_df.to_excel(os.path.join(output_csv_folder, '20240518_TS1_AllRegionICESat2TrueConstract.xlsx'))

    # ture_list = []
    # m5_list = []
    # m10_list = []
    # p5_list = []
    # p10_list = []
    # r10_list = []
    # r5_list = []
    # for i in range(int(min(point_df['Bin_50'])), int(max(point_df['Bin_50'])) + 1):
    #     ture_list.append(point_df[point_df['Bin_50'] == i][f'Delta_Ele'].mean())
    #     m5_list.append(point_df[point_df['Bin_50'] == i][f'M5'].mean())
    #     m10_list.append(point_df[point_df['Bin_50'] == i][f'M10'].mean())
    #     p5_list.append(point_df[point_df['Bin_50'] == i][f'P5'].mean())
    #     p10_list.append(point_df[point_df['Bin_50'] == i][f'P10'].mean())
    #     r5_list.append(point_df[point_df['Bin_50'] == i][f'R5'].mean())
    #     r10_list.append(point_df[point_df['Bin_50'] == i][f'R10'].mean())
    # output_df[f'TS1_T'] = ture_list
    # output_df[f'TS1_M5_T'] = ture_list
    # output_df[f'TS1_M10_T'] = ture_list
    # output_df[f'TS1_R5_T'] = ture_list
    # output_df[f'TS1_R10_T'] = ture_list
    # output_df[f'TS1_P5_T'] = ture_list
    # output_df[f'TS1_P10_T'] = ture_list
