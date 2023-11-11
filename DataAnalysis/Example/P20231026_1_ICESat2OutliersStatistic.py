# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/26 11:23
# @Author : Hexk
# @Descript : 绘制箱线图，并且统计筛选出去点的数量
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import PathOperation.PathGetFiles as PGFiles
import ReadRasterAndShape.ReadPoint2DataFrame as RPDF
import DataAnalysis.Drawing as Drawing

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    shape_point_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\1_PointData\9_AddDelta_EleField'
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\2_Method&Data\PointOutputFolder\SRTM_Point'
    output_pic_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\2_Method&Data'
    shape_path_list, shape_name_list = PGFiles.PathGetFiles(shape_point_folder, '.shp')
    srtm_path_list, srtm_name_list = [], []
    bin_list = [i * 50 for i in range(1, 5)]
    for index, item in enumerate(shape_name_list):
        if 'SRTM' in item:
            srtm_name_list.append(item)
            srtm_path_list.append(shape_path_list[index])
    """
    下面是一张一张输出
    """
    # for index, item in enumerate(srtm_path_list):
    #     input_rsdf = RPDF.ReadPoint2DataFrame(item)
    #     input_df = input_rsdf.ReadShapeFile()
    #     filter_list = []
    #     for bin_item in bin_list:
    #         boxplot_data_dict = dict()
    #         for i in np.arange(1, int(max(input_df[f'Bin_{bin_item}'])) + 1):
    #             boxplot_data_dict[i] = []
    #         for i, j in enumerate(input_df[f'Bin_{bin_item}']):
    #             boxplot_data_dict[j].append(input_df['Delta_Ele'][i])
    #         # 绘制箱线图
    #         print('正在绘制箱线图...')
    #         boxplot = Drawing.DrawingBoxs(boxplot_data_dict.aspect_values(), boxplot_data_dict.keys(), 'Elevation Bin',
    #                                       'Elevation Anomaly (m)',
    #                                       _title=f'Elevation Interval {bin_item}m')
    #         boxs_num, boxs_max, boxs_min, fliers_nums = Drawing.DrawingBoxsFilters(boxplot)
    #         print(f'箱子数量为:{boxs_num}.')
    #         for i in np.arange(int(boxs_num)):
    #             print(f'箱子{i + 1} --- Max:{boxs_max[i]}; Min:{boxs_min[i]}')
    #         filter_list.append(fliers_nums)
    #     filter_csv_path = os.path.join(output_folder, f'{srtm_name_list[index]}_Filters.csv')
    #     filter_df = pd.DataFrame([filter_list], columns=bin_list)
    #     filter_df.to_csv(filter_csv_path)
    """
    还是一张一张输出，不过是四年分四次，改变一下颜色
    """
    markerfacecolor_list = ['#1c6cd0', '#f45050', '#1e9d90', '#e9b824']
    input_rsdf = RPDF.ReadPoint2DataFrame(srtm_path_list[3])
    input_df = input_rsdf.ReadShapeFile()
    filter_list = []
    for bin_item in bin_list:
        boxplot_data_dict = dict()
        for i in np.arange(1, int(max(input_df[f'Bin_{bin_item}'])) + 1):
            boxplot_data_dict[i] = []
        for i, j in enumerate(input_df[f'Bin_{bin_item}']):
            boxplot_data_dict[j].append(input_df['Delta_Ele'][i])
        print('正在绘制箱线图...')
        pic_path = os.path.join(output_pic_folder, f'20231026_2_SRTM2022_Boxplot_Bin{bin_item}.png')
        boxplot = Drawing.DrawingBoxs(boxplot_data_dict.values(), boxplot_data_dict.keys(), 'Elevation Bin',
                                      'Elevation Anomaly (m)',
                                      _title=f'Elevation Interval {bin_item}m',
                                      _save_path=pic_path)
