from generation import *

class Person:
    def __init__(self, id, sex, age):
        self.id = id
        self.sex = sex
        self.age = age
        self.partner = None
        self.pregnacy = 0 #num of babys in actual pregnancy
        self.time_alone = 0
        self.max_child = max_child_wished()
        self.childs = []  #num of actual childrens

    def birthday(self):
        self.age += 1

    def married(self, p):
        self.partner = p
        
    def break_relation(self, time):
        self.time_alone = time
        self.partner = None


            


        


