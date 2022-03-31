'''
@file            :utils.py
@Description     :小工具方法
@Date            :2022/03/21 18:03:29
@Author          :幸福关中 && 轻编程
@version         :v1.0
@EMAIL           :1158920674@qq.com
@WX              :baywanyun
'''

def generate_tree(source, parent):
    """分类递归算法

    Args:
        source (_list_): [{id: 1, name: 'nav', parent: None }, {id: 2, name: 'nav', parent: 1 }]
        parent (_None_): 根据此字段进行分类递归
    Returns:
        _type_: _description_. 递归嵌套
    """
    tree = []
    for item in source:
        if item["parent"] == parent:
            item["sub_cates"] = generate_tree(source, item["id"])
            tree.append(item)
    return tree