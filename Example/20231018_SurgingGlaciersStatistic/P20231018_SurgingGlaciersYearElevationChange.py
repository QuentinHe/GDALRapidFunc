# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/18 10:38
# @Author : Hexk
# @Descript : 读取两个Raster,一个是变化，一个是ID标识，根据ID标识存入像元，并统计Total和Annual高程变化
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    pass