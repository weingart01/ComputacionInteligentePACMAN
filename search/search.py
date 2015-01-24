# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions

    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    # Carga de las acciones disponibles
    from game import Directions
    from util import Stack

    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    n = Directions.NORTH

    # Estructura del DFS
    frontera = Stack()  # es la lista
    frontera.push(problem.getStartState())  # anadimos el nodo inical a la frontera
    estadoActual = problem.getStartState()  # obtenemos el estado del nodo inicial
    nodosCerrados = set()
    nodosCerrados.add(estadoActual)  # creamos la estructura set para los nodos cerrados

    # result es el diccionario del tipo tupla que nos indica la solucion de los caminos
    # a seguir para la solucion del problema

    result = {}
    nodos = 0
    result[estadoActual] = [estadoActual, []]

    while (problem.isGoalState(estadoActual) == False):
        estadosSucesores = problem.getSuccessors(estadoActual)
        for hijos in estadosSucesores:
            if hijos[0] not in nodosCerrados:
                frontera.push(hijos)
                result[hijos[0]] = (estadoActual, [])
                for elements in result[estadoActual][1]:
                    result[hijos[0]][1].append(elements)
                result[hijos[0]][1].append(hijos[1])

        estadoActual = frontera.pop()[0]
        nodosCerrados.add(estadoActual)

    print "Nodos analizados: %i" % nodos

    return result[estadoActual][1]

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    closedset = []
    fringe = util.PriorityQueue()
    start = problem.getStartState()
    fringe.push( (start, []), heuristic(start, problem))

    while not fringe.isEmpty():
        node, actions = fringe.pop()

        if problem.isGoalState(node):
            return actions

        closedset.append(node)

        for coord, direction, cost in problem.getSuccessors(node):
            if not coord in closedset:
                new_actions = actions + [direction]
                score = problem.getCostOfActions(new_actions) + heuristic(coord, problem)
                fringe.push( (coord, new_actions), score)

    return []
    "*** YOUR CODE HERE ***"
    """
    from game import Directions
    from util import Queue

    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    n = Directions.NORTH

    # Estructura del DFS
    frontera = Queue()  # es la lista
    frontera.push(problem.getStartState())  # anadimos el nodo inical a la frontera
    estadoActual = problem.getStartState()  # obtenemos el estado del nodo inicial
    nodosCerrados = set()
    nodosCerrados.add(estadoActual)  # creamos la estructura set para los nodos cerrados

    # result es el diccionario del tipo tupla que nos indica la solucion de los caminos
    # a seguir para la solucion del problema

    result = {}
    nodos = 0
    result[estadoActual] = [estadoActual, []]

    print problem.isGoalState()

    while (problem.isGoalState(estadoActual) == False & frontera.isEmpty() == False):
        estadosSucesores = problem.getSuccessors(estadoActual)
        for hijos in estadosSucesores:
            if hijos[0] not in nodosCerrados:
                frontera.push(hijos)
                result[hijos[0]] = (estadoActual, [])
                for elements in result[estadoActual][1]:
                    result[hijos[0]][1].append(elements)
                result[hijos[0]][1].append(hijos[1])

        estadoActual = frontera.pop()[0]
        nodosCerrados.add(estadoActual)

    print "Nodos analizados: %i" % nodos

    return result[estadoActual][1]"""
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    """
    from game import Directions
    from util import PriorityQueue

    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    n = Directions.NORTH

    estadoActual = problem.getStartState()
    estadosCerrados = set()
    frontera = PriorityQueue()
    result = {}
    result[estadoActual] = (estadoActual, [], 0)
    distanciah = result[estadoActual][2] + heuristic(estadoActual, problem)
    frontera.push(estadoActual, distanciah)

    while (frontera.isEmpty() == False):
        estadoActual = frontera.pop()
        if (problem.isGoalState(estadoActual)):
            return result[estadoActual][1]
        else:
            estadosCerrados.add(estadoActual)
            estadosSucesores = problem.getSuccessors(estadoActual)
            for hijos in estadosSucesores:
                if hijos[0] not in estadosCerrados:
                    result[hijos[0]] = (estadoActual, [], result[estadoActual][2] + hijos[2])
                    for elements in result[estadoActual][1]:
                        result[hijos[0]][1].append(elements)
                    result[hijos[0]][1].append(hijos[1])
                    distanciah = result[hijos[0]][2] + heuristic(hijos[0], problem)
                    frontera.push(hijos[0], distanciah)

    visitedNodes = set()
    pQueue = util.PriorityQueue()
    goalState = (1,1)
    d = {}
    nodo = problem.getStartState()
    d[nodo] = (nodo, [], 0)
    distheur = d[nodo][2] + heuristic(nodo, problem)
    pQueue.push(nodo, distheur)

    while pQueue.isEmpty() == False:
        nodo = pQueue.pop()

        if problem.isGoalState(nodo):
            return d[nodo][1]

        visitedNodes.add(nodo)

        for nb in problem.getSuccessors(nodo):
            if nb[0] not in visitedNodes:
                d[nb[0]] = (nodo, [], d[nodo][2] + nb[2])
                for mov in d[nodo][1]:
                    d[nb[0]][1].append(mov)
                d[nb[0]][1].append(nb[1])
                distheur = d[nb[0]][2] + heuristic(nb[0], problem)
                pQueue.push(nb[0], distheur)
    """
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    #variable for whether or not goal has been reached
    #variable for whether or not goal has been reached
    reachedGoal=False
    exploredAll=False
    previousCost = 0;
    startState=problem.getStartState()
    exploredStatesDictionary=util.Counter()
    exploredStatesDictionary[0] = problem.getStartState()
    frontierDictionary=util.Counter()
    frontierList=problem.getSuccessors(problem.getStartState())

    #hash table for list of vertices as key
    vectorDictionary={}
    #create stack to hold the frontier states
    frontierQueue=util.PriorityQueue()
    #queue to hold list of actions
    actionsQueue=[]
    addedNodes=[]

        #push the frontier states onto the stack
        for i in frontierList:
        fNode=i
        frontierQueue.push(fNode,actionsQueue)

    for i in frontierList:
    actionsThisFar=copy.deepcopy(actionsQueue)
    successor = str(i[0])
    vectorDictionary[successor]=actionsThisFar

    #push the frontier states onto the stack
    for i in frontierList:
        fNode=i
        frontierQueue.push(fNode,i[2])
        addedNodes.append(fNode[0])

    #key variable, key to exploredStatesDictionary
    seenAlready=1
    while reachedGoal==False:
        for i in addedNodes:
            popped=addedNodes.pop()
            exploredStatesDictionary[seenAlready] = popped
            seenAlready = seenAlready + 1

    #get next state to explore, the first state from the stack
    #also save the action required to get to that point
    tempState=frontierQueue.pop()
    previousCost = tempState[2]
    nextState=tempState[0]

    nextAction=tempState[1]

    #save the explored state
    exploredStatesDictionary[seenAlready] = nextState

    seenAlready = seenAlready+1


    #next state becomes current state


    #badNode = frontierQueue.pop()
    #firstNode = frontierQueue.pop()
    reset = str(tempState[0])

    #problem
    newActionsList = vectorDictionary[reset]
    newActionsList.append(tempState[1])


    #empty the old action list

    actionsQueue=copy.deepcopy(newActionsList)


    currentState=nextState

    #check if it is goal


    if (problem.isGoalState(currentState)):
        reachedGoal=True

    else:
        #the current state is not the goal
        #acquire the new frontier

        frontierList=problem.getSuccessors(currentState)
        for i in frontierList:
            explored=False
            counter=0
            for k in exploredStatesDictionary:
                stateCo=exploredStatesDictionary[k]
                if ((i[0] == stateCo)):
                    explored = True
                    counter = counter+1

            elif ((explored == False) and (k == ((len(exploredStatesDictionary)))-1)):
                actionsThisFar=copy.deepcopy(actionsQueue)
                successor = str(i[0])
                vectorDictionary[successor]=actionsThisFar
                fNode = i
                hCost=heuristic(i[0],problem)
                newCost = i[2] + previousCost + hCost
                fNode=list(fNode)
                #update
                fNode[2]=newCost
                #back to tuple
                fNode=tuple(fNode)
                frontierQueue.push(fNode, newCost)
                addedNodes.append(fNode[0])
    "*** YOUR CODE HERE ***"
    length = len(actionsQueue)
    return actionsQueue
    """



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
