from copy import copy

from config import *
class findTheChain:
    def __init__(self, classes):
        self.classes = classes
        self.chains = self.chains_start()
        self.finalChains=[]
    def chains_start(self):
        chains=[]
        for i in self.classes:
            for j in i['methods']:
                if j['name'] in START_METHODS_PHP:
                    chains.append([[i['name'],j['name']]])
        return chains
    def chains_find(self):
        while self.chains:
            tmp_chain=self.chains.pop() #这个变量不许乱动啊喂，因为这个是后面所有链子分析的基础
            print(tmp_chain)
            # print(self.chains)
            a=copy(self.chains)
            a.append(tmp_chain)
            tmp_class=self.find_class(tmp_chain[-1][0])
            if self.contains_loop(tmp_chain):
                continue
            for i in EVIL_CALL:
                if tmp_chain[-1][0]==i[0] and tmp_chain[-1][-1]==i[-1]:
                    self.finalChains.append(tmp_chain)
            if tmp_chain[-1][-1] in tmp_class['evils']:
                self.finalChains.append(tmp_chain)
            if self.find_method(tmp_class,tmp_chain[-1][-1]):
                #这里是找对应method中调用的其他method，比如在a方法中调用了b，c方法，就会返回b，c方法组成的列表
                for i in self.find_method(tmp_class,tmp_chain[-1][-1]):
                    #i是能产生联系的方法名
                    for cls in self.classes:
                        #对所有class进行遍历
                        for j in cls['methods']:
                            # if j['name']==i['name'] or j['name']=='__call': 这里先保留一下对call的处置，后面可能需要单独来一个列表存放这些东西

                            if j['name']==i['name'] or j['name']=='__call':
                                tmp=copy(tmp_chain)
                                tmp.append([cls['name'],j['name']])
                                self.chains.append(tmp)
            if self.find_magic_call(tmp_class,tmp_chain[-1][-1]):
                for i in self.find_magic_call(tmp_class,tmp_chain[-1][-1]):
                    #i是能产生联系的方法名
                    for cls in self.classes:
                        #对所有class进行遍历
                        for j in cls['methods']:
                            if j['name']==i:
                                if tmp_class['name']==cls['name'] and tmp_chain[-1][-1]==i:
                                    continue
                                tmp=copy(tmp_chain)
                                tmp.append([cls['name'],j['name']])
                                self.chains.append(tmp)
            if self.find_func(tmp_class,tmp_chain[-1][-1]):
                for i in self.find_magic_call(tmp_class,tmp_chain[-1][-1]):
                    try:
                        # print(i['name'])
                        if i['name'][0][0]=="$":
                            self.finalChains.append(tmp_chain+"anyFunc")
                    except:
                        continue
            if self.find_obj_as_func(tmp_class,tmp_chain[-1][-1]):
                for cls in self.classes:
                    for j in cls['methods']:
                        if j['name'] == "__invoke" or j['name'] == "__call":
                            if tmp_class['name'] == cls['name'] and tmp_chain[-1][-1] == i:
                                continue
                            tmp = copy(tmp_chain)
                            tmp.append([cls['name'], j['name']])
                            self.chains.append(tmp)
            if self.find_to_get(tmp_class, tmp_chain[-1][-1]):
                for cls in self.classes:
                    for j in cls['methods']:
                        if j['name'] == "__get":
                            if tmp_class['name'] == cls['name'] and tmp_chain[-1][-1] == i:
                                continue
                            tmp = copy(tmp_chain)
                            tmp.append([cls['name'], j['name']])
                            self.chains.append(tmp)
            '''
            这里需要对每个chains写三份判断
            1、确定某方法中是否有恶意方法，有的话直接连带方法名压入✅
            2、确定某方法能不能走下去，能走下去就连带下一条链子压入，这里判断的是有没有其他类中方法的直接调用✅
            3、确定某方法能不能走下去，能走下去就连带下一条链子压入，这里判断的是有没有通过调用函数的方式间接调用到了其他类的方法✅
            4、判断当前的链子中是否存在两个以上的相同loop，有就弹出
            5、对get方法专门写一个单独的判断
            6、对__call和__invoke写单独判断
            不管123哪个方法生效，都会将原始链子弹出，这样就顺便实现了链子走不下去的困境
            '''
    def find_class(self,classname):
        for i in self.classes:
            if i['name']==classname:
                return i
    def find_func(self,targetclass,methodname):
        for i in targetclass['methods']:
            if i['name'] == methodname:
                return i['funcs']
    def find_method(self,targetclass, methodname):
        for i in targetclass['methods']:
            if i['name'] == methodname:
                return i['methods']
    def find_magic_call(self,targetclass, methodname):
        #这里echo应该要对参数判断下的
        MAGIC_FUNC=[]
        for i in FUNC_TO_CALL:
            MAGIC_FUNC.append(i[0])
        magic_list=[]
        for i in targetclass['methods']:
            if i['name'] == methodname:
                for j in i['funcs']:
                    if j['name'] in MAGIC_FUNC:
                        if j['name']=='echo':
                        #直接ban掉echo没有用到参数的
                            if not j['params'][0]:
                                continue
                        for k in FUNC_TO_CALL:
                            if k[0]==j['name']:
                                magic_list.append(k[1])
        return magic_list

    def find_obj_as_func(self,targetclass, methodname):
        for i in targetclass['methods']:
            if i['name'] == methodname:
                for j in i['methods']:
                    if "$" in j['name'][0]:
                        return True
        return False
    def find_to_get(self,targetclass, methodname):
        for i in targetclass['methods']:
            if i['name'] == methodname:
                for j in i['funcs']+i['methods']:
                    try:
                        for k in j['params']:
                            if len(k)>=2:
                                return True
                    except:
                        continue

    def contains_loop(self,lst):
        for chainlen in range(int((len(lst) + 1) / 2), 1, -1):
            for j in range(len(lst) - chainlen + 1):
                a = (str(lst[j:j + chainlen])[1:-1])
                if (str(lst).count(a)) > MAX_LOOPBACK+1:
                    return True
        return False

