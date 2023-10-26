# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/9/13 10:25
# @Author : Hexk
# @Descript : 使用一个矢量文件来掩膜提取栅格，矢量外的数据归为Nodata
import shutil
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
        destNameOrDestDS=_output_raster_path,
        srcDSOrSrcDSTab=_input_raster_path,
        options=mask_options
    )
    mask_result.FlushCache()
    del mask_result
    return _output_raster_path


if __name__ == '__main__':
    # input_shape_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\0_Landsat8\3_Landsat8_RGI_FourYear\3_Landsat8_RGI_2020.shp'
    # input_raster_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Predict_Result\TESTA\1_Reduce\NASA_2022\NASA_2022.tif'
    # output_raster_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Predict_Result\TESTA\2_MASK\NASA_2022_Bin50'
    # input_shape_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\0_Landsat8\3_Landsat8_RGI_FourYear\3_Landsat8_RGI_2020.shp"
    input_shape_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\1_ResearchArea\TP_Basin\TP_Basin.shp"
    input_raster_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\1_ResearchArea\TP_DEM\TP_DEM_Mask.tif"
    # output_raster_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231003\3_Mask_PredictResult\2019_Bin_50'
    output_raster_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\1_ResearchArea\TP_DEM\TP_DEM_Mask_1.tif'
    RasterShapeMaskRaster(input_shape_path, input_raster_path, output_raster_path)

