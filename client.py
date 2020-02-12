''' Client GUI application '''
from tkinter import *
import tkinter.messagebox as mbox
import socket
import pickle

# Exit function so a TCP-close flag is sent to server
def exit_app():
    s.close()
    quit()


def button_add():
    # Grabbing data from Entry boxes
    get_code = ent_code.get()
    get_description = ent_description.get()
    get_amount = ent_amount.get()

    # Create list and serialize the object to send it through socket
    item_data = [get_code, get_description, get_amount]
    serialized_data = pickle.dumps(item_data)
    # Send the serialized data through socket
    s.sendall(serialized_data)

    mbox.showinfo('Item Added!', f'Item code: {item_data[0]} \nItem description: {item_data[2]} \nAmount: {item_data[2]}')


# Establish connection to server when client program starts
RHOST = '127.0.0.1'
RPORT = 60000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((RHOST, RPORT))

# main window configurations
window = Tk()
window.title('StockItAll System Application')
window.configure()
window.geometry('400x140')

# Labels configuration
lbl_code = Label(window, text='Code:')
lbl_description = Label(window, text='Description:')
lbl_amount = Label(window, text='Amount:')

# Label placement
lbl_code.place(x=10, y=10)
lbl_description.place(x=10, y=35)
lbl_amount.place(x=10, y=60)

# Entry box configurations
ent_code = Entry(window)
ent_description = Entry(window)
ent_amount = Entry(window)

# Entry box placement
ent_code.place(x=115, y=10)
ent_description.place(x=115, y=35)
ent_amount.place(x=115, y=60)

# Button configuration
btn_add = Button(window, text='Add item', command=button_add)
btn_exit = Button(window, text='Exit', command=exit_app)

#Button placement
btn_add.place(x=145, y=90)
btn_exit.place(x=210, y=90)



window.mainloop()