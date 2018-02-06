import hou  


def updata_cam_resolution():
    
    nodelist = hou.selectedNodes()[0].allSubChildren()    
    camera_nodes = [node for node in nodelist if 'cam' == node.type().name()]    
    for camera in camera_nodes:    
        camera.parm('resx').set(1280)
        camera.parm('resy').set(720)