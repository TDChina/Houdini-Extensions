# -*- coding: UTF-8 -*-
# Copyright (c) 2018 ChuckBiBi
import hou


def check_selection():

    # 判断用户是否选中节点
    selection = hou.selectedNodes()
    if not selection:
        
        hou.ui.displayMessage("Nothing selected, please select a node")

    return selection


def link_node(child_node, parent_node):

    # 将创建的输出节点与选中的节点相连接
    child_node.setNextInput(parent_node)
    child_node.setPosition(parent_node.position())
    child_node.move([0, -1])
    child_node.setSelected(True)
    parent_node.setSelected(False)


def rename_node(node_type, node_name):

    # 生成创建的节点的名字
    if node_name is "":
        
        node_newname = node_type + "_1"

    else:
        
        node_newname = node_type + "_" + node_name

    return node_newname


def colour_node(node):

    # 设置创建的节点的颜色
    # TODO:将设置null节点的颜色功能加入panel中
    colour_node = hou.Color([0.5, 0.8, 0])
    node.setColor(colour_node)


def create_null_node():

     # 创建null节点
    selection = check_selection()

    for node in selection:
        
        input_name = hou.ui.readInput("CacheNode Name:", ("Create", "Cancel"))

        node_create = input_name[0]
        node_name = input_name[1]
        node_type = "OUT"

        if node_create is 0:
            
            node_newname = rename_node(node_type, node_name)
            parent = node.parent()
            out_null = parent.createNode("null", node_newname)

            link_node(out_null, node)
            colour_node(out_null)

        else:
            
            exit()

        out_null.setDisplayFlag(True)
        out_null.setRenderFlag(True)


class Cache(object):

    def __init__(self, node_type, node_name, parent):

        self.ndoe_type = node_type
        self.node_name = node_name
        self.parent = parent


    def generate_node_type(self, x):
        
        if x is not 3:
            
            x = str(x)
            type_dict = {"0" : "cache", "1" : "playblast", "2" : "render"}
            node_type = type_dict[x]
            return node_type

        else:
            
            exit()


    def record_node():
        
        pass


def create_cache_node():

    selection = check_selection()

    for node in selection:
        
        input_name = hou.ui.readInput(
            "CacheNode Type:", ("FileCache", "PlayBlast", "Render", "Cancel"))

        node_type = input_name[0]
        node_name = input_name[1]
        parent = node.parent()

        # 通过用户的选择实例化不同类型的输出节点
        cache_node = Cache(node_type, node_name, parent)

        node_type = cache_node.generate_node_type(node_type)
        node_newname = rename_node(node_type, node_name)
       

        # 创建cache节点
        node_type = "null"  # TODO:临时变量，等houdini中节点构建完后删除
        cache_node = parent.createNode(node_type, node_newname)
        link_node(cache_node, node)
        colour_node(cache_node)


if __name__ is "__main__":
    create_null_node()
    create_cache_node()
