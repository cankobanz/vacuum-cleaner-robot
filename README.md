# room-cleaner-robot
Robot that cleans room from dirts. Finds the optimum path eventually.  Same algorithms are applied as in finding path to escape a maze. This project was the first homework of Artificial Intelligence course I have taken.

In this project, the cleaner robot cleans the room by finding its path using various algorithms:
- DFS: Depth First Search
- BFS: Breadth First Search
- UCS: Uniform-Cost Search
- GS: Greedy Search that uses the Manhattan Distance to the closest dirt as the heuristics function.
- A*1: A* Search with Manhattan Distance to the closest dirt as the heuristics function.
- A*2: A* Search with heuristic that is explained  in project report file.

Input files look like this:  
![image](https://user-images.githubusercontent.com/81170575/197387572-b8ca759c-eded-4b55-8995-4985a80de7a0.png)

where:  
c is the agent(cleaner),  
x represents walls,  
<digits> represents dirts,  
j is the jumper  which moves the agent that moves an incoming agent to the next grid. 
  If the corresponding grid is occupied with an obstacle, the location of the agent will not change at all. 
  There are no jumpers placed next to each other. 
  
The vacuum cleaner has five actions:  
  - left, right, up, down moves the cleaner one grid, unless that grid is an obstacle.
  - suck action that sucks one dirt. (in order to clean n dirts in a grid, suck action should be executed n times)
  
Costs of the actions:
- Left and right: 1
- Up and down: 2
- Suck: 5
- Cost of actions are as above, even though those actions do not change the state of the agent.


Tie-breaker:
- Tie situations might occur during inserting into the fringe. The precedence used for fringe insertion tie-breaker is
as follows: suck, left, right, down, up
- For DFS and BFS, how to remove the nodes from the fringe is well-defined.
- For others, if costs/g-values/f-values are same, respect the insertion order (first-in first-out).



## TO RUN THE CODE
python cleaner_robot.py <search-type> <input_file>
where <search-type> can be DFS, BFS, UCS, GS, A*1 or A*2
  

Example Running Code:
python cleaner_robot.py BFS init1.txt

In the output, map is cleaned from dirts as:  
![image](https://user-images.githubusercontent.com/81170575/197387588-b0770a9e-8815-45be-87f2-551606ec64d2.png)

### Reporting:
- the number of expanded nodes
- the action sequence to achieve the goal
- the cost of the solution
- the heuristic function value of the initial state if the <search-type> is A*2.
  
Example Output:  
python robot_cleaner.py BFS init1.txt  
number of expanded nodes: 28  
path: right down right right suck suck right suck   
cost of the solution: 21  
