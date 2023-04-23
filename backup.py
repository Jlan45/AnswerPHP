# def parse_FunctionCall(target):
#     value=[]
#     current_node = target[1]
#     value.append(f"{current_node['name']}({current_node['params']})")
#     return value
# def parse_MethodCall(target):
#     value=[]
#     current_node = target[1]
#     value.append(f"{current_node['name']}({current_node['params']})")
#     try:
#         current_node = current_node['node'][1]
#     except:
#         pass
#     while isinstance(current_node, dict):
#         if "name" in current_node:
#             value.append(current_node["name"])
#         try:
#             current_node = current_node["node"][1]
#         except:
#             break
#     return value


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