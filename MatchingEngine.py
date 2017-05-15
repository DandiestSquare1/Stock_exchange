import ClientBook
import OrderBook

class MatchingEngine(OrderBook.OrderBook,ClientBook.ClientBook):
    '''
    Attributes: 
        OrderBook. Inherited.
        
        ClientBook. Inherited.
    '''
    def __init__(self):
        OrderBook.OrderBook.__init__(self)
        ClientBook.ClientBook.__init__(self)
    def matchOrders(self):
        '''
        Match the orders from the buy and sell sides.
        
        Return:
            crossType,fillPrice. Tuple, where crossType
            is 'b', 's', 'm', or 'n' cross type, and fillPrice
            is the price at the cross intersection of the
            supply and demand curves.
            
            fillPrice=-1 and crossType='n' when no crossing
            was possible.
            'b' - buy cross type.
            's' - sell cross type.
            'm' -  mixed cross type.
        '''
        if len(self.buys)==0 or len(self.sells)==0 or\
            self.buys.keys()[-1]<self.sells.keys()[0]:
            crossType='n'
            fillPrice=-1
            return crossType,fillPrice
        if self.buys.keys()[-1]==self.sells.keys()[0]:
            crossType='m'
            fillPrice=self.sells.keys()[0]
            return crossType,fillPrice
        allPrices=sorted(list(set(list(self.buys.keys())+\
                                list(self.sells.keys()))))
        fillPrice=0
        total_buys=0
        for x in self.buys.values():
            total_buys+=x[0] 
        total_sells=0
        crossType=''
        for x in allPrices: 
            trig=False
            if x in self.buys.keys():
                total_buys-=self.buys[x][0]
                crossType='b'
                trig=True
            if x in self.sells.keys():
                total_sells+=self.sells[x][0]
                crossType='s'
                if trig:
                    crossType='m'
            if total_buys<=total_sells:
                fillPrice=x
                break
        return crossType,fillPrice
    def fillOrders(self):
        '''
        Fill all the orders in the order book,
        after determining whether supply and demand
        have intersected, and if they have, at what
        price and under what crossing type. The
        orders at fillPrice, when only part
        of them can be filled, are processed by the
        FIFO principle.
        
        Return:
            void.
        '''
        crossType,fillPrice=self.matchOrders()
        if crossType=='n':
            return
        sellsFilled=0
        buysFilled=0
        for p in self.sells.keys(): 
            if p>=fillPrice: 
                break
            v=self.sells[p] 
            sellsFilled+=v[0] 
            for orderID in v[1]: 
                clientID=self.orderToClient[orderID]
                size=self.all_orders[orderID][2] 
                self.modifyClient(clientID,fillPrice*size,-size) 
                del self.all_orders[orderID]
            del self.sells[p] 
        for p in self.buys.keys()[::-1]: 
            if p<=fillPrice:
                break
            v=self.buys[p] 
            buysFilled+=v[0]
            for orderID in v[1]:
                clientID=self.orderToClient[orderID]
                size=self.all_orders[orderID][2] 
                self.modifyClient(clientID,-fillPrice*size,+size)
                del self.all_orders[orderID]
            del self.buys[p] 
        if crossType=='b': 
            diff=sellsFilled-buysFilled 
            for orderID in self.buys[fillPrice][1]: 
                clientID=self.orderToClient[orderID]
                size=self.all_orders[orderID][2]
                if size>=diff: 
                    self.modifyClient(clientID,-fillPrice*diff,+diff) 
                    self.modifyOrder(orderID,size-diff) 
                    if self.all_orders[orderID][2]==0:
                        del self.all_orders[orderID]
                    break
                self.modifyClient(clientID,-fillPrice*size,+size)
                self.buys[fillPrice][0]-=size
                diff-=size
                del self.all_orders[orderID]
            if self.buys[fillPrice][0]==0: 
                del self.buys[fillPrice]
            if fillPrice in self.buys:
                newSet=OrderedSet()
                for orderID in self.buys[fillPrice][1]:
                    if orderID in self.all_orders:
                        newSet.add(orderID)
                self.buys[fillPrice][1]=newSet
        if crossType=='s':
            diff=buysFilled-sellsFilled 
            for orderID in self.sells[fillPrice][1]: 
                size=self.all_orders[orderID][2]
                clientID=self.orderToClient[orderID]
                if size>=diff: 
                    self.modifyClient(clientID,fillPrice*diff,-diff) 
                    self.modifyOrder(orderID,size-diff)
                    if self.all_orders[orderID][2]==0:
                        del self.all_orders[orderID]
                    break
                self.modifyClient(clientID,fillPrice*size,-size) 
                self.sells[fillPrice][0]-=size
                diff-=size
                del self.all_orders[orderID]
            if self.sells[fillPrice][0]==0:
                del self.sells[fillPrice]
            if fillPrice in self.sells:
                newSet=OrderedSet()
                for orderID in self.sells[fillPrice][1]:
                    if orderID in self.all_orders:
                        newSet.add(orderID)
                self.sells[fillPrice][1]=newSet
        if crossType=='m': 
            if sellsFilled+self.sells[fillPrice][0]==\
                    buysFilled+self.buys[fillPrice][0]:
                for orderID in self.sells[fillPrice][1]:
                    size=self.all_orders[orderID][2]
                    sellsFilled+=size
                    del self.all_orders[orderID] 
                    clientID=self.orderToClient[orderID]
                    self.modifyClient(clientID,fillPrice*size,-size) 
                del self.sells[fillPrice]
                for orderID in self.buys[fillPrice][1]:
                    size=self.all_orders[orderID][2]
                    buysFilled+=size
                    del self.all_orders[orderID] 
                    clientID=self.orderToClient[orderID]
                    self.modifyClient(clientID,-fillPrice*size,+size)
                del self.buys[fillPrice]
            elif sellsFilled+self.sells[fillPrice][0]<\
                    buysFilled+self.buys[fillPrice][0]:
                for orderID in self.sells[fillPrice][1]:
                    clientID=self.orderToClient[orderID]
                    size=self.all_orders[orderID][2]
                    sellsFilled+=size
                    del self.all_orders[orderID] 
                    self.modifyClient(clientID,fillPrice*size,-size) 
                del self.sells[fillPrice]
                diff=sellsFilled-buysFilled
                for orderID in self.buys[fillPrice][1]:
                    clientID=self.orderToClient[orderID]
                    size=self.all_orders[orderID][2]
                    if size>=diff: 
                        self.modifyClient(clientID,-fillPrice*diff,+diff) 
                        self.modifyOrder(orderID,size-diff) 
                        if self.all_orders[orderID][2]==0:
                            del self.all_orders[orderID]
                        break
                    self.modifyClient(clientID,-fillPrice*size,+size) 
                    del self.all_orders[orderID] 
                    self.buys[fillPrice][0]-=size
                    diff-=size
                if self.buys[fillPrice][0]==0:
                    del self.buys[fillPrice]
                else: 
                    newSet=OrderedSet()
                    for orderID in self.buys[fillPrice][1]:
                        if orderID in self.all_orders:
                            newSet.add(orderID)
                    self.buys[fillPrice][1]=newSet
            elif sellsFilled+self.sells[fillPrice][0]>\
                    buysFilled+self.buys[fillPrice][0]:
                for orderID in self.buys[fillPrice][1]: 
                    clientID=self.orderToClient[orderID]
                    size=self.all_orders[orderID][2]
                    buysFilled+=size
                    del self.all_orders[orderID]
                    self.modifyClient(clientID,-fillPrice*size,+size) 
                del self.buys[fillPrice]
                diff=buysFilled-sellsFilled 
                for orderID in self.sells[fillPrice][1]:
                    clientID=self.orderToClient[orderID]
                    size=self.all_orders[orderID][2]
                    if size>=diff: 
                        self.modifyClient(clientID,fillPrice*diff,-diff) 
                        self.modifyOrder(orderID,size-diff) 
                        if self.all_orders[orderID][2]==0:
                            del self.all_orders[orderID]
                        break
                    self.modifyClient(clientID,fillPrice*size,-size)
                    del self.all_orders[orderID] 
                    self.sells[fillPrice][0]-=size
                    diff-=size
                if self.sells[fillPrice][0]==0:
                    del self.sells[fillPrice]
                else:
                    newSet=OrderedSet()
                    for orderID in self.sells[fillPrice][1]:
                        if orderID in self.all_orders:
                            newSet.add(orderID)
                    self.sells[fillPrice][1]=newSet



