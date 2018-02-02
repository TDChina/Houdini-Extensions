# -*- coding: UTF-8 -*-
# Copyright (c) 2018 ChuckBiBi


import hou


def check_selection():
    selection = hou.selectedNodes()
    if not selection:
        hou.ui.displayMessage("Nothing selected, please select a node")
    return selection


def create_null():
    selection = check_selection()
    for node in selection:
        input_name = hou.ui.readInput("CacheNode Name:", ("Create", "Cancel"))
        node_create = input_name[0]
        node_name = input_name[1]

        if node_create == 0:
            if node_name == "":
                node_name = "OUT_1"
            else:
                node_name = "OUT_" + node_name

            # 创建null节点并连接选中节点
            parent = node.parent()
            out_null = parent.createNode("null", node_name)
            out_null.setNextInput(node)

            # 移动null到选中节点下方一个单位
            out_null.setPosition(node.position())
            out_null.move([0, -1])

            # 改变节点的选择状态
            out_null.setSelected(True)
            node.setSelected(False)

            # 设置null节点的颜色
            # TODO:将设置null节点的颜色功能加入panel中
            node_color = hou.Color([0.5, 0.8, 0])
            out_null.setColor(node_color)
        else:
            break

        out_null.setDisplayFlag(True)
        out_null.setRenderFlag(True)


def create_cache():
    selection = check_selection()
    for node in selection:
        input_name = hou.ui.readInput(
            "CacheNode Type:", ("FileCache", "PlayBlast", "Render", "Cancel"))
        node_type = input_name[0]
        node_name = input_name[1]
        parent = node.parent()

        # 通过用户选择不同的类型创建不同类型的输出节点
        if node_type == 0:
            if node_name == "":
                node_name = "Cache_1"
            else:
                node_name = "Cache_" + node_name
            cache_cache = parent.createNode("rop_geometry", node_name)

        elif node_type == 1:
            if node_name == "":
                node_name = "Playblast_1"
            else:
                node_name = "Playblast_" + node_name
            cache_cache = parent.createNode("null", node_name)

        elif node_type == 2:
            if node_name == "":
                node_name = "Render_1"
            else:
                node_name = "Render_" + node_name
            cache_cache = parent.createNode("null", node_name)
        else:
            break

        cache_cache.setNextInput(node)
        cache_cache.setPosition(node.position())
        cache_cache.move([0, -1])
        cache_cache.setSelected(True)
        node.setSelected(False)


if __name__ == "__main__":
    create_cache()
