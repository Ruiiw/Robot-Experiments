import pickle
from parallelHillClimber import PARALLEL_HILL_CLIMBER

with open("pickle2", "rb") as f:
    p1 = pickle.load(f)

p1.Start_Simulation(' GUI')