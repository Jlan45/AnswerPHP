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
            print(tmp_chain[-1][0])
            tmp_class=self.find_class(tmp_chain[-1][0])
            if self.contains_loop(tmp_chain):
                continue
            if tmp_chain[-1][-1] in tmp_class['evils']:
                self.finalChains.append(tmp_chain)
            '''
            这里需要对每个chains写三份判断
            1、确定某方法中是否有恶意方法，有的话直接连带方法名压入
            2、确定某方法能不能走下去，能走下去就连带下一条链子压入
            不管12哪个方法生效，都会将原始链子弹出，这样就顺便实现了链子走不下去的困境
            '''
    def find_class(self,classname):
        for i in self.classes:
            if i['name']==classname:
                return i
    def contains_loop(self,chain):
        return False




