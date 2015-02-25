# analysis.py
# -----------
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


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

def question2():
    # Al disminuir el answerNoise(alpha) el estado posee la politica posee la totalidad del valor del siguiente estado
    # sin ningun tipo de distorsion, asi pues tras 5 iteraciones al estado (1,1) le consta que se obtiene 
    # mejor puntuacion si la politica es east
    answerDiscount = 0.9
    answerNoise = 0.01
    return answerDiscount, answerNoise

# Segun regulamos los parametros nuestras politicas cambian...
# si aumentamos LivingReward premiamos la lejania 
# a las casillas mas lejanas por lo que si queremos usar el camino corto deberemos premiar negativamente para 
# que el recorrido sea proximo a los estados bahia(con la peor puntuacion).
# Como hemos dicho anteriormente la regulacion del ruido nos permite que los valores de los estados se propaguen mejor
# entonces contra mas bajo sea nos permitira dar antes con un posible estado lejano con mejor puntuacion
def question3a():
    answerDiscount = 0.8
    answerNoise = 0.2
    answerLivingReward = -1.1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3b():
    answerDiscount = 0.5
    answerNoise = 0.4
    answerLivingReward = -0.5
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3c():
    answerDiscount = 0.5
    answerNoise = 0.0
    answerLivingReward = -0.5
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3d():
    answerDiscount = 0.5
    answerNoise = 0.2
    answerLivingReward = 0.0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3e():
    answerDiscount = 0.0
    answerNoise = 0.0
    answerLivingReward = 0.5
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question6():
    answerEpsilon = None
    answerLearningRate = None
    return 'NOT POSSIBLE'
    # return answerEpsilon, answerLearningRate
    # If not possible,

if __name__ == '__main__':
    print 'Answers to analysis questions:'
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print '  Question %s:\t%s' % (q, str(response))
