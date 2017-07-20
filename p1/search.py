# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def startingState(self):
    """
    Returns the start state for the search problem 
    """
    util.raiseNotDefined()

  def isGoal(self, state): #isGoal -> isGoal
    """
    state: Search state

    Returns True if and only if the state is a valid goal state
    """
    util.raiseNotDefined()

  def successorStates(self, state): #successorStates -> successorsOf
    """
    state: Search state
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
    """
    util.raiseNotDefined()

  def actionsCost(self, actions): #actionsCost -> actionsCost
    """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
    """
    util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:

  print "Start:", problem.startingState()
  print "Is the start a goal?", problem.isGoal(problem.startingState())
  print "Start's successors:", problem.successorStates(problem.startingState())\

  *** Took pseudo code from bfs non-recursive wikipedia page since it acts like a
        dfs just without a queue.
        https://en.wikipedia.org/wiki/Breadth-first_search ***
   """
  #print "Start:", problem.startingState()
  #print "Is the start a goal?", problem.isGoal(problem.startingState())
  #print "Start's successors:", problem.successorStates(problem.startingState())
  from util import Stack
  actionStack = Stack()
  visited_list = list()
  root = problem.startingState()
  actionStack.push((root, [])) #First node being added to the stack
  visited_list.append(root)

  while actionStack is not None:
        current = actionStack.pop() #check the top of the stack
        coordniates = current[0] #first part of tuple (x,y)
        path = current[1] #the direction in which the path is moving North, East, etc.
        if problem.isGoal(coordniates):
            print path
            return path
        successors = problem.successorStates(coordniates)
        for successor in successors:
            if successor[0] not in visited_list: #loops through successors to determine if they have been visited or not
                copy_path = path[:]
                #print "copy_path", copy_path
                copy_path.append(successor[1])
                visited_list.append(successor[0])
                print "visited", visited_list
                print
                actionStack.push((successor[0], copy_path))

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"

  from util import Queue

  action_queue = Queue()
  visited_list = list()
  root = problem.startingState()
  action_queue.push((root, []))


  while action_queue is not None:
        current = action_queue.pop()
        coordinates = current[0]
        path = current[1]
        if problem.isGoal(coordinates):
            return path
        successors = problem.successorStates(coordinates)
        for successor in successors:
            if successor[0] not in visited_list:
                copy_path = path[:]
                copy_path.append(successor[1])
                visited_list.append(successor[0])
                action_queue.push((successor[0],  copy_path))
              #util.raiseNotDefined()
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "

  from util import PriorityQueue
  #print "Start:", problem.startingState()
  #print "Start's successors:", problem.successorStates(problem.startingState())

  node = problem.startingState()
  frontier = PriorityQueue()
  visited_list = list()
  frontier.push((node, [], 0), 0)


  while frontier is not None:
          current = frontier.pop()
          coordniates = current[0]
          path = current[1]
          cost = current[2]
          if problem.isGoal(coordniates):
              return path
          successors = problem.successorStates(coordniates)
          for successor in successors:
              if successor[0] not in visited_list:
                  copy_path = path[:]
                  cost = cost + successor[2]
                  copy_path.append(successor[1])
                  visited_list.append((successor[0]))
                  frontier.push((successor[0], copy_path, cost), cost)

  #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  from util import PriorityQueue
  node = problem.startingState()
  frontier = PriorityQueue()
  visited_list = list()
  frontier.push((node, [], 0), 0)


  while frontier is not None:
        current = frontier.pop()
        coordinates = current[0]
        path = current[1]
        cost = current[2]
        if problem.isGoal(coordinates):
            return path
        succesors = problem.successorStates(coordinates)
        for successor in succesors:
            if successor[0] not in visited_list:
                copy_path = path[:]
                cost = successor[2] + cost
                copy_path.append(successor[1])
                visited_list.append(successor[0])
                problem_heuristic = cost + heuristic(successor[0], problem)
                frontier.push((successor[0], copy_path, cost), problem_heuristic)




  #util.raiseNotDefined()
    

  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
