# def find_evil_function(target_class,evil_functions):
#     for j in target_class['nodes']:
#         print(target_class['name'])
#         try:
#             if j['name'].lower() in evil_functions or j[0].lower() in evil_functions:
#                 print(j)
#         except:
import json


def get_the_classes(outf):
    #对文件中存在的每个Class进行提取
    Classes=[]
    for i in json.load(outf):
        if i[0] == "Class":
            Classes.append(i[1])
    return Classes
def prepare_class(target_class):
    #解析传入的Class列表，将其中的Class解析成分析器需要的格式
    Class={}
    Class['name']=target_class['name']
    Class['methods']=[]
    Class['variables']=[]
    for i in target_class['nodes']:
        if i[0]=="Method":
            Class['methods'].append(parse_method(i[1]))
        elif i[0]=="ClassVariables":
            Class['variables'].append(parse_variable(i[1]))
    return Class
def parse_variable(target_variable):
    #处理类中所有属性
    variable_dict={}
    variable_dict['name']=target_variable['nodes'][0][1]['name']
    variable_dict['modifiers']=(target_variable['modifiers'])
    variable_dict['initial']=target_variable['nodes'][0][1]['initial']
    return variable_dict
def parse_others(target):
    #处理类中其他内容
    if target[0]=="Echo":
        target=target[1]
        while isinstance(target, dict):
            if "name" in target:
                return
            try:
                target = target["node"][1]
            except:
                break
        pass

def parse_method(target_method):
    #处理类中方法，部分赋值相关内容还没有处理好
    method_dict={}
    method_dict['name']=target_method['name']
    method_dict['modifiers']=' '.join(target_method['modifiers'])
    method_dict['funcs'],method_dict['methods']=parse_method_nodes(target_method['nodes'])
    method_dict['params']=[]
    for i in target_method['params']:
        method_dict['params'].append(i[1]['name'])
    return method_dict
def parse_method_nodes(nodes):
    dosth=[[],[]] #0位存funcs，1位存methods
    for i in nodes:
        tmp_node=find_method_call(i)
        if tmp_node:
            #写method存储的处理
            print(tmp_node)
        tmp_node=find_func_call(i)
        if tmp_node:
            #写func存储的处理
            func={}
            func['name']=tmp_node['name']
            func['params']=[]
            for j in tmp_node['params']:
                if j[0]=="Parameter":
                    if j[1]['node'][0]=="Variable":
                        func['params'].append(j[1]['node'][1]['name'])
                    elif j[1]['node'][0]=="ArrayOffset":
                        func['params'].append(parse_arrayoffset(j[1]['node']))
            dosth[0].append(func)
        # elif i[0]=="Assignment":
        #     current_node= i[1]
        #     target=[]
        #     value=[]
        #     while isinstance(current_node, dict):
        #         if "name" in current_node:
        #             target.append(current_node["name"])
        #         try:
        #             current_node = current_node["node"][1]
        #         except:
        #             break
        #     current_node=i[1]['expr']
        #     if isinstance(current_node, str):
        #         value=current_node
        #     else:
        #         if current_node[0]=="MethodCall":
        #             value=parse_MethodCall(current_node)
        #         elif current_node[0]=="FunctionCall":
        #             #处理函数操作的赋值
        #             value=parse_FunctionCall(current_node)
        #         else:
        #             #处理非函数操作的赋值
        #             current_node=current_node[1]
        #             while isinstance(current_node, dict):
        #                 if "name" in current_node:
        #                     value.append(current_node["name"])
        #                 try:
        #                     current_node = current_node["node"][1]
        #                 except:
        #                     break
        #     func={"name":"assignment"}
        #     func['target']=target[::-1]
        #     func['value']=value[::-1]
        #     funcs.append(func)
        # elif i[0]=="If":
        #     for i in parse_method_nodes(i[1]['node'][1]['nodes']):
        #         funcs.append(i)
        # else:
        #     parse_others(i)
    return dosth
def parse_arrayoffset(target):
    arrayoffset=[]
    arrayoffset.append(target[1]['node'][1]['name'])
    arrayoffset.append(target[1]['expr'])
    return arrayoffset
def parse_expr(expr):
    pass

def parse_FunctionCall(target):
    value=[]
    current_node = target[1]
    value.append(f"{current_node['name']}({current_node['params']})")
    return value
def parse_MethodCall(target):
    value=[]
    current_node = target[1]
    value.append(f"{current_node['name']}({current_node['params']})")
    try:
        current_node = current_node['node'][1]
    except:
        pass
    while isinstance(current_node, dict):
        if "name" in current_node:
            value.append(current_node["name"])
        try:
            current_node = current_node["node"][1]
        except:
            break
    return value
def find_evil(target_class,evil_functions):
    #查找类中是否存在恶意函数
    evils=[]
    for i in target_class['methods']:
        for j in i['funcs']:
            if j['name'] in evil_functions:
                evils.append(i['name'])
    return evils

def find_method_call(node):
    """
    递归函数，用于获取"MethodCall"部分的属性
    """
    if isinstance(node, list): # 判断是否为列表类型
        if not node:  # 判断列表是否为空
            return None
        if node[0]=="MethodCall":
            return node[1]
        for item in node:
            result = find_method_call(item)
            if result: # 如果在子节点中找到了"MethodCall"，则返回结果
                return result
    elif isinstance(node, dict): # 判断是否为字典类型
        for value in node.values():
            result = find_method_call(value)
            if result: # 如果在子节点中找到了"MethodCall"，则返回结果
                return result
    return None # 如果没有找到"MethodCall"，返回None

def find_func_call(node):
    """
    递归函数，用于获取"MethodCall"部分的属性
    """
    if isinstance(node, list): # 判断是否为列表类型
        if not node:  # 判断列表是否为空
            return None
        if node[0]=="FunctionCall":
            return node[1]
        for item in node:
            result = find_func_call(item)
            if result: # 如果在子节点中找到了"MethodCall"，则返回结果
                return result
    elif isinstance(node, dict): # 判断是否为字典类型
        for value in node.values():
            result = find_func_call(value)
            if result: # 如果在子节点中找到了"MethodCall"，则返回结果
                return result
    return None # 如果没有找到"MethodCall"，返回None

def search_target_str(data, target_str, parent_keys=''):
    """
    递归搜索多层级对象中是否包含指定字符串，并输出包含该字符串的元素的层级键
    :param data: 多层级对象
    :param target_str: 要查找的字符串
    :param parent_keys: 父级键
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                search_target_str(value, target_str,  parent_keys + f"[{key!r}]")
            elif isinstance(value, str) and value.lower() in target_str:
                print( parent_keys + f"[{key!r}]")
            elif isinstance(key, str) and key.lower() in target_str:
                print( parent_keys + f"[{key!r}]")
    elif isinstance(data, list):
        for index, item in enumerate(data):
            if isinstance(item, (dict, list)):
                search_target_str(item, target_str, parent_keys + f"[{index}]")
            elif isinstance(item, str) and item.lower() in target_str:
                print(parent_keys + f"[{index}]")