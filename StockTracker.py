import csv


class StockItem:
    """StockItem object constructor class

    The StockItem class is used as a constructor for new inventory item objects and specifies the ID,
    description, and 'amount of items'. Further operations and maintenance of item objects are
    handled by the child-class StockTracker.

    Args:
    code (int): A unique code to reference each item
    description (str): A brief description of the item
    amount (int): How many of said item are in stock
    data (dict): A dictionary containing all information about the object
    """

    def __init__(self, code: int = None, description: str = None, amount: int = None):
        self.code = code
        self.description = description
        self.amount = amount
        self.data = {'CODE': self.code, 'DESCRIPTION': self.description, 'AMOUNT': self.amount}

    def __str__(self):
        return 'Object of StockItem class: An object containing details about a stock-item'


class StockTracker(StockItem):
    """Management of interactions between main.py and database

    StockTracker handles all interactions between main.py and the database. StockTracker includes methods for
    adding new items to database, updating specific item's inventory, or displaying the contents of the database.

     Args:
     _filename: Class variable for name of database file
     _fields: Class variable used by csv module to specify dictionary keys
     """

    _filename = 'StockTracker.csv'
    _fields = ['CODE', 'DESCRIPTION', 'AMOUNT']


    def addItem(self):
        """ add a new stockItem to inventory database """

        temp_list = []
        #   First checks if the new items code already exists.
        with open(self._filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=self._fields)
            for row in reader:
                temp_list.append(row.get('CODE'))
            if str(self.code) in temp_list:
                temp_list.clear()  # reset temp_list for next method call
                return 'Error: Item already exists!'

            else:
                #   Item is added if it its code is unique
                with open(self._filename, 'a', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=self._fields)
                    writer.writerow(self.data)
                    temp_list.clear()  # reset temp_list for next method call
                    return f"INFO: Item added by Server! Code: {self.data['CODE']}," \
                           f" Description: {self.data['DESCRIPTION']}, Amount: {self.data['AMOUNT']}"

    def updateItem(self):
        """ update a stockItems amount by code """

        csv_data = []  # temp list for modifying item entry
        #   Reads the contents of the csv-file to a temporary list object filled with each item-dictionary
        with open(self._filename, 'r', newline='') as csvfile_read:
            reader = csv.DictReader(csvfile_read, fieldnames=self._fields)
            for row in reader:
                csv_data.append(row)

        #   Searches the temporary list for the given keyword and changes its dictionary "amount"
        for item in csv_data:
            if str(self.code) == item.get('CODE'):
                item['AMOUNT'] = self.amount

        #   Open the csv-file in write-mode and re-write all entries from the temporary list
        with open(self._filename, 'w', newline='') as csvfile_write:
            writer = csv.DictWriter(csvfile_write, fieldnames=self._fields)
            for line in csv_data:
                writer.writerow(line)

            csv_data.clear()  # Clear list data after its function is done
            return 'INFO: Item updated!'


    def displayItem(self):
        """ Display all details of a item when given code """

        with open(self._filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=self._fields)
            #   Search each row in csv-file after the supplied "code" that matches both in number and length
            for row in reader:
                if str(self.code) in row.get('CODE') and len(str(self.code)) == len(row.get('CODE')):
                    return row  # Returns the full row of found item


    def displayInventory(self):
        """ Return entire inventory of database

        """

        filename = 'StockTracker.csv'
        fields = ['CODE', 'DESCRIPTION', 'AMOUNT']
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=fields)
            for row in reader:  # A generator that yields each row in CSV file one by one
                yield row

