from solution import SOLUTION
from parallelHillClimber import PARALLEL_HILL_CLIMBER
import pickle

# sol = SOLUTION(1)
# sol.Start_Simulation('GUI')

phc = PARALLEL_HILL_CLIMBER()
phc.Evolve()
phc.Show_Best()

with open ("pickle0", "wb") as f:
    pickle.dump(phc, f)