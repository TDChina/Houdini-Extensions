# -*- coding: UTF-8 -*-
# Copyright (c) 2018 ChuckBiBi
import hou
import os
import shutil
from CacheTools.config import path


def check_has_unsaved():

    # 当前hip可能是新建的场景还未保存过
    if hou.hipFile.hasUnsavedChanges():
        if hou.ui.displayMessage(
            "The current hip never saved ,you needs to be saved.",
            buttons=(" Save ", " Next Time ")
        ) == 0:
            path_hip = hou.ui.selectFile(
                # start_directory = path.set_project_path(), TODO:
                start_directory = "E:/Temporary/",
                title = "Save As",
                file_type = hou.fileType.Any,
                pattern = "*.hip",
                default_value = "test_v001.hip",
                chooser_mode = hou.fileChooserMode.Write
            )
            hou.hipFile.save(path_hip)
            
        else:
            exit()


def check_path_format(path):

    # 参数中的路径缺少盘符信息
    path_parm = path
    path_parm_dir = os.path.dirname(path_parm)
    path_drive = path_parm.split("/")[0]

    if path_drive == "":
        if hou.ui.displayMessage(
            "The 'Geometry File' format error,please check it!",
            details=(
                "The path format error is caused by not writing the correct 'Driver' information. \n"
                "like:'/geo/temp/...'. \n"
                "If you have 'Save to Disk' before 'Open Path',"
                "You may output cache to C:\."
            )
        ) == 0:
            exit()

    # 参数中的路径不在hip文件的目录下
    path_hip = hou.hipFile.path()
    path_hip_dir = os.path.dirname(path_hip)

    if path_hip_dir not in path_parm_dir:
        hou.ui.setStatusMessage(
            "You current cache path is not in /.hip."
        )


def get_list_amount(ls):

    # 得到列表中的元素的数量
    ls_count = 0

    if ls != []:
        for i in range(len(ls)):
            ls_count += 1

    return ls_count


def get_list_range(ls):

    # 得到列表中元素的序列范围
    ls_range = []
    ls_range_frame = "None"

    if ls != []:
        for i in range(len(ls)):
            temp = ls[i].split(".")
            for j in range(len(temp)):
                if temp[j].isdigit():
                    ls_range.append(temp[j])

        ls_range_start = ls_range[0]
        ls_range_end = ls_range[-1]
        ls_range_frame = "".join([ls_range_start, " ---- ", ls_range_end])

    return ls_range_frame


def getSizeInNiceString(sizeInBytes):

    # Convert the given byteCount into a string like: 9.9bytes/KB/MB/GB
    for (cutoff, label) in [(1024 * 1024 * 1024, "GB"),
                            (1024 * 1024, "MB"),
                            (1024, "KB"),
                            ]:
        if sizeInBytes >= cutoff:
            return "%.1f %s" % (sizeInBytes * 1.0 / cutoff, label)

    if sizeInBytes == 1:
        return "1 byte"

    else:
        bytes = "%.1f" % (sizeInBytes or 0,)
        return (bytes[:-2] if bytes.endswith('.0') else bytes) + " bytes"


def get_lsit_size(ls):

    # 得到列表中所有文件的总内存大小
    ls_size = 0

    if ls != []:
        for i in range(len(ls)):
            size = os.path.getsize(ls[i])
            ls_size += size

    ls_size = getSizeInNiceString(ls_size)

    return ls_size


def generate_files_list(path, region=0):

    # 根据缓存的命名格式将所有缓存文件生成一个列表
    path_file = path.split(".")
    path_file_os = path_file[0]
    path_dir = os.path.dirname(path_file_os)
    path_rule = path_file[0].split("/")[-1]
    path_files = []

    if os.path.exists(path_dir):
        path_dir_files = os.listdir(path_dir)
        if region:
            for i in range(len(path_dir_files)):
                path = "".join([path_dir, "/", path_dir_files[i]])
                path_files.append(path)

        else:
            for i in range(len(path_dir_files)):
                if path_rule in path_dir_files[i]:
                    path = "".join([path_dir, "/", path_dir_files[i]])
                    path_files.append(path)

    return path_files


# ====================
# interface function

def open_path(node):
    
    # 打开Geometry file下的路径
    path_parm = node.evalParm("file")
    check_path_format(path_parm)
    path_dir = os.path.dirname(path_parm)

    if not os.path.exists(path_dir):
        if hou.ui.displayMessage(
            "Geometry file path cannot be empty! Do you want to create one?",
            buttons=(" Yes ", " Next Time ")
        ) == 0:
            try:
                os.makedirs(path_dir)

            except WindowsError:
                check_has_unsaved()
                path_dir = os.path.dirname(node.evalParm("file"))
                os.makedirs(path_dir)

        else:
            exit()
    
    os.startfile(path_dir)


def destroy_geo(node):

    # 生成Geomerty file的文件列表和同层级目录下所有的文件列表
    path_parm = node.evalParm("file")
    path_dir = os.path.dirname(path_parm)
    path_os = path_parm.split("/")[-1].split(".")[0]
    check_path_format(path_parm)

    path_files = generate_files_list(path_parm)
    path_dir_files = generate_files_list(path_parm, region=1)

    # 获取缓存路径下文件的信息并反馈信息
    all_amount = get_list_amount(path_dir_files)
    all_size = get_lsit_size(path_dir_files)

    ls_amount = get_list_amount(path_files)
    ls_range = get_list_range(path_files)
    ls_size = get_lsit_size(path_files)

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
            "frame range: %s \n"
            % (all_amount, all_size, ls_amount, ls_size, path_os, ls_range)
        ),
        buttons=(" All ", " Only ", " Cancel ")
    )

    if user == 0:
        if not os.path.exists(path_dir):
            if hou.ui.displayMessage(
                "Folder does not exist!!!"
            ) == 0:
                exit()
        else:
            shutil.rmtree(path_dir)
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
            for i in range(len(path_files)):
                os.remove(path_files[i])
                hou.ui.setStatusMessage(
                    "Current cache destroy done!"
                )

    elif user == 2:
        exit()


if __name__ is "__main__":
    generate_files_list()
