# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/15 上午10:43
# @Author : Hexk
# @Descript : 提取ICESat点和预测值之间值。
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import ReadRasterAndShape.ReadRaster as RR
import ReadRasterAndShape.ReadPoint2DataFrame as RPDF
import PathOperation.PathGetFiles as PGF
import os

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'
if __name__ == '__main__':
    point_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\20240515_4_ClipPoint\20240515_ClipPoint.shp"
    raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\20240515_2_ClipRaster'
    predict_reclassify_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\2_PreTest_PredictData\1_Inter\3_MaskData\Mask_SRTM_2019_Bin_50\Mask_SRTM_2019_Bin_50\Reclassify\Reclassify.tif"
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\20240515_5_ClipPointExcel'
    ctype_list = ['M5', 'M10', 'P5', 'P10', 'R5', 'R10', 'Predict']
    bins = 'B50'

    point_rpdf = RPDF.ReadPoint2DataFrame(point_path)
    point_df = point_rpdf.ReadShapeFile()

    raster_path_list, raster_name_list = PGF.PathGetFiles(raster_folder, '.tif')
    raster_list = []
    file_name_list = []
    for raster_name_index, raster_name_item in enumerate(raster_name_list):
        for ctype_index, ctype_item in enumerate(ctype_list):
            if f'Clip_Mask_{bins}_{ctype_item}' in raster_name_item:
                raster_list.append(raster_path_list[raster_name_index])
                file_name_list.append(f'V_{raster_name_item.split("_")[2]}_{raster_name_item.split("_")[3]}')
    for index, item in enumerate(raster_list):
        raster_rr = RR.ReadRaster(item)
        raster_data = raster_rr.ReadRasterFile()
        point_row, point_column = point_rpdf.PointMatchRasterRowColumn(raster_rr.raster_ds_geotrans)
        raster_value_list = RR.SearchRasterRowColumnData(point_row, point_column, raster_data)
        temp_df = pd.DataFrame(raster_value_list, columns=[f'{file_name_list[index]}'])
        point_df = pd.concat([point_df, temp_df], axis=1)
    output_dict = dict()
    for ctype_index, ctype_item in enumerate(ctype_list):
        if ctype_item != 'Predict':
            temp_dict = dict()
            bin_predict_mean_list = []
            bin_original_mean_list = []
            # bin_dict = dict()
            for i in range(int(min(point_df[f'B50_{ctype_item}'])), int(max(point_df[f'B50_{ctype_item}'])) + 1):
                temp_df = point_df[point_df[f'B50_{ctype_item}'] == float(i)]
                bin_predict_mean_list.append(temp_df[f'V_B50_{ctype_item}'].mean())
                bin_original_mean_list.append(temp_df[f'DH_{ctype_item}'].mean())
            temp_dict[f'B50_Predict_{ctype_item}_Mean'] = bin_predict_mean_list
            temp_dict[f'B50_DH_{ctype_item}_Mean'] = bin_original_mean_list
            output_dict = dict(output_dict, **temp_dict)
    output_df = pd.DataFrame(output_dict)
    output_path = os.path.join(output_folder, '20240515_5_ClipPointExcel.xlsx')
    output_df.to_excel(output_path)

