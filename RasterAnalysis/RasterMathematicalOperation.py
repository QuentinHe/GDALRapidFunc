# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/9/13 9:43
# @Author : Hexk
# @Descript : 两个栅格相减
import shutil

import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadRaster as RR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def RasterSubtract(_main_raster_path, _output_folder, _output_name='RasterSubtractResult', *other_raster_path):
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


def RasterAdd(_main_raster_path, _output_folder, _output_name='RasterAddResult', *_other_raster_path):
    if _other_raster_path:
        main_rr = RR.ReadRaster(_main_raster_path)
        main_data = main_rr.ReadRasterFile()
        other_raster_data_list = []
        for index, item in enumerate(_other_raster_path):
            other_rr = RR.ReadRaster(item)
            other_data = other_rr.ReadRasterFile()
            other_raster_data_list.append(other_data)
        result = main_data
        for index, item in enumerate(other_raster_data_list):
            result += item
        if os.path.exists(_output_folder):
            shutil.rmtree(_output_folder)
        else:
            print('输出文件夹不存在，正在创建.')
        os.makedirs(_output_folder)
        output_result_path = os.path.join(_output_folder, f'{_output_name}.tif')
        main_rr.WriteRasterFile(result, output_result_path, _nodata=0)
    else:
        print('ERROR:未输入其他相加Raster.'.center(30, '*'))
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
    main_raster_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\5_GlaciersDepth\temp\SRTM_DEM.tif"
    other_raster_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\5_GlaciersDepth\temp\SRTM_2019_Mean.tif"
    output_raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\5_GlaciersDepth\temp\Add'
    RasterAdd(main_raster_path, output_raster_folder, 'SRTM_OutputDEM', *(other_raster_path,))
