class OrderBook:
    '''
    Attributes: 
        buys. SortedDict with key=price,
        value=[size,{orderID's}], where size
        is the total size of the buy orders at
        this price level, and {orderID's} are
        the ID's of the buy orders at this level.
        
        sells. SortedDict with key=price,
        value=[size,{orderID's}], where size
        is the total size of the sell orders at
        this price level, and {orderID's} are
        the ID's of the sell orders at this level.   
        
        all_orders. SortedDict with key=orderID,
        and value=[side,price,size], which maintains
        the side (buy or sell), limit price and size
        of each order, identified by its order ID.
    '''
    def __init__(self):
        self.buys=SortedDict() 
        self.sells=SortedDict() 
        self.all_orders=SortedDict() 
    def addOrder(self,orderID,side,price,size):
        '''
        Adds a new order to the book.
        
        Arguments:
            orderID. The ID of the order to be added.
            
            side. The buy ('B') or sell ('S').
            
            size. The size of the order to be added.
            
        Return:
            void.
        '''
        self.all_orders[orderID]=[side,price,size]
        if side=='B':
            if price not in self.buys.keys():
                self.buys[price]=[0,OrderedSet()]
            self.buys[price][0]+=size 
            self.buys[price][1].add(orderID) 
        elif side=='S':
            if price not in self.sells.keys():
                self.sells[price]=[0,OrderedSet()] 
            self.sells[price][0]+=size 
            self.sells[price][1].add(orderID)
    def cancelOrder(self,orderID):
        '''
        Cancels the given order from the book.
        
        Arguments:
            orderID. The ID of the order to be cancelled.
            
        Return:
            void.
        '''
        [side,price,size]=self.all_orders[orderID]
        del self.all_orders[orderID]
        if side=='B':
            self.buys[price][0]-=size
            self.buys[price][1].remove(orderID)
            if self.buys[price][0]==0: 
                del self.buys[price]
        elif side=='S':
            self.sells[price][0]-=size
            self.sells[price][1].remove(orderID)
            if self.sells[price][0]==0:
                del self.sells[price]
    def modifyOrder(self,orderID,newSize):
        '''
        Modifies the given order in the book,
        assigning it a new size.
        
        Arguments:
            orderID. The ID of the order to be modified.
            
            newSize. Change the size of the given order
            to this value.
            
        Return:
            void.
        '''
        [side,price,size]=self.all_orders[orderID]
        self.all_orders[orderID][2]+=(newSize-size)
        if side=='B':
            self.buys[price][0]+=newSize-size
        if side=='S':
            self.sells[price][0]+=newSize-size
