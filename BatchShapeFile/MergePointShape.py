# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/9/3 11:06
# @Author : Hexk
"""
NB：
    该文件的目的是将所有的Shape文件合并成1个，并新增字段“Years” “Months”用以表征ICESat2文件的生成日期。方便进行后续的日期分析。
    文件组成格式最好是：
    1.ATL06
        2.2019
        2.2020
            3.Shape_Folder
                4.xxx.shp
                4.xxx.dbf
                4.xxx.shx
                4.xxx.prj
    给定文件夹路径，自动读取处理，输出路径给到ATL06同级文件夹，“ATL06_Batch_Merge”.

NB2:
    该文件夹路径下不能存在任何除了需要处理的shp文件之外的shp，会导致读取 self.shape_absolute_path_list 出现多余shp，导致日期获取失败。
    同时创建父路径下ATL06_Merge那个地方有点问题，已经添加书签，但是结果都成功出来，我也懒得改了。
    😋
"""
import numpy as np
import pandas as pd
import os
from osgeo import gdal, ogr
import ReadRasterAndShape.ReadShape2DataFrame as rsdf


class BatchMergePointShape:
    def __init__(self, input_path):
        self.input_path = input_path
        self.output_path = input_path
        # shape 文件的绝对路径
        self.shape_absolute_path_list = []
        # 年 和 日期
        # self.files_dict = dict()
        # pass

    def BuildFilesPath(self):
        """
        获取所有的shape文件绝对路径，并分类成年和日期dict格式
        :return: [文件绝对路径]， {年:日期}
        """
        dir_path = os.walk(self.input_path)
        files_years = []
        for path, dir_lst, file_lst in dir_path:
            for file_name in file_lst:
                # 判断是否为shp文件
                if os.path.splitext(file_name)[-1] == '.shp':
                    # 将shp绝对路径添加进列表
                    self.shape_absolute_path_list.append(os.path.join(path, file_name))
                    # # 得到文件名和后缀
                    # name, suffix = os.path.splitext(file_name)
                    # name_date = name.split('_')[2][:8]
                    # # 判断文件日期
                    # if name_date[:4] not in files_years:
                    #     files_years.append(name_date[:4])
                    # if name_date[:4] in self.files_dict.keys():
                    #     self.files_dict[name_date[:4]].append(name_date[4:8])
                    # else:
                    #     self.files_dict[name_date[:4]] = [name_date[4:8]]
        return self.shape_absolute_path_list

    def MergeShapeFiles(self):
        gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
        gdal.SetConfigOption("SHAPE_ENCODING", "UTF-8")
        ogr.RegisterAll()
        feature_df = None
        year_sign = None
        shape_file_df_drop = None
        for path in self.shape_absolute_path_list:
            print(path)
            shape_file = rsdf.ReadPoint2DataFrame(path)
            shape_file_df = shape_file.ReadShapeFile()
            if 'Along_Trac' in shape_file_df:
                shape_file_df = shape_file_df.drop(columns=['Along_Trac'])
                if 'Beam' in shape_file_df:
                    shape_file_df_drop = shape_file_df.drop(columns=['Beam'])
            shape_file_df_drop = rsdf.DataFrameFormatConvert(shape_file_df_drop, int_field=['Segment_ID'],
                                                             float_field=['Latitudes', 'Longitudes', 'H_Li', 'Delta_H',
                                                                          'DEM_H'])
            # 分离出文件名和后缀，获取年月日
            print(f'当前文件路径为：{path}')
            year = os.path.splitext(path.split('\\')[-1])[0].split('_')[2][:4]
            date = os.path.splitext(path.split('\\')[-1])[0].split('_')[2][4:8]
            print(year, date, os.path.splitext(path.split('\\')[-1])[0])
            shape_file_df_drop['Year'] = year
            shape_file_df_drop['Date'] = date
            if year_sign is None:
                year_sign = year
                feature_df = shape_file_df_drop
            elif year_sign == year:
                print('年份相等.')
                print(path, self.shape_absolute_path_list[-1])
                feature_df = pd.concat([feature_df, shape_file_df_drop])
                if path == self.shape_absolute_path_list[-1]:
                    print('当前循环至最后，开始输出...')
                    rsdf.DataFrameWriteShape(feature_df, f'{self.output_path}\\ATL06_Merge', f'{year_sign}')
            else:
                # 某一年的已经读取完毕，开始写入
                print(f'上一个文件标记年份{year_sign}与本文件年份{year}不符合，开始写入{year_sign}年...')
                # 路径设定存在问题。需要设定为父文件夹创建ATL06_Merge
                rsdf.DataFrameWriteShape(feature_df, f'{os.path.join(self.output_path, "..", "ATL06_Merge")}',
                                         f'{year_sign}')
                year_sign = year
                feature_df = shape_file_df_drop
            print(f'当前已经合并点共{len(feature_df)}, 年份为{year_sign}')


if __name__ == '__main__':
    bmps = BatchMergePointShape(r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\ICESat2\4_Shape_Data\ATL06')
    shape_path_list = bmps.BuildFilesPath()
    bmps.MergeShapeFiles()
    # print(shape_path_list[-1])
