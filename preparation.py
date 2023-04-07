# def find_evil_function(target_class,evil_functions):
#     for j in target_class['nodes']:
#         print(target_class['name'])
#         try:
#             if j['name'].lower() in evil_functions or j[0].lower() in evil_functions:
#                 print(j)
#         except:
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