from world import *

class Event:
    def __init__(self, year, function, month = 0, args = None):
        """
        year: year the event occurs
        month: priority between months 
        function: action that occurs in the event
        args: arguments of function

        """
        self.year = year
        self.month = month
        self.function = function
        self.args = args
       
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
        self.events = [Event(-1, self.update_initial_population_event), Event(self.world.year, self.start_year_event), Event(iter, self.stop)]

    def stop(self):
        # print("Stop the simulation")
        self.running = False    

    def simulate(self):
        while(self.running):
            self.move()

        # print("total:", self.world.census.total(), "womans:",self.world.census.womans, "mens:", self.world.census.mens )
        # print("total alive:", self.world.census.total_alive(), "womans alive:", self.world.census.alive_woman, "mens alive:", self.world.census.alive_men)
        # print("new babys:", self.world.census.new_babys)
        return self.world.census_x_year, self.world.census
       
    def move(self):
        event = self.events[0]
        self.events = self.events[1:]
        event.do()

    def add_event(self, e):
        self.events.append(e)
        self.events = sorted(self.events, key = lambda x:(x.year, x.month))
        
    def update_initial_population_event(self):
        """
        Establish the dead year for the initial population 
        """
        for id in self.world.persons.keys():
            year = dead_year(self.world.persons[id].age, self.world.persons[id].sex)
            self.add_event(Event(year - self.world.persons[id].age , self.dead_person_event, 0, (id,)))

    def start_year_event(self):
        if len(self.world.persons) > 0:
            self.add_event(Event(self.world.year, self.matching_event, 1))
            self.add_event(Event(self.world.year, self.break_event, 2))
            self.add_event(Event(self.world.year, self.pregnancy_event, 3))
            # self.add_event(Event(self.world.year, self.new_year, 12))
            self.add_event(Event(self.world.year + 1, self.start_year_event, 0))
            self.world.year += 1
            self.world.update_ages()
        else:
            self.add_event(Event(0, self.stop))
        
    def matching_event(self):
        self.world.matching()
    
    def end_timealone_event(self, id):
        if self.world.persons.get(id, None) != None:
            self.world.persons[id].available = True

    def break_event(self):
        s = self.world.break_couple()
        for i in s:
            id, t = i
            self.add_event(Event(self.world.year + t, self.end_timealone_event, -1, (id,)))

    def pregnancy_event(self):
        couples = self.world.pregnancy()
        for c in couples:
            mother = c[0]
            father = c[1]
            num_childs = c[2]
            for i in range(num_childs):
                self.add_event(Event(self.world.year + 1, self.born_baby_event, -1, ((mother, father), )))

    def born_baby_event(self, info):
        result = self.world.create_baby(info)
        if result != None:
            id, sex = result
            dead = dead_year(0, sex)
            self.add_event(Event(self.world.year + dead, self.dead_person_event, 0, ((id,))))
    
    def dead_person_event(self, person_id):
        widower = self.world.update_dead(person_id)
        if widower != None:
            id, t = widower
            self.add_event(Event(self.world.year + t, self.end_timealone_event, -1, (id,)))

        

def main():
    w = World(100, 100)
    s = Simulator(100,  w)

    s.simulate()

    
if (__name__ == "__main__"):
    main()