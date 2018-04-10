# logicPlan.py
# ------------
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
In logicPlan.py, you will implement logic planning methods which are called by
Pacman agents (in logicAgents.py).
"""

import util
import sys
import logic
import game


pacman_str = 'P'
ghost_pos_str = 'G'
ghost_east_str = 'GE'
pacman_alive_str = 'PA'

class PlanningProblem:
    """
    This class outlines the structure of a planning problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the planning problem.
        """
        util.raiseNotDefined()

    def getGhostStartStates(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostPlanningProblem)
        """
        util.raiseNotDefined()

    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionPlanningProblem
        """
        util.raiseNotDefined()

def tinyMazePlan(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def sentence1():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.

    A or B
    (not A) if and only if ((not B) or C)
    (not A) or (not B) or C
    """
    "*** YOUR CODE HERE ***"
    A = logic.Expr("A")
    B = logic.Expr("B")
    C = logic.Expr("C")
    first = logic.disjoin(A, B)

    second = ( ~A ) % logic.disjoin(~B, C)
    third = logic.disjoin(~A, ~B, C)
    return logic.conjoin(first, second, third)

def sentence2():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.

    C if and only if (B or D)
    A implies ((not B) and (not D))
    (not (B and (not C))) implies A
    (not D) implies C
    """
    "*** YOUR CODE HERE ***"
    A = logic.Expr("A")
    B = logic.Expr("B")
    C = logic.Expr("C")
    D = logic.Expr("D")
    first = C % logic.disjoin(B, D)
    second = A >> logic.conjoin(~B, ~D)
    third = ~logic.conjoin(B, ~C) >> A
    fourth = ~D >> C
    return logic.conjoin(first, second, third, fourth)

def sentence3():
    """Using the symbols WumpusAlive[1], WumpusAlive[0], WumpusBorn[0], and WumpusKilled[0],
    created using the logic.PropSymbolExpr constructor, return a logic.PropSymbolExpr
    instance that encodes the following English sentences (in this order):

    (The Wumpus is alive at time 1)

    if and only if

    (
    (the Wumpus was alive at time 0)
    and
    (it was not killed at time 0)
    )

    or

    (
    (it was not alive at time 0)
    and
    (it was born at time 0)
    ).

    The Wumpus cannot both be alive at time 0 and be born at time 0.

    The Wumpus is born at time 0.
    """
    "*** YOUR CODE HERE ***"
    A = logic.PropSymbolExpr("WumpusAlive[1]")
    B = logic.PropSymbolExpr("WumpusAlive[0]")
    C = logic.PropSymbolExpr("WumpusKilled[0]")
    D = logic.PropSymbolExpr("WumpusBorn[0]")

    first = ( A ) % (logic.disjoin(logic.conjoin(B, ~C), logic.conjoin(~B, D)) )

    second = ~logic.conjoin(B, D)

    third = D


    return logic.conjoin(first, second, third)

def findModel(sentence):
    """Given a propositional logic sentence (i.e. a logic.Expr instance), returns a satisfying
    model if one exists. Otherwise, returns False.
    """
    "*** YOUR CODE HERE ***"
    cnf = logic.to_cnf(sentence)
    model = logic.pycoSAT(cnf)
    return model



def atLeastOne(literals) :
    """
    Given a list of logic.Expr literals (i.e. in the form A or ~A), return a single
    logic.Expr instance in CNF (conjunctive normal form) that represents the logic
    that at least one of the literals in the list is true.
    >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print logic.pl_true(atleast1,model1)
    False
    >>> model2 = {A:False, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    >>> model3 = {A:True, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    """
    "*** YOUR CODE HERE ***"
    return logic.disjoin(i for i in literals)


def atMostOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in
    CNF (conjunctive normal form) that represents the logic that at most one of
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"

    conjoinList = []
    for i in literals:
        for j in [l for l in literals if l != i]:
            # Appended pair is true iff i and j are both true
            conjoinList.append(logic.disjoin(~i, ~j))
    # In any pair of the literals, two cannot be both true
    return logic.conjoin(conjoinList)



def exactlyOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in
    CNF (conjunctive normal form)that represents the logic that exactly one of
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    return logic.conjoin(atLeastOne(literals), atMostOne(literals))

def extractActionSequence(model, actions):
    """
    Convert a model in to an ordered list of actions.
    model: Propositional logic model stored as a dictionary with keys being
    the symbol strings and values being Boolean: True or False
    Example:
    >>> model = {"North[3]":True, "P[3,4,1]":True, "P[3,3,1]":False, "West[1]":True, "GhostScary":True, "West[3]":False, "South[2]":True, "East[1]":False}
    >>> actions = ['North', 'South', 'East', 'West']
    >>> plan = extractActionSequence(model, actions)
    >>> print plan
    ['West', 'South', 'North']
    """
    "*** YOUR CODE HERE ***"
    messyList = []
    for key in model:
        # Add all the true action keys in model
        if model[key] is True:
             parsed = logic.PropSymbolExpr.parseExpr(key)
             if parsed[0] in actions:
                 messyList.append((parsed[0], int(parsed[1])))
    # And sort them basing on the time
    orderedList = sorted(messyList, key=lambda x: x[1])

    return [x[0] for x in orderedList]





def pacmanSuccessorStateAxioms(x, y, t, walls_grid):
    """
    Successor state axiom for state (x,y,t) (from t-1), given the board (as a
    grid representing the wall locations).
    Current <==> (previous position at time t-1) & (took action to move to x, y)
    """
    "*** YOUR CODE HERE ***"


    def noWallHere(coord):
        return not walls_grid[coord[0]][coord[1]]

    listPrev = []
    directions = ["East", "West", "South", "North"]
    at = [(x-1, y), (x+1, y), (x, y+1), (x, y-1)]
    for i in xrange(len(directions)):
        direc = directions[i]
        coord = at[i]
        if noWallHere(coord):
            prevAtHere = logic.PropSymbolExpr(pacman_str, coord[0], coord[1], t-1)
            prevGoThere = logic.PropSymbolExpr(direc, t-1)
            listPrev.append(logic.conjoin(prevAtHere, prevGoThere))

    pacmanNow = logic.PropSymbolExpr(pacman_str, x, y, t)

    return pacmanNow % logic.disjoin(i for i in listPrev)


def positionLogicPlan(problem):
    """
    Given an instance of a PositionPlanningProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()

    "*** YOUR CODE HERE ***"

    start = problem.getStartState()
    goal = problem.getGoalState()
    actions = [game.Directions.EAST, game.Directions.WEST, game.Directions.NORTH, game.Directions.SOUTH]



    # Start position expr
    KB = logic.PropSymbolExpr(pacman_str, start[0], start[1], 1)

    t = 1

    # Must be at start position when game starts
    for x in xrange(1, width + 1):
        for y in xrange(1, height + 1):
            if not walls[x][y] and (x, y) != start:
                notStartHere = ~logic.PropSymbolExpr(pacman_str, x, y, 1)
                KB = logic.conjoin(KB, notStartHere)

    while t <= 50:

        # One and only one action at one time
        currentActions = [logic.PropSymbolExpr(action, t) for action in actions]
        onlyAction = exactlyOne(currentActions)
        KB = logic.conjoin(KB, onlyAction)



        # For all the positions on the map
        for x in xrange(1, width + 1):
            for y in xrange(1, height + 1):

                # If no wall there
                if not walls[x][y]:

                    # Expr for pacman to be at this position at t+1
                    nextToGo = pacmanSuccessorStateAxioms(x, y, t + 1, walls)
                    KB = logic.conjoin(KB, nextToGo)

        # Expr for pacman to be at goal position at t+1
        goalProp = logic.PropSymbolExpr(pacman_str, goal[0], goal[1], t + 1)

        # The model to be solved
        modelToFind = logic.conjoin(KB, goalProp)

        solution = False
        solution = findModel(modelToFind)

        # Extract the sequence only when the solution is found
        if solution:
            return extractActionSequence(solution, actions)

        t += 1

    print "Error in positionLogicPlan"





def foodLogicPlan(problem):
    """
    Given an instance of a FoodPlanningProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()

    "*** YOUR CODE HERE ***"

    start, food = problem.getStartState()
    actions = [game.Directions.EAST, game.Directions.WEST, game.Directions.NORTH, game.Directions.SOUTH]


    # Start position expr
    pathKB = logic.PropSymbolExpr(pacman_str, start[0], start[1], 1)


    t = 1

    # Must be at start position when game starts
    for x in xrange(1, width + 1):
        for y in xrange(1, height + 1):
            if not walls[x][y] and (x, y) != start:
                notStartHere = ~logic.PropSymbolExpr(pacman_str, x, y, 1)
                pathKB = logic.conjoin(pathKB, notStartHere)

    while t <= 50:

        # For each step, foodKB does not necessarily base on the previous one
        foodKB = []
        eachFood = []

        # One and only one action at one time
        currentActions = [logic.PropSymbolExpr(action, t) for action in actions]
        onlyAction = exactlyOne(currentActions)
        pathKB = logic.conjoin(pathKB, onlyAction)


        # All the moves should be legal
        for x in xrange(1, width + 1):
            for y in xrange(1, height + 1):
                if not walls[x][y]:
                    nextToGo = pacmanSuccessorStateAxioms(x, y, t + 1, walls)
                    pathKB = logic.conjoin(pathKB, nextToGo)



        # onlyOnePos = []
        #
        # for x in xrange(1, width + 1):
        #     for y in xrange(1, height + 1):
        #         if not walls[x][y]:
        #             onlyOne = logic.PropSymbolExpr(pacman_str, x, y, t)
        #             onlyOnePos.append(onlyOne)
        #
        # KB = logic.conjoin(onlyOnePos)

        # Each food should be visited at least once in the past time
        for x in xrange(1, width + 1):
            for y in xrange(1, height + 1):
                if food[x][y]:
                    for timePassed in xrange(1, t+1):
                        oneFood = logic.PropSymbolExpr(pacman_str, x, y, timePassed)
                        eachFood.append(oneFood)

                    eachFoodVisited = atLeastOne(eachFood)

                    foodKB.append(eachFoodVisited)

                    # Flush the foods, because the next one would be different
                    eachFood = []

        foodKB = logic.conjoin(foodKB)
        combKB = logic.conjoin(foodKB, pathKB)

        solution = False


        solution = findModel(combKB)


        if solution:
            return extractActionSequence(solution, actions)

        t += 1



# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan

# Some for the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)
