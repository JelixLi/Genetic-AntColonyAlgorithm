import datetime
import math
import random
import unittest
from itertools import chain
import sys
import copy
import matplotlib.pyplot as plt
import csv

import genetic

PopSize = 0                
Position_Matrix = []        
Distance_Matrix = []       
Cities = 0          
ParentPopulation = []


def get_fitness(genes, idToLocationLookup):
    fitness = get_distance(idToLocationLookup[genes[0]],
                           idToLocationLookup[genes[-1]])

    for i in range(len(genes) - 1):
        start = idToLocationLookup[genes[i]]
        end = idToLocationLookup[genes[i + 1]]
        fitness += get_distance(start, end)

    return Fitness(round(fitness, 2))


def display(candidate, startTime):
    timeDiff = datetime.datetime.now() - startTime
    print("{}\t{}\t{}\t{}".format(
        ' '.join(map(str, candidate.Genes)),
        candidate.Fitness,
        candidate.Strategy.name,
        timeDiff))

def geographical_distance_sub(x,y):
    PI = 3.141592
    deg = round(x)
    min_val = x - deg 
    latitude = PI * (deg + 5.0*min_val/3.0) / 180.0
    deg = round(y)
    min_val = y - deg 
    longitude = PI * (deg + 5.0 * min_val / 3.0) / 180.0
    return latitude,longitude

def geographical_distance(locationA, locationB):
    RRR = 6378.388
    lat_1,lon_1 = geographical_distance_sub(locationA[0],locationA[1])
    lat_2,lon_2 = geographical_distance_sub(locationB[0],locationB[1])
    q1 = math.cos(lon_1 - lon_2)
    q2 = math.cos(lat_1 - lat_2)
    q3 = math.cos(lat_1 + lat_2)
    d = int(RRR*math.acos(0.5*((1.0+q1)*q2-(1.0-q1)*q3))+1.0)
    return d

def ATT_distance(locationA, locationB):
    xd = locationA[0] - locationB[0]
    yd = locationA[1] - locationB[1]
    rij = math.sqrt((xd*xd+yd*yd)/10.0)
    tij = round(rij)
    if tij<rij:
        return tij + 1
    else:
        return tij 

def EUC2d_distance(locationA,locationB):
    xd = locationA[0] - locationB[0]
    yd = locationA[1] - locationB[1]
    return round(math.sqrt(xd*xd + yd*yd))

def get_distance(locationA, locationB):
    # return geographical_distance(locationA,locationB)
    # return ATT_distance(locationA,locationB)
    return EUC2d_distance(locationA,locationB)

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

def mutate(genes, fnGetFitness):
    count = random.randint(2, len(genes))
    initialFitness = fnGetFitness(genes)
    while count > 0:
        count -= 1
        indexA, indexB = random.sample(range(len(genes)), 2)
        genes[indexA], genes[indexB] = genes[indexB], genes[indexA]
        fitness = fnGetFitness(genes)
        if fitness > initialFitness:
            return


def crossover(parentGenes, donorGenes, fnGetFitness):
    pairs = {Pair(donorGenes[0], donorGenes[-1]): 0}

    for i in range(len(donorGenes) - 1):
        pairs[Pair(donorGenes[i], donorGenes[i + 1])] = 0

    tempGenes = parentGenes[:]
    if Pair(parentGenes[0], parentGenes[-1]) in pairs:
        # find a discontinuity
        found = False
        for i in range(len(parentGenes) - 1):
            if Pair(parentGenes[i], parentGenes[i + 1]) in pairs:
                continue
            tempGenes = parentGenes[i + 1:] + parentGenes[:i + 1]
            found = True
            break
        if not found:
            return None

    runs = [[tempGenes[0]]]
    for i in range(len(tempGenes) - 1):
        if Pair(tempGenes[i], tempGenes[i + 1]) in pairs:
            runs[-1].append(tempGenes[i + 1])
            continue
        runs.append([tempGenes[i + 1]])

    initialFitness = fnGetFitness(parentGenes)
    count = random.randint(2, 20)
    runIndexes = range(len(runs))
    while count > 0:
        count -= 1
        for i in runIndexes:
            if len(runs[i]) == 1:
                continue
            if random.randint(0, len(runs)) == 0:
                runs[i] = [n for n in reversed(runs[i])]

        indexA, indexB = random.sample(runIndexes, 2)
        runs[indexA], runs[indexB] = runs[indexB], runs[indexA]
        childGenes = list(chain.from_iterable(runs))
        if fnGetFitness(childGenes) > initialFitness:
            return childGenes
    return childGenes


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
        # for i in range(5):
        #     ans = Perm(ans,idToLocationLookup)
        # ans_all.append(ans)
        # ans_all.append(Perm(ans,idToLocationLookup))
        ans_all.append(ans)
    return ans_all

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
    if nodes==None:
        return True
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

def check_opt(nodes,length):
    if len(nodes)!=length:
        return False
    check_dict = {}
    for n in nodes:
        if check_dict.get(n):
            return False
        check_dict[n] = True
    return True

class TravelingSalesmanTests(unittest.TestCase):

    # def test_att48(self):
    #     idToLocationLookup = readData("./data/rawdata/att48.tsp.csv")
    #     init_parents = ANN(idToLocationLookup)
    #     # init_parents = None
    #     optimalSequence = load_opt_data("att48.opt.tour")
    #     assert(check_opt(optimalSequence,48))
    #     assert(check(init_parents))
    #     self.solve(idToLocationLookup, optimalSequence,init_parents)

    # def test_berlin52(self):
    #     idToLocationLookup = readData("./data/rawdata/berlin52.tsp.csv")
    #     init_parents = ANN(idToLocationLookup)
    #     # init_parents = None
    #     optimalSequence = load_opt_data("berlin52.opt.tour")
    #     assert(check_opt(optimalSequence,52))
    #     assert(check(init_parents))
    #     self.solve(idToLocationLookup, optimalSequence,init_parents)

    # def test_eil101(self):
    #     idToLocationLookup = readData("./data/rawdata/eil101.tsp.csv")
    #     init_parents = ANN(idToLocationLookup)
    #     # init_parents = None
    #     optimalSequence = load_opt_data("eil101.opt.tour")
    #     assert(check_opt(optimalSequence,101))
    #     assert(check(init_parents))
    #     self.solve(idToLocationLookup, optimalSequence,init_parents)

    # def test_kroA100(self):
    #     idToLocationLookup = readData("./data/rawdata/kroA100.tsp.csv")
    #     init_parents = ANN(idToLocationLookup)
    #     # init_parents = None
    #     optimalSequence = load_opt_data("kroA100.opt.tour")
    #     assert(check_opt(optimalSequence,100))
    #     assert(check(init_parents))
    #     self.solve(idToLocationLookup, optimalSequence,init_parents)

    def test_kroA100(self):
        idToLocationLookup = readData("./data/rawdata/kroC100.tsp.csv")
        init_parents = ANN(idToLocationLookup)
        # init_parents = None
        optimalSequence = load_opt_data("kroC100.opt.tour")
        assert(check_opt(optimalSequence,100))
        assert(check(init_parents))
        self.solve(idToLocationLookup, optimalSequence,init_parents)

    # def test_benchmark(self):
    #     genetic.Benchmark.run(lambda: self.test_ulysses16())

    def solve(self, idToLocationLookup, optimalSequence,init_parents):
        geneset = [i for i in idToLocationLookup.keys()]

        def fnCreate():
            return random.sample(geneset, len(geneset))

        def fnDisplay(candidate):
            display(candidate, startTime)

        def fnGetFitness(genes):
            return get_fitness(genes, idToLocationLookup)

        def fnMutate(genes):
            mutate(genes, fnGetFitness)

        def fnCrossover(parent, donor):
            return crossover(parent, donor, fnGetFitness)

        optimalFitness = fnGetFitness(optimalSequence)
        print(optimalFitness)
        startTime = datetime.datetime.now()
        best = genetic.get_best(fnGetFitness, None, optimalFitness, None,
                                fnDisplay, fnMutate, fnCreate, maxAge=500,
                                poolSize=420, crossover=fnCrossover,init_parents=init_parents)

        self.assertTrue(not optimalFitness > best.Fitness)
        # genetic.get_best(fnGetFitness, None, optimalFitness, None,
        #                         fnDisplay, fnMutate, fnCreate, maxAge=500,
        #                         poolSize=25, crossover=fnCrossover,init_parents=init_parents)


def load_data(localFileName):
    """ expects:
        HEADER section before DATA section, all lines start in column 0
        DATA section element all have space in column  0
            <space>1 23.45 67.89
        last line of file is: " EOF"
    """
    with open(localFileName, mode='r') as infile:
        content = infile.read().splitlines()
    idToLocationLookup = {}
    for row in content:
        if "EOF" in row:
            break
        if row == " EOF":
            break
        if row[0] != ' ':  # HEADERS
            continue

        id, x, y = row.split(' ')[1:4]
        idToLocationLookup[int(id)] = [float(x), float(y)]
    return idToLocationLookup

def load_opt_data(localFileName):
    with open(localFileName, mode='r') as infile:
        content = infile.read().splitlines()
    idToLocationLookup = {}
    ret = []
    for row in content:
        ret.append(int(row))
    return ret

def load_data_1(localFileName):
    """ expects:
        HEADER section before DATA section, all lines start in column 0
        DATA section element all have space in column  0
            <space>1 23.45 67.89
        last line of file is: " EOF"
    """
    with open(localFileName, mode='r') as infile:
        content = infile.read().splitlines()
    idToLocationLookup = {}
    for row in content:
        id, x, y = row.split(' ')
        idToLocationLookup[int(id)] = [float(x), float(y)]
    return idToLocationLookup

def load_data_2(localFileName):
    """ expects:
        HEADER section before DATA section, all lines start in column 0
        DATA section element all have space in column  0
            <space>1 23.45 67.89
        last line of file is: " EOF"
    """
    with open(localFileName, mode='r') as infile:
        content = infile.read().splitlines()
    idToLocationLookup = {}
    for row in content:
        id, x, y = filter(None,row.split(' '))
        idToLocationLookup[int(id)] = [float(x), float(y)]
    return idToLocationLookup

class Fitness:
    def __init__(self, totalDistance):
        self.TotalDistance = totalDistance

    def __gt__(self, other):
        return self.TotalDistance < other.TotalDistance

    def __str__(self):
        return "{:0.2f}".format(self.TotalDistance)


class Pair:
    def __init__(self, node, adjacent):
        if node < adjacent:
            node, adjacent = adjacent, node
        self.Node = node
        self.Adjacent = adjacent

    def __eq__(self, other):
        return self.Node == other.Node and self.Adjacent == other.Adjacent

    def __hash__(self):
        return hash(self.Node) * 397 ^ hash(self.Adjacent)


if __name__ == '__main__':
    unittest.main()