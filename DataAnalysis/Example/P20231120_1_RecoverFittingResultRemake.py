# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/10 16:28
# @Author : Hexk
# @Descript : 20231120_1_RecoverFitting_Remake
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    excel_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\Result_WholeGlaicerMonthlyChange.xlsm"
    result_df = pd.read_excel(excel_path, sheet_name='Modify')
    month_labels = [i for i in range(1, 13)]
    plt.rc('font', family='Times New Roman', size=14)
    plt.figure(dpi=300)
    plt.plot(month_labels, list(result_df.iloc[0])[1:], c='#ff7f0e', linestyle='--', marker='o', markersize=5,
             markeredgewidth=1.5,
             label=result_df['Name'][0])
    plt.plot(month_labels, list(result_df.iloc[1])[1:], c='#7752fe', linestyle='-.', marker='s', markersize=5,
             markeredgewidth=1.5,
             label=result_df['Name'][1])
    # 平滑曲线3
    m = make_interp_spline(month_labels, list(result_df.iloc[2])[1:])
    xs = np.linspace(0.7, 12.3, 600)
    ys = m(xs)
    plt.plot(xs, ys, c='#00ccff', linewidth=2.5, label=result_df['Name'][2])
    plt.text(x=11, y=0.75, s='A=1.1', ha='center', va='center',
             fontdict={'fontsize': 22, 'color': '#c70039'})
    plt.xticks(ticks=month_labels, fontsize=22)
    plt.yticks(fontsize=22)
    plt.xlabel('Month', fontsize=22)
    plt.ylabel('Glacier Elevation Change(m)', fontsize=22)
    plt.legend(prop={'size': 14}, frameon=False)
    plt.tight_layout()
    plt.savefig(
        r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\2_Method&Data\20231207_1_RecoverFitting.jpeg')
    plt.show()
