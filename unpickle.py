import pickle
from parallelHillClimber import PARALLEL_HILL_CLIMBER
from pathlib import Path

root = Path(".")
myPath = root/"pickledRobots"/"pickle10"

with open(myPath, "rb") as f:
    p1 = pickle.load(f)

p1.Start_Simulation(' GUI')