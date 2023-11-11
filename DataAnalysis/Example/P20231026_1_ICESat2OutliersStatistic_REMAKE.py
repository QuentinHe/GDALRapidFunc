# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/14 15:19
# @Author : Hexk
# @Descript :
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import PathOperation.PathGetFiles as PGFiles
import ReadRasterAndShape.ReadPoint2DataFrame as RPDF
import DataAnalysis.Drawing as Drawing
import matplotlib.pyplot as plt

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

    plt.rc('font', family='Times New Roman', size=12)
    plt.grid(True)
    fig = plt.figure(figsize=(14, 6))
    """
    还是一张一张输出，不过是四年分四次，改变一下颜色
    """
    for shape_index, shape_item in enumerate(srtm_path_list):
        if shape_index == 2:
            break
        else:
            input_rsdf = RPDF.ReadPoint2DataFrame(shape_item)
            input_df = input_rsdf.ReadShapeFile()
            filter_list = []
            markerfacecolor_list = ['#1c6cd0', '#f45050', '#1e9d90', '#e9b824']

            for bin_item in bin_list:
                boxplot_data_dict = dict()
                for i in np.arange(1, int(max(input_df[f'Bin_{bin_item}'])) + 1):
                    boxplot_data_dict[i] = []
                for i, j in enumerate(input_df[f'Bin_{bin_item}']):
                    boxplot_data_dict[j].append(input_df['Delta_Ele'][i])
                print('正在绘制箱线图...')
                # boxplot = Drawing.DrawingBoxs(boxplot_data_dict.values(), boxplot_data_dict.keys(), 'Elevation Bin',
                #                               'Elevation Anomaly (m)',
                #                               _title=f'Elevation Interval {bin_item}m',
                #                               _save_path=pic_path)
                sub_num = f'24{int(shape_index * 4 + bin_item / 50)}'
                temp_p = fig.add_subplot(int(sub_num))
                temp_p.boxplot(boxplot_data_dict.values(),
                               medianprops={'color': 'red', 'linewidth': '1'},
                               meanline=True,
                               showmeans=True,
                               meanprops={'color': 'blue', 'ls': '--', 'linewidth': '1'},
                               flierprops={"marker": "o", "markerfacecolor": markerfacecolor_list[shape_index],
                                           "markersize": 6,
                                           "markeredgecolor": 'gray'},
                               labels=boxplot_data_dict.keys())
                # plt.title(_title, fontsize=16)
                # plt.xticks(fontsize=12)
                # plt.yticks(fontsize=12)
                # plt.xlabel(_x_axis_label, fontsize=16)
                # plt.ylabel(_y_axis_label, fontsize=16)
                # outliers_num = np.sum([item.get_ydata() for item in bp['fliers']])
                # plt.text(np.max(_x_data), np.min(_y_data), f'Outliers:{outliers_num}', fontsize=16)
    plt.tight_layout()
    plt.show()
    """
    改成4*4的一起绘制，然后输出
    """
