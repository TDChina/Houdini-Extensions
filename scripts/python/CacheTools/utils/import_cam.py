# -*- coding: UTF-8 -*-
# Copyright (c) 2018 ChuckBiBi
import hou  


def check_selection():
    
    # 判断用户是否选中节点
    selection = hou.selectedNodes()
    if not selection:
        
        hou.ui.displayMessage("Nothing selected, please select a node")

    return selection


def updata_cam_resolution(selection_node):
    
    #更新摄像机的分辨率
    selection = selection_node
    nodelist = selection[0].allSubChildren()    
    camera_nodes = [node for node in nodelist if 'cam' == node.type().name()]    
    for camera in camera_nodes:    
        camera.parm('resx').set(1280)
        camera.parm('resy').set(720)


def import_cam():
    
    selction_node = check_selection()
    updata_cam_resolution(selction_node)


if __name__ is "__main__":
    import_cam()