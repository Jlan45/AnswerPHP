import json

def get_the_classes(outf):
    # 对文件中存在的每个Class进行提取
    Classes = []
    for i in json.load(outf):
        if i[0] == "Class":
            Classes.append(i[1])
    return Classes
def prepare_class(target_class):
    '''
    传入类进行处理，返回一个处理好的字典，格式如下
      {
    "name": "类名",
    "methods": [
      {
        "name": "方法名",
        "modifiers": "方法修饰符（没啥用但是先做了）",
        "funcs": [
          {
            "name": "调用的函数名",
            "params": [方法的参数列表]
          }
        ],
        "methods": [该方法调用的其他方法],
        "params": [该方法的参数]
      }
    ],
    "variables": [
      {
        "name": "属性名",
        "modifiers": ["修饰符"],
        "initial": 初始化值，如果没有就是null
      }
    ],
    "calls": 会有的方法调用（感觉没什么用也确实没做解析）,
    "evils": [没用]
  }
    :param target_class:
    :return:
    '''
    Class = {}
    Class['name'] = target_class['name']
    Class['methods'] = []
    Class['variables'] = []
    for i in target_class['nodes']:
        if i[0] == "Method":
            #如果是Method节点就提取出对应的方法代码块进行解析
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
            func['params'] = [list(find_variable(i))]
            others_list.append(func)
    a=list(find_target_attr(target,"Include"))
    if a:
        for i in a:
            func={}
            func['name']='include'
            func['params'] = [list(find_variable(i))]
            others_list.append(func)
    a=list(find_target_attr(target,"Eval"))
    if a:
        for i in a:
            func={}
            func['name']='eval'
            func['params'] = [list(find_variable(i))]
            others_list.append(func)
    a=list(find_target_attr(target,"Return"))
    if a:
        for i in a:
            func={}
            func['name']='return'
            func['params'] = [list(find_variable(i))]
            others_list.append(func)
    a=list(find_target_attr(target,"IsSet"))
    if a:
        for i in a:
            func={}
            func['name']='isset'
            func['params'] = [list(find_variable(i))]
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
    #对每个子节点进行处理，解析出所有的方法调用和函数调用
        if i[0] == "FunctionCall":
            dosth[0].append(parse_functioncall(i[1]))
        elif i[0] =="MethodCall":
            dosth[0].append(parse_methodcall(i[1]))
    return dosth
def parse_methodcall(target):
    print(json.dumps(target))

def parse_functioncall(target):
    func={}
    func['params']=parse_params(target['params'])
    func
    print(json.dumps(target))

def parse_params(target):
    '''
    解析参数列表，具体实现直接看即可
    :param target:
    :return:
    '''
    params = []
    for i in target:
        if i[1]['node'][0]=="ObjectProperty" or i[1]['node'][0]=="ArrayOffset":
            params.append(parse_arrayoffset(i))
        elif i[1]['node'][0]=="Variable":
            params.append(i[1]['node'][1]['name'])
        elif i[1]['node'][0]=="MethodCall":
            params.append(parse_arrayoffset(i[1]['node'][1])+['()'])
    print(params)
    return params

def parse_arrayoffset(target):
    '''
    解析所有属性获取相关，可以解析数组或箭头调用
    返回一个列表，列表中每个元素都是一层属性
    :param target:
    :return:
    '''
    result = []
    if isinstance(target, dict):
        for key, value in target.items():
            if key == "name" and not isinstance(value, dict):
                result.append(str(value))
            elif key == "expr" and not isinstance(value, dict):
                result.append(str(value))
            else:
                result += parse_arrayoffset(value)
    elif isinstance(target, list):
        for item in target:
            result += parse_arrayoffset(item)
    return result


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
