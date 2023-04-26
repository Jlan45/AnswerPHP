import json
import sys
import config
from preparation import *
import php2json
from config import *
from findthechain import findTheChain

def GAMESTART(input_file="input.php"):
    try:
        with open(input_file,"r")as inf:
            with open("output.json","w")as outf:
                php2json.php2json(inf.read(),outf)
    #抓取错误
    except FileNotFoundError:
        print("请检查输入文件是否存在")
        exit()
    Classes=[]
    with open("output.json","r")as f:
        OringinalClasses=get_the_classes(f)
    for i in OringinalClasses:
        Classes.append(prepare_class(i))
    for i in Classes:
        i['evils']=find_evil(i, EVIL_FUNCTION_PHP)
        i['calls']=find_calls(i,FUNC_TO_CALL)
    with open("output.json", "w") as f:
        json.dump(Classes, f)
    WORKING=findTheChain(Classes)
    WORKING.chains_find()
    print(WORKING.finalChains)
if __name__=="__main__":
    # print(sys.argv)
    input_file="test.php"
    GAMESTART(input_file)

