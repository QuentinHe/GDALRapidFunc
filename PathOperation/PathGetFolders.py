# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/12 9:27
# @Author : Hexk
# @Descript : 获取指定folder下的所有folder，不包含子folder

import os


def PathGetFolders(_path_folder):
    """
    获取指定folder下的所有folder，不包含子folder
    :param _path_folder: 文件夹路径
    :return: 绝对文件夹路径list，文件夹名称list，不包含下一级子文件夹
    """
    _name_list = os.listdir(_path_folder)
    _folder_path_list = []
    _folder_name_list = []
    for index, item in enumerate(_name_list):
        # 这里不能采用remove移除，会导致指针错误遗漏一个元素
        if os.path.isdir(os.path.join(_path_folder, item)):
            _folder_name_list.append(item)
            _folder_path_list.append(os.path.join(_path_folder, item))
        else:
            continue
    return _folder_path_list, _folder_name_list


if __name__ == '__main__':
    path_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231009\0_BasePoint\NASA_2019_Bin_50'
    # path_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231009\0_BasePoint'
    folder_path_list, folder_name_list = PathGetFolders(path_folder)
