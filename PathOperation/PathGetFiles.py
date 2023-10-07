# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/9/19 14:55
# @Author : Hexk
# @Descript : 获取文件夹下指定文件的绝对路径和文件名称
import os


def PathGetFiles(_path, _file_suffix):
    """
    快速得到指定文件夹下的所有符合后缀条件的文件，并返回成绝对路径和文件名两个list
    :param _path: 指定路径
    :param _file_suffix: 后缀 eg: '.tif'
    :return: 绝对路径list， 文件名list
    """
    _path_list = []
    _files_list = []
    for root, dirs, files in os.walk(_path):
        for file in files:
            if os.path.splitext(file)[1] == _file_suffix:
                _path_list.append(os.path.join(root, file))
                _files_list.append(os.path.splitext(file)[0])
    return _path_list, _files_list

