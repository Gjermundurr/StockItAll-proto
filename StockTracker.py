import csv


class StockItem:
    ''' Stock-Item constructor class '''

    def __init__(self, code: int, description: str, amount: int):
        '''Create stock-item object with unique ID-tag, description and amount of item '''

        self.code = code
        self.description = description
        self.amount = amount

        self.data = {'CODE': self.code, 'DESCRIPTION': self.description, 'AMOUNT': self.amount}         # create dict object attribute for each item created


class StockTracker:
    ''' Management class of Stock-item objects to be used by CLI-menu '''

    def __init__(self, code=None, description=None, amount=None, item=None):
        self.code = code
        self.description = description
        self.amount = amount
        self.item = item

    def addItem(self):
        ''' add a new stockItem to inventory database '''

        fields = ['CODE', 'DESCRIPTION', 'AMOUNT']
        with open('stockdata.csv', 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writerow(self.data)


    def updateItem(self):
        ''' update a stockItems amount by code '''

        fields = ['CODE', 'DESCRIPTION', 'AMOUNT']
        data = []   # temp list for modifying item entry
        # reads the contents of the csv-file to a temporary list object filled with each item-dictionary
        with open('stockdata.csv', 'r', newline='') as csvfile_read:
            reader = csv.DictReader(csvfile_read, fieldnames=fields)
            for row in reader:
                data.append(row)

        # Searches the temporary list for the given keyword and changes its "amount"
        for item in data:
            if item.get('CODE') == str(self.code):
                item['AMOUNT'] = self.amount
        #
        with open('stockdata.csv', 'w', newline='') as csvfile_write:   # Overwrite the database with new changes
            writer = csv.DictWriter(csvfile_write, fieldnames=fields)
            for line in data:
                writer.writerow(line)
        data.clear()    # Clear list data after its function is done



    def DisplayItem(self):
        ''' Display all details of a item when given code '''

        fields = ['CODE', 'DESCRIPTION', 'AMOUNT']
        with open('stockdata.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=fields)
            for row in reader:
                if str(self.code) in row.get('CODE') and len(str(self.code)) == len(row.get('CODE')):
                    return row                                              # Returns the dictionary of selected code




    def DisplayInventory(self):
        ''' Display entire stock inventory'''

        fields = ['CODE', 'DESCRIPTION', 'AMOUNT']
        with open('stockdata.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=fields)
            for row in reader:
                yield row




