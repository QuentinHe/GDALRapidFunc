# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/22 11:02
# @Author : Hexk
# @Descript :
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


class ReadShape2DataFrame:
    """
    该类本质上是一个通用性质的常规类。
    适用于读取polygon point line 等多样数据。
    """

    def __init__(self, input_path):
        self.feature_geom_list = None
        self.input_path = input_path
        self.feature_columns = None
        self.layer_count = None
        self.layer_feature_count = None
        self.feature_columns_types = None
        self.geometry = None

    def ReadShapeFile(self):
        print('正在读取Shape文件'.center(30, '*'))
        print(''.center(30, '-'))
        print(f'{self.input_path}'.center(30, ' '))
        print(''.center(30, '-'))


    def CreateField(self, _output_shape_path, _field_name, _field_type, _field_value_list=None):
        """
        给初始化对象的shape文件创建一个新的字段，字段的值可以默认为按顺序排列，可以设定为传入的list
        :param _field_value_list:
        :param _field_type:
        :param _field_name:
        :param _output_shape_path:
        :return: None
        """
        print('正在读取复制文件'.center(30, '*'))
        print(''.center(30, '-'))
        gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
        gdal.SetConfigOption("SHAPE_ENCODING", "UTF-8")
        ogr.RegisterAll()
        driver = ogr.GetDriverByName('ESRI ShapeFile')
        ds = ogr.Open(self.input_path)
        layer = ds.GetLayerByIndex(0)
        layer.ResetReading()
        print('正在创建输出文件'.center(30, '-'))
        output_ds = driver.CreateDataSource(_output_shape_path)
        output_layer = output_ds.CopyLayer(layer, 'output_layer')
        print(f'复制后的字段个数为:{output_layer.GetLayerDefn().GetFieldCount()}'.center(30, ' '))
        print(f'正在为复制后文件创建新字段'.center(30, '-'))
        if _field_type == ogr.OFTInteger:
            output_field = ogr.FieldDefn(_field_name, ogr.OFTInteger)
            output_field.SetWidth(50)
        elif _field_type == ogr.OFTReal:
            output_field = ogr.FieldDefn(_field_name, ogr.OFTReal)
            output_field.SetWidth(50)
            output_field.SetPrecision(8)
        else:
            output_field = ogr.FieldDefn(_field_name, ogr.OFTString)
            output_field.SetWidth(50)
        output_layer.CreateField(output_field)
        print('正在写入新字段数据'.center(30, '-'))
        output_layer.ResetReading()
        if _field_value_list:
            output_feature = output_layer.GetNextFeature()
            output_feature_index = 0
            while output_feature:
                # print(output_feature.GetFieldAsString('Name'))
                output_feature.SetField(_field_name, _field_value_list[output_feature_index])
                output_layer.SetFeature(output_feature)
                output_feature = output_layer.GetNextFeature()
                output_feature_index += 1
        else:
            output_feature = output_layer.GetNextFeature()
            output_feature_index = 0
            while output_feature:
                # print(output_feature.GetFieldAsString('Name'))
                # print(output_feature_index + 1)
                output_feature.SetField(_field_name, output_feature_index + 1)
                output_layer.SetFeature(output_feature)
                output_feature = output_layer.GetNextFeature()
                output_feature_index += 1
        print('写入完成'.center(30, '-'))
        output_ds.Destroy()
        ds.Release()
        return None


if __name__ == '__main__':
    shape_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\7_ConstractGlaciers\20231025_MySelectGlaciers.shp"
    output_shape_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\7_ConstractGlaciers\20231025_MySelectGlaciers_GLACID.shp"
    polygon_rpdf = ReadShape2DataFrame(shape_path)
    polygon_df = polygon_rpdf.ReadShapeFile()
    polygon_rpdf.CreateField(output_shape_path, 'GLACID', ogr.OFTInteger)
