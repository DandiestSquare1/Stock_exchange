from sortedcontainers import SortedDict

class ClientBook:
    '''
    Attributes:    
        clients. SortedDict with the key=client ID,
        value=[cash,shares] list describing the
        portfolio of the client.
        
        orderToClient. SortedDict with the key=order ID,
        value=client ID, of the client who submitted the
        given order.
    '''
    def __init__(self):
        self.clients=SortedDict() 
        self.orderToClient=SortedDict()
    def addClient(self,clientID,cash,shares):
        '''
        Adds a new client.
        
        Arguments:      
            clientID. ID of the client to be added.
            
            cash. Client's endowment of cash.
            
            shares. Client's endowment of shares.
            
        Return:    
            void
        '''
        self.clients[clientID]=[cash,shares]
    def modifyClient(self,clientID,changeOfCash,\
                     changeOfShares):
        '''
        Modifies the client record.
     
        Arguments:    
            clientID. ID of the client to be modified.
            
            changeOfCash. Change of cash.
            
            changeOfShares. Change of shares.
            
        Return:
            void.
        '''
        self.clients[clientID][0]+=changeOfCash
        self.clients[clientID][1]+=changeOfShares
    def deleteClient(self,clientID):
        '''
        Deletes the client from the "clients" records.
        
        Arguments:
            clientID. ID of the client to be deleted.
            
        Return:
            void.
        '''
        del self.clients[clientID]
