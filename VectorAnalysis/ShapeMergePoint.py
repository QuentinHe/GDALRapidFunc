# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/9 15:33
# @Author : Hexk
# @Descript : 融合两个字段相同的shp point文件
import operator
import shutil

import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadPoint2DataFrame as RSDF
import PathOperation.PathGetFiles as PGFiles

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def ShapeMergePoint(_point_path_1, _output_folder, _output_file_name, *other_point_paths_tuple):
    ogr.RegisterAll()
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "UTF8")
    src_rsdf = RSDF.ReadPoint2DataFrame(_point_path_1)
    # 执行下面这句后才会有src_rsdf.feature_columns
    src_df = src_rsdf.ReadShapeFile()
    # 读取源shape文件
    driver = ogr.GetDriverByName('ESRI ShapeFile')
    src_ds = ogr.Open(_point_path_1)
    src_layer = src_ds.GetLayer()
    ref_srs = src_layer.GetSpatialRef()
    geom_tpye = src_layer.GetGeomType()
    # 读取第二个shape文件
    # sec_ds = ogr.Open(_point_path_2)
    # sec_layer = sec_ds.GetLayer()
    # sec_rsdf = RPDF.ReadPoint2DataFrame(_point_path_1)
    # 读取后续的多个shape文件
    other_point_ds = []
    other_point_layers = []
    other_point_rsdf = []
    # 传入的元组不为空
    if other_point_paths_tuple:
        for n in other_point_paths_tuple:
            other_ds = ogr.Open(n)
            other_layer = other_ds.GetLayer()
            other_rsdf = RSDF.ReadPoint2DataFrame(n)
            other_point_layers.append(other_layer)
            other_point_rsdf.append(other_rsdf)
            other_point_ds.append(other_ds)
    # 判断两个shape文件的字段数量是否一致
    phase_license = False
    for rsdf in other_point_rsdf:
        df = rsdf.ReadShapeFile()
        if operator.eq(src_rsdf.feature_columns, rsdf.feature_columns):
            print('初步字段检查一致')
            phase_license = True
        else:
            print('字段检查不一致')
            phase_license = False
            break
    if phase_license:
        # 创建输出shape文件
        output_path = os.path.join(_output_folder, _output_file_name)
        if os.path.exists(output_path):
            shutil.rmtree(output_path)
            print('正在删除已存在ShapeMergePoint文件夹路径')
        os.makedirs(output_path)
        print('已创建ShapeMergePoint文件夹路径')
        output_ds = driver.CreateDataSource(output_path)
        output_layer = output_ds.CreateLayer(_output_file_name, ref_srs, geom_tpye)
        # 写入src Point shape
        temp_feature = src_layer.GetFeature(0)
        for n in range(temp_feature.GetFieldCount()):
            output_field = ogr.FieldDefn(src_rsdf.feature_columns[n], temp_feature.GetFieldType(n))
            output_field.SetWidth(50)
            output_field.SetPrecision(8)
            output_layer.CreateField(output_field)
        src_layer.ResetReading()
        print('正在写入数据......')
        for num in range(src_layer.GetFeatureCount()):
            feature = src_layer.GetFeature(num)
            output_layer.CreateFeature(feature)
            output_feature = output_layer.GetFeature(output_layer.GetFeatureCount() - 1)
            for n in range(temp_feature.GetFieldCount()):
                output_feature.SetField(src_rsdf.feature_columns[n], feature.GetField(n))
            output_layer.SetFeature(output_feature)
        print(f'当前融合要素个数为：{output_layer.GetFeatureCount()}')
        src_ds.Release()
        for other_layer_index, other_layer_item in enumerate(other_point_layers):
            for num in range(other_layer_item.GetFeatureCount()):
                feature = other_layer_item.GetFeature(num)
                output_layer.CreateFeature(feature)
                output_feature = output_layer.GetFeature(output_layer.GetFeatureCount() - 1)
                for n in range(temp_feature.GetFieldCount()):
                    output_feature.SetField(src_rsdf.feature_columns[n], feature.GetField(n))
                output_layer.SetFeature(output_feature)
            other_point_ds[other_layer_index].Release()
            print(f'当前融合要素个数为：{output_layer.GetFeatureCount()}')
    else:
        print('阶段许可为False.')
    return None


if __name__ == '__main__':
    shape_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\1_PointData\12_SeasonalPoint'
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\1_PointData\13_MergeSeasonalPoint'
    shape_paths_list, shape_files_list = PGFiles.PathGetFiles(shape_folder, '.shp')
    dem_list = ['NASA', 'SRTM']
    bins_list = [i * 50 for i in range(1, 5)]
    for dem_index, dem_item in enumerate(dem_list):
        for bin_index, bin_item in enumerate(bins_list):
            # 先得到一年的文件
            files_year_list = []
            for file_index, file_item in enumerate(shape_files_list):
                if dem_item in file_item and f'Bin_{bin_item}' in file_item:
                    files_year_list.append(shape_paths_list[file_index])
            # 对一年的文件按照三个月进行分组
            # 回归日期91天，过境日期为1月后推
            months_list = [i + 2 for i in range(1, 13, 3)]
            months_path_dict = dict()
            for month_item in months_list:
                months_path_dict[month_item] = []
            for file_index, file_item in enumerate(files_year_list):
                file = os.path.split(file_item)[1]
                file_name = os.path.splitext(file)[0]
                month = file_name.rsplit('_', 1)[1][5:]
                for month_index, month_item in enumerate(months_list):
                    if month_index == 0:
                        if int(month) <= month_item:
                            months_path_dict[month_item].append(shape_paths_list[file_index])
                    elif month_index != 0:
                        if months_list[month_index - 1] < int(month) <= month_item:
                            months_path_dict[month_item].append(shape_paths_list[file_index])
            for i in months_list:
                point_path_1 = months_path_dict[i][0]
                output_name = f'{dem_item}_Bin_{bin_item}_Season{i}'
                point_path_tuple = (x for x in months_path_dict[i][1:])
                ShapeMergePoint(point_path_1, output_folder, output_name, *point_path_tuple)
    """
    *************************************************
    融合4年的数据，最后结果是四个等级的数据
    *************************************************
    """
    # point_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\1_PointData\10_FilterOutliersData'
    # output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\1_PointData\11_MergePoint'
    # point_path_list, point_name_list = PGFiles.PathGetFiles(point_folder, '.shp')
    # year_list = [i for i in range(2019, 2023)]
    # dem_list = ['NASA', 'SRTM']
    # bin_list = [i * 50 for i in range(1, 5)]
    # # 列出三个循环条件
    # for dem_item in dem_list:
    #     for bin_item in bin_list:
    #         merge_path_list = []
    #         output_name = None
    #         for year_item in year_list:
    #             # 在路径列表中查找符合结果的
    #             for name_index, name_item in enumerate(point_name_list):
    #                 split_list = name_item.split('_')
    #                 if split_list[0] == dem_item and int(split_list[1]) == year_item and int(split_list[3]) == bin_item:
    #                     merge_path_list.append(point_path_list[name_index])
    #                     output_name = f'{split_list[0]}_Bin_{int(split_list[3])}'
    #         # 开始融合
    #         output_path = os.path.join(output_folder, output_name)
    #         point_path_1 = merge_path_list[0]
    #         point_path_tuple = tuple(merge_path_list[1:])
    #         ShapeMergePoint(point_path_1, output_folder, output_name, *point_path_tuple)
