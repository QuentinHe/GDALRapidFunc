# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/9 11:22
# @Author : Hexk
# @Descript : 按照属性表字段对point shape进行重分类，读取全年的数据，并按照年份的日期，分为每个月的数据
import shutil

import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadPoint2DataFrame as RSDF
import PathOperation.PathGetFiles as PGF

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def ShapeReclassByDateField(_point_path, _output_folder):
    """
    按照日期Date Field对shp文件进行每月分类
    :param _point_path: 输入的shp point文件路径
    :param _output_folder: 输出的shp point文件夹
    :return: None
    """
    ogr.RegisterAll()
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "UTF8")
    point_rsdf = RSDF.ReadPoint2DataFrame(_point_path)
    point_df = point_rsdf.ReadShapeFile()
    # 过滤字段 point_df['Date']
    # 读取源shape文件
    driver = ogr.GetDriverByName('ESRI ShapeFile')
    src_ds = ogr.Open(_point_path)
    src_layer = src_ds.GetLayer()
    ref_srs = src_layer.GetSpatialRef()
    geom_tpye = src_layer.GetGeomType()
    # 按照月份分类点，并将12个月的layer放在dict中
    for i in range(1, 13):
        input_file_path, input_file = os.path.split(_point_path)
        input_file_name, input_file_suffix = os.path.splitext(input_file)
        output_path = os.path.join(_output_folder, input_file_name, f'{input_file_name}_Month{i}')
        if os.path.exists(output_path):
            shutil.rmtree(output_path)
            print('正在删除已存在ShapeReclassByDateField文件夹路径')
        os.makedirs(output_path)
        output_ds = driver.CreateDataSource(output_path)
        output_layer = output_ds.CreateLayer(f'{input_file_name}_Month{i}', ref_srs, geom_tpye)
        # 获取要素的相关信息
        temp_feature = src_layer.GetFeature(0)
        # 为12个layer创建字段
        for n in range(temp_feature.GetFieldCount()):
            output_field = ogr.FieldDefn(point_rsdf.feature_columns[n], temp_feature.GetFieldType(n))
            output_field.SetWidth(50)
            output_field.SetPrecision(8)
            output_layer.CreateField(output_field)
        src_layer.ResetReading()
        print(f'源Feature个数为:{src_layer.GetFeatureCount()}')
        print(f'开始按照DateField分类feature信息...')
        for num in range(src_layer.GetFeatureCount()):
            feature = src_layer.GetFeature(num)
            feature_date = feature.GetFieldAsString('Date')
            month = int(feature_date[:2])
            if month == i:
                output_layer.CreateFeature(feature)
                output_feature = output_layer.GetFeature(output_layer.GetFeatureCount() - 1)
                for n in range(temp_feature.GetFieldCount()):
                    output_feature.SetField(point_rsdf.feature_columns[n], feature.GetField(n))
                output_layer.SetFeature(output_feature)
            else:
                continue
        print(f'Month{i}的长度为:{output_layer.GetFeatureCount()}')
        output_ds.Release()
    src_ds.Release()
    return None


if __name__ == '__main__':
    point_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\1_PointData\11_MergePoint'
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\1_PointData\12_SeasonalPoint'
    files_path_list, files_name_list, = PGF.PathGetFiles(point_folder, '.shp')
    dem_list = ['NASA', 'SRTM']
    bin_list = [i * 50 for i in range(1, 5)]
    point_path = None
    for dem_index, dem_item in enumerate(dem_list):
        for bin_index, bin_item in enumerate(bin_list):
            for file_index, file_item in enumerate(files_name_list):
                if dem_item in file_item and f'Bin_{bin_item}' in file_item:
                    print(f'找到符合条件的{dem_item}  {bin_item} point shape文件.')
                    point_path = files_path_list[file_index]
                    ShapeReclassByDateField(point_path, output_folder)
                else:
                    print(f'未找到符合条件的{dem_item} {bin_item} point shape')
