import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER
import matplotlib.pyplot as plt
import numpy as np
import constants as c
import pickle

# phc = PARALLEL_HILL_CLIMBER()
# phc.Evolve()
# #phc.Show_Best()
# best = phc.Show_Best()

# with open ("pickle0", "wb") as f:
#     pickle.dump(best, f)

for i in range(1, 3):
    np.random.seed(i)
    phc = PARALLEL_HILL_CLIMBER()
    phc.Evolve()
    best = phc.Show_Best()
    with open ("pickle" + str(i), "wb") as f:
        pickle.dump(best, f)
    plt.plot([j + 1 for j in range(c.numberOfGenerations)], phc.best_fitnesses, label="Run " + str(i))
    print("FINISH RUN")


plt.title("Best Fitnesses Versus Generation")
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.legend()

plt.savefig("fitnessGraph.jpg")