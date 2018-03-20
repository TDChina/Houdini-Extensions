# -*- coding: UTF-8 -*-
# Copyright (c) 2018 ChuckBiBi
import os
import re
import json
import hou


path_hip = hou.hipFile.path()
path_hip_dir = os.path.dirname(path_hip)
hip_name = os.path.basename(path_hip)
hip_fname = os.path.splitext(hip_name)[0]


def check_hip_freshness():
    
    if hou.hipFile.name() == path_hip:  # 检查当前hip是不是新建的
        return

    if hou.ui.displayMessage(   # 是否保存当前hip
        "The current hip never saved ,you needs to be saved.",
        buttons=(" Save ", " Next Time ")
    ) == 0:
        path_hip_new = hou.ui.selectFile(
            # TODO:建立链接
            # start_directory =  
            start_directory="E:/Temporary/",
            title="Save As",
            file_type=hou.fileType.Any,
            pattern="*.hip",
            default_value="test_v001.hip",
            chooser_mode=hou.fileChooserMode.Write
        )
        hou.hipFile.save(path_hip_new)
    else:
        exit()


def increnment_version():

    # 检测hip命名是否带有带版本号，获取版本号，并升一版保存
    global hip_name
    check_hip_freshness()
    hou.hipFile.save(path_hip)  
    version_flag = "v0"

    if version_flag not in hip_name:
        version = "v000"
        hip_name = "".join([hip_fname, "_", version, ".hip"])

    version = re.findall(r"v0\d\d", hip_name)[0]
    version_increnment = "v" + "%03d" % (int(version[1:])+1)
    hip_name_new = "".join([hip_fname[:-5], "_", version_increnment, ".hip"])
    path_hip_new = path_hip_dir + "/" + hip_name_new
    hou.hipFile.save(path_hip_new)
    hou.ui.setStatusMessage(
                    "Hip version increnment and save done!"
                )


def set_project_path():
    
    # prj = x:/project/sence/cam/group/
    pass


def record_list():
    
    # template : prj/geo/group/temp/cam/node/version/
    ls_libs = {
    "ls_cache_group" : ["mod", "anim", "render", "cfx", "efx"],
    "ls_cache_group_mod" : ["prop", "char", "vegetation", "rock", "sence"],
    "ls_cache_group_cfx" : ["far", "cloth", "muscle"],
    "ls_cache_group_efx" : ["rbd", "filp", "pyro", "pop"],
    "ls_cache_status" : ["temp", "publish", "assets"],
    "ls_cache_status_assets" : ["..."]
    }

    json_str = json.dumps(ls_libs)
    json_dict = json.loads(json_str)
    data = json.dumps(json_dict, sort_keys=True, indent=4)

    with open(os.path.dirname(__file__) + "\data\ls_libs.json", "w") as file:
        file.write(data)

        print "Data file record completed...."


def extract_list(ls_libs_kind):
    
    with open(os.path.dirname(__file__) + "\data\ls_libs.json", "r") as load_file:
        data = load_file.read()

    ls_libs = json.loads(data)

    try:
        ls = ls_libs[ls_libs_kind]
    except:
        return []

    return ls


def generate_menu_list(lst, none_option=True, temp=False, reverse=False):
    
    # 根据用户选择的不同类，生成Houdini中menu的列表
    ls_input = lst if temp else extract_list("ls_" + lst)
    ls_menu = [0, "None"] if none_option else []

    if reverse:
        ls_temp = sorted(ls_input, reverse=True)
        num = len(ls_temp)
        for i in ls_temp:
            ls_menu.append(num)
            ls_menu.append(i)
            num -= 1
    else:
        for index, item in enumerate(ls_input, 1):
            x = index
            y = item.capitalize()
            ls_menu.append(x)
            ls_menu.append(y)

    return ls_menu


def get_value(node, ls_libs_kind, detail=False, group="none"):
    
    path_node = node.path() # 得到Houdini中当前menu选择的是什么类的缓存列表
    ls_kind = path_node + "/" + ls_libs_kind
    parm_eval = node.evalParm(ls_kind)

    temp = "ls_" + ls_libs_kind # 从ls_libs中获取当前下的具体的元素名称
    ls_name = (temp + group) if detail else temp    
    ls = ["none"] + extract_list(ls_name)
    value = str(ls[parm_eval])

    return value

 
def get_cam():
    
    # 获取"/obj"下所有的cam
    nodelist = hou.node("/obj").allSubChildren()    
    camera_nodes = [node for node in nodelist if 'cam' == node.type().name()]
    ls_cam =[]

    if not camera_nodes:
        return ["none"]

    for i in camera_nodes:
        ls_cam.append(i.name())

    return ls_cam


def get_all_version(path):

    # 获取path中所有的version
    ls_version = []

    if os.path.exists(path):    # 检查文件夹目录是否存在
        files = os.listdir(path)
        if files != []:
            for i in files:
                ls_version.append(i)
        else:
            ls_version = ["None"]
    else:
        ls_version = ["None"]

    return ls_version
    

# ====================
# interface function

def generate_path(node, set_path=True):
    
    cache_type = "geo"  # 获取组成路径的各个元素值，并生成元素组列表
    cache_status = get_value(node, "cache_status")
    cache_group = get_value(node, "cache_group")

    if cache_group == "none":   # 当组为none时，组的分类也为none
        cache_group_type = "none"
    else:
        try:
            cache_group_type = get_value(node, "cache_group_", detail=True, group=cache_group)
        except IndexError:
            hou.node(node.path()).parm("cache_group_").set(0)
            cache_group_type = "none"
        
    cache_name = node.name()
    cam = get_cam()[node.evalParm("cam")]

    element_list = [cache_type, cache_status, cache_group, cache_group_type, cache_name]    # 生成输出文件的路径各字段元素列表
    path_output_dir = path_hip_dir + "/"

    for i in element_list:
        if i == "none":
            continue
        path_output_dir += i + "/"

    ls_version = sorted(get_all_version(path_output_dir), reverse=True)
    version_max = ls_version[0]

    if version_max != "None":   # 如果返回的version列表中只有“None”，就输出“v001”
        version = ls_version[node.evalParm("version")]
    else:
        hou.node(node.path()).parm("version").set(0)
        version = "v001"

    path_output = path_output_dir + version + "/"       

    if set_path:    # 是否修改界面的task_path参数，如果false则修改的是load_path参数
        if node.evalParm("increnment"):     # 如果“increnment”参数被勾选，输出的version在返回的version列表中以最新版本号升一版
            if version_max != "None":
                version_up = "v" + "%03d" % (int(version_max[1:])+1)
                path_output = path_output_dir + version_up + "/"

        node.parm("task_path").set(path_output)
    else:
        node.parm("load_path").set(path_output)

        return path_output
        
    hou.ui.setStatusMessage("".join(["Generate geo path: ", path_output]))

    return path_output


if __name__ is "__main__":
    print "test"
