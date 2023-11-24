# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/13 上午9:50
# @Author : Hexk
# @Descript : 矢量转栅格，设定栅格值，再通过相加相减到指定栅格上
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr, gdalconst
import os
import ReadRasterAndShape.ReadRaster as RR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def vector2raster(_input_shape_path, _output_raster_path, _target_raster_path, bands=[1], burn_values=[0], field=None,
                  all_touch="False"):
    """
    > https://blog.csdn.net/df1445/article/details/124310188
    :param _input_shape_path:   shape路径
    :param _output_raster_path: 输出栅格路径
    :param _target_raster_path: 目标模板栅格路径
    :param bands:   波段数目
    :param burn_values: 像元值
    :param field:   或者转化为shape的字段值，默认为None， 使用如 'GLACID'
    :param all_touch:   转换方式，选择False刚好可以与原栅格重叠，是不饱和转化。
    :return:
    """
    # 打开栅格模板文件
    data = gdal.Open(_target_raster_path, gdalconst.GA_ReadOnly)
    # 确定栅格大小
    x_size = data.RasterXSize
    y_size = data.RasterYSize
    # 打开矢量文件
    vector = ogr.Open(_input_shape_path)
    # 获取矢量图层
    layer = vector.GetLayer()
    # 查看要素数量
    featureCount = layer.GetFeatureCount()
    # print(featureCount)

    # 创建输出的TIFF栅格文件
    targetDataset = gdal.GetDriverByName('GTiff').Create(_output_raster_path, x_size, y_size, 1, gdal.GDT_Byte)
    # 设置栅格坐标系与投影
    targetDataset.SetGeoTransform(data.GetGeoTransform())
    targetDataset.SetProjection(data.GetProjection())
    # 目标band 1
    band = targetDataset.GetRasterBand(1)
    # 白色背景
    # NoData_value = -999
    NoData_value = 0
    band.SetNoDataValue(NoData_value)
    band.FlushCache()
    if field:
        # 调用栅格化函数。RasterizeLayer函数有四个参数，分别有栅格对象，波段，矢量对象，options
        # options可以有多个属性，其中ATTRIBUTE属性将矢量图层的某字段属性值作为转换后的栅格值
        gdal.RasterizeLayer(targetDataset, bands, layer, burn_values=burn_values,
                            options=["ALL_TOUCHED=" + all_touch, "ATTRIBUTE=" + field])
    else:
        gdal.RasterizeLayer(targetDataset, bands, layer, burn_values=burn_values, options=["ALL_TOUCHED=" + all_touch])


if __name__ == '__main__':
    region_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\20240512_1_ModifyRegionShape\20240512_2_CutRegion.shp"
    srtm_dem_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\0_PreTest_BaseData\4_BaseSRTMDEM\SRTM\SRTM_DEM.tif"
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\20240513_1_RasterizeRegion'
    output_path = os.path.join(output_folder, '20240513_1_SRTM_Modify10.tif')
    vector2raster(region_path, output_path, srtm_dem_path, burn_values=[10])
