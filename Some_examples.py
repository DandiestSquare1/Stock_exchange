'''
Test cases for the stock exchange. 

Test is done by considering various
instances of the Simulation class,
with various buy/sell/mix cross types
for the supply and demand curves.

The expected results are provided in
the comments.
'''

from sortedcontainers import SortedDict
import matplotlib.pyplot as plt
import MatchingEngine

class Simulation(MatchingEngine.MatchingEngine):
    '''
    Attributes:
        MatchingEngine. Inherited.
    '''
    def __init__(self):
        MatchingEngine.MatchingEngine.__init__(self)
    def makeCumulativeBuys(self):
        '''
        Returns sorted dict with key=price,
        value=cumulative buy volume, equal
        to the volume of buys for the given
        price and higher.
        '''
        cumulative_buys=SortedDict()
        prevSize=0
        for x in self.buys.values():
            prevSize+=x[0]
        for p in self.buys.keys():
            cumulative_buys[p]=prevSize
            prevSize-=self.buys[p][0]
        return cumulative_buys
    def makeCumulativeSells(self):
        '''
        Returns sorted dict with key=price,
        value=cumulative sell volume, equal
        to the volume of sells for the given
        price and lower.
        '''
        cumulative_sells=SortedDict()
        prevSize=0
        for p in self.sells.keys():
            prevSize+=self.sells[p][0]
            cumulative_sells[p]=prevSize
        return cumulative_sells



# manual mix cross checker 1 #

simulation1=Simulation()
for c in range(12): 
    simulation1.addClient(c,10000,100)
simulation1.orderToClient={0: 1, 1: 5, 2: 3, 3: 0,\
4: 4, 5: 2, 6: 9, 7: 8, 8: 6, 9: 7,10:11,11:10}
simulation1.addOrder(11,'B',94.7,12)
simulation1.addOrder(9,'B',94.85,98)
simulation1.addOrder(10,'B',94.89,31)
simulation1.addOrder(0,'B',95.16,12)
simulation1.addOrder(4,'B',95.17,8)
simulation1.addOrder(8,'B',95.19,49)
simulation1.addOrder(3,'S',94.62,8)
simulation1.addOrder(2,'S',94.88,35)
simulation1.addOrder(6,'S',94.89,74)
simulation1.addOrder(7,'S',94.97,52)
simulation1.addOrder(1,'S',95.18,37)
simulation1.addOrder(5,'S',95.22,69)
print simulation1.matchOrders()
xb,yb=zip(*simulation1.makeCumulativeBuys().items())
xs,ys=zip(*simulation1.makeCumulativeSells().items())
supply_and_demand1=plt.figure(figsize=(10,6),dpi=300)
plt.plot(xb,yb,color='black',linestyle='-',\
drawstyle='steps-pre')
plt.plot(xs,ys,color='red',linestyle='-',\
drawstyle='steps-post')
plt.grid(True)
plt.xlabel('price')
plt.ylabel('volume')
plt.title('supply and demand')
plt.show()
supply_and_demand1.savefig("supply_and_demand1.pdf",\
dpi=300, facecolor='w', edgecolor='w',\
orientation='portrait', papertype=None, format=None,\
transparent=False, bbox_inches=None, pad_inches=0.1,\
frameon=None)

'''

After simulation1.fillOrders()
should return the simulation1.clients=

Client    Cash          Size
0         10759.12      92
1         8861.32       112
3         13321.15      65
4         9240.88       108 
6         5350.39       149
9         15408.73      43
11        7058.41       131

simulation1.buys=

price    size    id
94.70    12      11
94.85    98      9

simulation1.sells=

price    size    id
94.89    17      6
94.97    52      7
95.18    37      1
95.22    69      5

fillPrice=94.89
fillVolume=100

'''

# manual mix cross checker 2 #

simulation2=Simulation()
for c in range(18): 
    simulation2.addClient(c,10000,100)
simulation2.orderToClient={0: 6, 1: 4, 2: 8, 3: 2, 4: 7,\
5: 0, 6: 10, 7: 3, 8: 12, 9: 5,10:11,11:9,12:13,13:14,\
14:16,15:15,16:17,17:1}
simulation2.addOrder(5,'B',97.11,12)
simulation2.addOrder(17,'B',97.11,18)
simulation2.addOrder(1,'B',97.89,9)
simulation2.addOrder(9,'B',97.89,43)
simulation2.addOrder(2,'B',98.13,1)
simulation2.addOrder(11,'B',98.13,16)
simulation2.addOrder(8,'B',99.01,26)
simulation2.addOrder(12,'B',99.01,5)
simulation2.addOrder(14,'B',99.56,33)
simulation2.addOrder(16,'B',99.56,19)
simulation2.addOrder(3,'S',97.51,16)
simulation2.addOrder(7,'S',97.51,11)
simulation2.addOrder(0,'S',98.13,29)
simulation2.addOrder(4,'S',98.13,35)
simulation2.addOrder(6,'S',98.68,14)
simulation2.addOrder(10,'S',98.68,21)
simulation2.addOrder(13,'S',99.37,41)
simulation2.addOrder(15,'S',99.37,42)
print simulation2.matchOrders()
xb,yb=zip(*simulation2.makeCumulativeBuys().items())
xs,ys=zip(*simulation2.makeCumulativeSells().items())
supply_and_demand2=plt.figure(figsize=(10,6),dpi=300)
plt.plot(xb,yb,color='black',linestyle='-',\
drawstyle='steps-pre')
plt.plot(xs,ys,color='red',linestyle='-',\
drawstyle='steps-post')
plt.grid(True)
plt.xlabel('price')
plt.ylabel('volume')
plt.title('supply and demand')
plt.show()
supply_and_demand2.savefig("supply_and_demand2.pdf",\
dpi=300, facecolor='w',edgecolor='w',\
orientation='portrait', papertype=None,\
format=None,transparent=False, bbox_inches=None,\
pad_inches=0.1,frameon=None)

'''

After simulation.fillOrders()
should return the simulation2.clients=

Client    Cash          Size
6         12845.77      71
7         13434.55      65
2         11570.08      84
3         11079.43      89 
8         9901.87       101
12        7448.62       126
13        9509.35       105
16        6761.71       133
17        8135.53       119
9         9313.09       107


simulation2.buys=

price    size    id
97.11    12      5
97.11    18      17
97.89    9       1
97.89    43      9
98.13    9       11

simulation2.sells=

price    size    id
98.68    14      6
98.68    21      10
99.37    41      13
99.37    42      15

fillPrice=98.13
fillVolume=83

'''

# manual sell cross checker #

simulation3=Simulation()
for c in range(18): 
    simulation3.addClient(c,10000,100)
simulation3.orderToClient={0: 6, 1: 4, 2: 8, 3: 2, 4: 7,\
5: 0, 6: 10, 7: 3, 8: 12, 9: 5,10:11,11:9,12:13,13:14,\
14:16,15:15,16:17,17:1}
simulation3.addOrder(5,'B',97.11,12)
simulation3.addOrder(17,'B',97.11,18)
simulation3.addOrder(1,'B',97.89,9)
simulation3.addOrder(9,'B',97.89,43)
simulation3.addOrder(2,'B',98.09,1)
simulation3.addOrder(11,'B',98.09,16)
simulation3.addOrder(8,'B',99.01,26)
simulation3.addOrder(12,'B',99.01,5)
simulation3.addOrder(14,'B',99.56,33)
simulation3.addOrder(16,'B',99.56,19)
simulation3.addOrder(3,'S',97.51,16)
simulation3.addOrder(7,'S',97.51,11)
simulation3.addOrder(0,'S',98.13,29)
simulation3.addOrder(4,'S',98.13,35)
simulation3.addOrder(6,'S',98.68,14)
simulation3.addOrder(10,'S',98.68,21)
simulation3.addOrder(13,'S',99.37,41)
simulation3.addOrder(15,'S',99.37,42)
print simulation3.matchOrders()
xb,yb=zip(*simulation3.makeCumulativeBuys().items())
xs,ys=zip(*simulation3.makeCumulativeSells().items())
supply_and_demand3=plt.figure(figsize=(10,6),dpi=300)
plt.plot(xb,yb,color='black',linestyle='-',\
drawstyle='steps-pre')
plt.plot(xs,ys,color='red',linestyle='-',\
drawstyle='steps-post')
plt.grid(True)
plt.xlabel('price')
plt.ylabel('volume')
plt.title('supply and demand')
plt.show()
supply_and_demand3.savefig("supply_and_demand3.pdf",\
dpi=300, facecolor='w', edgecolor='w',\
orientation='portrait', papertype=None, format=None,\
transparent=False, bbox_inches=None, pad_inches=0.1,\
frameon=None)

'''

After simulation3.fillOrders()
should return the simulation3.clients=

Client    Cash         Size
12        7448.62      126
13        9509.35      105
16        6761.71      133
17        8135.53      119 
2         11570.08     84
3         11079.43     89
6         12845.77     71
7         12649.51     73


simulation3.buys=

price    size    id
97.11    12      5
97.11    18      17
97.89    9       1
97.89    43      9
98.09    1       2
98.09    16      11

simulation3.sells=

price    size    id
98.13    8       4
98.68    14      6
98.68    21      10
99.37    41      13
99.37    42      15

fillPrice=98.13
fillVolume=83

'''

# manual buy cross checker #

simulation4=Simulation()
for c in range(18): 
    simulation4.addClient(c,10000,100)
simulation4.orderToClient={0: 6, 1: 4, 2: 8, 3: 2, 4: 7,\
5: 0, 6: 10, 7: 3, 8: 12, 9: 5,10:11,11:9,12:13,13:14,\
14:16,15:15,16:17,17:1}
simulation4.addOrder(5,'B',97.28,12)
simulation4.addOrder(17,'B',97.28,18)
simulation4.addOrder(1,'B',97.95,9)
simulation4.addOrder(9,'B',97.95,43)
simulation4.addOrder(2,'B',98.19,16)
simulation4.addOrder(11,'B',98.19,16)
simulation4.addOrder(8,'B',99.01,26)
simulation4.addOrder(12,'B',99.01,5)
simulation4.addOrder(14,'B',99.56,33)
simulation4.addOrder(16,'B',99.56,19)
simulation4.addOrder(3,'S',97.51,16)
simulation4.addOrder(7,'S',97.51,11)
simulation4.addOrder(0,'S',98.13,29)
simulation4.addOrder(4,'S',98.13,35)
simulation4.addOrder(6,'S',98.68,14)
simulation4.addOrder(10,'S',98.68,21)
simulation4.addOrder(13,'S',99.37,41)
simulation4.addOrder(15,'S',99.37,42)
print simulation4.matchOrders()
xb,yb=zip(*simulation4.makeCumulativeBuys().items())
xs,ys=zip(*simulation4.makeCumulativeSells().items())
supply_and_demand4=plt.figure(figsize=(10,6),dpi=300)
plt.plot(xb,yb,color='black',linestyle='-',\
drawstyle='steps-pre')
plt.plot(xs,ys,color='red',linestyle='-',\
drawstyle='steps-post')
plt.grid(True)
plt.xlabel('price')
plt.ylabel('volume')
plt.title('supply and demand')
plt.show()
supply_and_demand4.savefig("supply_and_demand4.pdf",\
dpi=300, facecolor='w', edgecolor='w',\
orientation='portrait', papertype=None, format=None,\
transparent=False, bbox_inches=None, pad_inches=0.1,\
frameon=None)

'''

After simulation4.fillOrders()
should return the simulation4.clients=

Client    Cash         Size
2         11571.04     84
3         11080.09     89
6         12847.51     71
7         13436.65     65  
8         9214.48      108
12        7447.06      126
13        9509.05      105
16        6759.73      133
17        8134.39      119

simulation4.buys=

price    size    id
97.28    12      5
97.28    18      17
97.95    9       1
97.95    43      9
98.19    8       2
98.19    16      11

simulation4.sells=

price    size    id
98.68    14      6
98.68    21      10
99.37    41      13
99.37    42      15

fillPrice=98.19
fillVolume=91

'''
