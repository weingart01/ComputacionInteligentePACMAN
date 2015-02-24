# valueIterationAgents.py
# -----------------------
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
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"

        for k in range(0,self.iterations):
            # creamos unos values auxiliares para no solapar los que
            # ya utilizamos para el computo
            new_values = util.Counter()
            # obtenemos los estados
            states = self.mdp.getStates()
            # para cada estado...
            for state in states:
                # si no es un estado final, por que no tiene acciones
                if not self.mdp.isTerminal(state):
                    # obtenemos las acciones
                    actions = self.mdp.getPossibleActions(state)
                    # iniciamos el value
                    value = float("-inf")
                    # para cada accion posible
                    for action in actions:
                        # obtenemos el mejor valor
                        value = max(value, self.computeQValueFromValues(state, action))
                    # una vez hemos dado con el mejor valor, lo guardamos en el auxiliar
                    # con el correspondiente a su estado (indice)
                    new_values[state] = value
            # una vez hemos obtenido todos los valores, actualizamos el diccionario original
            self.values = new_values

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        Qvalue = 0.0
        # aplicamos la formula iterativa que hemos visto en teoria - ValueIteration
        for next_state, probability in self.mdp.getTransitionStatesAndProbs(state,action):
            Qvalue += probability * (self.mdp.getReward(state,action,next_state) + self.discount * self.values[next_state])
        return Qvalue
        #util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        # si es terminal, retornamos Nada, por que no tiene acciones en el estado terminal
        if self.mdp.isTerminal(state):
            return None
        # sino
        else:
            # obtenemos las posibles acciones
            actions = self.mdp.getPossibleActions(state)
            # *** probar *** aseguramos que cualquier estado no terminal, tenga acciones
            if len(actions) == 0:
                return None
            else:
                # iniciamos el value
                Value = -float('inf')
                # iniciamos la politica
                policy = None
                for action in actions:
                    # obtenemos el Qvalue
                    Qvalue = self.computeQValueFromValues(state,action)
                    # si el Qvalue es mejor
                    if Qvalue > Value:
                        # guardamos el mejor qvalue que encontramos
                        Value = Qvalue
                        # agregamos la accion a la politica
                        policy = action
                # devolvemos la politica
                return policy

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
