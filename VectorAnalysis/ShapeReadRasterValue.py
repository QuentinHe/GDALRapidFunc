# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/9/11 10:41
# @Author : Hexk
# @Descript : 用于读取Point点覆盖在Raster上的值，并将值写入DF中，输出成shp
#               不能用DF来输出，坐标系就不是空间直角坐标系了。
#               这个函数使用不能通用，需要对函数内部进行修改。
#               尤其是修改其中对输入字段格式的信息。 OFT.REAL等 若是INT则要用int
import shutil

import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadShape2DataFrame as RSDF
import ReadRasterAndShape.ReadRaster as RR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def ReadRasterValueToShapeField(_input_shape_path, _input_raster_path, _output_shape_path, _field_name):
    if not os.path.exists(_output_shape_path):
        os.makedirs(_output_shape_path)
        print('不存在ReadRasterValueToShapeField处理后的文件...')
    else:
        shutil.rmtree(_output_shape_path)
        print('ReadRasterValueToShapeField处理后的文件已存在，正在删除...')

    output_name = os.path.splitext(os.path.split(_output_shape_path)[-1])[0]
    # 读取矢量DataFrame
    input_shape_rsdf = RSDF.ReadPoint2DataFrame(_input_shape_path)
    input_shape_df = input_shape_rsdf.ReadShapeFile()
    # 读取栅格Raster
    input_raster_rr = RR.ReadRaster(_input_raster_path)
    input_raster_data = input_raster_rr.ReadRasterFile()
    # -------------------------------------
    # -------------------------------------
    # proj_x_list, proj_y_list = input_raster_rr.ReadRasterProjCoordinate()
    # proj_x_data = np.array(proj_x_list).reshape(input_raster_rr.raster_ds_y_size, input_raster_rr.raster_ds_x_size)
    # proj_y_data = np.array(proj_y_list).reshape(input_raster_rr.raster_ds_y_size, input_raster_rr.raster_ds_x_size)
    # -------------------------------------
    # -------------------------------------
    # 找到point对应的行列
    point_row, point_column = input_shape_rsdf.PointMatchRasterRowColumn(input_raster_rr.raster_ds_geotrans)
    print(f'检验获取行列点是否正常:{point_row[0], point_column[0]}')
    raster_point_value = RR.SearchRasterRowColumnData(input_raster_data, point_row, point_column)
    # 以下这一段只需要执行一次，之后可以注释掉
    # -------------------------------------
    # raster_point_proj_x_value = RR.SearchRasterRowColumnData(proj_x_data, point_row, point_column)
    # raster_point_proj_y_value = RR.SearchRasterRowColumnData(proj_y_data, point_row, point_column)
    # -------------------------------------
    driver = ogr.GetDriverByName('ESRI ShapeFile')
    src_ds = ogr.Open(input_shape_path)
    src_layer = src_ds.GetLayer()
    ref_srs = src_layer.GetSpatialRef()
    geom_tpye = src_layer.GetGeomType()
    output_ds = driver.CreateDataSource(_output_shape_path)
    output_layer = output_ds.CreateLayer(output_name, ref_srs, geom_tpye)

    temp_feature = src_layer.GetFeature(0)
    print('正在为Feature创建原有字段...')
    for n in range(temp_feature.GetFieldCount()):
        output_field = ogr.FieldDefn(input_shape_rsdf.feature_columns[n], temp_feature.GetFieldType(n))
        output_field.SetWidth(50)
        output_field.SetPrecision(8)
        output_layer.CreateField(output_field)
    print('正在为Feature创建新的字段...')
    # 下面这一段注销
    # -------------------------------------
    # output_feature_field_1 = ogr.FieldDefn('Proj_X', ogr.OFTReal)
    # output_feature_field_1.SetWidth(50)
    # output_feature_field_1.SetPrecision(8)
    # output_feature_field_2 = ogr.FieldDefn('Proj_Y', ogr.OFTReal)
    # output_feature_field_2.SetWidth(50)
    # output_feature_field_2.SetPrecision(8)
    # output_layer.CreateField(output_feature_field_1)
    # output_layer.CreateField(output_feature_field_2)
    # -------------------------------------
    output_feature_field_3 = ogr.FieldDefn(_field_name, ogr.OFTReal)
    output_feature_field_3.SetWidth(50)
    output_feature_field_3.SetPrecision(8)
    output_layer.CreateField(output_feature_field_3)

    print('正在写入字段信息...')
    for i in range(src_layer.GetFeatureCount()):
        feature = src_layer.GetFeature(i)
        output_layer.CreateFeature(feature)
        output_feature = output_layer.GetFeature(i)
        for n in range(temp_feature.GetFieldCount()):
            output_feature.SetField(input_shape_rsdf.feature_columns[n], feature.GetField(n))
        # ---------------------------------------
        # output_feature.SetField('Proj_X', raster_point_proj_x_value[i])
        # output_feature.SetField('Proj_Y', raster_point_proj_y_value[i])
        # ---------------------------------------
        output_feature.SetField(_field_name, float(raster_point_value[i]))
        output_layer.SetFeature(output_feature)
    print(f'写入完成.\n'
          f'原数据集长度为{src_layer.GetFeatureCount()},字段数量为:{src_layer.GetFeature(0).GetFieldCount()};\n'
          f'现数据集长度为{output_layer.GetFeatureCount()},字段数量为:{output_layer.GetFeature(0).GetFieldCount()};')
    src_ds.Release()
    output_ds.Release()


if __name__ == '__main__':
    input_shape_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\ICESat2\8_All_Raster_DataFrame_Data\4_Undulation\SRTM_2019\SRTM_2019.shp'
    input_raster_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\0_BaseDEM\SRTM_DEM\SRTM_DEM.tif'
    output_shape_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\ICESat2\8_All_Raster_DataFrame_Data\5_Elevation\SRTM_2019'

    ReadRasterValueToShapeField(input_shape_path, input_raster_path, output_shape_path, 'Elevation')
