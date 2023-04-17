from config import *
def chains_start(classes):
    chains=[]
    for i in classes:
        for j in i['methods']:
            if j['name'] in START_METHODS_PHP:
                chains.append([i['name'],j['name']])
    return chains