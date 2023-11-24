# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/13 下午3:29
# @Author : Hexk
# @Descript :
from osgeo import osr, ogr, gdal
import os
import numpy as np
import pandas
import ReadRasterAndShape.ReadRaster as RR
import ReadRasterAndShape.ReadPoint2DataFrame as RSDF
import PathOperation.PathGetFiles as PGF

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def RasterBaseRasterClearVector(_point_raster_value, _feature_columns, _threshold, _input_path, _output_folder,
                                _ouput_name):
    """
    按照DEM的值来过滤point要素
    NB:修改了一下该函数，目前并不知道有什么方法可以直接获取shp的Field名称，只能采取下策，输入一个_feature_columns来表示字段名称。
    :param _feature_columns: Field Names List
    :param _point_raster_value: Point点对应的栅格值，该值通过其他函数获得，其他函数在其他文件夹中已经存在；
    :param _threshold: 过滤阈值，坡度设定为保留30以内
    :param _input_path: 输入文件路径shp
    :param _output_folder: 输出文件夹
    :return: None
    """
    ogr.RegisterAll()
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "UTF8")

    output_name = os.path.splitext(os.path.split(_input_path)[-1])[0]+f'_{_ouput_name}'  # 2019
    ouput_path = os.path.join(_output_folder, output_name)

    driver = ogr.GetDriverByName('ESRI ShapeFile')
    src_ds = ogr.Open(_input_path)
    src_layer = src_ds.GetLayer()
    ref_srs = src_layer.GetSpatialRef()
    geom_tpye = src_layer.GetGeomType()

    output_ds = driver.CreateDataSource(_output_folder)
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
    point_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\6_RGI_Point_Data'
    slope_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\5_BaseDEMProductions\Slope'
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\7_Remove_Slope_Data'
    point_list, point_name = PGF.PathGetFiles(point_folder, '.shp')
    slope_list, slope_name = PGF.PathGetFiles(slope_folder, '.tif')

    for pointpath_index, pointpath_item in enumerate(point_list):
        point_rsdf = RSDF.ReadPoint2DataFrame(pointpath_item)
        point_df = point_rsdf.ReadShapeFile()
        for slopepath_index, slopepath_item in enumerate(slope_list):
            slope_rr = RR.ReadRaster(slopepath_item)
            slope_data = slope_rr.ReadRasterFile()
            point_row, point_column = point_rsdf.PointMatchRasterRowColumn(slope_rr.raster_ds_geotrans)
            point_raster_value = RR.SearchRasterRowColumnData(point_row, point_column, raster_ds_data=slope_data)
            target_name = slope_name[slopepath_index].split('_')[1]
            RasterBaseRasterClearVector(point_raster_value, point_rsdf.feature_columns, 30, pointpath_item,
                                        output_folder, target_name)
