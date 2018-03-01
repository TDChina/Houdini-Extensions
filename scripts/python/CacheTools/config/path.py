# -*- coding: UTF-8 -*-
# Copyright (c) 2018 ChuckBiBi
import os
import json
import hou
from CacheTools.utils import filecache as fc


def set_project_path():
    
    # prj = x:/project/sence/cam/group/
    pass


def extract_ls(name):
    
    # template : prj/geo/group/temp/cam/node/version/
    ls_libs = {
    "ls_cache_type" : ["geo", "filp", "render"],
    "ls_cache_group" : ["mod", "anim", "render", "cfx", "efx"],
    "ls_cache_group_mod" : ["prop", "char", "sence"],
    "ls_cache_group_cfx" : ["far", "cloth", "muscle"],
    "ls_cache_group_efx" : ["rbd", "filp", "pyro", "pop"],
    "ls_cache_status" : ["temp", "publish", "assets"],
    "ls_cache_status_assets" : ["..."]
    }
    
    ls = ls_libs[name] 

    return ls


def generate_menu_list(ls_temp, none=True, temp=False, reverse=False):
    
    # 根据用户选择的不同的类，生成Houdini中menu
    if temp:
        ls = ls_temp
    else:
        ls_name = "ls_" + ls_temp
        ls = extract_ls(ls_name)
    
    if none:
        ls_menu = [0, "None"]
    else:
        ls_menu = []

    if reverse:
        ls = sorted(ls, reverse=True)
        for i in range(len(ls)):
            x = len(ls)
            y = ls[i]
            ls_menu.append(x)
            ls_menu.append(y)
            x -= 1

    else:
        for index, item in enumerate(ls, 1):
            x = index
            y = item.capitalize()
            ls_menu.append(x)
            ls_menu.append(y)

    return ls_menu


def get_value(node, ls_libs_kind):
    
    # 得到Houdini中当前menu是什么类的缓存列表
    node_path = node.path()
    parm = node_path + "/" + ls_libs_kind
    parm_eval =  node.evalParm(parm)

    # 从ls库中获取当前类下的具体的元素名称
    ls_none = ["none"]
    ls_name = "ls_" + ls_libs_kind
    ls = ls_none + extract_ls(ls_name)

    # 返回Houdini中用户选中具体缓存元素的名称
    value = ls[parm_eval]

    return value

 
def get_cam():
    
    # 获取"/obj"下所有的cam
    nodelist = hou.node("/obj").allSubChildren()    
    camera_nodes = [node for node in nodelist if 'cam' == node.type().name()]
    ls_cam =[]

    for i in range(len(camera_nodes)):
        ls_cam.append(camera_nodes[i].name())

    return ls_cam


def increnment_version():

    # 检测用户创建的hip命名是否为name_version.hip，获取版本号
    fc.check_hip_freshness()
    path_hip = hou.hipFile.path()
    hou.hipFile.save(path_hip)
    path_hip_dir = os.path.dirname(path_hip)
    name_hip = path_hip.split("/")[-1]
    flag_version = "_v0"

    if flag_version not in path_hip:
        version = "v000"
        name_hip = "".join([name_hip.split(".")[0], "_", version, ".hip"])

    version = name_hip.split(".")[-2].split("_")[-1][1:]
    version_increnment = "v" + "%03d" % (int(version)+1)
    name_hip = "".join([name_hip.split(".")[0].split("_")[0], "_", version_increnment, ".hip"])
    path_hip_new = path_hip_dir + "/" + name_hip
    hou.hipFile.save(path_hip_new)

    hou.ui.setStatusMessage(
                    "Version increnment and save done!"
                )


def get_all_version(path):
    
    # 获取dir中所有的version
    path_dir = os.path.dirname(path)
    name = path.split("/")[-1].split("_")[0]
    ls_files = []
    ls_version = []

    if os.path.exists(path_dir):
        files = os.listdir(path_dir)
        
        for i in range(len(files)):
            if files[i].split(".")[-1] == path.split(".")[-1]:
                if name == files[i].split("_")[0] :
                    ls_files.append(files[i])

        if ls_files != []:
            for j in range(len(ls_files)):
                version = ls_files[j].split(".")[0].split("_")[-1]
                if version not in ls_version:
                    ls_version.append(version)
        else:
            ls_version = ["none"]

    else:
        ls_version = ["none"]

    return ls_version
    

# ====================
# interface function

def generate_path(node):

    # 获取组成路径的各个元素值
    c_type = get_value(node, "cache_type")
    c_group = get_value(node, "cache_group")
    c_status = get_value(node, "cache_status")
    c_name = node.name()

    cam = get_cam()[node.evalParm("cam")]
    temp = "E:/Temporary/test/geo/temp/filecache_v001.0001.bgeo.sc"
    version = get_all_version(temp)[node.evalParm("version")]

    # 建立输出缓存路径的组成元素字典
    element_list = {
        0 : c_type, 1 : c_group, 2 : c_status, 3 : cam, 4 : c_name, 5 : version
    }
    
    # 生成输出缓存的路径
    path_hip = os.path.dirname(hou.hipFile.path())
    path_cache = path_hip
    delimiter = "/"

    for i in range(len(element_list)):
        element = element_list[i]
        
        if element == "none":
            continue

        path_cache += "/" + element

    # 设置忽略的输出缓存类型
    kind = c_type

    if kind == "none":
        kind = ""

    # Houdini状态栏打印生成的路径结果
    if path_cache == path_hip:
        hou.ui.setStatusMessage(
            "".join(["Generate ", kind, " path: ", path_cache,
            "          ",
            "Generated path is in the same folder as hip,",
            "It is recommended that you choose again."
            ]))

    else:
        hou.ui.setStatusMessage(
            "".join(["Generate ", kind, " path: ", path_cache
            ]))
    
    return path_cache


if __name__ is "__main__":
    get_all_version()