# Evolutionary-Robot

This project is a Northwestern University CS396 (Artificial Life) assignment based on Ludobots tutorial and Karl Sims' paper. To run the program, install Python-based physics engine pybullet, and then run the command "python3 search.py" to generate simulations of 3D creatures. 

![](https://github.com/Ruiiw/CS396-Robots/blob/finalProject/teaser.gif)

The code starts with generating an initial cube. Then for each round, we randomly select a cube that has been generated and append a new cube of random size on a randomly selected cube face among [-x, +x, -y, +y, -z, +z] directions, as long as there is free space for the new cube. This allows the creature to grow in 3D space. All connected cubes are joined by joints, and some joints are randomly assigned with sensor neurons. The body parts with sensors are colored green. Since the creature has a fully connected brain, every motor neuron at every joint is connected to every sensor neuron, which allows the creature to move. 

![IMG_0815](https://user-images.githubusercontent.com/75329093/220264803-51d24e0d-7684-4923-b4a9-2fef3efc5d69.jpg)
