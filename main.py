import json
import config
from preparation import *
import php2json
from findthechain import *
from config import *
# with open("output.json","r")as f:
#     a=json.load(f)
# OringinalClasses=[]
# for i in a:
#     if i[0]=="Class":
#         OringinalClasses.append(i[1])
# for i in OringinalClasses:
#     print(i)
#     preparation.search_target_str(i,config.EVIL_FUNCTION_PHP)
#     print(i['nodes'][3][1]['name'])
# #['nodes'][3][1]['name']这个层级为类中方法位置






if __name__=="__main__":
    Classes=[]
    input_file="input.php"
    try:
        with open(input_file,"r")as inf:
            with open("output.json","w")as outf:
                php2json.php2json(inf.read(),outf)
    #抓取错误
    except FileNotFoundError:
        print("请检查输入文件是否存在")
        exit()
    with open("output.json","r")as f:
        # print(f.read())
        OringinalClasses=get_the_classes(f)
    for i in OringinalClasses:
        Classes.append(prepare_class(i))
    for i in Classes:
        i['evils']=find_evil(i, EVIL_FUNCTION_PHP)
    with open("output.json", "w") as f:
        json.dump(Classes, f)

    chains=chains_start(Classes)
    chains_find(Classes,chains)