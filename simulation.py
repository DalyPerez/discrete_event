from events import Simulator
from world import World
from matplotlib import pyplot as plt
from time import time

class Simulation:
    def __init__(self, w, m, iter):
        self.iter = iter
        self.initial_w = w
        self.initial_m = m


    def simulate(self, step):
        print ("<*> start simulate with Men: %d, Woman: %d, Year: %d (steps: %d)"%(self.initial_m, self.initial_w, self.iter, step))
        info = []
        for i in range(step):
            x = time()
            world = World(self.initial_w, self.initial_m)
            sim = Simulator(self.iter, world)
            census_x_year , census_final = sim.simulate()
            info.append(census_x_year)
            print ("    -> step", i, "(done)", " in %.1f seg"%(round(time() - x, 1)))
        self.info = info
        print ("<*> finish")
        return info

    def plot_couples_hist(self): #ok
        coup_x_sim = []
      
        for sim in self.info:
            coup_x_sim.append(sum([j.couples for j in sim]))
        # --------------------------------------------------------------
        plt.figure()        
        # plt.title("Cantidad de parejas generadas en %d simulaciones "%(len(self.info)))
        plt.hist(coup_x_sim)
        plt.savefig("couples_hist.png")
        plt.show()

    def plot_dead_hist(self):
        dead_x_sim = []
        for sim in self.info:
            dead_aux = [i.dead for i in sim]
            dead = []
            for i in range(len(dead_aux)):
                if i == 0:
                    dead.append(dead_aux[0])
                else:
                    dead.append(dead_aux[i] - dead_aux[i-1])

            dead_x_sim.append(sum(dead))


        # plt.title("Cantidad de parejas generadas en %d%d simulaciones " %(len(info)))
        plt.hist(dead_x_sim)
        plt.savefig("dead_hist.png")
        plt.show()

    def plot_results(self):

        babys_x_sim = []
        for sim in self.info:
            babys_aux = [i.new_babys for i in sim]
            babys = []
            for i in range(len(babys_aux)):
                if i == 0:
                    babys.append(babys_aux[0])
                else:
                    babys.append(babys_aux[i] - babys_aux[i-1])

            babys_x_sim.append(sum(babys))
        
        coup_x_sim = []
      
        for sim in self.info:
            coup_x_sim.append(sum([j.couples for j in sim]))


        dead_x_sim = []
        for sim in self.info:
            dead_aux = [i.dead for i in sim]
            dead = []
            for i in range(len(dead_aux)):
                if i == 0:
                    dead.append(dead_aux[0])
                else:
                    dead.append(dead_aux[i] - dead_aux[i-1])

            dead_x_sim.append(sum(dead))

        self.plot_hist(babys_x_sim, coup_x_sim, dead_x_sim, ("Bebes","Parejas","Muertes"))    

    def plot_hist(self, A, B, C, titles):
        ta, tb, tc = titles

        plt.figure()

        plt.subplot(131)
        plt.title(ta)
        plt.hist(A)

        plt.subplot(132)
        plt.title(tb)
        plt.hist(B)

        plt.subplot(133)
        plt.title(tc)
        plt.hist(C)

        plt.show()

    def get_simulate_couples(self):
        couples = [j.couples for j in self.info[0]]
        return couples
    
    def get_simulate_dead(self):
        solve = [j.dead for j in self.info[0]]
        result = [i for i in solve]
        for i in range(1, len(result)):
            result[i] = solve[i] - solve[i - 1]
        return result 

    def get_simulate_sex(self):
        alivemen = [i.alive_men for i in self.info[0]]
        alivewoman = [i.alive_woman for i in self.info[0]]
        X = [i for i in range(len(alivemen))]
        alive = [alivemen[i] + alivewoman[i] for i in X]
        result = alivemen, alivewoman, alive, X
        return result

def savefig(info, titles, labels, name = "result.png"):
    fig, axs = plt.subplots(2,2)
    markers = ["b:", "r:", "g:", "m:"]
    mapp = [(0, 0), (0, 1), (1,0), (1,1)]
    for i in range(len(info)):
        X = [j for j in range(len(info[i]))]
        x, y = mapp[i]
        axs[x, y].plot(X, info[i], markers[i], label = labels[i])
        axs[x, y].legend()
        axs[x, y].set_title(titles[i])
    # fig.savefig(name)
    plt.show()

def savefig2(info, titles, labels, name = "result.png"):
    fig, axs = plt.subplots(2,2)
    markers = ["b:", "r:", "g:", "m:"]
    mapp = [(0, 0), (0, 1), (1,0), (1,1)]
    for i in range(len(info)):
        am, aw, a, X = info[i]
        x, y = mapp[i]
        axs[x, y].plot(X, am, "b:", label = "hombres")
        axs[x, y].plot(X, aw, "r:", label = "mujeres")
        axs[x, y].plot(X, a, "g:", label = "total")
        axs[x, y].legend()
        axs[x, y].set_title(titles[i])
    plt.show()



def Visual_Simulate(Ss, configs, selector, labels):
    infos = [selector(s) for s in Ss]
    titles = ["Simulando con H:%d, M:%d, A:%d"%(conf[0], conf[1], conf[2]) for conf in configs]
    labels = [labels] * 4
    savefig(infos, titles, labels)

def Visual_Simulate2(Ss, configs, selector, labels):
    infos = [selector(s) for s in Ss]
    titles = ["Simulando con H:%d, M:%d, A:%d"%(conf[0], conf[1], conf[2]) for conf in configs]
    labels = [labels] * 4
    savefig2(infos, titles, labels)


    

config = [(50, 50, 100), (70, 70, 100), (100, 100, 100), (400, 400, 100)]
Ss = [Simulation(*conf) for conf in config]
for i in Ss:
    i.simulate(100)

selector_couples = lambda s : s.get_simulate_couples()
selector_dead = lambda s : s.get_simulate_dead()
selector_alives = lambda s : s.get_simulate_sex()


Visual_Simulate(Ss, config, selector_couples, "Parejas")
Visual_Simulate(Ss, config, selector_dead, "Muertes")
Visual_Simulate2(Ss, config, selector_alives, "Personas")


for s in Ss:
    s.plot_results()





        
