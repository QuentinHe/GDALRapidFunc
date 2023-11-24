# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/14 上午11:12
# @Author : Hexk
# @Descript :

import shutil

import numpy as np
from osgeo import gdal, ogr, osr
import os
import DataAnalysis.Drawing as Drawing
import ReadRasterAndShape.ReadPoint2DataFrame as RSDF
import PathOperation.PathGetFiles as PGFiles

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def ShapeFilterOutliers(_input_path, _output_folder, _x_df_field, _y_df_field):
    print('正在执行函数ShapeFilterOutliers,去除箱线图中的异常值...')
    input_rsdf = RSDF.ReadPoint2DataFrame(_input_path)
    input_df = input_rsdf.ReadShapeFile()
    boxplot_data_dict = dict()
    for i in np.arange(1, max(input_df[_x_df_field]) + 1):
        #     bin_50_dict[i] = []
        boxplot_data_dict[i] = []
    for index, item in enumerate(input_df[_x_df_field]):
        boxplot_data_dict[item].append(input_df[_y_df_field][index])
    # 绘制箱线图
    print('正在绘制箱线图...')
    boxplot = Drawing.DrawingBoxs(boxplot_data_dict.values(), boxplot_data_dict.keys(), _x_df_field, _y_df_field,
                                  _title=_x_df_field)
    boxs_num, boxs_max, boxs_min, fliers_length = Drawing.DrawingBoxsFilters(boxplot)
    # print(f'箱子数量为:{boxs_num}.')
    # for i in np.arange(int(boxs_num)):
    #     print(f'箱子{i + 1} --- Max:{boxs_max[i]}; Min:{boxs_min[i]}')
    # 读取shp文件
    ogr.RegisterAll()
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "UTF8")

    output_name = os.path.splitext(os.path.split(_output_folder)[-1])[0]
    if not os.path.exists(_output_folder):
        os.makedirs(_output_folder)
        print('不存在ShapeFilterOutliers处理后的文件，以创建文件夹...')
    else:
        shutil.rmtree(_output_folder)
        print('ShapeFilterOutliers处理后的文件已存在，正在删除...')

    driver = ogr.GetDriverByName('ESRI ShapeFile')
    src_ds = ogr.Open(_input_path)
    src_layer = src_ds.GetLayer()
    ref_srs = src_layer.GetSpatialRef()
    geom_tpye = src_layer.GetGeomType()

    output_ds = driver.CreateDataSource(_output_folder)
    output_layer = output_ds.CreateLayer(output_name, ref_srs, geom_tpye)
    temp_feature = src_layer.GetFeature(0)
    src_layer.ResetReading()
    print(f'源Feature个数为:{src_layer.GetFeatureCount()}')

    print('正在为Feature创建原有字段...')
    for n in range(temp_feature.GetFieldCount()):
        output_field = ogr.FieldDefn(input_rsdf.feature_columns[n], temp_feature.GetFieldType(n))
        output_field.SetWidth(50)
        output_field.SetPrecision(8)
        output_layer.CreateField(output_field)

    for num in np.arange(src_layer.GetFeatureCount()):
        feature = src_layer.GetFeature(num)
        filter_value = feature.GetFieldAsDouble(_y_df_field)
        filter_level = feature.GetFieldAsInteger(_x_df_field)
        if boxs_min[filter_level - 1] <= filter_value <= boxs_max[filter_level - 1]:
            output_layer.CreateFeature(feature)
            output_feature = output_layer.GetFeature(output_layer.GetFeatureCount() - 1)
            for n in range(temp_feature.GetFieldCount()):
                output_feature.SetField(input_rsdf.feature_columns[n], feature.GetField(n))
            output_layer.SetFeature(output_feature)
        # else:
        #     print(f'{feature.GetFieldAsDouble("Segment_ID")}')

    print(f'输出数据集长度为:{output_layer.GetFeatureCount()};'
          f'原数据集长度为:{src_layer.GetFeatureCount()};'
          f'过滤数量:{src_layer.GetFeatureCount() - output_layer.GetFeatureCount()};')
    src_ds.Release()
    output_ds.Release()
    return None


if __name__ == '__main__':
    input_folder_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\9_Add_Dleta_Elevation_Field'
    output_folder_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\10_Filter_Outliers_Data'
    # 遍历指定文件夹获取所有shp文件
    loop_fields = ['B50', 'B100', 'B150', 'B200']
    conditional_type = ['M5', 'M10', 'P5', 'P10', 'R5', 'R10']
    shape_path_list, shape_name_list = PGFiles.PathGetFiles(input_folder_path, '.shp')
    for index, item in enumerate(shape_path_list):
        for bins in loop_fields:
            for ctype in conditional_type:
                ShapeFilterOutliers(item,
                                    os.path.join(output_folder_path, shape_name_list[index] + '_' + bins + '_' + ctype),
                                    f'{bins}_{ctype}',
                                    f'DH_{ctype}')
                print(f'{os.path.join(output_folder_path, shape_name_list[index] + "_" + bins)}执行完毕.')
