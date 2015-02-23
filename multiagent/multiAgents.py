# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


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
        currentFood = currentGameState.getFood().asList()
        currentPos = currentGameState.getPacmanPosition()

        # Si el ghost en su siguiente estado es non-Scared (ScaredTimer == 0) y alcanza el agente Pacman
        # sera la peor accion tomada dado que este morira
        for newghostState in newGhostStates:
            if util.manhattanDistance(newghostState.getPosition(),newPos) == 0 and newghostState.scaredTimer == 0:
                return -float("inf")

        # Si nuestro ghost se mantiene en la misma posicion es el peor caso de accion
        if currentPos == newPos:
            return -float("inf")

        # Si hay comida cercana la accion que menos descuenta es la accion que va a la posicion de la comida mas cercana
        # De no haber comida, nuestro juego ha llegado a su exito
        if currentFood.__len__() > 0:
            closest_food = float("inf")
            for foodPos in currentFood:
                closest_food = min(closest_food,util.manhattanDistance(foodPos,newPos))
            return -closest_food
        else:
            return successorGameState.isWin()

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

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        # La funcion de evaluacion implementada anteriormente ira cediendo el turno al correspondiente agente
        # partiendo del root node max que en este caso es el pacman
        depth = 1
        agent = self.pacmanIndex
        return self.minimax_function(gameState, depth, agent)

    # Tal como en el patron del codigo de las transparencias indica, empleamos el metodo minimax_function
    # para ir cediendo el turno a cada uno e los agentes fantasma o bien al Pacman
    def minimax_function(self, gameState, depth, agent):
        # Si el indice del agente figura entre [1,numero_de_agentes-1] entonces estos haran
        # desempenaran acciones para minimizar el maximo score
        if agent in range(1,gameState.getNumAgents()):
            return self.min_value(gameState, depth, agent)
        # Si por el contrario el indice corresponde al pacman este tratara de maximizar el score
        # dadas unas acciones permitidas en un estado determinado
        if agent == self.pacmanIndex:
            return self.max_value(gameState, depth, agent)

    def max_value(self, gameState, depth, agent):
        # Si hemos llegado al fin de juego sea este victoria o derrota antes de que la altura corriente
        # rebase la maxima, retornamos la funcion de evaluacion
        if gameState.isWin() or gameState.isLose() or depth > self.depth:
            return self.evaluationFunction(gameState)

        # Fijamos el peor caso
        maximum = -float("inf")
        # Para cada accion disponible en un gameState evaluamos su puntuacion y en caso de ser mayor
        # que la actual actualizamos la puntuacion y la accion
        for action in gameState.getLegalActions(agent):
            value = self.minimax_function(gameState.generateSuccessor(agent,action), depth, agent+1)
            if value > maximum:
                maximum = value
                minimax_action = action
        # El resultado del ejercicio es la minimax action, asi pues por recursividad volvemos al root node
        # fijamos la minimax_action para la mejor puntuacion y lo retornamos
        if depth == 1:
            return minimax_action
        else:
            return maximum

    def min_value(self, gameState, depth, agent):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        
        # Fijamos el peor caso
        minimum = float("inf")    
        # Al igual que antes pretendemos buscar la mejor accion, en este caso la accion que minimice el score        
        for action in gameState.getLegalActions(agent):
            # Miramos el score minimo para cada combinacion de acciones de los agentes fantasmas que nos llevan
            # a diferentes gameStates
            if agent in range (1, gameState.getNumAgents()-1):
                value = self.minimax_function(gameState.generateSuccessor(agent, action), depth, agent+1)
            # Si nuestro agente es el ultimo en mover ya habremos acabado un nivel de profundidad(todos ya han movido)
            # y por tanto le toca a jugar al agente Pacman
            if agent == gameState.getNumAgents()-1:
                value = self.minimax_function(gameState.generateSuccessor(agent, action), depth+1, self.pacmanIndex)
            # Actualizamos el minimo mejor caso
            minimum = min(minimum, value)

        return minimum

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        depth = 1
        agent = self.pacmanIndex
        alpha = float("-inf")
        beta = float("inf")
        return self.max_value(gameState, depth, agent, alpha, beta)

    def alpha_beta_function(self, gameState, depth, agent, alpha, beta):
        # Si el indice del agente figura entre [1,numero_de_agentes-1] entonces estos haran
        # desempenaran acciones para minimizar el maximo score
        if agent in range(1,gameState.getNumAgents()):
            return self.min_value(gameState, depth, agent, alpha, beta)
        # Si por el contrario el indice corresponde al pacman este tratara de maximizar el score
        # dadas unas acciones permitidas en un estado determinado
        if agent == self.pacmanIndex:
            return self.max_value(gameState, depth, agent, alpha, beta)


    def max_value(self, gameState, depth, agent, alpha, beta):
        # si nos encontramos con un 
        if gameState.isWin() or gameState.isLose() or depth > self.depth:
            return self.evaluationFunction(gameState)

        # iniciamos la variable que nos proporcionara el mejor caso en los sucesores de este nodo en el peor de sus casos
        maximum = float("-inf")
        # otherwise, for evert action, find the successor, and run the minimize function on it. when a value
        # is returned, check to see if it's a new max value (or if it's bigger than the minimizer's best, then prune)
        for action in gameState.getLegalActions(agent):
            # run minimize (the minimize function will stack ghost responses)
            value = self.alpha_beta_function(gameState.generateSuccessor(agent, action), depth, agent+1, alpha, beta)

            # realizamos la poda si es que el valor es mayor que el beta
            if value > beta:
                return value

            # actualizamos la mejor accion que se pueda realizar si el value actual es mayor que el maximum
            if value > maximum:
                maximum = value
                alpha_beta_action = action

            # actualizamos el alpha en el mejor caso
            alpha = max(alpha, maximum)

        # if this is the first depth, then we're trying to return an ACTION to take. otherwise, we're returning a number. This
        # could theoretically be a tuple with both, but i'm lazy.
        if depth == 1:
            return alpha_beta_action
        else:
            return maximum



    def min_value(self, gameState, depth, agent, alpha, beta):
        # we don't know how many ghosts there are, so we have to run minimize
        # on a general case based off the number of agents
      
        # if a leaf node, return the eval function!
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        minimum= float("inf")
        numAgents = gameState.getNumAgents()

        # for every move possible by this ghost
        for action in gameState.getLegalActions(agent):
            if agent in range (1, gameState.getNumAgents()-1):
                value = self.alpha_beta_function(gameState.generateSuccessor(agent, action), depth, agent+1)
            # Si nuestro agente es el ultimo en mover ya habremos acabado un nivel de profundidad(todos ya han movido)
            # y por tanto le toca a jugar al agente Pacman
            if agent == gameState.getNumAgents()-1:
                value = self.alpha_beta_function(gameState.generateSuccessor(agent, action), depth+1, self.pacmanIndex)

            #prune
            if value < alpha:
                return value
            if value < minimum:
                minimum = value
                alpha_beta_action = action

            # new beta
            beta = min(beta, minimum)
        return minimum

        

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.maximize(gameState, 1, 0)
        

    def maximize(self, gameState, depth, agentIndex):
        maxEval= float("-inf")
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)


        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
        
            # run minimize (the minimize function will stack ghost responses)
            tempEval = self.minimize(successor, depth, 1)
            if tempEval > maxEval:
                maxEval = tempEval
                maxAction = action

        # if this is the first depth, then we're trying to return an ACTION to take. otherwise, we're returning a number. This
        # could theoretically be a tuple with both, but i'm lazy.
        if depth == 1:
            return maxAction
        else:
            return maxEval

    def minimize(self, gameState, depth, agentIndex):

        # we will add to this evaluation based on an even weighting of each action.
        minEval= 0
        numAgents = gameState.getNumAgents()
      
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        
        legalActions = gameState.getLegalActions(agentIndex)
        # calculate the weighting for each minimize action (even distribution over the legal moves).
        prob = 1.0/len(legalActions)
        for action in legalActions:
            successor = gameState.generateSuccessor(agentIndex, action)
            # if this is the last ghost..
            if agentIndex == numAgents - 1:
            # if we are at our depth limit...
                if depth == self.depth:
                    tempEval = self.evaluationFunction(successor)
                else: #maximize!
                    tempEval = self.maximize(successor, depth+1, 0)
            # we have to minimize with another ghost still.
            else:
                tempEval = self.minimize(successor, depth, agentIndex+1)

            # add the tempEval to the cumulative total, weighting by probability
            minEval += tempEval * prob

        return minEval

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

