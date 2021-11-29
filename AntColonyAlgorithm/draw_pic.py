import matplotlib.pyplot as plt
import datetime
from dateutil.parser import parse
import numpy as np

def extract_x(data):
    ret = []
    cnt = 2
    while cnt<len(data):
        ret.append(data[cnt])
        cnt = cnt +3
    return ret

def extract_y(data):
    ret = []
    cnt = 1
    while cnt<len(data):
        ret.append(data[cnt])
        cnt = cnt +3
    return ret

def extract_label(data):
    ret = []
    cnt = 0
    while cnt<len(data):
        ret.append(data[cnt])
        cnt = cnt +3
    return ret

# att48_data = [
#     1,62941,"0:00:00.047264",
#     2,62837,"0:00:00.094575",
#     15,62836,"0:00:00.919075",
#     24,62821,"0:00:01.753755",
#     49,62789,"0:00:03.762629",
#     55,62782,"0:00:04.253036",
#     93,62771,"0:00:06.874738",
#     99,62768,"0:00:07.636988",
#     226,62735,"0:00:15.119854",
#     656,62731,"0:00:43.612388"
# ]

# name = "att48"
# x = extract_x(att48_data)
# y = extract_y(att48_data)
# label = extract_label(att48_data)

# berlin52_data = [
#     1,10261,"0:00:00.250955",
#     2,10200,"0:00:00.510132",
#     3,10125,"0:00:00.763560",
#     21,9914,"0:00:02.608082",
#     31,9709,"0:00:03.957160",
#     115,9572,"0:00:13.271679",
#     126,9182,"0:00:14.478865"
# ]

# name = "berlin52"
# x = extract_x(berlin52_data)
# y = extract_y(berlin52_data)
# label = extract_label(berlin52_data)

# eil101_data = [
#     1,2053,"0:00:00.645683",
#     2,1874,"0:00:01.287729",
#     4,981,"0:00:02.125567",
#     5,964,"0:00:02.322905",
#     6,950,"0:00:02.521654",
#     7,949,"0:00:02.720050",
#     11,916,"0:00:03.515716",
#     152,906,"0:00:59.526204",
#     223,903,"0:01:25.987383",
#     667,880,"0:04:02.210596"
# ]

# name = "eil101"
# x = extract_x(eil101_data)
# y = extract_y(eil101_data)
# label = extract_label(eil101_data)

# kroA100_data = [
#     1,36138,"0:00:00.547365",
#     3,35959,"0:00:00.942182",
#     4,33087,"0:00:01.487845",
#     55,32679,"0:00:18.604772",
#     146,31212,"0:00:47.033598"
# ]

# name = "kroA100"
# x = extract_x(kroA100_data)
# y = extract_y(kroA100_data)
# label = extract_label(kroA100_data)

kroC100_data = [
    1,34466,"0:00:00.540847",
    2,33843,"0:00:01.080898",
    7,32609,"0:00:02.740020",
    17,32211,"0:00:06.468261",
    75,32045,"0:00:23.663628",
    104,31312,"0:00:33.986574",
    191,31267,"0:00:58.141543",
    883,30022,"0:04:36.484492"
]

name = "kroC100"
x = extract_x(kroC100_data)
y = extract_y(kroC100_data)
label = extract_label(kroC100_data)

plt.switch_backend('agg')
plt.figure()
plt.xlabel("time(H:M:S)")
plt.ylabel("distance")
plt.xticks(rotation=10)
plt.xticks(fontsize=6)
plt.plot(x, y,"--co",label=name)
for i in range(len(label)):
    plt.text(x[i],y[i]+155,label[i], fontsize=10, color = "c", style = "italic", weight = "light", verticalalignment='center', horizontalalignment='right', rotation=0)
plt.savefig(name+".png")