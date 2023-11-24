# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/9/13 9:43
# @Author : Hexk
# @Descript : 栅格计算器内容，包含一系列数学运算
import shutil

import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadRaster as RR
import PathOperation.PathGetFiles as PGFiles

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def RasterReduce(_main_raster_path, _output_folder, *other_raster_path, _output_name='RasterSubtractResult'):
    if other_raster_path:
        main_rr = RR.ReadRaster(_main_raster_path)
        main_data = main_rr.ReadRasterFile()
        other_raster_data_list = []
        for index, item in enumerate(other_raster_path):
            other_rr = RR.ReadRaster(item)
            other_data = other_rr.ReadRasterFile()
            other_raster_data_list.append(other_data)
        result = main_data
        for index, item in enumerate(other_raster_data_list):
            result -= item
        if os.path.exists(_output_folder):
            shutil.rmtree(_output_folder)
        else:
            print('输出文件夹不存在，正在创建.')
        os.makedirs(_output_folder)
        output_result_path = os.path.join(_output_folder, f'{_output_name}.tif')
        main_rr.WriteRasterFile(result, output_result_path, _nodata=0)
    else:
        print('ERROR:未输入其他相减Raster.'.center(30, '*'))
    return None


def RasterAdd(_main_raster_path, _output_folder, *_other_raster_path_tuple, _output_name='RasterAddResult'):
    if _other_raster_path_tuple:
        main_rr = RR.ReadRaster(_main_raster_path)
        main_data = main_rr.ReadRasterFile()
        other_raster_data_list = []
        for index, item in enumerate(_other_raster_path_tuple):
            print(f'item:{item}')
            other_rr = RR.ReadRaster(item)
            other_data = other_rr.ReadRasterFile()
            other_raster_data_list.append(other_data)
        result = main_data
        for index, item in enumerate(other_raster_data_list):
            result += item
        output_result_path = os.path.join(_output_folder, f'{_output_name}.tif')
        main_rr.WriteRasterFile(result, output_result_path, _nodata=0)
    else:
        print('ERROR:未输入其他相加Raster.'.center(30, '*'))
    return None


def RasterDivide(_main_raster_path, _output_raster_folder, *_other_raster_path_tuple, _denominator=None,
                 _denominator_raster_path=None):
    print('正在执行除法计算'.center(30, '*'))
    denominator = None
    if _denominator:
        # 说明raster除以一个常数
        denominator = _denominator
        print(f'分母为常数{denominator}')
    elif _denominator_raster_path:
        _denominator_rr = RR.ReadRaster(_denominator_raster_path)
        _denominator_data = _denominator_rr.ReadRasterFile()
        denominator = _denominator_data
        print(f'分母为矩阵{denominator.shape()}')
    else:
        print('_denominator和_denominator_raster_path均为None,无法执行运算.')
        return None
    if denominator:
        print('正在计算...')
        main_rr = RR.ReadRaster(_main_raster_path)
        main_data = main_rr.ReadRasterFile()
        main_result = main_data / denominator
        main_result_name = os.path.splitext(os.path.split(_main_raster_path)[1])[0]
        main_result_output_path = os.path.join(_output_raster_folder, f'Divide_{main_result_name}.tif')
        main_rr.WriteRasterFile(main_result, main_result_output_path, _nodata=0)
        if _other_raster_path_tuple:
            other_raster_data_list = []
            for index, item in enumerate(_other_raster_path_tuple):
                other_rr = RR.ReadRaster(item)
                other_data = other_rr.ReadRasterFile()
                other_raster_data_list.append(other_data)
            for index, item in enumerate(other_raster_data_list):
                other_result = item / denominator
                other_result_name = os.path.splitext(os.path.split(_other_raster_path_tuple[index])[1])[0]
                other_result_output_path = os.path.join(_output_raster_folder, f'{other_result_name}.tif')
                main_rr.WriteRasterFile(other_result, other_result_output_path, _nodata=0)
    return None


def RasterReduceMean(_main_raster_path, _output_raster_folder, *_other_raster_path_tuple):
    # 减去所有像元的平均值
    print('正在执行去除均值计算'.center(30, '*'))
    main_rr = RR.ReadRaster(_main_raster_path)
    main_data = main_rr.ReadRasterFile()
    main_data_list = np.array([x for x in main_data.reshape(-1) if x != 0])
    main_mean = np.mean(main_data_list)
    main_zero_indices = np.where(main_data == 0)
    main_result = main_data - main_mean
    main_result[main_zero_indices] = 0
    main_name = os.path.splitext(os.path.split(_main_raster_path)[1])[0]
    main_output_path = os.path.join(_output_raster_folder, f'{main_name}.tif')
    main_rr.WriteRasterFile(main_result, main_output_path, _nodata=0)
    if _other_raster_path_tuple:
        for index, item in enumerate(_other_raster_path_tuple):
            other_rr = RR.ReadRaster(item)
            other_data = other_rr.ReadRasterFile()
            other_data_list = np.array([x for x in other_data.reshape(-1) if x != 0])
            other_mean = np.mean(other_data_list)
            other_zero_indices = np.where(other_data == 0)
            other_result = other_data - other_mean
            other_result[other_zero_indices] = 0
            other_name = os.path.splitext(os.path.split(item)[1])[0]
            other_path = os.path.join(_output_raster_folder, f'{other_name}.tif')
            main_rr.WriteRasterFile(other_result, other_path, _nodata=0)
    return None


if __name__ == '__main__':
    # first_raster_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Predict_Result\TESTA\2_MASK\NASA_2022_Bin50\NASA_2022_Bin50.tif'
    # second_raster_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Predict_Result\TESTA\2_MASK\NASA_2021_Bin50\NASA_2021_Bin50.tif'
    # output_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Predict_Result\TESTA\3_Annual\NASA_2022_Change'
    # RasterSubtract(first_raster_path, second_raster_path, output_path)
    # main_raster_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\5_GlaciersDepth\1_MaskDEM\1_MaskDEM.tif"
    # other_raster_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Result_20231022\1_YearChangeResult\4_MeanData\SRTM_2019\SRTM_2019.tif"
    # output_raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\5_GlaciersDepth\2_OutputDEM'
    # RasterAdd(main_raster_path, output_raster_folder, 'SRTM_OutputDEM', *(other_raster_path,))
    # main_raster_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\5_GlaciersDepth\temp\SRTM_DEM.tif"
    # other_raster_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\5_GlaciersDepth\temp\SRTM_2019_Mean.tif"
    # output_raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\5_GlaciersDepth\temp\Add'
    # RasterAdd(main_raster_path, output_raster_folder, 'SRTM_OutputDEM', *(other_raster_path,))
    # raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\2_PredictData\2_Intra\4_MeanData'
    # raster_path_list, raster_name_list = PGFiles.PathGetFiles(raster_folder, '.tif')
    # srtm_path_list, srtm_name_list = [], []
    # for index, item in enumerate(raster_name_list):
    #     if 'SRTM' in item:
    #         srtm_name_list.append(item)
    #         srtm_path_list.append(raster_path_list[index])
    # output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231105_1_MonthlyChangeRate'
    # other_raster_path_tuple = tuple(srtm_path_list[0:])
    # print(srtm_name_list)
    # print(other_raster_path_tuple)
    # RasterDivide(srtm_path_list[0], output_folder, 19, *other_raster_path_tuple)
    # input_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231105_1_MonthlyChangeRate'
    # output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231105_2_MonthlyChangeReduceMean'
    # raster_path_list, raster_name_list = PGFiles.PathGetFiles(input_folder, '.tif')
    # other_raster_path_tuple = tuple(raster_path_list[1:])
    # RasterReduceMean(raster_path_list[0], output_folder, *other_raster_path_tuple)

    # # 计算Monthly变化全部相加，之后取平均
    # raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231105_2_MonthlyChangeReduceMean'
    # raster_path_list, raster_name_list = PGFiles.PathGetFiles(raster_folder, '.tif')
    # output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231107_1_MonthlyRasterSum'
    # other_path_tuple = tuple(raster_path_list[1:])
    # RasterAdd(raster_path_list[0], output_folder, *other_path_tuple)

    # 除法一次
    raster_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231107_1_MonthlyRasterSum\RasterAddResult.tif"
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231107_1_MonthlyRasterSum'
    RasterDivide(raster_path, output_folder, _denominator=12)
