# -*- coding: UTF-8 -*-
# Copyright (c) 2018 ChuckBiBi
import hou
import os
from shutil import rmtree


def open_path(node):

    try:
        path_parm = node.evalParm("file")
        path_dir = os.path.dirname(path_parm)
        os.startfile(path_dir)

    except WindowsError:
        if hou.ui.displayMessage(
            "Geometry file path cannot be empty! Do you need to create one?", ("Yes！","Next Time！")
            ) == 0:

            os.makedirs(path_dir)
            os.startfile(path_dir)


def destroy_geo(node):

    path_parm = node.evalParm("file")
    path_dir = os.path.dirname(path_parm) + "/"
    path_file = path_parm.split(".")
    path_files = []

    for i in range(len(path_file)):

        if path_file[i].isdigit():        
            delimiter = "."
            frame_end_parm = node.evalParmTuple("f")
            times = int(frame_end_parm[1])

            for j in range(times):            
                start_num = "%04d" % (j+1)
                path_file[i] = start_num
                path_files.append(delimiter.join(path_file))


    user = hou.ui.displayMessage(
            "Destroy all cache under current folder?\nor Current Geometry file cache?", ("All", "Current", "Cancel")
            )

    if user  == 0:

        try:
            shutil.rmtree(path_dir)

        except WindowsError:
            if hou.ui.displayMessage(
                "Folder does not exist!!!", ("Cancel",)
                ) == 0:

                exit()
    
    elif user == 1: 

        try:
            for i in range(len(path_files)):
                os.remove(path_files[i])

        except WindowsError:
            if hou.ui.displayMessage(
                "File does not exist!!!", ("Cancel",)
                ) == 0:

                exit()

    elif user == 2:

        exit()

