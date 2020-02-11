from StockTracker import *
from prettytable import PrettyTable
from sys import exit

def main_menu():
    select = 0
    while select != 5:
        print('''
    -------------------------------------------------------
    StockItAll System Interface
    -------------------------------------------------------
    (1)\t\tAdd a new item to stock
    (2)\t\tUpdate stock inventory of item
    (3)\t\tDisplay specific item
    (4)\t\tDisplay full item-inventory
    
    (5)\t\tExit''')
        select = int(input('''
    Select an option: '''))


        def menu_1():
            ''' Add a new item to stock '''

            print()
            code = int(input('\tEnter a stock code: '))
            description = input('\tEnter item description: ')
            amount = int(input('\tEnter item stock: '))
            new_item = StockItem(code=code, description=description, amount=amount)
            StockTracker.addItem(new_item)

        def menu_2():
            ''' Update stock inventory of item '''

            code = int(input('\tEnter code: '))
            amount = int(input('\tEnter new amount: '))
            update_item = StockTracker(code=code, amount=amount)
            StockTracker.updateItem(update_item)

        def menu_3():
            ''' Display item details from code '''
            code = input('\tEnter the Code of the item you wish to display: ')
            get_item = StockTracker(code=code)
            r_item = StockTracker.DisplayItem(get_item)

            PTable = PrettyTable()
            PTable.field_names = ['Code', 'Description', 'Amount']
            PTable.add_row([r_item['CODE'], r_item['DESCRIPTION'], r_item['AMOUNT']])
            print()
            print(PTable)

        def menu_4():
            PTable = PrettyTable()
            PTable.field_names = ['Code', 'Description', 'Amount']
            inventory = StockTracker.DisplayInventory(None)
            for item in inventory:
                PTable.add_row([item['CODE'], item['DESCRIPTION'], item['AMOUNT']])
            print(PTable)

        def menu_5():
            exit()


        if select == 1:
            menu_1()
        elif select == 2:
            menu_2()
        elif select == 3:
            menu_3()
        elif select == 4:
            menu_4()
        elif select == 5:
            menu_5()




if __name__ == '__main__':

    main_menu()