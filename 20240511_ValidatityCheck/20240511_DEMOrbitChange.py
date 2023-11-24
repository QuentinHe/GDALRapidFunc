# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/11 下午2:20
# @Author : Hexk
# @Descript : 根据ICESat2点的 SegmentID顺序排列SRTM DEM的值和预测栅格的值，形成三列列表。
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadRaster as RR
import ReadRasterAndShape.ReadPoint2DataFrame as RPDF
import time

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    # point_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\20240511_1_ProfilePoint\20240511_1_ProfilePoint.shp"
    # point_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\20240511_1_ProfilePoint\20240512_1-L_ProfilePoint.shp"
    point_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\20240511_1_ProfilePoint\20240512_1-R_ProfilePoint.shp"
    srtm_dem_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\Clip_SRTMDEM\SRTM_DEM_Clip.tif"
    predict_dem_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\2_PreTest_PredictData\1_Inter\4_MeanData\SRTM_2019.tif"
    output_csv_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\20240511_2_ProfilePointCSV'

    srtm_rr = RR.ReadRaster(srtm_dem_path)
    predict_rr = RR.ReadRaster(predict_dem_path)
    srtm_data = srtm_rr.ReadRasterFile()
    predict_data = predict_rr.ReadRasterFile()

    point_rpdf = RPDF.ReadPoint2DataFrame(point_path)
    point_df = point_rpdf.ReadShapeFile()
    point_row, point_column = point_rpdf.PointMatchRasterRowColumn(srtm_rr.raster_ds_geotrans)

    # 基准值
    srtm_list = RR.SearchRasterRowColumnData(point_row, point_column, raster_ds_data=srtm_data)
    # 预测值，需要与基准值相加
    predict_list = RR.SearchRasterRowColumnData(point_row, point_column, raster_ds_data=predict_data)
    predict_dem_list = [x + y for x, y in zip(srtm_list, predict_list)]
    # ICESat2实测值，需要从point中读取，point中的delta_ele
    # delta_list = point_df['Delta_Ele'].tolist()
    # icesat_list = [x + y for x, y in zip(srtm_list, delta_list)]
    icesat_h_li = point_df['H_Li'].tolist()
    latitudes = point_df['Latitudes'].tolist()

    df = pd.DataFrame()
    csv_dict = {
        f'SRTM_DEM': srtm_list,
        f'Predict_DEM': predict_dem_list,
        # f'ICESat2_List': icesat_list,
        f'H_Li': icesat_h_li,
        f'Latitudes':latitudes
    }
    csv_df = pd.DataFrame(csv_dict)
    df = pd.concat([df, csv_df], axis=1)
    times = time.strftime('%Y_%m_%d_%H%M%S', time.localtime())
    output_path = os.path.join(output_csv_folder, f'ProfilePoint_{times}.csv')
    df.to_csv(output_path)
