# -*- coding: UTF-8 -*-
# Copyright (c) 2018 ChuckBiBi
import hou
import json


def set_project_path():
    
    # prj = x:/project/sence/cam/group/
    pass


def extract_ls(name):
    
    # template : prj/geo/temp/cam/node/version/
    ls_libs = {
    "ls_cache_group" : ["mod", "anim", "render", "cfx", "efx"],
    "ls_mod" : ["prop", "char", "sence"],
    "ls_cfx" : ["far", "cloth", "muscle"],
    "ls_efx" : ["rbd", "filp", "pyro", "pop"],
    "ls_cache_type" : ["geo", "filp", "render"],
    "ls_cache_status" : ["temp", "publish", "assets"]
    
    }
    ls = ls_libs[name] 

    return ls


def set_cache_type():
    
    ls_name= "ls_cache_type"
    ls = extract_ls(ls_name)
    ls_cache_type = [0, "None"]

    for index, cache_type in enumerate(ls, 1):
        x = index ;y = cache_type.capitalize()
        ls_cache_type.append(x)
        ls_cache_type.append(y)
            
    return ls_cache_type


def get_value(node):
    
    node_path = node.path()
    parm_cache_type = node_path + "/cache_type"  
    ls_blank = ["none"]

    cache_type =  node.evalParm(parm_cache_type)
    ls_name= "ls_cache_type"
    ls_cache_type = ls_blank + extract_ls(ls_name)
    cache_type = ls_cache_type[cache_type]

    print ("cache_type ---> " + cache_type)

 
def set_status():
    pass


def get_cam():
    pass


def get_cache_name():
    pass


def set_version():
    pass

    
def record_path_data():
    pass


if __name__ is "__main__":
    set_cache_type()