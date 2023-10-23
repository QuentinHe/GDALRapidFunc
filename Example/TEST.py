# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/18 16:31
# @Author : Hexk
# @Descript :
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def func(**kwargs):
    print(len(kwargs))

    for key,value in kwargs.items():
        print(key, value)
    return None


if __name__ == '__main__':
    test_dict = dict(
        Proj_X='path1',
        Proj_Y='path2'
    )
    func(**test_dict)
