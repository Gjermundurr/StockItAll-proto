from StockTracker import *
from prettytable import PrettyTable
from sys import exit
import logging
import threading
import socket
import pickle

#   logging module configuration of layout
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, datefmt='%H:%M:%S')

try:
    #   Check if database file exists. if not; file is created
    test_file = open('StockTracker.csv', mode='x')
    test_file.close()
    logging.info(f'ERROR: Database not found, File is created!')

except FileExistsError:
    logging.info(f'INFO: Database found: StockTracker.csv')


def server_socket():
    """ Server thread: listens for client-application connection """
    #   Looping the server listener to allow client to reconnect repeatedly
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 60000))
    server.listen()
    while True:
        conn, addr = server.accept()
        try:
            with conn:  # Executes when a connection is accepted
                logging.info(f'INFO: Client connected: IP {addr[0]} Port {addr[1]}')

                while True:
                    # Deserializes received data and adds new object to database
                    data = conn.recv(1024)
                    if not data:
                        break
                    recv_item = pickle.loads(data)
                    new_item = StockTracker(code=recv_item[0], description=recv_item[1], amount=recv_item[2])
                    StockTracker.AddItem(new_item)
                    logging.info(f"INFO: Item added by Client! Code: {new_item.data['CODE']}, Description: "
                                 f"{new_item.data['DESCRIPTION']}, Amount: {new_item.data['AMOUNT']}")
                    continue

            logging.info(f'INFO: Client disconnected: IP {addr[0]} Port {addr[1]}')
        except ConnectionResetError:
            #   If connection terminates with receiving TCP-FIN bit the server restarts the listener
            server.close()
            logging.info(f'INFO: Client disconnected: IP {addr[0]} Port {addr[1]}')


def main_menu():
    """ CLI-menu loop function """

    while True:
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
            # Input sanitation if user enters characters instead of numbers
            logging.info('ERROR: Use a number to select an option from the menu!')
            continue

        if select == 1:
            #   Add a new item to inventory
            while True:
                try:
                    code = int(input('Enter a Item code: '))
                    description = input('Enter Item description: ')
                    amount = int(input('Enter Item stock: '))
                    new_item = StockTracker(code=code, description=description, amount=amount)
                    return_value = StockTracker.AddItem(new_item)
                    print('Item - ', new_item)
                    logging.info(return_value)
                    break
                except ValueError:
                    print()
                    logging.info('ERROR: Use digits only for Code and Amount!')

        elif select == 2:
            #   Update StockItems amount by code
            while True:
                try:
                    code = int(input('Enter Code: '))
                    amount = int(input('Enter new Amount: '))
                    update_item = StockTracker(code=code, amount=amount)
                    return_value = StockTracker.UpdateItem(update_item)
                    logging.info(return_value)
                    break
                except ValueError:
                    print()
                    logging.info('ERROR: Use numbers only!')

        elif select == 3:
            #   Display specific item details from given code
            try:
                code = int(input('Enter Item code: '))
                get_item = StockTracker(code=code)
                return_item = StockTracker.ReturnItem(get_item)
                #   Printing a table containing the item
                PTable = PrettyTable()
                PTable.field_names = ['Code', 'Description', 'Amount']
                PTable.add_row([return_item['CODE'], return_item['DESCRIPTION'], return_item['AMOUNT']])
                print('''
        StockItAll Inventory:''')
                print(PTable)
            except (ValueError, TypeError):
                print()
                logging.info('ERROR: This item does not exist!')

        elif select == 4:
            #   Displays entire inventory of csv file
            inventory = StockTracker.ReturnInventory(None)
            PTable = PrettyTable()
            PTable.field_names = ['Code', 'Description', 'Amount']
            for item in inventory:
                PTable.add_row([item['CODE'], item['DESCRIPTION'], item['AMOUNT']])
            print('''
        StockItAll Inventory:''')
            print(PTable)

        elif select == 5:
            #   Exit option
            logging.info('MESSAGE: Server shutting down... Good-bye!')
            exit()

        elif select > 5 or select < 1:
            #   limits menu input options between 1-5
            print()
            logging.info('ERROR: This is not an option!')


#   Threading functions main_menu and server_socket
t1 = threading.Thread(target=server_socket, daemon=True)
t2 = threading.Thread(target=main_menu)
t1.start()
t2.start()
