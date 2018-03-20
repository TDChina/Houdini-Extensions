# -*- coding: UTF-8 -*-
# Copyright (c) 2018 ChuckBiBi
import hou


rop_parent = hou.node('/out')

def check_selection():
    
    """检查用户是否有选中节点
    """

    selection = hou.selectedNodes()
    if not selection:       
        hou.ui.displayMessage("Nothing selected, please select a node")

    return selection


def link_node(child_node, parent_node):
    
    """与输入的上游（父）节点连接
    """

    child_node.setNextInput(parent_node)
    child_node.setPosition(parent_node.position())
    child_node.move([0, -1])
    child_node.setSelected(True)
    parent_node.setSelected(False)


def rename_node(node_type, node_name):
    
    """将节点的命名用规范的格式来命名
    """

    if node_name is "":       
        node_newname = node_type + "_1"
        
    else:       
        node_newname = node_type + "_" + node_name

    return node_newname


def colour_node(node):
    
    """设置创建的节点的颜色
    """

    # TODO:将设置null节点的颜色功能加入panel中
    colour_node = hou.Color([0.5, 0.8, 0])
    node.setColor(colour_node)


class Cache(object):
    
    def __init__(self, ndoe):
    
        self.ndoe = ndoe
        self.inputs = []


    def judge_cache(self):
        return self.node.type().name() == "filecache"


    def generate_rop_name(self):
        return self.node.name() + "_cache"


def get_upstream(node):
    
    cache_node = []
    for i in node.inputs():
        if i.type().name() == "filecache":
            cache_node.append(i)

        else:
            cache_node.extend(get_upstream(i))

    return cache_node


def to_cache(node):
    
    cache = Cache(node)
    cache.inputs = [to_cache(i) for i in get_upstream(node)]
    
    return cache


def to_Rop(cache):
    
    r = rop_parent.node(chain.ropName())

    if not r:
        r = rop_parent.createNode('fetch' if chain.isFC() else 'merge')  
        r.setName(chain.ropName())  
    else:  
        for i in range(len(r.inputs())):  
            r.setInput(i, None)  

    r.setColor(chain.node.color())  

    if chain.isFC():  
        r.parm('source').set(chain.node.path() + '/render')  
      
    for i, input_rop in enumerate([toRop(i) for i in chain.inputs]):
        r.setInput(i, input_rop)
        
    r.moveToGoodPosition()  

    return r  
    
def create_null_node():
    
     # 创建null节点
    selection = check_selection()

    for node in selection:     
        input_name = hou.ui.readInput("CacheNode Name:", ("Create", "Cancel"))

        node_creating = input_name[0]
        node_name = input_name[1]
        node_type = "OUT"

        if not node_creating:        
            node_newname = rename_node(node_type, node_name)
            parent = node.parent()
            out_null = parent.createNode("null", node_newname)

            link_node(out_null, node)
            colour_node(out_null)

        else:       
            exit()

        out_null.setDisplayFlag(True)
        out_null.setRenderFlag(True)


def create_cache_node():
    
    selection = check_selection()

    for node in selection:     
        input_name = hou.ui.readInput(
            "CacheNode Name:", ("Create", "Cancel"))

        if not input_name[0]:
            node_type = "cache"
        else:
            exit()

        node_name = input_name[1]
        node_newname = rename_node(node_type, node_name)
        parent = node.parent()
 
        cache_node = Cache(node)    # 实例化缓存输出节点，并创建cache缓存节点
        node_type = "null"  # TODO:临时变量，等houdini中节点构建完后删除
        cache_node = parent.createNode(node_type, node_newname)
        link_node(cache_node, node)
        colour_node(cache_node)

        cache_node.setDisplayFlag(True)
        cache_node.setRenderFlag(True)
         

if __name__ is "__main__":
    create_null_node()
    create_cache_node()
