import csv


class StockItem:
    """ Stock-Item constructor class """

    def __init__(self, code: int, description: str, amount: int):
        """ The constructor contains all required arguments for a Stockitem to be created """
        self.code = code
        self.description = description
        self.amount = amount

        #   Give all items an attribute with a dictionary containing its details
        self.data = {'CODE': self.code, 'DESCRIPTION': self.description, 'AMOUNT': self.amount}


class StockTracker:
    """ Back-end Management class of Stock-item objects to be used by CLI-menu and Tkinter GUI app """

    def __init__(self, code=None, description=None, amount=None, item=None, data=None):
        """ arguments for when specific arguments are needed by different method calls """
        self.code = code
        self.description = description
        self.amount = amount
        self.item = item
        self.data = data

    def addItem(self):
        """ add a new stockItem to inventory database """
        temp_list = []
        fields = ['CODE', 'DESCRIPTION', 'AMOUNT']
        with open('stockdata.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=fields)
            for row in reader:
                temp_list.append(row.get('CODE'))
            if str(self.code) in temp_list:
                return 'An item already exists with this code!'

            else:
                with open('stockdata.csv', 'a', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fields)
                    writer.writerow(self.data)
                    return 'Item added to inventory!'


    def updateItem(self):
        """ update a stockItems amount by code """

        fields = ['CODE', 'DESCRIPTION', 'AMOUNT']
        data = []  # temp list for modifying item entry
        #   Reads the contents of the csv-file to a temporary list object filled with each item-dictionary
        with open('stockdata.csv', 'r', newline='') as csvfile_read:
            reader = csv.DictReader(csvfile_read, fieldnames=fields)
            for row in reader:
                data.append(row)

        #   Searches the temporary list for the given keyword and changes its dictionary "amount"
        for item in data:
            if item.get('CODE') == str(self.code):
                item['AMOUNT'] = self.amount

        #   Open the csv-file in write-mode and re-write all entries from the temporary list
        with open('stockdata.csv', 'w', newline='') as csvfile_write:  # Overwrite the database with new changes
            writer = csv.DictWriter(csvfile_write, fieldnames=fields)
            for line in data:
                writer.writerow(line)
        data.clear()  # Clear list data after its function is done

    def displayItem(self):
        """ Display all details of a item when given code """

        fields = ['CODE', 'DESCRIPTION', 'AMOUNT']
        with open('stockdata.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=fields)
            #   Search each row in csv-file after the supplied "code" that matches both in number and length
            for row in reader:
                if str(self.code) in row.get('CODE') and len(str(self.code)) == len(row.get('CODE')):
                    return row  # Returns the full row

    def displayInventory(self):
        """ Display entire stock inventory"""

        fields = ['CODE', 'DESCRIPTION', 'AMOUNT']
        with open('stockdata.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=fields)
            for row in reader:  # A generator that yields each row one by one
                yield row
