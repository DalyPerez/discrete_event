from generation import *

class Person:
    def __init__(self, id, sex, age):
        self.id = id
        self.sex = sex
        self.age = age
        self.partner = None
        self.childs = 0
        self.pregnancy = 0               # num of babys in actual pregnancy
        self.max_child = max_child_wished()
        self.available = True            # if the person is available or not
   

class Census:
    """
    Summarizes the population info once the simulation is finished
    """
    def __init__(self, w, m):
        self.womans = w
        self.mens = m
        self.alive_woman = w
        self.alive_men = m
        self.new_babys = 0
        self.dead = 0

    

    def born_baby(self, sex):
        self.new_babys += 1
        if sex == 1:
            self.womans += 1
            self.alive_woman += 1
        else:
            self.mens += 1
            self.alive_men += 1

    def dead_p(self ):
        self.dead += 1

    def total(self):
        return self.womans + self.mens

    def total_alive(self):
        return self.alive_woman + self.alive_men

    def dead_person(self, sex):
        if sex == 1:
            self.alive_woman -= 1
        else:
            self.alive_men -= 1
    
class CensusAnnual:
    """
    Contain the population info in one year
    """
    def __init__(self, w, m, aw, am, nb, d, c):
        self.womans = w
        self.mens = m
        self.alive_woman = aw
        self.alive_men = am
        self.new_babys = nb
        self.dead = d
        self.couples = c
        


        


