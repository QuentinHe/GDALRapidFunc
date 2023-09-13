# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/9/13 10:25
# @Author : Hexk
# @Descript : 使用一个矢量文件来掩膜提取栅格，矢量外的数据归为Nodata
import shutil
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def RasterShapeMaskRaster(_input_shape_path, _input_raster_path, _output_raster_path):
    """
    实现根据矢量掩膜栅格
    mask_options中还有许多可调节参数，根据gdal.warp函数可以实现重投影和重采样
    详细见下:
    > https://www.jianshu.com/p/821c741ff169
    :param _input_shape_path: 输入的矢量文件
    :param _input_raster_path: 输入的栅格文件
    :param _output_raster_path: 输出掩膜后的栅格文件
    :return: None
    """
    print('正在根据矢量掩膜栅格文件...')
    if os.path.exists(_output_raster_path):
        shutil.rmtree(_output_raster_path)
        print('正在删除已存在文件夹...')
    else:
        os.makedirs(_output_raster_path)
        print('已创建输出文件夹.')
    output_name = os.path.splitext(os.path.split(_output_raster_path)[-1])[0] + '.tif'
    gdal.AllRegister()
    prog_func = gdal.TermProgress_nocb
    mask_options = gdal.WarpOptions(
        format='GTIFF',
        cutlineDSName=_input_shape_path,
        cropToCutline=True,
        dstNodata=0,
        callback=prog_func
    )
    mask_result = gdal.Warp(
        destNameOrDestDS=os.path.join(_output_raster_path, output_name),
        srcDSOrSrcDSTab=_input_raster_path,
        options=mask_options
    )
    mask_result.FlushCache()
    del mask_result
    return None


if __name__ == '__main__':
    input_shape_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\0_Landsat8\3_Landsat8_RGI_FourYear\3_Landsat8_RGI_2020.shp'
    input_raster_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Analysis_Raster_Result\NASA_DeltaH_2022\NASA_DeltaH_2022.tif'
    output_raster_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Predict_Result\Delta_H_Analysis\Delta_NASA_2022'
    RasterShapeMaskRaster(input_shape_path, input_raster_path, output_raster_path)
