# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/8 20:00
# @Author : Hexk
# @Descript : 根据excel绘制冰川季节性变化曲线 20231110_1_GlaciersSeasonalChangeCurve
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import matplotlib.pyplot as plt

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    excel_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\Result_ThreeGlacierChange.xlsx"
    group1_df = pd.read_excel(excel_path, sheet_name='Group1')  # 7
    group2_df = pd.read_excel(excel_path, sheet_name='Group2')  # 8
    group3_df = pd.read_excel(excel_path, sheet_name='Group3')  # 4

    month_labels = [i for i in range(1, 13)]
    plt.rc('font', family='Times New Roman', size=22)
    plt.figure(figsize=(10, 8), dpi=300)

    p1 = plt.subplot(311)
    p1.plot(month_labels, list(group1_df.iloc[0])[1:], c='#E53935', marker='o', markersize=5, markeredgewidth=1.5,
            label=group1_df['Glaciers_Name'][0])
    p1.plot(month_labels, list(group1_df.iloc[1])[1:], c='#D81B60', marker='v', markersize=5, markeredgewidth=1.5,
            label=group1_df['Glaciers_Name'][1])
    p1.plot(month_labels, list(group1_df.iloc[2])[1:], c='#8E24AA', marker='^', markersize=5, markeredgewidth=1.5,
            label=group1_df['Glaciers_Name'][2])
    p1.plot(month_labels, list(group1_df.iloc[3])[1:], c='#5E35B1', marker='s', markersize=5, markeredgewidth=1.5,
            label=group1_df['Glaciers_Name'][3])
    p1.plot(month_labels, list(group1_df.iloc[4])[1:], c='#1E88E5', marker='<', markersize=5, markeredgewidth=1.5,
            label=group1_df['Glaciers_Name'][4])
    p1.plot(month_labels, list(group1_df.iloc[5])[1:], c='#039BE5', marker='>', markersize=5, markeredgewidth=1.5,
            label=group1_df['Glaciers_Name'][5])
    p1.plot(month_labels, list(group1_df.iloc[6])[1:], c='#00ACC1', marker='D', markersize=5, markeredgewidth=1.5,
            label=group1_df['Glaciers_Name'][6])
    p1.legend(loc=(1.01, 0), fontsize=12)
    p1.set_xticks(ticks=month_labels)
    p1.text(x=2.5, y=2, s='Group1', ha='center', va='center',
            fontdict={'fontsize': 20, 'color': '#aa00ff', 'weight': 'bold'})
    # p1.title.set_text('Group1')

    p2 = plt.subplot(312)
    p2.plot(month_labels, list(group2_df.iloc[0])[1:], c='#00ACC1', marker='o', markersize=5, markeredgewidth=1.5,
            label=group2_df['Glaciers_Name'][0])
    p2.plot(month_labels, list(group2_df.iloc[1])[1:], c='#00897B', marker='v', markersize=5, markeredgewidth=1.5,
            label=group2_df['Glaciers_Name'][1])
    p2.plot(month_labels, list(group2_df.iloc[2])[1:], c='#43A047', marker='^', markersize=5, markeredgewidth=1.5,
            label=group2_df['Glaciers_Name'][2])
    p2.plot(month_labels, list(group2_df.iloc[3])[1:], c='#7CB342', marker='s', markersize=5, markeredgewidth=1.5,
            label=group2_df['Glaciers_Name'][3])
    p2.plot(month_labels, list(group2_df.iloc[4])[1:], c='#FFEB3B', marker='<', markersize=5, markeredgewidth=1.5,
            label=group2_df['Glaciers_Name'][4])
    p2.plot(month_labels, list(group2_df.iloc[5])[1:], c='#FFB300', marker='>', markersize=5, markeredgewidth=1.5,
            label=group2_df['Glaciers_Name'][5])
    p2.plot(month_labels, list(group2_df.iloc[6])[1:], c='#F57C00', marker='D', markersize=5, markeredgewidth=1.5,
            label=group2_df['Glaciers_Name'][6])
    p2.plot(month_labels, list(group2_df.iloc[7])[1:], c='#F4511E', marker='P', markersize=5, markeredgewidth=1.5,
            label=group2_df['Glaciers_Name'][7])
    p2.legend(loc=(1.01, 0), fontsize=12)
    p2.set_ylabel('Glacier Elevation Relation Change (m)', fontsize=22)
    p2.set_xticks(ticks=month_labels)
    p2.text(x=2.5, y=2, s='Group2', ha='center', va='center',
            fontdict={'fontsize': 20, 'color': '#2979ff', 'weight': 'bold'})
    # p2.title.set_text('Group2')

    p3 = plt.subplot(313)
    p3.plot(month_labels, list(group3_df.iloc[0])[1:], c='#E53935', marker='v', markersize=5, markeredgewidth=1.5,
            label=group3_df['Glaciers_Name'][0])
    p3.plot(month_labels, list(group3_df.iloc[1])[1:], c='#1E88E5', marker='^', markersize=5, markeredgewidth=1.5,
            label=group3_df['Glaciers_Name'][1])
    p3.plot(month_labels, list(group3_df.iloc[2])[1:], c='#43A047', marker='<', markersize=5, markeredgewidth=1.5,
            label=group3_df['Glaciers_Name'][2])
    p3.plot(month_labels, list(group3_df.iloc[3])[1:], c='#FDD835', marker='>', markersize=5, markeredgewidth=1.5,
            label=group3_df['Glaciers_Name'][3])
    p3.legend(loc=(1.01, 0), fontsize=12)
    p3.set_xticks(ticks=month_labels)
    p3.text(x=2.5, y=1, s='Group3', ha='center', va='center',
            fontdict={'fontsize': 20, 'color': '#f57f17', 'weight': 'bold'})
    # p3.title.set_text('Group3')

    plt.xlabel('Month', fontsize=22)
    plt.tight_layout()
    plt.savefig(
        r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\202312107_11_Figure13.jpeg')
    plt.show()
