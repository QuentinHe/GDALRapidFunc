# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/12 下午2:26
# @Author : Hexk
# @Descript : 根据icesat point提取SRTM DEM， 用Hli-SRTMDEM， 提取predict dem。绘制散点图在下一个python文件中。
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import ReadRasterAndShape.ReadRaster as RR
import ReadRasterAndShape.ReadPoint2DataFrame as RPDF
import os

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    icesat_2019_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\20240511_1_ProfilePoint\20240512_1-R_ProfilePoint.shp"
    icesat_2020_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\20240511_1_ProfilePoint\20240512_2_2020_ProfilePoints.shp"
    icesat_2022_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\20240511_1_ProfilePoint\20240512_2_2022_ProfilePoints.shp"
    predict_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\2_PredictData\1_Inter\4_MeanData\SRTM_2019\SRTM_2019.tif"
    srtm_dem_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\Clip_SRTMDEM\SRTM_DEM_Clip.tif'
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\20240511_3_ContractOrbitPointShape'


    i2019_rpdf = RPDF.ReadPoint2DataFrame(icesat_2019_path)
    i2020_rpdf = RPDF.ReadPoint2DataFrame(icesat_2020_path)
    i2022_rpdf = RPDF.ReadPoint2DataFrame(icesat_2022_path)
    i2019_df = i2019_rpdf.ReadShapeFile()
    i2020_df = i2020_rpdf.ReadShapeFile()
    i2022_df = i2022_rpdf.ReadShapeFile()

    predict_rr = RR.ReadRaster(predict_path)
    srtm_rr = RR.ReadRaster(srtm_dem_path)
    predict_data = predict_rr.ReadRasterFile()
    srtm_data = srtm_rr.ReadRasterFile()

    i2019_point_row, i2019_point_column = i2019_rpdf.PointMatchRasterRowColumn(srtm_rr.raster_ds_geotrans)
    i2020_point_row, i2020_point_column = i2020_rpdf.PointMatchRasterRowColumn(srtm_rr.raster_ds_geotrans)
    i2022_point_row, i2022_point_column = i2022_rpdf.PointMatchRasterRowColumn(srtm_rr.raster_ds_geotrans)

    # 读2019的像元值
    i2019_srtm_list = RR.SearchRasterRowColumnData(i2019_point_row, i2019_point_column, srtm_data)
    i2019_predict_list = RR.SearchRasterRowColumnData(i2019_point_row, i2019_point_column, predict_data)
    # 读2020
    i2020_srtm_list = RR.SearchRasterRowColumnData(i2020_point_row, i2020_point_column, srtm_data)
    i2020_predict_list = RR.SearchRasterRowColumnData(i2020_point_row, i2020_point_column, predict_data)
    # 2022
    i2022_srtm_list = RR.SearchRasterRowColumnData(i2022_point_row, i2022_point_column, srtm_data)
    i2022_predict_list = RR.SearchRasterRowColumnData(i2022_point_row, i2022_point_column, predict_data)

    # 写入DF
    i2019_temp_dict = {
        'Row': i2019_point_row,
        'Column': i2019_point_column,
        'SRTM_DEM': i2019_srtm_list,
        'Predict': i2019_predict_list
    }
    i2019_temp_df = pd.DataFrame(i2019_temp_dict)

    i2020_temp_dict = {
        'Row': i2020_point_row,
        'Column': i2020_point_column,
        'SRTM_DEM': i2020_srtm_list,
        'Predict': i2020_predict_list
    }
    i2020_temp_df = pd.DataFrame(i2020_temp_dict)

    i2022_temp_dict = {
        'Row': i2022_point_row,
        'Column': i2022_point_column,
        'SRTM_DEM': i2022_srtm_list,
        'Predict': i2022_predict_list
    }
    i2022_temp_df = pd.DataFrame(i2022_temp_dict)
    # 拼接df
    i2019_df = pd.concat([i2019_df, i2019_temp_df], axis=1)
    i2019_df['H_SRTM'] = i2019_df['H_Li'] - i2019_df['SRTM_DEM']
    i2020_df = pd.concat([i2020_df, i2020_temp_df], axis=1)
    i2020_df['H_SRTM'] = i2020_df['H_Li'] - i2020_df['SRTM_DEM']
    i2022_df = pd.concat([i2022_df, i2022_temp_df], axis=1)
    i2022_df['H_SRTM'] = i2022_df['H_Li'] - i2022_df['SRTM_DEM']


    # 写出
    RPDF.DataFrameWriteShape(i2019_df, output_folder, '20240512_1_2019Point')
    RPDF.DataFrameWriteShape(i2020_df, output_folder, '20240512_2_2020Point')
    RPDF.DataFrameWriteShape(i2022_df, output_folder, '20240512_3_2022Point')
