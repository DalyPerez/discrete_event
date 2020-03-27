from events import Simulator
from world import World
from matplotlib import pyplot as plt

class Simulation:
    def __init__(self, w, m, iter):
        self.iter = iter
        self.initial_w = w
        self.initial_m = m


    def simulate(self, step):
        info = []
        for i in range(step):
            world = World(self.initial_w, self.initial_m)
            sim = Simulator(self.iter, world)
            census_x_year , census_final = sim.simulate()
            info.append(census_x_year)
            print ("step", i, "(done)")
        return info

    def plot_couples_x_year(self, info):
        coup_x_sim = []
        for sim in info:
            coup_x_sim.append(sum([j.couples for j in sim]))
            couples = [i.couples for i in sim]
            X = [i for i in range(len(couples))]
            plt.plot(X, couples, "b:", label = "cantidad de parejas")
            plt.show()

            

        # plt.title("Cantidad de parejas generadas en %d%d simulaciones " %(len(info)))
        plt.hist(coup_x_sim)
        plt.show()

        

        # couples = [i.couples for i in info[0]]
        # X = [i for i in range(len(couples))]

        # mean = 1. * sum(coup_x_sim)/len(coup_x_sim)
        # print ("Aprox Expected Value of Couples:", mean)
        # plt.subplot(121)
        # plt.hist(coup_x_sim)
        # plt.subplot(122)
        # plt.title("Cantidad de parejas por anno")
        # plt.plot(X, couples, "b:", label = "cantidad de parejas")
        # plt.legend()
        # plt.show()


    def plot_results(self, info):
        babys = []
        for i in info:
            babys.append(sum([j.new_babys for j in i]))
        
        alivemen = [i.alive_men for i in info[0]]
        alivewoman = [i.alive_woman for i in info[0]]
        X = [i for i in range(len(alivemen))]
        alive = [alivemen[i] + alivewoman[i] for i in X]
        
        
        mean = 1. * sum(babys)/len(babys)
        print ("Aprox Expected Vaue of Babys:", mean)
        plt.subplot(121)
        plt.hist(babys)
        plt.subplot(122)
        plt.title("alive person per year")
        plt.plot(X, alivemen, "b:", label = "men alive")
        plt.plot(X, alivewoman, "r:", label = "woman alive")
        plt.plot(X, alive, "g-", label = "alive")
        plt.legend()
        plt.show()






        
    


s = Simulation(50, 50, 100)
info = s.simulate(10)
# s.plot_results(info)
s.plot_couples_x_year(info)




        
