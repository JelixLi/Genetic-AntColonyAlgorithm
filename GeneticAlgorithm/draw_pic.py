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
    cnt = 0
    while cnt<len(data):
        ret.append(data[cnt])
        cnt = cnt +3
    return ret

def extract_label(data):
    ret = []
    cnt = 1
    while cnt<len(data):
        ret.append(data[cnt])
        cnt = cnt +3
    return ret

# att48_data = [
#     12861.00,"Create","0:00:00.000190",
#     12435.00,"Create","0:00:00.000263",
#     12012.00,"Create","0:00:00.000570",
#     11991.00,"Mutate","0:00:09.965714"
# ]

# name = "att48"
# x = extract_x(att48_data)
# y = extract_y(att48_data)
# label = extract_label(att48_data)

# berlin52_data = [
#     10929.00,"Create","0:00:00.000164",
#     10072.00,"Create","0:00:00.000514",
#     9461.00,"Create","0:00:00.000565",
#     9395.00,"Create","0:00:00.001057",
#     9304.00,"Create","0:00:00.001106",
#     8206.00,"Create","0:00:00.001443",
#     8181.00,"Create","0:00:00.001527"
# ]

# name = "berlin52"
# x = extract_x(berlin52_data)
# y = extract_y(berlin52_data)
# label = extract_label(berlin52_data)

# eil101_data = [
#     803.00,"Create","0:00:00.000263",
#     777.00,"Create","0:00:00.000489",
#     774.00,"Create","0:00:00.001671",
#     764.00,"Create","0:00:00.001764",
#     763.00,"Create","0:00:00.001849",
#     746.00,"Create","0:00:00.002116"
# ]

# name = "eil101"
# x = extract_x(eil101_data)
# y = extract_y(eil101_data)
# label = extract_label(eil101_data)

# kroA100_data = [
#     27807.00,"Create","0:00:00.000289",
#     26133.00,"Create","0:00:00.000404",
#     25647.00,"Create","0:00:00.002252",
#     25525.00,"Create","0:00:00.003227",
#     25420.00,"Create","0:00:00.003658",
#     24698.00,"Create","0:00:00.006046"
# ]

# name = "kroA100"
# x = extract_x(kroA100_data)
# y = extract_y(kroA100_data)
# label = extract_label(kroA100_data)

kroC100_data = [
    26227.00,"Create","0:00:00.000263",
    25968.00,"Create","0:00:00.000367",
    25519.00,"Create","0:00:00.000453",
    23660.00,"Create","0:00:00.000600",
    23606.00,"Crossover","0:00:35.368867"
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
    plt.text(x[i],y[i]+85,label[i], fontsize=10, color = "c", style = "italic", weight = "light", verticalalignment='center', horizontalalignment='right', rotation=0)
plt.savefig(name+".png")