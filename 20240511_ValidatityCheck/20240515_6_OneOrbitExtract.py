# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/15 下午3:26
# @Author : Hexk
# @Descript :
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadRaster as RR
import ReadRasterAndShape.ReadPoint2DataFrame as RPDF
import PathOperation.PathGetFiles as PGF
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'
if __name__ == '__main__':
    raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\20240518_1_OneOrbitProfile'
    raster_list, raster_name_list = PGF.PathGetFiles(raster_folder, '.tif')
    point_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\23_OneOrbit\20240515_1_OneOrbit\20240515_1_OneOrbit.shp"

    point_rpdf = RPDF.ReadPoint2DataFrame(point_path)
    point_df = point_rpdf.ReadShapeFile()
    for index, item in enumerate(raster_name_list):
        temp_raster_rr = RR.ReadRaster(raster_list[index])
        temp_raster_data = temp_raster_rr.ReadRasterFile()
        point_row, point_column = point_rpdf.PointMatchRasterRowColumn(temp_raster_rr.raster_ds_geotrans)
        point_value_list = RR.SearchRasterRowColumnData(point_row, point_column, temp_raster_data)
        temp_name = f'V_{item.split("_")[2]}_{item.split("_")[3]}'
        temp_df = pd.DataFrame(point_value_list, columns=[temp_name])
        point_df = pd.concat([point_df, temp_df], axis=1)

    latitudes_list = point_df['Latitudes']
    delta_h_list = point_df['H_Li'] - point_df['V_SRTM_DEM']
    b50_m5_list = point_df['V_B50_M5']
    b50_m10_list = point_df['V_B50_M10']
    b50_p5_list = point_df['V_B50_P5']
    b50_p10_list = point_df['V_B50_P10']
    b50_r5_list = point_df['V_B50_R5']
    b50_r10_list = point_df['V_B50_R10']
    predict_list = point_df['V_B50_Predict']

    # 总共8条线，画4个子图
    plt.rc('font', family='Times New Roman', size=20)
    fig, axes = plt.subplots(2, 2, dpi=300, figsize=(12, 8))

    plt.subplot(221)
    plt.plot(latitudes_list, delta_h_list, linewidth=3, alpha=0.6, c='#008B8B', label='ICESat-2')
    plt.plot(latitudes_list, predict_list, linewidth=2, linestyle='solid', c='#DC143C', label='Normal')
    ax = plt.gca()
    ax.axes.xaxis.set_ticklabels([])
    plt.legend(loc='upper right', frameon=False, prop={'weight': 'bold'})

    plt.subplot(222)
    plt.plot(latitudes_list, delta_h_list, linewidth=3, alpha=0.6, c='#008B8B')
    plt.plot(latitudes_list, b50_m5_list, linewidth=2, alpha=0.8, linestyle='solid', c='#cd6688', label='M5')
    plt.plot(latitudes_list, b50_m10_list, linewidth=2, linestyle='solid', c='#7a316f', label='M10')
    ax = plt.gca()
    ax.axes.xaxis.set_ticklabels([])  # 只显示刻度线
    plt.legend(loc='upper right', frameon=False, prop={'weight': 'bold'})

    plt.subplot(223)
    plt.plot(latitudes_list, delta_h_list, linewidth=3, alpha=0.6, c='#008B8B')
    plt.plot(latitudes_list, b50_p5_list, linewidth=2, linestyle='solid', c='#ffaf45', label='P5')
    plt.plot(latitudes_list, b50_p10_list, linewidth=2, linestyle='solid', c='#fb6d48', label='P10')
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))
    plt.legend(loc='upper right', frameon=False, prop={'weight': 'bold'})

    plt.subplot(224)
    plt.plot(latitudes_list, delta_h_list, linewidth=3, alpha=0.6, c='#008B8B')
    plt.plot(latitudes_list, b50_r5_list, linewidth=2, linestyle='solid', c='#6c5b7b', label='R5')
    plt.plot(latitudes_list, b50_r10_list, linewidth=2, alpha=0.8, linestyle='solid', c='#ff7e67', label='R10')
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))
    plt.legend(loc='upper right', frameon=False, prop={'weight': 'bold'})

    fig.text(0.5, 0.005, 'Latitudes (°)', fontsize=24, fontweight='bold', ha='center')
    fig.text(0.001, 0.5, 'Glacier Elevation Change (m)', fontsize=24, fontweight='bold', va='center',
             rotation='vertical')
    # plt.xticks(ticks=month_labels)
    # plt.xlabel('Latitudes (°)', fontsize=16)
    # plt.ylabel('Glacier Elevation Change (m)', fontsize=16)
    # plt.legend(prop={'size': 12})
    plt.tight_layout()
    plt.savefig(r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\Image\20240515_1_OrbitProfile.jpeg")
    plt.show()


    # 计算一下平均移动的距离
    print(f"ICEsat2 Mean:{np.mean(delta_h_list)}")
    print(f"Predict Mean:{np.mean(predict_list)}")
    print(f"M5 Mean:{np.mean(b50_m5_list)}")
    print(f"M10 Mean:{np.mean(b50_m10_list)}")
    print(f"P5 Mean:{np.mean(b50_p5_list)}")
    print(f"P10 Mean:{np.mean(b50_p10_list)}")
    print(f"R5 Mean:{np.mean(b50_r5_list)}")
    print(f"R10 Mean:{np.mean(b50_r10_list)}")
