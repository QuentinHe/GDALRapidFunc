# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/9/16 14:06
# @Author : Hexk
# @Descript : 对矢量数据表进行运算，实现某一列减某一列，并输出到新的一个字段中
import shutil

import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadShape2DataFrame as RSDF

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def ShapeFieldCalculate(_input_path, _output_path, _first_field, _second_field, _result_field):
    ogr.RegisterAll()
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "UTF8")

    output_name = os.path.splitext(os.path.split(_output_path)[-1])[0]
    if not os.path.exists(_output_path):
        os.makedirs(_output_path)
        print('不存在ShapeFieldCalculate处理后的文件，以创建文件夹...')
    else:
        shutil.rmtree(_output_path)
        print('ShapeFieldCalculate处理后的文件已存在，正在删除...')

    driver = ogr.GetDriverByName('ESRI ShapeFile')
    src_ds = ogr.Open(_input_path)
    src_layer = src_ds.GetLayer()
    ref_srs = src_layer.GetSpatialRef()
    geom_tpye = src_layer.GetGeomType()

    output_ds = driver.CreateDataSource(_output_path)
    output_layer = output_ds.CreateLayer(output_name, ref_srs, geom_tpye)
    temp_feature = src_layer.GetFeature(0)
    src_layer.ResetReading()

    # 获取原表表头
    input_rsdf = RSDF.ReadPoint2DataFrame(_input_path)
    input_df = input_rsdf.ReadShapeFile()
    print('正在为Feature创建原有字段...')
    for n in range(temp_feature.GetFieldCount()):
        output_field = ogr.FieldDefn(input_rsdf.feature_columns[n], temp_feature.GetFieldType(n))
        output_field.SetWidth(50)
        output_field.SetPrecision(8)
        output_layer.CreateField(output_field)
    print('正在为Feature创建新的字段...')
    output_field = ogr.FieldDefn(_result_field, ogr.OFTReal)
    output_field.SetWidth(50)
    output_field.SetPrecision(5)
    output_layer.CreateField(output_field)

    for item in np.arange(src_layer.GetFeatureCount()):
        feature = src_layer.GetFeature(item)
        output_layer.CreateFeature(feature)
        output_feature = output_layer.GetFeature(item)
        for n in range(temp_feature.GetFieldCount()):
            output_feature.SetField(input_rsdf.feature_columns[n], feature.GetField(n))
        reduce_result = feature.GetFieldAsDouble(_first_field) - feature.GetFieldAsDouble(_second_field)
        output_feature.SetField(_result_field, reduce_result)
        output_layer.SetFeature(output_feature)

    print(f'写入完成.\n'
          f'原数据集字段数量为:{src_layer.GetFeature(0).GetFieldCount()};\n'
          f'现数据集字段数量为:{output_layer.GetFeature(0).GetFieldCount()};')
    src_ds.Release()
    output_ds.Release()


if __name__ == '__main__':
    input_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\ICESat2\8_All_Raster_DataFrame_Data\5_Elevation\SRTM_2019\SRTM_2019.shp'
    output_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20230916\1_FilterOutliers\0_AddReduceElevation\SRTM_2019'
    ShapeFieldCalculate(input_path, output_path, 'H_Li', 'Elevation', 'Delta_Ele')
