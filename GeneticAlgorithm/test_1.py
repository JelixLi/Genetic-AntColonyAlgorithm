import random
import sys
import copy
import matplotlib.pyplot as plt
import csv
import math

PopSize = 0                
Position_Matrix = []        
Distance_Matrix = []       
Cities = 0          
ParentPopulation = []    

def get_distance(locationA, locationB):
    sideA = locationA[0] - locationB[0]
    sideB = locationA[1] - locationB[1]
    sideC = math.sqrt(sideA * sideA + sideB * sideB)
    return sideC

def readData(path):
    global Position_Matrix,Cities,Distance_Matrix
    file = open(path)
    f_csv = csv.reader(file,delimiter=' ') 
    idToLocationLookup = {}
    for row in f_csv:
        Position_Matrix.append([row[1],row[2]])
        idToLocationLookup[int(row[0])] = [float(row[1]), float(row[2])]
    Cities = len(Position_Matrix)
    for i in range(Cities):
        Distance_Matrix.append([])
        for j in range(Cities):
            if i == j :
                Distance_Matrix[i].append(0)
                continue
            # x = float(Position_Matrix[i][0])-float(Position_Matrix[j][0])
            # y = float(Position_Matrix[i][1])-float(Position_Matrix[j][1])
            # Distance_Matrix[i].append(round(math.sqrt(math.pow(x,2) + math.pow(y,2))))
            locationA = [float(Position_Matrix[i][0]),float(Position_Matrix[j][0])]
            locationB = [float(Position_Matrix[i][1]),float(Position_Matrix[j][1])]
            Distance_Matrix[i].append(get_distance(locationA,locationB))
    return idToLocationLookup

def deleteCurNode(ind,nodes):
    return nodes[:ind] + nodes[ind+1:]

def getNodeWithMinDist(cur_node,nodes,idToLocationLookup):
    dists = [get_distance(idToLocationLookup[cur_node],idToLocationLookup[n]) for n in nodes]
    d = nodes[dists.index(min(dists))]
    return d

def ANN(idToLocationLookup):
    nodes = list(idToLocationLookup.keys())
    ans_all = []
    for n in nodes:
        cur_node = n 
        ans = [cur_node]
        temp_nodes = nodes[:]
        for i in range(len(nodes)-1):
            temp_nodes = deleteCurNode(temp_nodes.index(cur_node),temp_nodes)
            cur_node = getNodeWithMinDist(cur_node,temp_nodes,idToLocationLookup)
            ans.append(cur_node)
        ans_all.append(Perm(ans,idToLocationLookup))
    return ans_all


def rule(_path,cityi,cityj,cityk,cityl):
    path = []
    idxi,idxj,idxk = _path.index(cityi),_path.index(cityj),_path.index(cityk)
    for i in range(idxi+1):
        path.append(_path[i])
    for i in range(idxk,idxj-1,-1):
        path.append(_path[i])
    if _path[0] != cityl:
        idxl = _path.index(cityl)
        for i in range(idxl,Cities):
            path.append(_path[i])
    return path

def fitness(path):
    length = 0
    for i in range(Cities-1):
        length = length + Distance_Matrix[path[i]-1][path[i+1]-1]
    length = length + Distance_Matrix[path[Cities-1]-1][path[0]-1]
    return 1/length

def Perm(_path,idToLocationLookup):
    edges,sidelen = [],[]
    for i in range(0,Cities-1):
        edges.append([_path[i],_path[i+1]])
    edges.append([_path[Cities-1],_path[0]])
    for i in range(0,Cities):
        sidelen.append(Distance_Matrix[edges[i][0]-1][edges[i][1]-1])
    temp = copy.deepcopy(sidelen)
    idx1 = temp.index(max(temp))
    temp[idx1] == -1
    while(True):
        idx2 = temp.index(max(temp))
        if idx2!=idx1-1 and idx2!=idx1+1:
            break
        else:
            temp[idx2] == -1
    tempidx = idx1
    idx1 = idx1 if idx1<idx2 else idx2
    idx2 = tempidx
    cityi,cityj = edges[idx1][0],edges[idx1][1]
    cityk,cityl = edges[idx2][0],edges[idx2][1]
    path_perm1 = rule(_path,cityi,cityj,cityk,cityl)
    minlen = sys.maxsize
    for i in range(Cities):
        for j in range(Cities):
            if minlen>Distance_Matrix[i][j] and edges.count([i,j])!=1 and i!=j:
                minlen = Distance_Matrix[i][j]
                cityi,cityj = i+1,j+1
    for i in range(len(edges)):
        if edges[i][0]== cityi:
            idx1 = i
        if edges[i][0] == cityj:
            idx2 = i
    tempidx = idx1
    idx1 = idx1 if idx1<idx2 else idx2
    idx2 = tempidx        
    cityi,cityj = edges[idx1][0],edges[idx1][1]
    cityk,cityl = edges[idx2][0],edges[idx2][1]
    path_perm2 = rule(_path,cityi,cityj,cityk,cityl)            
    minlen = sys.maxsize
    for i in range(Cities):
        for j in range(Cities):
            if minlen>Distance_Matrix[i][j] and edges.count([i,j])!=1 and i!=j:
                minlen = Distance_Matrix[i][j]
                for k in range(len(edges)):
                    if edges[k][0] == i+1:
                        idx1 = k
                    if edges[k][0] == j+1:
                        idx2 = k
    tempidx = idx1
    idx1 = idx1 if idx1<idx2 else idx2
    idx2 = tempidx        
    cityi,cityj = edges[idx1][0],edges[idx1][1]
    cityk,cityl = edges[idx2][0],edges[idx2][1]
    path_perm3 = rule(_path,cityi,cityj,cityk,cityl)
    temp = copy.deepcopy(sidelen)
    idx1 = temp.index(max(temp))
    cityi = edges[idx1][0]
    minlen = sys.maxsize
    for i in range(len(edges)):
        if i !=idx1-1 and i!=idx1+1 and minlen>Distance_Matrix[edges[idx1][0]-1][edges[i][1]-1]:
            minlen = Distance_Matrix[edges[idx1][0]-1][edges[i][1]-1]
            idx2 = i
    tempidx = idx1
    idx1 = idx1 if idx1<idx2 else idx2
    idx2 = tempidx        
    cityi,cityj = edges[idx1][0],edges[idx1][1]
    cityk,cityl = edges[idx2][0],edges[idx2][1]
    path_perm4 = rule(_path,cityi,cityj,cityk,cityl)
    path_perm = [_path,path_perm1,path_perm2,path_perm3,path_perm4]
    minPath =[]
    minfitness = sys.maxsize
    for i in range(len(path_perm)):
        if minfitness > fitness(path_perm[i]):
            minfitness = fitness(path_perm[i])
            minPath = copy.deepcopy(path_perm[i])
    return minPath

def check(nodes):
    for nn in nodes:
        check_dict = {}
        for n in nn:
            if check_dict.get(n):
                return False
            check_dict[n] = True
    s = len(nodes[0])
    for nn in nodes:
        if not len(nn)==s:
            return False
    return True

if __name__ == '__main__':
    idToLocationLookup = readData("./data/rawdata/att48.tsp.csv")
    nodes = ANN(idToLocationLookup)
    assert(check(nodes))
    print(nodes)