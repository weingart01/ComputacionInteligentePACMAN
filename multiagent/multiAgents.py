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
    remaining food (newFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.
    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    #Let's do the manhatten distance
    distance = []
    foodList = currentGameState.getFood().asList()
    pacmanPos = list(successorGameState.getPacmanPosition())
    if action == 'Stop':
        return -99999.99
    for ghostState in newGhostStates:
        if ghostState.getPosition() == tuple(pacmanPos) and ghostState.scaredTimer is 0:
            return -99999.99
    #Non-Scared Ghost reaches the PACMAN

    for food in foodList:
        distance.append(-1*util.manhattanDistance(food,pacmanPos))
    return max(distance)

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
    self.depth = int(depth)
    self.pacmanIndex = 0



class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    def maximize(self, gameState, depth, agentIndex):
        maxEval= float("-inf")
        if gameState.isWin() or gameState.isLose() or depth > self.depth:
            return self.evaluationFunction(gameState)
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            tempEval = self.minimize(successor, depth, 1)
            #maxEval = max(maxEval, tempEval)
            if tempEval > maxEval:
                maxEval = tempEval
                maxAction = action
        if depth == 1:
            return maxAction
        else:
            return maxEval

    def minimize(self, gameState, depth, agent):
        minEval= float("inf")
        numAgents = gameState.getNumAgents()
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        for action in gameState.getLegalActions(agent):
            successor = gameState.generateSuccessor(agent, action)
            #miramos el ultimo nodo fantasma
            if agent == numAgents - 1:
                tempEval = self.maximize(successor, depth+1, 0)
            else:
                #Busca la min function de otro fantasma
                tempEval = self.minimize(successor, depth, agent+1)
            minEval = min(tempEval, minEval)
            #if tempEval < minEval:
            #    minEval = tempEval

        return minEval

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
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
        "*** YOUR CODE HERE ***"
        maxAction = self.maximize(gameState, 1, 0)
        return self.maximize(gameState,1,0)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def max_prune(self, gameState, depth, agentIndex, alpha, beta):
        # init the variables
        maxEval= float("-inf")
        # if this is a leaf node with no more actions, return the evaluation function at this state
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        # otherwise, for evert action, find the successor, and run the minimize function on it. when a value
        # is returned, check to see if it's a new max value (or if it's bigger than the minimizer's best, then prune)
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
        # run minimize (the minimize function will stack ghost responses)
            tempEval = self.min_prune(successor, depth, 1, alpha, beta)
        #prune
            if tempEval > beta:
                return tempEval
            if tempEval > maxEval:
                maxEval = tempEval
                maxAction = action
            #reassign alpha
            alpha = max(alpha, maxEval)
            # if this is the first depth, then we're trying to return an ACTION to take. otherwise, we're returning a number. This
            # could theoretically be a tuple with both, but i'm lazy.
        if depth == 1:
            return maxAction
        else:
            return maxEval

    def min_prune(self, gameState, depth, agentIndex, alpha, beta):
        minEval= float("inf")
        # we don't know how many ghosts there are, so we have to run minimize
        # on a general case based off the number of agents
        numAgents = gameState.getNumAgents()
        # if a leaf node, return the eval function!
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        # for every move possible by this ghost
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
        # if this is the last ghost to minimize
            if agentIndex == numAgents - 1:
            # if we are at our depth limit, return the eval function
                if depth == self.depth:
                    tempEval = self.evaluationFunction(successor)
                else:
                    #maximize!
                    tempEval = self.max_prune(successor, depth+1, 0, alpha, beta)
                    # pass this state on to the next ghost
            else:
                tempEval = self.min_prune(successor, depth, agentIndex+1, alpha, beta)
            #prune
            if tempEval < alpha:
                return tempEval
            if tempEval < minEval:
                minEval = tempEval
                minAction = action
            # new beta
            beta = min(beta, minEval)
        return minEval

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        maxAction = self.max_prune(gameState, 1, 0, float("-inf"), float("inf"))
        return maxAction

 
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
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
        "*** YOUR CODE HERE ***"
        curDepth = 0
        currentAgentIndex = 0
        val = self.value(gameState, currentAgentIndex, curDepth)
        #print "Returning %s" % str(val)
        return val[0]

    def value(self, gameState, currentAgentIndex, curDepth): 
        if currentAgentIndex >= gameState.getNumAgents():
            currentAgentIndex = 0
            curDepth += 1

        if curDepth == self.depth:
            return self.evaluationFunction(gameState)

        if currentAgentIndex == self.pacmanIndex:
            return self.maxValue(gameState, currentAgentIndex, curDepth)
        else:
            return self.expValue(gameState, currentAgentIndex, curDepth)
        
    def expValue(self, gameState, currentAgentIndex, curDepth):
        v = ["unknown", 0]
        
        if not gameState.getLegalActions(currentAgentIndex):
            return self.evaluationFunction(gameState)
        
        prob = 1.0/len(gameState.getLegalActions(currentAgentIndex))
        
        for action in gameState.getLegalActions(currentAgentIndex):
            if action == "Stop":
                continue
            
            retVal = self.value(gameState.generateSuccessor(currentAgentIndex, action), currentAgentIndex + 1, curDepth)
            if type(retVal) is tuple:
                retVal = retVal[1] 

            v[1] += retVal * prob
            v[0] = action
        
        #print "Returning minValue: '%s' for agent %d" % (str(v), currentAgentIndex)
        return tuple(v)

    def maxValue(self, gameState, currentAgentIndex, curDepth):
        v = ("unknown", -1*float("inf"))
        
        if not gameState.getLegalActions(currentAgentIndex):
            return self.evaluationFunction(gameState)

        for action in gameState.getLegalActions(currentAgentIndex):
            if action == "Stop":
                continue
            
            retVal = self.value(gameState.generateSuccessor(currentAgentIndex, action), currentAgentIndex + 1, curDepth)
            if type(retVal) is tuple:
                retVal = retVal[1] 

            vNew = max(v[1], retVal)

            if vNew is not v[1]:
                v = (action, vNew) 
        
        #print "Returning maxValue: '%s' for agent %d" % (str(v), currentAgentIndex)
        return v
 

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).
    DESCRIPTION: Evaluation is based on the 
    -> Distance to the nearest food
    -> Closest Ghost
    -> The current score
    -> How many capsules are on the board
    -> How many scared ghosts there are
    The goal is to try to increase the score while getting closer to other food pellets,
    staying away from the closestGhost (if possible) unless
    are scared, getting rid of capsules, and eating 
    scaredGhosts whenever possible
    """        
    "*** YOUR CODE HERE ***"
    #Let's do the manhatten distance
    distanceToFood = []
    distanceToNearestGhost = []
    distanceToCapsules = []
    score = 0

    foodList = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()
    capsuleList = currentGameState.getCapsules()
    numOfScaredGhosts = 0

    pacmanPos = list(currentGameState.getPacmanPosition())

    for ghostState in ghostStates:
        if ghostState.scaredTimer is 0:
            numOfScaredGhosts += 1
            distanceToNearestGhost.append(0)
            continue

        gCoord = ghostState.getPosition()
        x = abs(gCoord[0] - pacmanPos[0])
        y = abs(gCoord[1] - pacmanPos[1])
        if (x+y) == 0:
            distanceToNearestGhost.append(0)
        else:
            distanceToNearestGhost.append(-1.0/(x+y))

    for food in foodList:
        x = abs(food[0] - pacmanPos[0])
        y = abs(food[1] - pacmanPos[1])
        distanceToFood.append(-1*(x+y))  

    if not distanceToFood:
        distanceToFood.append(0)

    return max(distanceToFood) + min(distanceToNearestGhost) + currentGameState.getScore() - 100*len(capsuleList) - 20*(len(ghostStates) - numOfScaredGhosts)
 

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