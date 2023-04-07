import json
import config
import preparation
with open("output.json","r")as f:
    a=json.load(f)
Classes=[]
for i in a:
    if i[0]=="Class":
        Classes.append(i[1])
for i in Classes:
    print(i)
    preparation.search_target_str(i,config.EVIL_FUNCTION_PHP)
    print(i['nodes'][3][1]['name'])
#['nodes'][3][1]['name']这个层级为类中方法位置