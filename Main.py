''' Server program '''
from StockTracker import *


def main_menu():
    print('''
    -------------------------------------------------------
    StockItAll System Interface
    -------------------------------------------------------
    (1)\t\tAdd a new item to stock
    (2)\t\tUpdate a stock items Code and Amount
    (3)\t\tDisplay item details by Code 
    (4)\t\tDisplay entire inventory list
    
    (5)\t\tExit
    ''')
    select = int(input('\tSelect your choice: '))



    def menu_1():
        code = int(input('Enter a stock code: '))
        description = input('Enter item description: ')
        amount = int(input('Enter item stock: '))
        new_item = StockTracker(code=code, description=description, amount=amount)
        new_item.addItem()

    def menu_2():
        pass

    def menu_3():
        pass


    def menu_4():
        pass


    def menu_5():
        pass


    if select == 1:
        menu_1()
    elif select == 2:
        pass
    elif select == 3:
        pass
    elif select == 4:
        pass
    elif select == 5:
        pass




if __name__ == '__main__':

    main_menu()