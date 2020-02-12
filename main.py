from StockTracker import *
from prettytable import PrettyTable
from sys import exit
import logging
import threading
import socket
import pickle


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, datefmt='%H:%M:%S')

def server_thread():
    HOST = '127.0.0.1'
    PORT = 60000

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    while True:
        conn, addr = server.accept()
        with conn:

            print()
            logging.info(f'Client connected: IP {addr[0]} Port {addr[1]}')
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                recv_item = pickle.loads(data)
                new_item = StockItem(code=recv_item[0], description=recv_item[1], amount=recv_item[2])
                StockTracker.addItem(new_item)
                continue
        logging.info(f'Client disconnected: IP {addr[0]} Port {addr[1]}')




def main_menu():

    condition = True
    while condition:
        print()
        print('''
    -------------------------------------------------------
    StockItAll System Interface
    -------------------------------------------------------
    (1)\t\tAdd a new item to stock
    (2)\t\tUpdate stock inventory of item
    (3)\t\tDisplay specific item
    (4)\t\tDisplay full item-inventory
    
    (5)\t\tExit''')

        try:
            select = int(input('''Select an option: '''))

        except ValueError:
            print()
            logging.info('Error:\t Use a number to select an option from the menu!')
            continue


        def menu_1():
            ''' Add a new item to stock '''

            while True:
                try:
                    code = int(input('Enter a Item code: '))
                    description = input('Enter Item description: ')
                    amount = int(input('Enter Item stock: '))
                    new_item = StockItem(code=code, description=description, amount=amount)
                    StockTracker.addItem(new_item)
                    print()
                    logging.info(f'Added!\t Code: {code} Description: {description} Amount: {amount}')
                    break
                except ValueError:
                    print()
                    logging.info('Error: Please use numbers for Item Code and Amount!')

        def menu_2():
            ''' Update stock inventory of item '''

            code = int(input('Enter Code: '))
            amount = int(input('Enter new Amount: '))
            update_item = StockTracker(code=code, amount=amount)
            StockTracker.updateItem(update_item)

        def menu_3():
            ''' Display item details from code '''

            code = input('Enter Item code: ')
            get_item = StockTracker(code=code)
            r_item = StockTracker.DisplayItem(get_item)

            PTable = PrettyTable()
            PTable.field_names = ['Code', 'Description', 'Amount']
            PTable.add_row([r_item['CODE'], r_item['DESCRIPTION'], r_item['AMOUNT']])
            print()
            print('''
        StockItAll Inventory:''')
            print(PTable)

        def menu_4():
            PTable = PrettyTable()
            PTable.field_names = ['Code', 'Description', 'Amount']
            inventory = StockTracker.DisplayInventory(None)
            for item in inventory:
                PTable.add_row([item['CODE'], item['DESCRIPTION'], item['AMOUNT']])
            print('''
        StockItAll Inventory:''')
            print(PTable)

        def menu_5():
            print()
            logging.info('Exiting program. Goodbye!')
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
        elif select >5 or select < 1:
            print()
            logging.info('Error:\t This is not an option!')


t1 = threading.Thread(target=server_thread)
t2 = threading.Thread(target=main_menu)

t1.start()
t2.start()

