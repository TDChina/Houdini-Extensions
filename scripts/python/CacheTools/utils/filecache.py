# -*- coding: UTF-8 -*-
# Copyright (c) 2018 ChuckBiBi
import os
import re
import shutil
import json
import hou
from CacheTools.config import generate_path
reload(generate_path)


path_hip = hou.hipFile.path()
path_dir = os.path.dirname(path_hip)


def check_path_format(path):

    path_dir = os.path.dirname(path)
    path_drive = os.path.splitdrive(path)[0]

    # 路径不在hip文件的根目录下
    if path_dir not in path_dir:
        hou.ui.setStatusMessage(
            "You current cache path is not in " + path_dir
        )

    # 路径缺少盘符信息
    if path_drive:
        return

    if hou.ui.displayMessage(
        "The 'Geometry File' format error,please check it!",
        details=(
            "The path format error is caused by not writing the correct 'Drive' information. \n"
            "like:'/geo/temp/...'. \n"
            "If you have 'Save to Disk' before 'Open Path',"
            "You may output cache to C:\."
        )
    ) == 0:
        exit()


def get_list_range(ls_files):

    # 得到列表中文件名中的的序列范围
    ls_range = []
    ls_range_frame = "None"

    if ls_files:
        for i in ls_files:
            temp = i.split(".")
            for j in temp:
                if j.isdigit():
                    ls_range.append(j)

        ls_range_start = ls_range[0]
        ls_range_end = ls_range[-1]
        ls_range_frame = "".join([ls_range_start, " ---- ", ls_range_end])

    return ls_range_frame


def get_size_format(size_in_bytes):

    # 将给定的bytes格式转换成以下几种格式：bytes/KB/MB/GB
    for (cutoff, label) in [(1024 * 1024 * 1024, "GB"),
                            (1024 * 1024, "MB"),
                            (1024, "KB"),
                            ]:
        if size_in_bytes >= cutoff:
            return "%.1f %s" % (size_in_bytes * 1.0 / cutoff, label)

    if size_in_bytes == 1:
        return "1 byte"

    else:
        bytes = "%.1f" % (size_in_bytes or 0,)
        return (bytes[:-2] if bytes.endswith('.0') else bytes) + " bytes"


def get_lsit_size(ls_files):

    # 得到列表中所有文件的总内存大小
    ls_files_size = 0

    if ls_files:
        for i in ls_files:
            file_size = os.path.getsize(i)
            ls_files_size += file_size

    ls_size = get_size_format(ls_files_size)

    return ls_size


def generate_files_list(path_file, part=1):

    # 根据缓存文件的路径命名格式将所有缓存文件生成一个列表
    path_file_name = path_file.split(".")[0]
    path_dir = os.path.dirname(path_file_name)
    path_rule = path_file_name.split("/")[-1]
    path_files = []

    if os.path.exists(path_dir):
        path_dir_files = os.listdir(path_dir)
        for i in path_dir_files:
            if part:
                if path_rule in i:
                    path = "".join([path_dir, "/", i])
                    path_files.append(path)

            else:
                path = "".join([path_dir, "/", i])
                path_files.append(path)

    return path_files


# ====================
# interface function

def open_path(node):

    # 打开Geometry file下的路径
    generate_path.check_hip_freshness()
    path_parm = node.evalParm("file")
    path_dir = os.path.dirname(path_parm)
    check_path_format(path_parm)

    if not os.path.exists(path_dir):
        if hou.ui.displayMessage(
            "Geometry file path cannot be empty! Do you want to create one?",
            buttons=(" Yes ", " Next Time ")
        ) == 0:
            os.makedirs(path_dir)

        else:
            exit()

    os.startfile(path_dir)


def destroy_geo(node):

    # 生成Geomerty file的文件列表和同层级目录下所有的文件列表
    generate_path.check_hip_freshness()
    path_parm = node.evalParm("file")
    path_parm_dir = os.path.dirname(path_parm)
    check_path_format(path_parm)
    path_files = generate_files_list(path_parm)
    path_dir_files = generate_files_list(path_parm, part=0)

    # 获取缓存路径下文件的信息并反馈信息
    all_amount = len(path_dir_files)
    all_size = get_lsit_size(path_dir_files)
    ls_amount = len(path_files)
    ls_size = get_lsit_size(path_files)
    ls_range = get_list_range(path_files)
    file_name = path_parm.split("/")[-1]
    name = file_name.split("_")[0]
    temp = re.findall(r"v\d\d\d", file_name)
    version = "none" if not temp else temp[0]

    user = hou.ui.displayMessage(
        "Destroy all cache in the Geometry file folder? \n"
        "or only destroy Geometry file cache?",
        details=(
            "========== Files in folders.: \n"
            "amount: %d \n"
            "szie: %s \n\n"
            "========== Geometry files: \n"
            "amount: %d \n"
            "szie: %s \n"
            "name: %s \n"
            "version: %s \n"
            "frame_span: %s \n"
            % (all_amount, all_size, ls_amount, ls_size, name, version, ls_range)
        ),
        buttons=(" All ", " Only ", " Cancel ")
    )

    if user == 0:
        if not os.path.exists(path_parm_dir):
            if hou.ui.displayMessage(
                "Folder does not exist!!!"
            ) == 0:
                exit()
        else:
            shutil.rmtree(path_parm_dir)
            hou.ui.setStatusMessage(
                "Folder destroy done!"
            )

    elif user == 1:
        if path_files == []:
            if hou.ui.displayMessage(
                "File does not exist!!!"
            ) == 0:
                exit()
        else:
            for i in path_files:
                os.remove(i)
                hou.ui.setStatusMessage(
                    "Current cache destroy done!"
                )

    elif user == 2:
        exit()


if __name__ is "__main__":
    generate_files_list()
