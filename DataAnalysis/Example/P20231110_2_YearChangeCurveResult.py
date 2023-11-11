# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/10 17:04
# @Author : Hexk
# @Descript :
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import matplotlib.pyplot as plt

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    excel_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\Result_YearChange.xlsx"
    result_df = pd.read_excel(excel_path, sheet_name='Result')
    bin_labels = [i for i in range(1, 17)]
    plt.plot(bin_labels, list(result_df.iloc[0])[1:], c='#1976D2', marker='o', markersize=5, markeredgewidth=1.5,
             label=result_df['Name'][0])
    plt.xticks(ticks=bin_labels)
    plt.show()
