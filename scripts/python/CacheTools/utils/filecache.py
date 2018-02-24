# -*- coding: UTF-8 -*-
# Copyright (c) 2018 ChuckBiBi
import hou
import os
from shutil import rmtree


def check_hasUnsaved():

    if hou.hipFile.hasUnsavedChanges():
        if hou.ui.displayMessage(
            "The current hip isn't saved ,you needs to be saved.",
            buttons = (" Cancel ",)
            ) == 0:
            exit()


def open_path(node):

    try:
        path_parm = node.evalParm("file")
        path_dir = os.path.dirname(path_parm)
        os.startfile(path_dir)

    except WindowsError:
        if hou.ui.displayMessage(
            "Geometry file path cannot be empty! Do you need to create one?",
            buttons = (" Yes ", " Next Time ")
            ) == 0:

            try:
                os.makedirs(path_dir)
                os.startfile(path_dir)

            except WindowsError:
                check_hasUnsaved()
                os.makedirs(path_dir)
                os.startfile(path_dir)

        else:
            exit()


def generate_files_list(node, file):
    
    path_parm = file
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
    
    return path_files


def destroy_geo(node):

    path_parm = node.evalParm("file")
    path_dir = os.path.dirname(path_parm) + "/"
    path_files = generate_files_list(node, path_parm)

    user = hou.ui.displayMessage(
            "Destroy all cache under current folder?\nor Current Geometry file cache?",
            buttons = (" All ", " Current ", " Cancel ")
            )

    if user  == 0:
        try:
            shutil.rmtree(path_dir)
            hou.ui.setStatusMessage("Folder destroy done!")

        except WindowsError:
            if hou.ui.displayMessage(
                "Folder does not exist!!!", ("Cancel",)
                ) == 0:
                exit()
    
    elif user == 1: 
        try:
            for i in range(len(path_files)):
                os.remove(path_files[i])
                hou.ui.setStatusMessage("Current cache destroy done!")
                
        except WindowsError:
            if hou.ui.displayMessage(
                "File does not exist!!!", ("Cancel",)
                ) == 0:
                exit()

    elif user == 2:
        exit()

