# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/17 上午11:10
# @Author : Hexk
# @Descript : 三子图，对比TS1中的三种情况,四子图
import PathOperation.PathGetFiles as PGF
import PathOperation.PathFilesOperation as PFO
import XGBoostRegression.IntegrationXGBoostRegression as IXGBR
import ReadRasterAndShape.ReadPoint2DataFrame as RSDF
import ReadRasterAndShape.ReadRaster as RR
import numpy as np
import ErrorAnalysis.ErrorAnalysis as EA
import os
import pandas as pd
import matplotlib.pyplot as plt

from RasterAnalysis.RasterClipByShape import RasterClipByShape

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'
if __name__ == '__main__':
    excel_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\Image\TS1_Result.xlsx"
    chart1_df = pd.read_excel(excel_path, sheet_name='TS1_AllRegion')

    plt.rc('font', family='Times New Roman', size=18)
    plt.figure(dpi=300, figsize=(10, 14))

    # list(excel_df)
    chart1_x_list = list(chart1_df)
    chart1_y_list = chart1_df.mean() / 20

    plt.rcParams['ytick.direction'] = 'in'  # 将x的刻度线方向设置向内
    plt.subplot(321)
    chart1_color = ['#78d6c6', '#419197', '#ffbb70', '#ed9455', '#68d2e8', '#03aed2', '#ff5d5d']
    plt.barh(chart1_x_list, width=chart1_y_list, height=0.8, color=chart1_color)
    ax = plt.gca()
    ax.invert_xaxis()
    # plt.xticks(rotation=-90, position=(0, 1), ha='center')
    plt.yticks(ha='center', position=(-0.15, 0), fontsize=20)
    plt.xlabel('Elevation Change Rate (m/a)', fontsize=20)
    for i in range(len(chart1_x_list)):
        plt.text(chart1_y_list[i], chart1_x_list[i], '{:.3f}'.format(chart1_y_list[i]), va="center", ha="right",
                 fontsize=16)
    plt.title("All Region", fontweight='bold')

    chart2_df = pd.read_excel(excel_path, sheet_name='TS1_ClipRegion')
    # plt.rcParams['ytick.direction'] = 'in'  # 将x的刻度线方向设置向内
    plt.subplot(322)
    chart2_x_list = list(chart2_df)
    chart2_y_list = chart2_df.mean() / 20
    chart2_color = ['#78d6c6', '#419197', '#ffbb70', '#ed9455', '#68d2e8', '#03aed2', '#ff5d5d']
    plt.bar(chart2_x_list, chart2_y_list, width=0.8, color=chart2_color)
    plt.plot(chart2_x_list, chart2_y_list, '#3876bf', marker='o', markerfacecolor='white')
    ay = plt.gca()
    ay.invert_yaxis()
    plt.xticks(rotation=-90, position=(0, 0), ha='center', fontsize=20)
    # plt.yticks(ha='center', position=(-0.15, 0))
    plt.ylabel('Elevation Change Rate (m/a)', fontsize=20)
    for i in range(len(chart2_x_list)):
        plt.text(chart2_x_list[i], chart2_y_list[i] + 0.05, '{:.2f}'.format(chart2_y_list[i]), va="center", ha="center",
                 fontsize=16)
    plt.title("Modifier Area", fontweight='bold')

    plt.subplot(312)
    chart4_df_1 = pd.read_excel(excel_path, sheet_name='TS1_AllRegion_ICESat_Predict')
    chart4_df_2 = pd.read_excel(excel_path, sheet_name='TS1_AllRegion_ICESat_True')
    chart4_x_list = list(chart4_df_1)
    predict4_list = chart4_df_1.mean() / 20
    icesat4_list = chart4_df_2.mean() / 20
    chart4_x = np.arange(len(chart4_x_list))
    width = 0.4
    left4_x = chart4_x
    right4_x = chart4_x + width
    plt.bar(left4_x, predict4_list, width=width, color='#ff8787', label='BMRFM')
    plt.bar(right4_x, icesat4_list, width=width, color='#f8c4b4', label='ICESat-2')
    ax = plt.gca()
    ax.invert_yaxis()
    plt.xticks(chart4_x + width / 2, labels=['M5', 'M10', 'P5', 'P10', 'R5', 'R10', 'Normal'],
               fontsize=20)
    plt.ylabel('Elevation Change Rate (m/a)', fontsize=20)
    for i in range(len(chart4_x_list)):
        if i == 3:
            plt.text(right4_x[i], icesat4_list[i] + 0.03, '{:.2f}'.format(icesat4_list[i]), va='bottom', ha='center',
                     fontsize=16)
            plt.text(left4_x[i], predict4_list[i], '{:.2f}'.format(predict4_list[i]), va='bottom', ha='center',
                     fontsize=16)
        else:
            plt.text(left4_x[i], predict4_list[i], '{:.2f}'.format(predict4_list[i]), va='bottom', ha='center',
                     fontsize=16)
            plt.text(right4_x[i], icesat4_list[i], '{:.2f}'.format(icesat4_list[i]), va='bottom', ha='center',
                     fontsize=16)
    plt.legend(loc='upper left', prop={'size': 18})
    plt.title("All Region", fontweight='bold')

    plt.subplot(313)
    chart3_df_1 = pd.read_excel(excel_path, sheet_name='TS1_ICESat_Predict')
    chart3_df_2 = pd.read_excel(excel_path, sheet_name='TS1_ICESat_True')
    chart3_x_list = list(chart3_df_1)
    predict_list = chart3_df_1.mean() / 20
    icesat_list = chart3_df_2.mean() / 20
    chart3_x = np.arange(len(chart3_x_list))
    width = 0.4
    left_x = chart3_x
    right_x = chart3_x + width
    plt.bar(left_x, predict_list, width=width, color='#7469b6', label='BMRFM')
    plt.bar(right_x, icesat_list, width=width, color='#ad88c6', label='ICESat-2')
    ax = plt.gca()
    ax.invert_yaxis()
    plt.xticks(chart3_x + width / 2, labels=['M5', 'M10', 'P5', 'P10', 'R5', 'R10', 'Normal'],
               fontsize=20)
    plt.ylabel('Elevation Change Rate (m/a)', fontsize=20)
    for i in range(len(chart3_x_list)):
        if i == 3:
            plt.text(right_x[i], icesat_list[i] + 0.1, '{:.2f}'.format(icesat_list[i]), va='bottom', ha='center',
                     fontsize=16)
            plt.text(left_x[i], predict_list[i], '{:.2f}'.format(predict_list[i]), va='bottom', ha='center',
                     fontsize=16)
        else:
            plt.text(left_x[i], predict_list[i], '{:.2f}'.format(predict_list[i]), va='bottom', ha='center',
                     fontsize=16)
            plt.text(right_x[i], icesat_list[i], '{:.2f}'.format(icesat_list[i]), va='bottom', ha='center', fontsize=16)
    plt.legend(loc='upper left', prop={'size': 18})
    plt.title("Modifier Area", fontweight='bold')

    plt.tight_layout()
    plt.savefig(
        r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\Image\20240517_3_TS1_BarChart.jpeg')
    plt.show()
