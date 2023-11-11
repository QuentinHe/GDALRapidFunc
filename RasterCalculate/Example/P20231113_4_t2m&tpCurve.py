# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/13 14:01
# @Author : Hexk
# @Descript :
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'
