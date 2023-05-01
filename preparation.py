import json

def get_the_classes(outf):
    # 对文件中存在的每个Class进行提取
    Classes = []
    for i in json.load(outf):
        if i[0] == "Class":
            Classes.append(i[1])
    return Classes


def prepare_class(target_class):
    # 解析传入的Class列表，将其中的Class解析成分析器需要的格式
    Class = {}
    Class['name'] = target_class['name']
    Class['methods'] = []
    Class['variables'] = []
    for i in target_class['nodes']:
        if i[0] == "Method":
            Class['methods'].append(parse_method(i[1]))
        elif i[0] == "ClassVariables":
            Class['variables'].append(parse_variable(i[1]))
    Class['calls']=find_method_call(Class)
    return Class


def parse_variable(target_variable):
    # 处理类中所有属性
    variable_dict = {}
    variable_dict['name'] = target_variable['nodes'][0][1]['name']
    variable_dict['modifiers'] = (target_variable['modifiers'])
    variable_dict['initial'] = target_variable['nodes'][0][1]['initial']
    return variable_dict

def find_method_call(target):
    return None

def find_calls(target,call_list):
    calls=[]
    for i in call_list:
        for j in i[0]:
            return None


def parse_others(target):
    others_list=[]
    other_name_list=['Echo','Include','Eval','Return','IsSet']
    a=list(find_target_attr(target,"Echo"))
    if a:
        for i in a:
            func = {}
            func['name'] = 'echo'
            func['params'] = list(find_variable(i))
            others_list.append(func)
    a=list(find_target_attr(target,"Include"))
    if a:
        for i in a:
            func={}
            func['name']='include'
            func['params']=list(find_variable(i))
            others_list.append(func)
    a=list(find_target_attr(target,"Eval"))
    if a:
        for i in a:
            func={}
            func['name']='eval'
            func['params']=list(find_variable(i))
            others_list.append(func)
    a=list(find_target_attr(target,"Return"))
    if a:
        for i in a:
            func={}
            func['name']='return'
            func['params']=list(find_variable(i))
            others_list.append(func)
    a=list(find_target_attr(target,"IsSet"))
    if a:
        for i in a:
            func={}
            func['name']='isset'
            func['params']=list(find_variable(i))
            others_list.append(func)
    # 处理类中其他内容
    return others_list


def parse_method(target_method):
    # 处理类中方法，部分赋值相关内容还没有处理好
    method_dict = {}
    method_dict['name'] = target_method['name']
    method_dict['modifiers'] = ' '.join(target_method['modifiers'])
    method_dict['funcs'], method_dict['methods'] = parse_method_nodes(target_method['nodes'])
    method_dict['params'] = []
    for i in target_method['params']:
        method_dict['params'].append(i[1]['name'])
    return method_dict


def parse_method_nodes(nodes):
    dosth = [[], []]  # 0位存funcs，1位存methods
    for i in nodes:
        tmp_node = list(find_target_attr(i, "MethodCall"))
        if tmp_node:
            # 写method存储的处理
            for j in tmp_node:
                method = {}
                method['name'] = j['name']
                method['variable'] = list(find_variable(j))
                method['variable'].reverse()
                method['variable'].pop()
                '''
                对于属性判断等后面在做，目前所有工作为找链子服务
                下面的代码考虑并不完全，可以后面再改改
                '''
                # for j in tmp_node['params']:
                #     if j[0]=="Parameter":
                #         if j[1]['node'][0]=="Variable":
                #             method['params'].append(j[1]['node'][1]['name'])
                #         elif j[1]['node'][0]=="ArrayOffset":
                #             method['params'].append(parse_arrayoffset(j[1]['node']))
                dosth[1].append(method)
        tmp_node = list(find_target_attr(i, "FunctionCall"))
        if tmp_node:
            for j in tmp_node:
                # 写func存储的处理
                func = {}
                func['name'] = j['name']
                func['params'] = []
                # for j in tmp_node['params']:
                #     if j[0] == "Parameter":
                #         if j[1]['node'][0] == "Variable":
                #             func['params'].append(j[1]['node'][1]['name'])
                #         elif j[1]['node'][0] == "ArrayOffset":
                #             func['params'].append(parse_arrayoffset(j[1]['node']))
                dosth[0].append(func)
        tmp_node = parse_others(i)
        if tmp_node:
            dosth[0]+=tmp_node
    return dosth


def parse_arrayoffset(target):
    arrayoffset = []
    arrayoffset.append(target[1]['node'][1]['name'])
    arrayoffset.append(target[1]['expr'])
    return arrayoffset


def find_evil(target_class, evil_functions):
    # 查找类中是否存在恶意函数
    evils = []
    for i in target_class['methods']:
        for j in i['funcs']:
            if j['name'] in evil_functions:
                evils.append(i['name'])
    return evils


def find_target_attr(node, attrname):
    """
    递归查找相对应的属性
    """
    if isinstance(node, list):  # 判断是否为列表类型
        try:
            if node[0] == attrname:
                yield node[1]
            for item in node:
                yield from find_target_attr(item, attrname)
        except:
            pass
    elif isinstance(node, dict):  # 判断是否为字典类型
        for value in node.values():
            yield from find_target_attr(value, attrname)


def find_variable(node):
    '''
    {'lineno': 14, 'node': ['Variable', {'lineno': 14, 'name': '$nnnn'}], 'name': 'aaaa', 'params': []}
    {'lineno': 29, 'node': ['ObjectProperty', {'lineno': 29, 'node': ['Variable', {'lineno': 29, 'name': '$this'}], 'name': 'aaa'}], 'name': 'aaa', 'params': []}
    {'lineno': 30, 'node': ['Variable', {'lineno': 30, 'name': '$x'}], 'name': 'x', 'params': []}
    '''
    if isinstance(node, dict):
        if 'name' in node:
            yield node['name']
        for value in node.values():
            yield from find_variable(value)
    elif isinstance(node, list):
        for item in node:
            yield from find_variable(item)


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
                search_target_str(value, target_str, parent_keys + f"[{key!r}]")
            elif isinstance(value, str) and value.lower() in target_str:
                print(parent_keys + f"[{key!r}]")
            elif isinstance(key, str) and key.lower() in target_str:
                print(parent_keys + f"[{key!r}]")
    elif isinstance(data, list):
        for index, item in enumerate(data):
            if isinstance(item, (dict, list)):
                search_target_str(item, target_str, parent_keys + f"[{index}]")
            elif isinstance(item, str) and item.lower() in target_str:
                print(parent_keys + f"[{index}]")
