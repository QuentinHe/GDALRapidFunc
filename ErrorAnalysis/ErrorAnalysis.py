# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/9/12 16:25
# @Author : Hexk
# @Descript : 常用的误差计算分析
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
import ReadRasterAndShape.ReadRaster as RR
import ReadRasterAndShape.ReadShape2DataFrame as RSDF

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def mae(_validate, _predict):
    _result = mean_absolute_error(_validate, _predict)
    print(f'MAE:{_result}')
    return _result


def mse(_validate, _predict):
    _result = mean_squared_error(_validate, _predict)
    print(f'MSE:{_result}')
    return _result


def rmse(_validate, _predict):
    _result = np.sqrt(mean_squared_error(_validate, _predict))
    print(f'RMSE:{_result}')
    return _result


def ErrorStatistics(_input_shape_path, _input_raster_path, _output_csv_path, _bins_field, _input_level_path=None):
    shape_rsdf = RSDF.ReadPoint2DataFrame(_input_shape_path)
    shape_df = shape_rsdf.ReadShapeFile()

    raster_rr = RR.ReadRaster(_input_raster_path)
    raster_data = raster_rr.ReadRasterFile()
    raster_list = raster_data.reshape(-1)

    point_row, point_column = shape_rsdf.PointMatchRasterRowColumn(raster_rr.raster_ds_geotrans)
    predict_value = RR.SearchRasterRowColumnData(raster_data, point_row, point_column)

    predict_value_bin_dict = dict()
    validate_bin_dict = dict()
    for i in range(int(max(shape_df[_bins_field]))):
        predict_value_bin_dict[i + 1] = []
        validate_bin_dict[i + 1] = []
    for index, item in enumerate(shape_df[_bins_field]):
        predict_value_bin_dict[int(item)].append(predict_value[index])
        validate_bin_dict[int(item)].append(shape_df['Delta_Ele'][index])

    total_mae = mae(shape_df['Delta_Ele'], predict_value)
    total_mse = mse(shape_df['Delta_Ele'], predict_value)
    total_rmse = rmse(shape_df['Delta_Ele'], predict_value)
    delta_h_std = np.std(predict_value)
    print(f'Delta_H_STD:{delta_h_std}')

    bin_rmse = []
    bin_mae = []
    bin_validate_std = []
    bin_predict_std = []
    for i in predict_value_bin_dict:
        bin_rmse.append(rmse(validate_bin_dict[i], predict_value_bin_dict[i]))
        bin_mae.append(mae(validate_bin_dict[i], predict_value_bin_dict[i]))
        bin_validate_std.append(np.std(validate_bin_dict[i]))
        bin_predict_std.append(np.std(predict_value_bin_dict[i]))

    csv_dict = dict(
        Bin_MAE=bin_mae,
        Bin_RMSE=bin_rmse,
        Bin_Validate_STD=bin_validate_std,
        Bin_Predict_STD=bin_predict_std,
        Total_MAE=total_mae,
        Total_MSE=total_mse,
        Total_RMSE=total_rmse,
        Total_Delta_H_STD=delta_h_std
    )
    csv_df = pd.DataFrame(csv_dict)
    csv_df.to_csv(_output_csv_path)

    # 统计分箱误差
    if _input_level_path is not None:
        level_rr = RR.ReadRaster(_input_level_path)
        level_data = level_rr.ReadRasterFile()
        level_list = np.array(level_data.reshape(-1))
        delta_h_dict = dict()
        for i in range(int(max(shape_df[_bins_field]))):
            delta_h_dict[i + 1] = []
        threshold = 50
        for index, item in enumerate(level_list):
            if raster_list[index] != 0 and np.abs(raster_list[index]) <= threshold:
                delta_h_dict[int(item)].append(raster_list[index] / 19)
        delta_h_mean = []
        for i in delta_h_dict:
            delta_h_mean.append(np.mean(delta_h_dict[i]))
        print(delta_h_mean, np.mean(delta_h_mean))


if __name__ == '__main__':
    input_shape_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20230916\1_FilterOutliers\1_FilterOutliers\NASA_2019_Bin_50'
    input_raster_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20230916\1_FilterOutliers\3_MaskResult\NASA_2019\NASA_2019.tif'
    output_csv_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20230916\1_FilterOutliers\4_CSV\NASA_BIN_50.csv'
    input_level_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Analysis_Raster_Result\0_TEMP_Reclassify\NASA_Reclassify_50.tif'
    ErrorStatistics(input_shape_path, input_raster_path, output_csv_path, 'Bin_50', _input_level_path=input_level_path)
