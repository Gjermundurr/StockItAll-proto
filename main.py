from StockTracker import *
from prettytable import PrettyTable
from sys import exit
import logging
import threading
import socket
import pickle

#   logging module configuration of layout
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, datefmt='%H:%M:%S')


def server_thread():
    """ Server thread: listens for incoming connections from the Client-application """

    #   Servers IP and PORT
    HOST = '127.0.0.1'
    PORT = 60000

    #   Looping the server listener in case server does not recieve a TCP-FIN bit
    while True:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen()
        while True:
            conn, addr = server.accept()

            try:
                with conn:  # Executes when a connection is accepted
                    print()
                    logging.info(f'Client connected: IP {addr[0]} Port {addr[1]}')

                    while True:
                        #   A loop that deserializes the data then creates a new StockItem object and adds it to the database
                        data = conn.recv(1024)
                        if not data:
                            break
                        recv_item = pickle.loads(data)
                        new_item = StockItem(code=recv_item[0], description=recv_item[1], amount=recv_item[2])
                        StockTracker.addItem(new_item)
                        continue

                logging.info(f'Client disconnected: IP {addr[0]} Port {addr[1]}')
            except ConnectionResetError:
                #   If connection unexpectedly terminates the server listener will reset
                server.close()
                logging.info(f'Client disconnected: IP {addr[0]} Port {addr[1]}')

def main_menu():
    """ CLI-menu loop that is executed as a separate thread """

    while True:
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
            select = int(input('''
    Select an option: '''))

        except ValueError:
            print()
            logging.info('Error:\t Use a number to select an option from the menu!')
            continue

        if select == 1:
            """ Add a new item to stock """
            while True:
                try:
                    code = int(input('Enter a Item code: '))
                    description = input('Enter Item description: ')
                    amount = int(input('Enter Item stock: '))
                    new_item = StockItem(code=code, description=description, amount=amount)
                    print()
                    logging.info(f'INFO:\t' + StockTracker.addItem(new_item))
                    break
                except ValueError:
                    print()
                    logging.info('Error:\t Use digits only for Code and Amount!')

        elif select == 2:
            """ Update stock inventory of item """
            while True:
                try:
                    code = int(input('Enter Code: '))
                    amount = int(input('Enter new Amount: '))
                    update_item = StockTracker(code=code, amount=amount)
                    item_return = StockTracker.updateItem(update_item)
                    logging.info('INFO:'+f'{item_return}')
                    break
                except ValueError:
                    print()
                    logging.info('Error:\t Enter digits only!')

        elif select == 3:
            """ Display item details from code """
            try:
                code = int(input('Enter Item code: '))
                get_item = StockTracker(code=code)
                r_item = StockTracker.displayItem(get_item)
                #   Printing a table containing the item
                PTable = PrettyTable()
                PTable.field_names = ['Code', 'Description', 'Amount']
                PTable.add_row([r_item['CODE'], r_item['DESCRIPTION'], r_item['AMOUNT']])
                print()
                print('''
            StockItAll Inventory:''')
                print(PTable)

            except (ValueError, TypeError):
                print()
                logging.info('Error:\t This item does not exist!')

        elif select == 4:
            inventory = StockTracker.displayInventory(None)
            PTable = PrettyTable()
            PTable.field_names = ['Code', 'Description', 'Amount']
            for item in inventory:
                PTable.add_row([item['CODE'], item['DESCRIPTION'], item['AMOUNT']])
            print('''
        StockItAll Inventory:''')
            print(PTable)

        elif select == 5:
            print()
            logging.info('INFO:\t Shutting down server ...')
            logging.info('INFO:\t Exiting StockItAll System CLI-menu. Good-bye!')
            exit()

        elif select > 5 or select < 1:  # Input sanitation that limits user input to the specified option
            print()
            logging.info('Error:\t This is not an option!')


#   Thread 1 is set to daemon so it is killed when the main_menu calls for Exit
t1 = threading.Thread(target=server_thread, daemon=True)
t2 = threading.Thread(target=main_menu)
t1.start()
t2.start()
