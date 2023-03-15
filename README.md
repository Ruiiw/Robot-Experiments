# Evolutionary-Robot

The goal for this project is to randomly generate and mutate robots to get the ones that can move the longest distance. For the engineer option, I ran the program for 50,000 simulations. 

![](https://github.com/Ruiiw/CS396-Robots/blob/finalProject/teaser.gif)

Link to the 2 minute summary video: https://youtu.be/P0ujz6WudWk


## Usage
To run the program, install Python-based physics engine pybullet, and then run the command "python3 search.py" to generate simulations of 3D creatures. The code is intended to run on Mac OS. 

I saved a few best robots to demonstrate the results. Navigate to the file “test_body.py” and change the integer input to SIMULATION to an integer in the range of [1, 8], then run the file to see one of the 8 saved robots. Note that if you have already run "python3 search.py", the urdf and nndf files are omitted. In that case, copy all the files from the directory “savedRobots” to the root directory, and then run “test_body.py”. 


## Robot Generation
The code starts with generating an initial cube. Then for each round, we randomly select a cube that has been generated and append a new cube of random size on a randomly selected cube face among [-x, +x, -y, +y, -z, +z] directions, as long as there is free space for the new cube. This allows the creature to grow in 3D space. All connected cubes are joined by joints, and some joints are randomly assigned with sensor neurons. The body parts with sensors are colored green. Since the creature has a fully connected brain, every motor neuron at every joint is connected to every sensor neuron, which allows the creature to move. 

![IMG_0815](https://user-images.githubusercontent.com/75329093/220264803-51d24e0d-7684-4923-b4a9-2fef3efc5d69.jpg)


This diagram illustrates how the genotype of each robot maps to its phenotype.
![IMG_0879](https://user-images.githubusercontent.com/75329093/225231830-2567cd2a-9020-4f63-94ae-205077c39782.jpg)


## Robot Mutation
Mutation of the robots in each generation is done with parallel hill climber. In each generation, each parent robot in the population spawns a child that has a changed value in the weights of the fully connected brain, which might lead to an improvement or deterioration in its performance. If the child behaves better than the parent (meaning it has higher fitness value), we replace the parent with the child. After running 500 generations with populations of size 10 for 10 simulations, we end up with 10 best parent robots that can move the furthest in their lineage. 

![IMG_0878](https://user-images.githubusercontent.com/75329093/225232017-cb7dddb9-1d0e-4494-829b-2a965d5ff1b4.jpg)

![IMG_0881](https://user-images.githubusercontent.com/75329093/225232558-8075da78-6eb2-425d-bebf-ffb06d4eab0d.jpg)


## Results

![fitnessGraph](https://user-images.githubusercontent.com/75329093/225227302-7f8b9895-f108-46e0-91eb-020ac511185f.jpg)

From the fitness graph, we can see that parallel hill climber does a good job in improving each robot’s locomotion, as most robot’s fitness values’ still increase after 300 generations. However, since the method above only mutates the brain of the robot, it is very hard to improve the robot’s locomotion by only changing it’s synapse weights sometimes because a robot might be generated with a body that is not suitable for moving (robot from run 10 might be an example of that.) Potential future work could focus on adding or removing a link on the robot's body in each generation to evolve the robot’s body for better performance as well. 


## Credit
This project is a Northwestern University CS396 (Artificial Life) assignment based on Ludobots tutorial and Karl Sims' paper.
