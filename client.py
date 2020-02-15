from tkinter import *
import tkinter.messagebox as mbox
import socket
import pickle


def button_add():
    #   Grabbing data from Entry boxes
    get_code = ent_code.get()
    get_description = ent_description.get()
    get_amount = ent_amount.get()

    #   Create list with Entry data and convert the data to bytes and send it to server
    item_data = [get_code, get_description, get_amount]
    serialized_data = pickle.dumps(item_data)
    client.sendall(serialized_data)
    mbox.showinfo('Item Added!', f'Item code: {item_data[0]} \nItem description: '
                                 f'{item_data[1]} \nAmount: {item_data[2]}')
    #   Clear Entry fields after data is sent
    ent_code.delete(0, 100)
    ent_description.delete(0, 100)
    ent_amount.delete(0, 100)


def button_exit():
    #   Terminate socket connection and exit
    client.close()
    quit()


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 60000))

#   Window configurations
window = Tk()
window.title('StockItAll System Application')
window.configure()
window.geometry('400x140')

#   Labels configuration
lbl_code = Label(window, text='Code:')
lbl_description = Label(window, text='Description:')
lbl_amount = Label(window, text='Amount:')
lbl_code.place(x=10, y=10)
lbl_description.place(x=10, y=35)
lbl_amount.place(x=10, y=60)

#   Entry box configurations
ent_code = Entry(window)
ent_description = Entry(window)
ent_amount = Entry(window)
ent_code.place(x=115, y=10)
ent_description.place(x=115, y=35)
ent_amount.place(x=115, y=60)

#   Button configuration
btn_add = Button(window, text='Add item', command=button_add)
btn_exit = Button(window, text='Exit', command=button_exit)
btn_add.place(x=145, y=90)
btn_exit.place(x=210, y=90)

window.mainloop()
