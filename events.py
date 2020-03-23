from world import *

class Event:
    def __init__(self, year, function, month = 0, args = None):
        self.year = year
        self.function = function
        self.args = args
        self.month = month

    def do(self):
        if self.args != None:
            self.function(*self.args)
        else:
            self.function()

class Simulator:
    def __init__(self, iter, world):
        self.iter = iter
        self.world = world
        self.running = True
        self.events = [Event(self.world.year, self.start_year_event), Event(iter, self.stop)]

    def stop(self):
        print("Stop the simulation")
        self.running = False

    def simulate(self):
        while(self.running):
            self.move()
        print("alive:", len(self.world.persons), "total:", self.world.count)
        # recolectar resultados from world

    def move(self):
        event = self.events[0]
        self.events = self.events[1:]
        event.do()

    def add_event(self, e):
        self.events.append(e)
        self.events = sorted(self.events, key = lambda x:(x.year, x.month))

    def start_year_event(self):
        self.add_event(Event(self.world.year, self.dead_event, 0))
        if len(self.world.persons) > 0:
            self.add_event(Event(self.world.year, self.matching_event, 1))
            self.add_event(Event(self.world.year, self.pregnancy_event, 2))
            self.add_event(Event(self.world.year, self.new_year, 12))
            self.add_event(Event(self.world.year + 1, self.start_year_event, 0))
        else:
            self.add_event(Event(0, self.stop))
        
    def dead_event(self):
        self.world.dead()

    def new_year(self):
        self.world.year += 1
        print("Happy New Year:,", self.world.year)
        
    def matching_event(self):
        self.world.matching()
        print("couples:", self.world.couples)

    def pregnancy_event(self):
        couples = self.world.pregnancy()
        for c in couples:
            mother = c[0]
            father = c[1]
            num_childs = c[2]
            for i in range(num_childs):
                self.add_event(Event(self.world.year + 1, self.born_baby_event, -1, ((mother, father),)))

    def born_baby_event(self, info):
        if self.world.persons[info[0]] != None: #if the mom is alive, born the baby
            self.world.born_baby(info)
        




        

        
w = World(5000, 5000)
s = Simulator(100,  w)

s.simulate()
