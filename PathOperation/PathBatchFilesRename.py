# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/11 9:48
# @Author : Hexk
# @Descript : 批量修改文件名，并修改文件夹格式

import os
import PathOperation.PathGetFiles as PGF
import shutil


def MoveFile(_file_path, _new_file_folder):
    """
    移动文件到新的文件夹中
    :param _file_path: 文件路径
    :param _new_file_folder: 新的文件夹
    :return: None
    """
    if os.path.exists(_file_path):
        print(f'{_file_path}存在.')
        if os.path.exists(_new_file_folder):
            print(f'{_new_file_folder}已存在')
        else:
            os.makedirs(_new_file_folder)
            print(f'{_new_file_folder}不存在，已创建.')
        shutil.move(_file_path, _new_file_folder)
    else:
        print(f'{_file_path}不存在.')
    return None


def RenameFile(_file_path, _new_file_name):
    """
    重命名新的文件
    :param _file_path: 原文件路径
    :param _new_file_name: 新文件名
    :return: None
    """
    if os.path.exists(_file_path):
        print(f'{_file_path}已存在.')
        _path = os.path.split(_file_path)[0]
        _suffix = os.path.splitext(os.path.split(_file_path)[1])[1]
        _new_file_path = os.path.join(_path, f'{_new_file_name}{_suffix}')
        os.rename(_file_path, _new_file_path)
    else:
        print(f'{_file_path}不存在.')
    return None


def RemoveFolder(_folder):
    shutil.rmtree(_folder)
    return None


if __name__ == '__main__':
    path_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231009\2_PredictData\2_MergeData'
    files_path_list, files_name_list = PGF.PathGetFiles(path_folder, '.tif')
    target_folder_list = [i.split('\\')[6] for i in files_path_list]
    target_folder_prefix = '\\'.join(files_path_list[0].split('\\')[:6])
    for target_folder_index, target_folder_item in enumerate(target_folder_list):
        target_folder_path = os.path.join(target_folder_prefix, target_folder_item)
        MoveFile(files_path_list[target_folder_index], target_folder_path)
        file_path, file_name = PGF.PathGetFiles(target_folder_path, '.tif')
        RenameFile(file_path[0], target_folder_item)
