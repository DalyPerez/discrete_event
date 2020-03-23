from generation import *
from person import *
# from events import *

class World:
    def __init__(self, w, m):
        self.count = 0
        self.date = (0, 0)
        self.year = 0
        self.persons = {}
        self.alive = []
        self.died_person = []
        self.couples = []
        self.create_population(w, m)
        

    def create_population(self, W, M):
        self.count = W + M
        sex = 0
        for i in range(1, self.count + 1):
            if i > M:
                sex = 1
            age = U(0, 100)
            p = Person(i, sex, age)
            self.persons[i] = p
            self.alive.append(i)
    
    def born_baby(self, info):
        mom, dad = info
        self.count += 1
        print("Born baby:", self.count)
        p = Person(self.count,sex_child(), 0)
        self.persons[mom].pregnacy -= 1
        self.persons[mom].childs.append(p.id)
        self.persons[dad].childs.append(p.id)
        self.persons[self.count] = p
        self.alive.append(self.count)

    def dead(self ):
        self.died_person = []
        for i in self.alive:
            p = self.persons[i]
            if die(p.age, p.sex):  #ver si tenia pareja
                print("Dead person:", i)
                self.died_person.append(i)
                self.update_dead(i)
                self.persons.__delitem__(i)
            else:
                p.age += 1
        self.update_alive()
        print("Year: ", self.year, "dead", len(self.died_person), "persons")
    
    def update_dead(self, id):
        p = self.persons[id]
        if p.partner != None:
            if p.sex == 1: # was women
                couple = ( id, p.partner)
            else:
                couple = (p.partner, id)
            self.couples = [c for c in self.couples if c != couple]
            self.persons[p.partner].partner = None #TODO enviuda=> time alone        
        
    def update_alive(self):
        self.alive = []
        for i in self.persons.keys():
            self.alive.append(i)

    def alone_persons(self):
        p = []
        for i in self.persons.keys():
            if self.persons[i].partner == None:
                p.append(i)
        return p

    def matching(self):
        w_wish_partner = []
        m_wish_partner = []
        for i in self.alone_persons():
            p = self.persons[i]
            if p.age > 12 and want_partner(p.age):
                if p.sex == 1:
                    w_wish_partner.append(i)
                else:
                    m_wish_partner.append(i)

        m_mask = [0 for i in range(len(m_wish_partner))]

        for i in w_wish_partner:
            for j in range(len(m_wish_partner)):
                if not m_mask[j] and get_partner(self.persons[i].age, self.persons[m_wish_partner[j]].age):
                    self.couples.append((i, m_wish_partner[j]))
                    self.persons[i].partner = m_wish_partner[j]
                    self.persons[m_wish_partner[j]].partner = i
                    m_mask[j] = 1
                    break
                    
    def break_couple(self):
        l = []
        for i in self.couples:
            if breaking():
                self.persons[i[0]].partner = None
                self.persons[i[1]].partner = None
            else:
                l.append(i)
        self.couples = l

    def pregnancy(self):
        info = []
        for c in self.couples:
            w = self.persons[c[0]]
            m = self.persons[c[1]]
            if(w.pregnacy == 0 and len(w.childs) < w.max_child and len(m.childs) < m.max_child ):
                if pregnant(w.age):
                    num_child = pregnancy_child()
                    w.pregnacy = num_child
                    info.append((c[0], c[1], num_child))
        return info
                   

def main():
    w = World(10, 10)

    w.matching()
    print(w.couples)
    w.dead()
    w.matching()
    print(w.couples)
    w.dead()
    # print(w.pregnancy())
    
if (__name__ == "__main__"):
    main()
       
