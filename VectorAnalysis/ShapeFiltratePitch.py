# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/9/6 9:36
# @Author : Hexk
# 过滤矢量文件中的面积小于某个阈值的小图斑

from osgeo import ogr, gdal, osr
import os
import numpy as np
import pandas as pd


def ShapeFiltratePitch(_input_path, _output_path, _area_threshold):
    """
    过滤POLYGON Shape中的细小图斑，根据面积来过滤。
    :param _input_path: 输入文件路径
    :param _output_path: 输出文件的路径，不包括shp名称
    :param _area_threshold: 设定过滤面积阈值，单位平方米
    :return: None
    """
    driver = ogr.GetDriverByName('ESRI SHAPEFILE')
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "UTF8")

    src_ds = driver.Open(_input_path)
    src_layer = src_ds.GetLayer(0)
    src_ref = src_layer.GetSpatialRef()
    src_geom_type = src_layer.GetGeomType()

    output_name = os.path.splitext(os.path.split(_input_path)[1])[0]
    output_filename = f'{output_name}_ClearPitch.shp'
    output_abs_path = os.path.join(_output_path, output_filename)
    if os.path.exists(_output_path):
        print('当前输出文件夹路径已经存在.')
    else:
        os.makedirs(_output_path)

    if os.path.exists(output_abs_path):
        driver.DeleteDataSource(output_abs_path)
    else:
        print('需要输出的shape文件并不存在.')
    output_ds = driver.CreateDataSource(output_abs_path)
    output_layer = output_ds.CreateLayer(output_filename, srs=src_ref, geom_type=src_geom_type)

    src_layer.ResetReading()
    i = 0
    print(f'源文件包含Feature个数:{src_layer.GetFeatureCount()}')
    while i < src_layer.GetFeatureCount():
        feature = src_layer.GetFeature(i)
        geometry = feature.GetGeometryRef()
        geometry_area = geometry.Area()
        if geometry_area >= _area_threshold:
            # src_layer.DeleteFeature(i)
            # print(f'删除第{i}个Feature'.center(20, '-'))
            output_layer.CreateFeature(feature)
        i += 1
    print(f'过滤斑块后文件包含Feature个数:{output_layer.GetFeatureCount()}')
    output_ds.Release()
    src_ds.Destroy()


if __name__ == '__main__':
    input_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\0_Landsat8\2_Landsat8_2022_NDSI_Clip_Update\Update_2_Landsat8_2022_NDSI_Clip_Update.shp'
    output_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\0_Landsat8\2_Landsat8_2022_NDSI_Clip_Update_FilterPitch'
    ShapeFiltratePitch(input_path, output_path, 50000)
