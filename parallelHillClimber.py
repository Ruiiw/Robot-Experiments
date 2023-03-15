from solution import SOLUTION
import constants as c
import copy
import os

class PARALLEL_HILL_CLIMBER:

    def __init__(self):
        self.nextAvailableID = 0
        self.parents = {}
        self.best_fitnesses = []
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
        
        # os.system("rm brain*.nndf")
        # os.system("rm fitness*.txt")
        #os.system("rm body*.urdf")

    def Evolve(self):
        self.Evaluate(self.parents)
        for currentGeneration in range(c.numberOfGenerations):
            print("generation", currentGeneration)
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        #self.Print()
        self.Select()

    def Spawn(self):
        self.children = {}
        for i in self.parents:
            self.children[i] = copy.deepcopy(self.parents[i])
            self.children[i].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1
        #print("child", self.children)

    def Mutate(self):
        for child in self.children:
            self.children[child].Mutate()

    def Select(self):
        best_fitness = -1000
        for i in self.parents:
            if self.parents[i].fitness < self.children[i].fitness:
                self.parents[i] = self.children[i]
            best_fitness = max(self.parents[i].fitness, best_fitness)
        self.best_fitnesses.append(best_fitness)
        


    def Print(self):
        print("\n")
        for i in self.parents:
            print("parent fitness: ", self.parents[i].fitness, "child fitness:", self.children[i].fitness)
        print("\n")
       

    def Show_Best(self):
        best = self.parents[0]
        for parent in self.parents.values():
            if best.fitness > parent.fitness:
                best = parent

        best.Start_Simulation(' GUI')
        return best

    def Evaluate(self, solutions):
        for idx in solutions:
            solutions[idx].Start_Simulation(" DIRECT")
            #print("evaluate")

        for idx in solutions:
            solutions[idx].Wait_For_Simulation_To_End()

    

