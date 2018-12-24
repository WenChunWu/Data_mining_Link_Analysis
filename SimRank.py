import numpy as np

#輸入想要開啟的文件檔，因為要算開啟那個檔案的node數
choose = '' 
while(choose not in ['1', '2', '3', '4', '5']):
	print ('Enter the number to open the file(number1~5):')
	choose = input('graph: ')
	if (choose == '1'):
		nodeNum = 6
		fileName = './hw3dataset/graph_1.txt'
	elif (choose == '2'):
		nodeNum = 5
		fileName = './hw3dataset/graph_2.txt'
	elif (choose == '3'):
		nodeNum = 4
		fileName = './hw3dataset/graph_3.txt'
	elif (choose == '4'):
		nodeNum = 7
		fileName = './hw3dataset/graph_4.txt'
	elif (choose == '5'):
		nodeNum = 469
		fileName = './hw3dataset/graph_5.txt'

file = open(fileName) 

#不同圖的初始節點
inlinks = [0]*(nodeNum)
graph = np.zeros((nodeNum, nodeNum))
graph_T = np.zeros((nodeNum, nodeNum))

#讀檔並進行資料前處理
for line in file:
	line = line.replace('\n', '')
	link = line.split(',')
	#print (link[0], link[1])
	graph[int(link[0])-1][int(link[1])-1] = 1
	#print(graph[int(link[0])][int(link[1])])

#正規化每個節點的總連接值
def normalized(inlinks, graph, nodeNum):
	for i in range(nodeNum):
		for j in range(nodeNum):
			if graph[j][i] == 1:
				inlinks[i] += 1
	for i in range(nodeNum):
		for j in range(nodeNum):
			if graph[j][i] != 0:
				graph[j][i] = graph[j][i]/inlinks[i]
def simRank (graph, nodeNum):
	sim_value = np.mat(np.identity(nodeNum))
	for i in range(10):
		C = 0.5
		sim_value_new = C*graph.T*sim_value*graph
		for i in range(nodeNum):
			sim_value_new[i,i] = 1
		sim_value = sim_value_new
	return sim_value

normalized(inlinks, graph, nodeNum)
graph = np.mat(graph)
sim_value = simRank (graph,nodeNum)
print ('SimRank value:')
print (sim_value)