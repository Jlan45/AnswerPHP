from copy import copy

from config import *
def chains_start(classes):
    chains=[]
    for i in classes:
        for j in i['methods']:
            if j['name'] in START_METHODS_PHP:
                chains.append([[i['name'],j['name']]])
    return chains
def chains_find(classes,chains):
    finalChains=[]
    for i in chains:
        tmpChain=copy(i)
        for j in classes:
            if i[-1][0]==j['name']:
                for k in j['methods']:
                    if k['name']==i[-1][-1]:
                        for f in k['funcs']:
                            if f['name'] in EVIL_FUNCTION_PHP:
                                tmpChain.append([f['name']])
                                finalChains.append(tmpChain)
                break
    print(finalChains)
    print(chains)
    return chains