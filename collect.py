#!/usr/bin/env python3

#-----COLLECTION CLASS-----
class Collection:

    __storage = []

    def add(self, obj):
        self.__storage.append(obj)

    def getAll(self):
        return self.__storage
