import csv


class StockItem:
    ''' Stock-Item constructor class '''


    def __init__(self, code: int, description: str, amount: int):
        '''Create stock-item object with unique ID-tag, description and amount of item '''

        self.code = code
        self.description = description
        self.amount = amount

        self.data = {'Code': self.code, 'Description': self.description, 'Amount': self.amount}


class StockTracker(StockItem):
    ''' Management class of Stock-item objects to be used by CLI-menu '''


    def addItem(self):
        ''' add a new stockItem to inventory '''

        with open('StockTracker.data', 'ab') as stocktracker_data_file:
            pickle.dump(self.data, stocktracker_data_file)




    def updateItem(self):
        ''' update a stockItem '''
        pass


    def getItem(self):
        ''' return a stockTtem when given key/value '''
        pass


    def getIndex(self):
        ''' return the key/value of stockItem when given code (id) '''
        pass


    def getDetails(self):
        ''' return details of a specific stockItem '''
        pass


    def listItems(self):
        ''' return the entire inventory of stockItems '''
        pass


