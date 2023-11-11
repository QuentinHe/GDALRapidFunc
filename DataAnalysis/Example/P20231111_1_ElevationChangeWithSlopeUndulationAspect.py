# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/11 14:18
# @Author : Hexk
# @Descript : 绘制高程变化与坡度、坡向、起伏度、高程之间的变化关系图
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import matplotlib.pyplot as plt

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    excel_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\Result_YearChange.xlsx"
    elevation_df = pd.read_excel(excel_path, sheet_name='Elevation')
    slope_df = pd.read_excel(excel_path, sheet_name='Slope')
    undulation_df = pd.read_excel(excel_path, sheet_name='Undulation')
    aspect_df = pd.read_excel(excel_path, sheet_name='Aspect')

    # plt.style.use('ggplot')
    plt.rc('font', family='Times New Roman', size=12)
    plt.figure(figsize=(8, 6))

    p1 = plt.subplot(221)
    elevation_labels = [5375, 5425, 5475, 5525, 5575, 5625, 5675, 5725, 5775, 5825, 5875, 5925, 5975, 6025, 6075, 6125]
    elevation_data = [i * 20 for i in list(elevation_df.iloc[0])[1:]]
    p1.plot(elevation_labels, elevation_data, c='#146c94', marker='s', markersize=4, markeredgewidth=1)
    p1.set_xlabel('Elevation(m)')
    p1.set_ylabel('Elevation Change(m)')

    p2 = plt.subplot(222)
    slope_labels = [0, 3.37, 5.13, 7.12, 9.70, 13.33, 18.96, 27.44]
    p2.plot(slope_labels, slope_df['Slope'], c='#eb6440', marker='v', markersize=4, markeredgewidth=1)
    p2.set_xlabel('Slope(°)')

    p3 = plt.subplot(223, polar=True)
    aspect_labels = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    aspect_values = aspect_df['Mean'] * 20
    angles = np.linspace(0, 2 * np.pi, len(aspect_values), endpoint=False)
    aspect_values = np.concatenate((aspect_values, [aspect_values[0]]))
    angles = np.concatenate((angles, [angles[0]]))
    aspect_labels = np.concatenate((aspect_labels, [aspect_labels[0]]))
    p3.plot(angles, aspect_values, c='#495c83', marker='o', markersize=4, markeredgewidth=1)
    p3.fill(angles, aspect_values, facecolor='#afd3e2', alpha=0.25)
    p3.set_thetagrids(angles * 180 / np.pi, aspect_labels)
    # 设置极坐标正方向 顺时针和逆时针
    p3.set_theta_direction(-1)
    # 设置极坐标0°位置
    p3.set_theta_zero_location('N')
    p3.set_rlim(-15, 5)
    p3.set_rticks(np.arange(-15, 6, 10))
    p3.set_xlabel('Aspect')

    p4 = plt.subplot(224)
    undulation_labels = [0, 5, 7, 10, 13, 18, 26, 40]
    p4.plot(undulation_labels, undulation_df['Mean'] * 20, c='#005555', marker='^', markersize=4, markeredgewidth=1)
    p4.set_xlabel('Undulation(m)')

    plt.tight_layout()
    plt.show()
