# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/12 9:03
# @Author : Hexk
# @Descript : 统计shp point文件中点的个数，并输出成CSV
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import PathOperation.PathGetFiles as PGFile
import PathOperation.PathGetFolders as PGFolder
import ReadRasterAndShape.ReadPoint2DataFrame as RSDF

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def ShapePointCountStatisticByDF(_shape_point_path):
    """
    通过DF获取，在DF不存在时候使用Layer方法，理论上Layer方法更快
    :param _shape_point_path: shape输入路径
    :return: point个数
    """
    shape_point_rsdf = RSDF.ReadPoint2DataFrame(_shape_point_path)
    shape_df = shape_point_rsdf.ReadShapeFile()
    return len(shape_df)


def ShapePointCountStatisticByLayer(_shape_point_path):
    """
    Recommend！！ 优先采用该方法！！
    :param _shape_point_path: shape输入路径
    :return: point个数
    """
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "UTF-8")
    ogr.RegisterAll()
    ds = ogr.Open(_shape_point_path)
    ds.GetLayerCount()
    layer = ds.GetLayerByIndex(0)
    layer.ResetReading()
    feature_num = layer.GetFeatureCount(0)
    del ds
    return feature_num


def ShapeFieldClassifyCountStatistic(_shape_path, _classify_field):
    """
    根据分类字段统计各类中要素数量
    :param _shape_path: shape文件路径
    :param _classify_field: 分类字段
    :return: 等级字段数量列表
    """
    point_rsdf = RSDF.ReadPoint2DataFrame(_shape_path)
    point_df = point_rsdf.ReadShapeFile()
    level_list = [0 for _i in range(int(np.max(point_df[_classify_field])))]
    for _i in point_df[_classify_field]:
        level_list[int(_i) - 1] += 1
    return level_list


def ShapeCountStatisticByDate(_shape_path, _date_field, _output_csv_path=None):
    """
    统计字段'Date=0526'这种格式的point，每个月有多少个点，并输出成csv
    :param _shape_path:
    :param _date_field:
    :param _output_csv_path:
    :return:
    """
    # 仅能统计类似于 ‘0526’这种格式
    shape_rsdf = RSDF.ReadPoint2DataFrame(_shape_path)
    shape_df = shape_rsdf.ReadShapeFile()
    month_dict = dict()
    for i in range(1, 13):
        month_dict[i] = 0
    for row in shape_df[_date_field].itertuples():
        date = getattr(row, _date_field[0])[0:2]
        month_dict[int(date)] += 1
    month_count_df = pd.DataFrame(month_dict, index=[0])
    print(month_count_df)
    if _output_csv_path:
        month_count_df.to_csv(_output_csv_path)
    return None


if __name__ == '__main__':
    shape_point_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231009\0_BasePoint'
    main_folder_paths_list, main_folder_name_list = PGFolder.PathGetFolders(shape_point_folder)
    sec_folder_paths_dict = dict()
    sec_folder_name_dict = dict()
    for index, item in enumerate(main_folder_name_list):
        sec_folder_paths_dict[item], sec_folder_name_dict[item] = PGFolder.PathGetFolders(main_folder_paths_list[index])
    for main_folder_index, main_folder_item in enumerate(main_folder_name_list):
        month_list = []
        point_count_list = []
        output_df = pd.DataFrame()
        for sec_folder_item in sec_folder_paths_dict[main_folder_item]:
            shape_paths_list, shape_files_list = PGFile.PathGetFiles(sec_folder_item, '.shp')
            for index, item in enumerate(shape_files_list):
                month = item.rsplit('_', 1)[1][5:]
                month_list.append(month)
            for i in shape_paths_list:
                point_count = ShapePointCountStatisticByLayer(i)
                point_count_list.append(point_count)
        csv_dict = dict(
            Month=month_list,
            Point_Count=point_count_list
        )
        csv_df = pd.DataFrame(csv_dict)
        output_df = pd.concat([output_df, csv_df], axis=1)
        output_csv_path = os.path.join(main_folder_paths_list[main_folder_index],
                                       main_folder_paths_list[main_folder_index].rsplit('\\', 1)[1] + '_Counts.csv')
        output_df.to_csv(output_csv_path)
        print(main_folder_paths_list[main_folder_index].rsplit('\\', 1)[1] + '写入完成.')
