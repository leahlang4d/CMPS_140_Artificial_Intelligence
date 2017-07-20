# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  def __init__(self, mdp, discountRate = 0.9, iters = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.

      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
    self.mdp = mdp
    self.discountRate = discountRate
    self.iters = iters
    self.values = util.Counter() # A Counter is a dict with default 0

    #which is an extension of the Pythons default dictionary with default values
    #of all keys set to zero so you dont need to initialize the
    #value for each state

    """Description:
    [Commented throughout the lines.]
    """
    """ YOUR CODE HERE """


    for iter in range(iters): #iterate through the amount of iterations
        states = self.mdp.getStates()
        best_value = util.Counter()#temporary best value Counter. Will store the state
        for state in states: #get all possible states
            value_actions = self.mdp.getPossibleActions(state)
            maxValue = float('-inf') #set the max value to be the lowest possible min
            for action in value_actions:#for actions that are possible actions from this state
                totalValue = 0
                t_next_prob = self.mdp.getTransitionStatesAndProbs(state, action)
                for next_state, probability in t_next_prob: #t_next_prob(nextState, prob) for all successors to this specified state
                    value_reward = self.mdp.getReward(state, action, next_state)
                    value = self.values[next_state]
                    totalValue += probability * (value_reward + (self.discountRate * value)) #apply value iteration
                if totalValue >= maxValue:
                    maxValue = totalValue
                    best_value[state] = maxValue #save the max value to best_value counter
        self.values = best_value #returning values of counter for each state


    #util.raiseNotDefined()
    """ END CODE """

  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """
    return self.values[state]

    """Description:
    [Enter a description of what you did here.]
    """
    """ YOUR CODE HERE """
    util.raiseNotDefined()
    """ END CODE """

  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    """Description:
    [For Qvalue it iterates through the states and
     probability of that state and adds them together to the totalValue.]
    """
    """ YOUR CODE HERE """
    totalQvalue = 0
    tStatesandProb = self.mdp.getTransitionStatesAndProbs(state, action)
    #iterate through possible maxes and find the best reward the tuple is (nextState(int,int), transistionProbablity)
    for next_state, probability in tStatesandProb: #doAction
        #look at slide 32 in AI M4
        reward = self.mdp.getReward(state, action, next_state)
        value = self.values[next_state]
        totalQvalue += probability * (reward + (self.discountRate * value))
    return totalQvalue

    util.raiseNotDefined()
    """ END CODE """

  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """

    """Description:
    [Check to see if the state is the terminal state, if not then take that
    action of that state and find the best action that that state can take.]
    """
    """ YOUR CODE HERE """
    terminalState = self.mdp.isTerminal(state)
    if terminalState:
        return None
    value = float('-inf')
    b_action = 0
    actions = self.mdp.getPossibleActions(state)
    for action in actions:
        tmp_best = self.getQValue(state, action)
        if tmp_best >= value:
            value = tmp_best
            b_action = action
    return b_action
    #util.raiseNotDefined()
    """ END CODE """

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
