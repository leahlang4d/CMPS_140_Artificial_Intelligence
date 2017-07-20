# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPosition = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.treeDepth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.treeDepth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
  #******************************************************************
  # Minimax algorithm used for minimizing the loss for the worst case
  # The pseudo used here is from the book and wikipedia.
  #******************************************************************


    #Start with the current best move being negative infinity and
    #for each legel move if action is a better move to make then what is
    #currently there then return that best worst case action for max
    curr_path = float('-inf')
    opt_action = Directions.STOP
    pacmanLegalActions = gameState.getLegalActions(0)
    for action in pacmanLegalActions:
        path = self.minValue(1, gameState.generateSuccessor(0, action))
        if path > curr_path:
            curr_path = path
            opt_action = action
    return opt_action

  def maxValue(self, tree_depth, gameState):
      #test for terminal state see if the tree depth is 4 or pacman loses
      # or wins. Tree depth can be equal to self.treeDepth
      lose = gameState.isLose()
      win = gameState.isWin()
      if tree_depth == 4 or lose or win:
          #evalutation will returns the score of that state
        return self.evaluationFunction(gameState)
      v = float('-inf')
      #loop through pacmans actions to find the best min it can get
      pacmanLegalActions = gameState.getLegalActions(0)
      for action in pacmanLegalActions:
        v = max(v, self.minValue(tree_depth + 1, gameState.generateSuccessor(0,action)))
      return v


  def minValue(self,tree_depth ,gameState):
        lose = gameState.isWin()
        win = gameState.isLose()
        if tree_depth == 4 or lose or win:
          return self.evaluationFunction(gameState)
        v = float('inf')
        #Save what indexes the ghost are
        ghosts = [1, gameState.getNumAgents()]
        #Gets the length of the number of agents
        ghosts_length=len(ghosts)
        #goes through the indexes of ghost
        for numghost in range (0,ghosts_length):
            for action in gameState.getLegalActions(numghost) :
                v = min(v, self.maxValue(tree_depth + 1, gameState.generateSuccessor(numghost, action))) #take average of the min of the max value
            return v

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.treeDepth and self.evaluationFunction
    """
    #*****************************************************************
    #Alpha-beta Pruning
    #Just like min max above but have to keep track of alpha and beta
    #*****************************************************************
    curr_path = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    opt_action = Directions.STOP
    pacmanLegalActions = gameState.getLegalActions(0)
    # need to loop over all the actions
    for action in pacmanLegalActions:
        path = self.minValue(1, alpha, beta, gameState.generateSuccessor(0, action))
        if path > curr_path:
            curr_path = path
            opt_action = action
        #If the min value is greater then current value return it
        if path >= beta:
            return opt_action
        alpha = max(alpha, path)
    return opt_action




  def maxValue(self, tree_depth, alpha, beta , gameState):
       lose = gameState.isLose()
       win = gameState.isWin()
       if tree_depth == 4 or lose or win:
        return self.evaluationFunction(gameState)
       v = float('-inf')
       pacmanLegalActions = gameState.getLegalActions(0)
       for action in pacmanLegalActions:
           v = max(v, self.minValue(tree_depth + 1,alpha, beta, gameState.generateSuccessor(0, action)))
           if v >= beta:
              return v
           alpha = max(alpha, v)
       return v

  def minValue(self, tree_depth,alpha, beta, gameState):
        lose = gameState.isWin()
        win = gameState.isLose()
        if tree_depth == 4 or lose or win:
            return self.evaluationFunction(gameState)
        v = float('inf')
        ghosts = [1, gameState.getNumAgents()]
        ghosts_length = len(ghosts)
        for numghost in range(0, ghosts_length):
            for action in gameState.getLegalActions(numghost):
                v = min(v, self.maxValue(tree_depth + 1,alpha, beta, gameState.generateSuccessor(numghost, action)))
                #if the min(v) is less than alpha then return it else
                #we want beta to be the max min
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """
  numeber_actions = 0
  def getAction(self, gameState):
    """
      Returns the expectimax action using self.treeDepth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """

    curr_path = float('-inf')
    opt_action = Directions.STOP
    pacmanLegalActions = gameState.getLegalActions(0)
    for action in pacmanLegalActions:
        path = self.expectiminimax(1, gameState.generateSuccessor(0, action))
        if path > curr_path:
          curr_path = path
          opt_action = action
    return opt_action




  def expectiminimax(self, tree_depth, gameState):

        lose = gameState.isLose()
        win = gameState.isWin()
        if tree_depth == MultiAgentSearchAgent().treeDepth or lose or win:
            return self.evaluationFunction(gameState)
        ghosts =[1, gameState.getNumAgents()]
        ghosts_length = len(ghosts)
        v = 0
        number_actions=0
        #the only difference here is that we are taking an average score
        for numghost in range(0, ghosts_length):
            for action in gameState.getLegalActions(numghost):
                    number_actions = len(gameState.getLegalActions(numghost))
                    v += self.maxValue(tree_depth + 1, gameState.generateSuccessor(numghost, action))
            return v/number_actions

  def maxValue(self, tree_depth, gameState):
        lose = gameState.isLose()
        win = gameState.isWin()
        if tree_depth == MultiAgentSearchAgent().treeDepth or lose or win:
            return self.evaluationFunction(gameState)
        v = float('-inf')
        pacmanLegalActions = gameState.getLegalActions(0)
        for action in pacmanLegalActions:
            v = max(v, self.expectiminimax(tree_depth + 1, gameState.generateSuccessor(0, action)))
        return v

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

