# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/9 15:29
# @Author : Hexk
# @Descript : 按照季节月份来进行分级回归预测
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'
