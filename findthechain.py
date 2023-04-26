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
            tmp_class=self.find_class(tmp_chain[-1][0])
            if self.contains_loop(tmp_chain):
                continue
            if tmp_chain[-1][-1] in tmp_class['evils']:

                self.finalChains.append(tmp_chain)
            if self.find_method(tmp_class,tmp_chain[-1][-1]):
                #这里写完了对method产生的联系
                for i in self.find_method(tmp_class,tmp_chain[-1][-1]):
                    for cls in self.classes:
                        for j in cls['methods']:
                            if j['name']==i['name']:
                                tmp=copy(tmp_chain)
                                tmp.append([cls['name'],j['name']])
                                self.chains.append(tmp)
            '''
            这里需要对每个chains写三份判断
            1、确定某方法中是否有恶意方法，有的话直接连带方法名压入
            2、确定某方法能不能走下去，能走下去就连带下一条链子压入，这里判断的是有没有其他类中方法的直接调用
            3、确定某方法能不能走下去，能走下去就连带下一条链子压入，这里判断的是有没有通过调用函数的方式间接调用到了其他类的方法
            4、判断当前的链子中是否存在两个以上的相同loop，有就弹出
            不管123哪个方法生效，都会将原始链子弹出，这样就顺便实现了链子走不下去的困境
            '''
    def find_class(self,classname):
        for i in self.classes:
            if i['name']==classname:
                return i

    def find_method(self,targetclass, methodname):
        for i in targetclass['methods']:
            if i['name'] == methodname:
                return i['methods']

    def contains_loop(self,chain):
        return False




