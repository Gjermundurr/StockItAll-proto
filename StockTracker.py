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
        return f'Code: {self.code}, Description: {self.description}, Amount: {self.amount}'


class StockTracker(StockItem):
    """Operator-class between main.py and database

    Inherits the constructor of StockItem. StockTracker handles all interactions between main.py
    and the database. StockTracker receives an item objects containing item attributes and performs
    the needed function such as adding new items, modifying existing items, or returning the contents
    of the database.

     Class Attr:
     _filename: Name of database file
     _fields: Specifies dictionary keys to the csv module
     """

    _filename = 'StockTracker.csv'
    _fields = ['CODE', 'DESCRIPTION', 'AMOUNT']

    def AddItem(self):
        """ add a new stockItem to inventory database """

        temp_list = []
        #   First checks if the new items code already exists.
        with open(self._filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=self._fields)
            for row in reader:
                temp_list.append(row.get('CODE'))
            if str(self.code) in temp_list:
                return 'ERROR: Item code already in use!'

            else:
                #   No duplicate Item code was found, new object is appended to db
                with open(self._filename, 'a', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=self._fields)
                    writer.writerow(self.data)
                    return 'INFO: Item added to database!'

    def UpdateItem(self):
        """ update a stockItems amount by code """

        temp_list = []
        #   Append all rows in csv-file to a temporary list
        with open(self._filename, 'r', newline='') as csvfile_read:
            reader = csv.DictReader(csvfile_read, fieldnames=self._fields)
            for row in reader:
                temp_list.append(row)

        #   Find the matching "code" and set new "amount"
        for item in temp_list:
            if str(self.code) == item.get('CODE'):
                item['AMOUNT'] = self.amount

        #   Write back all entries in temp_list
        with open(self._filename, 'w', newline='') as csvfile_write:
            writer = csv.DictWriter(csvfile_write, fieldnames=self._fields)
            for line in temp_list:
                writer.writerow(line)
            return 'INFO: Item updated!'

    def ReturnItem(self):
        """ Display all details of a specific item by code """

        with open(self._filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=self._fields)
            #   Search each row in csv-file after the supplied "code" that matches both in number and length
            for row in reader:
                if str(self.code) in row.get('CODE') and len(str(self.code)) == len(row.get('CODE')):
                    return row  # Returns the full row of found item

    def ReturnInventory(self):
        """ Return entire inventory of database"""

        filename = 'StockTracker.csv'
        fields = ['CODE', 'DESCRIPTION', 'AMOUNT']
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=fields)
            for row in reader:  # A generator that yields each row in CSV file one by one
                yield row
