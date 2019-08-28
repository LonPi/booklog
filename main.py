#!/usr/bin/env python3

import json
from item import *
from collect import *
from tkinter import *
from tkinter import ttk

booklist = Collection()

#-----GUI APPLICATION-----
class App(Frame):

    def __init__(self, master):
        super(App, self).__init__()
        self.master = master
        self.pack()

        self.master.protocol('W_DELETE_WINDOW', self.click_quit)
        # self.master.bind('<Return>', self.input_return)
        self.master.bind('<Escape>', self.click_quit)

        #dummy data
        # booklist.add(Book('Potatoes to Spagetti', 19.50, 5))
        # booklist.add(Book('Homemade Cookbook', 17.00, 6))
        # booklist.add(Storybook('The Three Carrots', 25.00, 0, 'horror'))

        #-----LAYOUTS-----
        #-----Item Log Display Layout
        list_frame = Frame(self)
        list_frame.pack(padx=10, pady=20, anchor='w')

        Label(list_frame, text="Books on system").grid(row=0, column=0, sticky='w')

        self.tree = ttk.Treeview (list_frame, height = 10, columns=('#1','#2'))
        self.tree.heading('#0', text='Name', anchor = 'w')
        self.tree.heading('#1', text='Price', anchor = 'w')
        self.tree.heading('#2', text='Stock', anchor = 'w')
        self.tree.grid()

        self.update_tree()  #UPDATES ITEM LOG DISPLAY

        self.var_filter = BooleanVar()
        filter_storybook = Checkbutton(list_frame, text='Filter: Storybooks only', variable=self.var_filter, command=lambda: self.input_checkbox('filter_storybook'))
        filter_storybook.grid(row=4)

        #-----Addition of Books Layout
        dialog_frame = Frame(self)
        dialog_frame.pack(padx=10, pady=15, anchor='w')
        Label(dialog_frame, text="Add book").grid(row=0, column=1)
        Label(dialog_frame, text="Title: ").grid(row=1, column=0)
        Label(dialog_frame, text="Price: ").grid(row=2, column=0)
        Label(dialog_frame, text="Stock: ").grid(row=3, column=0)
        Label(dialog_frame, text="Genre: ").grid(row=5, column=0)

        #-----Input Fields
        self.title_input = Entry(dialog_frame, background='white', width=35)
        self.title_input.grid(row=1, column=1)
        self.title_input.focus_set()
        self.price_input = Entry(dialog_frame, background='white', width=35)
        self.price_input.grid(row=2, column=1)
        self.stock_input = Entry(dialog_frame, background='white', width=35)
        self.stock_input.grid(row=3, column=1)
        self.genre_input = Entry(dialog_frame, background='white', width=35, state='disabled')
        self.genre_input.grid(row=5, column=1)

        #-----Input Error Display
        self.title_err = Label(dialog_frame, text="")
        self.price_err = Label(dialog_frame, text="")
        self.stock_err = Label(dialog_frame, text="")
        self.genre_err =  Label(dialog_frame, text="")
        self.title_err.grid(row=1, column=3)
        self.price_err.grid(row=2, column=3)
        self.stock_err.grid(row=3, column=3)
        self.genre_err.grid(row=5, column=3)

        add_storybook = Checkbutton(dialog_frame, text='Storybook', command=lambda: self.input_checkbox('add_storybook'))
        add_storybook.grid(row=4)

        Button(self, text='Add', command=lambda: self.input_return('add')).pack(side='left')
        Button(self, text='Quit', command=self.click_quit).pack(side='right')


#-----FUNCTIONS-----
    def input_return(self, event=None):
        """ text field input processing """
        if event == 'add':
            valid = True
            toAdd = ""
            title = self.title_input.get()
            price = self.price_input.get()
            stock = self.stock_input.get()

            # ERROR CHECKING UPON ADD BOOKS TEXT FIELDS
            if title == "":
                self.title_err['text'] = 'Title is missing'
                valid = False
            else:
                self.title_err['text'] = ""

            if price == "":
                self.price_err['text'] = 'Price is missing'
                valid = False
            elif price.isalpha():
                self.price_err['text'] = 'Price is invalid'
                valid = False
            else:
                self.price_err['text'] = ""

            if stock == "":
                self.stock_err['text'] = 'Stock is missing'
                valid = False
            elif not stock.isdigit():
                self.stock_err['text'] = 'Stock is invalid'
                valid = False
            else:
                self.stock_err['text'] = ""


            if self.genre_input.cget('state')=='normal':
                genre = self.genre_input.get()

                if genre == "":
                    self.genre_err['text'] = 'Genre is missing'
                    valid = False
                else:
                    self.genre_err['text'] = ""

            if valid:
                if self.genre_input.cget('state')=='disabled':
                    toAdd = Book(title,price,stock)
                    booklist.add(toAdd)
                else:
                    toAdd = Storybook(title,price,stock,genre)
                    booklist.add(toAdd)
                self.update_tree()


    def input_checkbox(self, event=None):
        """ checkbox features """
        if event == 'add_storybook':            # enable addition of storybooks
            self.genre_input.config(state=DISABLED if self.genre_input.cget('state')==NORMAL else NORMAL)
        elif event == 'filter_storybook':       # filters storybooks on treeview
            if self.var_filter.get():
                self.update_tree('storybook')
            else:
                self.update_tree()

    def update_tree(self, event=None):
        """ updates display of books on system """
        for i in self.tree.get_children():
            self.tree.delete(i)

        if event == 'storybook':
            for book in booklist.getAll():
                if type(book) == Storybook:
                    self.tree.insert('', 'end', text=book.title, values=("${:.2f}".format(float(book.price)), book.stock))
        else:
            for book in booklist.getAll():
                self.tree.insert('', 'end', text=book.title, values=("${:.2f}".format(float(book.price)), book.stock))

    def click_quit(self, event=None):
        """ exits program """
        self.json_save()
        root.destroy()
        print('Exitted program. Bye')

    def json_save(self):
        """ save data to json format """
        data = []
        for book in booklist.getAll():
            item = book.jsonify()
            data.append(item)

        jsonData = json.dumps(data, indent=2)
        # print(jsonData)

        with open('books.json', 'w') as f:
            json.dump(data, f)


        print('For JSON validator, jsonlint:')
        data = []
        for book in booklist.getAll():
            if type(book) is Book:
                item = book.jsonify()
                data.append(item)
        jsonData = json.dumps(data, indent=2)
        print(jsonData)
#-----START MAIN-----
if __name__ == '__main__':

    """ load inventory save file """
    data = []
    with open('books.json', 'r') as f:
        try:
            data = json.load(f)
        except Exception as e:
            print('No file loaded')

    for item in data:
        try:
            booklist.add(Storybook(item['title'],item['price'],item['stock'],item['genre']))
        except Exception as e:
            booklist.add(Book(item['title'],item['price'],item['stock']))

    root = Tk()
    root.title("Book Log")
    root.tk_setPalette(background='#ececec')
    app = App(root)
    root.mainloop()
