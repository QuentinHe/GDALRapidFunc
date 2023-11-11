# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/13 10:59
# @Author : Hexk
# @Descript : 文件批量压缩，存在一点小问题，压缩会把所有文件夹目录全部压缩。
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import zipfile
import shutil
import PathOperation.PathGetFiles as PGFiles

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def ZipFiles(_files_list, _output_name):
    f = zipfile.ZipFile(_output_name, 'w', zipfile.ZIP_DEFLATED)
    for file in _files_list:
        f.write(file)
    f.close()
    return None


if __name__ == '__main__':
    file_folder = r'E:\Shape_Result'
    shp_path_list, shp_name_list = PGFiles.PathGetFiles(file_folder, '.shp')
    cpg_path_list, cpg_name_list = PGFiles.PathGetFiles(file_folder, '.cpg')
    dbf_path_list, dbf_name_list = PGFiles.PathGetFiles(file_folder, '.dbf')
    prj_path_list, prj_name_list = PGFiles.PathGetFiles(file_folder, '.prj')
    sbn_path_list, sbn_name_list = PGFiles.PathGetFiles(file_folder, '.sbn')
    sbx_path_list, sbx_name_list = PGFiles.PathGetFiles(file_folder, '.sbx')
    output_zip_folder = r'E:\Shape_Result'
    # output_zip_path = os.path.join(output_zip_folder, 'result')
    # shutil.make_archive(output_zip_path, 'zip', file_folder)
    for shp_name_index, shp_name_item in enumerate(shp_name_list):
        temp_files = [shp_path_list[shp_name_index]]
        cpg_index = cpg_name_list.index(shp_name_item)
        dbf_index = dbf_name_list.index(shp_name_item)
        prj_index = prj_name_list.index(shp_name_item)
        sbn_index = sbn_name_list.index(shp_name_item)
        sbx_index = sbx_name_list.index(shp_name_item)
        temp_files.append(cpg_path_list[cpg_index])
        temp_files.append(dbf_path_list[dbf_index])
        temp_files.append(prj_path_list[prj_index])
        temp_files.append(sbn_path_list[sbn_index])
        temp_files.append(sbx_path_list[sbx_index])
        output_zip_path = os.path.join(output_zip_folder, f'{shp_name_item}.zip')
        ZipFiles(temp_files, output_zip_path)

