import csv
import sys
import random
import copy
import math
import numpy as np
import matplotlib.pyplot as plt
import datetime

M = 25       #蚂蚁数量
Alpha = 1    #信息素重要程度因子
Beta = 5  #启发函数重要程度因子
RHO = 0.1 #信息素挥发因子
Q = 100     #常系数
HEU = []  #启发函数
TAU = []  #信息素矩阵

Cities = 0 #城市数量
Position_Matrix = []
Distance_Matrix = [] #距离矩阵
Ant_Paths = [] #MxN的矩阵，用来记录每个蚂蚁的路径
Path_Length = [] #每条蚂蚁路径的长度

Iter_Max = 1000 #迭代次数
Best_Path = []  #每一次迭代的最佳路径
Best_Length = sys.maxsize #最佳路径长度
Set_City = []

def ATT_distance(locationA, locationB):
    xd = locationA[0] - locationB[0]
    yd = locationA[1] - locationB[1]
    rij = math.sqrt((xd*xd+yd*yd)/10.0)
    tij = round(rij)
    if tij<rij:
        return tij + 1
    else:
        return tij 

#读入数据，并得到位置矩阵和距离矩阵
def readData(path):
    global Position_Matrix,Cities,Distance_Matrix,Set_City,HEU
    file = open(path)
    f_csv = csv.reader(file,delimiter=' ') 
    for row in f_csv:
        Position_Matrix.append([row[1],row[2]])
        global Cities
    Cities = len(Position_Matrix)
    for i in range(Cities):
        Distance_Matrix.append([])
        for j in range(Cities):
            if i == j :
                Distance_Matrix[i].append(0)
                continue
            x = float(Position_Matrix[i][0])-float(Position_Matrix[j][0])
            y = float(Position_Matrix[i][1])-float(Position_Matrix[j][1])
            Distance_Matrix[i].append(round(math.sqrt(math.pow(x,2) + math.pow(y,2))))
            # Distance_Matrix[i].append(ATT_distance([float(Position_Matrix[i][0]),float(Position_Matrix[j][0])],[float(Position_Matrix[i][1]),float(Position_Matrix[j][1])]))
    for i in range(1,Cities+1):
        Set_City.append(i)
    for i in range(Cities):
        HEU.append([])
        for j in range(Cities):
            if i==j:
                HEU[i].append(0)
                continue
            HEU[i].append(1/Distance_Matrix[i][j])
            
#计算每个蚂蚁的路径距离
def pathLength():
    global Path_Length
    for i in range(M):
        length = 0
        for j in range(Cities-1):
            length = length + Distance_Matrix[Ant_Paths[i][j]-1][Ant_Paths[i][j+1]-1]
        length = length + Distance_Matrix[Ant_Paths[i][Cities-1]-1][Ant_Paths[i][0]-1]
        Path_Length.append(length)

#更新信息素
def updateTAU():
    global TAU
    Delta_Tau = [[0 for i in range(Cities)] for j in range(Cities)]
    for i in range(M):
        for j in range(Cities-1):
            Delta_Tau[Ant_Paths[i][j]-1][Ant_Paths[i][j+1]-1] = Delta_Tau[Ant_Paths[i][j]-1][Ant_Paths[i][j+1]-1] + Q/Path_Length[i]
        Delta_Tau[Ant_Paths[i][Cities-1]-1][Ant_Paths[i][0]-1] = Delta_Tau[Ant_Paths[i][Cities-1]-1][Ant_Paths[i][0]-1] + Q/Path_Length[i]
    for i in range(Cities):
        for j in range(Cities):
            TAU[i][j] = (1-RHO)*TAU[i][j] + Delta_Tau[i][j]

#更新全局信息素
def updateGlobalPheromone():
    global TAU
    minlen = min(Path_Length)
    idx = Path_Length.index(minlen)
    bestpath = Ant_Paths[idx]
    for j in range(Cities-1):
        TAU[bestpath[j]-1][bestpath[j+1]-1] = TAU[bestpath[j]-1][bestpath[j+1]-1] + 100/minlen
    TAU[bestpath[Cities-1]-1][bestpath[0]-1] = TAU[bestpath[Cities-1]-1][bestpath[0]-1] + 100/minlen

#多样性
def diversity():
    Dmin = min(Path_Length)
    Dmax = max(Path_Length)
    Daverage = np.mean(Path_Length)
    ED = (Daverage-Dmin)/(Dmax-Dmin)
    if ED>=0.5:
        return True #SA
    else: 
        return False #Mutation

#模拟退火算法
def SA(path):
    coldingrate = 0.99
    initPath = copy.deepcopy(path)
    Temperature = 100
    oldPath = initPath
    oldlen = getPathLength(oldPath)
    while Temperature > 10:
        newPath = getNewPath(oldPath)
        newlen = getPathLength(newPath)
        delta = newlen-oldlen
        if delta<0 or math.exp(-(delta/Temperature))>random.uniform(0,1):
            oldlen = newlen
            oldPath = copy.deepcopy(newPath)
        Temperature = coldingrate*Temperature
    return oldPath

#变异操作
def mutation(path):
    k1 = random.randint(0,Cities-1)
    if k1 == Cities-1:
        k2 = 0
    else:
        k2 = k1+1
    temp = path[k1]
    path[k1] = path[k2]
    path[k2] = temp


def getPathLength(path):
    length = 0
    for j in range(Cities-1):
        length = length + Distance_Matrix[path[j]-1][path[j+1]-1]
    length = length + Distance_Matrix[path[Cities-1]-1][path[0]-1]
    return length

def getNewPath(oldPath):
    path = copy.deepcopy(oldPath)
    k1 = random.randint(0,Cities-1)
    k2 = random.randint(0,Cities-1)
    temp = path[k1]
    path[k1] = path[k2]
    path[k2] = temp
    return path

#运行
def run():
    start = datetime.datetime.now()

    global Ant_Paths,TAU,Best_Path,Best_Length
    TAU = [[0.5 for i in range(Cities)] for j in range(Cities)]

    for i in range(Iter_Max):
        # if i%20==0:  
        #     print("迭代次数",i)
        #随机产生起点城市
        for j in range(M):
            r = random.randint(1,Cities)
            Ant_Paths.append([r])
        #逐个蚂蚁路径选择
        for j in range(M):
            currant = Ant_Paths[j][0]
            for k in range(1,Cities):
                hasVisited = list(set(Ant_Paths[j]).intersection(set(Set_City)))
                notVisited = list(set(Set_City)-set(hasVisited))
                
                #总的转移概率
                sumprob = 0
                for m in range(len(notVisited)):
                    sumprob = sumprob + math.pow(TAU[currant-1][notVisited[m]-1],Alpha)*math.pow(HEU[currant-1][notVisited[m]-1],Beta)
                #计算城市之间的转移概率
                p = []
                for m in range(len(notVisited)):
                    p.append(math.pow(TAU[currant-1][notVisited[m]-1],Alpha)*math.pow(HEU[currant-1][notVisited[m]-1],Beta)/sumprob)
                
                #选择下一个城市
                choose_n = math.ceil(len(p)/2)
                sample = random.sample(p,choose_n)
                nextCity = notVisited[p.index(max(sample))]
                Ant_Paths[j].append(nextCity)
                currant = nextCity    
        pathLength()#计算每个蚂蚁的路径长度
        updateTAU()#更新信息素
        #按照论文的内容加入模拟退火和变异操作
        diversityCondition = diversity()
        if diversityCondition:
            for n in range(M):
                newPath = SA(Ant_Paths[n]) #模拟退火
                Ant_Paths[n] = newPath
        else:
            for n in range(M):
                r = random.random()
                if r <0.1:
                    mutation(Ant_Paths[n]) #变异操作
        Path_Length.clear()
        pathLength()#再次计算每个蚂蚁的路径长度
        updateGlobalPheromone()
        
        bl = min(Path_Length)       
        if bl < Best_Length:
            Best_Path = Ant_Paths[Path_Length.index(bl)]
            Best_Length = bl    
            print(i+1,Best_Length,datetime.datetime.now()-start)   
        Path_Length.clear()
        Ant_Paths.clear() #清空准备下一次迭代  
    print(Best_Path)


if __name__ == '__main__':
    # readData("./data/rawdata/att48.tsp.csv")
    # readData("./data/rawdata/berlin52.tsp.csv")
    # readData("./data/rawdata/eil101.tsp.csv")
    # readData("./data/rawdata/kroA100.tsp.csv")
    readData("./data/rawdata/kroC100.tsp.csv")
    run()
    
