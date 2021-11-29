import math

PopSize = 0                
Position_Matrix = []        
Distance_Matrix = []       
Cities = 0          
ParentPopulation = [] 

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

def get_distance(locationA, locationB):
    sideA = locationA[0] - locationB[0]
    sideB = locationA[1] - locationB[1]
    sideC = math.sqrt(sideA * sideA + sideB * sideB)
    return sideC

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

def Perm(nodes,idToLocationLookup):
    dists = []
    for i in range(len(nodes)):
        dists.append(get_distance(idToLocationLookup[nodes[i]],idToLocationLookup[nodes[(i+1)%len(nodes)]]))
    sorted_dists = sorted(dists)
    max_dist_index = (dists.index(sorted_dists[-1]) + 1) % len(nodes)
    min_dist_index = dists.index(sorted_dists[-2])
    smaller_index = min(max_dist_index,min_dist_index)
    bigger_index = max(max_dist_index,min_dist_index)
    if ((smaller_index + 1) % len(nodes) == bigger_index) or (smaller_index==bigger_index):
        return nodes
    return nodes[:smaller_index+1] + list(reversed(nodes[smaller_index+1:bigger_index+1])) + nodes[bigger_index+1:]

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

def test():
    idToLocationLookup = load_data("ulysses22.tsp")
    # nodes = ANN(idToLocationLookup)
    # print(nodes)
    # print(check(nodes))

    # idToLocationLookup = load_data_1("att48.tsp")
    nodes = ANN(idToLocationLookup)
    assert(check(nodes))
    print(nodes)


test()