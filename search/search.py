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
    from util import Stack                       # utilizamos el EDA Stack para la implementacion de la frontera
    frontera = Stack()                           # es la lista frontera, de los nodos a analizar
    frontera.push((problem.getStartState(),[]))  # anadimos el nodo inical a la frontera
    nodosCerrados = set()                        # creamos la estructura set para los nodos cerrados

    while not frontera.isEmpty():                # miramos si la frontera no esta vacia
        nodoActual, camino = frontera.pop()      # quitamos el nodo a tratar, el ultimo que ha entrado en este caso
        if problem.isGoalState(nodoActual):      # verificamos si es un nodo que pertenece al conjunto Sg (Goal)
            return camino                        # si es asi, enviamos la respuesta
        nodosCerrados.add(nodoActual)            # si no, lo agregamos a los nodos cerrados
        for hijo, direccion, coste in problem.getSuccessors(nodoActual):  # expandimos el nodo que acabamos de ver
            if hijo not in nodosCerrados:                                 # Loop detection, vemos si ya lo hemos visto
                frontera.push((hijo, camino + [direccion]))               # si no, lo agregamos a la frontera

    return []

    # util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    from util import Queue                      # utilizamos el EDA Queue para la implementacion de la frontera
    frontera = Queue()                          # es la frontera, esta vez es una cola
    frontera.push((problem.getStartState(), []))# anadimos el nodo inicial a la frontera
    nodosCerrados = set()                       # creamos la estructura para los nodos cerrados
    # nodosCerrados = set(problem.getStartState())

    while not frontera.isEmpty():               # vemos si la frontera esta vacia
        nodoActual, camino = frontera.pop()     # quitamos el nodo a tratar, el primero que ha entrado en este caso
        if problem.isGoalState(nodoActual):     # si el nodo es un estado que se corresponde a uno de Sg (Goal)
            return camino                       # retornamos como solucion el camino
        nodosCerrados.add(nodoActual)           # si no, lo agregamos a los nodos cerrados
        for hijo, direccion, coste in problem.getSuccessors(nodoActual):    # expandimos el nodo
            if hijo not in nodosCerrados:                                   # Loop detection, vemos si ya lo hemos visto
                nodosCerrados.add(hijo)                                     # si no esta dentro, lo agregamos a vistos
                frontera.push((hijo, camino[0:len(camino)] + [direccion]))  # si no esta, lo agregamos a la frontera
    return []

    # util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue

    frontera = PriorityQueue()                      # utilizamos el EDA que se corresponde al comportamiento de una cola de prioridad
    frontera.push((problem.getStartState(), []), 0) # anadimos el primer nodo a la frontera, al inicio tiene prioridad 0
    nodosCerrados = set()                           # creamos el set de los nodos cerrados

    while not frontera.isEmpty():                   # miramos si la frontera esta vacia
        nodoActual, camino = frontera.pop()         # extraemos el nodo a tratar
        if problem.isGoalState(nodoActual):         # si el nodo tiene un estado que esta dentro de Sg
            return camino                           # devolvemos la solucion
        if nodoActual not in nodosCerrados:         # Loop detection (1)
            nodosCerrados.add(nodoActual)           # agregamos el nodo actual a nodos cerrados
            for hijo, direccion, coste in problem.getSuccessors(nodoActual):    # expandimos el nodo cerrado
                if hijo not in nodosCerrados:                                   # Loop detection (2)
                    nuevocamino = camino + [direccion]                          # creamos el camino del hijo
                    frontera.push((hijo, nuevocamino), problem.getCostOfActions(nuevocamino)) # agregamos el hijo a la frontera
    return []

    # util.raiseNotDefined()

# (1) nos indica si ya hay un estado igual a el que queremos introducir, para evitar vueltas
# (2) evita las vueltas del hijo al padre
# como utilizamos una priority Queue no hace falta mirar en la frontera si ya existe el mismo en la frontera
# ya que la prioridad que utilizamos nos ahorra el trabajo de eliminar peores estados, porque siempre estaremos
# viendo primero los mejores estados

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
    # la implementacion del A* es similar al Uniform Cost Search, ya que Dijkstra no posee la heuristica
    # mas abajo, hemos implementado la funcion f(n) que en este caso, se corresponde a nuestra prioridad

    from util import PriorityQueue

    frontera = PriorityQueue()
    frontera.push((problem.getStartState(), []), 0)
    nodosCerrados = set()

    while not frontera.isEmpty():
        nodoActual, camino = frontera.pop()
        if problem.isGoalState(nodoActual):
            return camino
        if nodoActual not in nodosCerrados:
            nodosCerrados.add(nodoActual)
            for hijo, direccion, coste in problem.getSuccessors(nodoActual):
                if hijo not in nodosCerrados:
                    nuevocamino = camino + [direccion]
                    fn = problem.getCostOfActions(nuevocamino) + heuristic(hijo, problem)   # f(n) = g(n) + h(n)
                    frontera.push((hijo, nuevocamino), fn)
    return []

    # util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
