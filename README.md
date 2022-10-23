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
xxxxxxxxxx
x  1   1 x
x   x  j x
x j x  2 x
x c x    x
xxxxxxxxxx

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
o Tie situations might occur during inserting into the fringe. The precedence used for fringe insertion tie-breaker is
as follows: suck, left, right, down, up
o For DFS and BFS, how to remove the nodes from the fringe is well-defined.
o For others, if costs/g-values/f-values are same, respect the insertion order (first-in first-out).



## TO RUN THE CODE
python cleaner_robot.py <search-type> <input_file>

Example:
python cleaner_robot.py BFS init1.txt

In the output, map is cleaned from dirts as:
xxxxxxxxxx
x        x
x   x  j x
x j x    x
x c x    x
xxxxxxxxxx
### Reporting:
o the number of expanded nodes
o the action sequence to achieve the goal
o the cost of the solution
o the heuristic function value of the initial state if the <search-type> is A*2.
