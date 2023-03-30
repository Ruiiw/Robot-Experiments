import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER
import matplotlib.pyplot as plt
import numpy as np
import constants as c
import pickle
from pathlib import Path

root = Path(".")

for i in range(1):
    np.random.seed(i)
    phc = PARALLEL_HILL_CLIMBER()
    phc.Evolve()
    best = phc.Show_Best()
    pickleName = "pickle" + str(i)
    myPath = root/"pickledRobots"/pickleName
    with open (myPath, "wb") as f:
        pickle.dump(best, f)
    plt.plot([j + 1 for j in range(c.numberOfGenerations)], phc.best_fitnesses, label="Run " + str(i))
    print("FINISH RUN")


plt.title("Best Fitnesses Versus Generation")
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.legend()

plt.savefig("fitnessGraph.jpg")