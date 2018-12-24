import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

G = nx.DiGraph()
f=open("./hw3dataset/graph_1.txt","r")  
f_list=[]
count=0
index=0
for line in f.readlines():
    line = line.strip()
    Init_list_1=line.split(',')
    for i in Init_list_1:
        count+=1
        if(count==1):
            index=int(i)
        elif(count==2):
            G.add_edge(index,int(i))
            count=0
nx.draw_networkx(G)
#plt.show() 

def pagerank(G, alpha=0.15, personalization=None, 
             max_iter=100, tol=1.0e-6, nstart=None, weight='weight', 
             dangling=None): 
    if len(G) == 0: 
        return {} 
    #若圖不是有向圖，將它變成有向圖
    if not G.is_directed(): 
        D = G.to_directed() 
    else: 
        D = G 
  
    W = nx.stochastic_graph(D, weight=weight) 
    N = W.number_of_nodes() 
  
    # 如果沒有給予初始節點，會選擇固定的起始向量
    if nstart is None: 
        x = dict.fromkeys(W, 1.0 / N) 
    else: 
        # 正規化起始向量
        s = float(sum(nstart.values())) 
        x = dict((k, v / s) for k, v in nstart.items()) 
  
    if personalization is None: 
        # 如果沒有給出，則統一分配同一個個人化向量
        p = dict.fromkeys(W, 1.0 / N) 
    else: 
        missing = set(G) - set(personalization) 
        if missing: 
            raise NetworkXError('Personalization dictionary '
                                'must have a value for every node. '
                                'Missing nodes %s' % missing) 
        s = float(sum(personalization.values())) 
        p = dict((k, v / s) for k, v in personalization.items()) 
  
    if dangling is None: 
        # 如果未指定懸掛向量，就要使用個性化向量
        dangling_weights = p 
    else: 
        missing = set(G) - set(dangling) 
        if missing: 
            raise NetworkXError('Dangling node dictionary '
                                'must have a value for every node. '
                                'Missing nodes %s' % missing) 
        s = float(sum(dangling.values())) 
        dangling_weights = dict((k, v/s) for k, v in dangling.items()) 
    dangling_nodes = [n for n in W if W.out_degree(n, weight=weight) == 0.0] 
  
    #開始進行迭代
    for _ in range(max_iter): 
        xlast = x 
        x = dict.fromkeys(xlast.keys(), 0) 
        danglesum = alpha * sum(xlast[n] for n in dangling_nodes) 
        for n in x: 
            # 這是一個向左乘的矩陣乘法運算
            for nbr in W[n]: 
                x[nbr] += alpha * xlast[n] * W[n][nbr][weight] 
            x[n] += danglesum * dangling_weights[n] + (1.0 - alpha) * p[n] 
        # 檢查是否收斂 
        err = sum([abs(x[n] - xlast[n]) for n in x]) 
        if err < N*tol: 
            return x 
    raise NetworkXError('pagerank: power iteration failed to converge '
                        'in %d iterations.' % max_iter) 
page_score=nx.pagerank(G,0.3) #設定damp factor
print(page_score) 