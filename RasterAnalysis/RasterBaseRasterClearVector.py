# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/9/7 9:41
# @Author : Hexk
# 根据矢量点覆盖的在栅格上的值决定是否去除或保留该矢量点

from osgeo import osr, ogr, gdal
import os
import numpy as np
import pandas
import ReadRasterAndShape.ReadRaster as RR
import ReadRasterAndShape.ReadShape2DataFrame as RSDF

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def RasterBaseRasterClearVector(_point_raster_value, _feature_columns, _threshold, _input_path, _output_path):
    """
    按照DEM的值来过滤point要素
    NB:修改了一下该函数，目前并不知道有什么方法可以直接获取shp的Field名称，只能采取下策，输入一个_feature_columns来表示字段名称。
    :param _feature_columns: Field Names List
    :param _point_raster_value: Point点对应的栅格值，该值通过其他函数获得，其他函数在其他文件夹中已经存在；
    :param _threshold: 过滤阈值，坡度设定为保留30以内
    :param _input_path: 输入文件路径shp
    :param _output_path: 输出文件夹
    :return: None
    """
    ogr.RegisterAll()
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "UTF8")

    output_name = os.path.splitext(os.path.split(_output_path)[-1])[0]  # 2019

    if not os.path.exists(_output_path):  # \2019
        os.makedirs(_output_path)  # \2019
        print('不存在ClearRasterValue阈值处理后的文件...')
    else:
        os.remove(_output_path)  # \2019
        print('ClearRasterValue阈值处理后的文件已存在，正在删除...')

    driver = ogr.GetDriverByName('ESRI ShapeFile')
    src_ds = ogr.Open(_input_path)
    src_layer = src_ds.GetLayer()
    ref_srs = src_layer.GetSpatialRef()
    geom_tpye = src_layer.GetGeomType()

    output_ds = driver.CreateDataSource(_output_path)
    output_layer = output_ds.CreateLayer(output_name, ref_srs, geom_tpye)
    # 为output_layer创建Field，此时8个field字段就写入到output_layer中
    temp_feature = src_layer.GetFeature(0)
    for n in range(temp_feature.GetFieldCount()):
        output_field = ogr.FieldDefn(_feature_columns[n], temp_feature.GetFieldType(n))
        output_field.SetWidth(50)
        output_field.SetPrecision(8)
        output_layer.CreateField(output_field)
    src_layer.ResetReading()
    i = 0
    print(f'源Feature个数为:{src_layer.GetFeatureCount()}')
    print(f'开始写入feature信息...')
    while i < src_layer.GetFeatureCount():
        feature = src_layer.GetFeature(i)
        if _point_raster_value[i] < _threshold:
            output_layer.CreateFeature(feature)
            # 为output_layer的feature赋值
            output_feature = output_layer.GetFeature(output_layer.GetFeatureCount() - 1)
            # print(output_layer.GetFeature(output_layer.GetFeatureCount() - 1).GetFieldCount())
            for n in range(temp_feature.GetFieldCount()):
                output_feature.SetField(_feature_columns[n], feature.GetField(n))
            output_layer.SetFeature(output_feature)
        i += 1
    print(f'写入完成...')
    print(f'过滤后Feature个数为:{output_layer.GetFeatureCount()}')
    output_ds.Release()
    src_ds.Release()


if __name__ == '__main__':
    raster_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\1_DEM_Slope\NASA_DEM\1_NASA_Slope.tif'
    point_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\ICESat2\6_RGI_Point_Data\2022\2022.shp'
    output_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\ICESat2\7_Remove_Slope_Data\NASA_2022'
    # 获取Raster 的Data多维数组
    raster_RR = RR.ReadRaster(raster_path)
    raster_data = raster_RR.ReadRasterFile()
    # 将Point读取转化为DF
    point_RSDF = RSDF.ReadPoint2DataFrame(point_path)
    point_df = point_RSDF.ReadShapeFile()
    # 读取Point对应在Raster上的行列数
    point_row, point_column = point_RSDF.PointMatchRasterRowColumn(raster_RR.raster_ds_geotrans)
    # 根据行列数读取Raster值
    point_raster_value = RR.SearchRasterRowColumnData(raster_data, point_row, point_column)
    RasterBaseRasterClearVector(point_raster_value, point_RSDF.feature_columns, 30, point_path, output_path)
