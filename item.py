#!/usr/bin/env python3

#-----BOOK CLASSES-----
class Book:

    title = ""
    price = 0.00
    stock = 0

    def __init__(self,title, price, stock):
        self.title = title
        self.price = price
        self.stock = stock

    def setPrice(self, price):
        self.price = price

    def setStock(self, stock):
        self.stock = stock

    def getPrice(self):
        return self.price

    def getStock(self):
        return self.stock

    def jsonify(self):
        item = {
            "title": self.title,
            "price": self.price,
            "stock": self.stock
        }
        return item

class Storybook(Book):

    genre = ""

    def __init__(self,title, price, stock, genre):
        super().__init__(title, price, stock)
        self.genre = genre

    def jsonify(self):
        item = super().jsonify()
        item["genre"] = self.genre
        return item
