from generation import *
from person import Person, Census, CensusAnnual



class World:
    def __init__(self, w, m):
        self.count = w + m
        self.census = Census(w, m)
        self.year = 0
        self.persons = {}
        self.alive = []
        self.couples = []
        self.create_population(w, m)
        self.census_x_year = []
      
    def create_population(self, W, M):
        self.count = W + M
        sex = 0
        for i in range(1, self.count + 1):
            if i > M:
                sex = 1
            age = rd.randint(0, 100)
            p = Person(i, sex, age)
            self.persons[i] = p
            self.alive.append(i)
    
    def create_baby(self, info_parents = None):
        self.count += 1
        if info_parents == None:
            return None
        
        mom, dad = info_parents
        if self.persons.get(mom, None) != None : 
            self.persons[mom].pregnancy -= 1
            self.persons[mom].childs += 1
            if self.persons.get(dad, None) != None :
                self.persons[dad].childs += 1
            sex = sex_child()
            self.census.born_baby(sex)
            p = Person(self.count, sex, 0)
            self.persons[self.count] = p
            self.alive.append(self.count)
            return self.count, sex
        return None
        
    
    def update_alive(self):
        self.alive = []
        for i in self.persons.keys():
            self.alive.append(i)
    
    def update_dead(self, id):
        p = self.persons[id]
        self.census.dead_p()
            
        self.census.dead_person(p.sex)
        self.persons.__delitem__(id)

        if p.partner != None:
            if p.sex == 1: # was women
                couple = ( id, p.partner)
            else:
                couple = (p.partner, id)
            self.couples = [c for c in self.couples if c != couple] #delete the couple

            widower = self.persons[p.partner]
            widower.partner = None 
            widower.available = False
            return (widower.id, self.define_time_alone(widower.id))    #time along for p.partner

        return None  

    def update_ages(self):
        for id in self.persons.keys():
            self.persons[id].age += 1
        self.census_x_year.append(self.extract_info_census())

    def extract_info_census(self):
        return CensusAnnual(self.census.womans, self.census.mens, self.census.alive_woman, self.census.alive_men, self.census.new_babys, self.census.dead, len(self.couples))

    def alone_persons(self):
        p = []
        for i in self.persons.keys():
            if self.persons[i].available and self.persons[i].partner == None:
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
        break_c = []
        for i in self.couples:
            if breaking():
                self.persons[i[0]].partner = None
                self.persons[i[1]].partner = None
                break_c.append((i[0], self.define_time_alone(i[0])))
                break_c.append((i[1], self.define_time_alone(i[1])))
                self.persons[i[0]].available = False
                self.persons[i[1]].available = False
            else:
                l.append(i)
        self.couples = l
        return break_c

    def pregnancy(self):
        info = []
        for c in self.couples:
            w = self.persons[c[0]]
            m = self.persons[c[1]]
            if(w.pregnancy == 0 and w.childs < w.max_child and m.childs < m.max_child ):
                if pregnant(w.age):
                    num_child = pregnancy_child() #TODO arreglar pregnancy
                    w.pregnancy = num_child
                    info.append((c[0], c[1], num_child))
        return info
                   
    def define_time_alone(self, id):
        p = self.persons[id]
        t = time_alone(p.age)
        return t
       
