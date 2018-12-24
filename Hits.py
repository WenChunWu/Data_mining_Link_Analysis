import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

G = nx.DiGraph()
f=open("./hw3dataset/graph_1.txt","r")  #讀檔
f_list=[]
count=0
index=0
#每行讀取
for line in f.readlines():
    line = line.strip() 
    Init_list_1=line.split(',') #將逗號刪除
    for i in Init_list_1: #將每行讀到的數值add到G中
        count+=1
        if(count==1):
            index=int(i)
        elif(count==2):
            G.add_edge(index,int(i)) #加入到G中
            count=0

nx.draw_networkx(G)
plt.show() 

#Hits演算法
def hits(G,max_iter=None,tol=1.0e-8,nstart=None,normalized=True):
    if type(G) == nx.MultiGraph or type(G) == nx.MultiDiGraph: #若有多個邊同時加入同一個node中，會顯示錯誤
        raise Exception("hits() not defined for graphs with multiedges.")
    if len(G) == 0:
        return {},{}
    # 如果沒有給予初始節點，會選擇固定的起始向量
    if nstart is None:
        h=dict.fromkeys(G,1.0/G.number_of_nodes())
    else:
        h=nstart
        # 正規化起始向量
        s=1.0/sum(h.values())
        for k in h:
            h[k]*=s
    i=0
    while True: # 開始進行迭代
        hlast=h
        h=dict.fromkeys(hlast.keys(),0)
        a=dict.fromkeys(hlast.keys(),0)
        # 這是一個向左乘的矩陣乘法運算
        for n in h:
            for nbr in G[n]:
                a[nbr]+=hlast[n]*G[n][nbr].get('weight',1)
        # 乘上h=Ga
        for n in h:
            for nbr in G[n]:
                h[n]+=a[nbr]*G[n][nbr].get('weight',1)
        # 正規化向量
        s=1.0/max(h.values())
        for n in h: h[n]*=s
        # 正規化向量
        s=1.0/max(a.values())
        for n in a: a[n]*=s
        # 檢查是否收斂
        err=sum([abs(h[n]-hlast[n]) for n in h])
        if err < tol:
            break
        if i>max_iter:
            raise NetworkXError(\
            "HITS: power iteration failed to converge in %d iterations."%(i+1))
        i+=1
    if normalized: #若normalized，則會將Hub及Authority進行正規化，加總各為1
        s = 1.0/sum(a.values())
        for n in a:
            a[n] *= s
        s = 1.0/sum(h.values())
        for n in h:
            h[n] *= s
    return h,a
h,a=nx.hits(G)
print('Hub:',h)
print('Authority',a)
