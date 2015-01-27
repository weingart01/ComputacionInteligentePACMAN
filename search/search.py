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
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue

    frontera = PriorityQueue()
    frontera.push((problem.getStartState(),[]),0)
    nodosCerrados = set()

    while not frontera.isEmpty():
        estadoActual, path = frontera.pop()
        if problem.isGoalState(estadoActual):
            return path
        if estadoActual not in nodosCerrados:
            nodosCerrados.add(estadoActual)
            for hijos, action, cost in problem.getSuccessors(estadoActual):
                if hijos not in nodosCerrados:
                    newpath = path + [action]
                    frontera.push((hijos ,newpath), problem.getCostOfActions(newpath))
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    """print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    from util import PriorityQueue

    frontera = PriorityQueue()
    frontera.push((problem.getStartState(),[]),0)
    nodosCerrados = set()

    while not frontera.isEmpty():
        estadoActual, path = frontera.pop()
        if problem.isGoalState(estadoActual):
            return path
        if estadoActual not in nodosCerrados:
            nodosCerrados.add(estadoActual)
            for hijos, action, cost in problem.getSuccessors(estadoActual):
                if hijos not in nodosCerrados:
                    newpath = path + [action]
                    fn = problem.getCostOfActions(newpath) + heuristic(hijos, problem)
                    frontera.push((hijos ,newpath), fn)
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
